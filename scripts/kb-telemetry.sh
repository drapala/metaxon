#!/usr/bin/env bash
# kb-telemetry.sh — PostToolUse/PreToolUse hook: captures operational events to JSONL
#
# Events written: command_finished, state_written, article_written,
#                 friction_recorded, doc_opened
#
# Output: raw/meta/ops/events/YYYY-MM-DD.jsonl
# Each line is a JSON event (raw, no interpretation).

set -euo pipefail

INPUT=$(/bin/cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

[ -z "$FILE_PATH" ] && exit 0

PROJECT_ROOT="/Users/drapala/projects/llm-kb"
EVENTS_DIR="$PROJECT_ROOT/raw/meta/ops/events"
mkdir -p "$EVENTS_DIR"

DATE=$(date +%Y-%m-%d)
LOG_FILE="$EVENTS_DIR/$DATE.jsonl"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SESSION_ID=$(echo "$DATE-$$" | md5 | cut -c1-8)

# ── Classify event from file path ─────────────────────────────────────────────

EVENT_TYPE=""
SURFACE=""
SIGNAL=""

# Protocol/doc lookups → possible recall burden signal
case "$FILE_PATH" in
  *PROTOCOL.md|*PHILOSOPHY.md|*ONBOARDING.md|*QUARANTINE.md|*TROUBLESHOOTING.md)
    EVENT_TYPE="doc_opened"
    SURFACE="protocol-docs"
    SIGNAL="recall_burden_proxy"
    ;;
esac

# kb-state reads → state visibility check
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */outputs/state/kb-state.yaml)
      if [ "$TOOL" = "Read" ]; then
        EVENT_TYPE="state_read"
        SURFACE="kb-state"
        SIGNAL="state_lookup"
      else
        EVENT_TYPE="state_written"
        SURFACE="kb-state"
      fi
      ;;
  esac
fi

# Command completion markers (session logs)
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */logs/sessions/*/ingest-*)    EVENT_TYPE="command_finished"; SURFACE="ingest" ;;
    */logs/sessions/*/ask-*)       EVENT_TYPE="command_finished"; SURFACE="ask" ;;
    */logs/sessions/*/promote-*)   EVENT_TYPE="command_finished"; SURFACE="promote" ;;
    */logs/sessions/*/emerge-*)    EVENT_TYPE="command_finished"; SURFACE="emerge" ;;
    */logs/sessions/*/challenge-*) EVENT_TYPE="command_finished"; SURFACE="challenge" ;;
    */logs/sessions/*/review-*)    EVENT_TYPE="command_finished"; SURFACE="review" ;;
    */logs/sessions/*/scout-*)     EVENT_TYPE="command_finished"; SURFACE="scout" ;;
    */logs/sessions/*/dream-*)     EVENT_TYPE="command_finished"; SURFACE="dream" ;;
    */logs/sessions/*/retro-*)     EVENT_TYPE="command_finished"; SURFACE="retro" ;;
    */logs/sessions/*/friction-*)  EVENT_TYPE="command_finished"; SURFACE="friction" ;;
  esac
fi

# Article writes
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */wiki/concepts/*.md)
      EVENT_TYPE="article_written"; SURFACE="wiki"
      ;;
  esac
fi

# Friction events captured manually
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */raw/meta/ops/friction-*.md)
      EVENT_TYPE="friction_recorded"; SURFACE="meta"
      ;;
  esac
fi

[ -z "$EVENT_TYPE" ] && exit 0

# ── Write event ───────────────────────────────────────────────────────────────

FILE_BASENAME=$(basename "$FILE_PATH")

if [ -n "$SIGNAL" ]; then
  echo "{\"ts\":\"$TS\",\"event\":\"$EVENT_TYPE\",\"surface\":\"$SURFACE\",\"file\":\"$FILE_BASENAME\",\"signal\":\"$SIGNAL\",\"session\":\"$SESSION_ID\"}" >> "$LOG_FILE"
else
  echo "{\"ts\":\"$TS\",\"event\":\"$EVENT_TYPE\",\"surface\":\"$SURFACE\",\"file\":\"$FILE_BASENAME\",\"session\":\"$SESSION_ID\"}" >> "$LOG_FILE"
fi

exit 0
