---
title: "Foresight Pipeline Design"
sources:
  - path: wiki/concepts/scientific-research-programmes.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autonomous-emergence-pipeline-risks.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autoresearch-programme-vitality.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [meta-kb, foresight, strategy, conjecture, lifecycle, provenance]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: synthesis
synthesis_sources:
  - wiki/concepts/scientific-research-programmes.md
  - wiki/concepts/autonomous-emergence-pipeline-risks.md
  - wiki/concepts/autoresearch-programme-vitality.md
---

## Resumo

Hipóteses estratégicas emergem em conversa e somem se não capturadas estruturalmente. O `/foresight` é um pipeline para capturar, qualificar e integrar essas hipóteses à KB sem contaminar o corpus de artigos fundamentados em raw/. Quatro decisões de design não-triviais guiam a implementação: namespace separado, provenance tipo `conjecture`, restrições ao emerge_queue, e ciclo de vida por superação (não só refutação).

## Conteúdo

### Por que hipóteses estratégicas precisam de tratamento especial

Artigos `wiki/concepts/` têm um pressuposto implícito: derivam de fontes externas (`raw/`). O sistema de confiança — source_quality, interpretation_confidence, /challenge, Bradford tracking — pressupõe uma âncora externa. Hipóteses estratégicas violam esse pressuposto: emergem de raciocínio cross-domain do próprio compilador, não de fontes independentes.

Tratar hipóteses estratégicas como artigos normais introduz dois riscos:
1. **Falso positivo epistêmico:** /emerge pode conectar uma hipótese sem raw/ a um artigo promovido e o oracle confirmar um loop interno (o compilador conectando suas próprias hipóteses a si mesmo).
2. **Bradford contaminado:** stance `challenging` numa hipótese estratégica sem fonte externa não mede pressão epistêmica real.

### Q1 — Namespace: wiki/strategy/ vs wiki/concepts/

`wiki/strategy/` é o namespace correto para hipóteses estratégicas. Razões:

- **Não entra em _registry.md:** O registry rastreia fontes raw/ e seus derivados. Hipóteses estratégicas não têm fonte raw/ — incluí-las contaminaria Bradford tracking e stance_status.
- **Ciclo de vida diferente:** Artigos `wiki/concepts/` são demovidos por contradição evidencial. Hipóteses estratégicas podem ser *superadas sem serem refutadas* (a hipótese era válida, mas o contexto mudou ou uma implementação mais concreta a tornou redundante).
- **_index.md mantém ponteiro:** A presença no índice permite /ask acessar hipóteses como contexto, sem equipará-las epistemicamente a artigos promovidos.

(⚠️ nossa interpretação) O risco de contaminação Bradford é real: se stance `challenging` for atribuído a uma hipótese estratégica e entrar no registry, o gate 25% pode bloquear ingest legítimos por causa de pressão epistêmica artificial.

### Q2 — Provenance: conjecture

Campo `provenance: conjecture` marca o status epistêmico na origem, não como degradação. Campos obrigatórios:

```yaml
provenance: conjecture
epistemic_status: hypothesis  # hypothesis | speculative | working-assumption
testable_prediction: "..."    # falsificador explícito — sem isso, não é conjecture, é opinião
conjecture_trigger:
  session: outputs/logs/sessions/YYYY-MM-DD/foresight-HH-MM.md
  context: "..."              # o que estava sendo discutido quando a hipótese emergiu
conjectured_on: YYYY-MM-DD
lifecycle_state: active       # active | superseded | integrated | abandoned
```

`testable_prediction` é obrigatório. Sem um falsificador explícito, a hipótese não tem critério de promoção nem de demoção — fica como opinião não-falsificável, que o /challenge não pode processar. Isso aplica o critério de Popper diretamente na captura.

`epistemic_status` distingue gradações:
- `hypothesis`: tem mecanismo causal proposto + falsificador
- `speculative`: mecanismo proposto, sem falsificador claro ainda
- `working-assumption`: adotada pragmaticamente, não pela evidência (ex: "single-brain escala para multi-agent")

### Q3 — Restrições ao emerge_queue

O /emerge com hipóteses estratégicas tem regras assimétricas:

