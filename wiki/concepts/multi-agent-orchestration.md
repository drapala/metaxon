---
title: "Multi-Agent Orchestration"
sources:
  - path: raw/articles/claude-code-internals-harness-engineering.md
    type: article
    quality: primary
  - path: raw/papers/deep-research-survey-autonomous-agents.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [agent-architecture, coordination, parallelism]
source_quality: high
interpretation_confidence: high
resolved_patches: []
---

## Resumo

Multi-agent orchestration is the coordination of specialized LLM agents working on sub-tasks of a larger goal. Two patterns dominate: single-agent (one LLM handles everything sequentially) and multi-agent (specialized workers coordinated by a master). Claude Code's Coordinator Mode and the Deep Research survey both converge on a 4-phase workflow pattern.

## Conteúdo

### Single-Agent vs. Multi-Agent

| Pattern | Examples | Strengths | Weaknesses |
|---------|----------|-----------|------------|
| Single-agent | DeepResearcher, WebThinker, Search-R1 | Integrated end-to-end learning, simpler | Context pollution, sequential bottleneck |
| Multi-agent | AgentRxiv, AI Scientist, OpenResearcher | Independent optimization, parallelism | Coordination overhead, context isolation |

### Claude Code's Coordinator Mode

`CLAUDE_CODE_COORDINATOR_MODE=1` transforms Claude Code into a multi-agent orchestrator.

**Core discipline:** "Never write 'based on your findings'" — the coordinator must synthesize worker research into specific specs with file paths, line numbers, and exactly what to change. Workers don't synthesize; the coordinator does.

**4-Phase Workflow:**

| Phase | Who | Purpose |
|-------|-----|---------|
| Research | Workers (parallel) | Investigate codebase, find files |
| Synthesis | Coordinator | Read findings, craft implementation specs |
| Implementation | Workers | Make changes per spec, commit |
| Verification | Workers | Prove the code works |

**Communication:** Workers push `<task-notification>` XML messages on completion. Coordinator never polls.

**Concurrency rules:**
- Read-only (research): run in parallel freely
- Write-heavy (implementation): one at a time per file set
- Verification: can run alongside implementation on different file areas

### Continue vs. Spawn Decision

| Situation | Action | Reason |
|-----------|--------|--------|
| Research explored exact files to edit | Continue | Worker has files in context |
| Research broad, implementation narrow | Spawn fresh | Avoid exploration noise |
| Correcting a failure | Continue | Worker has error context |
| Verifying another's code | Spawn fresh | Verifier needs fresh eyes |
| Wrong approach entirely | Spawn fresh | Wrong context pollutes retry |

### Agent Isolation Modes

Three isolation levels in Claude Code:
- **Default** — shared filesystem, separate conversation context
- **Worktree** — isolated git branch copy, changes merged on exit
- **Remote (CCR)** — runs on a separate machine

### The Deep Research Pipeline Parallel

The Deep Research survey identifies the same 4-phase pattern at the research level:
1. Planning → Research
2. Question Developing → Synthesis
3. Web Exploration → Implementation (gathering)
4. Report Generation → Verification (output)

The convergence suggests this is a fundamental pattern for agent coordination, not specific to code or research.

### Task System Internals

Background tasks use file-based IPC with concurrent-session locking:
- Task IDs: base-36 encoding with type prefixes (b=bash, a=agent, r=remote)
- Lock retries: 30 attempts with 5-100ms backoff (~2.6s max wait)

## Interpretação

Nenhuma interpretação significativa neste artigo — conteúdo é factual direto das fontes.

## Conexões

- [[autonomous-research-agents]] — the Deep Research survey's multi-agent systems share the same coordination patterns
- [[context-management]] — agent isolation prevents context pollution between workers
- [[memory-consolidation]] — shared source (Claude Code internals); coordinator workers could benefit from persistent memory

## Fontes

- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — Coordinator Mode architecture, 4-phase workflow, isolation modes, task system
- [Deep Research Survey](../../raw/papers/deep-research-survey-autonomous-agents.md) — single vs. multi-agent taxonomy, workflow architectures, parameter optimization
