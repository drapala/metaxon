#!/usr/bin/env bash
# kb-telemetry.sh — PreToolUse + PostToolUse hook: captures operational events to JSONL
#
# Events: command_started, command_finished, state_read, state_written,
#         article_written, doc_opened, friction_recorded
#
# command_started: fires on PreToolUse when agent reads a command file
# command_finished: fires on PostToolUse when session log is written
# Together they enable: duration, abandonment detection, interrupted flows
#
# State surfaces: any file that acts as coordination state (not just kb-state.yaml)
# Extend STATE_SURFACES below as the system grows.
#
# Output: raw/meta/ops/events/YYYY-MM-DD.jsonl

set -euo pipefail

INPUT=$(/bin/cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")
HOOK_EVENT=$(echo "$INPUT" | jq -r '.hook_event // empty' 2>/dev/null || echo "")

[ -z "$FILE_PATH" ] && exit 0

PROJECT_ROOT="/Users/drapala/projects/llm-kb"
EVENTS_DIR="$PROJECT_ROOT/raw/meta/ops/events"
mkdir -p "$EVENTS_DIR"

DATE=$(date +%Y-%m-%d)
LOG_FILE="$EVENTS_DIR/$DATE.jsonl"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
# Stable session ID per shell PID — groups events from same invocation
SESSION_ID=$(echo "$DATE-$$" | md5 | cut -c1-8)

# ── State surfaces (extend as system grows) ────────────────────────────────────
# Any file that functions as coordination state, even if not named "state"
is_state_surface() {
  local f="$1"
  case "$f" in
    */outputs/state/kb-state.yaml) return 0 ;;
    */wiki/meta/system-map.md)     return 0 ;;
    */wiki/meta/friction-log.md)   return 0 ;;
    */wiki/_index.md)              return 0 ;;
    */wiki/_registry.md)           return 0 ;;
  esac
  return 1
}

# ── Classify event ─────────────────────────────────────────────────────────────

EVENT_TYPE=""
SURFACE=""
SIGNAL=""

# 1. command_started — PreToolUse on Read of a command file
#    This is the signal that a command is beginning execution
if [ "$HOOK_EVENT" = "PreToolUse" ] && [ "$TOOL" = "Read" ]; then
  case "$FILE_PATH" in
    */.claude/commands/ingest.md)    EVENT_TYPE="command_started"; SURFACE="ingest" ;;
    */.claude/commands/ask.md)       EVENT_TYPE="command_started"; SURFACE="ask" ;;
    */.claude/commands/promote.md)   EVENT_TYPE="command_started"; SURFACE="promote" ;;
    */.claude/commands/emerge.md)    EVENT_TYPE="command_started"; SURFACE="emerge" ;;
    */.claude/commands/challenge.md) EVENT_TYPE="command_started"; SURFACE="challenge" ;;
    */.claude/commands/review.md)    EVENT_TYPE="command_started"; SURFACE="review" ;;
    */.claude/commands/scout.md)     EVENT_TYPE="command_started"; SURFACE="scout" ;;
    */.claude/commands/synthesize.md) EVENT_TYPE="command_started"; SURFACE="synthesize" ;;
    */.claude/commands/dream.md)     EVENT_TYPE="command_started"; SURFACE="dream" ;;
    */.claude/commands/retro.md)     EVENT_TYPE="command_started"; SURFACE="retro" ;;
    */.claude/commands/friction.md)  EVENT_TYPE="command_started"; SURFACE="friction" ;;
    */.claude/commands/prioritize.md) EVENT_TYPE="command_started"; SURFACE="prioritize" ;;
    */.claude/commands/lint-epistemic.md) EVENT_TYPE="command_started"; SURFACE="lint-epistemic" ;;
    */.claude/commands/curate.md)    EVENT_TYPE="command_started"; SURFACE="curate" ;;
  esac
fi

# 2. Protocol/doc lookups — recall burden proxy
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    *PROTOCOL.md|*PHILOSOPHY.md|*ONBOARDING.md|*QUARANTINE.md|*TROUBLESHOOTING.md)
      EVENT_TYPE="doc_opened"
      SURFACE="protocol-docs"
      SIGNAL="recall_burden_proxy"
      ;;
  esac
fi

# 3. State surfaces — read or write
if [ -z "$EVENT_TYPE" ] && is_state_surface "$FILE_PATH"; then
  if [ "$TOOL" = "Read" ] || [ "$HOOK_EVENT" = "PreToolUse" ]; then
    EVENT_TYPE="state_read"
    SURFACE="state"
    SIGNAL="state_lookup"
  else
    EVENT_TYPE="state_written"
    SURFACE="state"
  fi
fi

# 4. command_finished — session log written
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */logs/sessions/*/ingest-*)     EVENT_TYPE="command_finished"; SURFACE="ingest" ;;
    */logs/sessions/*/ask-*)        EVENT_TYPE="command_finished"; SURFACE="ask" ;;
    */logs/sessions/*/promote-*)    EVENT_TYPE="command_finished"; SURFACE="promote" ;;
    */logs/sessions/*/emerge-*)     EVENT_TYPE="command_finished"; SURFACE="emerge" ;;
    */logs/sessions/*/challenge-*)  EVENT_TYPE="command_finished"; SURFACE="challenge" ;;
    */logs/sessions/*/review-*)     EVENT_TYPE="command_finished"; SURFACE="review" ;;
    */logs/sessions/*/scout-*)      EVENT_TYPE="command_finished"; SURFACE="scout" ;;
    */logs/sessions/*/dream-*)      EVENT_TYPE="command_finished"; SURFACE="dream" ;;
    */logs/sessions/*/retro-*)      EVENT_TYPE="command_finished"; SURFACE="retro" ;;
    */logs/sessions/*/friction-*)   EVENT_TYPE="command_finished"; SURFACE="friction" ;;
    */logs/sessions/*/synthesize-*) EVENT_TYPE="command_finished"; SURFACE="synthesize" ;;
  esac
fi

# 5. Article writes
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */wiki/concepts/*.md) EVENT_TYPE="article_written"; SURFACE="wiki" ;;
  esac
fi

# 6. Friction events
if [ -z "$EVENT_TYPE" ]; then
  case "$FILE_PATH" in
    */raw/meta/ops/friction-*.md) EVENT_TYPE="friction_recorded"; SURFACE="meta" ;;
  esac
fi

[ -z "$EVENT_TYPE" ] && exit 0

# ── Write event ────────────────────────────────────────────────────────────────

FILE_BASENAME=$(basename "$FILE_PATH")

if [ -n "$SIGNAL" ]; then
  printf '{"ts":"%s","event":"%s","surface":"%s","file":"%s","signal":"%s","session":"%s"}\n' \
    "$TS" "$EVENT_TYPE" "$SURFACE" "$FILE_BASENAME" "$SIGNAL" "$SESSION_ID" >> "$LOG_FILE"
else
  printf '{"ts":"%s","event":"%s","surface":"%s","file":"%s","session":"%s"}\n' \
    "$TS" "$EVENT_TYPE" "$SURFACE" "$FILE_BASENAME" "$SESSION_ID" >> "$LOG_FILE"
fi

exit 0
