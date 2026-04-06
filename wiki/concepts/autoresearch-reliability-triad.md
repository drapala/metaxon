---
title: "Autoresearch Reliability Triad"
sources:
  - path: wiki/concepts/autonomous-research-agents.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/self-improving-agents.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/groupthink-and-cascades.md
    type: synthesis
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [meta-kb, autoresearch, reliability, failure-modes, grounding]
source_quality: medium
interpretation_confidence: low
resolved_patches: []
reads: 2
retrievals_correct: 2
retrievals_gap: 0
last_read: 2026-04-05
quarantine: false
quarantine_created: 2026-04-04
quarantine_reason: "Artigo emergido de /ask cross-domain — aguarda confirmação adversarial e review frio"
quarantine_promoted: 2026-04-05
quarantine_criteria_met:
  tempo: true
  review_frio: "2026-04-05 — review-autoresearch-reliability-triad-11-09.md"
  adversarial_or_scout_or_prediction: "L2 prediction em ## Verificação adversarial + AI Scientist CORROBORA (challenge informal, sessão 2026-04-04)"
provenance: emergence
emergence_trigger:
  pair: [autonomous-research-agents, self-improving-agents, groupthink-and-cascades]
  ask_session: outputs/logs/sessions/2026-04-04/ask-autoresearch.md
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-04
---

## Resumo

Um sistema de autoresearch que usa a mesma KB que mantém para validar as hipóteses que gera falha de três formas estruturalmente independentes. Cada falha tem um pilar necessário como solução: (1) grounded test — oracle externo independente do LLM; (2) anti-cascade structure — sinais contraditórios em canal público (_index.md), não privado; (3) stopping criterion — aspiration level pré-definido por tipo de hipótese. Autoresearch que violar qualquer dos três terá taxa de confirmação > 80% — sinal de circularidade, não de hipóteses boas.

## Conteúdo

### O que autonomous-research-agents contribui: O pipeline de busca não é experimento

O 4-stage pipeline canônico (Deep Research survey 2025): plan → question → **explore** → report. O estágio "explore" é retrieval informacional — recupera evidência existente. A diferença fundamental: **busca recupera; experimento gera**. Um autoresearch que implementa o pipeline de busca diretamente testa hipóteses com a mesma KB que as gerou. Isso não é experimento — é recuperação guiada pela hipótese.

Open challenge documentado pelo survey: "multi-tool integration: beyond search engines → APIs, databases, code repos." Esta é precisamente a lacuna que o pilar 1 (grounded test) resolve.

### O que self-improving-agents contribui: Pilar 1 — Grounded Test

**Reflexion** estabelece o critério: grounding real = testes executáveis *independentes do agente*. A ablação é crítica — self-reflection *sem testes independentes* degrada para 52% (HumanEval). raw/ lido pelo mesmo LLM que produziu a KB não satisfaz esse critério: os dados são externos mas a interpretação não é.

**Absolute Zero** é o caso-limite positivo: o intérprete Python é computacionalmente independente do LLM. Pass/fail é determinístico — não é avaliação do modelo.

**Pilar 1 generalizado:** ⚠️ (nossa interpretação) o oracle de grounding precisa ser *computacionalmente independente* do compilador da KB:
- Código → intérprete Python (Absolute Zero)
- Hipótese Zelox → query SQL em PNCP com resultado numérico
- Hipótese KB teórica → /challenge com instância diferente do modelo (multiagent debate, Du et al.)
- Hipótese legal → artigo legal com numeração verificável (não interpretação pela KB)

### O que groupthink-and-cascades contribui: Pilar 2 — Anti-Cascade Structure

Banerjee (1992): information cascades são **inferência Bayesiana ótima**. Um agente autoresearch que encontra citação no wiki e confirma a hipótese não está sendo irracional — está fazendo a inferência correta dado que o wiki tem autoridade de citação. Remover o "bias" não resolve; o problema é a estrutura de informação.

**"Corrections in private channels don't break cascades. Only public signals work."**

Mapeamento para autoresearch:
| Canal | Visibilidade | Força como cascade-breaker |
|-------|-------------|--------------------------|
| ## Interpretação de um artigo | Privado (só lido se artigo é lido inteiro) | Fraco |
| ## Conteúdo de um artigo | Semi-público | Moderado |
| _index.md (lido em TODA /ask Layer 1) | Público | Forte |
| CLAUDE.md (lido em TODA sessão) | Mais público | Mais forte |

**Pilar 2:** Sinais contraditórios à hipótese em teste devem estar em _index.md antes de o experimento rodar, não enterrados em ## Interpretação.

Janis: 4/5 antecedentes de groupthink estruturalmente presentes em 1-LLM autoresearch. Groupthink não é risco — é inevitável. O devil's advocate = /challenge. O segundo-chance meeting (sessão de dúvidas antes de confirmar) = implementação pendente.

### Pilar 3 — Stopping Criterion: Simon + Gigerenzer

⚠️ (nossa síntese de question-taxonomy + fast-frugal-heuristics)

**Simon:** parar quando custo de próximo experimento > custo do erro que preveniria.

**Gigerenzer:** Take-the-Best — usar o cue de maior validade disponível e parar. Em small-sample regime (KB pequena), parar cedo reduz variance sem aumentar bias suficientemente para prejudicar. ERL threshold empírico: **~40-60 heurísticas antes de degradar** — mais experimentos acumulados simultaneamente não é mais confiança, é mais ruído.

