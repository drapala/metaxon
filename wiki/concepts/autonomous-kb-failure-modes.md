---
title: "Autonomous KB Failure Modes"
sources:
  - path: raw/papers/calm-llm-judge-biases.md
    type: paper
    quality: primary
  - path: raw/papers/judgebench-evaluating-llm-judges.md
    type: paper
    quality: primary
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/synapse-episodic-semantic-memory.md
    type: paper
    quality: primary
  - path: raw/papers/multiagent-debate-factuality.md
    type: paper
    quality: primary
  - path: raw/papers/model-collapse-recursive-training.md
    type: paper
    quality: primary
  - path: raw/papers/wikipedia-era-llms-risks.md
    type: paper
    quality: primary
  - path: raw/papers/llms-reliability-as-knowledge-bases.md
    type: paper
    quality: primary
created: 2026-04-04
updated: 2026-04-05
tags: [meta-kb, failure-analysis, safety, original-insight]
source_quality: high
interpretation_confidence: medium
resolved_patches:
  - date: 2026-04-05
    original: "[patch: novo failure mode — List & Pettit 2002]"
    incorporated_as: "Failure Mode 5 — Judgment Aggregation Impossibility, adicionado a ## Gaps não resolvidos / Especulação"
    source: judgment-aggregation
reads: 4
retrievals_correct: 2
retrievals_gap: 0
last_read: 2026-04-05
provenance: emergence
emergence_trigger:
  pair: [llm-as-judge, self-improving-agents]
  ask_session: null
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-04
quarantine: false
quarantine_created: 2026-04-04
quarantine_reason: "retrofit — speculative synthesis"
quarantine_promoted: 2026-04-05
quarantine_criteria_met:
  tempo: true
  review_frio: true  # satisfied by challenge 2026-04-05 (different session/date from creation)
  adversarial_or_scout_or_prediction: true  # 2 challenges: 11-09 + 16-30, both PUBLICÁVEL
---

## Resumo

An LLM-operated KB without human intervention degrades silently over ~30 days through 4 failure modes: semantic convergence (articles homogenize), authority bias cascade (errors crystallize via circular validation), index bloat (growth without quality gate), and forced tension resolution (nuance eliminated). The system appears healthy on all automated metrics while quality erodes — the KB equivalent of reward hacking.

## Conteúdo

### Failure Mode 1: Semantic Convergence (Week 1-2)

**Mechanism:** Self-enhancement bias (CALM: 16.1% error) + unsupervised /review = LLM rewrites articles in its preferred style each review cycle. "Convert vague to precise" and "deduplicate" are opportunities to homogenize.

**Academic formalization: Model Collapse** (Shumailov et al., Nature 2024). Recursive self-consumption destroys distributional diversity — "tails of the original content distribution disappear." Applied to KBs: when an LLM compiles wiki from its own synthesis, diversity narrows and nuance disappears. The mitigation from the paper: "if data accumulates and models train on a mixture of real and synthetic data, model collapse no longer occurs." For us: /review must always re-read raw/ (real data), never operate only on wiki/ (synthetic data).

**Empirical validation: Wikipedia risks** (Huang et al., 2025). "AI-revised Wikipedia content lowered RAG performance, particularly in factual accuracy." Stylistic homogenization detected at Wikipedia scale: sentences becoming "more AI-like, with longer, more complex sentences." Our KB is a micro-scale version of the same phenomenon.

**Why invisible:** Wiki gets *more consistent*, not less. All /review metrics stay green. Problem is qualitative: wiki loses perspective diversity that justifies having multiple sources.

**Evidence:** ERL shows random heuristic inclusion degrades after 40-60 items. When all articles use same formulations, _index.md loses discriminative power. Note: this 40-60 threshold also applies to _index.md scaling — see [[raptor-vs-flat-retrieval]] Gap 3 for the connection between ERL's selection limit and the practical threshold for sub-index migration.

**Breaks:** /ask on subtle topics returns generic answers. Distinctions from original sources (Karpathy writes differently than an academic paper) are lost.

