---
title: "Knowledge Collapse in LLMs"
sources:
  - path: raw/papers/knowledge-collapse-recursive-synthetic-training.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-05
updated: 2026-04-05
tags: [model-collapse, knowledge-base, degradation, synthetic-data]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
provenance: source
---

## Resumo

"Knowledge collapse" is a three-stage degradation process in LLMs trained recursively on synthetic data: factual accuracy erodes silently while surface fluency and format compliance remain intact, producing outputs that are confidently wrong before any metric turns red. Keisha et al. (2025) distinguish this from Shumailov et al.'s model collapse — it is prompt-dependent and conditional rather than a uniform distributional drift. Domain-specific training delays collapse by 15× compared to general training.

## Conteúdo

### The Three-Stage Framework

**Stage A — Knowledge Preservation:** Models maintain reliable factual accuracy and instruction adherence. Normal operation.

**Stage B — Knowledge Collapse (silent):** Factual accuracy deteriorates while task format adherence persists. Models produce well-formatted, fluent, coherent responses that are factually incorrect. All surface-level quality metrics (fluency, format compliance, entailment scores) remain green. This is the critical danger zone.

**Stage C — Instruction-following Collapse:** Complete breakdown. Accuracy approaches random baselines (≤0.28), outputs become incoherent. Collapse becomes externally visible for the first time.

The Stage B → Stage C transition is what surfaces in incident reports. Stage A → Stage B is invisible.

### Quantitative Results

**Synthetic ratio effects on collapse speed:**
- 25% synthetic: prolonged Stage A; U-shaped perplexity (real data acts as regularizer)
- 50% synthetic: mid-generation transition to Stage B
- 100% synthetic: rapid Stage A→B transition, progressing to Stage C

**Instruction format mediates collapse timing** (50% synthetic):
- Short-answer prompts: stay above random baseline until Generation 8
- Zero-shot prompts: intermediate degradation
- Few-shot prompts: collapse by Generation 6
- Two-way ANOVA: F=12.67, p<0.001 — "collapse trajectory and timing are mediated by instruction format rather than occurring uniformly"

**Domain-specific training (15× improvement):**

| Metric | Domain-specific | General |
|---|---|---|
| Accuracy decay rate (per generation) | −0.00054 | −0.00837 |
| Perplexity growth | 35 | 170 |
| Entropy trajectory | 3.5 → 3.3 (stable) | 4.2 → 2.5 (narrowing) |

### Entailment Illusion

At 100% synthetic ratio, entailment scores showed spurious late increases — the model appears to maintain semantic coherence while factual accuracy has already collapsed. Automated semantic quality metrics can actively mislead during Stage B.

### Experimental Setup

- Model: GEMMA 3 1B IT
- Training corpus: WikiText-2 (8,000 64-token prompts); evaluation: 5 MMLU subjects (100 Q&A each)
- Training intensity: 0.5 epochs per generation (light-touch updates)
- Domain-specific mitigation corpus: World Religions

### Distinction from Shumailov et al. (Nature 2024)

Shumailov et al. documented statistical tail truncation: models trained recursively on synthetic outputs gradually focus on high-frequency patterns, omitting low-probability tokens — a prompt-agnostic distributional drift.

Knowledge collapse is **prompt-dependent and conditional**: the same model can exhibit Stage B on zero-shot prompts while still performing adequately on short-answer prompts. This conditionality is what makes it harder to detect and what produces the "confidently wrong" failure mode.

Both phenomena can co-occur in a KB setting; they are mechanistically distinct.

## Interpretação

### Operacionalização do "Metrics Stay Green" Problem

(⚠️ nossa interpretação) Stage B is the empirical instantiation of the central concern in [[autonomous-kb-failure-modes]] FM1 (Semantic Convergence): "the system appears healthy on all automated metrics while quality erodes." Keisha et al. provide a specific, reproducible mechanism for how this happens — fluency and format compliance dissociate from factual accuracy under recursive synthetic training — and quantify the window before Stage C.

The FM1 mitigation in autonomous-kb-failure-modes is: "/review must always re-read raw/ (real data), never operate only on wiki/ (synthetic data)." Keisha et al. provide a causal explanation for why this works: mixing real data with synthetic acts as a regularizer that delays collapse (U-shaped perplexity at 25% synthetic). The recommendation is grounded, not just precautionary.

### Domain-Specificity of raw/ as Structural Protection

(⚠️ nossa interpretação) The 15× collapse-resistance improvement from domain-specific training maps directly to a design choice in this KB: raw/ accumulates domain-specific sources (AI/ML/agentic systems) rather than broad general-purpose text. If the KB ever becomes a training signal for a downstream LLM — or if /review cycles increasingly rely on wiki/ rather than raw/ — the domain-specific composition of raw/ provides structural delay before Stage B onset. The implication is: resist scope creep in raw/ not only for coherence reasons, but as a collapse-resistance mechanism.

### Instruction Format as a Detection Lever

(⚠️ nossa interpretação) The instruction-format sensitivity finding (few-shot collapses faster than short-answer) has a practical implication for [[autonomous-kb-failure-modes]]: if a KB uses a fixed evaluation format (e.g., always few-shot), it will detect Stage C faster but will miss Stage B entirely on other prompt types. A robust health check should probe with multiple instruction formats. This is a gap in the current KB's /challenge and /lint-epistemic commands.

### Relation to Self-Improving Agents

(⚠️ nossa interpretação) [[self-improving-agents]] describes the compounding risk when an agent uses its own outputs as training signal. Knowledge collapse provides the degradation timeline: Stage B emerges before any self-improvement loop would flag a problem, meaning the agent continues to "improve" (by its own metrics) while factual grounding deteriorates. The 100% synthetic ratio scenario maps directly to a self-improving agent with no grounded feedback — Stage C can arrive within a handful of training generations.

## Conexões

- [[autonomous-kb-failure-modes]] — Stage B operationalizes FM1's "metrics stay green while quality erodes"; domain-specificity of raw/ is a structural mitigation
- [[self-improving-agents]] — 100% synthetic training ≈ agent with no grounded feedback; Stage C timeline applies
- [[autoresearch-reliability-triad]] — fluency/format dissociating from factual accuracy is a reliability failure mode
- [[multi-agent-orchestration]] — instruction-format sensitivity means multi-agent pipelines using different prompt styles will collapse at different rates

## Fontes

- [Keisha et al. 2025](../../raw/papers/knowledge-collapse-recursive-synthetic-training.md) — defines 3-stage knowledge collapse, quantifies 15× domain-specific mitigation, distinguishes from Shumailov et al. model collapse
