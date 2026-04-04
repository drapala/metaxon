# Independent Review Prompt — Spot-Check 3 Wiki Articles Against Raw Sources

## Instructions

You are an independent reviewer. You did NOT write these wiki articles. Your job is to find errors, misinterpretations, and unjustified claims.

Below are 3 wiki articles from an LLM-compiled knowledge base, each followed by the raw source papers they cite. The wiki articles were written by an LLM that compiled the raw sources — you are checking its work.

For EACH article, evaluate:

### 1. Factual Accuracy
- Does the article accurately represent the numbers, results, and claims from the raw sources?
- Are any statistics wrong, exaggerated, or taken out of context?
- Flag specific claims with the exact quote from raw/ that confirms or contradicts.

### 2. Interpretation Fidelity
- Does the article's synthesis faithfully represent what the papers actually argue?
- Are there claims in the wiki that SOUND like they come from the sources but are actually the LLM's own interpretation?
- Watch for: overstatements ("proves" vs "suggests"), false generalization (result on one benchmark stated as universal), and missing caveats that the original paper included.

### 3. Semantic Convergence Check
- Does the article's writing style differ from the raw sources, or has it been homogenized into a single academic voice?
- Karpathy's source is an informal tweet thread. Does the article preserve that informality or rewrite it as formal prose?
- If all three articles sound identical in tone despite citing very different source types (tweets, academic papers, repo READMEs), that's a problem.

### 4. Missing Nuance
- What did the original papers say that the wiki articles DON'T mention?
- Are there important limitations, caveats, or failure cases from the papers that were dropped?

### 5. Unjustified Connections
- The articles contain [[wikilinks]] connecting concepts. Are any of these connections claimed but not actually supported by the underlying sources?
- Is the article making the sources say something they don't?

## Output Format

For each article, provide:
```
ARTICLE: [name]
VERDICT: ACCURATE / MOSTLY ACCURATE / INACCURATE

FACTUAL ERRORS: [list with specific quotes from raw/ that contradict]
INTERPRETATION ISSUES: [list of claims that go beyond what sources say]
MISSING NUANCE: [what the sources say that the article omits]
STYLE: [preserved / homogenized]
UNJUSTIFIED CONNECTIONS: [wikilinks that aren't supported by sources]

SEVERITY: [critical / moderate / minor]
```

Be harsh. The purpose is to find what's wrong, not to confirm the wiki is good. If everything looks correct, say so — but err on the side of flagging suspicious interpretations.

---

## Articles and Sources to Review
=== ARTICLE: agent-memory-architectures ===

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
  - path: raw/papers/coala-cognitive-architectures-language-agents.md
    type: paper
    quality: primary
  - path: raw/papers/em-llm-human-episodic-memory.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [memory, architecture, agent-design, cognitive-science]
source_quality: high
interpretation_confidence: high
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

**Critical limitation:** Eviction is mechanical (FIFO + pressure-based), not experience-driven. A memory that caused 3 consecutive retrieval failures is treated identically to one that never failed. MemGPT has no mechanism to learn from retrieval errors — it manages *space*, not *quality*. See [[reflexion-weighted-knowledge-graphs]] for a proposed architecture that addresses this gap by combining Reflexion's failure feedback with graph topology.

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

### Decision Framework: Compression vs. Associative Structure

When should an agent compress aggressively (MemGPT-style) vs. preserve full associative structure (HippoRAG-style)? The papers converge on four decision axes:

| Axis | Compress (MemGPT/Letta) | Preserve (HippoRAG/Synapse) |
|------|------------------------|----------------------------|
| **Context budget** | Tight (fixed window, no external storage) | Flexible (can page in from KG) |
| **Query pattern** | Mostly single-hop, factual recall | Multi-hop reasoning across distant memories |
| **Knowledge growth** | Slow or batch (can rebuild) | Continuous, incremental (needs edge addition) |
| **Failure cost** | Low (generic answers acceptable) | High (wrong associations cause cascading errors) |

**Hybrid position (Synapse):** 95% token reduction WITH graph topology preserved. Spreading activation + lateral inhibition achieves compression without losing associative paths. Trade-off: cognitive tunneling — hub nodes suppress minor details (β=0.15).

**Rate-distortion lens (Kellogg):** The decision is fundamentally a rate-distortion trade-off — at what compression ratio does the loss of associative structure exceed the token cost of preserving it? Aggressive compression is correct when the distortion budget is high (generic recall); structure preservation is correct when distortion must be minimized (multi-hop reasoning, causal chains).

**Practical heuristic for this KB:**
- At current scale (~16 articles): HippoRAG-style — wikilinks preserve full associative structure, context budget is not a constraint
- At 200+ articles with sub-indices: Synapse-style — spreading activation via index hierarchy provides compression with topology
- MemGPT-style compression is appropriate for ephemeral conversational memory (KAIROS/Dream), NOT for compiled knowledge (wiki articles)

### Tension: Engineering Taxonomy vs. Cognitive Science Taxonomy

CoALA (Sumers et al., 2023) bridges classical cognitive architectures (SOAR, ACT-R) with modern LLM agents, formalizing memory types from cognitive science:

