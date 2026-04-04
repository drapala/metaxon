---
title: "Context Management"
sources:
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/papers/memgpt-llms-as-operating-systems.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [agent-architecture, retrieval, token-budget]
resolved_patches: []
---

## Resumo

Context management encompasses the strategies agents use to operate within finite token budgets while maintaining coherent, long-running conversations. Claude Code's implementation reveals a multi-layered compaction hierarchy that progressively trades fidelity for space — a pattern directly applicable to any knowledge base retrieval system.

## Conteúdo

### The Core Problem

LLMs have fixed context windows. As conversations grow, agents must decide what to keep, summarize, or discard. The challenge is doing this without losing critical information or breaking conversation coherence.

### Claude Code's 4-Layer Compaction Hierarchy

Claude Code implements progressively aggressive strategies, triggered in order:

**1. Microcompaction** (lightest)
- Time-based: clear tool results older than a TTL
- Size-based: truncate when accumulated tokens exceed threshold
- Tool-specific: only compacts FileRead, Bash, Grep, Glob, WebSearch, WebFetch, FileEdit, FileWrite
- Cache-aware: preserves prompt cache integrity

**2. Snip Compaction**
- History truncation preserving the assistant's "protected tail"
- Non-destructive: full history kept in REPL for scrollback
- Tracks tokens freed for accurate budget calculations

**3. Auto-Compaction** (triggered at `context_window - 13,000` tokens)
1. Strip images/documents from older messages
2. Group messages by API round
3. Call compaction model for summary
4. Replace old messages with CompactBoundaryMessage
5. Re-inject up to 5 files + skills post-compaction (50K for files, 25K for skills)
- Circuit breaker: max 3 consecutive failures

**4. Context Collapse** (heaviest, lazy)
- Committed only when API returns 413 (prompt too long)
- Cascade: collapse drain → reactive compact → surface error

### Bandwidth-Aware Retrieval Pattern

This hierarchy maps directly to knowledge base retrieval:
- **Layer 1** (always loaded): lightweight index/pointers — analogous to `_index.md`
- **Layer 2** (on-demand): article content — analogous to `wiki/concepts/*.md`
- **Layer 3** (spot-check): raw sources — analogous to `raw/`

The principle: never read more than you need at each layer. Escalate only when the lighter layer is insufficient.

### System Context Injection

Two tiers injected into every request:
- **System context** (memoized): git status, cache breaker
- **User context** (memoized): CLAUDE.md contents, current date

Both are memoized per session to avoid redundant computation.

## Conexões

- [[memory-consolidation]] — memory pruning is a form of context management across sessions
- [[hybrid-search]] — QMD's retrieval layers mirror the bandwidth-aware pattern
- [[autonomous-research-agents]] — the Deep Research pipeline faces similar context budget decisions
- [[raptor-vs-flat-retrieval]] — compaction hierarchy maps to RAPTOR's multi-level abstraction
- [[kb-architecture-patterns]] — Pattern 4 (Bandwidth-Aware Retrieval) formalizes this article's hierarchy
- [[agent-memory-architectures]] — MemGPT's virtual context is the production implementation of this pattern

## Fontes

- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — primary source for the 4-layer compaction hierarchy, system context injection, and implementation details
- [MemGPT](../../raw/papers/memgpt-llms-as-operating-systems.md) — OS-inspired virtual context management: memory pressure warnings, queue eviction, self-directed memory ops
