---
source: https://protege.stanford.edu/publications/ontology_development/ontology101.pdf
authors: Natalya F. Noy, Deborah L. McGuinness
date: 2001-01-01
type: article
quality: primary
stance: neutral
---

# Ontology Development 101: A Guide to Creating Your First Ontology

## Why Develop an Ontology?

Key reasons (from the paper):
- To share common understanding of the structure of information
- To enable reuse of domain knowledge
- To make domain assumptions explicit
- To separate domain knowledge from operational knowledge
- To analyze domain knowledge

## The 7-Step Methodology

### Step 1: Determine Domain and Scope
Define competency questions the ontology should answer:
- "What are the characteristics of a good Merlot?"
- "Which wines go well with grilled fish?"

Scope = which questions the ontology CAN answer. Equally important: which it CANNOT.

### Step 2: Consider Reusing Existing Ontologies
Before building from scratch, check if someone already formalized this domain. Libraries of reusable ontologies exist.

### Step 3: Enumerate Important Terms
List all terms relevant to the domain without worrying about overlap, relationships, or properties. Just brainstorm terms.

### Step 4: Define Classes and Class Hierarchy
Organize terms into classes using one of three approaches:
- **Top-down**: start with most general concepts, then specialize
- **Bottom-up**: start with most specific, then generalize
- **Combination**: start with most salient concepts, then generalize and specialize

Key principles:
- IS-A hierarchy: "every instance of a subclass is an instance of the superclass"
- Transitivity: if B is subclass of A and C is subclass of B, then C is subclass of A
- Single vs multiple inheritance

### Step 5: Define Properties (Slots)
Attach properties to classes. Two types:
- **Intrinsic**: flavor, color, body (of a wine)
- **Extrinsic**: name, area (of a wine)
- **Relations**: maker, grape (linking to other classes)
- **Parts**: ingredients (component relationships)

### Step 6: Define Facets (Constraints)
Constrain property values:
- **Cardinality**: how many values (single, multiple)
- **Value type**: String, Number, Boolean, Instance, Class
- **Allowed values**: enumeration of permitted values
- **Default values**: typical values

### Step 7: Create Instances
Fill in the ontology with specific individuals: "Chateau Lafite Rothschild Pauillac" is an instance of Pauillac Wine.

## Key Design Principles

1. **There is no one correct ontology** — "There is no one correct way to model a domain. The best solution depends on the application and anticipated extensions."
2. **Ontology development is iterative** — start rough, refine through use
3. **Concepts should be close to objects/relationships in your domain** — nouns become classes, verbs become relations
4. **Avoid synonyms as separate classes** — one concept = one class
5. **Naming conventions matter** — consistent prefix/suffix for classes vs properties

## Relevance to LLM Knowledge Bases

This paper defines the methodology we SHOULD have followed but didn't:

1. **Step 1 (domain + scope)**: We never defined competency questions. "What can this KB answer?" is undefined. /question addresses this retroactively.

2. **Step 3 (enumerate terms)**: We did this implicitly via /ingest concepts. But our "concepts" are LLM-identified, not domain-expert-enumerated.

3. **Step 4 (class hierarchy)**: Our wiki has NO hierarchy. All 18 articles are peers in concepts/. No IS-A relationships. "agent-memory-architectures" SHOULD be a superclass with "memgpt-pattern", "synapse-pattern", etc. as subclasses. Instead, all patterns are sections within one flat article.

4. **Step 5 (properties)**: Our wikilinks are untyped. [[memory-consolidation]] from context-management doesn't say WHETHER it's "is-part-of", "is-analogous-to", "is-prerequisite-for", or "contradicts". All links are the same.

5. **"There is no one correct ontology"**: validates our iterative approach. But we've been iterating on CONTENT without ever defining STRUCTURE.
