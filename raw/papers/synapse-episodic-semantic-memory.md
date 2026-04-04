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
