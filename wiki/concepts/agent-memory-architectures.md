---
title: "Agent Memory Architectures"
sources:
  - path: raw/papers/memgpt-llms-as-operating-systems.md
    type: paper
    quality: primary
  - path: raw/papers/synapse-episodic-semantic-memory.md
    type: paper
    quality: primary
  - path: raw/articles/tim-kellogg-layers-memory-compression.md
    type: article
    quality: secondary
  - path: raw/papers/memory-age-ai-agents-survey.md
    type: paper
    quality: primary
  - path: raw/papers/hipporag-neurobiological-memory.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [memory, architecture, agent-design]
confidence: high
resolved_patches: []
---

## Resumo

Agent memory architectures define how persistent knowledge is structured, stored, and accessed across sessions. Three dominant patterns have emerged: hierarchical tiers (MemGPT/Letta), dynamic graphs (Synapse), and layered compression (Letta/Kellogg). All solve the same fundamental problem — operating within finite context windows — but differ in how they trade fidelity for space.

## Conteúdo

### Pattern 1: Hierarchical Tiers (MemGPT → Letta)

MemGPT (2023) introduced virtual context management inspired by OS memory hierarchies. The LLM agent manages its own memory through self-directed function calls.

**Memory hierarchy:**

| Tier | OS Analogy | Contents | Access |
|------|-----------|----------|--------|
| System Instructions | ROM | Prompt, function schemas | Read-only |
| Working Context | Registers | Key facts, preferences, persona | Read-write via functions |
| FIFO Queue | RAM | Rolling message history + summaries | Managed by queue manager |
| Recall Storage | SSD | Full message database, searchable | Function calls |
| Archival Storage | Disk | Arbitrary text, unbounded | Function calls |

**Key mechanisms:**
- Memory pressure warnings at 70% context capacity
- Queue eviction at 100%: flush 50%, generate recursive summary
- Agent decides what to store/retrieve/forget — self-directed, not pipeline-driven
- Heartbeat events allow autonomous internal processing chains

**Evolution to Letta (4 blocks):**
- Core Memory (always in context) → Working Context
- Message Buffer (rolling window) → FIFO Queue
- Archival Memory (unbounded) → Archival Storage
- Recall Memory (on-demand rehydration) → Recall Storage

### Pattern 2: Dynamic Graph (Synapse)

Synapse (2026) models memory as a graph where relevance emerges from spreading activation rather than static vector similarity.

**Two node types:**
- **Episodic nodes**: discrete interaction turns (text + embeddings + timestamps)
- **Semantic nodes**: abstract concepts extracted every N=5 turns (dedup at τ=0.92)

**Three edge types:** temporal (sequential), abstraction (episode↔concept), association (concept↔concept)

**Spreading activation (4 phases):**
1. Initialize: BM25 + dense retrieval anchor query nodes
2. Propagate: activation flows through edges with fan-effect normalization (prevents hub flooding)
3. Lateral inhibition: winner-take-all suppresses competing nodes (β=0.15, top-M=7)
4. Sigmoid activation: convergence in T=3 iterations

**Triple Hybrid Retrieval:** S(v) = 0.5·semantic + 0.3·activation + 0.2·PageRank

**Results (LoCoMo benchmark):**
- Avg F1: 40.5 (vs GraphRAG 18.3, MemGPT 28.0, Zep 39.7)
- 95% token reduction vs full-context methods
- 11× cost reduction, 4× faster

**Solves "Contextual Isolation":** standard RAG fails when causally related memories share no semantic overlap. Graph topology enables multi-hop traversal through "Bridge Nodes."

**Trade-off:** Lateral inhibition can suppress minor details when hub nodes activate strongly (Cognitive Tunneling).

### Pattern 3: Layered Compression (Rate-Distortion Framework)

Tim Kellogg (2025) frames agent memory as a rate-distortion problem: maximize useful signal within fixed context windows while minimizing information loss.

**Letta's 4 blocks as CPU cache analogy:**

| Block | Analogy | Capacity | Fidelity |
|-------|---------|----------|----------|
| Core Memory | L1 cache | Minimal | Zero distortion |
| Message Buffer | L2 cache | Fixed window | Lossy over time |
| Archival Memory | Disk | Unbounded | High distortion |
| Recall Memory | DMA | On-demand | Rehydration |

**Key insight:** "Compression becomes cognitive work: summarizing before archival forces understanding; searching archives requires reasoning about importance."

**Single-agent vs multi-agent compression:**
- Single-agent (Letta/Cognition): one entity manages compressed memories. Maintains coherent reasoning thread. Cognition recommends dedicated compression model.
- Multi-agent (Anthropic): parallel subagents each compress different aspects. Lead agent integrates. Reduces path-dependence. Outperforms single-agent on broad queries.
- Coordination challenge (Cognition critique): context can't be shared thoroughly across agents → "decision-making becomes too dispersed"

