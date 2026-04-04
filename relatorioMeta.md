# Relatório Meta: Claims Pré-2024 com Risco de Obsolescência

date: 2026-04-04
query: "Quais claims da KB dependem de papers publicados antes de 2024 e têm maior probabilidade de terem sido superados por trabalho posterior?"
confidence: média (análise interna, sem web search de verificação)

---

## Fontes Pré-2024 na KB (9 papers computacionais)

| Fonte | Data | Claims que fundamenta |
|-------|------|----------------------|
| LMs Know What They Know | 2022-07 | "Mostly calibrated, fails on hard" |
| Socratic Prompting | 2023-02 | 6 Socratic techniques for LLMs |
| Reflexion | 2023-03 | 91% HumanEval, 52% sem testes, +8pp verbal |
| Multiagent Debate | 2023-05 | Multi-LLM debate melhora factuality |
| Model Collapse | 2023-05 | "Tails disappear" em self-consumption |
| CoALA | 2023-09 | Cognitive architecture framework |
| Promptbreeder | 2023-09 | Self-referential prompt evolution |
| MemGPT | 2023-10 | Virtual context management, FIFO eviction |
| Self-RAG | 2023-10 | Structured reflection tokens |

Nota: fontes de epistemologia (Popper 1934, Lakatos 1970, Simon 1956, Pearl 2018) e ontologia (BFO, DOLCE, OWL, Noy) NÃO envelhecem da mesma forma — são frameworks teóricos, não benchmarks. Excluídas desta análise.

---

## RISCO ALTO — Claims provavelmente superados

### 1. Reflexion: "91% pass@1 no HumanEval" (2023-03)

**O claim:** Reflexion com GPT-4 atinge 91% no HumanEval, superando GPT-4 baseline (80.1%).

**Por que provavelmente superado:**
- HumanEval é um benchmark de 2021 com 164 problemas. Em 2026, modelos frontier provavelmente excedem 91% SEM Reflexion — o delta que Reflexion adicionava (80→91) pode ter sido absorvido pelo modelo base.
- O claim importa para a KB não pelo número absoluto (91%) mas pelo MECANISMO (verbal reflection + testes = melhoria). O mecanismo pode continuar válido mesmo que o benchmark esteja saturado.
- Verificado em raw/: 91% confirmado no paper. Mas "surpassing GPT-4" refere-se ao GPT-4 de 2023, não ao GPT-4o/4.1 de 2025-2026.

**Impacto na KB:** Alto — Reflexion é citada em 5+ artigos como evidência de que verbal reflection funciona. Se o delta verbal diminuiu em modelos mais novos (porque o baseline subiu), a magnitude do efeito que a KB cita está inflada.

**Pearl level:** O mecanismo (L2: ablation mostra que testes importam) provavelmente sobrevive. O número (L1: 91% neste benchmark) provavelmente não.

**Ação:** /scout por "Reflexion 2025 2026" para verificar se o mecanismo foi replicado em modelos mais recentes.

### 2. MemGPT: Virtual context management com FIFO (2023-10)

**O claim:** MemGPT usa hierarchical tiers com FIFO eviction + memory pressure warnings como paradigma de agent memory.

**Por que provavelmente superado:**
- MemGPT evoluiu pra **Letta** (o próprio raw/ documenta isso). A KB cita MemGPT como arquitetura fundacional, mas Letta formalizou e refinou os 4 blocos.
- Context windows cresceram dramaticamente (8K → 128K → 1M+). A motivação original de MemGPT ("context windows are too small") é menos premente com modelos de 200K-1M tokens.
- Hindsight (2025, 83.6% LongMemEval com 20B), Zep (2025, 94.8% DMR), e A-MEM (2025) SUPERAM MemGPT em benchmarks modernos. O artigo agent-memory-architectures já documenta isso.
- Synapse (2026) SUPERA MemGPT explicitamente no LoCoMo (40.5 vs 28.0 F1).

**Impacto na KB:** Médio — a KB já tem 7 patterns mais recentes em agent-memory-architectures. MemGPT é histórico, não current SOTA. Mas o artigo context-management ainda usa MemGPT como referência principal para virtual context — deveria referenciar os sucessores.

