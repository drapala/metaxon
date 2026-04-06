#!/usr/bin/env bash
# paper-quality-gate.sh — External quality signal via Semantic Scholar API.
# Usage: bash scripts/paper-quality-gate.sh --arxiv <arXiv-ID> [--min-citations N]
#
# Given an arXiv ID, queries Semantic Scholar for citation count and venue.
# Returns:
#   eligible: true  — paper meets quality threshold (citable venue OR citation count)
#   eligible: false — paper is unverified (low citations, unknown venue, preprint-only)
#
# Thresholds (defaults):
#   --min-citations 10  (papers with 0 citations are treated as unverified)
#   Venues: ICLR, NeurIPS, ICML, ACL, EMNLP, JMLR, AAAI, CVPR, ICCV, ECCV, KDD, WWW,
#           SIGMOD, VLDB, ICSE, FSE, SOSP, OSDI, SIGCOMM, UAI, AISTATS, CoRL
#
# Exit codes:
#   0 — eligible: true (safe to auto-ingest)
#   1 — eligible: false (send to ingest_queue with unverified: true)
#   2 — usage error or API unavailable (treat as unverified)
#
# Env var: SEMANTIC_SCHOLAR_API_KEY (optional — raises rate limit from 100/5min to 1/s)

set -euo pipefail

ARXIV_ID=""
MIN_CITATIONS=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --arxiv) ARXIV_ID="$2"; shift 2 ;;
    --min-citations) MIN_CITATIONS="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$ARXIV_ID" ]]; then
  echo "Usage: paper-quality-gate.sh --arxiv <arXiv-ID> [--min-citations N]" >&2
  exit 2
fi

# Strip "arXiv:" prefix if user included it
ARXIV_ID="${ARXIV_ID#arXiv:}"
ARXIV_ID="${ARXIV_ID#arxiv:}"

# Known high-quality venues (case-insensitive substring match)
QUALITY_VENUES=(
  "NeurIPS" "Neural Information Processing"
  "ICLR" "International Conference on Learning Representations"
  "ICML" "International Conference on Machine Learning"
  "ACL" "Association for Computational Linguistics"
  "EMNLP"
  "NAACL"
  "JMLR" "Journal of Machine Learning Research"
  "AAAI"
  "CVPR" "ICCV" "ECCV"
  "KDD" "WWW"
  "SIGMOD" "VLDB"
  "ICSE" "FSE"
  "SOSP" "OSDI"
  "SIGCOMM"
  "UAI" "AISTATS" "CoRL"
  "Science" "Nature" "Cell"
)

# Build API URL
API_URL="https://api.semanticscholar.org/graph/v1/paper/arXiv:${ARXIV_ID}"
FIELDS="title,citationCount,venue,year,publicationVenue,isOpenAccess,externalIds"

# Set auth header if API key provided
AUTH_HEADER=""
if [[ -n "${SEMANTIC_SCHOLAR_API_KEY:-}" ]]; then
  AUTH_HEADER="x-api-key: ${SEMANTIC_SCHOLAR_API_KEY}"
fi

# Query API (curl is more reliable in scripts; xh for interactive use)
CURL_ARGS=(-s --max-time 10)
if [[ -n "${SEMANTIC_SCHOLAR_API_KEY:-}" ]]; then
  CURL_ARGS+=(-H "x-api-key: ${SEMANTIC_SCHOLAR_API_KEY}")
fi

# Retry up to 3 times with backoff (handles transient 429)
RESPONSE=""
for attempt in 1 2 3; do
  RESPONSE=$(curl "${CURL_ARGS[@]}" "${API_URL}?fields=${FIELDS}" 2>/dev/null) || RESPONSE=""
  if [[ -n "$RESPONSE" ]]; then
    # Check if it's a 429 and we should retry
    IS_429=$(echo "$RESPONSE" | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    print('yes' if d.get('code','') == '429' else 'no')
except:
    print('no')
" 2>/dev/null || echo "no")
    if [[ "$IS_429" == "no" || "$attempt" -eq 3 ]]; then
      break
    fi
    echo "⚠️  Rate limited (attempt ${attempt}/3), waiting ${attempt}s..." >&2
    sleep "$attempt"
  fi
done

if [[ -z "$RESPONSE" ]]; then
  echo "⚠️  Semantic Scholar API unavailable — treating as unverified" >&2
  echo "eligible: false"
  echo "reason: api_unavailable"
  exit 1
fi

# Check for error/rate-limit response
ERROR=$(echo "$RESPONSE" | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    if 'error' in d or 'code' in d:
        print(d.get('message','error'))
    else:
        print('ok')
except:
    print('parse_error')
" 2>/dev/null || echo "parse_error")

if [[ "$ERROR" != "ok" ]]; then
  if echo "$ERROR" | grep -qi "429\|too many\|rate"; then
    echo "⚠️  Rate limited by Semantic Scholar API. Set SEMANTIC_SCHOLAR_API_KEY for higher limits." >&2
    echo "eligible: false"
    echo "reason: rate_limited"
  elif echo "$ERROR" | grep -qi "not found\|404"; then
    echo "⚠️  Paper not found in Semantic Scholar: arXiv:${ARXIV_ID}" >&2
    echo "eligible: false"
    echo "reason: not_found"
  else
    echo "⚠️  API error: ${ERROR}" >&2
    echo "eligible: false"
    echo "reason: api_error"
  fi
  exit 1
fi

# Parse fields
CITATION_COUNT=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('citationCount', 0))")
VENUE=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('venue', '') or '')")
TITLE=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title', 'Unknown'))")
YEAR=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('year', 'Unknown'))")
PUB_VENUE_NAME=$(echo "$RESPONSE" | python3 -c "
import sys,json
d=json.load(sys.stdin)
pv=d.get('publicationVenue') or {}
print(pv.get('name','') or '')
" 2>/dev/null || echo "")

# Check venue quality
VENUE_MATCH=""
for V in "${QUALITY_VENUES[@]}"; do
  if echo "${VENUE}${PUB_VENUE_NAME}" | grep -qi "$V" 2>/dev/null; then
    VENUE_MATCH="$V"
    break
  fi
done

# Decision logic
ELIGIBLE="false"
REASON=""

if [[ -n "$VENUE_MATCH" ]]; then
  ELIGIBLE="true"
  REASON="venue:${VENUE_MATCH}"
elif [[ "$CITATION_COUNT" -ge "$MIN_CITATIONS" ]]; then
  ELIGIBLE="true"
  REASON="citations:${CITATION_COUNT}"
else
  ELIGIBLE="false"
  if [[ "$CITATION_COUNT" -eq 0 ]]; then
    REASON="no_citations_no_venue"
  else
    REASON="low_citations:${CITATION_COUNT}/${MIN_CITATIONS}_required"
  fi
fi

# Output
echo "---"
echo "arxiv_id: ${ARXIV_ID}"
echo "title: \"${TITLE}\""
echo "year: ${YEAR}"
echo "venue: \"${VENUE:-unknown}\""
echo "citation_count: ${CITATION_COUNT}"
echo "eligible: ${ELIGIBLE}"
echo "reason: ${REASON}"
echo "---"

if [[ "$ELIGIBLE" == "true" ]]; then
  echo "✅ Quality gate PASSED — eligible for auto-ingest" >&2
  exit 0
else
  echo "🚫 Quality gate FAILED — add to ingest_queue with unverified: true" >&2
  exit 1
fi
