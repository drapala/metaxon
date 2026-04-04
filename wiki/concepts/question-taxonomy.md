---
title: "Question Taxonomy"
sources:
  - path: raw/articles/miles-seven-research-gaps-taxonomy.md
    type: article
    quality: primary
  - path: raw/articles/socratic-prompting-llms.md
    type: paper
    quality: primary
  - path: raw/articles/oblique-strategies-lateral-thinking.md
    type: note
    quality: tertiary
created: 2026-04-04
updated: 2026-04-04
tags: [meta-kb, methodology, questioning, epistemology]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

The quality of KB insights depends more on the questions asked than the sources ingested. Three frameworks inform systematic questioning: Miles' 7 Research Gaps (where to look), Socratic Methods (how to probe), and Oblique Strategies (how to reframe). Together they enable typed questions that open investigation rather than close it.

## Conteúdo

### 7 Types of Research Gaps (Miles, 2017)

| Gap Type | What it finds | /ask Template |
|----------|-------------|---------------|
| **Evidence** (contradiction) | Conflicting findings between sources | "Papers X and Y reach opposite conclusions about Z. What assumption differs?" |
| **Knowledge Void** | Unstudied territory | "What has NO ONE studied in this domain?" |
| **Practical-Knowledge** | Theory-practice disconnect | "Research says X works, practitioners do Y. Why?" |
| **Methodological** | Method-limited findings | "All studies used method A. What would method B reveal?" |
| **Empirical** (evaluation void) | Claims without data | "This sounds compelling. Where's the evidence?" |
| **Theoretical** (application void) | Theory not applied to relevant domain | "Theory T works for D1. What happens in D2?" |
| **Population** | Context-limited findings | "This works for X. Does it work for Y?" |

### 6 Socratic Techniques (Chang, 2023)

| Technique | Purpose | /ask Application |
|-----------|---------|-----------------|
| **Definition** (τί ἐστι) | Clarify before reasoning | "Before answering, define [concept] in this context" |
| **Elenchus** (cross-examination) | Find contradictions | /challenge command is elenchus applied to articles |
| **Dialectic** (thesis→antithesis→synthesis) | Resolve opposing views | Tension resolution table IS dialectic |
| **Maieutics** (intellectual midwifery) | Guided discovery from what's already known | Follow wikilinks to discover unstated connections |
| **Generalization** (induction) | Specific examples → general principle | How taxonomy articles (kb-architecture-patterns) are generated |
| **Counterfactual** | "What if the opposite were true?" | Most powerful /challenge question: "Under what conditions does this fail?" |

### Oblique Strategies for KB Questioning

Default /ask: direct question → direct answer. Linear.

Oblique approach: reframe BEFORE answering.

| Strategy | Application |
|----------|------------|
| "Reverse" | Invert: "when does this NOT work?" |
| "Use an old idea" | Apply foundational concept to modern problem |
| "What is the reality of the situation?" | Strip interpretation, look at raw/ only |
| "Emphasize differences" | Find divergence, not convergence |
| "Look closely at the most embarrassing details" | Focus on weakest claim |
| "Do nothing for as long as possible" | Don't ask yet — let questions emerge naturally |

### Question Types for /ask

| Type | When to use | Template |
|------|-----------|----------|
| **CONTRADIÇÃO** | Two articles disagree | "X and Y reach opposite conclusions. What assumption differs?" |
| **ESCALA** | Mechanism described at one scale | "This works with 10 nodes. At what point does it break?" |
| **FRONTEIRA** | Need to find limits | "Simplest case where this is necessary — and most complex where it still works?" |
| **MECANISMO OCULTO** | Paper describes WHAT works but not WHY | "What underlying mechanism explains the observed results?" |
| **AUSÊNCIA** | Need to find blind spots | "What did all three authors NOT ask? What was out of scope for institutional, not intellectual reasons?" |
| **TRANSFERÊNCIA** | Concept from one domain | "Theory T works in D1. What happens in D2?" |
| **EMPÍRICA** | Claim without evidence | "This framework sounds compelling. What would a test look like?" |

### Perguntas Proibidas (fecham em vez de abrir)

- "Is X better than Y?" → binary, kills nuance. Better: "Under what conditions does X outperform Y?"
- "What is X?" → definitional, no insight. Better: "What does X explain that nothing else does?"
- "Summarize X" → compression, not discovery. Better: "What does X imply that the author didn't explore?"
- "Do you agree with X?" → asks LLM for opinion (self-enhancement bias). Better: "What evidence would change your mind about X?"

## Interpretação

This taxonomy is our synthesis — Miles, Chang, and Eno didn't design these for LLM knowledge bases. The mapping from research gaps → /ask templates is our interpretation. The "perguntas proibidas" list is our prescription based on over-synthesis experience.

## Conexões

- [[tension-resolution]] — Evidence Gap questions are the discovery mechanism for tensions
- [[curation-anti-bias]] — Knowledge Void and Population Gap questions identify missing sources
- [[autonomous-kb-failure-modes]] — Empirical Gap questions detect speculative claims
- [[llm-as-judge]] — "Do you agree?" is a prohibited question due to self-enhancement bias

## Fontes

- [Miles — 7 Research Gaps](../../raw/articles/miles-seven-research-gaps-taxonomy.md) — taxonomy of 7 gap types with definitions, widely cited in research methodology
- [Socratic Prompting](../../raw/articles/socratic-prompting-llms.md) — 6 Socratic techniques mapped to LLM prompting: definition, elenchus, dialectic, maieutics, generalization, counterfactual
- [Oblique Strategies](../../raw/articles/oblique-strategies-lateral-thinking.md) — lateral thinking via reframing: "honor thy error as hidden intention," reverse, emphasize differences
