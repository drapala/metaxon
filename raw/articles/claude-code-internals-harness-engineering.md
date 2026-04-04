---
source: https://sathwick.xyz/blog/claude-code.html
author: Sathwick
date: 2026-03-31
type: article
---

# Reverse-Engineering Claude Code: Harness Engineering Internals

Seleção de seções relevantes para knowledge base engineering: query engine, context management, multi-agent coordination, KAIROS/auto-dreaming, memory system, coordinator mode, e hooks.

## Query Engine (Section 4)

The query engine manages conversations across two coordinating files. `QueryEngine.ts` handles session-level orchestration including system context building, message management, API calls, permission tracking, and cost accumulation. Core `submitMessage(prompt, options)` method operates as an AsyncGenerator yielding SDK messages throughout each turn.

The query loop in `query.ts` is a resilient state machine: prefetch memory + skills (parallel) → apply message compaction (snip, microcompact, context collapse) → call API with streaming → handle streaming errors (fallback, retry) → execute tools (concurrent or serial) → check recovery paths (compact, collapse drain, token escalation).

Tool execution partitions calls by safety: read-only operations run concurrently (up to 10 simultaneous), while write operations execute serially with context propagation between batches.

When approaching output token exhaustion, the engine injects an invisible meta-message and continues the loop via `token_budget_continuation` transition, with max 3 consecutive recovery attempts.

## Context Management (Section 10)

### Auto-Compaction

When token count exceeds `context_window - 13,000`:

1. Strip images/documents from older messages (replace with `[image]` markers)
2. Group messages by API round (assistant + tool results)
3. Call the compaction model to generate a summary
4. Replace old messages with a `CompactBoundaryMessage`
5. Re-inject up to 5 files + skills post-compaction (50K token budget for files, 25K for skills)

Circuit breaker: max 3 consecutive compaction failures before giving up.

### Microcompaction

Lighter-weight compression for tool results:

- **Time-based** — Clear tool results older than a TTL
- **Size-based** — Truncate when accumulated tool result tokens exceed threshold
- **Tool-specific** — Only compacts: FileRead, Bash, Grep, Glob, WebSearch, WebFetch, FileEdit, FileWrite
- **Cache-aware** — A "cached" variant preserves prompt cache integrity via `CacheEditsBlock`

### Snip Compaction

History truncation strategy (feature-gated):

- Remove old messages beyond a snip boundary
- Preserve the assistant's "protected tail" for context continuity
- Track tokens freed for accurate token budget calculations
- Full history preserved in REPL for UI scrollback (non-destructive)

### Context Collapse

Staged collapses committed lazily — only when API returns 413:

```
API 413 → Collapse drain (commit staged collapses)
        → If insufficient → Reactive compact (full summarization)
        → If still insufficient → Surface error to user
```

### System Context

Two tiers injected into every request:

- **System context** (memoized per session): git status (branch, recent commits, file status — truncated at 2000 chars), cache breaker
- **User context** (memoized per session): CLAUDE.md file contents (auto-discovered from project + parent directories), current date

## Multi-Agent Architecture (Section 13)

### Agent Spawning

`AgentTool` spawns child agents with configurable isolation:

- **Default** — Shared filesystem, separate conversation context
- **Worktree** — Isolated git branch copy, changes merged on exit
- **Remote (CCR)** — Runs on a separate machine

Agents are addressable by name for inter-agent messaging via `SendMessage`.

### Task System

Background tasks use file-based IPC with concurrent-session locking:

- Task types: local_bash, local_agent, remote_agent, in_process_teammate, local_workflow, monitor_mcp, dream
- Task statuses: pending, running, completed, failed, killed
- Task IDs use base-36 encoding with type prefixes (b=bash, a=agent, r=remote)
- Lock retries: 30 attempts with 5-100ms backoff (~2.6s max wait)

### Worktree Isolation

1. Create a temporary git worktree on a new branch
2. Agent works in the worktree (safe to make destructive changes)
3. On exit: keep changes (merge) or discard (clean up)

