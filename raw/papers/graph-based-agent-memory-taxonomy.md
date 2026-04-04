---
source: https://arxiv.org/abs/2602.05665
authors: Chang Yang, Chuang Zhou, et al. (20 authors)
date: 2026-02-05
type: paper
arxiv: "2602.05665"
stance: neutral
github: https://github.com/DEEP-PolyU/Awesome-GraphMemory
---

# Graph-based Agent Memory: Taxonomy, Techniques, and Applications

## Abstract

Comprehensive survey of agent memory through graph-based lens. Taxonomy: short-term vs long-term, knowledge vs experience, non-structural vs structural. Analyzes key techniques across memory lifecycle — extraction, storage, retrieval, evolution.

## Taxonomy

### Temporal: Short-term vs Long-term
- Short-term: immediate, limited, volatile after task
- Long-term: persistent, accumulated, foundational for personalization

### Functional: Knowledge vs Experience
| Dimension | Knowledge Memory | Experience Memory |
|-----------|-----------------|-------------------|
| Nature | Passive, static, objective | Proactive, dynamic, personalized |
| Source | Pre-loaded databases | Agent interactions, trajectories, feedback |
| Purpose | Reliable factual backbone | Adaptive context learning |
| Validity | Context-independent, slowly updated | Situation-specific, rapidly evolving |

### Structural
- Non-structural: linear buffers, vector embeddings, key-value stores
- Structural: KGs, hierarchical trees, temporal graphs, hypergraphs

### Cognitive Types
Semantic (decontextualized facts), Procedural (routines), Associative (latent connections), Working (scratchpad), Episodic (chronological), Sentiment (emotional tone)

## Memory Lifecycle (4 stages)

### Extraction
NER, relation extraction, event segmentation, multimodal joint embeddings

### Storage
KGs (triples), hierarchical trees (recursive summarization), temporal graphs (bi-temporal), hypergraphs (n-ary), hybrid architectures

### Retrieval (6 operator types)
| Operator | Implementation |
|----------|---------------|
| Similarity-based | Vector embedding search |
| Rule-based | Symbolic filtering, heuristics |
| Temporal-based | Decay functions, validity windows |
| Graph-based | Traversal (intra/inter-layer) |
| RL-based | Q-function optimization |
| Agent-based | Tool integration, SQL queries |

Enhancement: multi-round (iterative refinement), post-retrieval (intermediate representation), hybrid-source (internal + external)

### Evolution
- Internal: consolidation (merge similar), graph reasoning (inference), reorganization (topology optimization)
- External: environmental feedback, active inquiry

**Topology optimization**: agents optimize graphs by increasing edge weights or creating shortcuts between correlated nodes to compile experience into more efficient structures.

## Key Insight

"Traditional memory paradigms (buffers, vectors, logs) represent degenerate graph cases." Graph-based memory is a unified framework — relationship-first modeling rather than sequential flattening.

## Benchmarks (7 categories)
Interaction, Personalization, Web, LongContext, Continual, Environments, Tool/Gen

## Challenges
- Scalability (topology explosion)
- Temporal consistency (cross-chain hallucinations)
- Conflict resolution (knowledge vs experience)
- Information loss in compression
- Cross-modal grounding
