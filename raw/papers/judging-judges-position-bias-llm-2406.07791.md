---
source: https://arxiv.org/abs/2406.07791
authors: Lin Shi, Chiyu Ma, Wenhua Liang, Xingjian Diao, Weicheng Ma, Soroush Vosoughi
date: 2024-06-12
type: paper
quality: primary
stance: confirming
venue: AACL-IJCNLP 2025
---

# Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge

## Abstract

LLM-as-a-Judge has emerged as a promising alternative to human evaluators across various tasks. Position bias — the tendency to favor solutions based on their position in the prompt — compromises its reliability. Systematic study evaluating 15 LLM judges across MTBench and DevBench benchmarks (22 tasks, ~40 solution-generating models, 150,000+ evaluation instances).

## Three Evaluation Metrics

### Repetition Stability (RS)
"Percentage of most frequent selections across multiple trials." Ensures judgments are not random noise. Near-perfect capable judges: RS > 0.95.

### Position Consistency (PC)
Ratio of consistent evaluations when answer order is permuted. Higher = less position bias.
- Claude-3.5-Sonnet (MTBench): PC = 0.82
- GPT-4 (MTBench): PC = 0.82
- Claude-3-Haiku: PC = 0.57
- Gemini-1.0-pro: low PC

### Preference Fairness (PF)
Min-max scaled from -1 to +1. -1 = always prefers first position (primacy bias), +1 = always prefers last (recency bias), 0 = perfect fairness.
- Claude-3.5-Sonnet: PF = 0.01 (near-perfect fairness)

## Intervention Protocol (Level 2 Evidence)

Position-swapping protocol: identical prompts with candidate answers in permuted order. This is a direct do-operator intervention: do(position=A_first) vs do(position=B_first). By holding all content constant and varying only position, the study isolates position as a causal variable — not a correlate.

**Key finding:** position bias is systematic (non-random). "Capable judges demonstrated near-perfect Repetition Stability scores over 0.95, confirming bias stems from systematic patterns rather than randomness."

## Sources of Bias: Three-Level Framework

### Judge-Level Factors
Capability and training of the judge model determines baseline position consistency. More capable models show higher PC and RS.

### Candidate-Level Factors (Quality Gap)
**Parabolic relationship between quality gap and position consistency:**
- Large quality gap → high PC (judge correctly identifies better answer regardless of position)
- Small quality gap (similar-quality candidates) → maximum position bias (judge defaults to position heuristic)

Quality gap is the strongest predictor of consistent judging. "Overall win rate compared to baseline expectations" used to measure this.

### Task-Level Factors
Position bias varies substantially across tasks and domains. Prompt component length has **weak** influence — counter-intuitive: longer prompts don't substantially increase positional effects.

## Judge Rankings (MTBench)

**Most reliable (highest PC):**
- Claude-3.5-Sonnet: PC = 0.82, PF = 0.01
- GPT-4: PC = 0.82

**Most biased (lowest PC):**
- Claude-3-Haiku: PC = 0.57
- Gemini-1.0-pro: low consistency and high preference variability

## Methodological Details

- 15 judge models evaluated
- Benchmarks: MTBench, DevBench
- 22 tasks, ~40 solution-generating models
- 150,000+ evaluation instances
- Both pairwise and listwise comparisons
- Three metrics applied simultaneously (RS, PC, PF)