**Pearl level:** O paradigma (tiered memory) sobrevive em todos os sucessores. Os números específicos de MemGPT (benchmarks com GPT-4-turbo 2023) estão obsoletos.

**Ação:** Qualificar MemGPT como "foundational (2023), superseded by Letta, Hindsight, Zep, A-MEM" nos artigos que o citam.

### 3. LMs Know What They Know: "Mostly calibrated" (2022-07)

**O claim:** Larger models show good calibration. Models can estimate P(True) and P(IK). Calibration breaks down on unfamiliar tasks.

**Por que possivelmente superado:**
- Testado em modelos até 2022 (GPT-3, early GPT-4). Modelos 2025-2026 (GPT-4.1, Claude Opus, Gemini) podem ter calibração diferente (melhor ou pior).
- JudgeBench (2024-2025) já complementa: "GPT-4o near random on hard tasks." Mas JudgeBench testa AVALIAÇÃO, não calibração de conhecimento próprio.
- A tensão "mostly calibrated vs near random" documentada em llm-as-judge pode ter resolução diferente com modelos mais recentes.

**Impacto na KB:** Médio — a tensão está documentada como difficulty-contingent ("calibrado em fácil, falha em difícil"). Essa resolução provavelmente sobrevive mesmo com modelos novos, porque é estrutural (fácil = in-distribution, difícil = out-of-distribution).

**Pearl level:** O padrão (L1: calibration degrades with difficulty) provavelmente é robusto. Os números específicos (r=0.78-0.81 consistency on wrong answers, testado em 26 modelos de 2022) podem ter mudado.

**Ação:** Baixo urgência. O padrão qualitativo provavelmente se mantém.

---

## RISCO MÉDIO — Claims possivelmente complementados

### 4. Model Collapse: "Tails disappear" (2023-05, publicado Nature 2024)

**Status:** O paper foi publicado na Nature em 2024 — revisado por pares, robusto. O mecanismo (recursive self-consumption) é formal e independente de modelo específico. Provavelmente ROBUSTO, mas com nuances:
- Paper posterior (2024): "Is Model Collapse Inevitable?" mostra que mistura de dados reais+sintéticos previne collapse. Nossa KB já documenta essa mitigação.
- A aplicação de model collapse a KBs (nossa interpretação) permanece não testada.

### 5. Multiagent Debate: "Melhora factuality" (2023-05)

**Status:** Multi-agent approaches evoluíram muito desde 2023. O claim específico (debate melhora factuality) provavelmente se mantém, mas o landscape de multi-agent é muito mais sofisticado agora (AgentRxiv, AI Scientist, OpenResearcher, coordinator mode do Claude Code).

### 6. CoALA: Cognitive architecture framework (2023-09)

**Status:** Framework conceitual, não benchmark. A taxonomia (working/episodic/semantic/procedural) é de ciência cognitiva, não de ML — não "envelhece" como benchmarks. A Memory Survey (2025, 47 authors) propõe taxonomia diferente (forms/functions/dynamics) que complementa mas não invalida CoALA.

### 7. Self-RAG: Reflection tokens (2023-10)

**Status:** O conceito de reflection tokens ([Retrieve], [IsRel], [IsSup], [IsUse]) provavelmente foi absorvido por frameworks mais recentes. O claim no wiki (Section em retrieval-augmented-generation) é usado como inspiração para /ask checkpoints, não como SOTA.

### 8. Promptbreeder: Self-referential improvement (2023-09)

**Status:** O conceito (evolve both task prompts AND mutation prompts) é citado na KB como "Fase 3 potential" — nunca como claim factual. Baixo risco de obsolescência porque nunca foi claim central.

---

## RISCO BAIXO — Claims provavelmente robustos

### 9. Socratic Prompting (2023-02)

**Status:** Framework de técnicas (definition, elenchus, dialectic, maieutics, generalization, counterfactual). São técnicas milenares aplicadas a LLMs — não envelhecem.

---

## Resumo de Ações

