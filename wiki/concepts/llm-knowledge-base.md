---
title: "LLM Knowledge Base"
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
  - path: raw/papers/wikipedia-era-llms-risks.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [core-concept, knowledge-management, wiki, obsidian]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

An LLM Knowledge Base is a personal knowledge system where raw sources are "compiled" by an LLM into an interlinked markdown wiki, then queried via the same LLM for Q&A with source citation. The pattern emerged in April 2026 from practitioners (Karpathy, Elvis/DAIR.ai) who independently converged on the same architecture: raw/ → ingest → wiki/ → ask.

## Conteúdo

### The Core Loop

```
raw/ (immutable sources)
  → /ingest (LLM compiles concepts)
    → wiki/ (interlinked .md articles)
      → /ask (retrieval + Q&A with citations)
        → outputs/ (reports, slides, visualizations)
          → optionally filed back into wiki/
```

Key insight from Karpathy: "a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge." The LLM shifts from code tool to knowledge compiler.

### Karpathy's Architecture (April 2026)

- **raw/**: articles, papers, repos, datasets, images indexed into a directory
- **Wiki**: LLM incrementally "compiles" .md files with summaries, backlinks, concepts, articles, cross-links
- **Ingest**: Obsidian Web Clipper for articles → markdown; hotkey to download images locally
- **IDE**: Obsidian as frontend (view raw, wiki, visualizations). "The LLM writes and maintains all of the data of the wiki, I rarely touch it directly."
- **Q&A**: At ~100 articles / ~400K words, LLM answers complex questions without fancy RAG. Auto-maintained index files + brief summaries sufficient at this scale.
- **Output**: Markdown files, Marp slides, matplotlib images — all viewable in Obsidian. Outputs often filed back into wiki.
- **Linting**: LLM health checks find inconsistent data, impute missing data, suggest new article candidates.
- **Scaling vision**: "synthetic data generation + finetuning to have your LLM 'know' the data in its weights instead of just context windows"

### Elvis/DAIR.ai's Extensions

Elvis builds on the same pattern with key additions:

- **Automated curation**: a tuned Skill that finds high-signal research papers daily, replacing manual review
- **QMD indexing**: uses Tobi Lütke's [[hybrid-search|QMD]] for semantic search over the paper collection
- **Visual artifacts**: interactive artifact generator using MCP tools inside an agent orchestrator, visualizing insights from 100s of papers
- **Actionability focus**: "the research is only as good as the research questions. And the research questions are only as good as the insights the agents have access to."
- **Strong claim**: "everyone should be building both their own agent harnesses and their personal knowledge bases. Those are going to be a huge differentiator."

### Paulo Silveira's Human-in-the-Loop Variant (Open Claw)

A contrasting approach from Paulo Silveira (March 2026): the LLM assists with capture and classification, but humans maintain editorial control.

**Pipeline:** Telegram (voice/text/photos/links) → Whisper transcription → journaling → Claude Sonnet classification into concepts → drafts for blog posts. Storage in Git vault with Journal + Concepts + Drafts.

**Key philosophical difference:** "Eu poderia tentar deixar essa concatenação de ideias e reestruturação do texto para a máquina... Não farei." Silveira argues that full LLM rewriting creates generic "slop." The LLM organizes; the human writes.

**Historical context:** References Zettelkasten, personal wikis, and Dostoevsky dictating to his wife as stenographer. The pattern is old; the tools are new.

**Trade-off:** Capture time doesn't decrease, but no idea is lost. The bottleneck shifts from capture to synthesis — exactly where human judgment adds the most value.

### The "Ephemeral Wiki" Vision

Karpathy's follow-up: "every question to a frontier grade LLM spawns a team of LLMs to automate the whole thing: iteratively construct an entire ephemeral wiki, lint it, loop a few times, then write a full report. Way beyond a `.decode()`."

This connects to [[autonomous-research-agents]] — a persistent KB is a durable instance of what deep research agents do ephemerally.

### Index-Based Retrieval (Why Not RAG?)

Karpathy's surprising finding: at ~small scale (~100 articles), auto-maintained index files + brief summaries are sufficient. No need for embeddings or vector databases. The LLM "reads all the important related data fairly easily."

This maps to a 3-layer bandwidth-aware retrieval pattern:
1. Lightweight index (always loaded)
2. Article content (on-demand)
3. Raw sources (spot verification)

See [[context-management]] for the formal hierarchy and [[retrieval-augmented-generation]] for when RAG becomes necessary.

### Risks of LLM-Compiled Knowledge (challenging source)

The "Wikipedia in the Era of LLMs" study (Huang et al., 2025) provides empirical evidence that LLM-compiled content degrades the knowledge it compiles:

- AI-revised Wikipedia content **lowered RAG performance**, particularly in factual accuracy
- Feedback loop risk: "RAG systems could end up retrieving AI-generated information to fact-check AI-generated responses"
- Stylistic homogenization detected: sentences becoming "more AI-like, with longer, more complex sentences"
- If the wiki feels too synthetic, the human stops engaging — reducing the human-in-the-loop correction mechanism

This directly challenges the LLM-as-Compiler pattern. The mitigation: raw/ immutability ensures the "real data" is always accessible, but only if /review and /ask always re-read raw/ rather than trusting wiki alone. See [[autonomous-kb-failure-modes]] for the full degradation timeline.

## Interpretação

Ver seções marcadas com (⚠️) no Conteúdo acima — conteúdo interpretativo está inline por razões de coesão narrativa.

## Conexões

- [[retrieval-augmented-generation]] — the academic framing of when LC vs RAG is needed
- [[hybrid-search]] — QMD as the upgrade path when flat index retrieval hits limits
- [[memory-consolidation]] — the KB's /review cycle mirrors the dream consolidation pattern
- [[autonomous-research-agents]] — KB is persistent deep research; deep research is ephemeral KB
- [[kb-architecture-patterns]] — taxonomy of 4 KB patterns; this KB implements Pattern 1
- [[obsidian-agent-workflow]] — the frontend layer for viewing and navigating the wiki
- [[autonomous-kb-failure-modes]] — what goes wrong when the compilation loop runs unsupervised

## Fontes

- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — original tweet defining the architecture: raw/ → compile → wiki/ → Q&A → lint
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — extensions: automated curation, QMD search, visual artifacts, actionability
- [Paulo Silveira — Open Claw](../../raw/articles/paulo-silveira-open-claw-pkm.md) — human-in-the-loop variant: LLM classifies, human writes. Anti-slop philosophy
- [Wikipedia Risks](../../raw/papers/wikipedia-era-llms-risks.md) — (challenging) AI-revised content lowers RAG performance, stylistic homogenization empirically detected