| Cognitive Science (CoALA) | Engineering (Memory Survey) | Tension |
|--------------------------|---------------------------|---------|
| Episodic (specific events) | Experiential (case-based) | Overlapping but not identical — episodic is autobiographical, experiential includes abstract strategies |
| Semantic (general knowledge) | Factual (world knowledge) | Close match, but semantic memory includes learned associations, not just facts |
| Procedural (how to do things) | Experiential (skill-based) | Procedural is implicit; engineering "skills" are explicit action sequences |
| Working (active processing) | Working (current buffer) | Same concept, same name, compatible |

The cognitive science categories have decades of experimental validation. The engineering categories are pragmatic but ungrounded. Neither is wrong — they optimize for different things (explaining cognition vs. building systems).

### Tension: Concept Segmentation vs. Surprise Segmentation

EM-LLM (Fountas et al., 2024) applies human episodic memory principles to segment information not by concept (our /ingest approach) but by Bayesian surprise — points where prediction error exceeds a threshold.

| Segmentation Method | Basis | Validation |
|--------------------|-------|-----------|
| Concept-based (our /ingest) | LLM judgment: "is this a new concept?" | Pragmatic, untested against human cognition |
| Surprise-based (EM-LLM) | Statistical: `-log P(xt\|x1...xt-1) > T` | 25-35x improvement in event boundary alignment with human perception |

EM-LLM's finding: "LLM-perceived surprise can serve as a proxy for cognitive signals that drive human event segmentation." Results: 40% improvement on retrieval tasks, 30.5% over RAG on LongBench.

**Implication for this KB:** Our /ingest segments sources by concept (LLM decides where one idea ends and another begins). EM-LLM suggests segmenting by surprise (where the content shifts unexpectedly) would better match how humans organize information. These aren't mutually exclusive — concepts could be refined using surprise as a secondary signal.

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

- [[context-management]] — MemGPT's virtual context is the production implementation of bandwidth-aware retrieval; compression decision depends on context budget constraints
- [[tension-resolution]] — the RAPTOR vs HippoRAG tension (architecture-contingent) is one instance of the compress vs. preserve decision
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
- [CoALA](../../raw/papers/coala-cognitive-architectures-language-agents.md) — cognitive architecture framework: bridges SOAR/ACT-R with LLM agents, formalizes memory types from cognitive science
- [EM-LLM](../../raw/papers/em-llm-human-episodic-memory.md) — surprise-based segmentation aligned with human event perception, 40% retrieval improvement, 25-35x better boundary alignment


=== RAW SOURCE: memgpt ===
---
source: https://arxiv.org/abs/2310.08560
authors: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
date: 2023-10-12
type: paper
arxiv: "2310.08560"
---

# MemGPT: Towards LLMs as Operating Systems

## Abstract

Addresses constrained context windows via "virtual context management" inspired by OS memory hierarchies. Creates the illusion of larger memory through data movement between fast and slow storage. MemGPT manages different memory tiers and uses interrupts for control flow. Demonstrated on document analysis and multi-session chat.

## Core Architecture: Virtual Context Management

Inspired by OS virtual memory: pages are swapped between main memory (context window) and disk (external storage).

### Memory Hierarchy

| Tier | OS Analogy | Contents | Access |
|------|-----------|----------|--------|
| **System Instructions** | ROM | MemGPT prompt, function schemas | Read-only, static |
| **Working Context** | Register file | Key facts, preferences, persona | Read-write via functions |
| **FIFO Queue** | RAM | Rolling message history + summaries | Read-write via queue manager |
| **Recall Storage** | SSD/cache | Full message database, searchable | External, via function calls |
| **Archival Storage** | Disk | Arbitrary-length text objects, unbounded | External, via function calls |

### Memory Management Functions (Self-Directed)

The LLM agent has access to self-directed memory operations:
- `core_memory_append/replace`: modify working context
- `archival_memory_insert/search`: store to / retrieve from long-term storage
- `conversation_search`: search past message history
- `send_message`: communicate with user (only visible output)

### Queue Manager
    // ... 1516 lines omitted
function calls sequentially before returning control to the
    // ... 1515 lines omitted
from knowledge accumulated in prior conversations. To
    // ... 1514 lines omitted
from the LLM inference, similar to the original retrieverreader setup in Liu et al. (2023a).
    // ... 1513 lines omitted
from the user about your prior
// ... 1512 more lines (total: 1553)

=== RAW SOURCE: synapse ===
---
source: https://arxiv.org/abs/2601.02744
authors: Hanqi Jiang, Junhao Chen, Yi Pan, Ling Chen, Weihang You, Yifan Zhou, Ruidong Zhang, Andrea Sikora, Lin Zhao, Yohannes Abate, Tianming Liu
date: 2026-01-06
type: paper
arxiv: "2601.02744"
---

# SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation

## Abstract

Standard RAG systems fail to address the disconnected nature of long-term agentic memory. Synapse models memory as a dynamic graph where relevance emerges from spreading activation rather than pre-computed links. Integrates lateral inhibition and temporal decay. Triple Hybrid Retrieval fuses geometric embeddings with activation-based graph traversal. Significantly outperforms SOTA on LoCoMo benchmark in complex temporal and multi-hop reasoning tasks.

## Architecture: Unified Episodic-Semantic Graph

Graph 𝒢=(𝒱,ℰ) with two node types:

- **Episodic Nodes** (𝒱_E): Discrete interaction turns with textual content, dense embeddings (all-MiniLM-L6-v2), and timestamps
- **Semantic Nodes** (𝒱_S): Abstract concepts (entities, preferences) extracted via LLM every N=5 turns; dedup at similarity threshold τ_dup=0.92