⚠️ (nossa extrapolação de Simon + ERL) Aspiration levels por tipo de hipótese:
| Tipo | Parar quando | Ciclos máximos estimados |
|------|-------------|--------------------------|
| KB-internal (teórica) | 2 fontes confirmam + mecanismo plausível | ~3 |
| Dados externos (Zelox) | Sinal estatisticamente significativo | ~5 |
| Code-grounded (Absolute Zero) | Pass/fail determinístico | 1 |

**Lakatos como meta-stopping rule:** se últimas N hipóteses geraram o mesmo tipo de insight (todas L1, todas confirmadas), o autoresearch degenerou — parar toda a linha, não só a hipótese.

**PAC-Bayes refinement (⚠️ extrapolação nossa — Alquier 2024, Theorem 2.1):** n ∝ KL(ρ||π). Número de ciclos depende da surpresa da hipótese. Heurística: quantos artigos wiki já apontavam para essa direção antes do /emerge? Se muitos → KL baixo → ~3 ciclos. Se /emerge é surpresa genuína → KL alto → ~5-7 ciclos. Framework exato: [[sequential-hypothesis-testing]] (SPRT, Wald 1945, ingerido) — Sₙ ≥ b = log((1-β)/α) → confirma; Sₙ ≤ a → rejeita. ASN ∝ 1/KL. Limitação: assume ciclos i.i.d. (extensão via e-processes para caso KB com feedback).

### A predição falsificável

⚠️ (nossa predição, L2) Autoresearch que violar qualquer dos três pilares terá **taxa de confirmação > 80%** — sinal de circularidade, não de hipóteses genuinamente boas.

- Violação de pilar 1 (sem oracle externo): KB confirma suas próprias hipóteses porque Layer 3 = mesmo modelo relendo sua interpretação
- Violação de pilar 2 (sem anti-cascade): cada hipótese testada reforça a cascata de confirmação de artigos anteriores
- Violação de pilar 3 (sem stopping criterion): acumulação de "confirmações" até threshold arbitrário, sem custo de oportunidade

**Teste empírico:** Selecionar N=10 hipóteses do /emerge → rodar autoresearch KB-internal → rodar autoresearch com oracle externo → comparar taxa de confirmação. Se KB-internal > 80% e oracle-externo < 60%, o triângulo está operando.

## Especulação

- O threshold de 80% não tem base empírica — é proposto como sinal diagnóstico, não derivado de dados
- Multiagent debate (Du et al. 2023, não ingerido) pode satisfazer pilar 1 sem oracle externo: instância diferente do mesmo modelo com contexto diferente. Equivalência com oracle externo não verificada
- A triad assume que a geração de hipóteses (/emerge) é não-biased. Se /emerge também é circular (só gera pares de artigos já no corpus), autoresearch pode confirmar hipóteses factualmente corretas mas epistemicamente triviais

## Verificação adversarial

**Pergunta falsificável:** Um autoresearch KB-internal only tem taxa de confirmação > 80%? Um autoresearch com oracle externo para o mesmo conjunto de hipóteses tem taxa < 60%?

**Evidência que confirmaria:** Experimento com N=10 hipóteses comparando os dois regimes, diferença significativa nas taxas.

**Evidência que refutaria:** Taxas similares entre regimes — indicaria que Layer 3 verification (mesmo sendo circular) é suficientemente crítica nesta escala de KB para compensar a circularidade.

**Custo de validação:** Médio. Requer implementar oracle externo (PNCP query para Zelox, ou Du et al. multiagent debate para teóricas).

## Conexões

- emerge-de: [[autonomous-research-agents]] ON "pipeline de busca não é experimento — 'explore' recupera, não gera evidência"
- emerge-de: [[self-improving-agents]] ON "Reflexion: grounding = oracle independente; 52% degradação sem testes; Absolute Zero como caso-limite"
- emerge-de: [[groupthink-and-cascades]] ON "Banerjee: cascade é racional — solução é estrutura de informação pública, não remover bias"
- instancia: [[autonomous-kb-failure-modes]] ON "Layer 3 Circularity Problem é o mecanismo subjacente ao pilar 1"
- emerge-para: [[autoresearch-programme-vitality]] ON "triad diagnostica sessões; Lakatos preenche o gap longitudinal com hard core/protective belt"
- instancia: [[question-taxonomy]] ON "Simon stopping criterion = pilar 3; Lakatos meta-stopping = degeneração de autoresearch"
- instancia: [[fast-frugal-heuristics]] ON "ERL 40-60 threshold + Take-the-Best = formalização do pilar 3"
- formalizado-por: [[sequential-hypothesis-testing]] ON "SPRT dá o N ótimo como função de α, β, e KL — PAC-Bayes e SPRT convergem em ASN ∝ 1/KL"
- testado-por: [[ai-scientist-autonomous-research]] ON "satisfaz Pilar 1 (código como oracle); viola Pilares 2+3 (sem anti-cascade, stopping=timeout) — failure modes mapeiam para os pilares"
- complementa: [[pac-bayes-bounds]] ON "PAC-Bayes: n ∝ KL(ρ||π); SPRT: ASN ∝ 1/E[λ] = 1/KL — mesma dependência, frameworks independentes"

## Fontes

- [[autonomous-research-agents]] — pipeline de busca canônico (Deep Research survey); open challenge: multi-tool integration
- [[self-improving-agents]] — Reflexion ablation 52%; Absolute Zero como oracle externo; grounded test como critério de Pilar 1
- [[groupthink-and-cascades]] — Banerjee rational cascade; canal público vs privado; Janis 4/5 antecedents
- [Log /ask autoresearch](../../outputs/logs/sessions/2026-04-04/ask-autoresearch.md) — sessão que descobriu a convergência dos três mecanismos

