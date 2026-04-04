---
title: "Requisite Variety (Ashby)"
sources:
  - path: raw/articles/ashby-requisite-variety.md
    type: article
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [cybernetics, control-theory, variety, error-floor, foundational]
source_quality: high
interpretation_confidence: low
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: true
quarantine_created: 2026-04-04
quarantine_reason: "5+ speculations in KB application section"
quarantine_promoted: null
quarantine_criteria_met:
  tempo: false
  review_frio: false
  adversarial_or_scout_or_prediction: false
---

## Resumo

Ashby's Law of Requisite Variety (1956): "Only variety can destroy variety." V(outcomes) ≥ V(disturbances) / V(regulator). A regulator with insufficient variety has an irreducible error floor. Applied to KB: 1 LLM with fixed variety compiling knowledge of higher variety → irreducible error. More process (16 /ingest steps, 9 commands, 6 hooks) doesn't increase V(regulator). All 5 documented failure modes may be symptoms of insufficient variety, not independent bugs. Speculative — application to LLM KBs untested.

## Conteúdo

### Definição Formal (Ashby, 1956, Chapter 11)

**"Only variety can destroy variety."**

V(O) ≥ V(D) / V(R)

| Variable | Definition | Verified in raw/ |
|----------|-----------|-----------------|
| V(D) | Variety of disturbances (perturbations from environment) | ✓ raw/ line 27 |
| V(R) | Variety of regulator (available responses) | ✓ raw/ line 28 |
| V(O) | Variety of outcomes (what we want to minimize) | ✓ raw/ line 29 |

For perfect control V(O) = 1: requires V(R) ≥ V(D).
If V(R) < V(D): error floor = disturbances that pass unregulated.

**Key distinctions (all verified in raw/):**
- Variety ≠ complexity — it's the NUMBER of distinct states a system can assume
- Control = ABSORPTION of disturbance variety by regulator, not elimination
- Regulator can be passive (filter) or active (compensator)
- Essential variables: what MUST be kept within limits for system survival

**Condition:** Necessary, not sufficient. V(R) ≥ V(D) is needed but regulator also needs correct STRUCTURE (mapping disturbance → response).

### Error Floor

When V(R) < V(D), some disturbances pass the regulator unregulated. This creates an irreducible error floor that NO improvement within the regulator's current variety can reduce. The ONLY fix is increasing V(R).

From raw/ (verified): "Se V(R) < V(D), alguns distúrbios passam sem regulação → error floor."

The error floor is not a bug to fix — it's a mathematical consequence of insufficient variety. Adding more steps to the regulation process (within the same V(R)) redistributes error across outcomes but cannot reduce total error below the floor.

### Applications (documented in literature, verified in raw/)

- Viable System Model (Beer, 1972) — organizational management
- Conant-Ashby theorem (1970): "Every good regulator of a system must be a model of that system"
- Management cybernetics: hierarchies AMPLIFY variety upward and ATTENUATE downward

### What Ashby Does NOT Resolve (verified in raw/)

- How to MEASURE variety in symbolic/linguistic systems (Ashby worked with discrete automata)
- How to INCREASE V(R) — the law says it's necessary, not how to get it
- Static formulation — doesn't model systems that LEARN and change V(R) over time

## Interpretação

### Aplicação à KB: classificação das anomalias