**Edge Types:**
1. Temporal Edges: link sequential episodes
2. Abstraction Edges: bidirectionally connect episodes to concepts
3. Association Edges: model latent correlations between semantic nodes

Scalability: top-K edge pruning (K=15) and node garbage collection maintain active graph ≤10,000 nodes.

## Spreading Activation Mechanism

4 sequential phases instead of static vector similarity:

### 1. Initialization (Dual Trigger)
- Lexical Trigger: BM25 sparse retrieval for named entities
- Semantic Trigger: Dense retrieval for conceptual similarity

### 2. Propagation with Fan Effect
u_i^(t+1) = (1-δ)·a_i^(t) + Σ_{j∈N(i)} [S·w_{ji}·a_j^(t)]/fan(j)
- S=0.8 (spreading factor), fan(j) = out-degree normalizes hub influence
- Temporal decay: w_{ji} = e^{-ρ|τ_i-τ_j|} (ρ=0.01)

### 3. Lateral Inhibition
Winner-take-all competition suppresses competing nodes (β=0.15, top-M=7). Enforces sparsity and filters noise.

### 4. Sigmoid Activation
Stability in T=3 iterations with δ=0.5 retention.

## Triple Hybrid Retrieval

S(v_i) = λ_1·sim(h_i, h_q) + λ_2·a_i^(T) + λ_3·PageRank(v_i)
- λ={0.5, 0.3, 0.2} (Semantic, Activation, Structural)
- Top-k=30 nodes, reordered topologically
- Scores cached, updated only during consolidation (N=5 turns)

## The Contextual Isolation Problem

Standard RAG assumes relevance = semantic proximity to query. Fails for causal or transitive reasoning. Example: "Why am I anxious?" — vector search finds "anxiety" mentions but misses a schedule conflict logged weeks prior (the root cause shares no lexical/embedding overlap). Synapse resolves via graph topology: causally connected information through intermediate "Bridge Nodes."

## LoCoMo Benchmark Results

| Method | Multi-Hop F1 | Temporal F1 | Open Domain F1 | Single-Hop F1 | Adversarial F1 | Avg F1 |
|--------|-------------|------------|----------------|--------------|----------------|--------|
| **Synapse** | **35.7** | **50.1** | **25.9** | **48.9** | **96.6** | **40.5** |
| Zep | 35.5 | 48.5 | 23.1 | 48.0 | 65.4 | 39.7 |
| MemoryOS | 35.3 | 41.2 | 20.0 | 48.6 | — | 38.0 |
| A-Mem | 27.0 | 45.9 | 12.1 | 44.7 | 50.0 | 33.3 |
| MemGPT | 26.7 | 25.5 | 9.2 | 41.0 | 43.3 | 28.0 |
| GraphRAG | 16.5 | 22.4 | 10.1 | 24.5 | 15.2 | 18.3 |
| Vectors Only | 27.5 | 14.7 | — | — | — | 25.2 |

## Ablation: What Matters Most

| Removed | Avg F1 | Drop |
|---------|--------|------|
| Full Synapse | 40.5 | — |
| (-) Node Decay | 30.7 | -9.8 |
| (-) Activation Dynamics | 30.5 | -10.0 |
| (-) Graph Structure | 32.9 | -7.6 |
| (-) Fan Effect | 36.1 | -4.4 |
| (-) Lateral Inhibition | 39.4 | -1.1 |

Node decay is the sole temporal reasoning driver. Graph structure outperforms vector-only by 15.3 points.

## Efficiency

| Method | Tokens | Latency | Cost/1k | F1 | Cost Efficiency |
|--------|--------|---------|---------|-----|-----------------|
| Synapse | ~814 | 1.9s | $0.24 | 40.5 | 167.3 |
| MemGPT | ~16,977 | 8.5s | $2.67 | 28.0 | 10.5 |

95% token reduction vs full-context. 11× cost reduction. 4× faster.

## Limitation: Cognitive Tunneling

Lateral inhibition can suppress minor details when hub nodes activate strongly. Trade-off: aggressive sparsity improves complex reasoning but occasionally prunes edge-case facts.


=== ARTICLE: retrieval-augmented-generation ===
---
title: "Retrieval-Augmented Generation"
sources:
  - path: raw/papers/long-context-vs-rag-evaluation.md
    type: paper
    quality: primary
  - path: raw/papers/raptor-recursive-abstractive-retrieval.md
    type: paper
    quality: primary
  - path: raw/papers/hipporag-neurobiological-memory.md
    type: paper
    quality: primary
  - path: raw/papers/self-rag-retrieve-generate-critique.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [retrieval, rag, long-context, evaluation]
source_quality: high
interpretation_confidence: high
resolved_patches: []
---

## Resumo

Retrieval-Augmented Generation (RAG) augments LLM responses by retrieving relevant documents from an external corpus before generation. A December 2024 evaluation of ~13,600 questions found that long context (LC) outperforms RAG overall (56.3% vs 49.0%), but RAG retains irreplaceable value for ~10% of questions — particularly dialogue-based contexts and open-ended queries. Neither approach dominates universally; hybrid strategies are recommended.

## Conteúdo

### LC vs. RAG: Head-to-Head

