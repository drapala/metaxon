---
title: "Formal Ontology for Knowledge Bases"
sources:
  - path: raw/articles/noy-ontology-development-101.md
    type: article
    quality: primary
  - path: raw/articles/bfo-basic-formal-ontology.md
    type: article
    quality: primary
  - path: raw/articles/dolce-descriptive-ontology.md
    type: article
    quality: secondary
  - path: raw/articles/owl2-primer-knowledge-representation.md
    type: article
    quality: primary
  - path: raw/articles/relation-ontology-obo.md
    type: article
    quality: primary
created: 2026-04-04
updated: 2026-04-04
tags: [ontology, structure, typed-relations, meta-kb]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Five ontology frameworks reveal structural gaps in this KB: untyped wikilinks, no class hierarchy, no competency questions, and no continuant/occurrent distinction. The applicable primitives are: typed relations (part-of, contradicts, derives-from), entity classification (continuant vs occurrent), property characteristics (symmetry, transitivity), and a 7-step development methodology. Practical adoption requires typed wikilink conventions, not full OWL tooling.

## Conteúdo

### What Ontology Exposes About This KB (Noy 101 diagnostic)

| Noy Step | What it prescribes | What this KB has | Gap |
|----------|-------------------|------------------|-----|
| 1. Domain + scope | Define competency questions | None defined | /question created retroactively, but no formal scope |
| 2. Reuse existing | Check prior ontologies | We do reuse (via /scout) | Adequate |
| 3. Enumerate terms | List all relevant terms | 18 concept articles | Implicit, not systematic |
| 4. Class hierarchy | IS-A relationships | ALL articles are peers in concepts/ | No hierarchy. "agent-memory-architectures" should be superclass of patterns 1-8 |
| 5. Properties (slots) | Typed relationships | 114 untyped wikilinks | Every link is the same — no part-of vs contradicts vs derives-from |
| 6. Facets (constraints) | Value restrictions | source_quality + interpretation_confidence | Partial — 2 properties exist, but not formalized |
| 7. Instances | Specific individuals | 54 raw/ sources are instances | Adequate |

### Entity Types: Continuant vs Occurrent (BFO)

BFO's top division applies directly to KB content:

| BFO Category | KB Entity | Examples |
|-------------|-----------|---------|
| **Continuant** (persists wholly) | Wiki articles, concepts, sources | memory-consolidation.md persists across sessions |
| **Occurrent** (unfolds in time) | /ask sessions, /review runs, /ingest cycles | Each /ask is a process with temporal parts |
| **Quality** (of a continuant) | Article properties | source_quality:high, interpretation_confidence:medium |
| **Disposition** (may manifest) | Documented tensions | Tension between RAG and KB may or may not resolve |
| **Role** (externally conferred) | Article function in context | Same article serves as "factual reference" in one /ask and "speculative hypothesis" in another |

**Key insight:** Our KB treats everything as continuant (static articles). But /ask sessions, /review cycles, and /ingest runs are OCCURRENTS — processes with temporal parts, inputs, outputs. We track continuants (articles) but not occurrents (processes). We don't know which /ask sessions used which articles, when, or whether the answers were correct.

### Typed Relations: What Our Wikilinks Should Express (RO + OWL)

Currently all 114 wikilinks are `[[X]]` — semantically identical. Five relation types would cover 90% of our actual link meanings:

| Relation | Formal type | Current wikilink | Typed version |
|----------|------------|-----------------|---------------|
| **part-of** | Mereological (transitive) | `[[agent-memory-architectures]]` from memory-consolidation | `partOf: agent-memory-architectures` |
| **contradicts** | Symmetric | `[[retrieval-augmented-generation]]` from llm-knowledge-base (tension) | `contradicts: retrieval-augmented-generation ON "need for RAG"` |
| **derives-from** | Derivation | `[[reflexion-weighted-knowledge-graphs]]` from tension-resolution | `derivedFrom: memgpt AND reflexion AND hipporag` |
| **validates** | Asymmetric | `[[kb-architecture-patterns]]` from raptor-vs-flat | `validates: kb-architecture-patterns.pattern4` |
| **supersedes** | Temporal + asymmetric | Hindsight vs RWKG | `supersedes: reflexion-weighted-knowledge-graphs (partially)` |