| KB Anomaly | Ashby says | Classification |
|-----------|-----------|----------------|
| **Semantic convergence** | **EXPLAINS mecanisticamente.** V(compiler) = 1 style. V(sources) = many styles. Compiler MUST compress many → 1. Convergence is not bias — it's the mathematical consequence of V(R) < V(D) in the style dimension. | Ashby is deeper than Janis: groupthink is the social manifestation; insufficient variety is the information-theoretic cause. |
| **"More is worse"** | **EXPLAINS mecanisticamente.** Each new source adds V(D) while V(R) stays fixed. More sources + same compiler = larger V gap = more error. Gigerenzer describes WHEN (small samples); Ashby explains WHY (V gap grows). | Complementary: Gigerenzer = statistical mechanism (bias-variance); Ashby = control-theoretic mechanism (variety gap). |
| **Layer 3 circularity** | **EXPLAINS mecanisticamente.** Self-regulation with V(self-evaluator) = V(evaluated). V gap = 0 states of additional variety. Correction capacity = 0 bits beyond what the regulator already contains. | The LLM reading its own wiki has no MORE variety than when it wrote it. Auto-correction is bounded by V(self). |
| **Corpus bias (73% AI/ML)** | **EXPLAINS mecanisticamente.** Compiler selects sources within its OWN high-V domains. Sources outside compiler's variety (psychology, biology) are underrepresented because compiler can't process them with high fidelity. Selection bias = variety-limited sampling. | The bias reflects V(compiler) topology, not conscious choice. |
| **Over-synthesis** | **EXPLAINS mecanisticamente.** Cross-paper taxonomy requires V high enough to maintain distinctions between papers. Numbers are low-V (a number is a number). Nuance is high-V (requires many states to represent). Compiler has V sufficient for numbers, insufficient for nuance. | Over-synthesis = running out of variety in the nuance dimension while still having plenty in the factual dimension. |

**All 5 anomalies are symptoms of ONE cause: V(compiler) < V(knowledge domain).**

### Predições Testáveis

**Predição A: Multiple compilers > single compiler in output diversity**

GPT-4 + Claude + Gemini compiling same KB = V(R) ≈ 3 × V(single). Output should have more diverse formulations, more perspectives preserved, less convergence.

- Pearl level: **L2** (intervention: do(add-models), measure diversity)
- Test: compile same 10 sources with 1 model vs 3 models. Measure stylistic diversity of wiki articles (embedding distance between article and raw source).
- Falsifier: if 3-model KB has SAME or LESS stylistic diversity than 1-model KB, variety is not the limiting factor.

**Predição B: Process improvements don't reduce error floor**

Adding more /ingest steps, more hooks, more commands — all operate within V(single model). Error floor stays constant.

- Pearl level: **L2** (intervention: do(add-process), measure error)
- Test: compare /ask accuracy on same questions: KB-with-9-commands vs KB-with-3-commands, same model, same sources.
- Falsifier: if 9-command KB has SIGNIFICANTLY fewer errors than 3-command KB on out-of-distribution questions, process CAN reduce error floor (Ashby wrong for this domain).

**Predição C: Lateral sources improve KB more than same-domain sources**

Because V(compiler) ∩ V(lateral domain) exploits DIFFERENT regions of V(compiler) than V(compiler) ∩ V(AI/ML). The compiler has untapped variety for psychology, biology, economics.

- Pearl level: **L2** (intervention: do(add-lateral-source), measure /ask improvement)
- Test: ingest 5 AI/ML papers vs 5 lateral-domain sources. Compare /ask novelty (insights not in existing articles).
- Falsifier: if AI/ML sources produce MORE novel insights than lateral sources, domain variety of the compiler is not the explanation.

**Predição D: Error floor is measurable**

V(compiler) can be approximated by: diversity of formulations across wiki articles (how many distinct ways the compiler expresses similar concepts). V(domain) can be approximated by: diversity of formulations across raw sources. Error floor ≈ V(raw) - V(wiki).

- Pearl level: **L1** (association: measure V, correlate with error)
- Test: compute embedding diversity of raw/ vs wiki/. Correlate with /ask error rate on spot-check.
- Falsifier: if V gap doesn't correlate with error rate, variety is not the mechanism.

**Predição E: /review reduces error WITHIN the floor but not below it**

Each /review redistributes errors (fixes some, introduces others) but total error stays constant at floor.

- Pearl level: **L2** (intervention: do(run-review), measure before/after)
- Test: spot-check error count before and after /review across multiple cycles. If total error plateaus at a constant, that's the floor.
- Falsifier: if error count decreases monotonically with each /review (no plateau), there's no floor (Ashby wrong for this domain).

### O que Ashby NÃO resolve

1. **How to MEASURE V(LLM).** Ashby worked with finite automata. V(GPT-4) is not well-defined. Proxy: embedding diversity of outputs across prompts? Token distribution entropy? No consensus.

2. **Dynamic V.** The law in its simplest form is static. An LLM in conversation CHANGES its effective V as context grows. Is V(LLM + 59 sources in context) > V(LLM alone)? Probably, but Ashby doesn't model this.

