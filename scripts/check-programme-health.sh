#!/usr/bin/env bash
# check-programme-health.sh — PostToolUse hook for Write on wiki/concepts/*.md
# Triggered after a new wiki article is written (final step of /ingest).
# Reads kb-state.yaml → programme_health.confirming_ratio.
# If ratio > 0.8 AND window >= 10: warns that KB is in Lakatos degenerative zone.
set -euo pipefail

INPUT=$(/bin/cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_response.filePath // empty')

# Only fire on new wiki concept articles (final step of /ingest)
[[ "$FILE_PATH" == */wiki/concepts/*.md || "$FILE_PATH" == wiki/concepts/*.md ]] || exit 0

PROJECT_ROOT="/Users/drapala/projects/llm-kb"
KB_STATE="${PROJECT_ROOT}/outputs/state/kb-state.yaml"

[ -f "$KB_STATE" ] || exit 0

# Read programme_health fields using yq
# Graceful fallback if fields don't exist yet
RATIO=$(yq '.programme_health.confirming_ratio.ratio // 0' "$KB_STATE" 2>/dev/null || echo "0")
WINDOW=$(yq '.programme_health.confirming_ratio.window // 0' "$KB_STATE" 2>/dev/null || echo "0")
CONFIRMING=$(yq '.programme_health.confirming_ratio.confirming // 0' "$KB_STATE" 2>/dev/null || echo "0")

# Float comparison via python3 (locale-safe)
IS_DEGENERATIVE=$(python3 -c "
ratio = float('${RATIO}')
window = int('${WINDOW}'.split('.')[0])
print('yes' if ratio > 0.80 and window >= 10 else 'no')
" 2>/dev/null || echo "no")

if [ "$IS_DEGENERATIVE" = "yes" ]; then
  ARTICLE=$(basename "$FILE_PATH" .md)
  cat <<EOF
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"⚠️ LAKATOS WARNING — KB em zona degenerativa. Últimos ${WINDOW} ingest: ${CONFIRMING}/${WINDOW} confirming (ratio ${RATIO}). O artigo '${ARTICLE}' é confirming ou gera predição nova? Se confirming, rode /challenge antes de /ingest para verificar se já existe evidência suficiente. Para continuar mesmo assim, classifique explicitamente no kb-state.yaml antes de prosseguir."}}
EOF
fi