| Metric | Long Context | RAG |
|--------|-------------|-----|
| Overall accuracy | 56.3% | 49.0% |
| Questions won exclusively | 3,433 | 1,843 |
| Questions answered exclusively | — | ~10% |

### When LC Wins

- Wikipedia and narrative sources (dense, well-structured content)
- Factual questions ("Who?", "Where?")
- Content where information is distributed across the full document

### When RAG Wins

- Dialogue-based contexts (naturally segmented)
- General search queries
- Open-ended questions ("How?")
- When relevant information is concentrated in specific chunks

### Retriever Comparison

| Retriever Type | Accuracy | Example |
|---------------|----------|---------|
| Chunk-based | 20-22% | Traditional chunking |
| Index-based | 30-36% | BM25, sparse retrieval |
| Summarization-based (RAPTOR) | 38.5% | Hierarchical summarization |

RAPTOR (summarization-based) significantly outperformed chunk-based approaches — suggesting that the quality of retrieved content matters more than retrieval method sophistication.

### RAPTOR: How Summarization-Based Retrieval Works

RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) constructs a hierarchical tree from documents:

1. Segment into 100-token chunks → embed with SBERT
2. Cluster similar chunks via Gaussian Mixture Models (soft clustering — nodes can belong to multiple clusters)
3. Summarize each cluster via LLM
4. Re-embed summaries → repeat until no further clustering feasible

This creates a multi-level tree: raw chunks at the bottom, progressively abstract summaries at each level above. Average compression ratio: 0.28 (72% compression per level).

**Two retrieval strategies:**
- **Collapsed Tree** (superior): flatten the tree, retrieve nodes by cosine similarity across all levels
- **Tree Traversal**: start at root, descend through layers. More structured, less flexible.

**Results (with GPT-4):**

| Dataset | RAPTOR | Previous SOTA | Gain |
|---------|--------|---------------|------|
| QuALITY | 82.6% | 62.3% | +20.3 pp |
| QASPER | 55.7% | 53.9% | +1.8 pp |
| NarrativeQA | 30.8% ROUGE-L | 23.5% | +7.3 pp |

Non-leaf (summary) nodes contribute 23-57% of retrieved content depending on dataset — confirming that hierarchical summaries capture information that flat chunking misses.

Hallucination rate in tree nodes: only 4% (minor), and hallucinations did not propagate to parent nodes.

### HippoRAG: Graph-Based Retrieval via PageRank

HippoRAG (NeurIPS 2024) takes a different approach: instead of summarization trees (RAPTOR), it builds a knowledge graph and retrieves via Personalized PageRank.

**Architecture:**
1. Offline: LLM extracts (entity, relation, entity) triples → schemaless knowledge graph
2. Online: extract query entities → map to graph → Personalized PageRank from query nodes → rank passages

**Results:** +20% on 2WikiMultiHopQA, 10-30× cheaper and 6-13× faster than iterative methods (IRCoT). Single-step multi-hop retrieval via graph associations.

**Key advantage over RAPTOR:** HippoRAG "can continuously integrate new knowledge by simply adding edges" — no tree rebuild needed. Closer to our /ingest pattern (incremental addition). RAPTOR requires re-clustering on new content.

**Relevance to our wiki:** Our [[wikilinks]] are effectively a manually-built HippoRAG knowledge graph. Entities = concept articles, edges = wikilinks, retrieval = following links from query-relevant articles. PageRank could inform a future /search scoring system.

### Self-RAG: Structured Self-Critique During Retrieval

Self-RAG (Asai et al., 2023) adds reflection tokens inline during generation:

| Token | Question | When |
|-------|----------|------|
| [Retrieve] | Should I retrieve now? | Before each generation step |
| [IsRel] | Is the retrieved passage relevant? | After retrieval |
| [IsSup] | Is my response supported by the passage? | After generation |
| [IsUse] | Is the response useful? (1-5) | Final check |

The model learns WHEN to retrieve (not always), WHAT is relevant (not all content), and WHETHER its response is supported (not blindly trusting itself).

**Mapping to our /ask:**
- After Layer 1: "are these the right articles?" → [IsRel] equivalent
- After Layer 2: "is my synthesis supported by what I read?" → [IsSup] equivalent
- After Layer 3: "did raw/ verification change my answer?" → structured reflection

Self-RAG formalizes our circuit breaker as explicit checkpoints rather than implicit judgment. A /ask that logged these reflection decisions would make the retrieval process traceable and debuggable.

### Error Patterns

**RAG failures:**
- Retrieval failures (relevant chunks not found)
- Misinterpretation of fragmented context
- Information spanning multiple chunks is lost

**LC failures:**
- Question misinterpretation
- Semantic specificity issues (confusing related but distinct concepts)
- Noise in long contexts dilutes attention

### The "Context Relevance" Insight

A critical finding: synthetic long contexts (concatenated passages with noise) often mirror RAG pipelines, introducing evaluation bias. Fair comparison requires distinguishing:
- Realistic long texts (novels, papers)
- Synthetic contexts (concatenated passages)

### Implications for Knowledge Bases

For an LLM KB at small scale (~100-200 articles):
- **LC approach works well** — load the index + relevant articles into context
- **No RAG needed yet** — Karpathy's finding confirmed by this paper

At larger scale:
- **Hybrid approach** — use [[hybrid-search]] (QMD) to retrieve relevant chunks, then load into context
- The 3-layer retrieval pattern (index → articles → raw) is effectively a manual RAG with human-designed relevance

