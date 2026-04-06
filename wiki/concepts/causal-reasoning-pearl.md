---
title: "Causal Reasoning (Pearl)"
sources:
  - path: raw/papers/pearl-book-of-why-ch1-3.md
    type: article
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [epistemology, causality, methodology, framework]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
reads: 1
retrievals_correct: 1
retrievals_gap: 0
last_read: 2026-04-05
provenance: source
quarantine: false
quarantine_created: 2026-04-04
quarantine_reason: "retrofit — speculative synthesis"
quarantine_promoted: 2026-04-05
quarantine_criteria_met:
  tempo: true
  review_frio: "2026-04-05 — sessão separada, cold review"
  adversarial_or_scout_or_prediction: "challenge 2026-04-05 + predição falsificável L2 adicionada"
---

## Resumo

Pearl's ladder of causation defines 3 irreducible levels: association (seeing), intervention (doing), counterfactual (imagining). Each level answers different questions and no amount of data at a lower level can derive answers at a higher level. The KB has been operating almost entirely at Level 1. (⚠️ hipótese, não verificada) O /ask pode ter tropeçado em perguntas contrafactuais porque Level 3 requer causal model explícito — mas o diagnóstico é retroativo e irreproduzível.

## Conteúdo

### A Escada Causal

#### NÍVEL 1 — ASSOCIAÇÃO (Seeing)

**Definição (Pearl):** P(y|x) — probability of Y given we OBSERVED X. Conditional probability. Correlation. Regression.

**Pergunta:** "O quê?" / "How likely is Y given I see X?"

**Exemplo na KB:** "5 sources observe that self-improvement and self-assessment co-occur in the same systems." Todas as tensões documentadas em [[tension-resolution]] operam aqui — observamos que artigos A e B dizem coisas diferentes, mas não sabemos qual causa a divergência.

**Limitação:** Cannot distinguish cause from effect. Cannot determine if changing X would change Y. "No machine can derive answers to Level 2 queries from Level 1 data alone, regardless of how much data it has."

#### NÍVEL 2 — INTERVENÇÃO (Doing)

**Definição (Pearl):** P(y|do(x), z) — probability of Y given we INTERVENE and SET X to x. The do-operator. NOT conditional probability: P(y|do(x)) ≠ P(y|x).

**Pergunta:** "E se eu fizer X?" / "What would Y be if I change X?"

**Exemplo na KB:** Reflexion ablation — removing test generation (do(no-tests)) caused performance to drop from 91% to 52%. This IS an intervention: the researchers changed one variable and measured the effect. The Reflexion ablation is Level 2 evidence.

**Limitação:** Tells you what WILL happen if you intervene. Cannot tell you what WOULD HAVE happened in a world where the intervention didn't exist. Cannot separate "verbal reflection is necessary" from "any structured feedback would have worked."

#### NÍVEL 3 — CONTRAFACTUAL (Imagining)

**Definição (Pearl):** P(y_x | x', y') — given that X was x' and Y was y', what WOULD Y have been if X had been x instead? Requires structural causal models (SCMs).

**Pergunta:** "Por quê? O que teria acontecido se X não tivesse ocorrido?"

**Exemplo na KB:** A pergunta "é verbalidade epifenômeno da ancoragem?" é Level 3. "Se verbal reflection NÃO tivesse sido usada, mas com mesma ancoragem (testes executáveis), o improvement teria sido o mesmo?" O /ask tropeçou aqui em duas sessões consecutivas porque Level 3 requer um causal model, não mais dados.

**Limitação:** Requires a causal MODEL, not just data. Two datasets can agree on all Level 1 and Level 2 queries while disagreeing on Level 3. Under-determined by data alone.

### Princípio formal: níveis não são redutíveis