### Failure Mode 2: Authority Bias Cascade (Week 2-3)

**Mechanism:** Authority bias (CALM) makes LLM trust cited claims more. Wiki articles cite raw/. When /ask verifies wiki against raw/ (Layer 3), it tends to *confirm* because raw/ was the original source — circular validation loop.

**Compounding:** Without human reading raw/ with fresh eyes, /ingest misinterpretations crystallize. JudgeBench: self-assessment on difficult problems is near-random. If original interpretation was plausibly wrong, LLM "verifies" and agrees with itself.

**Evidence:** Reflexion ablation — self-reflection without *independent* grounded feedback degrades to 52% (on HumanEval, with test generation). raw/ is grounded but read by the same LLM. Ground truth needs independent evaluator.

**Empirical validation (Zheng et al., 2024):** Testing 26 LLMs as knowledge bases found that larger models are MORE consistently wrong: "models with 65-70B parameters demonstrate higher consistency even when providing wrong answers." The correlation paradox: r=0.78-0.81 between consistency on correct AND wrong answers. You can't get one without the other. This means our authority cascade isn't speculative — it's an empirically documented property of LLMs as knowledge stores. Cross-paper synthesis (our wiki's novel insights) falls under "unseen knowledge" where factuality degrades most.

### Failure Mode 3: Index Bloat (Week 2-4)

**Mechanism:** Automated /ingest without human quality gate. Confidence scoring (high/medium/low) is self-assessment (failure mode 2 applies). Tertiary sources create low-value articles that occupy _index.md space.

**Breaks:** _index.md approaches migration trigger (~200 entries). /ask spends more tokens on orientation, less on depth. ERL shows indiscriminate inclusion is counterproductive.

**Evidence:** Tim Kellogg — "compression becomes cognitive work." Without human deciding what deserves wiki vs. stays in raw/, agent treats everything as equally important.

### Failure Mode 4: Forced Tension Resolution (Week 3-4)

**Mechanism:** /review item 9 detects tensions and attempts resolution. Without human validating that a tension is *real* (contingent), agent tends to force consistency by eliminating one claim.

**Breaks:** Wiki becomes dogmatic. Loses conditional reasoning ("when to use LC vs RAG?") because the condition was eliminated.

**Evidence:** Tension-resolution protocol says "NEVER force artificial consistency" but agent judges what's "artificial" via self-evaluation (near-random per JudgeBench).

### Degradation Timeline

```
(⚠️ SPECULATIVE: these day ranges have NO empirical basis.
No study has measured KB degradation timelines. The ordering
of failure modes is our hypothesis, not observed data.)

Day 1-7:   Works well. Same phase benchmarks measure. (Honeymoon)
Day 7-14:  Semantic convergence starts. Invisible to automated metrics.
Day 14-21: Authority bias crystallizes errors. Tensions force-resolved.
Day 21-30: Wiki looks healthy (0 warnings) but /ask answers are generic
           and occasionally plausibly wrong. Degradation undetectable
           without external ground truth test.
```

### The Core Problem (⚠️ our framework, not from sources)

The system optimizes visible metrics (0 warnings, correct links, cited sources) while real quality erodes. We frame this as analogous to reward hacking — but no source has documented this specific phenomenon in knowledge bases.

### Mitigations

| Failure | Mitigation | Automatable? |
|---------|-----------|-------------|
| Semantic convergence | Style divergence metric: compare article text to raw/ source style | Yes — could be a /review check |
| Authority cascade | Human re-reads 2-3 random articles/week against raw/ | No — needs independent evaluator |
| Index bloat | Human quality gate on /ingest, or hard cap on articles per week | Partially — cap is automatic, judgment is not |
| Forced tension | Require human `> [!patch]` before any tension resolution is applied | Yes — rule change in /review |

### The Layer 3 Circularity Problem (⚠️ our analysis)

The /ask protocol treats raw/ verification (Layer 3) as grounded feedback. But this conflates two types of grounding:

- **Data grounding** (what raw/ provides): the original text is immutable and available
- **Interpretation grounding** (what raw/ does NOT provide): the same LLM that wrote the wiki reads raw/ and evaluates its own interpretation

