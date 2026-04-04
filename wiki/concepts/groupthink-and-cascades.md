---
title: "Groupthink and Information Cascades"
sources:
  - path: raw/articles/janis-groupthink.md
    type: article
    quality: primary
  - path: raw/articles/banerjee-information-cascade.md
    type: article
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [psychology, decision-theory, failure-modes, lateral-domain]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
---

## Resumo

Two phenomena from psychology and economics (groupthink, Janis 1972; information cascades, Banerjee 1992) were independently studied for 50+ years before this KB re-discovered them as "semantic convergence" and "authority bias cascade." The literature has tested mitigations empirically. Several of the KB's proposed fixes (/challenge, spot-check, /curate) are re-inventions of Janis' standard prescriptions (devil's advocate, outside experts, independent sub-groups).

## Conteúdo

### Mapeamento de Re-descobertas

| KB Failure Mode | Nome na literatura | Paper | Décadas de estudo | KB re-inventou como |
|----------------|-------------------|-------|-------------------|---------------------|
| Semantic convergence | **Groupthink** (pressures toward uniformity) | Janis, 1972 | 50+ anos | "semantic convergence" (2026) |
| Authority bias cascade | **Information cascade** (rational herding) | Banerjee, 1992 | 30+ anos | "authority bias cascade" (2026) |
| Over-synthesis (homogenization) | **Defective decision making** (selective bias, incomplete alternatives) | Janis, 1972 | 50+ anos | "over-synthesis" (2026) |
| Forced tension resolution | **Illusion of invulnerability** + collective rationalization | Janis, 1972 | 50+ anos | "forced tension resolution" (2026) |
| Layer 3 circularity | **Cascade stops information aggregation** | Banerjee, 1992 | 30+ anos | "Layer 3 circularity" (2026) |

### O que a literatura sabe que a KB não sabia

**1. Groupthink antecedents PREDICT occurrence (Janis)**

5 antecedent conditions: high cohesiveness, structural insulation, directive leadership, homogeneity, high stress.

A KB compiled by 1 LLM in 1 session:
- High cohesiveness: ✅ (1 compiler = maximally cohesive)
- Structural insulation: ✅ (no external review until we added spot-check)
- Directive leadership: ✅ (CLAUDE.md states preferences before "discussion")
- Homogeneity: ✅ (1 model = identical perspective on everything)
- High stress: ⬜ (not applicable — no time pressure)

**4/5 antecedents present.** Groupthink is not a risk — it's structurally inevitable given the architecture.

**2. Information cascades are RATIONAL (Banerjee)**

The KB frames authority bias as "bias" (implying irrationality). Banerjee shows it's optimal Bayesian inference: the LLM is RATIONAL to confirm its own wiki when wiki claims have citation authority. The fix isn't "remove bias" — it's "change the information structure" (make contradicting signals more visible).

**3. Early signals have disproportionate influence (Banerjee)**

The first articles written set the cascade direction. All subsequent articles are downstream. This explains why kb-architecture-patterns (score 26, written early) shapes 13 dependent articles — it's the seed of the cascade.

**4. One strong contradicting signal breaks a cascade (Banerjee)**

Value of /curate and spot-check is NOT proportional to frequency. ONE good challenge can undo months of cascade. This justifies running /challenge rarely but thoroughly.

### Mitigações: Literatura vs KB

| Janis prescription (1972) | KB equivalent (2026) | Status |
|--------------------------|---------------------|--------|
| **Devil's advocate** | /challenge command | Re-invented. Matches Janis exactly. |
| **Outside experts** | Spot-check prompt (paste in another LLM) | Re-invented. |
| **Independent sub-groups** | Multiagent spot-check (2 system prompts) | Re-invented. |
| **Leader impartiality** | — | NOT IMPLEMENTED. CLAUDE.md states preferences upfront. Violates Janis. |
| **Second-chance meeting** | — | NOT IMPLEMENTED. No "express residual doubts" session after article is written. |
| **Norms valuing critical evaluation** | /curate adversarial quota (stance tracking) | Partially implemented. |

**2 missing prescriptions** that the KB should adopt:

1. **Leader impartiality:** CLAUDE.md should NOT state how articles "should" be written before the agent compiles them. The template prescribes structure — but content preferences (e.g., "wiki is hint, not truth") are directive leadership. Alternative: let the agent compile first, THEN evaluate against principles.

2. **Second-chance meeting:** After /ingest produces an article, hold a dedicated "doubt session" where the SOLE goal is surfacing what feels wrong. Not /challenge (which is adversarial). Not /review (which is systematic). A moment of "what am I uncomfortable about?" This is anti-groupthink: creating space for the discomfort that uniformity suppresses.

### Cascade-Breaking Applied to KB Architecture

Banerjee shows: corrections in PRIVATE channels don't break cascades. Only PUBLIC signals work.

Applied to KB:
- Correction in ## Interpretação (read only if article is fully read) = PRIVATE = weak cascade-breaker
- Correction in ## Conteúdo (read during Layer 2 depth) = SEMI-PUBLIC = moderate
- Correction in _index.md pointer (read during EVERY /ask Layer 1) = PUBLIC = strong cascade-breaker
- Correction in CLAUDE.md (read during EVERY session) = MOST PUBLIC = strongest

**Implication:** When a cascade-breaking insight is found (e.g., "RWKG subsumed by prior work"), don't bury it in ## Interpretação. Put it in the _index.md pointer. That's where the cascade breaks.

## Interpretação

The mapping KB-failure-modes → groupthink/cascades is our interpretation. Janis studied policy decisions (Bay of Pigs, Vietnam). Banerjee studied sequential economic decisions. Neither studied LLM knowledge bases. The structural similarity is L1 (association); whether the SAME mitigation mechanisms work in KB context is untested (L2 would require implementing leader impartiality and second-chance meeting, then measuring effect).

The claim "4/5 antecedents present" is strong because the mapping is structural, not analogical — high cohesiveness of 1 LLM IS the definition, not an analogy to it.

## Conexões

- instanceOf: [[autonomous-kb-failure-modes]] — semantic convergence IS groupthink; authority cascade IS information cascade. The failure modes article RE-DISCOVERED these phenomena.
- validates: [[curation-anti-bias]] — /curate adversarial quota = Janis' "norms valuing critical evaluation." Literature validates the approach.
- validates: [[llm-as-judge]] — self-enhancement bias (CALM) is a MECHANISM for groupthink symptom #5 (self-censorship). The LLM censors dissenting interpretations.
- explains: [[kb-architecture-patterns]] — 13 inbound links on kb-architecture-patterns = cascade seed (Banerjee: early signals have disproportionate weight)

## Fontes

- [Janis — Groupthink](../../raw/articles/janis-groupthink.md) — 5 antecedents, 8 symptoms, 7 defective decision symptoms, 6 prevention remedies. 50+ years of research.
- [Banerjee — Information Cascades](../../raw/articles/banerjee-information-cascade.md) — sequential herding is RATIONAL, cascades are fragile (1 strong signal breaks them), early signals have disproportionate weight

## Quality Gate
- [x] Wikilinks tipados: 4 (instanceOf, validates ×2, explains)
- [x] Re-descobertas explicitamente nomeadas: 5 failure modes mapped to literature
- [x] Mitigações comparadas: 6-row table KB vs Janis, 2 missing identified
- [x] Resumo calibrado: "re-discovered" language, not "invented." Acknowledges 50+ years of prior work.
