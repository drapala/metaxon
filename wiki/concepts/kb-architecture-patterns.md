---
title: "KB Architecture Patterns"
sources:
  - path: raw/articles/karpathy-llm-knowledge-bases.md
    type: note
    quality: tertiary
  - path: raw/articles/elvis-personal-kb-agents.md
    type: note
    quality: tertiary
  - path: raw/articles/paulo-silveira-open-claw-pkm.md
    type: article
    quality: secondary
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/papers/long-context-vs-rag-evaluation.md
    type: paper
    quality: primary
  - path: raw/papers/raptor-recursive-abstractive-retrieval.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [taxonomy, architecture, patterns]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Four distinct architectural patterns for LLM-powered knowledge bases have emerged from practitioners and research. They differ in who controls synthesis (LLM vs human), how retrieval scales (index vs search vs RAG), and where the bottleneck sits (ingest quality vs context budget vs editorial judgment).

## Conteúdo

### Pattern 1: LLM-as-Compiler

**Originator:** Karpathy (April 2026)

**Architecture:** `raw/ → LLM compiles wiki/ → LLM does Q&A → outputs filed back`

**Key characteristics:**
- LLM is the sole writer; human rarely touches wiki directly
- Index files + brief summaries sufficient at ~100 articles / ~400K words
- Outputs (reports, slides) cycle back to enrich the wiki
- Linting via periodic LLM health checks

**Strengths:** Closed loop, incremental, works without RAG at small scale.
**Weaknesses:** Scale limited by context window. No explicit source verification. Quality depends on ingest prompt.

**When to use:** Solo researcher, <200 articles, single domain.

### Pattern 2: Agent-as-Curator

**Originator:** Elvis/DAIR.ai (April 2026)

**Architecture:** `Automated curation → hybrid search (QMD) → MCP visual artifacts → actionable insights`

**Key characteristics:**
- Tuned Skill automates paper discovery and filtering
- [[hybrid-search|QMD]] provides BM25 + vector + reranking over the corpus
- MCP tools power interactive visualizations inside agent orchestrator
- Focus on actionability: "research questions are only as good as the insights agents have access to"

**Strengths:** Scales to 100s of papers via semantic search. Automated curation removes human bottleneck. Visual artifacts surface non-obvious patterns.
**Weaknesses:** Complex setup (QMD, MCP, orchestrator). Depends on external tooling.

**When to use:** Heavy paper consumption, 200+ sources, need for visual exploration.

### Pattern 3: Human-in-the-Loop

**Originator:** Paulo Silveira / Open Claw (March 2026)

**Architecture:** `Multi-modal capture → LLM classifies → human writes final output`

**Key characteristics:**
- Telegram as universal input (voice, text, photos, links)
- Whisper transcribes audio; Claude Sonnet classifies into concepts
- Human retains editorial control over final synthesis
- Anti-slop philosophy: "letting machines generate final drafts creates generic-feeling content"

**Strengths:** Preserves authorial voice. No idea lost. Historical pattern (Zettelkasten, Dostoevsky's dictation).
**Weaknesses:** Doesn't scale. Synthesis bottleneck is human.

**When to use:** Personal brand writing, high-stakes content, when voice matters more than throughput.

### Pattern 4: Bandwidth-Aware Retrieval

**Originator:** Claude Code internals (March 2026)

**Architecture:** `Layered retrieval with progressive escalation + circuit breakers`

**Key characteristics:**
- 3+ layers: lightweight index (always loaded) → article content (on-demand) → raw sources (spot-check)
- Progressive compaction: micro → snip → auto → collapse
- Circuit breakers prevent thrashing (max 3 consecutive failures)
- Principle: "never read more than you need at each layer"

**Strengths:** Token-efficient, production-proven. Graceful degradation under pressure.
**Weaknesses:** Designed for conversations, not knowledge bases. No notion of source quality.

**When to use:** Any KB retrieval system. This is a universal pattern, not an alternative to the others — it's how retrieval should work within any of the above.

### Comparison Matrix

| Pattern | Who synthesizes | Retrieval | Scale | Bottleneck |
|---------|----------------|-----------|-------|------------|
| LLM-as-Compiler | LLM | Index-based (LC) | ~200 articles | Ingest quality |
| Agent-as-Curator | LLM + tools | Hybrid search | 1000+ papers | Tooling setup |
| Human-in-the-Loop | Human | LLM classification | ~50 outputs | Human time |
| Bandwidth-Aware | (meta-pattern) | Layered escalation | Any | Context budget |

## Interpretação

### RAPTOR Analogy for _index.md

RAPTOR's summary nodes contribute 23-57% of useful retrieved content. Our _index.md with ~150 char pointers serves a similar function — but this is an analogy, not a validation. RAPTOR operates on document chunks with embeddings; our _index operates on concept pointers read by an LLM. The mechanism is different even if the abstraction-level pattern resembles.

| RAPTOR Level | KB Equivalent (analogy) |
|-------------|--------------------------|
| Raw chunks (leaf nodes) | raw/ sources |
| Cluster summaries (mid-level) | wiki/concepts/ articles |
| Root summaries (top-level) | _index.md pointers |

### ERL's Heuristics Result Applied to KB

ERL shows heuristics (+7.8%) > trajectories (-1.9%) on Gaia2. Our wiki articles resemble heuristics (distilled principles by concept). But ERL tested on agent task execution, not knowledge compilation — the transfer is plausible but not directly validated.

### KAIROS-Review Parallel

The KAIROS cycle (orient → gather → consolidate → prune) resembles a /review cycle. Both consolidate knowledge, but KAIROS operates on ephemeral conversational memory; /review on durable compiled knowledge. The parallel suggests borrowing KAIROS's trigger gates (time-based, session-based) for /review automation.

## Conexões

- [[llm-knowledge-base]] — Pattern 1 is the core architecture of this KB
- [[hybrid-search]] — Pattern 2's retrieval layer; our Fase 2-3 upgrade path
- [[context-management]] — Pattern 4 formalized; our /ask already implements 3 layers
- [[memory-consolidation]] — KAIROS cycle parallels /review; trigger gates transferable
- [[retrieval-augmented-generation]] — Academic evidence that LC > RAG at small scale (Pattern 1 validated)
- [[self-improving-agents]] — ERL validates concept articles > raw sources; Reflexion parallels our patch system
- [[tension-resolution]] — framework for detecting and resolving contradictions between articles, informed by 5 papers

## Fontes

- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — Pattern 1: the original architecture
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — Pattern 2: automated curation + QMD + visual artifacts
- [Paulo Silveira — Open Claw](../../raw/articles/paulo-silveira-open-claw-pkm.md) — Pattern 3: human-in-the-loop, anti-slop philosophy
- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — Pattern 4: compaction hierarchy, circuit breakers
- [LC vs RAG Paper](../../raw/papers/long-context-vs-rag-evaluation.md) — Validates Pattern 1 at small scale (LC 56.3% vs RAG 49.0%)
- [RAPTOR Paper](../../raw/papers/raptor-recursive-abstractive-retrieval.md) — Validates _index.md as manual RAPTOR tree; summary nodes contribute 23-57% of retrieval
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — Heuristics > trajectories: concept articles validated as superior to raw source dumps
