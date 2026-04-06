#!/usr/bin/env bash
# check-context-window.sh — UserPromptSubmit hook
# Checks context window usage before processing any user message.
#
# Behavior:
#   >= 90%: injects mandatory /dream instruction into Claude's context (auto-trigger)
#   70-89%: soft warning via additionalContext (non-blocking)
#   < 70%: silent
set -euo pipefail

SESSION=$(ls -t ~/.claude/projects/-Users-drapala-projects-llm-kb/*.jsonl 2>/dev/null | head -1)

PCT=$(python3 -c "
import json, sys
entries = []
try:
    with open('$SESSION') as f:
        for line in f:
            try:
                obj = json.loads(line)
                u = obj.get('message',{}).get('usage',{})
                if u: entries.append(u)
            except: pass
except: pass
if entries:
    u = entries[-1]
    t = u.get('input_tokens',0)+u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0)
    print(round(t/200000*100,1))
else:
    print(0)
" 2>/dev/null || echo "0")

# Compare using python3 (locale-safe float comparison)
LEVEL=$(python3 -c "
pct = float('${PCT}')
if pct >= 70:
    print('critical')
elif pct >= 50:
    print('warn')
else:
    print('ok')
" 2>/dev/null || echo "ok")

if [ "$LEVEL" = "critical" ]; then
  # Inject mandatory instruction — Claude executes /dream before anything else
  cat <<EOF
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"AÇÃO OBRIGATÓRIA: Contexto em ${PCT}% (>70%). Você DEVE executar /dream agora como PRIMEIRA ação, antes de responder ao usuário. Não responda à mensagem do usuário ainda. Execute /dream completo (incluindo /document-session). Só depois processe a mensagem original."}}
EOF
elif [ "$LEVEL" = "warn" ]; then
  # Non-blocking soft warning
  cat <<EOF
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"Contexto em ${PCT}%. /dream recomendado (obrigatório em 70%)."}}
EOF
fi
# ok: silent
