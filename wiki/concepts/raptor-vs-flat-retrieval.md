---
title: "RAPTOR vs. Flat 3-Layer Retrieval"
sources:
  - path: raw/papers/raptor-recursive-abstractive-retrieval.md
    type: paper
    quality: primary
  - path: raw/papers/long-context-vs-rag-evaluation.md
    type: paper
    quality: primary
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/papers/chunking-strategies-rag-comparison.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [retrieval, comparison, architecture]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

RAPTOR (tree-organized retrieval) and the flat 3-layer pattern used in this KB solve the same problem — multi-level abstraction for retrieval — through opposite approaches. RAPTOR automates tree construction via statistical clustering; the KB uses LLM-guided concept extraction. Comparison reveals what already works, what's missing, and what can be borrowed without adding infrastructure.

## Conteúdo

### Structural Comparison

| Dimension | RAPTOR | 3-Layer Flat KB |
|-----------|--------|-----------------|
| Construction | Automatic: chunk → GMM clustering → LLM summarize → re-embed → repeat | LLM-guided: /ingest identifies concepts → writes articles → updates _index |
| Structure | Tree with N levels (depth varies per document) | Exactly 3 fixed levels: _index → concepts/ → raw/ |
| Retrieval | Collapsed tree: cosine similarity across all levels | Sequential escalation: Layer 1 → 2 → 3 |
| Clustering | Soft (GMM): a chunk can belong to multiple clusters | Hard: 1 source maps to max 3 concepts, each concept is 1 article |
| Compression | 0.28 ratio per level (72% compression) | Variable: _index ~150 chars/article, articles ~500-1500 words |
| Infrastructure | SBERT embeddings + GMM + LLM summarization pipeline | Zero — just .md files and an LLM |

### What Already Works (Validated by RAPTOR)

**1. _index.md is a RAPTOR root node.** RAPTOR's summary nodes contribute 23-57% of useful retrieved content. Our _index with ~150 char pointers serves the same function: fast orientation without loading content. Blueprint principle 7 ("Index = pointers, not content") is academically validated.

**2. Layer 1→2→3 escalation ≈ collapsed tree.** RAPTOR's collapsed tree (which outperforms tree traversal) selects nodes from any level by relevance. Our /ask does the same manually: start at index, descend to articles, verify in raw/ when needed.

**3. Concept-based > chunk-based.** RAPTOR outperforms chunk-based retrievers (38.5% vs 20-22%). Our /ingest groups by concept, not by source — exactly what RAPTOR does via clustering. The difference: our "clustering" is semantic (LLM decides), not statistical (GMM decides).

### Exploitable Gaps (No Infrastructure Required)

**Gap 1: Soft clustering via bidirectional backlinks.**

RAPTOR uses soft clustering: a chunk can belong to multiple clusters. Our /ingest already allows a source to feed multiple articles (max 3 concepts), but the reverse is weak — articles reference sources, but don't systematically reference other articles covering the same sub-concept.

**Improvement:** If two articles cite the same raw/ source, they should have bidirectional wikilinks. This simulates soft clustering via backlinks. In Obsidian, the graph view renders these clusters visually.

**Gap 2: Explicit compression targets per level.**

RAPTOR measures 0.28 ratio (72% compression) per level. We have no compression target. _index.md has ~150 chars/article, but wiki articles vary from 500 to 2000+ words without a target.

**Improvement:** The article template already requires a 2-3 sentence summary. A /review heuristic should enforce that summaries actually function as "intermediate nodes" — if a summary is weak or generic, /review rewrites it. This improves Layer 1 → Layer 2 transition without structural changes.

**Gap 3: Adaptive depth (3 fixed levels → sub-indices).**

RAPTOR generates N levels based on document depth. Our KB has exactly 3 fixed levels. The _index.md comment says "~200 entries" as migration trigger, but this number conflates two different limits:

1. **Token capacity limit (~200 articles):** At ~150 chars/article, 200 articles ≈ 30K chars ≈ 7.5K tokens. This fits in context, so ~200 is not a hard limit but an orientation budget.

