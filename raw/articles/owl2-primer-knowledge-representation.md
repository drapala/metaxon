---
source: https://www.w3.org/TR/owl2-primer/
authors: W3C OWL Working Group
date: 2012-12-11
type: article
quality: primary
stance: neutral
---

# OWL 2 Primer: Web Ontology Language

## What OWL 2 Provides

Formal framework for expressing ontologies — computational artifacts with precise statements about a domain. Enables machines to REASON automatically: verify consistency, derive new facts from existing information.

## 3 Building Blocks

| Entity | What it is | Example |
|--------|-----------|---------|
| **Class** | Groups related individuals (conceptual category) | Person, Wine, WikiArticle |
| **Property** | Defines relationships | hasWife (object), hasAge (data), creator (annotation) |
| **Individual** | Specific object in domain | Mary, Chateau Lafite, memory-consolidation.md |

## Property Types

**Object properties**: connect individuals to individuals (hasAuthor, cites, contradictsClaimOf)
**Datatype properties**: connect individuals to data values (hasConfidence, hasWordCount)
**Annotation properties**: metadata about the ontology itself (rdfs:comment, dc:creator)

## Class Expressions (Logic)

| Expression | What it does | Example |
|-----------|-------------|---------|
| Intersection (AND) | Both conditions | SynthesisArticle AND HasPriorWork |
| Union (OR) | Either condition | Confirming OR Challenging |
| Complement (NOT) | Negation | NOT EmpiricallyTested |
| Existential (∃) | Has at least one | hasTension some KnownTension |
| Universal (∀) | All values from | hasSource only PrimarySource |
| Cardinality | Exact/min/max count | hasSource min 2 |

## Property Characteristics

| Feature | Meaning | KB example |
|---------|---------|-----------|
| Symmetry | If A→B then B→A | contradicts (if A contradicts B, B contradicts A) |
| Asymmetry | If A→B then NOT B→A | isSubconceptOf |
| Transitivity | If A→B→C then A→C | isPartOf chains |
| Inverse | P and Q are inverses | cites / isCitedBy |
| Functionality | At most one value | hasMainTopic (each article has one primary topic) |

## Open-World Assumption

Missing facts aren't false — they're UNKNOWN. This suits KBs where information is incomplete. Contrasts with databases (closed-world: absence = falsehood).

## Relevance to LLM Knowledge Bases

OWL provides the formal language for what our wikilinks currently lack:

1. **Typed links**: Instead of [[memory-consolidation]] (untyped), we could express:
   - `context-management partOf agent-memory-architectures`
   - `rag contradicts llm-knowledge-base ON "need for RAG at small scale"`
   - `reflexion-weighted-kg derivedFrom memgpt AND reflexion AND hipporag`

2. **Reasoning**: If we type relationships, an OWL reasoner could automatically:
   - Detect inconsistencies (article claims X, but linked article claims NOT X)
   - Infer missing links (if A partOf B and B partOf C, then A partOf C)
   - Classify articles (any article with 2+ primary sources AND no prior work challenge = high confidence)

3. **Open-world assumption**: matches our retrieval skepticism — absence of evidence ≠ evidence of absence. When /ask doesn't find an article, it means we don't know, not that the answer is no.

4. **Practical limitation**: Obsidian wikilinks are untyped strings. Full OWL would require different tooling. But we CAN approximate typed links via conventions: `[[partOf:memory-consolidation]]` or frontmatter relation arrays.
