---
source: https://en.wikipedia.org/wiki/Upper_ontology
authors: Nicola Guarino, Aldo Gangemi et al.
date: 2002-01-01
type: article
quality: secondary
stance: neutral
---

# DOLCE: Descriptive Ontology for Linguistic and Cognitive Engineering

## Core Principle: Cognitive, Not Realist

DOLCE treats ontological categories as "cognitive artifacts" dependent on human perception, cultural factors, and social conventions. Deliberately DESCRIPTIVE (how humans categorize) rather than PRESCRIPTIVE (how the world is).

Contrasts with BFO's realism. DOLCE says: categories reflect human cognition, not objective reality.

## Top-Level Categories

| Category | What it covers |
|----------|---------------|
| **Endurant** | Objects wholly present at each moment (physical objects, social objects) |
| **Perdurant** | Events, processes — have temporal parts |
| **Quality** | Individual properties (color, weight) |
| **Abstract** | Sets, regions, other non-temporal, non-spatial entities |

### Endurants vs Perdurants (key distinction)
- Endurant: "this apple" exists wholly now. It was also wholly present yesterday.
- Perdurant: "eating the apple" has temporal parts. The beginning is not the same as the end.

## DOLCE-Ultralite (practical version)

Simplified OWL version by Aldo Gangemi. Reduced modal axioms. Extended to include Descriptions and Situations (D&S) framework. Widely adopted. Source of many ontology design patterns.

## Relevance to LLM Knowledge Bases

DOLCE's cognitive orientation is more appropriate for a KB than BFO's realism:

- Our wiki articles are COGNITIVE artifacts (compiled by LLM from human sources), not representations of mind-independent reality
- "Concept" in our KB is closer to DOLCE's cognitive category than BFO's natural kind
- The distinction between how humans categorize (DOLCE) and how reality is structured (BFO) maps to our Conteúdo (what sources say) vs Interpretação (how we frame it)

But BFO's TYPED RELATIONS (part-of, has-quality, participates-in) are useful regardless of ontological orientation. We can adopt BFO's relation vocabulary with DOLCE's cognitive stance.
