---
source: https://arxiv.org/abs/2502.12110
authors: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang
date: 2025-02-17
type: paper
arxiv: "2502.12110"
stance: confirming
---

# A-MEM: Agentic Memory for LLM Agents

## Abstract

Dynamic agentic memory following Zettelkasten principles. Creates interconnected knowledge networks through dynamic indexing and linking. Memory evolution: new memories trigger updates to existing memories' descriptions, keywords, and tags. Tested on 6 foundation models, outperforms baselines.

## Zettelkasten Architecture

Each memory note contains:
- Original content (c_i), timestamp (t_i)
- LLM-generated keywords (K_i), tags (G_i)
- Contextual descriptions (X_i)
- Dense embeddings (e_i)
- Linked memories (L_i)

## Memory Evolution (Key Innovation)

When new memory m_n added:
1. Find k nearest neighbors via embedding similarity
2. LLM evaluates whether to evolve each historical memory m_j
3. If yes: update contextual descriptions, keywords, tags of existing memory
4. "Continuous refinement" of understanding across the entire network

This is EXACTLY what our /ingest does: adding a new source can trigger updates to existing wiki articles' content, connections, and metadata.

## Dynamic Linking (2 stages)
1. Similarity-based retrieval (cosine similarity)
2. LLM-driven analysis: evaluates top-k for causal links and conceptual patterns beyond embedding similarity

## Results (LoCoMo, 6 models)

Multi-Hop F1 improvements:
| Model | Baseline | A-Mem | Gain |
|-------|----------|-------|------|
| GPT-4o-mini | 18.41 | **45.85** | +149% |
| GPT-4o | 9.09 | **39.41** | +334% |
| Qwen-1.5b | 4.25 | **24.32** | +472% |

Token efficiency: 1,200-2,500 tokens/query vs 16,900 for LoCoMo/MemGPT (7-14x reduction).

## Ablation
| Component removed | Multi-Hop F1 |
|-------------------|-------------|
| Full A-Mem | **45.85** |
| Without evolution only | 31.24 (-32%) |
| Without links + evolution | 24.55 (-46%) |

Both linking AND evolution are essential. Evolution alone provides +32% over no-evolution.

## Validates Our Architecture

A-Mem is the closest academic validation of our /ingest pattern:
- Atomic notes with metadata ≈ wiki articles with frontmatter
- Dynamic linking ≈ wikilinks between concepts
- Memory evolution ≈ /ingest updating existing articles when new sources arrive
- Zettelkasten principles ≈ our "1 concept = 1 file" heuristic

Key difference: A-Mem does evolution AUTOMATICALLY (LLM decides). Our /ingest follows explicit rules from CLAUDE.md. A-Mem's approach is more autonomous; ours is more controlled.
