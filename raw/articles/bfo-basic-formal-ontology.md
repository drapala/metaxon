---
source: https://en.wikipedia.org/wiki/Basic_Formal_Ontology
authors: Barry Smith et al.
date: 2020-01-01
type: article
quality: primary
stance: neutral
---

# BFO 2020: Basic Formal Ontology

ISO/IEC 21838-2 standard. The most widely adopted upper ontology in biomedical and scientific domains (400+ ontologies built on BFO).

## Top-Level Division: Continuant vs Occurrent

| Category | Definition | Time relation |
|----------|-----------|---------------|
| **Continuant** | Wholly present at any time it exists (all parts present) | Persists through time |
| **Occurrent** | Extends in time, only partially present at any moment | Unfolds through time |

### Continuants (things that persist)

**Independent Continuants** — objects that can exist on their own:
- Material entities (organisms, artifacts, portions of matter)
- Immaterial entities (sites, boundaries, spatial regions)

**Dependent Continuants** — can't exist without a bearer:
- Qualities (color, mass, temperature) — always of something
- Realizable entities:
  - Dispositions (fragility, solubility) — may or may not manifest
  - Roles (student, catalyst) — externally conferred
  - Functions (pumping for a heart) — selected-for dispositions

### Occurrents (things that happen)

- Processes (cell division, running, reasoning)
- Process boundaries (temporal instants)
- Temporal regions (time intervals)
- Spatiotemporal regions

## Key Design Principle: Realism

BFO represents mind-independent reality. Categories correspond to genuine divisions in the world, not human conceptual schemes. Contrasts with DOLCE (cognitive/linguistic orientation).

## Relevance to LLM Knowledge Bases

BFO's continuant/occurrent split maps to a fundamental KB distinction:

| BFO | KB equivalent |
|-----|--------------|
| **Continuant** (persists) | Wiki articles — concepts that endure across sessions |
| **Occurrent** (unfolds) | /ask sessions, /review cycles, /ingest runs — processes that happen |
| **Quality** (of a continuant) | source_quality, interpretation_confidence — properties of articles |
| **Disposition** (may manifest) | Tensions — may or may not resolve |
| **Role** (externally conferred) | Article's role changes: "factual reference" vs "speculative synthesis" |
| **Function** (selected-for) | /ask retrieves, /ingest compiles, /review maintains — each article has a function in the system |

BFO would type our wikilinks:
- [[X]] "part-of" Y (memory-consolidation is part of agent-memory-architectures)
- [[X]] "has-quality" Y (article has confidence:high)
- [[X]] "participates-in" Y (article participates in tension resolution)
- [[X]] "precedes" Y (context-management understanding precedes raptor-vs-flat)

Currently ALL our wikilinks are untyped — [[X]] could mean any of these. BFO provides the vocabulary to fix that.
