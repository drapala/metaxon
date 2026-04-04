# Wiki Index

<!-- 1 line per article: title + short context (~150 chars max) -->
<!-- MIGRATION TRIGGER: selection accuracy degrades at ~50-80 entries (ERL: random selection degrades at 40-60 items). -->
<!-- Token capacity limit is higher (~200 entries ≈ 7.5K tokens), but LLM selection accuracy is the binding constraint. -->
<!-- Split into thematic sub-indices (_index-agents.md, _index-retrieval.md, etc.) per RAPTOR mid-level node pattern. -->
<!-- Observable signal: /ask Layer 1 consistently misses relevant articles → time to split. -->

- [LLM Knowledge Base](concepts/llm-knowledge-base.md) — THE core loop: raw/→ingest→wiki/→ask. Karpathy, Elvis, Silveira practitioner approaches. No RAG needed at <200 articles
- [KB Architecture Patterns](concepts/kb-architecture-patterns.md) — TAXONOMY of 4 patterns (who synthesizes × how retrieval scales). ERL validates concept articles > raw dumps
- [Retrieval-Augmented Generation](concepts/retrieval-augmented-generation.md) — LC vs RAG eval: LC wins 56.3% vs 49%, but RAG irreplaceable for ~10%. Hybrid recommended
- [Context Management](concepts/context-management.md) — WITHIN-SESSION: 4-layer compaction (micro→snip→auto→collapse). How to operate within finite token budgets
- [Memory Consolidation](concepts/memory-consolidation.md) — CROSS-SESSION: KAIROS/Dream 4-phase cycle (orient→gather→consolidate→prune). How to persist knowledge between sessions
- [Multi-Agent Orchestration](concepts/multi-agent-orchestration.md) — Coordinator mode, single vs multi-agent, 4-phase workflow, isolation modes
- [Autonomous Research Agents](concepts/autonomous-research-agents.md) — 4-stage pipeline (plan→question→explore→report), benchmarks, 5 open challenges
- [Hybrid Search](concepts/hybrid-search.md) — QMD: BM25+vector+reranking on-device, RRF fusion, smart chunking, MCP integration
- [RAPTOR vs. Flat 3-Layer Retrieval](concepts/raptor-vs-flat-retrieval.md) — Tree vs flat comparison: _index.md validated as RAPTOR root node, 3 improvements without infra
- [Agent Memory Architectures](concepts/agent-memory-architectures.md) — STORAGE STRUCTURES: MemGPT tiers, Synapse graph, Letta compression, CoALA cognitive taxonomy, EM-LLM surprise segmentation
- [Self-Improving Agents](concepts/self-improving-agents.md) — Reflexion (verbal reflection) + ERL (heuristics > trajectories). Validates concept articles over raw dumps
- [Tension Resolution](concepts/tension-resolution.md) — 5 mechanisms from papers inform design: grounded verification, self-enhancement risk, heuristic resolution, dynamic criteria, graph discovery
- [LLM-as-Judge](concepts/llm-as-judge.md) — 12 biases (self-enhancement most critical), GPT-4o near random on hard evals, dynamic criteria > static rubrics
- [Reflexion-Weighted Knowledge Graphs](concepts/reflexion-weighted-knowledge-graphs.md) — Original synthesis: adaptive retrieval topology where graph restructures based on failure feedback
- [Autonomous KB Failure Modes](concepts/autonomous-kb-failure-modes.md) — WHAT GOES WRONG without human: 4 silent failures over 30 days. System looks healthy while degrading
- [Curation Anti-Bias](concepts/curation-anti-bias.md) — HOW TO FIX IT: 3 bias layers + 5 improvements. Adversarial quota, split confidence, style check, multiagent spot-check
- [Question Taxonomy](concepts/question-taxonomy.md) — 7 research gaps + 6 Socratic techniques + oblique strategies. Typed questions that open instead of close
- [Obsidian as Agent Wiki](concepts/obsidian-agent-workflow.md) — Default frontend for LLM KBs, vault separation pattern, 4-piece stack (app+clipper+CLI+skills)
