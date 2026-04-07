# /algedonic — Canal Algedônico

Protocolo de distúrbio do sistema. Implementa o canal algedônico do VSM (Beer):
sinais que bypassam S3/S4 e chegam diretamente a S5 quando o sistema detecta
ameaça à viabilidade.

**Não é um command interativo** — é a especificação canônica do DisturbanceEvent
que outros commands emitem. Leia este arquivo antes de emitir qualquer evento.

---

## DisturbanceEvent — Schema Canônico

```yaml
id: <uuid gerado no momento da emissão>
ts: <ISO timestamp UTC — ex: 2026-04-06T14:32:00Z>
origin: session-start | dream | friction | kb-state-scan
type: retrieval_failure | l1_contradiction | quarantine_repeat |
      cross_session_drift | gate_failure | quarantine_stale
severity: medium | high | critical   # SEMPRE derivada — nunca aceita como input
evidence: []                         # lista de slugs de artigos ou paths de sessões
bypass_s3: false                     # true = escala direto para S5 sem passar por S3/S4
resolved: false
resolved_at: null
```

---

## Regras de Severidade (derivação obrigatória)

| type + condição               | severity | bypass_s3 |
|-------------------------------|----------|-----------|
| retrieval_failure (1 artigo)  | medium   | false     |
| retrieval_failure (3+ artigos)| high     | true      |
| l1_contradiction              | high     | true      |
| quarantine_repeat             | high     | true      |
| cross_session_drift           | critical | true      |
| gate_failure                  | critical | true      |
| quarantine_stale > 24h        | medium   | false     |

**Invariante:** severity é sempre calculada aqui. Qualquer comando que tente
passar `severity` como parâmetro deve ser ignorado — derive pelas regras acima.

---

## Ações por Severity

### medium
1. Append evento em `algedonic_events` em `outputs/state/kb-state.yaml`

### high
1. Append evento em `algedonic_events`
2. Cria `outputs/inbox/algedonic-YYYYMMDD-HHMMSS.md` com o evento em YAML

### critical
1. Append evento em `algedonic_events`
2. Cria `outputs/inbox/algedonic-YYYYMMDD-HHMMSS.md`
3. Atualiza `system_state: degraded` em `outputs/state/kb-state.yaml`

---

## Como Emitir um DisturbanceEvent

**Usa `yq` para preservar comentários no kb-state.yaml.** Não usar yaml.dump
(destrói comentários no round-trip).

Execute este script Python:

```python
import uuid, datetime, json, subprocess
from pathlib import Path

# ── 1. Configurar ────────────────────────────────────────────────────────────
TYPE     = "quarantine_stale"   # substituir pelo type correto
ORIGIN   = "kb-state-scan"      # substituir pelo origin correto
EVIDENCE = ["artigo-slug"]       # substituir pela evidência real

# Derivar severity e bypass_s3 pelas regras canônicas
RULES = {
    "retrieval_failure_single": ("medium",   False),
    "retrieval_failure_multi":  ("high",     True),
    "l1_contradiction":         ("high",     True),
    "quarantine_repeat":        ("high",     True),
    "cross_session_drift":      ("critical", True),
    "gate_failure":             ("critical", True),
    "quarantine_stale":         ("medium",   False),
}
severity, bypass_s3 = RULES[TYPE]

ts_now  = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
ts_file = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")

event = {
    "id":          str(uuid.uuid4()),
    "ts":          ts_now,
    "origin":      ORIGIN,
    "type":        TYPE,
    "severity":    severity,
    "evidence":    EVIDENCE,
    "bypass_s3":   bypass_s3,
    "resolved":    False,
    "resolved_at": None,
}

# ── 2. Append em kb-state.yaml via yq (preserva comentários) ─────────────────
event_json = json.dumps(event)
subprocess.run(
    ["yq", "-i", f".algedonic_events += [{event_json}]", "outputs/state/kb-state.yaml"],
    check=True
)

# ── 3. Ação por severity ─────────────────────────────────────────────────────
if severity in ("high", "critical"):
    inbox = Path("outputs/inbox")
    inbox.mkdir(exist_ok=True)
    lines = "\n".join(f"  {k}: {json.dumps(v)}" for k, v in event.items())
    (inbox / f"algedonic-{ts_file}.md").write_text(
        f"# DisturbanceEvent — {TYPE}\n\n```yaml\n{lines}\n```\n"
    )

if severity == "critical":
    subprocess.run(
        ["yq", "-i", '.system_state = "degraded"', "outputs/state/kb-state.yaml"],
        check=True
    )

print(f"DisturbanceEvent emitido: {TYPE} / {severity} / bypass_s3={bypass_s3}")
```

---

## Scan de Quarantine Stale (origin: kb-state-scan)

Executado pelo session-start hook como parte do Check 1.
Detecta artigos em quarentena que satisfazem critérios de promoção mas
permaneceram estagnados por > 24h.

**Condição de emissão:**
- Artigo com `quarantine: true`
- `quarantine_created` (ou data de criação) + 24h < agora
- Todos os critérios de promoção satisfeitos (tempo ✓, review_frio ✓, critério 3 ✓)
- Não existe evento `resolved: false` com o mesmo artigo em `evidence` e `type: quarantine_stale`

Se condição satisfeita → emite DisturbanceEvent `type: quarantine_stale`, `origin: kb-state-scan`.

---

## Invariantes do Sistema

1. **severity é sempre derivada** — nunca aceita como input externo
2. **critical nunca auto-resolve** — `resolved: true` exige ação explícita do humano
3. **algedonic_events é append-only** — nunca deletar eventos; marcar `resolved: true` ao fechar
4. **bypass_s3: true** significa sinal que escala direto para S5 sem passar por S3/S4
5. **Idempotência de scan** — verificar existência de evento não-resolvido antes de emitir novo

---

## Resolução de Eventos

Para fechar um evento (após ação corretiva):

```yaml
# Em kb-state.yaml, localizar pelo id:
- id: <uuid>
  ...
  resolved: true
  resolved_at: "YYYY-MM-DDTHH:MM:SSZ"
```

- `medium` e `high`: podem ser auto-resolvidos pelo command após ação corretiva verificada
- `critical`: **somente resolução manual pelo humano**

Após resolver todos os eventos `critical` e `high`, atualizar `system_state: healthy`.