**Conclusion:** "Extending AI cognition requires engineering intentional forgetting. Memory becomes meaningful precisely because it isn't perfect recording."

### The Canonical Taxonomy (Memory Survey, 2025)

The "Memory in the Age of AI Agents" survey (47 authors, Dec 2025) provides the most comprehensive taxonomy:

**Key distinctions:**
- Agent memory ≠ LLM memory (parametric weights)
- Agent memory ≠ RAG (retrieval technique, not full lifecycle)
- Agent memory ≠ Context engineering (prompt management, not persistence)

**Forms (what carries memory):**

| Form | Description | Examples |
|------|-------------|---------|
| Token-level | Explicit text in context (flat/planar/hierarchical) | Chat history, MemGPT tiers, RAPTOR trees |
| Parametric | Encoded in model weights | Fine-tuning, LoRA adapters |
| Latent | Compressed representations | Embeddings, hidden states |

**Functions (why memory exists):**

| Function | What it stores |
|----------|---------------|
| Factual | World knowledge, user preferences, entity states |
| Experiential | Past solutions, strategies, skills (case/strategy/skill-based) |
| Working | Active processing buffer for current task |

**Dynamics (how memory operates):**

| Dynamic | Process |
|---------|---------|
| Formation | Summarization, distillation, graph construction, embedding, fine-tuning |
| Evolution | Consolidation, updating, forgetting (Ebbinghaus decay) |
| Retrieval | Vector similarity, graph traversal, activation-based, hybrid |

### Pattern 4: Knowledge Graph Retrieval (HippoRAG)

HippoRAG (NeurIPS 2024) models memory as a knowledge graph with Personalized PageRank retrieval, inspired by hippocampal memory indexing theory.

**Architecture:**
1. Offline: LLM OpenIE → noun phrase nodes + relation edges → schemaless KG + synonymy edges
2. Online: extract query entities → map to KG → Personalized PageRank → rank passages

**Key advantage:** incrementally adds edges (no rebuild needed, unlike RAPTOR's tree re-clustering). 10-30× cheaper, 6-13× faster than iterative methods.

**Connection to wikilinks:** Our wiki's `[[wikilinks]]` are a manually-built HippoRAG graph. Entities = articles, edges = links, retrieval = following paths from query-relevant articles.

### Mapping to This Knowledge Base

| Architecture | KB Equivalent |
|-------------|---------------|
| MemGPT Working Context | CLAUDE.md (always loaded) |
| MemGPT FIFO Queue | Current conversation context |
| MemGPT Archival | raw/ (unbounded source storage) |
| MemGPT Recall | /ask Layer 3 (on-demand raw/ verification) |
| Synapse Episodic | raw/ sources (timestamped events) |
| Synapse Semantic | wiki/concepts/ (abstract concepts extracted from episodes) |
| Synapse Activation | /ask relevance scoring via _index.md |
| Letta Core Memory | _index.md (always loaded, zero distortion) |
| Letta Archival | raw/ (unbounded, high distortion via summarization) |

## Conexões

- [[context-management]] — MemGPT's virtual context is the production implementation of bandwidth-aware retrieval
- [[memory-consolidation]] — consolidation operates on these architectures (KAIROS on MemGPT-like tiers, Dream on file-based memory)
- [[hybrid-search]] — Synapse's Triple Hybrid Retrieval parallels QMD's BM25+vector+reranking
- [[retrieval-augmented-generation]] — Synapse solves Contextual Isolation that standard RAG fails on
- [[self-improving-agents]] — all architectures enable self-improvement by persisting learned experience
- [[raptor-vs-flat-retrieval]] — RAPTOR = hierarchical tree, Synapse = dynamic graph, both beat flat retrieval

## Fontes

- [MemGPT](../../raw/papers/memgpt-llms-as-operating-systems.md) — virtual context management, OS-inspired tiers, self-directed memory operations, queue manager
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — graph memory with spreading activation, triple hybrid retrieval, 95% token reduction, LoCoMo SOTA
- [Tim Kellogg — Layers of Memory](../../raw/articles/tim-kellogg-layers-memory-compression.md) — rate-distortion framework, single vs multi-agent compression, "compression is cognition"
- [Memory in the Age of AI Agents](../../raw/papers/memory-age-ai-agents-survey.md) — canonical taxonomy: forms (token/parametric/latent), functions (factual/experiential/working), dynamics (formation/evolution/retrieval)
- [HippoRAG](../../raw/papers/hipporag-neurobiological-memory.md) — KG + PageRank retrieval: incremental, 10-30× cheaper, wikilinks as manual KG