| Prioridade | Fonte | Ação |
|-----------|-------|------|
| ALTA | Reflexion (2023) | /scout por replicação em modelos 2025-2026. Verificar se delta verbal se mantém. |
| ALTA | MemGPT (2023) | Qualificar como "foundational, superseded" nos artigos que citam. |
| MÉDIA | LMs Know (2022) | Verificar se calibration pattern se mantém com modelos 2025-2026. |
| BAIXA | Model Collapse, CoALA, Multiagent Debate, Self-RAG, Promptbreeder, Socratic | Monitorar, não agir agora. |

## Padrão Geral

A KB tem uma **assimetria temporal**: papers de MECANISMO (como Reflexion funciona, como Model Collapse funciona) envelhecem mais devagar que papers de BENCHMARK (91% no HumanEval, 28.0 F1 no LoCoMo). 

A KB deveria distinguir:
- **Claims de mecanismo** (L2): "verbal reflection + testes = melhoria" — provavelmente robusto
- **Claims de benchmark** (L1): "91% no HumanEval com GPT-4" — provavelmente obsoleto

O Quality Gate CHECK 2 (instance→class) já captura parcialmente isso. Mas deveria haver um CHECK adicional: **temporal freshness** — quando o número foi medido, com qual modelo, e se o benchmark está saturado.

---

**Fontes wiki:** [[self-improving-agents]], [[agent-memory-architectures]], [[llm-as-judge]], [[causal-reasoning-pearl]], [[retrieval-augmented-generation]]

**Fontes raw verificadas:**
- [Reflexion](raw/papers/reflexion-verbal-reinforcement-learning.md) — 91%, 52%, +8pp confirmados
- [MemGPT](raw/papers/memgpt-llms-as-operating-systems.md) — FIFO, Letta evolution confirmados
- [LMs Know](raw/papers/lm-know-what-they-know.md) — "mostly", r=0.78-0.81 confirmados

**Confiança:** média — análise de obsolescência sem verificação via web search (não busquei se Reflexion foi replicado em 2025-2026, apenas inferi probabilidade)

**Gaps:**
- Nenhuma verificação de "Reflexion 2025 2026" feita — /scout necessário
- Nenhuma verificação de benchmarks atuais de HumanEval — saturação provável mas não confirmada

---

# Relatório Meta: Single Point of Failure Analysis

date: 2026-04-04
query: "Qual artigo tem maior risco de ser single point of failure — erro factual propagando via wikilinks?"
confidence: alta (dados empíricos do grafo)

---

## Metodologia

**Risco de propagação = inbound links × confidence risk**

- Inbound links = quantos artigos DEPENDEM deste (citam via wikilink)
- Confidence risk = probabilidade de conter erro:
  - high confidence = 1 (menor risco)
  - medium confidence = 2
  - low confidence = 3

**Score = inbound × confidence_risk.** Maior score = maior risco de propagação.

## Ranking Completo

| Rank | Artigo | Inbound | Confidence | Score | Risco |
|------|--------|---------|-----------|-------|-------|
| **1** | **kb-architecture-patterns** | **13** | **medium (2)** | **26** | **CRÍTICO** |
| 2 | tension-resolution | 9 | medium (2) | 18 | Alto |
| 3 | self-improving-agents | 11 | high (1) | 11 | Alto |
| 4 | agent-memory-architectures | 7 | medium (2) | 14 | Alto |
| 5 | reflexion-weighted-knowledge-graphs | 7 | low (3) | 21 | Alto |
| 6 | autonomous-kb-failure-modes | 6 | medium (2) | 12 | Alto |
| 7 | context-management | 10 | high (1) | 10 | Médio |
| 8 | memory-consolidation | 9 | high (1) | 9 | Médio |
| 9 | retrieval-augmented-generation | 7 | high (1) | 7 | Médio |
| 10 | hybrid-search | 8 | medium (2) | 16 | Alto |
| 11 | llm-knowledge-base | 6 | medium (2) | 12 | Médio |
| 12 | raptor-vs-flat-retrieval | 5 | medium (2) | 10 | Médio |
| 13 | llm-as-judge | 6 | high (1) | 6 | Baixo |
| 14 | autonomous-research-agents | 6 | medium (2) | 12 | Médio |
| 15 | multi-agent-orchestration | 3 | high (1) | 3 | Baixo |
| 16 | question-taxonomy | 2 | medium (2) | 4 | Baixo |
| 17-21 | (5 artigos com 1 inbound) | 1 | varies | 1-3 | Mínimo |