3. **When V(R) = V(D), WHICH responses map to WHICH disturbances.** Having enough variety is necessary but the regulator also needs correct structure. A model with V ≥ V(domain) but wrong internal mapping (hallucination) fails despite sufficient variety. Ashby: necessary, not sufficient.

4. **Multi-regulator coordination.** If 3 models compile a KB, is V(total) = V(M1) + V(M2) + V(M3) or V(M1) ∪ V(M2) ∪ V(M3)? Depends on independence. Ashby doesn't model multi-regulator systems (Beer does, in VSM).

### Verificação da análise L0

The /ask anterior (before this source existed) predicted:

| L0 prediction | Raw/ supports? |
|--------------|----------------|
| "V(regulador) << V(sistema)" | ✓ — the formal law confirms this framing |
| "Error floor irreducible within same V(R)" | ✓ — "Se V(R) < V(D), alguns distúrbios passam sem regulação" |
| "Semantic convergence = V gap in style dimension" | **Partially** — Ashby doesn't discuss "dimensions" of variety. Style as a dimension is our interpretation. |
| "More process ≠ more variety" | ✓ — consistent with law: adding steps within V(R) doesn't increase V(R) |
| "Multiple models increase V(R)" | **Not in Ashby** — multi-regulator is Beer's extension, not Ashby's original |
| "Predição: lateral sources match V(compiler) better" | **Not in Ashby** — this is our application of variety to source selection |

**Delta:** L0 analysis was broadly correct on the law itself. Over-extended on applications to multi-model and lateral sources — those are our interpretations, not Ashby's claims.

## Conexões

- explains: [[autonomous-kb-failure-modes]] — all 5 failure modes are symptoms of V(compiler) < V(domain)
- explains: [[fast-frugal-heuristics]] ON "more is worse" — Gigerenzer = statistical mechanism (bias-variance); Ashby = control-theoretic mechanism (variety gap). Complementary.
- explains: [[groupthink-and-cascades]] — groupthink is social manifestation; insufficient variety is the information-theoretic cause
- refines: [[curation-anti-bias]] ON "more adversarial sources = better" — Ashby: depends on whether adversarial sources increase V(R) or just V(D)
- contradicts: [[curation-anti-bias]] ON "process improvements fix bias" — Ashby: process within same V cannot reduce error below floor. Only V increase can.

## Fontes

- [Ashby — Requisite Variety](../../raw/articles/ashby-requisite-variety.md) — "Only variety can destroy variety" (Ch.11), error floor when V(R) < V(D), essential variables, Conant-Ashby theorem. Items marked [verificar na fonte] in raw/ are uncertain.

## Níveis epistêmicos

### Descrição (verificado em raw/)
- "Only variety can destroy variety" — V(O) ≥ V(D) / V(R)
- Error floor when V(R) < V(D) — irreducible
- Necessary condition, not sufficient
- Variety ≠ complexity
- Ashby's examples: thermostat, nervous system

### Interpretação (aplicação à KB — not from Ashby)
- All 5 failure modes as symptoms of V gap
- "Semantic convergence = V gap in style dimension"
- "More is worse = V(D) grows while V(R) fixed"
- "Layer 3 circularity = V(self-eval) = V(self), 0 additional bits"

### Especulação (predições não testadas)
- Multiple compilers > single compiler (Predição A)
- Process improvements don't reduce floor (Predição B)
- Lateral sources exploit untapped V(compiler) regions (Predição C)
- Error floor is measurable via embedding diversity (Predição D)
- /review plateaus at floor (Predição E)

## Quality Gate
- [x] Wikilinks tipados: 5 (explains ×3, refines, contradicts)
- [x] Claims Ashby vs editorial: Conteúdo = Ashby verified. Interpretação = our application. Especulação = our predictions.
- [x] Meta-KB em seção própria: all KB applications in Interpretação, not Conteúdo
- [x] Resumo calibrado: "Speculative — application to LLM KBs untested"

> ⚠️ QUARENTENA: Este artigo não pode ser linkado por outros artigos até ser promovido via /promote.
> Critérios pendentes: tempo (24h), review frio, adversarial/scout/predição.