In Reflexion's terms, grounded feedback means **executable tests** — unit tests that pass or fail independently of the agent's judgment. raw/ read by the same LLM is closer to self-reflection without tests (the 52% degradation case). The data is external; the interpretation is not.

A complementary mechanism (⚠️ nossa interpretação via [[curse-of-knowledge-llm-judge]]): **reference-anchoring bias**. ComplexEval (Li et al., 2025) shows that when LLM judges are given reference material as evaluation context, they anchor to that reference rather than evaluating independently — producing over-reliance rather than verification. Applied to Layer 3: the standard /ask sequence (wiki read in Layer 2 → raw/ read in Layer 3) primes the model with its own prior interpretation before it reads the source. The raw/ verification is structurally anchoring-inducing. This is a distinct failure mechanism from Reflexion's "self-reflection without test generation" — it explains not just *why* Layer 3 lacks independence but *how* the wiki actively contaminates the verification step.

This means Layer 3 is necessary but insufficient. It catches factual errors (wrong numbers, misattributed claims) but cannot catch interpretive errors (correct facts assembled into wrong conclusions). The /ask protocol should be understood as: Layer 3 provides data verification, not interpretation verification. See [[llm-as-judge]] for why the same model cannot reliably judge its own interpretive work (self-enhancement bias 16.1%).

### Architectural Insight

The blueprint's existing mechanisms (raw/ immutable, patches humanos, retrieval cético, confidence scoring) are correct — but they were designed as **guardrails with human in the loop**. Without human, the agent can satisfy all rules while circumventing their intent: verify raw/ and agree with itself, assign high confidence to own work, resolve tensions "following protocol."

The fix is not more rules — it's **external ground truth** (most reliable option). At least one verification channel must be independent of the LLM that maintains the wiki. ⚠️ Caveata pós-challenge: S2R (ACL 2025) propõe self-verification treinável que pode mitigar parcialmente — "only fix" é forte demais; "most reliable fix" é mais preciso. Concretely, this means either: (1) a different model for /review than for /ingest, (2) human spot-checks, or (3) executable validation (tests, type-checks, API calls that return ground truth).

⚠️ Caveata adicional (challenge 2026-04-05): "different model" não garante independência epistêmica se os modelos foram treinados em datasets sobrepostos — fenômeno documentado empiricamente em [[knowledge-collapse-llm]] (arXiv:2512.15011: multi-model mitiga collapse mas com ponto ótimo não-linear; independência decresce com overlap de training data). A opção mais robusta é (3) executable validation, que é estruturalmente independente de treinamento.

### Multiagent Debate as Middle Ground

Du et al. (2023) propose a fourth option: multiagent debate. Multiple LLM instances generate independent evaluations, read each other's responses, and debate across rounds to converge toward consensus. This significantly enhances factual validity and reduces hallucinations.

**Applied to /review:** instead of one LLM evaluating its own wiki, spawn 2-3 independent evaluations of each article, then debate disagreements. This mitigates self-enhancement bias without requiring a human — the "independent evaluator" is another instance of the same model, but with a different conversation history and evaluation context.

**Tension with single-agent:** Tim Kellogg documents Cognition's critique that multi-agent creates "fragile systems" with "dispersed decision-making." Multiagent debate fixes bias but adds coordination cost and context fragmentation. Neither single-agent nor multi-agent /review dominates — the choice depends on whether bias risk (single) or coordination fragility (multi) is the bigger threat for the specific article being reviewed.

## Níveis epistêmicos

### Descrição (verificado nas fontes)
- Self-enhancement bias up to 16.1% on Qwen2 (CALM)
- Self-reflection without test generation degrades to 52% on HumanEval (Reflexion)
- GPT-4o near random on hard evaluation tasks (JudgeBench)
- Random heuristic inclusion degrades after 40-60 items (ERL, on Gaia2)
- Model collapse: recursive self-consumption destroys distributional diversity (Shumailov et al., Nature)
- AI-revised Wikipedia content lowered RAG performance (Huang et al.)

