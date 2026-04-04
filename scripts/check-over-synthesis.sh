#!/usr/bin/env bash
# check-over-synthesis.sh — PostToolUse hook for Write|Edit on wiki/concepts/*.md
# Checks if a wiki article has interpretation signals but no ## Interpretação section.
set -euo pipefail

INPUT=$(/bin/cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_response.filePath // empty')

# Only process wiki concept articles
[[ "$FILE_PATH" == */wiki/concepts/*.md || "$FILE_PATH" == wiki/concepts/*.md ]] || exit 0

# Resolve to absolute path if needed
if [ ! -f "$FILE_PATH" ]; then
  # Try from the project root
  PROJECT_ROOT="/Users/drapala/projects/llm-kb"
  FILE_PATH="${PROJECT_ROOT}/${FILE_PATH}"
  [ -f "$FILE_PATH" ] || exit 0
fi

HAS_INTERP=$(/usr/bin/grep -c '^## Interpreta' "$FILE_PATH" || true)
[ "$HAS_INTERP" -gt 0 ] && exit 0

INTERP_SIGNALS=$(/usr/bin/grep -c -E 'our interpretation|our synthesis|design analogy|therefore.*KB|maps to.*our|parallels.*our|resembles.*our|our speculative|our design' "$FILE_PATH" || true)

if [ "$INTERP_SIGNALS" -gt 2 ]; then
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Over-synthesis warning: $(basename "$FILE_PATH") has ${INTERP_SIGNALS} interpretation markers but no ## Interpretação section. Move interpretive claims to a separate section.\"}}"
fi
