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
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/wikipedia-era-llms-risks.md
    type: paper
    quality: primary
  - path: raw/papers/model-collapse-recursive-training.md
    type: paper
    quality: primary
  - path: raw/papers/chunking-strategies-rag-comparison.md
    type: paper
    quality: primary
  - path: raw/notes/gbrain-sqlite-pkm-spec.md
    type: note
    quality: secondary
    stance: challenging
created: 2026-04-03
updated: 2026-04-05
tags: [taxonomy, architecture, patterns]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: emergence
emergence_trigger:
  pair: [llm-knowledge-base, context-management]
  ask_session: null
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-03
---

## Resumo

Four architectural patterns for LLM-powered KBs plus one cross-cutting retrieval constraint. Pattern 4 (DB-Backed PKM / GBrain) adds a SQLite-based alternative to file-based wikis — challenging the current KB's architecture at scale. GBrain names the "thin CLI + fat skills" design principle already implicit in Claude Code and this KB's command structure. Scale thresholds throughout are 1-anecdote estimates, not benchmarks. Bandwidth-Aware Retrieval is a role/constraint, not a pattern (reclassified from "Pattern 4" in original — that was a category error).

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

**When to use:** Solo researcher, small scale. Karpathy reports ~100 articles working well — upper bound unknown (no data beyond 1 anecdote).

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

**When to use:** Heavy paper consumption. Elvis reports "100s of papers" — no precise threshold stated.

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

### Pattern 4: DB-Backed PKM (GBrain)

**Originator:** Garry Tan (April 2026)

**Architecture:** `SQLite (compiled_truth + timeline) ← thin CLI + fat skills → MCP → Claude Code`

**Key characteristics:**
- Single-file database: SQLite + FTS5 + vector embeddings — no server, no Docker, no connection strings
- **"Thin CLI + fat skills"**: harness is ~500 lines TypeScript; all intelligence lives in markdown skill files read at runtime by Claude Code. Updating a workflow = editing a .md file, not recompiling.
- **Two-layer storage model**:
  - "Above the line" = compiled_truth (synthesized, current intelligence)
  - "Below the line" = timeline (append-only raw evidence)
- Three search methods unified: FTS5 keyword + vector semantic + structured relational
- MCP server exposes brain to Claude Code, Cursor, and compliant clients via stdio
- Lossless round-trip export (SQLite → markdown) prevents lock-in

**Scale rationale:** Designed to replace file-based wikis past ~7,471 markdown files (~2.3GB) where "git struggles." No benchmark data — 1 practitioner's use case.

**Strengths:** Zero-infrastructure, unified search, harness pattern enables workflow changes without recompilation. MCP integration is native.
**Weaknesses:** SQLite not designed for concurrent writes. Vendor lock-in risk reduced by export but not eliminated. No independent validation of scale claims.

**When to use:** Solo researcher who has exhausted git-based markdown at scale (thousands of files). When hybrid search in a single file is preferable to file system + external vector DB.

**Design principle extracted (generalizable beyond GBrain):**

> **"Thin CLI + fat skills"**: keep the harness minimal and dumb; encode all workflow intelligence in human-readable instruction files. This is also the pattern of Claude Code's CLAUDE.md + .claude/commands/, and of this KB's /ask, /ingest, /emerge commands. GBrain names and formalizes what is already implicit here.

### Cross-Cutting Concern: Bandwidth-Aware Retrieval

**Not a pattern — a constraint.** This applies to ALL three patterns above, not as an alternative. It describes HOW retrieval should work within any architecture, not WHICH architecture to choose.

**Source:** Claude Code internals (March 2026)

**Mechanism:** Layered retrieval with progressive escalation + circuit breakers:
- 3+ layers: lightweight index (always loaded) → article content (on-demand) → raw sources (spot-check)
- Progressive compaction: micro → snip → auto → collapse
- Circuit breakers prevent thrashing (max 3 consecutive failures)
- Principle: "never read more than you need at each layer"

**Strengths:** Token-efficient, production-proven. Graceful degradation under pressure.
**Weaknesses:** Designed for conversations, not knowledge bases. No notion of source quality.

**Ontological note (BFO):** Patterns 1-3 are Independent Continuants (architectures). Bandwidth-Aware Retrieval is a Role — a function applied to any architecture depending on context. Previously listed as "Pattern 4" which was a category error.

### Comparison Matrix

