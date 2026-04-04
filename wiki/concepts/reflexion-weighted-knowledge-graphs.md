---
title: "Reflexion-Weighted Knowledge Graphs"
sources:
  - path: raw/papers/memgpt-llms-as-operating-systems.md
    type: paper
    quality: primary
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/hipporag-neurobiological-memory.md
    type: paper
    quality: primary
  - path: raw/papers/synapse-episodic-semantic-memory.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [synthesis, architecture, adaptive-retrieval, original-insight]
confidence: medium
resolved_patches: []
---

## Resumo

A synthesis that no individual paper proposes: agent memory should rewrite itself topologically in response to failures, not just accumulate in tiers. Combines MemGPT's storage hierarchy, Reflexion's verbal learning signal, and HippoRAG's graph retrieval into a unified concept — adaptive retrieval topology where the knowledge graph restructures based on experiential feedback.

## Conteúdo

### The Gap

Each paper solves one layer:

| Paper | Layer | What it solves | What it misses |
|-------|-------|---------------|----------------|
| MemGPT | Storage | Where to keep memory (tiers, eviction) | Eviction is mechanical (FIFO/pressure), not experience-driven |
| Reflexion | Learning | How to learn from failure (verbal reflection) | Reflections stored as flat list, no topology |
| HippoRAG | Retrieval | How to find via graph (PageRank, multi-hop) | Graph is static post-indexing, doesn't learn from usage |

### The Synthesis

Combine all three:

1. **Structure as knowledge graph** (HippoRAG): entities as nodes, relations as edges, retrieval via Personalized PageRank
2. **Reflexion feedback modifies edge weights**: when retrieval leads to failure, verbal reflection identifies which edges were misleading → those edge weights decrease
3. **Topological eviction** (MemGPT-inspired): instead of evicting by recency (FIFO), evict nodes whose edges have accumulated negative weight from repeated failures

### Concrete Example

Agent queries "deploy pipeline." HippoRAG retrieves article via PageRank. Agent uses information, fails. Reflexion generates: "article assumes AWS, but context was GCP." Instead of storing this as flat text, the reflection **modifies the edge weight** between "deploy-pipeline" and "aws" — reducing retrieval probability when context is GCP. Next query about deploy: PageRank propagates differently because the topology *learned* from the failure.

### Nearest Existing Work

Synapse comes closest: spreading activation + temporal decay (ρ=0.01). But decay is time-based, not experience-based. Temporal decay assumes older = less useful — fails for domains where foundational knowledge is old but critical.

### Caveats

CALM bias research adds a critical warning: the Reflexion feedback that modifies edges is subject to self-enhancement bias (16.1% error). The agent may generate reflections that *reinforce* retrieval patterns instead of correcting them — a degenerative positive feedback loop. Mitigation: verify against raw/ (Layer 3) before modifying edge weights.

### Mapping to This KB

| Concept | KB Equivalent |
|---------|---------------|
| Knowledge graph | Wiki with [[wikilinks]] |
| Edge weight modification | /review reescrita ativa |
| Reflexion signal | Tensions documented + patches |
| Topological eviction | /review item 9 (tension → patch or heuristic) |
| MemGPT tiers | 3 layers (_index → articles → raw/) |

**Practical implication:** /review should prioritize articles involved in /ask failures — not sweep uniformly. If /ask answered poorly and user corrected, those articles get priority in next /review. This is Reflexion-weighted review.

## Conexões

- [[agent-memory-architectures]] — MemGPT tiers and HippoRAG graph are the components being combined
- [[self-improving-agents]] — Reflexion's verbal feedback becomes the learning signal for graph adaptation
- [[retrieval-augmented-generation]] — HippoRAG's incremental edge addition is the base retrieval mechanism
- [[tension-resolution]] — tensions are the signal that edge weights should change
- [[llm-as-judge]] — self-enhancement bias is the primary risk in autonomous edge weight modification

## Fontes

- [MemGPT](../../raw/papers/memgpt-llms-as-operating-systems.md) — storage hierarchy, self-directed eviction, memory pressure mechanisms
- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — verbal feedback as learning signal, without grounding degrades to 52%
- [HippoRAG](../../raw/papers/hipporag-neurobiological-memory.md) — knowledge graph + PageRank, incremental edge addition, multi-hop retrieval
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — nearest existing work: spreading activation + temporal decay (not experience-based)
