---
source: https://arxiv.org/abs/2405.14831
authors: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su
date: 2024-05-23
type: paper
arxiv: "2405.14831"
venue: NeurIPS 2024
---

# HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models

## Abstract

RAG framework modeled after hippocampal memory indexing theory. Combines LLMs with knowledge graphs and Personalized PageRank. Up to 20% improvement on multi-hop QA. Single-step retrieval comparable to iterative methods while being 10-30× cheaper and 6-13× faster.

## Architecture (3 Components Mirroring Human Memory)

### Offline Indexing
- LLM performs open information extraction (OpenIE) on passages → noun phrase nodes + relation edges
- Builds schemaless knowledge graph ("hippocampal index")
- Adds synonymy edges between similar noun phrases via retrieval encoders

### Online Retrieval
1. Extract named entities from query using LLM
2. Map query entities to knowledge graph nodes via retrieval encoders
3. Apply **Personalized PageRank (PPR)** using query nodes as seeds
4. Rank passages by aggregating node probabilities

### Node Specificity
Neurobiologically plausible alternative to IDF: inverse of passage frequency per node.

## Key Results

| Metric | MuSiQue | 2WikiMultiHopQA | HotpotQA |
|--------|---------|-----------------|----------|
| R@5 Improvement | ~3% | ~20% | Competitive |
| Efficiency vs IRCoT | 10-30× cheaper, 6-13× faster | — | — |
| All-Recall Gap | +3.4% over ColBERTv2 | +20.3% over ColBERTv2 | Modest |

Single-step multi-hop retrieval: retrieves all supporting documents in one step via graph associations (vs iterative methods needing multiple LLM calls).

## Ablation Findings

- PPR significantly outperforms simple baselines (query nodes only, direct neighbors)
- GPT-3.5 produces 2× more triples than REBEL; Llama-3 8B matches GPT-3.5
- Node specificity: 2-4% improvement on MuSiQue and HotpotQA
- Synonymy edges: largest impact on entity-centric datasets

## Comparison to RAPTOR

Unlike RAPTOR (which summarizes during indexing), HippoRAG "can continuously integrate new knowledge by simply adding edges to its KG." More flexible for incremental updates — closer to how our /ingest works (adding sources without rebuilding the tree).

## Relevance to Knowledge Bases

HippoRAG's knowledge graph is structurally similar to a wiki with wikilinks: entities are nodes, relations are edges, and retrieval follows link paths rather than vector similarity alone. Our wiki's [[wikilinks]] between concepts serve the same purpose as HippoRAG's knowledge graph edges — enabling multi-hop traversal. The Personalized PageRank approach could inform a future /search command.