### Definition Ambiguity

No consensus on what constitutes "long context":
- Studies use thresholds from 8K to 128K tokens
- Model capabilities evolve faster than benchmarks

## Conexões

- [[llm-knowledge-base]] — the KB uses LC at small scale, needs RAG at larger scale
- [[hybrid-search]] — QMD implements the hybrid retrieval approach this paper recommends
- [[context-management]] — compaction strategies are relevant when LC approaches hit token limits
- [[raptor-vs-flat-retrieval]] — RAPTOR compared against our 3-layer flat pattern
- [[kb-architecture-patterns]] — RAPTOR validates Pattern 4 and the _index.md summarization layer

## Fontes

- [Long Context vs. RAG](../../raw/papers/long-context-vs-rag-evaluation.md) — systematic evaluation: ~13,600 questions, 12 QA datasets, retriever comparison, error analysis
- [RAPTOR](../../raw/papers/raptor-recursive-abstractive-retrieval.md) — hierarchical tree retrieval: recursive clustering + summarization, +20pp on QuALITY, 4% hallucination rate
- [HippoRAG](../../raw/papers/hipporag-neurobiological-memory.md) — graph-based retrieval: KG + PageRank, +20% on 2WikiMultiHopQA, 10-30× cheaper than iterative, incremental updates
- [Self-RAG](../../raw/papers/self-rag-retrieve-generate-critique.md) — structured reflection tokens: [Retrieve], [IsRel], [IsSup], [IsUse] — formalizes retrieval self-critique as traceable checkpoints


=== RAW SOURCE: long-context-vs-rag ===
---
source: https://arxiv.org/abs/2501.01880
authors: Xinze Li, Yixin Cao, Yubo Ma, Aixin Sun
date: 2024-12-27
type: paper
arxiv: "2501.01880"
---

# Long Context vs. RAG for LLMs: An Evaluation and Revisits

## Abstract

The paper examines two complementary approaches for incorporating extended external information into language models. The authors revisit recent studies on this topic, highlighting key insights and discrepancies, and conduct a broader evaluation by excluding questions answerable from existing knowledge, identifying superior retrieval techniques, and using expanded benchmark datasets.

Key findings: extended context windows generally surpass RAG in question-answering tasks, particularly for Wikipedia queries. However, RAG shows benefits for dialogue-based and general search queries. The authors emphasize the overlooked importance of context relevance in existing studies.

## Key Contributions

1. Survey of existing studies analyzing implementations and disagreements between LC and RAG research
2. Fair evaluation framework filtering out questions answerable from parametric knowledge alone
3. Best retriever identification through systematic comparison of chunk-based, index-based, and summarization-based methods
4. Dataset expansion from ~2,000 to ~20,000 questions for statistical robustness

## Main Findings

### Performance Results

- LC correctly answers 56.3% of filtered questions versus RAG's 49.0%
- LC outperforms on 3,433 questions; RAG on 1,843 (loose evaluation)
- Nearly 10% of questions answered exclusively by RAG, indicating irreplaceable value

### Contextual Strengths

- LC excels with Wikipedia and narrative sources, particularly for dense, well-structured content
- RAG demonstrates advantages with dialogue-based contexts and naturally segmented information
- LC performs better for factual questions ("Who," "Where"); RAG comparable for open-ended queries ("How")

### Retriever Analysis

RAPTOR (summarization-based) outperformed alternatives with 38.5% correct answers, exceeding chunk-based retrievers (20-22%) and matching/exceeding index-based approaches (30-36%).

## Critical Discussion Points

### Context Relevance

Distinguishing between realistic long texts (novels, papers) and synthetic contexts (concatenated passages with noise) proves essential. Synthetic long contexts often mirror RAG pipelines, potentially introducing bias.

### Definition Ambiguity

Studies lack consensus on what constitutes "long context," with thresholds ranging from 8K to 128K tokens depending on research focus and model capabilities.

### Framework Considerations

Three key dimensions shape fair comparisons:
- Context length
- Context relevance
- Experimental settings (short RAG vs. long input; long RAG vs. long input; RAG over increasing context)

## Error Analysis

**RAG failures:** Primary issues include retrieval failures and misinterpretation of fragmented context, particularly when relevant information spans multiple chunks.

**LC failures:** Tend toward question misinterpretation and semantic specificity issues, struggling to distinguish between related but distinct concepts in noisy contexts.

## Implications

Neither approach universally dominates. Performance depends heavily on:
- Knowledge source characteristics
- Question type and reasoning requirements
- Information density and segmentation patterns
- Model architecture and size variations

The authors advocate for hybrid strategies and context-aware selection between approaches rather than blanket adoption of either method.

## Limitations

Focuses exclusively on text-based contexts. Examines only retrievers present in compared papers. Rapid model evolution may alter comparative outcomes.

---

*Nota: conteúdo transcrito via web fetch do HTML do arxiv — consultar PDF original para tabelas, figuras e dados completos.*


=== RAW SOURCE: raptor ===
---
source: https://arxiv.org/abs/2401.18059
authors: Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, Christopher D. Manning
date: 2024-01-31
type: paper
arxiv: "2401.18059"
---

# RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

## Abstract

