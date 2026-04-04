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
- [Requisite Variety (Ashby)](concepts/requisite-variety.md) — "Only variety can destroy variety." V(compiler) < V(domain) → irreducible error floor. All 5 failure modes = 1 cause. 5 testable L2 predictions. Predição C parcialmente confirmada.
- [Stigmergic Coordination (Grassé)](concepts/stigmergic-coordination.md) — KB = stigmergic system: wiki is environment, wikilinks are pheromones. Typed links = better coordination. Observado em sessão: /ingest sem conexões → /ask descobriu-as espontaneamente.
- [Complexity and Emergence (Waldrop)](concepts/complexity-emergence.md) — VOCABULARY: emergence, edge of chaos, fitness landscape, path dependence. May (1972) âncora os claims. KB drifting toward order-death — predição com falsificador.
- [Predictive Processing (Friston)](concepts/predictive-processing.md) — Supersedes "LLM as amplifier": prediction error minimizer. Self-assessment = convergence to minimum surprise. Suportado por Tulving+McClelland (prior work).
- [Causal Reasoning (Pearl)](concepts/causal-reasoning-pearl.md) — CAUSAL LEVELS: association (seeing), intervention (doing), contrafactual (imagining). KB has 8 L1, 5 L2, 0 L3 claims
- [Formal Ontology for KBs](concepts/formal-ontology-for-kbs.md) — STRUCTURAL GAPS: untyped wikilinks, no hierarchy, no competency questions. 5 typed relations, continuant/occurrent, adoption path
- [Obsidian as Agent Wiki](concepts/obsidian-agent-workflow.md) — Default frontend for LLM KBs, vault separation pattern, 4-piece stack (app+clipper+CLI+skills)
- [Variety Gap Analysis](concepts/variety-gap-analysis.md) — ⚠️ ESPECULATIVO. Gap V(compiler)/V(domain) por dimensão. Gap Beer/VSM preenchido. Gap Shannon parcialmente preenchido.
- [Bibliometrics](concepts/bibliometrics.md) — Pritchard 1969: "application of math/stats to books and media." Field definition. Utility-tracker = bibliometrics da KB (⚠️ nossa interpretação)
- [Bradford's Law of Scattering](concepts/bradford-law-scattering.md) — Bradford 1934: zonas 1:n:n², rendimento decrescente. Proxy para V gap por domínio (⚠️ interpretação)
- [Information Theory (Shannon)](concepts/information-theory-shannon.md) — H = −Σ p log p. Bit como unidade. Capacidade de canal. Proxy V(LLM) via entropia = ⚠️ interpretação. Hub fundacional do cluster info-theory.
- [Viable System Model (Beer)](concepts/viable-system-model-beer.md) — Variety attenuation/amplification, recursão VSM. Multi-regulator coordination. Estende Ashby para organizações hierárquicas.
- [Information Bottleneck (Tishby)](concepts/information-bottleneck.md) — L[p(x̃|x)] = I(X̃;X) − βI(X̃;Y). Compressão que preserva relevância. Operacionaliza tradeoff V/relevância.
- [Partial Information Decomposition (Wibral)](concepts/partial-information-decomposition.md) — Unique + shared + synergistic information. Diagnóstico de ensembles de compiladores.
- [Team Decision Theory (Ho & Chu)](concepts/team-decision-theory.md) — ⏳QUARANTINED. Information structures, precedence diagram. Multi-compiler coordination. OCR degradado ~30%.
- [Rate Distortion Theory](concepts/rate-distortion-theory.md) — R(D) = min I(X;X̂) s.t. E[d]≤D. Theorem 13.2.1. Gaussian: R(D)=½log(σ²/D). Foundation for IB and CEO problem.
- [Network Information Theory](concepts/network-information-theory.md) — Slepian-Wolf: correlated sources encodable at H(X,Y) with independent encoders. MAC capacity region. Wyner-Ziv. CEO problem foundations.
- [CEO Problem](concepts/ceo-problem.md) — L encoders observe noisy Yᵢ of source X independently; CEO reconstructs at distortion D. Under log loss: Berger-Tung is tight (Courtade 2014, first general result).
- [Rational Inattention](concepts/rational-inattention.md) — Sims 2003: I(X;Y)≤C constraint. Gaussian: Var(Y|X)=σ²/e^{2C}. Rate distortion applied to cognition. Price stickiness as endogenous output.
- [Judgment Aggregation](concepts/judgment-aggregation.md) — ⚠️ CHALLENGING. Theorem 1: no function satisfies U+A+S + consistent collective judgments. Doctrinal paradox. Majority voting on claims → logical inconsistency.
- [PAC-Bayes Bounds](concepts/pac-bayes-bounds.md) — E[R(θ)]≤E[r(θ)]+√(KL(ρ||π)/n). Prior/posterior on predictors. First non-vacuous bounds on NNs (Dziugaite 2017). Ensemble generalization framework.
- [Heuristics and Biases](concepts/heuristics-and-biases.md) — K&T (1974): 3 heurísticas (representatividade, disponibilidade, ancoragem) → vieses sistemáticos previsíveis. Atalhos adaptativos com zonas de falha.
- [Prospect Theory](concepts/prospect-theory.md) — K&T (1979): valor sobre ganhos/perdas, não riqueza final. Loss aversion (λ≈2). Certainty effect, reflection effect. ~80k citações Econometrica.
- [Social Choice Aggregation](concepts/social-choice-aggregation.md) — Arrow (1950): impossibilidade com Unanimidade+IIA+Não-Ditadura → única SWF é ditadura. Black (1948): single-peaked prefs → eleitor mediano vence (escape route).
- [Complexity-Stability Tradeoff](concepts/complexity-stability-tradeoff.md) — May (1972): σ√(nC) < 1 para estabilidade. Complexidade aleatória → instabilidade. Contra-intuitivo; modularidade necessária.
- [Resource Competition and Coexistence](concepts/resource-competition-coexistence.md) — Tilman (1994): modelos espaciais com trade-off colonização-competição permitem coexistência ilimitada num único recurso. Resolve paradoxo de exclusão competitiva.
- [Zipf's Law and Power Laws in Language](concepts/zipf-law-power-laws.md) — Ferrer-i-Cancho (2003): Zipf emerge na transição de fase λ*≈0.41 entre comunicação inútil e perfeita. Piantadosi (2014): nenhuma teoria explica tudo ainda.
- [Falsificationism and Demarcation](concepts/falsificationism-demarcation.md) — Popper (1963): ciência = falsificável, não verificável. Einstein > Freud/Adler: risco epistêmico. Confirmações fáceis valem pouco.
- [Scientific Research Programmes](concepts/scientific-research-programmes.md) — Lakatos (1970): hard core + protective belt + heurísticas. Progressivo (novas predições) vs. degenerativo (só acomoda). Responde à crítica Duhem-Quine a Popper.
- [Episodic and Semantic Memory](concepts/episodic-semantic-memory.md) — Tulving (2002): episódica = autonoética, temporal, 1ª pessoa; semântica = noética, atemporal. Hipocampo crítico para episódica. Mental time travel.
- [Complementary Learning Systems](concepts/complementary-learning-systems.md) — McClelland (1995): catastrophic interference → dois sistemas. Hipocampo (rápido/esparso) + neocórtex (lento/distribuído). Replay durante sono = consolidação sistêmica.
