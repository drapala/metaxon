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