| Pattern | Who synthesizes | Retrieval | Scale | Bottleneck |
|---------|----------------|-----------|-------|------------|
| LLM-as-Compiler | LLM | Index-based (LC) | ~100 articles (1 anecdote) | Ingest quality |
| Agent-as-Curator | LLM + tools | Hybrid search | "100s of papers" (1 anecdote) | Tooling setup |
| Human-in-the-Loop | Human | LLM classification | Unknown (no data) | Human time |

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

## Verificação Adversarial

**Claim mais fraco (Pattern 4):** "git struggles at 7,471 files / 2.3GB." Git handles thousands of small text files fine; the real bottleneck is embedding search + diff on large blobs. The claim is too broad without benchmark data — 1 practitioner's use case.

**O que o GBrain não diz:** (a) no comparison between SQLite and file-based at equal scale; (b) SQLite has its own limits (concurrent writes, blob storage overhead); (c) "thin CLI + fat skills" works because Claude Code reads files — this won't generalize to tools without file access.

**Simplificações:** "git doesn't scale" was condensed — it's specifically slow for operations on thousands of large files and for embedding search, not for version history or small text files.

**Prior work:** GBrain explicitly references Claude Code internals (GStack pattern). The "thin CLI + fat skills" pattern precedes GBrain in the Claude Code ecosystem.

## Conexões

- instanceOf: [[llm-knowledge-base]] — this KB is an instance of Pattern 1 (LLM-as-Compiler)
- complementsAt: [[hybrid-search]] — Pattern 2's retrieval layer; Pattern 4 internalizes FTS5+vector
- derivedFrom: [[context-management]] — Bandwidth-Aware Retrieval formalized from Claude Code internals
- complementsAt: [[memory-consolidation]] — KAIROS cycle parallels /review; trigger gates transferable
- validates: [[retrieval-augmented-generation]] — LC > RAG at small scale (consistent with Pattern 1, not validation)
- validates: [[self-improving-agents]] — ERL heuristics > trajectories on Gaia2 (domain transfer not tested)
- contradicts: [[obsidian-agent-workflow]] ON "file-based markdown is the default PKM backend at scale" — Pattern 4 proposes SQLite as alternative past ~7K files

## Fontes

- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — Pattern 1: the original architecture
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — Pattern 2: automated curation + QMD + visual artifacts
- [Paulo Silveira — Open Claw](../../raw/articles/paulo-silveira-open-claw-pkm.md) — Pattern 3: human-in-the-loop, anti-slop philosophy
- [Claude Code Internals](../../raw/articles/claude-code-internals-harness-engineering.md) — Bandwidth-Aware Retrieval (cross-cutting constraint); thin CLI pattern precursor
- [GBrain Spec](../../raw/notes/gbrain-sqlite-pkm-spec.md) — (challenging) Pattern 4: DB-Backed PKM; formalizes "thin CLI + fat skills"; challenges file-based wikis at scale
- [LC vs RAG Paper](../../raw/papers/long-context-vs-rag-evaluation.md) — Consistent with Pattern 1 at small scale (LC 56.3% vs RAG 49.0%; paper says "neither universally dominates")
- [RAPTOR Paper](../../raw/papers/raptor-recursive-abstractive-retrieval.md) — Analogous to _index.md pattern. Not a validation — RAPTOR doesn't test wikis or manual pointers.
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — Consistent with concept articles approach (heuristics > trajectories on Gaia2; domain transfer not tested)
- [Wikipedia Risks](../../raw/papers/wikipedia-era-llms-risks.md) — (challenging) AI-revised content lowers RAG performance. Challenges Pattern 1 core assumption.
- [Model Collapse](../../raw/papers/model-collapse-recursive-training.md) — (challenging) Recursive self-consumption destroys diversity. Pattern 1 feedback loop is self-consumption.
- [Chunking Benchmarks](../../raw/papers/chunking-strategies-rag-comparison.md) — (challenging) Page-level chunking won NVIDIA benchmark. Concept-based segmentation may not be optimal.

## Quality Gate
- [x] Wikilinks tipados: 7 relações tipadas (instanceOf, complementsAt ×2, derivedFrom, validates ×2, contradicts)
- [x] Instance→class: escala do GBrain qualificada como "1 practitioner's use case, sem benchmark"
- [x] Meta-KB separado: "thin CLI + fat skills" como princípio extraído, não como descrição desta KB
- [x] Resumo calibrado: menciona "challenging the current KB's architecture"