2. **Selection accuracy limit (~50-80 articles):** [[self-improving-agents|ERL]] shows that random heuristic inclusion degrades after 40-60 items, and LLM-based selective retrieval (k=20) peaks at 56.1%. When /ask reads _index.md and selects 5-10 candidates from 200 entries, it's doing LLM-based selection from a flat list — the same task ERL benchmarked. The degradation signal is not running out of tokens, but the LLM failing to select the right articles. This suggests real degradation starts at **50-80 articles**, well before the ~200 token limit.

**Observable degradation signal:** /ask should track when Layer 1 selection misses relevant articles (detectable when Layer 2 reading reveals that a non-selected article would have been more relevant, or when the user corrects an answer). A pattern of misses indicates _index.md has exceeded the LLM's reliable selection capacity.

**Improvement (Fase 2):** Group articles into thematic sub-indices: `_index-agents.md`, `_index-retrieval.md`. Each sub-index is a RAPTOR mid-level node. The main _index.md points to sub-indices instead of individual articles. This creates a 2-step selection: first select the right sub-index (from ~5-10 sub-indices), then select articles within it (from ~20-40). Both steps stay well within the ERL-validated selection window. This is "Option A" from the blueprint's _index migration plan, now with theoretical justification from both RAPTOR (mid-level node contribution 23-57%) and ERL (selection degrades at 40-60 items).

### Challenging Evidence: Concept-Based May Not Be Optimal (Chunking Benchmarks)

Multiple 2024-2025 benchmarks challenge our assumption that concept-based segmentation is sufficient:

- **NVIDIA study**: page-level chunking won at 0.648 accuracy — preserving author's original structure beats re-segmentation for well-structured documents
- **Chroma research**: up to 9% recall variation across chunking methods — non-trivial
- **Proposition chunking** (atomic facts) outperforms concept-level for factoid queries
- **Optimal strategy depends on query type**: factoid queries need 256-512 tokens, analytical queries need 1024+

Our /ingest uses concept-level articles (~500-1500 words) — potentially suboptimal for factoid /ask queries where finer granularity would help. For synthesis queries, concept-level is likely correct.

No single strategy dominates. The practical implication: our concept-based approach may be leaving retrieval quality on the table for certain query types, but switching to chunk-based would hurt synthesis queries. A hybrid (concept articles + atomic fact index) may be the optimal Fase 2 design.

### What NOT to Import

- **GMM clustering**: LLM-guided concept extraction is more precise for knowledge bases than statistical embedding clustering. RAPTOR needs GMM because it operates on raw chunks without semantics; we operate on sources the LLM already comprehends.
- **Embeddings for Layer 1 retrieval**: at ~9 articles, reading _index.md whole is more efficient than any embedding pipeline. At ~200 articles, [[hybrid-search|QMD]] solves this better than DIY embeddings.

## Interpretação

Ver seções marcadas com (⚠️) no Conteúdo acima — conteúdo interpretativo está inline por razões de coesão narrativa.

## Conexões

- [[retrieval-augmented-generation]] — RAPTOR is the top-performing RAG retriever (38.5% vs 20-22% chunk-based)
- [[kb-architecture-patterns]] — validates Pattern 4 (Bandwidth-Aware Retrieval) with academic evidence
- [[context-management]] — the 3-layer escalation pattern originates from Claude Code's compaction hierarchy
- [[hybrid-search]] — QMD is the practical alternative to RAPTOR for Fase 2-3 scaling

## Fontes

- [RAPTOR Paper](../../raw/papers/raptor-recursive-abstractive-retrieval.md) — tree construction, 0.28 compression, 23-57% non-leaf contribution, 4% hallucination rate
- [LC vs RAG Paper](../../raw/papers/long-context-vs-rag-evaluation.md) — RAPTOR 38.5% vs chunk-based 20-22%, confirms summarization-based retrieval superiority
- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — the 3-layer bandwidth-aware pattern that our /ask implements
- [Chunking Benchmarks](../../raw/papers/chunking-strategies-rag-comparison.md) — (challenging) page-level won NVIDIA benchmark, 9% recall variation, proposition chunking beats concept for factoid queries