| Par | Permitido? | Razão |
|-----|-----------|-------|
| `[strategy/X] × [concepts/Y promovido]` | ✅ SIM | Y tem âncora raw/; oracle pode avaliar isomorfismo real |
| `[strategy/X] × [concepts/Y quarentena]` | ⚠️ CONDICIONAL | Apenas se Y já passou Gate 3; sinalizar `stability:tentative` |
| `[strategy/X] × [strategy/Y]` | ❌ NÃO | Dois sem âncora raw/ → oracle avalia hipóteses do compilador com hipóteses do compilador. Equivale ao circular oracle já documentado em `autonomous-emergence-pipeline-risks` |

(⚠️ nossa interpretação) A proibição `[strategy/X] × [strategy/Y]` deriva diretamente de [[autonomous-emergence-pipeline-risks]]: oracle co-gerado pelo mesmo sistema que gerou os inputs viola Systematicity. O resultado seria consenso espúrio, não emergência genuína.

### Q4 — Ciclo de vida: superação sem refutação

Artigos `wiki/concepts/` têm dois destinos: promovidos (ficam) ou demovidos (retirados por contradição). Hipóteses estratégicas precisam de um terceiro destino: **superadas sem serem refutadas**.

Estados de lifecycle:

```
active → superseded   # hipótese válida, mas mais concreta a tornou redundante
active → integrated   # hipótese foi absorvida por artigo wiki/concepts/ promovido
active → abandoned    # falsificador testado, hipótese falhou (equivale a demoção)
active → active       # hipótese sobreviveu a /challenge (raro — requer fonte externa)
```

`superseded` não é uma falha epistêmica — é maturação. A hipótese "KB precisa de sub-índices para escalar" é válida e correta, mas quando sub-índices forem implementados, ela vira `integrated` (absolvida pelo artigo de arquitetura resultante).

O critério de promoção de uma hipótese estratégica é diferente: não é `/challenge` que passa nos 3 critérios, mas sim:
1. Evidência externa independente confirma o mecanismo proposto (→ ingerir como artigo normal)
2. Implementação concreta valida a hipótese (→ `integrated`, ponteiro para o artefato)
3. O falsificador é testado e falha (→ `abandoned`)
4. Hipótese mais específica a absorve (→ `superseded`)

## Interpretação

(⚠️ nossa interpretação) O /foresight resolve um gap real: o sistema atual captura o que foi *descoberto* (via /ingest) e o que foi *sintetizado* (via /ask + /synthesize), mas não o que foi *hipotizado* em conversa. Hipóteses estratégicas são o estágio pré-raw/ do programa de pesquisa — análogas ao que Lakatos chamaria de heurística positiva: "o que devemos pesquisar a seguir."

A restrição `[strategy/X] × [strategy/Y]` no emerge_queue é o análogo epistêmico do safeguard de provenance documentado em `autonomous-emergence-pipeline-risks`: assim como /emerge sem raw/ gera "falso positivo composto via novos /emerges", /emerge de dois conjectures gera consenso circular.

`testable_prediction` obrigatório não é burocracia — é a diferença entre o sistema se auto-alimentar com hipóteses não-testáveis (degenerativo em Lakatos) e gerar demanda real por novos ingest (progressivo).

## Conexões

- depende-de: [[scientific-research-programmes]] ON "lifecycle states mapeiam para distinção progressivo/degenerativo de Lakatos; testable_prediction como critério de demarcação"
- depende-de: [[autonomous-emergence-pipeline-risks]] ON "restrição [strategy×strategy] no emerge_queue deriva diretamente do circular oracle risk"
- complementa: [[autoresearch-programme-vitality]] ON "foresight captura heurística positiva do programa; vitality mede se o programa está gerando predições novas (confirming_ratio)"
- instancia: [[falsificationism-demarcation]] ON "testable_prediction obrigatório aplica critério de demarcação Popper na captura de hipóteses"
- instancia: [[autonomous-kb-failure-modes]] ON "hipóteses sem raw/ sem restrição = failure mode 1 (convergência interna) via canal diferente"

## Fontes

- [[scientific-research-programmes]] — hard core/protective belt; progressivo/degenerativo; heurística positiva como direção de pesquisa
- [[autonomous-emergence-pipeline-risks]] — circular oracle; falso positivo composto; restrição provenance:emergence sem raw/
- [[autoresearch-programme-vitality]] — confirming_ratio; last_novel_prediction; distinção hard core / protective belt na KB
- [Sessão /ask foresight](../../outputs/logs/sessions/2026-04-05/ask-foresight-design.md) — sessão que originou as quatro decisões de design
