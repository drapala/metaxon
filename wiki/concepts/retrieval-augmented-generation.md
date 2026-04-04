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
created: 2026-04-03
updated: 2026-04-03
tags: [retrieval, rag, long-context, evaluation]
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
