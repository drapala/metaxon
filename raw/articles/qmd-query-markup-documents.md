---
source: https://github.com/tobi/qmd
author: Tobi Lütke (tobi)
date: 2026-04-03
type: repo
---

# QMD - Query Markup Documents

An on-device search engine for everything you need to remember. Index your markdown notes, meeting transcripts, documentation, and knowledge bases. Search with keywords or natural language. Ideal for your agentic flows.

QMD combines BM25 full-text search, vector semantic search, and LLM re-ranking—all running locally via node-llama-cpp with GGUF models.

## Quick Start

```sh
npm install -g @tobilu/qmd

# Create collections
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings

# Add context to help with search results
qmd context add qmd://notes "Personal notes and ideas"
qmd context add qmd://meetings "Meeting transcripts and notes"

# Generate embeddings for semantic search
qmd embed

# Search
qmd search "project timeline"           # Fast keyword search
qmd vsearch "how to deploy"             # Semantic search
qmd query "quarterly planning process"  # Hybrid + reranking (best quality)
```

## Using with AI Agents

QMD's `--json` and `--files` output formats are designed for agentic workflows:

```sh
qmd search "authentication" --json -n 10
qmd query "error handling" --all --files --min-score 0.4
qmd get "docs/api-reference.md" --full
```

## MCP Server

Exposes an MCP (Model Context Protocol) server for tighter integration.

**Tools exposed:**
- `query` — Search with typed sub-queries (`lex`/`vec`/`hyde`), combined via RRF + reranking
- `get` — Retrieve a document by path or docid (with fuzzy matching suggestions)
- `multi_get` — Batch retrieve by glob pattern, comma-separated list, or docids
- `status` — Index health and collection info

**Claude Code** — Install the plugin:

```bash
claude plugin marketplace add tobi/qmd
claude plugin install qmd@qmd
```

Or configure MCP manually in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

### HTTP Transport

For a shared, long-lived server that avoids repeated model loading:

```sh
qmd mcp --http                    # localhost:8181
qmd mcp --http --daemon           # background daemon
qmd mcp stop                      # stop via PID file
```

## Architecture — Hybrid Search Pipeline

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
    RRF Fusion (k=60)
    Original query ×2 weight
    Top-rank bonus: +0.05/#1, +0.02/#2-3
         │
         ▼
    Top 30 candidates → LLM Re-ranking (qwen3-reranker, yes/no + logprobs)
         │
         ▼
    Position-Aware Blend:
      Rank 1-3:  75% RRF / 25% reranker
      Rank 4-10: 60% RRF / 40% reranker
      Rank 11+:  40% RRF / 60% reranker
```

## Score Normalization

| Backend | Raw Score | Conversion | Range |
|---------|-----------|------------|-------|
| FTS (BM25) | SQLite FTS5 BM25 | `Math.abs(score)` | 0 to ~25+ |
| Vector | Cosine distance | `1 / (1 + distance)` | 0.0 to 1.0 |
| Reranker | LLM 0-10 rating | `score / 10` | 0.0 to 1.0 |

## Smart Chunking

Documents are chunked into ~900-token pieces with 15% overlap using smart boundary detection. Break points are scored by type (headings: 100-50, code fences: 80, horizontal rules: 60, blank lines: 20, list items: 5).

Code fence protection: break points inside code blocks are ignored — code stays together.

**AST-Aware Chunking** (`--chunk-strategy auto`) uses tree-sitter to chunk code files at function, class, and import boundaries. Supported for `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, and `.rs`.

## GGUF Models (via node-llama-cpp)

| Model | Purpose | Size |
|-------|---------|------|
| embeddinggemma-300M-Q8_0 | Vector embeddings (default) | ~300MB |
| qwen3-reranker-0.6b-q8_0 | Re-ranking | ~640MB |
| qmd-query-expansion-1.7B-q4_k_m | Query expansion (fine-tuned) | ~1.1GB |

Models are auto-downloaded from HuggingFace and cached in `~/.cache/qmd/models/`.

Custom embedding model via `QMD_EMBED_MODEL` env var (e.g., Qwen3-Embedding for multilingual/CJK support).

## SDK / Library Usage

```typescript
import { createStore } from '@tobilu/qmd'

const store = await createStore({
  dbPath: './my-index.sqlite',
  config: {
    collections: {
      docs: { path: '/path/to/docs', pattern: '**/*.md' },
    },
  },
})

const results = await store.search({ query: "authentication flow" })
await store.close()
```

## Data Storage

Index stored in: `~/.cache/qmd/index.sqlite`

Schema: collections, path_contexts, documents, documents_fts, content_vectors, vectors_vec, llm_cache.

## Requirements

- Node.js >= 22 or Bun >= 1.0.0
- macOS: `brew install sqlite` (for extension support)

## License

MIT
