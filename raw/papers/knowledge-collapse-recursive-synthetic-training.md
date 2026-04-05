---
title: "Knowledge Collapse in LLMs: When Fluency Survives but Facts Fail under Recursive Synthetic Training"
authors:
  - Figarri Keisha
  - Zekun Wu
  - Ze Wang
  - Adriano Koshiyama
  - Philip Treleaven
year: 2025
venue: arXiv
arxiv_id: "2509.04796"
url: https://arxiv.org/abs/2509.04796
submitted: 2025-09-05
type: paper
quality: primary
---

## Abstract

This paper defines "knowledge collapse" as a three-stage phenomenon where factual accuracy deteriorates while surface fluency persists, creating "confidently wrong" outputs during recursive synthetic training. Through controlled experiments, researchers demonstrate that collapse trajectory depends critically on instruction format, distinguishing this from traditional model collapse through its conditional, prompt-dependent nature. Domain-specific synthetic training achieves substantial improvements in collapse resistance while maintaining computational efficiency.

## Three-Stage Knowledge Collapse Framework

**Stage A — Knowledge Preservation:** Models maintain reliable factual accuracy with high instruction adherence. Normal operation.

**Stage B — Knowledge Collapse (critical):** Factual accuracy deteriorates while task format adherence persists. The "dangerous competence valley" — models produce well-formatted but factually incorrect responses. Metrics (fluency, format compliance) stay green while factual accuracy erodes silently.

**Stage C — Instruction-following Collapse:** Complete breakdown where accuracy approaches random baselines (≤0.28) and outputs become incoherent. Collapse becomes externally visible.

Stage B is the critical danger zone: degradation is invisible to surface-level quality metrics.

## Methodology

- **Model:** GEMMA 3 1B IT
- **Training corpus:** WikiText-2 (8,000 64-token prompts)
- **Evaluation:** Five MMLU subjects (100 Q&A each)
- **Training intensity:** 0.5 epochs per generation (light-touch updates)
- **Synthetic fractions tested:** α ∈ {0.25, 0.50, 1.0}
- **Instruction formats tested:** zero-shot, few-shot, short-answer

## Key Findings

### Synthetic Ratio Effects on Collapse Speed

- **25% synthetic:** Prolonged Stage A stability; Stage B transition only at later generations
- **50% synthetic:** Quicker Stage A-to-B transition at mid-generation
- **100% synthetic:** Rapid Stage A-to-B transition in early generations, progressing quickly to Stage C
- 25% synthetic ratio demonstrated a U-shaped perplexity trajectory, indicating real data's regularization effect

### Instruction Format Mediates Collapse

Two-way ANOVA revealed significant instruction×generation interaction (F=12.67, p<0.001), confirming that "collapse trajectory and timing are mediated by instruction format rather than occurring uniformly."

At 50% synthetic ratio:
- **Short-answer prompts:** Remain above random baseline until Generation 8
- **Zero-shot prompts:** Intermediate degradation pattern
- **Few-shot prompts:** Collapse rapidly by Generation 6

### Domain-Specific Training: 15× Improvement in Collapse Resistance

Domain-aligned training (World Religions corpus) vs. general training:

| Metric | Domain-specific | General |
|---|---|---|
| Accuracy decay rate (per generation) | −0.00054 | −0.00837 |
| Perplexity growth | 35 | 170 |
| Entropy (start → end) | 3.5 → 3.3 (stable) | 4.2 → 2.5 (narrowing) |

Statistical significance: p<0.001 with significant interaction effects. The 15× improvement in decay rate is the headline result.

Domain-specific models maintained moderate greedy rates without dominant-option bias; general models showed vocabulary narrowing.

### Entailment Illusion

At 100% synthetic ratio, entailment scores showed spurious late increases — the model appears to maintain semantic coherence (high entailment) while factual accuracy has already collapsed. This is a specific failure mode of automated quality metrics.

## Distinction from Shumailov et al. (Nature 2024) Model Collapse

Shumailov et al. documented that models trained recursively on synthetic outputs "gradually focus on high-frequency patterns while omitting low-probability tokens" — a statistical tail truncation effect that is prompt-agnostic.

Knowledge collapse is **prompt-dependent and conditional**: collapse trajectory and timing depend on instruction format, allowing models to maintain task competence during factual erosion (Stage B) rather than experiencing uniform distributional drift. The two phenomena can co-occur but are mechanistically distinct.

## Practical Implications

- Keeping training data domain-specific (rather than broad/general) substantially delays collapse onset
- Fluency and format compliance metrics are insufficient for detecting Stage B collapse — task-specific factual metrics are required
- Real data mixed with synthetic (even at 25%) acts as a regularizer that delays collapse
- Framework enables reproducible assessment of factual deterioration across different language models