RAPTOR addresses limitations in retrieval-augmented language models by proposing a hierarchical approach. Rather than retrieving only brief text segments, the method recursively embeds, clusters, and summarizes document chunks into a multi-level tree structure. At inference time, the system retrieves relevant information across lengthy documents at varying levels of detail. Coupling RAPTOR retrieval with GPT-4 improves the best performance on the QuALITY benchmark by 20% in absolute accuracy.

## Core Method

### Tree Construction Process

1. Segment documents into 100-token chunks, preserving sentence boundaries
2. Embed chunks using SBERT (multi-qa-mpnet-base-cos-v1)
3. **Cluster** similar chunks using Gaussian Mixture Models (GMMs) with soft clustering (nodes can belong to multiple clusters)
4. **Summarize** each cluster via GPT-3.5-turbo
5. **Re-embed** summaries
6. **Repeat** until no further clustering is feasible

Bottom-up process creates a multi-layer tree where parent nodes contain summaries of child clusters.

### Clustering Details

- UMAP for dimensionality reduction before GMM
- Bayesian Information Criterion (BIC) determines optimal cluster numbers
- Two-step: global clusters first, then local clustering within them
- Average compression ratio: 0.28 (72% compression — summary/child content)

### Retrieval Strategies

**Collapsed Tree** (superior performance):
- Flattens entire tree structure
- Retrieves nodes via cosine similarity to query embedding
- Accumulates nodes until token limit (default 2000 tokens)
- Allows flexible selection across all abstraction levels

**Tree Traversal**:
- Starts at root, selects top-k nodes
- Progressively descends through child layers
- More structured but less flexible

## Experimental Results

### Performance

| Dataset | RAPTOR + GPT-4 | Previous SOTA | Improvement |
|---------|----------------|---------------|-------------|
| QuALITY (accuracy) | 82.6% | 62.3% (CoLISA) | +20.3 pp |
| QASPER (F-1) | 55.7% | 53.9% (CoLT5 XL) | +1.8 pp |
| NarrativeQA (ROUGE-L) | 30.8% | 23.5% (BM25) | +7.3 pp |

### Layer Contribution

Non-leaf nodes contribute substantially to retrieval:
- NarrativeQA (DPR): 57.4% of retrieved nodes from non-leaf layers
- QuALITY (DPR): 32.3% from non-leaf layers
- QASPER (DPR): 23% from non-leaf layers

Performance improved when querying full tree vs single layers, confirming "hierarchical summaries offer benefits that contiguous chunk methods cannot match."

### Hallucination Analysis

Of 150 sampled nodes, only 4% contained minor hallucinations (adding information not in source). Hallucinations did not propagate to parent nodes and had no impact on QA performance.

### Computational Efficiency

- Token expenditure scales linearly with document length
- Build time increases linearly (feasible on consumer hardware)

## Key Insight

RAPTOR's advantage over flat chunking: "integrating information across lengthy documents at different levels of abstraction." For multi-hop questions requiring synthesis across distant parts of a document, RAPTOR retrieves comprehensive context while traditional retrievers return narrow, localized chunks.

## Relevance to Knowledge Bases

The `_index.md` pattern in an LLM knowledge base is effectively a manual RAPTOR tree:
- Level 0: raw source chunks (raw/)
- Level 1: wiki articles with summaries (wiki/concepts/)
- Level 2: index pointers (~150 chars each) (_index.md)

The key difference: RAPTOR automates the tree construction via clustering + summarization, while a KB relies on LLM-guided concept extraction. Both achieve the same goal — multi-level abstraction for retrieval.


=== ARTICLE: self-improving-agents ===
---
title: "Self-Improving Agents"
sources:
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/self-evolving-agents-survey.md
    type: paper
    quality: primary
  - path: raw/papers/textgrad-automatic-differentiation-text.md
    type: paper
    quality: primary
  - path: raw/papers/promptbreeder-self-referential-improvement.md
    type: paper
    quality: primary
  - path: raw/papers/absolute-zero-reinforced-self-play.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [agent-architecture, self-improvement, reflection, learning]
source_quality: high
interpretation_confidence: high
resolved_patches: []
---

## Resumo

Self-improving agents learn from experience without weight updates, using verbal reflection, heuristic generation, or feedback loops to improve future performance. Two foundational approaches: Reflexion (reflect on failures → store in episodic memory → retry) and ERL (reflect on outcomes → generate reusable heuristics → retrieve for future tasks). A critical finding: abstracted heuristics transfer better than raw trajectories.

## Conteúdo

### The Core Problem

LLM agents make the same mistakes repeatedly across sessions. Traditional RL requires weight updates (expensive, unstable). Self-improving agents use the LLM's own language capabilities to learn from experience within the context window.

### Reflexion: Learning from Failure via Verbal Reflection

**Architecture (3 components):**
- **Actor**: LLM generates actions
- **Evaluator**: scores outputs (exact match, heuristics, or LLM-based)
- **Self-Reflection**: generates verbal feedback analyzing failures → actionable insights

**Loop:** trajectory → evaluation → verbal reflection → memory update → retry

**Memory:**
- Short-term: current trajectory (fine-grained)
- Long-term: stored self-reflections (1-3 experiences, bounded by context)

**Key insight:** Converts scalar/binary feedback into verbal feedback — "action A_i led to incorrect A_{i+1}" with suggested alternatives. Mimics human learning from mistakes.

