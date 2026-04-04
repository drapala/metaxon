---
title: "Obsidian as Agent Wiki"
sources:
  - path: raw/articles/kepano-obsidian-agent-workflow.md
    type: note
    quality: secondary
  - path: raw/articles/karpathy-llm-knowledge-bases.md
    type: note
    quality: tertiary
  - path: raw/articles/elvis-personal-kb-agents.md
    type: note
    quality: tertiary
created: 2026-04-03
updated: 2026-04-03
tags: [obsidian, tooling, workflow, ide]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Obsidian is emerging as the default frontend/IDE for LLM-compiled knowledge bases. Three independent practitioners (Karpathy, Elvis, Kepano) converge on the same setup: a local-first markdown editor with graph view, backlinks, and plugin ecosystem — where the LLM writes the wiki and the human reads it in Obsidian. Kepano (CEO of Obsidian) endorses vault separation as the recommended pattern.

## Conteúdo

### Why Obsidian?

- **Local-first**: all data is plain markdown files on disk — no vendor lock-in
- **Wikilinks**: `[[concept]]` syntax creates an interlinked knowledge graph
- **Graph view**: visual exploration of concept connections
- **Plugin ecosystem**: Marp for slides, Web Clipper for ingestion, community plugins for visualization
- **Human-first philosophy**: "You can explore the Obsidian website and app without ever encountering the word 'AI' or a sparkly button" (Kepano)

### The Four Pieces (Kepano's Stack)

1. **Obsidian app** — the local-first markdown editor
2. **Obsidian Web Clipper** extension — capture web content in .md format
3. **Obsidian CLI** — agents interact with the full app feature set (backlinks, bases, etc.)
4. **Obsidian Skills** — agents know how to create .md, .base, and .canvas files

Reference: https://obsidian.md/help/headless

### Vault Separation Pattern

Kepano's recommended approach for contamination mitigation:

> "Keep your personal vault clean and create a messy vault for your agents."

> "I prefer my personal Obsidian vault to be high signal:noise, and for all the content to have known origins."

**Two vaults:**
- **Personal vault**: high signal:noise, known origins, human-curated
- **Agent vault**: LLM-generated, auto-compiled, potentially messy

This separation prevents LLM-generated content from contaminating the human's trusted knowledge space. An [[llm-knowledge-base]] like this one is the "agent vault."

### Practitioner Usage

| Who | How they use Obsidian |
|-----|----------------------|
| Karpathy | IDE frontend for raw data, compiled wiki, and derived visualizations. Uses Web Clipper + image hotkey for ingestion. Marp for slides. |
| Elvis | MD vaults for research papers. Visual artifact generator with MCP tools. Interactive data views. |
| Kepano | Endorses the pattern officially. Advocates vault separation and headless CLI for agent interaction. |

## Interpretação

Nenhuma interpretação significativa neste artigo — conteúdo é factual direto das fontes.

## Conexões

- [[llm-knowledge-base]] — Obsidian is the default frontend for the raw/ → wiki/ → outputs/ loop
- [[hybrid-search]] — QMD can index Obsidian vaults as collections for semantic search
- [[kb-architecture-patterns]] — all 3 practitioner patterns (Karpathy, Elvis, Silveira) use Obsidian

## Fontes

- [Kepano — Obsidian Agent Workflow](../../raw/articles/kepano-obsidian-agent-workflow.md) — CEO endorsement: 4-piece stack, vault separation, human-first philosophy
- [Karpathy — LLM Knowledge Bases](../../raw/articles/karpathy-llm-knowledge-bases.md) — Obsidian as IDE, Web Clipper, Marp slides
- [Elvis — Personal KB for Agents](../../raw/articles/elvis-personal-kb-agents.md) — MD vaults, visual artifacts, interactive views