OWL property characteristics that matter:
- **Symmetry** for contradicts (if A contradicts B, B contradicts A)
- **Transitivity** for part-of (if A partOf B partOf C, then A partOf C)
- **Asymmetry** for derives-from (A derives from B doesn't mean B derives from A)

### Cognitive vs Realist Orientation (DOLCE vs BFO)

| Dimension | BFO (realist) | DOLCE (cognitive) | This KB |
|-----------|--------------|-------------------|---------|
| Categories represent | Mind-independent reality | Human cognition | **DOLCE** — our concepts are LLM-compiled cognitive artifacts |
| "Correct" ontology | One true structure | Depends on purpose | **DOLCE** — "no one correct ontology" (Noy) |
| Relations | Formal, axiomatic | Descriptive | **Hybrid** — formal types (RO) with cognitive stance (DOLCE) |

### Open-World Assumption (OWL)

OWL: missing facts aren't false — they're unknown. This matches our architecture:
- /ask says "Gaps: what the wiki doesn't cover" — open-world
- /review doesn't assume "no warnings = no problems" — explicitly checks for invisible degradation
- Absence of a tension between two articles doesn't mean they agree — it means we haven't checked

### Perguntas que este framework habilita na KB que antes não eram formuláveis

1. **"What is X part of?"** — currently impossible without reading the article. Typed part-of links would answer via graph traversal.

2. **"What contradicts X?"** — currently requires reading tension-resolution.md. Typed contradicts links would surface automatically.

3. **"What derives from source Y?"** — currently requires grepping _registry.md. Typed derives-from links would trace provenance.

4. **"Is the inference chain A→B→C valid?"** — currently impossible. If part-of is transitive and A partOf B partOf C, a reasoner could verify A partOf C automatically.

5. **"Which articles are occurrents (process descriptions) vs continuants (entity descriptions)?"** — We could separate "what memory consolidation IS" (continuant) from "how /review WORKS" (occurrent). Currently mixed.

6. **"What properties does concept X have across all articles that mention it?"** — Currently scattered in frontmatter + prose. Formal slots would aggregate.

## Interpretação

### Practical Adoption Path (without full OWL tooling)

Full OWL is overkill for 18 articles. But typed wikilink conventions are free:

**Phase 1 (now, 18 articles):** Conventions in wikilink descriptions
```markdown
## Conexões
- [[partOf:agent-memory-architectures]] — consolidation is one memory pattern
- [[contradicts:retrieval-augmented-generation]] ON "need for RAG at small scale"
- [[derivedFrom:memgpt,reflexion,hipporag]] — synthesized from 3 sources
```

**Phase 2 (50+ articles):** Frontmatter relation arrays
```yaml
relations:
  part_of: [agent-memory-architectures]
  contradicts: [{target: retrieval-augmented-generation, scope: "RAG at small scale"}]
  derived_from: [memgpt, reflexion, hipporag]
```

**Phase 3 (200+ articles):** Consider actual OWL tooling or graph database.

### Competency Questions (Noy Step 1, retroactive)

This KB should be able to answer:
1. "What are the main architectural patterns for agent memory?" → agent-memory-architectures
2. "When does LC outperform RAG?" → retrieval-augmented-generation
3. "What risks does an unsupervised KB face?" → autonomous-kb-failure-modes
4. "How should I formulate questions for maximum insight?" → question-taxonomy
5. "What has this KB gotten wrong?" → /challenge results, epistemic audit

Questions it CANNOT currently answer:
1. "What is the complete provenance chain for claim X?" (no typed derives-from)
2. "Which articles are process descriptions vs entity descriptions?" (no continuant/occurrent)
3. "What would break if article X were removed?" (no typed dependency links)

## Verificação adversarial

- **Claim mais fraco:** "5 typed relations would cover 90% of link meanings" — untested. Would need to classify all 114 wikilinks to verify.
- **O que as fontes NÃO dizem:** None of the 5 sources tested typed wikilinks in markdown-based KBs. All assume RDF/OWL tooling.
- **Simplificações:** OWL reasoning requires closed axioms; our KB has open-ended text. The "reasoning" benefits (inconsistency detection, transitive inference) may not work with text-based approximations.

## Conexões

- [[question-taxonomy]] — Noy Step 1 (competency questions) is what /question retroactively provides
- [[tension-resolution]] — "contradicts" relation type would formalize tension detection
- [[kb-architecture-patterns]] — ontology would add class hierarchy to flat article structure
- [[autonomous-kb-failure-modes]] — typed links enable dependency analysis (what breaks if X changes)
- [[agent-memory-architectures]] — BFO continuant/occurrent maps to memory types (persistent vs process)

## Fontes

- [Noy — Ontology 101](../../raw/articles/noy-ontology-development-101.md) — 7-step methodology, "no one correct ontology," class hierarchy + typed properties
- [BFO 2020](../../raw/articles/bfo-basic-formal-ontology.md) — continuant vs occurrent, qualities, dispositions, roles, functions (ISO 21838-2)
- [DOLCE](../../raw/articles/dolce-descriptive-ontology.md) — cognitive vs realist orientation, categories as human artifacts not objective reality
- [OWL 2 Primer](../../raw/articles/owl2-primer-knowledge-representation.md) — classes, typed properties, reasoning, open-world assumption, class expressions
- [Relation Ontology](../../raw/articles/relation-ontology-obo.md) — standardized relations: part-of, precedes, derives-from, participates-in
