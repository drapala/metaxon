---
source: https://oborel.github.io/
authors: OBO Foundry Consortium
date: 2005-01-01
type: article
quality: primary
stance: neutral
---

# OBO Relation Ontology (RO)

Collection of standardized relations for cross-ontology interoperability. Part of OBO Foundry. Used by 400+ biomedical ontologies built on BFO.

## Core Relation Types

### Mereological (part-whole)
| Relation | Meaning | KB example |
|----------|---------|-----------|
| part_of | X is part of Y | memory-consolidation part_of agent-memory-architectures |
| has_part | Y has X as part | agent-memory-architectures has_part memory-consolidation |

### Temporal
| Relation | Meaning | KB example |
|----------|---------|-----------|
| precedes | X happens before Y | /ingest precedes /review |
| preceded_by | Y happens after X | /review preceded_by /ingest |
| develops_from | X develops from Y | question-taxonomy develops_from curation-anti-bias (emerged from it) |

### Participatory
| Relation | Meaning | KB example |
|----------|---------|-----------|
| participates_in | X participates in Y | reflexion-weighted-kg participates_in tension (as subject) |
| has_participant | Y has X as participant | tension has_participant reflexion-weighted-kg |

### Derivation
| Relation | Meaning | KB example |
|----------|---------|-----------|
| derives_from | X is derived from Y | kb-architecture-patterns derives_from karpathy + elvis + silveira sources |
| has_output | Process Y produces output X | /ingest has_output wiki article |
| has_input | Process Y takes input X | /ingest has_input raw/ source |

## Design Principle

Relations should be:
- **Reusable** across domains (not domain-specific)
- **Formally defined** with logical axioms
- **Composable** (chain relations: part_of + participates_in)

## Relevance to LLM Knowledge Bases

Our 114 wikilinks are ALL untyped — [[X]] means "related somehow." RO provides the vocabulary to type them:

Currently: `- [[memory-consolidation]] — memory pruning is a form of context management`
Could be: `- [[partOf:memory-consolidation]] — memory pruning is part_of cross-session context management`

The inline description after the wikilink serves as informal typing. RO would formalize it. Whether that formalization is worth the cost depends on scale — at 18 articles, probably not. At 200+, the reasoning benefits (transitive inference, inconsistency detection) become valuable.
