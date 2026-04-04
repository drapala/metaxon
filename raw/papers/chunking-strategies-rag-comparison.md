---
source: https://arxiv.org/abs/2504.19754
authors: Various (NVIDIA benchmark + multiple studies)
date: 2025-04-01
type: paper
stance: challenging
---

# Chunking Strategies for RAG: Comparative Benchmarks

## Key Benchmark Results (2024-2025)

### NVIDIA Study
- Page-level chunking: 0.648 accuracy (won)
- Factoid queries: best at 256-512 tokens
- Analytical queries: best at 1024+ tokens
- Query type affects optimal chunk size significantly

### Chroma Research
- LLMSemanticChunker: 0.919 recall
- ClusterSemanticChunker: 0.913 recall
- RecursiveCharacterTextSplitter: 0.854-0.895 recall
- Performance varies up to 9% across methods

### Max-Min Semantic Chunking
- Average AMI scores: 0.85-0.90
- Average accuracy: 0.56
- Outperforms fixed-size on coherence metrics

### Proposition Chunking
- Breaks content into atomic fact-based units
- Each unit self-contained and precise
- Significantly improves retrieval accuracy for factoid queries

## Direct Challenge to Our KB's Concept-Based Segmentation

Our /ingest segments by "concept" (LLM judgment). These benchmarks show:

1. **No single strategy dominates** — optimal chunking depends on query type, domain, and document structure. Our one-size-fits-all concept approach may be suboptimal for different source types.

2. **Proposition chunking** (atomic facts) outperforms concept chunking for factoid queries — our wiki articles mix atomic facts with interpretive synthesis. For /ask factoid queries, finer granularity might help.

3. **Page-level chunking won the NVIDIA benchmark** — suggesting that for well-structured documents (papers, articles), preserving the author's original structure beats any re-segmentation. Our raw/ sources already have good structure; the question is whether /ingest's concept extraction improves or degrades retrieval vs. just indexing raw/ directly.

4. **9% recall variation across methods** — not trivial. If our concept-based approach is in the lower range, we're leaving significant retrieval quality on the table.

## Mitigation

The benchmarks suggest a hybrid approach: concept-level articles for /ask synthesis queries (where our approach is strong) + atomic proposition index for factoid queries (where our approach may be weak). This maps to sub-indices: one organized by concept (current), one by atomic fact (future).
