# Wiki Index

<!-- 1 line per article: title + short context (~150 chars max) -->
<!-- MIGRATION TRIGGER: selection accuracy degrades at ~50-80 entries (ERL: random selection degrades at 40-60 items). -->
<!-- Token capacity limit is higher (~200 entries ≈ 7.5K tokens), but LLM selection accuracy is the binding constraint. -->
<!-- Split into thematic sub-indices (_index-agents.md, _index-retrieval.md, etc.) per RAPTOR mid-level node pattern. -->
<!-- Observable signal: /ask Layer 1 consistently misses relevant articles → time to split. -->

- [LLM Knowledge Base](concepts/llm-knowledge-base.md) — Core loop: raw/→wiki/→ask. Practitioner-described (not independently validated). Risks: AI-compiled content degrades RAG, model collapse
- [KB Architecture Patterns](concepts/kb-architecture-patterns.md) — OUR TAXONOMY of 4 patterns. Pattern 4 is a role/meta-pattern, not architecture. Scale thresholds extrapolated, not measured
- [Retrieval-Augmented Generation](concepts/retrieval-augmented-generation.md) — LC vs RAG eval: LC wins 56.3% vs 49%, but RAG irreplaceable for ~10%. Hybrid recommended
- [Context Management](concepts/context-management.md) — WITHIN-SESSION: 4-layer compaction (micro→snip→auto→collapse). How to operate within finite token budgets
- [Memory Consolidation](concepts/memory-consolidation.md) — CROSS-SESSION: KAIROS/Dream 4-phase cycle (orient→gather→consolidate→prune). How to persist knowledge between sessions
- [Multi-Agent Orchestration](concepts/multi-agent-orchestration.md) — Coordinator mode, single vs multi-agent, 4-phase workflow, isolation modes
- [Autonomous Research Agents](concepts/autonomous-research-agents.md) — 4-stage pipeline (plan→question→explore→report), benchmarks, 5 open challenges
- [Hybrid Search](concepts/hybrid-search.md) — QMD: BM25+vector+reranking on-device, RRF fusion, smart chunking, MCP integration
- [RAPTOR vs. Flat 3-Layer Retrieval](concepts/raptor-vs-flat-retrieval.md) — Tree vs flat comparison: structural parallels (not validation). Chunking benchmarks challenge concept-based segmentation
- [Agent Memory Architectures](concepts/agent-memory-architectures.md) — STORAGE STRUCTURES: MemGPT tiers, Synapse graph, Letta compression, CoALA cognitive taxonomy, EM-LLM surprise segmentation
- [Self-Improving Agents](concepts/self-improving-agents.md) — Reflexion (verbal) + ERL (heuristics) + RMM (RL) + TextGrad (verbal vs scalar gradients) + Absolute Zero (binary reward). L2: verbal +8pp, ancoragem +39pp
- [Tension Resolution](concepts/tension-resolution.md) — 5 mechanisms from papers inform design: grounded verification, self-enhancement risk, heuristic resolution, dynamic criteria, graph discovery
- [LLM-as-Judge](concepts/llm-as-judge.md) — 12 biases (self-enhancement most critical), GPT-4o near random on hard evals, dynamic criteria > static rubrics
- [Reflexion-Weighted Knowledge Graphs](concepts/reflexion-weighted-knowledge-graphs.md) — Original synthesis: adaptive retrieval topology where graph restructures based on failure feedback
- [Immune-Inspired Credit Assignment](concepts/immune-inspired-credit-assignment.md) — PARADIGM ALTERNATIVE: amplify successes, let failures die (CLONALG). Dissolves credit assignment. Never applied to KGs (confirmed gap, L1)
- [Groupthink and Cascades](concepts/groupthink-and-cascades.md) — RE-DISCOVERIES: semantic convergence = groupthink (Janis 1972), authority cascade = information cascade (Banerjee 1992). 50+ years of prior work. 2 missing Janis prescriptions.
- [Autonomous KB Failure Modes](concepts/autonomous-kb-failure-modes.md) — WHAT GOES WRONG without human: 4 silent failures over 30 days. System looks healthy while degrading
- [Curation Anti-Bias](concepts/curation-anti-bias.md) — HOW TO FIX IT: 3 bias layers + 5 improvements. Adversarial quota, split confidence, style check, multiagent spot-check
- [Question Taxonomy](concepts/question-taxonomy.md) — 7 frameworks (Miles, Socratic, Oblique, Popper, Lakatos, AHRQ, Simon). 10 question types + stopping rule
- [Fast-and-Frugal Heuristics (Gigerenzer)](concepts/fast-frugal-heuristics.md) — EXPLAINS "compression > raw": bias-variance trade-off. Less-is-more in small samples. PREDICTS reversal at scale (500+ articles)
- [Requisite Variety (Ashby)](concepts/requisite-variety.md) — ⏳QUARANTINED. "Only variety can destroy variety." V(compiler) < V(domain) → irreducible error floor. All 5 failure modes = 1 cause. 5 testable predictions.
- [Causal Reasoning (Pearl)](concepts/causal-reasoning-pearl.md) — CAUSAL LEVELS: association (seeing), intervention (doing), contrafactual (imagining). KB has 8 L1, 5 L2, 0 L3 claims
- [Formal Ontology for KBs](concepts/formal-ontology-for-kbs.md) — STRUCTURAL GAPS: untyped wikilinks, no hierarchy, no competency questions. 5 typed relations, continuant/occurrent, adoption path
- [Obsidian as Agent Wiki](concepts/obsidian-agent-workflow.md) — Default frontend for LLM KBs, vault separation pattern, 4-piece stack (app+clipper+CLI+skills)