## Análise dos Top 3

### #1 — kb-architecture-patterns (Score: 26) — SINGLE POINT OF FAILURE

**13 artigos dependem deste.** É o hub central da KB. Qualquer erro aqui propaga pra 62% do wiki.

**Erros que propagariam:**
- "Pattern 4 é uma arquitetura" → na verdade é um role/meta-pattern. Se citado como arquitetura por 13 artigos downstream, todos herdam a confusão categorial.
- Scale thresholds extrapolados (~200 artigos) → apresentados como se fossem empiricos. 13 artigos podem referenciá-los como fato.
- "ERL validates concept articles" → ERL testou em Gaia2 (agent tasks), não em KBs. Se downstream cita como "validação", over-synthesis propaga.

**Status:** Resumo já foi calibrado (commit 6ce0c32: "OUR TAXONOMY, Pattern 4 is role, thresholds extrapolated"). Mas o CORPO do artigo ainda tem interpretações no Conteúdo.

**Mitigação:** Este artigo deveria ser o primeiro a ter typed wikilinks completos e ## Interpretação totalmente separada. Qualquer erro aqui tem 13x amplification factor.

### #2 — reflexion-weighted-knowledge-graphs (Score: 21) — SPECULATIVE HUB

**7 artigos dependem + confidence LOW.** O score é alto porque baixa confiança × muitos dependentes = alto risco de propagar especulação como fato.

**Erros que propagariam:**
- "Edge weight modification via verbal feedback" → conceito especulativo não implementado. Se citado como mecanismo por downstream, vira claim L1 apresentado como L2.
- "Credit assignment unsolved" → agora parcialmente superado por immune-inspired-credit-assignment (CLONALG dissolve o problema).
- Prior work subsume 80%+ do que RWKG propunha (Hindsight, Zep, AriGraph, RMM, AIS).

**Status:** Resumo já diz "speculative synthesis, partially subsumed." Prior work section extensiva. Mas é o artigo mais citado com interpretation_confidence:low — structurally risky.

**Mitigação:** Considerar rebaixar para "historical synthesis" ou mover claims não-subsumed pra immune-inspired-credit-assignment. O valor remanescente do RWKG é a NARRATIVA de como chegamos lá, não o mecanismo proposto.

### #3 — self-improving-agents (Score: 11) — BENCHMARK PROPAGATION VECTOR

**11 artigos dependem + confidence HIGH.** Score menor que os acima, mas este é o artigo que propaga números de benchmark (91% HumanEval, 52% sem testes, +8pp verbal, -1.9% trajectories, 40-60 ERL threshold).

**Erros que propagariam:**
- "91% HumanEval" com GPT-4 de 2023 → provavelmente obsoleto (benchmark saturado com modelos 2026). Se 11 artigos citam como evidência de que verbal reflection funciona, citam um número que pode não representar o delta real em modelos atuais.
- "16.1% self-enhancement bias" (de llm-as-judge via self-improving-agents) → Qwen2-specific. Se propagado sem qualifier a 11 artigos downstream, inflaciona o risco percebido.
- "+8pp verbal over episodic" → dado de 1 benchmark (HumanEval), 1 modelo (GPT-4 2023). Se propagado como "verbal contribui ~8pp em geral", over-generaliza.

**Status:** interpretation_confidence:high — mas deveria ser medium dado que os benchmarks são de 2023. O artigo é factual sobre O QUE os papers dizem, mas os papers dizem coisas sobre modelos de 2023.

**Mitigação:** Adicionar "temporal freshness" qualifier: "these results are from 2023 models; delta may differ with 2025-2026 models."

## Padrão Emergente: Hub Topology Creates Fragility