### Interpretação (inferido, não declarado pelos autores)
- The 4 failure modes (semantic convergence, authority cascade, index bloat, forced tension) are our framework — no source describes these specific modes for knowledge bases
- "Layer 3 Circularity Problem" is our analysis applying Reflexion's test-generation finding to raw/ verification. Note: executable tests are stronger grounding than reading raw/
- The 16.1% figure is used as general indicator but is Qwen2-specific; Claude-3.5 is more resilient

### Especulação (proposto pela KB, sem evidência empírica)
- The ~30 day degradation timeline (Day 1-7 honeymoon, etc.) has NO empirical basis — day ranges are invented
- The 4 mitigation proposals are untested design recommendations
- "KB equivalent of reward hacking" is an analogy, not a demonstrated phenomenon
- "External ground truth" as the fix is our prescription, not from any source

### Gaps não resolvidos
- No empirical data on actual KB degradation rates exists
- Whether multiagent debate actually mitigates self-enhancement in KB review is untested
- The 40-60 ERL threshold is extrapolated from agent tasks to wiki management — domain transfer not validated
- **Failure Mode 5 — Judgment Aggregation Impossibility (multi-compiler):** Majority voting on individual claims cannot simultaneously satisfy (a) anonymity, (b) systematicity, and (c) logical consistency of collective judgments (List & Pettit 2002, Theorem 1). KB with multiple compilers voting claim-by-claim can be internally inconsistent even when each compiler is individually consistent — structural impossibility, not fixable by better prompting. Fonte: [[judgment-aggregation]].

## Conexões

- [[llm-as-judge]] — self-enhancement bias (16.1%) and authority bias are the root causes
- [[self-improving-agents]] — Reflexion without grounded feedback degrades to 52%; applies to autonomous /review
- [[tension-resolution]] — forced resolution is failure mode 4; protocol already says "never force" but enforcement requires human
- [[memory-consolidation]] — /review and /dream operate on the wiki; both susceptible to convergence
- [[kb-architecture-patterns]] — all 4 patterns assume human-in-the-loop for quality; none designed for full autonomy
- [[raptor-vs-flat-retrieval]] — ERL's 40-60 item selection limit applies to both semantic convergence detection and index scaling thresholds
- [[reflexion-weighted-knowledge-graphs]] — adaptive topology could mitigate failure mode 1 if edge weights incorporate external signal
- contradicts: [[judgment-aggregation]] ON "claim-level voting in multi-compiler KB → structural logical inconsistency (Theorem 1)"
- emerge-para: [[autoresearch-reliability-triad]] ON "Layer 3 Circularity Problem como um dos três mecanismos de falha convergentes"
- [[curse-of-knowledge-llm-judge]] — reference-anchoring bias: mecanismo complementar ao Reflexion framing para Layer 3 Circularity
- [[knowledge-collapse-llm]] — Stage B (fluency intact, facts degrading) empiricamente confirma FM1 "metrics stay green"


## Fontes

- [CALM](../../raw/papers/calm-llm-judge-biases.md) — self-enhancement 16.1%, authority bias, circular validation risk
- [JudgeBench](../../raw/papers/judgebench-evaluating-llm-judges.md) — self-assessment near random on hard tasks, reliability inflated by benchmark difficulty
- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — without independent grounding, self-reflection degrades to 52%
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — random inclusion degrades after 40-60; indiscriminate growth is counterproductive
- [Model Collapse](../../raw/papers/model-collapse-recursive-training.md) — recursive self-consumption destroys diversity (Nature 2024); mixture of real+synthetic data prevents collapse
- [Wikipedia Risks](../../raw/papers/wikipedia-era-llms-risks.md) — AI-revised content lowers RAG performance; stylistic homogenization detected empirically
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — Cognitive Tunneling: hub suppression as analogy for convergence
- [LLMs as KBs Reliability](../../raw/papers/llms-reliability-as-knowledge-bases.md) — 26 models tested: larger models more consistently wrong (r=0.78-0.81), cross-paper synthesis = "unseen knowledge" where factuality degrades most
