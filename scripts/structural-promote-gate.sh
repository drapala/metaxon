#!/usr/bin/env bash
# structural-promote-gate.sh — Gate 2 of kb-auto-promote-protocol
# Runs 6 structural checks on a wiki article.
# Usage: ./structural-promote-gate.sh wiki/concepts/article.md
# Exit 0: all checks passed (eligible for cross-model challenge)
# Exit 1: one or more checks failed (quarantine with reasons)
# Stdout: JSON with check results
set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo '{"error":"file not found","file":"'"$FILE"'"}' >&2
  exit 2
fi

PROJECT_ROOT="/Users/drapala/projects/llm-kb"
ABS_FILE="$FILE"
if [ ! -f "$ABS_FILE" ]; then
  ABS_FILE="${PROJECT_ROOT}/${FILE}"
fi
[ -f "$ABS_FILE" ] || { echo '{"error":"file not found"}' >&2; exit 2; }

ARTICLE=$(basename "$ABS_FILE" .md)
FAILURES=()
WARNINGS=()

# Parse frontmatter via python3 (locale-safe, handles YAML quirks)
read_frontmatter() {
  python3 - "$ABS_FILE" "$1" "$2" <<'PYEOF'
import sys, re
filepath, field, default = sys.argv[1], sys.argv[2], sys.argv[3]
content = open(filepath).read()
m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if not m:
    print(default); sys.exit(0)
fm = m.group(1)
for line in fm.splitlines():
    if line.startswith(field + ':'):
        val = line[len(field)+1:].strip().strip('"').strip("'")
        print(val if val else default); sys.exit(0)
print(default)
PYEOF
}

PROVENANCE=$(read_frontmatter "provenance" "source")
SQ=$(read_frontmatter "source_quality" "unknown")
IC=$(read_frontmatter "interpretation_confidence" "unknown")

# ── Check 1: Claims have citations to raw/ ──────────────────────────────────
# A source article should have at least 1 link to ../../raw/
# synthesis/emergence articles reference wiki/ — skip raw check for those
if [ "$PROVENANCE" = "source" ]; then
  RAW_LINKS=$(/usr/bin/grep -c '\.\./\.\./raw/' "$ABS_FILE" 2>/dev/null || true)
  if [ "$RAW_LINKS" -eq 0 ]; then
    FAILURES+=("check1_no_raw_citations:source article has no links to raw/ — claims unverifiable")
  fi
fi

# ── Check 2: ⚠️ markers present when ## Interpretação section exists ────────
HAS_INTERP=$(/usr/bin/grep -c '^## Interpreta' "$ABS_FILE" 2>/dev/null || true)
if [ "$HAS_INTERP" -gt 0 ]; then
  MARKERS=$(/usr/bin/grep -c '⚠️' "$ABS_FILE" 2>/dev/null || true)
  if [ "$MARKERS" -eq 0 ]; then
    FAILURES+=("check2_missing_markers:## Interpretação exists but no ⚠️ markers found — interpretive claims unmarked")
  fi
fi

# ── Check 3: ## Interpretação and ## Conteúdo are separate sections ──────────
CONTEUDO_LINE=$(/usr/bin/grep -n '^## Conteúdo' "$ABS_FILE" 2>/dev/null | head -1 | cut -d: -f1 | tr -d '[:space:]' || true)
INTERP_LINE=$(/usr/bin/grep -n '^## Interpreta' "$ABS_FILE" 2>/dev/null | head -1 | cut -d: -f1 | tr -d '[:space:]' || true)
CONTEUDO_LINE="${CONTEUDO_LINE:-0}"
INTERP_LINE="${INTERP_LINE:-0}"

if [ "$CONTEUDO_LINE" -gt 0 ] && [ "$INTERP_LINE" -gt 0 ]; then
  # Check that ## Interpretação comes AFTER ## Conteúdo
  if [ "$INTERP_LINE" -le "$CONTEUDO_LINE" ]; then
    FAILURES+=("check3_sections_out_of_order:## Interpretação (line $INTERP_LINE) appears before ## Conteúdo (line $CONTEUDO_LINE)")
  fi
elif [ "$CONTEUDO_LINE" -eq 0 ] && [ "$PROVENANCE" = "source" ]; then
  WARNINGS+=("check3_missing_conteudo:source article has no ## Conteúdo section")
fi

# ── Check 4: Wikilinks are typed ────────────────────────────────────────────
# Count total [[wikilinks]] and typed links (word: [[link]])
TOTAL_WIKILINKS=$(/usr/bin/grep -oE '\[\[[a-z][a-z0-9-]*\]\]' "$ABS_FILE" 2>/dev/null | wc -l | tr -d '[:space:]' || true)
TYPED_WIKILINKS=$(/usr/bin/grep -oE '(contradicts|instancia|emerge-de|emerge-para|validates|complementa|derivedFrom|partOf|formalizado-por|testado-por|complementsAt|depende-de|implica-em):[[:space:]]*\[\[' "$ABS_FILE" 2>/dev/null | wc -l | tr -d '[:space:]' || true)
TOTAL_WIKILINKS="${TOTAL_WIKILINKS:-0}"
TYPED_WIKILINKS="${TYPED_WIKILINKS:-0}"

if [ "$TOTAL_WIKILINKS" -gt 2 ] && [ "$TYPED_WIKILINKS" -eq 0 ]; then
  FAILURES+=("check4_untyped_wikilinks:${TOTAL_WIKILINKS} wikilinks found but 0 are typed — add relation types (contradicts, instancia, emerge-de, etc.)")
fi

# ── Check 5: Predição falsificável present for emergence articles ───────────
if [ "$PROVENANCE" = "emergence" ]; then
  HAS_PRED=$(/usr/bin/grep -c '^## Pred' "$ABS_FILE" 2>/dev/null || true)
  HAS_PRED="${HAS_PRED:-0}"
  if [ "$HAS_PRED" -eq 0 ]; then
    FAILURES+=("check5_missing_prediction:emergence article has no ## Predição falsificável section — required for quarantine promotion")
  fi
fi

# ── Check 6: source_quality + interpretation_confidence coherence ────────────
if [ "$SQ" = "low" ]; then
  FAILURES+=("check6_low_source_quality:source_quality=low — no primary or secondary sources; auto-promote ineligible")
fi

if [ "$SQ" = "high" ] && [ "$IC" = "low" ]; then
  WARNINGS+=("check6_coherence_flag:source_quality=high but interpretation_confidence=low — mark with ⚠️ and verify claims")
fi

# ── Build JSON output ────────────────────────────────────────────────────────
PASS=$([ ${#FAILURES[@]} -eq 0 ] && echo "true" || echo "false")

FAILURES_JSON="["
for i in "${!FAILURES[@]}"; do
  [ $i -gt 0 ] && FAILURES_JSON+=","
  FAILURES_JSON+="\"${FAILURES[$i]}\""
done
FAILURES_JSON+="]"

WARNINGS_JSON="["
for i in "${!WARNINGS[@]}"; do
  [ $i -gt 0 ] && WARNINGS_JSON+=","
  WARNINGS_JSON+="\"${WARNINGS[$i]}\""
done
WARNINGS_JSON+="]"

cat <<EOF
{
  "article": "${ARTICLE}",
  "provenance": "${PROVENANCE}",
  "source_quality": "${SQ}",
  "interpretation_confidence": "${IC}",
  "pass": ${PASS},
  "failures": ${FAILURES_JSON},
  "warnings": ${WARNINGS_JSON},
  "checks_run": 6
}
EOF

[ "$PASS" = "true" ] && exit 0 || exit 1
