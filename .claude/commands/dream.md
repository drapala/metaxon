# /dream

Wrapper local do skill global /dream. Adiciona logging de contexto e atualização de kb-state.yaml.

## Passo 1 — Captura contexto antes

Execute e guarde o resultado:

```bash
SESSION=$(ls -t ~/.claude/projects/-Users-drapala-projects-llm-kb/*.jsonl 2>/dev/null | head -1)
python3 -c "
import json
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
    print('n/a')
"
```

Guarda este valor como `CONTEXT_BEFORE`.

## Passo 2 — Executa /dream global

Invoque o skill global `/dream` (`.claude/skills/dream/SKILL.md`).
Siga todas as instruções do skill normalmente.

## Passo 3 — Atualiza kb-state.yaml

Após o /dream completar, atualize `outputs/state/kb-state.yaml`:

```yaml
updated: YYYY-MM-DD
fast_cycle:
  sessions_since_last_dream: 0  # reset
slow_cycle:
  dream:
    last_run: YYYY-MM-DD
    context_before_pct: [CONTEXT_BEFORE]
    triggered_by: context | manual | session_count
    # context = disparado pelo check de uso >= 70%
    # manual = usuário rodou explicitamente
    # session_count = sessions_since_last_dream atingiu threshold
```

Salve também em `outputs/logs/sessions/YYYY-MM-DD/dream-HH-MM.md`:
```markdown
---
date: YYYY-MM-DD
context_before_dream: [CONTEXT_BEFORE]%
triggered_by: [motivo]
---

[resumo do que foi consolidado — copiado do output do skill global]
```

## Passo 4 — Verifica e reporta

Imprima ao final:
```
/dream completo.
Contexto antes: [CONTEXT_BEFORE]%
Trigger: [motivo]
```

## Passo 5 — Invoca /document-session

Imediatamente após o Passo 4, execute o comando `/document-session`.
Não espere instrução do usuário — faz parte do ciclo /dream.

## Quando rodar

- Quando session-start reportar 🔴 (contexto >= 70%)
- Quando usuário chamar explicitamente
- Quando `fast_cycle.sessions_since_last_dream >= 3` em kb-state.yaml

---

## Após /dream completar

Atualize `outputs/state/kb-state.yaml`:
1. `sessions_since_last_dream: 0` ← reset
2. `last_updated` com data atual
