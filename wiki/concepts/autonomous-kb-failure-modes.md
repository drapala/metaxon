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
created: 2026-04-03
updated: 2026-04-03
tags: [meta-kb, failure-analysis, safety, original-insight]
confidence: high
resolved_patches: []
---

## Resumo

An LLM-operated KB without human intervention degrades silently over ~30 days through 4 failure modes: semantic convergence (articles homogenize), authority bias cascade (errors crystallize via circular validation), index bloat (growth without quality gate), and forced tension resolution (nuance eliminated). The system appears healthy on all automated metrics while quality erodes — the KB equivalent of reward hacking.

## Conteúdo

### Failure Mode 1: Semantic Convergence (Week 1-2)

**Mechanism:** Self-enhancement bias (CALM: 16.1% error) + unsupervised /review = LLM rewrites articles in its preferred style each review cycle. "Convert vague to precise" and "deduplicate" are opportunities to homogenize.

**Why invisible:** Wiki gets *more consistent*, not less. All /review metrics stay green. Problem is qualitative: wiki loses perspective diversity that justifies having multiple sources.

**Evidence:** ERL shows random heuristic inclusion degrades after 40-60 items. When all articles use same formulations, _index.md loses discriminative power.

**Breaks:** /ask on subtle topics returns generic answers. Distinctions from original sources (Karpathy writes differently than an academic paper) are lost.

### Failure Mode 2: Authority Bias Cascade (Week 2-3)

**Mechanism:** Authority bias (CALM) makes LLM trust cited claims more. Wiki articles cite raw/. When /ask verifies wiki against raw/ (Layer 3), it tends to *confirm* because raw/ was the original source — circular validation loop.

**Compounding:** Without human reading raw/ with fresh eyes, /ingest misinterpretations crystallize. JudgeBench: self-assessment on difficult problems is near-random. If original interpretation was plausibly wrong, LLM "verifies" and agrees with itself.

**Evidence:** Reflexion ablation — self-reflection without *independent* grounded feedback degrades to 52%. raw/ is grounded but read by the same LLM. Ground truth needs independent evaluator.

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
Day 1-7:   Works well. Same phase benchmarks measure. (Honeymoon)
Day 7-14:  Semantic convergence starts. Invisible to automated metrics.
Day 14-21: Authority bias crystallizes errors. Tensions force-resolved.
Day 21-30: Wiki looks healthy (0 warnings) but /ask answers are generic
           and occasionally plausibly wrong. Degradation undetectable
           without external ground truth test.
```

### The Core Problem

The system optimizes visible metrics (0 warnings, correct links, cited sources) while real quality erodes. This is the KB equivalent of reward hacking documented by CARMO.

### Mitigations

| Failure | Mitigation | Automatable? |
|---------|-----------|-------------|
| Semantic convergence | Style divergence metric: compare article text to raw/ source style | Yes — could be a /review check |
| Authority cascade | Human re-reads 2-3 random articles/week against raw/ | No — needs independent evaluator |
| Index bloat | Human quality gate on /ingest, or hard cap on articles per week | Partially — cap is automatic, judgment is not |
| Forced tension | Require human `> [!patch]` before any tension resolution is applied | Yes — rule change in /review |

### Architectural Insight

The blueprint's existing mechanisms (raw/ immutable, patches humanos, retrieval cético, confidence scoring) are correct — but they were designed as **guardrails with human in the loop**. Without human, the agent can satisfy all rules while circumventing their intent: verify raw/ and agree with itself, assign high confidence to own work, resolve tensions "following protocol."

The fix is not more rules — it's **external ground truth**. At least one verification channel must be independent of the LLM that maintains the wiki.

## Conexões

- [[llm-as-judge]] — self-enhancement bias (16.1%) and authority bias are the root causes
- [[self-improving-agents]] — Reflexion without grounded feedback degrades to 52%; applies to autonomous /review
- [[tension-resolution]] — forced resolution is failure mode 4; protocol already says "never force" but enforcement requires human
- [[memory-consolidation]] — /review and /dream operate on the wiki; both susceptible to convergence
- [[kb-architecture-patterns]] — all 4 patterns assume human-in-the-loop for quality; none designed for full autonomy
- [[reflexion-weighted-knowledge-graphs]] — adaptive topology could mitigate failure mode 1 if edge weights incorporate external signal

## Fontes

- [CALM](../../raw/papers/calm-llm-judge-biases.md) — self-enhancement 16.1%, authority bias, circular validation risk
- [JudgeBench](../../raw/papers/judgebench-evaluating-llm-judges.md) — self-assessment near random on hard tasks, reliability inflated by benchmark difficulty
- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — without independent grounding, self-reflection degrades to 52%
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — random inclusion degrades after 40-60; indiscriminate growth is counterproductive
- [Synapse](../../raw/papers/synapse-episodic-semantic-memory.md) — Cognitive Tunneling: hub suppression as analogy for convergence