**Results:**
- HumanEval Python: 80.1% (GPT-4) → 91.0% (Reflexion)
- AlfWorld: +22% absolute over ReAct (130/134 tasks in 12 iterations)
- HotPotQA: CoT 0.61 → 0.75 (+14%)

**Ablation:** Self-reflection without grounded feedback (tests) degrades to 52%. Trajectory replay without reflection: no improvement. Verbal reflection outperforms episodic memory by 8%. Critically, Reflexion's "grounded feedback" means **executable tests** — not document verification by the same LLM. This distinction matters for KB systems where Layer 3 raw/ verification is read by the same model that wrote the wiki (see [[autonomous-kb-failure-modes]] "The Layer 3 Circularity Problem").

### ERL: Heuristics > Trajectories

**Framework (2 stages):**
1. Post-task: reflect on outcomes → generate structured heuristics with trigger conditions
2. New task: LLM-based retrieval of relevant heuristics → inject into system prompt

**Critical finding:**

| Approach | Performance |
|----------|------------|
| Raw trajectories (few-shot) | -1.9% vs baseline (WORSE) |
| Heuristics (ERL) | +7.8% vs baseline |

Heuristics provide "distilled strategic principles that generalize across tasks." Trajectories are too specific and can hurt. Example heuristic: "When sending emails to attendees, first resolve names to email addresses via Contacts tool."

**Selective retrieval matters:**
- Random inclusion peaks at 40-60 heuristics then degrades
- LLM-based retrieval (k=20): 56.1% — best
- Failure-derived heuristics excel on Search (+14.3%)
- Success-derived heuristics optimize Execution (+9.0%)

### The Spectrum of Self-Improvement

| Method | What's stored | Granularity | Transfer |
|--------|--------------|-------------|----------|
| Reflexion | Verbal self-reflections | Per-failure | Same task (retry) |
| ERL | Abstracted heuristics | Per-outcome | Cross-task |
| Agent KB | Structured experiences | Per-trajectory | Cross-framework |
| Agent KB | Structured experiences | Per-trajectory | Cross-framework |
| KAIROS/Dream | Memory consolidation | Per-session | Cross-session |

### TextGrad: Optimizing via Textual Feedback

TextGrad treats LLM-generated textual feedback as "gradients" flowing backward through a computational graph. Each component (prompt, code, molecule) receives targeted natural language criticism and improves iteratively. Follows PyTorch conventions (Variable, loss function, optimizer).

| PyTorch | TextGrad |
|---------|----------|
| Tensor | Variable (text string) |
| Loss function | Evaluation prompt |
| Gradient | Textual feedback from LLM |
| Optimizer.step() | Apply feedback to update variable |

Results: +20% relative gains on coding problems, improved GPT-4o zero-shot QA. Applicable beyond agents — optimizes any text-based component.

**Relevance:** TextGrad automates the evaluate → feedback → update loop. Our patch system is manual TextGrad; a future /lint could implement automated textual gradient feedback on wiki articles.

### The Self-Evolving Agent Taxonomy

The Self-Evolving Agents survey (2025) provides the broadest taxonomy, organizing self-improvement across three dimensions:

**What to evolve:** model parameters, memory, tools/skills, prompts

**When to evolve:**
- Pre-deployment (training-time adaptation)
- During execution (in-context learning, reflection) ← Reflexion
- Post-execution (experience consolidation) ← ERL, KAIROS
- Continuous (ongoing background evolution) ← auto-dream

**How to evolve:**
- Self-reflection (Reflexion, ERL)
- Reinforcement learning (reward-driven)
- Evolutionary methods (Promptbreeder)
- Knowledge transfer (cross-domain, Agent KB)
- Synthetic data generation (Absolute Zero)

Our KB maps to this taxonomy: /ingest = pre-deployment, /ask = during execution, /review = post-execution, /dream = continuous.

### Promptbreeder: Self-Referential Prompt Evolution

Evolutionary approach: population of (task prompt, mutation prompt) pairs. The mutation prompt mutates the task prompt; both are selected by fitness. Self-referential: the system evolves the tools that evolve the prompts, preventing stagnation. Outperforms Chain-of-Thought on reasoning benchmarks.

**Relevance:** Our /ingest and /ask prompts are static (hand-written in CLAUDE.md). Promptbreeder-style evolution could optimize them based on /ask quality metrics. Fase 3 potential.

### Absolute Zero: Self-Play Without Data

Models autonomously generate training tasks and improve reasoning via RL. Code execution provides a cheap, reliable, scalable reward signal — no human annotation needed. Surpasses baselines using tens of thousands of human-annotated examples.

**Relevance:** A self-improving KB could use self-play: agent generates questions about its own wiki → attempts to answer → evaluates against raw/ → uses feedback to improve articles and retrieval. This would automate the /ask → evaluate → /review cycle entirely.

### Relevance to This Knowledge Base

Our pipeline already implements self-improvement patterns:
- **Patch system** (`> [!patch]`) = manual Reflexion: identify error → verbal feedback → incorporate
- **/review reescrita ativa** = automated ERL: reflect on wiki state → generate improvements → apply
- **Heuristics > trajectories** validates our design: concept-based articles (heuristics) > raw source dumps (trajectories)

## Conexões

