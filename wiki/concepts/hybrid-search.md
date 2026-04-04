---
title: "Hybrid Search"
sources:
  - path: raw/articles/qmd-query-markup-documents.md
    type: repo
    quality: primary
  - path: raw/articles/elvis-personal-kb-agents.md
    type: note
    quality: tertiary
created: 2026-04-03
updated: 2026-04-03
tags: [search, retrieval, tooling]
resolved_patches: []
---

## Resumo

Hybrid search combines keyword-based (BM25) and semantic (vector) retrieval with LLM re-ranking to find relevant documents in a knowledge base. QMD by Tobi Lütke is the reference implementation: an on-device search engine that runs entirely locally via GGUF models, designed specifically for markdown knowledge bases and agentic workflows.

## Conteúdo

### Why Hybrid?

Neither keyword nor semantic search alone is sufficient:
- **BM25 (keyword)**: fast, great for exact terms, misses semantic similarity
- **Vector (semantic)**: captures meaning, misses exact matches and rare terms
- **Hybrid + reranking**: combines both, then uses an LLM to sort by actual relevance

### QMD's Hybrid Pipeline

```
User Query
    │
    ├──► Query Expansion (fine-tuned LLM) → 2 alternative queries
    └──► Original Query (×2 weight)
         │
         ▼
    For each query: BM25 (FTS5) + Vector Search
         │
         ▼
    RRF Fusion (k=60), original query ×2 weight
    Top-rank bonus: +0.05/#1, +0.02/#2-3
         │
         ▼
    Top 30 → LLM Re-ranking (qwen3-reranker, yes/no + logprobs)
         │
         ▼
    Position-Aware Blend:
      Rank 1-3:  75% RRF / 25% reranker
      Rank 4-10: 60% RRF / 40% reranker
      Rank 11+:  40% RRF / 60% reranker
```

**Design insight:** Pure RRF can dilute exact matches when expanded queries don't match. The top-rank bonus and position-aware blending preserve high-confidence retrieval results.

### Score Normalization

| Backend | Raw Score | Conversion | Range |
|---------|-----------|------------|-------|
| FTS (BM25) | SQLite FTS5 | `Math.abs(score)` | 0 to ~25+ |
| Vector | Cosine distance | `1 / (1 + distance)` | 0.0 to 1.0 |
| Reranker | LLM 0-10 rating | `score / 10` | 0.0 to 1.0 |

### Smart Chunking

Documents chunked into ~900-token pieces with 15% overlap. Break points scored by type:
- Headings: 50-100 (H6-H1)
- Code fences: 80
- Horizontal rules: 60
- Blank lines: 20
- List items: 5

Code fence protection: break points inside code blocks are ignored.

**AST-Aware Chunking** (`--chunk-strategy auto`): uses tree-sitter for code files, chunking at function/class/import boundaries. Supported: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`.

### Local GGUF Models

| Model | Purpose | Size |
|-------|---------|------|
| embeddinggemma-300M-Q8_0 | Vector embeddings | ~300MB |
| qwen3-reranker-0.6b-q8_0 | Re-ranking | ~640MB |
| qmd-query-expansion-1.7B-q4_k_m | Query expansion (fine-tuned) | ~1.1GB |

All auto-downloaded, cached in `~/.cache/qmd/models/`. No cloud dependency.

### Integration Modes

- **CLI**: `qmd search`, `qmd vsearch`, `qmd query`
- **MCP Server**: exposes `query`, `get`, `multi_get`, `status` tools
- **SDK**: `@tobilu/qmd` npm package with `createStore()` API
- **HTTP**: `qmd mcp --http` for shared long-lived server

### Relevance to Knowledge Bases

QMD is the tool Elvis (@omarsar0) uses to index his research paper collection. It's designed for the exact use case: markdown knowledge bases with agentic search. The MCP integration means an LLM agent can use QMD as a search tool directly.

For our KB, QMD represents the Fase 2-3 upgrade path when `_index.md` flat retrieval hits its limits (~200 articles).

## Conexões

- [[context-management]] — hybrid search addresses the same problem (finding relevant content within budget) at the retrieval level
- [[autonomous-research-agents]] — web exploration stage in deep research uses similar hybrid retrieval patterns
- [[llm-knowledge-base]] — QMD is the Fase 2-3 upgrade when flat _index.md hits limits
- [[raptor-vs-flat-retrieval]] — QMD is the practical alternative to RAPTOR for scaling retrieval

## Fontes

- [QMD — Query Markup Documents](../../raw/articles/qmd-query-markup-documents.md) — full architecture: hybrid pipeline, RRF fusion, smart chunking, GGUF models, MCP integration, SDK
