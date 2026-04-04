---
source: https://github.com/drapala/dream
upstream: https://github.com/sathwick-p/dream
author: Sathwick P (sathwick-p)
date: 2026-04-01
type: repo
---

# Dream — Memory Consolidation Skill for Claude Code

Give Claude Code a long-term memory that actually works. `/dream` is a memory consolidation skill that reviews recent sessions and distills them into durable, well-organized memories.

## The Problem

Claude Code forgets everything between sessions. Preferences, corrections, project context — gone.

## The Fix

4-phase memory consolidation:

1. **Orient** — scan memory directory, read index, skim files
2. **Gather** — scan recent session transcripts for new signals
3. **Consolidate** — create/update/merge memory files
4. **Prune** — remove stale memories, update MEMORY.md index

## What Gets Remembered

- Corrections and confirmed approaches
- Role, expertise, and preference signals
- Project decisions, deadlines, and context
- External system pointers (dashboards, trackers, docs)

## What Doesn't

- Code patterns, architecture, file paths (derivable from the code)
- Git history (that's what `git log` is for)
- Debugging solutions (the fix is in the code)

## 4 Memory Types

- **User**: role, preferences, knowledge level
- **Feedback**: corrections and confirmations on approach
- **Project**: ongoing work, goals, deadlines
- **Reference**: pointers to external systems

## Install

```bash
git clone https://github.com/sathwick-p/dream.git && cd dream && ./install.sh
```

Installs one file: `~/.claude/skills/dream/SKILL.md`

### Enhanced auto-extraction

For Claude to proactively save memories during normal work:

```bash
./install.sh --memory /path/to/your/project   # per project
./install.sh --memory ~/.claude                # global
```

## Relationship to KAIROS

Dream is a standalone open-source implementation of the KAIROS auto-dreaming subsystem described in the Claude Code internals article. KAIROS runs automatically via gates (24h, 5 sessions); Dream is manually invoked via `/dream`.