## KAIROS: Auto-Dreaming and Memory Consolidation (Section 18)

KAIROS is an alternate UX mode where Claude functions as a long-lived autonomous agent persisting across sessions. The most concrete subsystem is auto-dreaming, a background memory consolidation agent that runs as a forked subagent.

### Dream Gates (cost-reducing order)

1. Time-based (hours since last consolidation, default 24h)
2. Session-based (minimum sessions since consolidation, default 5)
3. Lock-based (file locks prevent concurrent consolidation)
4. Scan throttling (every 10 minutes)

### 4-Phase Dream Prompt

1. **Orient** — list memory directory, read index, skim files
2. **Gather recent signal** — check daily logs, grep transcripts narrowly
3. **Consolidate** — write/update memory files, merge duplicates, convert relative dates
4. **Prune and index** — update entrypoint index max ~25KB, remove stale pointers

Tool constraints: Bash restricted to read-only operations (ls, find, grep, cat, stat, wc, head, tail). File writes go through standard Edit/Write tools.

Dream task state tracks: phase, sessions under review, files touched, rolling window of recent assistant turns, abort capability, and prior modification time for lock rollback on failure.

## Memory System (Section 21)

Persistent context across conversations stored in `~/.claude/projects/<sanitized-project-root>/memory/`.

### 4 Memory Types

- **User memories**: role, preferences, knowledge level
- **Feedback memories**: corrections and confirmations on approach
- **Project memories**: ongoing work, goals, deadlines
- **Reference memories**: pointers to external systems

### Index

`MEMORY.md` (~25KB max) serves as table of contents loaded into every conversation.

### Recall

Sonnet-powered relevance selector scans up to 200 files, returns the 5 most relevant to the user's query. Demand-driven, not static indexing.

### Deliberate Exclusions

The system excludes: code patterns, architecture, git history, debugging solutions — anything derivable from the current project state.

## Coordinator Mode (Section 20)

`CLAUDE_CODE_COORDINATOR_MODE=1` transforms Claude Code into a multi-agent orchestrator.

### Architecture

Master coordinator directs parallel workers. Workers report back as XML `<task-notification>` messages. Coordinator never polls — workers push completion.

### Discipline

"Never write 'based on your findings'" — coordinator must synthesize worker research into specific specs with file paths, line numbers, and exactly what to change.

### 4-Phase Workflow

| Phase | Who | Purpose |
|-------|-----|---------|
| Research | Workers (parallel) | Investigate codebase, find files |
| Synthesis | Coordinator | Read findings, craft implementation specs |
| Implementation | Workers | Make changes per spec, commit |
| Verification | Workers | Prove the code works |

### Concurrency Rules

- Read-only tasks (research) — parallel freely
- Write-heavy tasks (implementation) — one at a time per file set
- Verification — can run alongside implementation on different file areas

### Continue vs. Spawn

| Situation | Action | Reason |
|-----------|--------|--------|
| Research explored the exact files to edit | Continue | Worker already has files in context |
| Research was broad, implementation narrow | Spawn fresh | Avoid exploration noise |
| Correcting a failure | Continue | Worker has error context |
| Verifying another worker's code | Spawn fresh | Verifier needs fresh eyes |
| Wrong approach entirely | Spawn fresh | Wrong context pollutes retry |

## Hooks: User-Defined Automation (Section 22)

Four hook types: command (shell execution), prompt (LLM evaluation), HTTP (POST to URL), agent (agentic verification loops).

Configuration: Event → Matcher[] → Hook[] where events include PreToolUse, PostToolUse, PreMessage, PostMessage. Matchers accept permission-rule-syntax patterns (e.g., `"Bash(git *)"`) to fire selectively.

Advanced features: `async: true` (background), `asyncRewake: true` (background with wake-on-exit-code-2), `once: true` (auto-removes after first execution), `statusMessage` (custom spinner text). Environment variable interpolation in HTTP headers requires explicit allowlist to prevent credential leakage.
