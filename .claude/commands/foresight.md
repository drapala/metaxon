# /foresight

Captura hipóteses estratégicas emergentes e as integra ao pipeline da KB.

## Quando usar

Use /foresight quando:
- Uma hipótese arquitetural surge em conversa e seria perdida no chat
- Uma conexão cross-domain ainda não tem evidência externa suficiente para /ingest
- Um "e se..." com consequências de design precisa ser preservado para teste futuro

NÃO use /foresight para:
- Artigos com fonte raw/ disponível → use /ingest
- Conexões já com evidência → use /synthesize ou /ask
- Reflexões puramente operacionais sem testable_prediction

---

## Processo

### 1. Elicitar a hipótese

Se o usuário deu a hipótese diretamente, extraia os campos abaixo. Se a hipótese está implícita na conversa, pergunte:

- "Qual é o mecanismo proposto? (não só o que acontece, mas por quê)"
- "O que seria necessário para essa hipótese ser falsa?"
- "Qual o horizonte — isso é relevante por semanas, meses, ou enquanto o sistema existir?"

### 2. Preencher o template

```yaml
title: "..."
hypothesis: "..."           # 1-2 frases; afirmação positiva testável
premises:
  - "..."                   # o que precisa ser verdade para a hipótese funcionar
architectural_consequences:
  - "..."                   # o que mudaria no design se a hipótese for confirmada
testable_prediction: "..."  # falsificador explícito: "Se X, então Y mensurável"
horizon: weeks | months | persistent
epistemic_status: hypothesis | speculative | working-assumption
```

**Regra:** Se não conseguir preencher `testable_prediction`, classifique como `epistemic_status: speculative` e sinalize ao usuário: "Esta hipótese ainda não tem falsificador — registrada como especulativa. Deseja refinar antes?"

### 3. Criar artigo em wiki/strategy/

Nome do arquivo: `wiki/strategy/SLUG.md` (kebab-case da hipótese)

Template de artigo:

```markdown
---
title: "..."
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [strategy, ...]
source_quality: low          # sem raw/ = sempre low
interpretation_confidence: low
provenance: conjecture
epistemic_status: hypothesis | speculative | working-assumption
testable_prediction: "..."
conjecture_trigger:
  session: outputs/logs/sessions/YYYY-MM-DD/foresight-HH-MM.md
  context: "..."
conjectured_on: YYYY-MM-DD
lifecycle_state: active
---

## Hipótese

[1-2 frases]

## Premissas

- [o que precisa ser verdade]

## Mecanismo proposto

[por que isso funcionaria — causalidade, não correlação]

## Consequências arquiteturais

- [o que muda no design se confirmado]

## Predição testável

[falsificador explícito]

## Conexões tentativas

- [conceito relacionado que poderia confirmar ou refutar]

## Histórico

- [YYYY-MM-DD] — hipótese capturada em [contexto]
```

### 4. Atualizar _index.md

Adicione ponteiro em `wiki/_index.md`:

```
- [Título](strategy/SLUG.md) — ⚠️ CONJECTURE. [1 linha descrevendo a hipótese e o falsificador]
```

**Não adicionar ao _registry.md** — hipóteses estratégicas não têm fonte raw/ e não participam do Bradford tracking.

### 5. Avaliar elegibilidade para emerge_queue

Verifique se a hipótese tem par legítimo no emerge_queue:

| Condição | Ação |
|----------|------|
| Par `[strategy/X] × [concepts/Y promovido]` | ✅ Adicionar ao emerge_queue em kb-state.yaml |
| Par `[strategy/X] × [concepts/Y quarentena]` | ⚠️ Adicionar com flag `stability:tentative` |
| Par `[strategy/X] × [strategy/Y]` | ❌ Proibido — dois sem raw/ = oracle circular |

Se elegível, adicione ao emerge_queue:
```yaml
emerge_queue:
  - pair: [strategy/SLUG, concepts/ARTIGO-PROMOVIDO]
    stability: tentative  # se Y em quarentena
    added_by: foresight
    added_on: YYYY-MM-DD
```

### 6. Salvar log

Salve log em `outputs/logs/sessions/YYYY-MM-DD/foresight-HH-MM.md`:

```markdown
---
session_id: YYYY-MM-DD-HH-MM
type: foresight
---

## Hipótese capturada

[título]

## Campos

hypothesis: ...
testable_prediction: ...
epistemic_status: ...

## Arquivo criado

wiki/strategy/SLUG.md

## emerge_queue

[adicionado / não elegível / motivo]
```

---

## Ciclo de vida — quando encerrar uma hipótese

| Evento | lifecycle_state | Ação |
|--------|----------------|------|
| Evidência externa confirma mecanismo | → ingerir como artigo normal | `integrated` — ponteiro para novo artigo |
| Implementação valida a hipótese | → artefato criado | `integrated` — ponteiro para o artefato |
| Falsificador testado, hipótese falhou | → equivale a demoção | `abandoned` — registrar por que falhou |
| Hipótese mais específica a absorve | → maturação normal | `superseded` — ponteiro para hipótese sucessora |
| Contexto mudou, hipótese obsoleta | → revisão explícita | `superseded` ou `abandoned` com nota |

Para atualizar lifecycle:
1. Altere `lifecycle_state` no frontmatter do artigo
2. Adicione entrada em `## Histórico` com data e motivo
3. Se `integrated`: atualize o artigo absorvente com ponteiro de volta
4. Se no emerge_queue: remova o par

---

## Restrições epistêmicas

- **Sem raw/ → source_quality: low sempre.** Mesmo se a hipótese for brilhante.
- **testable_prediction é obrigatório para `epistemic_status: hypothesis`.** Sem falsificador = `speculative`.
- **Não usar /challenge em hipóteses estratégicas sem fonte raw/** — /challenge pressupõe base evidencial para confrontar.
- **[strategy/X] × [strategy/Y] no emerge_queue = proibido.** Oracle avaliaria hipóteses do compilador contra hipóteses do compilador — circular oracle documentado em `autonomous-emergence-pipeline-risks`.
- **Bradford tracking não inclui wiki/strategy/**. Stance não se aplica a conjectures.

---

## Output

```
FORESIGHT — HIPÓTESE CAPTURADA
Arquivo: wiki/strategy/SLUG.md
epistemic_status: [hypothesis|speculative|working-assumption]
testable_prediction: [falsificador]
emerge_queue: [adicionado com par X×Y | não elegível — motivo]
lifecycle_state: active
```