- [[memory-consolidation]] — KAIROS/Dream is self-improvement across sessions; Reflexion is within-task
- [[kb-architecture-patterns]] — ERL validates Pattern 1 (concept articles > raw sources)
- [[autonomous-research-agents]] — Deep Research pipeline could use Reflexion for iterative query refinement
- [[context-management]] — self-reflection memories compete for context budget
- [[llm-as-judge]] — 12 biases affect self-evaluation loops; self-enhancement (16.1%) is the central risk
- [[agent-memory-architectures]] — memory structures that enable self-improvement
- [[multi-agent-orchestration]] — Agent KB enables cross-framework knowledge transfer

## Fontes

- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — verbal RL: 91% HumanEval, +22% AlfWorld, reflection > replay by 8%
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — heuristics > trajectories: +7.8% Gaia2, selective retrieval critical, failure heuristics excel on search
- [Self-Evolving Agents Survey](../../raw/papers/self-evolving-agents-survey.md) — broadest taxonomy: what/when/how to evolve, covers models, memory, tools, prompts
- [TextGrad](../../raw/papers/textgrad-automatic-differentiation-text.md) — textual gradients as optimization: PyTorch-style feedback loop, +20% coding gains
- [Promptbreeder](../../raw/papers/promptbreeder-self-referential-improvement.md) — self-referential prompt evolution: evolves both task prompts and mutation prompts
- [Absolute Zero](../../raw/papers/absolute-zero-reinforced-self-play.md) — self-play reasoning with zero data: code execution as reward signal, surpasses human-annotated baselines


=== RAW SOURCE: reflexion ===
---
source: https://arxiv.org/abs/2303.11366
authors: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
date: 2023-03-20
type: paper
arxiv: "2303.11366"
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

## Abstract

Introduces Reflexion, which reinforces language agents through linguistic feedback rather than weight updates. Agents verbally reflect on task feedback signals and maintain reflective text in memory to improve future decisions. Achieves 91% pass@1 on HumanEval (surpassing GPT-4's 80%).

## Core Architecture (3 Components)

- **Actor (M_a)**: LLM that generates text/actions conditioned on state observations + memory
- **Evaluator (M_e)**: Scores outputs using task-specific metrics (exact match, heuristics, LLM-based)
- **Self-Reflection (M_sr)**: Generates verbal feedback analyzing trajectory failures → actionable insights

### Memory Structure

- **Short-term**: current trajectory history (fine-grained recent details)
- **Long-term**: stored self-reflections from prior trials (bounded to 1-3 experiences)

### Iterative Loop

trajectory generation → evaluation → verbal reflection → memory update → retry

When evaluator deems performance inadequate, agent generates reflection analyzing failure, stores as linguistic experience, attempts task again with augmented context.

## Verbal Reinforcement Mechanism
// ... 35 more lines (total: 67)

=== RAW SOURCE: erl ===
---
source: https://arxiv.org/abs/2603.24639
authors: Marc-Antoine Allard, Arnaud Teinturier, Victor Xing, Gautier Viaud
date: 2026-03-25
type: paper
arxiv: "2603.24639"
---

# ERL: Experiential Reflective Learning for Self-Improving LLM Agents

## Abstract

Agents struggle to adapt to specialized environments and don't leverage past interactions. ERL enables improvement through experience: reflect on outcomes → generate reusable heuristics → retrieve and apply to future tasks. +7.8% over ReAct on Gaia2. Selective heuristic retrieval outperforms reusing trajectories.

## Framework (2 Stages)

### 1. Heuristic Generation (post-task)

After execution, agents reflect on trajectories and outcomes to create structured heuristics:
- Analysis identifying success/failure causes
- Actionable guidelines with explicit trigger conditions and recommended actions

Example: "When sending emails to calendar attendees, first resolve names to email addresses via the Contacts tool"

### 2. Retrieval-Augmented Execution (new tasks)

LLM scores stored heuristics for relevance, injects top-k into system prompt.

## Heuristics vs. Trajectories (Critical Finding)

| Approach | Execution | Search | Overall |
|----------|-----------|--------|---------|
| Raw trajectories (few-shot) | -1.9% vs baseline | — | Worse |
| Heuristics (ERL) | +5.5% | +23.8% | +7.8% |

Heuristics provide "distilled strategic principles that generalize across tasks" rather than task-specific examples. Raw trajectories fail to improve and can hurt performance.

## Gaia2 Benchmark Results

| Method | Execution | Search | Overall |
|--------|-----------|--------|---------|
| Baseline (ReAct) | 43.1% | 53.6% | 48.3% |
| Few-shot | 41.7% | 51.2% | 46.4% |
| ExpeL | 45.8% | 56.0% | 50.9% |
| **ERL** | **51.4%** | **60.7%** | **56.1%** |

## Selective Retrieval Findings

- Random selection peaks at 40-60 heuristics then degrades — indiscriminate inclusion is counterproductive
- LLM-based retrieval (k=20): 56.1% — best
- Embedding-based retrieval (k=20): 53.3%
- Failure-derived heuristics excel on Search (+14.3%)
- Success-derived heuristics optimize Execution (+9.0%)

## Cost

ERL incurs 40% increased API costs due to ~20k tokens of heuristics appended per turn. Prompt caching partially mitigates.

## Relevance to Knowledge Bases

ERL's heuristic generation is the academic formalization of our /review reescrita ativa: reflect on wiki state → generate actionable guidelines → apply to future /ask and /ingest. The finding that heuristics > trajectories validates our design choice of concept-based articles over raw source dumps.

