# /dream

Wrapper local do skill global /dream. Adiciona logging de contexto e atualização de kb-state.yaml.

## Fase 0 — INCOMPLETE SCAN

Execute antes de qualquer outra coisa. Identifica artigos incompletos e prioriza por impacto no retrieval.

### 0.1 — Detecta stubs

Um artigo é **incompleto** se qualquer um for verdadeiro:
- `## Conteúdo` ausente ou com < 50 palavras (proxy de stub — artigos bem escritos têm ≥ 100 palavras)
- Status no registry é `stub-wiki`

**Nota:** artigos usam prosa OU bullet points em `## Conteúdo`. Contar bullets é errado — conta palavras.

Rode via python3:

```python
import re
from pathlib import Path
from collections import Counter

wiki_dir = Path("wiki/concepts")
articles = [f for f in wiki_dir.glob("*.md") if not f.stem.startswith("_")]

# In-degree via wikilinks
in_degree = Counter()
reads_map = {}
for f in articles:
    text = f.read_text()
    for link in re.findall(r'\[\[([^\]|#]+)', text):
        in_degree[link.strip().lower().replace(' ', '-')] += 1
    m = re.search(r'^reads:\s*(\d+)', text, re.MULTILINE)
    reads_map[f.stem] = int(m.group(1)) if m else 0

STUB_THRESHOLD = 50  # palavras

stubs = []
for f in articles:
    text = f.read_text()
    conteudo = re.search(r'^## Conteúdo\s*\n(.*?)(?=^## |\Z)', text, re.DOTALL | re.MULTILINE)
    word_count = len(conteudo.group(1).split()) if conteudo else 0
    if word_count >= STUB_THRESHOLD:
        continue
    deg = in_degree.get(f.stem, 0)
    reads = reads_map.get(f.stem, 0)
    priority = deg * 2 + reads
    stubs.append({"stem": f.stem, "in_degree": deg, "reads": reads,
                  "priority": priority, "words": word_count})

stubs.sort(key=lambda x: x["priority"], reverse=True)
print(f"Stubs found: {len(stubs)}")
for s in stubs[:10]:
    print(f"  priority={s['priority']:3d} deg={s['in_degree']:2d} reads={s['reads']} words={s['words']:3d}  {s['stem']}")
```

### 0.2 — Classifica por elegibilidade Option B

Para cada stub, verifica critérios de auto-complete seguro:

| Critério | Check |
|----------|-------|
| `in_degree < 5` | Não é hub crítico |
| Nenhum artigo L1 depende exclusivamente dele | Grep por wikilinks em artigos L1 do hard_core |
| `epistemic_status: L0` ou ausente (stub nunca avaliado) | Frontmatter |
| Tem pelo menos 1 fonte raw/ no frontmatter | Pode ser completado com evidência real |

Artigos que passam em **todos** os critérios → **Option B eligible** (auto-complete).
Demais → apenas registrados na fila para completude manual.

### 0.3 — Escreve fila em kb-state.yaml

```yaml
stub_completion_queue:
  updated: YYYY-MM-DD
  total_stubs: N
  top5:
    - stem: artigo-X
      in_degree: N
      reads: N
      completion_priority: N
      option_b_eligible: true|false
      ineligibility_reason: null | "in_degree >= 5" | "L1 dependency" | "sem fontes"
```

### 0.4 — Auto-complete (Option B eligible apenas)

Para cada artigo Option B eligible (máximo 3 por /dream para limitar blast radius):

**a) Lê fontes**
- Extrai `sources[].path` do frontmatter
- Lê cada source file em raw/
- Extrai claims factuais (números, resultados, descrições de arquitetura)

**b) Preenche `## Conteúdo`**
- Escreve 3-6 bullet points com claims diretos das fontes
- Cada claim rastreável a uma source específica
- NÃO preenche `## Interpretação` — deixa vazia (artigo puramente factual é o objetivo)
- Atualiza `updated: YYYY-MM-DD` no frontmatter
- Remove `epistemic_status: L0` do frontmatter se presente

**c) Challenge externo**
Chama GPT-4o e Gemini sobre os claims preenchidos:

> "Este artigo sobre [título] afirma: [claims]. Avalie cada claim como VÁLIDO, INCERTO ou INVÁLIDO com justificativa em 1 frase. Responda em JSON: {claims: [{text, verdict, justification}]}"

- Se GPT E Gemini retornam todos VÁLIDO ou INCERTO: artigo aprovado
- Se qualquer INVÁLIDO de qualquer modelo: marca para revisão humana, não aplica

**d) Resultado**
- Aprovado: `quarantine: false`, `challenge_type: auto-complete`
  Registra em `completion_tracking` no kb-state.yaml:
  ```yaml
  completion_tracking:
    article-slug:
      completed_at: YYYY-MM-DD
      completion_method: auto
      reads_before: N        # lido do frontmatter agora
      reads_after_7d: null   # Fase 0.5 preenche depois de 7 dias
      retrieval_confirmed: false
  ```
- Reprovado: mantém stub, anota razão em kb-state.yaml para revisão humana

---

## Fase 0.5 — RETRIEVAL VALIDATION

Roda após Fase 0. Valida se artigos auto-completados estão sendo recuperados pelo retrieval.

### Lógica

Usa **logs de sessão como fonte primária** — mais robusto que `reads` no frontmatter
(que depende do utility-tracker ser executado). Logs são append-only e não dependem
de nenhum hook.