More data at Level 1 cannot answer Level 2 questions. More data at Level 2 cannot answer Level 3 questions. This is a formal impossibility (Pearl's hierarchy theorem), not a practical limitation. Ingerir mais papers não resolve — precisa mudar o NÍVEL de raciocínio.

### Classificação do corpus existente

| Paper/Source | Claim principal | Nível | Justificativa |
|-------------|----------------|-------|---------------|
| LC vs RAG (Li et al.) | "LC outperforms RAG 56.3% vs 49%" | 1 (associação) | Benchmark comparison — observa performance, não intervém em variáveis causais |
| RAPTOR (Sarthi et al.) | "Summary nodes contribute 23-57% of retrieval" | 1 (associação) | Observa contribuição, não testa "if we remove summaries, what happens?" |
| Reflexion ablation | "Without test generation → 52%" | **2 (intervenção)** | Removes one variable (tests), measures effect. do(no-tests). |
| ERL (Allard et al.) | "Heuristics +7.8% vs trajectories -1.9%" | **2 (intervenção)** | Compares two treatments on same benchmark. do(heuristics) vs do(trajectories). |
| CALM (Ye et al.) | "Self-enhancement bias up to 16.1%" | 1 (associação) | Measures bias rate, doesn't test if removing bias improves outcomes |
| JudgeBench (Tan et al.) | "GPT-4o near random on hard tasks" | 1 (associação) | Observa performance, não intervém |
| Model Collapse (Shumailov) | "Recursive self-consumption destroys diversity" | **2 (intervenção)** | Trains on own output (do(self-consume)), measures degradation |
| LMs Know (Kadavath) | "Mostly calibrated, fails on hard" | 1 (associação) | Observa calibration, doesn't test if improving calibration improves performance |
| Hindsight | "83.6% on LongMemEval with 4 networks" | 1 (associação) | Benchmark result, not ablation of individual networks |
| Zep/Graphiti | "94.8% DMR, 90% latency reduction" | 1 (associação) | Performance comparison, not causal |
| A-MEM | "Memory evolution: +32% when removed" | **2 (intervenção)** | Ablation study: do(no-evolution) |
| PoC RWKG (our test) | "Adding 1 wikilink changed /ask answer" | **2 (intervenção)** | We intervened (added link), measured effect |
| Wikipedia risks (Huang) | "AI-revised content lowers RAG performance" | 1 (associação) | Observes correlation, doesn't isolate cause |

**Contagem: 8 Level 1 (associação), 5 Level 2 (intervenção), 0 Level 3 (contrafactual).**

A KB não tem NENHUMA evidência Level 3. Toda inferência contrafactual ("se X não tivesse acontecido...") é especulação, não evidência.

### Perguntas habilitadas

1. "Em qual nível causal opera a evidência pra este claim?" — antes não formulável, agora é checklist
2. "Esta pergunta requer nível 2 ou 3? Se sim, temos dados desse nível?" — previne over-inference
3. "O que seria necessário pra SUBIR de nível neste claim?" — design experimental orientado
4. "A KB está inferindo contrafactuais de dados associativos?" — detecta o erro mais comum

### Perguntas proibidas (pareciam causais mas são associativas)

- ❌ "RAPTOR valida nosso _index.md" → Nível 1 (co-ocorrência de padrões), não nível 2 (teste de intervenção)
- ❌ "ERL valida concept articles > raw dumps" → Nível 2 em Gaia2, mas transferência pra KBs é nível 1 (analogia, não intervenção)
- ❌ "Model collapse prova que /review sem humano degrada" → Nível 2 em weights, nível 1 em KBs (analogia)
- ❌ "Over-synthesis é o failure mode principal" → Nível 1 (observado em 1 review), não nível 2 (não testamos "remove over-synthesis → quality improves")

### Conexão com a anomalia

A anomalia "verbal reflection melhora mas self-assessment falha":

**A explicação "LLM como amplificador"** opera no **Nível 1** — observamos co-ocorrência de (improvement + ancoragem) e (failure + sem ancoragem). Chamamos isso de "amplificação" mas é pattern-matching em co-ocorrências.

**Para subir ao Nível 2:** precisaríamos do design 2x2 (verbal × ancoragem) no mesmo benchmark. O dado mais próximo: Reflexion ablation (com/sem testes) é nível 2 pra ancoragem, mas episodic-memory-vs-verbal (+8pp) é o único dado nível 2 pra verbalidade — 1 benchmark, 1 modelo, insuficiente.

**Para subir ao Nível 3:** "Se verbal reflection NÃO tivesse sido usada (com mesma ancoragem), o improvement teria sido o mesmo?" Requer um structural causal model do processo de learning-from-experience. Nenhum paper no corpus constrói esse modelo.

(⚠️ hipótese diagnóstica, irreproduzível) Sessões de /ask que tropeçaram em perguntas sobre a anomalia podem ter falhado porque a pergunta era L3 e a KB só tinha evidência L1/L2 — mas o diagnóstico é retroativo. Alternativas: artigos ausentes na época, query mal formulada.

## Interpretação

A classificação do corpus (tabela acima) é nossa — Pearl não classifica papers de agent memory. A contagem "8 Level 1, 5 Level 2, 0 Level 3" é verificável nos papers mas a CLASSIFICAÇÃO de cada paper é nosso julgamento.

A designação "perguntas proibidas" é forte — esses claims não são ERRADOS, são claims de nível 1 apresentados como se fossem nível 2. A ação correta: qualificá-los com o nível, não removê-los.

## Níveis epistêmicos

### Descrição (de Pearl)
- 3 níveis da escada causal (definições formais, operadores, exemplos canônicos)
- Irreducibilidade entre níveis (hierarchy theorem)
- Do-calculus (3 regras)

### Interpretação (aplicação à KB)
- Classificação dos 13 papers em níveis causais
- Mapeamento de anomalias da KB a níveis
- "Perguntas proibidas" como claims de nível baixo apresentados como alto

### Especulação (o que a KB infere mas Pearl não afirma)
- "LLM como amplificador" é nível 1 — Pearl não discute LLMs
- O design 2x2 proposto é nossa formulação, não de Pearl
- A predição "ancoragem ~5x mais importante que verbalidade" não tem base formal

## Conexões

- contradicts: [[self-improving-agents]] ON "verbal reflection IS the mechanism" — Pearl diria: verbal reflection CORRELATES with improvement (L1), ablation shows ancoragem CAUSES improvement (L2), verbalidade vs scalar is UNTESTED (L3)
- validates: [[question-taxonomy]] — adds causal level as question dimension
- derivedFrom: [[reflexion-weighted-knowledge-graphs]] — RWKG is a L1 hypothesis (co-occurrence) presented as L2 (mechanism). Pearl exposes this.
- partOf: [[formal-ontology-for-kbs]] — causal relations are a type the ontology needs
- emerge-para: [[evaluation-order-independence]] ON "L3 impossível internamente → única solução é intervenção L2 no design externo"

## Fontes

- [Pearl — Book of Why Ch1-3](../../raw/papers/pearl-book-of-why-ch1-3.md) — ladder of causation (3 levels), do-calculus, hierarchy theorem: levels are formally irreducible

## Predição falsificável

**(L2, testável)** Papers classificados como L2 (intervenção) na tabela acima mostrarão effect size estável em replicações com benchmarks diferentes; papers classificados como L1 (associação) mostrarão alta variância. Fundamento: evidência L2 captura mecanismo causal; L1 captura correlação — correlações são instáveis por construção enquanto mecanismos são transferíveis.

**Teste concreto:** Selecionar 3 claims L2 da tabela (Reflexion ablation, ERL, A-MEM) e 3 claims L1 (LC vs RAG, RAPTOR, CALM). Para cada: checar se outros benchmarks nos mesmos papers reportam effect sizes consistentes. Se L2 tem variância < 20% entre benchmarks e L1 tem variância > 40%, predição confirmada.

**Evidência que refutaria:** L2 papers com effect sizes altamente variáveis entre benchmarks — indicaria que os "mecanismos" identificados são igualmente instáveis, e que a distinção L1/L2 não prediz estabilidade empírica.

## Quality Gate
- [x] Wikilinks tipados: 4 substituições (contradicts, validates, derivedFrom, partOf)
- [x] Instance→class: 0 claims numéricos (framework, not benchmark)
- [x] Meta-KB separado: examples reference KB but are in Conteúdo as application (appropriate for framework article)
- [x] Resumo calibrado: includes "almost entirely at Level 1" and "lacked vocabulary for"
