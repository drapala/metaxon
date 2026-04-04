---
title: "Memory Consolidation"
sources:
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/articles/dream-memory-consolidation-skill.md
    type: repo
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [agent-architecture, memory, persistence]
resolved_patches: []
---

## Resumo

Memory consolidation is the process by which an LLM agent reviews recent interactions and distills durable signals into persistent storage, enabling cross-session continuity. The KAIROS subsystem in Claude Code and its open-source implementation (Dream) define the current state of the art: a 4-phase cycle with gated triggers and typed memory classification.

## Conteúdo

### Why Memory Consolidation Matters

LLM agents forget everything between sessions. Without consolidation, users repeat corrections, re-explain preferences, and lose project context. Memory consolidation turns ephemeral conversations into persistent knowledge.

### The KAIROS Auto-Dreaming System

KAIROS is Claude Code's internal mechanism for background memory consolidation, running as a forked subagent.

**Trigger Gates** (evaluated in cost-reducing order):
1. Time-based: hours since last consolidation (default 24h)
2. Session-based: minimum sessions since last run (default 5)
3. Lock-based: file locks prevent concurrent consolidation
4. Scan throttling: every 10 minutes

**4-Phase Dream Cycle:**
1. **Orient** — list memory directory, read index, skim files
2. **Gather** — check daily logs, grep transcripts narrowly for new signals
3. **Consolidate** — write/update memory files, merge duplicates, convert relative dates to absolute
4. **Prune** — update entrypoint index (max ~25KB), remove stale pointers

**Safety constraints:** Bash restricted to read-only operations. File writes go through standard Edit/Write tools only.

### 4 Memory Types

| Type | Purpose | Examples |
|------|---------|---------|
| User | Role, preferences, knowledge level | "Senior Go dev, new to React" |
| Feedback | Corrections and confirmed approaches | "Don't mock the database in tests" |
| Project | Ongoing work, goals, deadlines | "Auth rewrite driven by compliance" |
| Reference | Pointers to external systems | "Pipeline bugs tracked in Linear INGEST" |

### Index Architecture

`MEMORY.md` (~25KB max) serves as the table of contents, loaded into every conversation. It contains only pointers (~150 chars per entry), not content.

**Recall mechanism:** A Sonnet-powered relevance selector scans up to 200 memory files and returns the 5 most relevant to the current query. Demand-driven, not static.

### Dream: Open-Source Implementation

Dream (`/dream`) is a standalone open-source implementation of KAIROS auto-dreaming, installable as a Claude Code skill. Same 4-phase cycle, same 4 memory types, same exclusion principles.

Key difference: KAIROS runs automatically via gates (24h, 5 sessions). Dream is manually invoked via `/dream`. KAIROS is internal to Claude Code; Dream is a one-file skill anyone can install.

Enhanced mode (`--memory`): makes Claude proactively save memories during normal work, not just during `/dream` runs.

### Deliberate Exclusions

The system does not store:
- Code patterns, architecture, file paths (derivable from code)
- Git history (use `git log`)
- Debugging solutions (the fix is in the code)

Principle: if it's derivable from current state, don't persist it.

## Conexões

- [[context-management]] — memory consolidation is cross-session context management
- [[autonomous-research-agents]] — persistent memory could improve research agent personalization (currently a gap per the survey)
- [[kb-architecture-patterns]] — KAIROS cycle parallels /review; trigger gates transferable
- [[self-improving-agents]] — memory consolidation is cross-session self-improvement; Reflexion is within-task
- [[agent-memory-architectures]] — consolidation operates on these structures (KAIROS on MemGPT-like tiers, Dream on file-based memory)

## Fontes

- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — KAIROS architecture, dream gates, 4-phase cycle, memory types, recall mechanism
- [Dream Repo](../../raw/articles/dream-memory-consolidation-skill.md) — open-source implementation: installable skill, same 4-phase cycle, enhanced auto-extraction mode