A KB tem topologia de **hub-and-spoke**: 3 artigos (kb-architecture-patterns, self-improving-agents, context-management) concentram ~34 inbound links de um total de ~135. Isso significa:
- 3 artigos influenciam 25% de todas as conexões
- Um erro em qualquer um dos 3 tem amplificação 10-13x
- A robustez da KB depende desproporcionalmente da qualidade desses 3

**Comparação com immune networks (aiNet):** O sistema imune evita single points of failure via REDUNDÂNCIA — múltiplos anticorpos cobrem o mesmo antígeno. Se um falha, outros compensam. Nossa KB não tem redundância — cada conceito tem 1 artigo. Se kb-architecture-patterns tiver um erro, não existe artigo alternativo sobre o mesmo tema que forneceria perspectiva diferente.

**Possível mitigação (não implementada):** Para os top 3 hubs, criar "artigos-sombra" (adversarial articles) que apresentam o mesmo tema de perspectiva oposta. Ex: "kb-architecture-patterns-critique" que documenta por que a taxonomia pode estar errada. Isso é o equivalente de diversidade imunológica — múltiplos "anticorpos" para o mesmo "antígeno."

## Ação Recomendada (por prioridade)

| # | Ação | Artigo | Custo | Impacto |
|---|------|--------|-------|---------|
| 1 | Separar Conteúdo/Interpretação completamente | kb-architecture-patterns | 15 min | Previne propagação de over-synthesis a 13 artigos |
| 2 | Temporal freshness qualifier nos benchmarks 2023 | self-improving-agents | 5 min | Previne propagação de números obsoletos a 11 artigos |
| 3 | Rebaixar RWKG interpretation_confidence ou mover valor remanescente | reflexion-weighted-knowledge-graphs | 10 min | Reduz risco de especulação propagando a 7 artigos |
| 4 | /challenge no kb-architecture-patterns (nunca foi challenged) | kb-architecture-patterns | 15 min | Hub nunca testado adversarially |

---

**Fontes wiki:** todas as 21 (análise topológica do grafo inteiro)

**Fontes raw verificadas:** N/A — dados são contagens de links, não claims de papers

**Confiança:** alta para topologia (contagens diretas), média para análise de risco (nosso julgamento sobre que tipos de erro propagam)

**Insight inesperado:** A KB tem topologia hub-and-spoke sem redundância — anti-pattern do ponto de vista imunológico. O sistema imune resolve isso com múltiplos anticorpos por antígeno. A KB poderia resolver com artigos adversariais por hub.

---

# Relatório Meta: AIS vs RWKG — Classificação Causal da Analogia

date: 2026-04-04
query: "AIS resolve credit assignment via clonal selection. RWKG tem estrutura causal análoga ou apenas superficialmente similar? Classifique em L1/L2/L3."
confidence: alta (classificação Pearl formal), média (derivações próprias)

---

## Mapeamento Estrutural

| Componente | RWKG | CLONALG |
|-----------|------|---------|
| O que evolui | Edge weights | População de anticorpos |
| Signal | Verbal reflection (rico, subjetivo) | Binding affinity (scalar, objetivo) |
| Credit assignment | **Explícito**: identificar edge falho | **Implícito**: amplificar o que funcionou |
| Memória | Weights persistem | "Population IS the memory" |
| Coordenação | Centralizado (1 LLM) | Descentralizado (seleção populacional) |
| Nível Pearl necessário | **L3** (contrafactual: "se este edge não existisse...") | **L1** (associação: "este path funcionou?") |

## Classificação Pearl

| Claim | Nível | Justificativa |
|-------|-------|---------------|
| "RWKG e CLONALG são similares" | L1 | Co-ocorrência de features (grafos, feedback, adaptação) |
| "CLONALG produziria resultados similares a RWKG em KGs" | L1 | Não testado: do(CLONALG-on-KG) |
| "RWKG requer L3 para credit assignment" | L2 | Derivação formal: "se este edge não existisse..." = contrafactual |
| "CLONALG evita necessidade de L3" | L2 | Derivação formal: "este path funciona?" = associação L1 |

## O Insight Não-Óbvio

