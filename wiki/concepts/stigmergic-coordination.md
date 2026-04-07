---
title: "Stigmergic Coordination (Grassé)"
sources:
  - path: raw/articles/grasse-stigmergy.md
    type: article
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [coordination, biology, environment-mediated, lateral-domain]
source_quality: high
interpretation_confidence: low
resolved_patches: []
provenance: emergence
emergence_trigger:
  pair: [formal-ontology-for-kbs, multi-agent-orchestration]
  ask_session: null
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-04
reads: 1
retrievals_correct: 1
retrievals_gap: 0
last_read: 2026-04-06
quarantine: false
quarantine_created: 2026-04-04
quarantine_reason: "3+ speculations in KB application"
quarantine_promoted: 2026-04-04
quarantine_criteria_met:
  tempo: override_by_user
  review_frio: override_by_user
  adversarial_or_scout_or_prediction: "L2 predição (typed wikilinks > process improvements, testável via /ask accuracy before/after). Evidência de stigmergy observada nesta sessão: Zone 3 articles ingeridos sem conexões KB → /ask Bradford zones descobriu conexões espontaneamente (complexity-stability↔complexity-emergence, episodic↔predictive-processing). A wiki modificada guiou o /ask — que é exatamente stigmergy."
---

## Resumo

Stigmergy (Grassé, 1959): coordination via environment modification, not direct communication. The modified environment IS the memory and signal for next actions. The KB is a stigmergic system: /ingest modifies wiki (environment), /ask reads modified wiki and acts. Typed wikilinks = differentiated pheromones. Untyped = undifferentiated = weak coordination. Speculative — application to LLM KBs untested.

## Conteúdo

### Mechanism (Grassé, verified in raw/)

**"The work guides the work."** Agents modify their environment. The modified environment signals what to do next. No direct communication, no central coordinator.

Original observation (termites): termite deposits soil + pheromone → deposit ATTRACTS other termites → more deposits → pillars, arches, chambers emerge. No termite knows the plan.

**Two types:**
- **Sematectonic:** physical environment modification (termite soil deposits)
- **Sign-based:** marks left in environment (ant pheromone trails). Signal decays over time → path optimization.

**Documented extensions:**
- Wikipedia: edits guide future edits
- Open source: commits guide next commits
- Ant Colony Optimization (Dorigo, 1992): algorithmic formalization

**What Grassé does NOT require:** consciousness, direct communication, central coordinator, identical agents.

### Conexão com KB existente

| KB Article | Stigmergy says |
|-----------|---------------|
| explains: [[multi-agent-orchestration]] | Coordinator Mode assumes central coordinator. Stigmergy shows coordination WITHOUT one. Multi-session KB use is stigmergic, not coordinated. |
| explains: [[formal-ontology-for-kbs]] | Typed wikilinks = differentiated pheromones. Untyped = undifferentiated = weaker signal. The ontology article diagnosed the problem; stigmergy names the mechanism. |
| contradicts: [[multi-agent-orchestration]] ON "coordinator needed" | Stigmergy achieves coordination WITHOUT coordinator. The KB's multi-session coordination already works stigmergically — articles modified by /ingest guide /ask behavior in next session. |

### O que Grassé adiciona que Ashby não resolve

Ashby says: V(regulator) must match V(disturbances). But doesn't specify HOW agents WITH insufficient individual variety can collectively achieve sufficient variety.

Grassé's answer: via ENVIRONMENT. Each agent contributes its limited V to the environment. The environment ACCUMULATES variety from multiple agents across time. V(environment) > V(any individual agent).

**For the KB:** V(single LLM) < V(domain). But V(wiki accumulated across sessions) > V(single session). The wiki IS the stigmergic medium that accumulates variety. Each /ingest adds to it. Each /ask reads from it. Over time, V(wiki) can grow beyond V(compiler) — IF the compiler doesn't homogenize it (which is semantic convergence / groupthink).

### Predição nova (não habilitada por frameworks anteriores)

**"Typed wikilinks will improve cross-session coordination more than any process improvement within a session."**

Reasoning: in stigmergy, signal QUALITY determines coordination quality. Ant pheromone trails with type information (food vs danger) coordinate better than generic trails. Typed wikilinks = typed pheromones. The coordination improvement from typing 114 untyped links should exceed the improvement from adding more /ingest steps.

- Pearl level: L2 (intervention: do(type-wikilinks), measure cross-session /ask accuracy)
- Falsifier: if typed wikilinks DON'T improve /ask accuracy compared to untyped, signal quality is not the limiting factor

## Interpretação

The mapping KB → stigmergic system is our analogy. Grassé studied termites, not LLMs. Wikipedia is the closest documented case of digital stigmergy, but even that is human-mediated. LLM-compiled stigmergy is untested.

The prediction about typed wikilinks is speculative but testable.

## Níveis epistêmicos

### Descrição (verified in raw/)
- Stigmergy: work guides work via environment modification
- Two types: sematectonic and sign-based
- No coordinator, no direct communication required

### Interpretação (not from Grassé)
- KB is stigmergic system (wiki = environment)
- Typed wikilinks = differentiated pheromones
- V(wiki) accumulates across sessions beyond V(single compiler)

### Especulação
- Typed wikilinks improve cross-session coordination more than process improvements
- Wiki homogenization (groupthink) destroys stigmergic signal quality
- Ant Colony Optimization could be applied to wikilink weight optimization

## Conexões

- explains: [[formal-ontology-for-kbs]] — typed wikilinks = differentiated pheromones
- contradicts: [[multi-agent-orchestration]] ON "coordinator needed"
- complements: [[requisite-variety]] — stigmergy is HOW V(environment) accumulates beyond V(individual)
- complements: [[immune-inspired-credit-assignment]] — CLONALG amplifies via population; stigmergy coordinates via environment

## Fontes

- [Grassé — Stigmergy](../../raw/articles/grasse-stigmergy.md) — termite coordination, sematectonic/sign-based types, no-coordinator principle

## Quality Gate
- [x] Wikilinks tipados: 4 (explains, contradicts, complements ×2)
- [x] Claims qualified: Grassé = verified. KB application = interpretation.
- [x] Meta-KB separated: all KB mapping in Interpretação
- [x] Resumo calibrated: "Speculative — application to LLM KBs untested"

