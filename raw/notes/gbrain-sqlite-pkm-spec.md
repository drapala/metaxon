# GBrain: Complete Build Spec

**Source:** https://gist.github.com/garrytan/49c88e83cf8d7ae95e087426368809cb  
**Author:** Garry Tan  
**Date captured:** 2026-04-05  
**Type:** Design specification (practitioner-authored)

---

## Overview

GBrain is an open-source personal knowledge management system designed to replace
file-based wikis that have outgrown Git's scalability. The project documentation
describes it as "open-source personal knowledge brain. SQLite + FTS5 + vector
embeddings in one file."

## Core Architecture

The system employs a "thin CLI + fat skills" pattern borrowed from GStack. The
command-line interface (~500 lines of TypeScript) dispatches to a minimal core
library, while intelligence resides in markdown skill files that Claude Code reads
and executes. This separation allows updates to workflows without recompilation.

## Technical Foundation

**Database Layer:** SQLite with full-text search (FTS5) and vector embeddings in a
single file, eliminating the need for separate services or infrastructure.

**Storage Model:** Two content layers:
- "Above the line (compiled truth)" — current intelligence, synthesized content
- "Below the line (timeline)" — append-only evidence, raw source material

This architecture maps directly to database columns in the pages table.

**Schema — 9 tables:**
- `pages`: title, compiled_content, timeline, metadata
- FTS5 virtual table for keyword search
- `page_embeddings` for vector similarity search
- Supporting tables: links, tags, timeline_entries, raw_enrichment_data

**CLI commands:** get, put, search, query, ingest, link, timeline, list, stats, export, import

## Search Capabilities

Three search approaches combined: full-text keyword (FTS5), semantic vector (embeddings),
and structured relational queries. Results merge and rank across methods.

## MCP Integration

MCP server exposes the brain to Claude Code, Cursor, and other compliant clients
via stdio transport. Eliminates custom integration overhead.

## Migration Strategy

Migration from 7,471 existing markdown files (~2.3GB) into the database. Rationale:
"git struggles" at this scale. Round-trip export capability ensures no lock-in.

## Skill Files (5 documented workflows)

- **Ingest:** meetings, articles, documents → structured pages
- **Query:** multi-method search and synthesis
- **Maintain:** lint checks for contradictions and stale information
- **Enrich:** API-driven data augmentation (Crustdata and similar)
- **Briefing:** daily status compilation

"Claude Code reads these skill files at startup, eliminating the need to encode
workflows into compiled code."

## Development

Seven-phase build sequence. Estimated total build time: ~2.5 hours using Claude Code.
Phases: database + core commands → search → import/export → MCP server → polish.
