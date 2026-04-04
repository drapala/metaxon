# Wiki Index

<!-- 1 line per article: title + short context (~150 chars max) -->
<!-- MIGRATION TRIGGER: when this file exceeds ~200 entries, split into thematic sub-indices -->
<!-- (_index-agents.md, _index-retrieval.md, etc.) per RAPTOR mid-level node pattern -->

- [LLM Knowledge Base](concepts/llm-knowledge-base.md) — raw/→ingest→wiki/→ask loop, Karpathy+Elvis+Silveira architectures, index retrieval at small scale
- [KB Architecture Patterns](concepts/kb-architecture-patterns.md) — 4 patterns: LLM-as-Compiler, Agent-as-Curator, Human-in-the-Loop, Bandwidth-Aware Retrieval
- [Retrieval-Augmented Generation](concepts/retrieval-augmented-generation.md) — LC vs RAG eval: LC wins 56.3% vs 49%, but RAG irreplaceable for ~10%. Hybrid recommended
- [Context Management](concepts/context-management.md) — 4-layer compaction hierarchy (micro→snip→auto→collapse), bandwidth-aware retrieval pattern
- [Memory Consolidation](concepts/memory-consolidation.md) — KAIROS/Dream 4-phase cycle (orient→gather→consolidate→prune), 4 memory types, gated triggers
- [Multi-Agent Orchestration](concepts/multi-agent-orchestration.md) — Coordinator mode, single vs multi-agent, 4-phase workflow, isolation modes
- [Autonomous Research Agents](concepts/autonomous-research-agents.md) — 4-stage pipeline (plan→question→explore→report), benchmarks, 5 open challenges
- [Hybrid Search](concepts/hybrid-search.md) — QMD: BM25+vector+reranking on-device, RRF fusion, smart chunking, MCP integration
- [RAPTOR vs. Flat 3-Layer Retrieval](concepts/raptor-vs-flat-retrieval.md) — Tree vs flat comparison: _index.md validated as RAPTOR root node, 3 improvements without infra
- [Agent Memory Architectures](concepts/agent-memory-architectures.md) — 3 patterns: hierarchical tiers (MemGPT), dynamic graph (Synapse), layered compression (Letta)
- [Self-Improving Agents](concepts/self-improving-agents.md) — Reflexion (verbal reflection) + ERL (heuristics > trajectories). Validates concept articles over raw dumps
- [Tension Resolution](concepts/tension-resolution.md) — 5 mechanisms from papers inform design: grounded verification, self-enhancement risk, heuristic resolution, dynamic criteria, graph discovery
- [LLM-as-Judge](concepts/llm-as-judge.md) — 12 biases (self-enhancement most critical), GPT-4o near random on hard evals, dynamic criteria > static rubrics
- [Reflexion-Weighted Knowledge Graphs](concepts/reflexion-weighted-knowledge-graphs.md) — Original synthesis: adaptive retrieval topology where graph restructures based on failure feedback
- [Autonomous KB Failure Modes](concepts/autonomous-kb-failure-modes.md) — 4 silent failures over 30 days: semantic convergence, authority cascade, index bloat, forced tension resolution
- [Obsidian as Agent Wiki](concepts/obsidian-agent-workflow.md) — Default frontend for LLM KBs, vault separation pattern, 4-piece stack (app+clipper+CLI+skills)