```python
import re, datetime, glob
from pathlib import Path
import yaml

today = datetime.date.today()
wiki_dir = Path("wiki/concepts")
logs_dir = Path("outputs/logs/sessions")

kb = yaml.safe_load(Path("outputs/state/kb-state.yaml").read_text())
tracking = kb.get("completion_tracking", {})

to_review = []
confirmed = []

for article_id, meta in tracking.items():
    if meta.get("retrieval_confirmed"):
        continue

    completed_at = datetime.date.fromisoformat(str(meta["completed_at"]))
    age_days = (today - completed_at).days
    if age_days < 7:
        continue

    # Fonte primária: contagem de menções em logs de sessão após completed_at
    mention_count = 0
    for log_path in sorted(logs_dir.rglob("*.md")):
        # Extrai data do caminho (outputs/logs/sessions/YYYY-MM-DD/...)
        try:
            log_date = datetime.date.fromisoformat(log_path.parts[-2])
        except ValueError:
            continue
        if log_date <= completed_at:
            continue
        if article_id in log_path.read_text():
            mention_count += 1

    # Fallback: delta de reads no frontmatter
    article_path = wiki_dir / f"{article_id}.md"
    reads_delta = 0
    if article_path.exists():
        m = re.search(r'^reads:\s*(\d+)', article_path.read_text(), re.MULTILINE)
        reads_now = int(m.group(1)) if m else 0
        reads_delta = reads_now - meta.get("reads_before", 0)

    retrieved = mention_count > 0 or reads_delta > 0

    if retrieved:
        confirmed.append({"id": article_id, "mentions": mention_count, "reads_delta": reads_delta})
    else:
        to_review.append({"id": article_id, "age_days": age_days, "reason": "não recuperado"})

print(f"Retrieval confirmed: {len(confirmed)}")
for c in confirmed:
    print(f"  ✓ {c['id']} (logs={c['mentions']}, reads+{c['reads_delta']})")
print(f"Fila de revisão: {len(to_review)}")
for r in to_review:
    print(f"  ✗ {r['id']} — {r['age_days']}d sem aparição em logs")
```

### Atualiza kb-state.yaml

Para artigos confirmados:
```yaml
completion_tracking:
  article-slug:
    retrieval_confirmed: true
    reads_after_7d: N
```

Para artigos não recuperados: adiciona à `stub_completion_queue` com motivo `retrieval_failure` — mesmo fluxo de revisão dos stubs normais.

---

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

## Passo 1.5 — Executa Fase 0

Execute a Fase 0 completa (seções 0.1 a 0.4) antes de invocar o skill global.
A fila `stub_completion_queue` deve estar gravada em kb-state.yaml antes do Passo 2.

## Passo 2 — Executa /dream global

Invoque o skill global `/dream` (`.claude/skills/dream/SKILL.md`).
Siga todas as instruções do skill normalmente.
O skill global tem seu próprio INVENTORY — a Fase 0 complementa, não substitui.

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

## Passo 4.5 — Fase X: COST REPORT

Leia `outputs/reports/skill-usage.jsonl`. Filtre registros do dia atual (campo `ts` começa com hoje YYYY-MM-DD). Se não houver registros, pule silenciosamente.

Se houver registros insuficientes via hook (< 3 entradas), execute primeiro:

```bash
source .venv/bin/activate
python3 scripts/parse-session-logs.py --date $(date +%Y-%m-%d)
```

Depois releia o JSONL.

### Tabela 1 — Custo por skill

Agrupe por `skill`. Para cada skill:

| skill | calls | input_tokens | output_tokens | cost_usd | p50_duration_ms |
|---|---|---|---|---|---|

`p50_duration_ms`: mediana dos `duration_ms` não-zero. Se todos zero (hook não capturou timing), omitir coluna.

### Tabela 2 — Capital allocation (custo por resultado)

Cruza registros de skill-usage.jsonl com os logs da sessão do dia para contar outcomes:

| métrica | count | custo_total_usd | custo_médio_usd |
|---|---|---|---|
| artigos promovidos | N | X | X |
| challenges válidos (outcome=APPROVED ou verdict=PUBLICÁVEL) | N | X | X |
| patches auto-aplicados | N | X | X |
| retrievals confirmados (completion_tracking) | N | X | X |
| oracles concordantes (oracle.agreement=true) | N | X | X |
| oracles em SPLIT (oracle.agreement=false) | N | X | X |

Para counts: leia kb-state.yaml (`challenge.challenged_since_last_promote`, `completion_tracking`) e session logs do dia.

### Tabela 3 — Custo oracle vs. Claude

Agrupe registros com `oracle != null`:

| model | calls | cost_usd | agreement_rate |
|---|---|---|---|

Linha final: `total_oracle_cost_usd / total_claude_cost_usd = ratio` — mede quanto do orçamento vai para validação externa.

### Linha final

```
Custo total da sessão: $X.XXXX
Oracle ratio: XX% (validação externa / custo Claude)
```

### Salva relatório

Escreva em `outputs/reports/pipeline-cost-YYYY-MM-DD.md`:

```markdown
---
date: YYYY-MM-DD
total_cost_usd: X.XXXX
oracle_ratio: X.XX
---

## Custo por Skill
[tabela 1]

## Capital Allocation
[tabela 2]

## Custo Oracle
[tabela 3]

## Total
Custo total: $X.XXXX | Oracle ratio: XX%
```

---

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
