---
title: "Curation Anti-Bias"
sources:
  - path: raw/papers/calm-llm-judge-biases.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/knowledge-conflicts-llms-survey.md
    type: paper
    quality: primary
  - path: raw/papers/lm-know-what-they-know.md
    type: paper
    quality: primary
  - path: raw/papers/multiagent-debate-factuality.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [meta-kb, quality, bias, curation]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
---

## Resumo

Curation bias in an LLM KB operates at 3 layers: selection (what enters raw/), interpretation (what /ingest extracts), and evaluation (how quality is judged). Five concrete improvements address these: adversarial source quota, split confidence scoring, style preservation checks, ERL-based ingest thresholds, and multiagent spot-checks. Key principle: the problem isn't having bias — it's having invisible, cumulative bias.

## Conteúdo

### 3 Layers of Bias

**Layer 1 — Selection Bias (what enters raw/)**

All sources chosen in one session, by one person, from one network cluster. The corpus reflects:
- Recency bias: almost everything 2023-2026, no foundational work
- Network bias: sources from the same social cluster (Karpathy → Elvis → Kepano)
- Confirmation bias: papers that validate the chosen architecture. No paper argues *against* LLM KBs.

**Layer 2 — Interpretation Bias (what /ingest extracts)**

"LMs Know What They Know" confirms: LLM self-assessment is reliable for factual claims but degrades on interpretive synthesis. Knowledge Conflicts survey: LLMs show "strong confirmation bias toward parametric knowledge" — when /ingest has 15 articles about sophisticated memory architectures, it reads the 16th paper with confirming lenses.

**Layer 3 — Evaluation Bias (how we judge quality)**

Self-enhancement bias (CALM: 16.1%) means the LLM assigns higher confidence to its own work. ERL shows indiscriminate inclusion degrades after 40-60 items. Without threshold, the wiki grows without quality gate.

### 5 Improvements

**1. Adversarial Source Quota**
Every source gets `stance: confirming | challenging | neutral` in frontmatter. After 5 consecutive confirming sources, /ingest alerts the user to seek a challenging source. Breaks confirmation bias via counting, not judgment.

**2. Split Confidence Scoring**
Replace single `confidence` with two independent signals:
- `source_quality: high|medium|low` — objective, based on source type+quality count (reliable)
- `interpretation_confidence: medium|medium|low` — subjective, LLM self-assessment (unreliable on hard claims)

When they diverge (source_quality:high but interpretation_confidence:medium), flag for human review.

**3. Style Preservation Check**
In /review, compare article style to raw/ source style. If a wiki article about an informal tweet reads like an academic paper, semantic convergence has occurred. Flag articles whose formulations don't appear in any cited raw/ source.

**4. ERL-Based Ingest Threshold**
When wiki exceeds 40 articles, require novelty score for new articles (concept not covered, or contradicts existing claim). When wiki exceeds 80, require sub-indices before growing further.

**5. Multiagent Spot-Check**
For 2-3 random articles per /review, generate 2 independent evaluations (different system prompts: "critical reviewer" vs "supportive reviewer"). Divergence between them surfaces issues a single evaluation hides.

## Interpretação

Ver seções marcadas com (⚠️) no Conteúdo acima — conteúdo interpretativo está inline por razões de coesão narrativa.

## Conexões

- [[autonomous-kb-failure-modes]] — the 4 failure modes that these improvements address
- [[llm-as-judge]] — self-enhancement bias and calibration limits inform improvements 2 and 5
- [[self-improving-agents]] — ERL's selective retrieval threshold informs improvement 4
- [[tension-resolution]] — adversarial sources create productive tensions (improvement 1)
- [[kb-architecture-patterns]] — Pattern 3 (Human-in-the-Loop) is the ultimate bias check

## Fontes

- [CALM](../../raw/papers/calm-llm-judge-biases.md) — self-enhancement 16.1%, authority bias quantified
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — random inclusion degrades after 40-60, selective retrieval critical
- [Knowledge Conflicts](../../raw/papers/knowledge-conflicts-llms-survey.md) — confirmation bias toward parametric knowledge, GPT-4 13% inconsistency
- [LMs Know What They Know](../../raw/papers/lm-know-what-they-know.md) — "mostly" calibrated, degrades on hard/unfamiliar tasks
- [Multiagent Debate](../../raw/papers/multiagent-debate-factuality.md) — independent evaluations + debate reduce hallucinations and bias