**CLONALG funciona com MENOS poder causal que RWKG precisa.** RWKG exige L3 (contrafactual). CLONALG opera com L1 (associação). Um sistema que precisa de menos poder inferencial é mais robusto.

Mas resolvem problemas DIFERENTES:
- RWKG: corrigir o grafo existente (quais edges estão errados?)
- CLONALG: gerar um grafo melhor (quais paths inteiros funcionam?)

Possivelmente complementares: RWKG pra grafos pequenos (poucas edges pra avaliar), CLONALG pra grafos grandes (population selection).

## Veredicto

A analogia é **L1 (superficialmente similar) com diferença causal estrutural relevante** (um requer L3, o outro não). A analogia é produtiva (gerou insight sobre níveis causais) mas NÃO é causal (não prova que um substitui o outro).

Testar requer L2: implementar ambos no mesmo benchmark.

---

**Fontes:** AIS Tutorial (raw/articles/), Pearl Book of Why (raw/papers/), Reflexion (raw/papers/)
**Gaps:** Zero implementações de CLONALG em KGs. "Pequeno→RWKG, grande→CLONALG" é especulação sem dados.

---

# Relatório Meta: Anomalia Verbal Reflection — Análogo Biológico

date: 2026-04-04
query: "A anomalia 'verbal reflection melhora mas self-assessment falha' tem análogo biológico? O sistema imune tem o mesmo problema?"
confidence: alta (analogia existe), baixa (profundidade da analogia é L1)

---

## A Anomalia em LLMs (5 fontes verificadas)

| Fonte | O que mostra |
|-------|-------------|
| Reflexion | +39pp com testes (feedback externo), 52% sem testes |
| JudgeBench | Self-assessment ≈ random em problemas difíceis |
| CALM | Self-enhancement até 16.1% (Qwen2) |
| LMs Know | r=0.78-0.81 — consistente quando certo E errado |
| Model Collapse | Self-consumption destrói diversidade |

**Resumo:** Melhora com feedback externo. Falha em auto-avaliação sem ground truth.

## O Análogo Biológico

| Dimensão | LLM | Sistema Imune |
|----------|-----|---------------|
| Melhora com feedback externo | Sim (+39pp com testes) | Sim (clonal selection com antígeno) |
| Auto-avalia sem feedback | Não (≈ random) | **Não** (sem antígeno → sem seleção) |
| Falha de auto-avaliação | Self-enhancement bias | Autoimmune disease |
| Erro consistente | r=0.78-0.81 | Autoimmunity crônica |
| Prevenção | Ground truth externo | Tolerância central (thymic selection) |

## Classificação Pearl

**L1 (associação).** A analogia é superficial:
- Ambos falham em auto-avaliação sem feedback externo ✓
- Mas mecanismos são DIFERENTES: LLM = viés estatístico de distribuição; imune = falha de tolerância celular
- "Autoimmunity ≈ self-enhancement bias" é co-ocorrência de padrão, não identidade de mecanismo

## Solução Biológica Que Sugere Solução LLM (L1, não testada)

**Tolerância central:** o thymus ELIMINA T-cells auto-reactivas durante maturação.

**Aplicado a LLMs:** durante /ingest, implementar "thymic selection" que elimina claims onde o LLM mostra consistência excessiva (r > threshold) como potencial self-enhancement. Flag, não elimina automaticamente.

**Status:** especulação L1. Ninguém testou.

## Gaps

- 0 fontes sobre patologia imune (autoimmunity, tolerance failure)
- 0 fontes sobre computational models of immune tolerance
- Analogia autoimmunity ↔ self-enhancement = L1 até que mecanismos sejam comparados formalmente

---

**Fontes:** AIS Tutorial, Reflexion, LMs Know, CALM, JudgeBench (todos verificados em raw/)
**Insight:** O sistema imune e o LLM compartilham a mesma limitação fundamental: precisam de feedback externo para funcionar, e falham previsivelmente quando tentam se auto-avaliar. A diferença é que a biologia evoluiu tolerância central (prevenção de autoimmunity). LLMs não têm equivalente.
