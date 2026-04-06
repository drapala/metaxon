#!/usr/bin/env bash
# bradford-gate.sh — Hard enforcement for Bradford zone balance.
# Usage: bash scripts/bradford-gate.sh --stance <confirming|challenging|neutral>
# Exit 0: source is allowed to be ingested.
# Exit 1: source is BLOCKED (quota exceeded).
#
# Rule: if current challenging_ratio > 0.25 AND new source is "challenging" → BLOCK.
# Confirming and neutral sources always pass.

set -euo pipefail

STANCE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --stance) STANCE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [[ -z "$STANCE" ]]; then
  echo "Usage: bradford-gate.sh --stance <confirming|challenging|neutral>" >&2
  exit 2
fi

# Only challenging sources are subject to the gate
if [[ "$STANCE" != "challenging" ]]; then
  exit 0
fi

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="${PROJECT_ROOT}/wiki/_registry.md"

if [[ ! -f "$REGISTRY" ]]; then
  # No registry yet — allow
  exit 0
fi

# Count stances in registry (data rows only — skip header, separator, and wiki/concepts entries)
# wiki/concepts entries are synthesis/emergence articles, not raw sources — exclude them
TOTAL=$(grep -E '^\| raw/' "$REGISTRY" | grep -v "^| Path" | wc -l | tr -d ' ')
CHALLENGING=$(grep -E '^\| raw/' "$REGISTRY" | grep -c '| challenging |' || true)

if [[ "$TOTAL" -lt 5 ]]; then
  # Not enough data to enforce — allow
  exit 0
fi

# Calculate ratio if this new challenging source were added
NEW_CHALLENGING=$(( CHALLENGING + 1 ))
NEW_TOTAL=$(( TOTAL + 1 ))

RESULT=$(python3 -c "
challenging = $NEW_CHALLENGING
total = $NEW_TOTAL
ratio = challenging / total if total > 0 else 0
print(f'{ratio:.3f}')
print('BLOCK' if ratio > 0.25 else 'ALLOW')
")

RATIO=$(echo "$RESULT" | head -1)
DECISION=$(echo "$RESULT" | tail -1)

if [[ "$DECISION" == "BLOCK" ]]; then
  cat >&2 <<EOF
🚫 BRADFORD GATE — BLOQUEADO

  Quota de fontes challenging excedida.
  Atual: ${CHALLENGING}/${TOTAL} challenging ($(python3 -c "print(f'{$CHALLENGING/$TOTAL*100:.1f}%')"))
  Com esta fonte: ${NEW_CHALLENGING}/${NEW_TOTAL} challenging → ${RATIO} (limite: 0.25 / 25%)

  Esta fonte NÃO pode ser ingerida agora.
  Para prosseguir: ingira uma fonte confirming ou neutral primeiro para reequilibrar o corpus.
  Fonte pode ser salva em raw/ para ingestão futura.
EOF
  exit 1
fi

# ALLOW — print current stats to stderr for visibility
echo "✅ Bradford gate: OK — ${CHALLENGING}/${TOTAL} challenging ($(python3 -c "print(f'{$CHALLENGING/$TOTAL*100:.1f}%')")), projetado ${NEW_CHALLENGING}/${NEW_TOTAL} (${RATIO})" >&2
exit 0
