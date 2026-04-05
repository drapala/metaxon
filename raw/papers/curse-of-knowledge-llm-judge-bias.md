---
title: "Curse of Knowledge: When Complex Evaluation Context Benefits yet Biases LLM Judges"
authors:
  - Weiyuan Li
  - Xintao Wang
  - Siyu Yuan
  - Rui Xu
  - Jiangjie Chen
  - Qingqing Dong
  - Yanghua Xiao
  - Deqing Yang
year: 2025
venue: EMNLP 2025 Findings
arxiv: "2509.03419"
version: v2 (October 2025)
type: paper
quality: primary
---

## Abstract

LLM-as-judge systems commonly use auxiliary information — reference answers and evaluation rubrics — to improve judgment quality on complex tasks. This paper introduces ComplexEval, a benchmark that systematically exposes and quantifies Auxiliary Information Induced Biases (AIIBs). Findings demonstrate that all tested models show significant susceptibility to these biases, with bias magnitude increasing alongside task complexity. Large Reasoning Models (LRMs) display unexpected vulnerability: despite superior baseline accuracy, they are more susceptible to AIIBs than general models. The results challenge the prevailing assumption that richer evaluation contexts uniformly improve LLM-as-judge reliability.

## Key Findings

### ComplexEval Benchmark

Two-tier benchmark designed to expose biases introduced by auxiliary information:

- **ComplexEval-Basic**: 1,056 samples across 12 domains using comprehensive adversarial attacks
- **ComplexEval-Advanced**: 400 samples across 3 challenging domains (mathematics, creative writing, role-playing) using targeted attacks

### Five Identified Bias Types (Auxiliary Information Induced Biases)

**Reference-Based Biases:**

1. **Format Bias**: Models overvalue superficial stylistic alignment with reference answers rather than content quality. Particularly strong in mathematics domain.

2. **Solution Fixation Bias**: Models penalize semantically valid alternative solutions that diverge from the provided reference solution. QwQ-32B reaches 45%+ Attack Success Rate (ASR) on this bias type.

3. **Stereotype Amplification Bias**: Reference materials trigger latent stereotypes in the model, amplifying inherent biases.

**Rubric-Based Biases:**

4. **Criteria Loophole Bias**: Models neglect evaluation dimensions absent from rubrics, limiting their inherent evaluation capabilities.

5. **Criteria Entanglement Bias**: Models assign similar scores across rubric dimensions despite explicit weighting differences — a "halo effect." Particularly high in creative writing (e.g., Qwen2.5-32B: 29% ASR).

### Quantitative Results

**On original (non-attacked) samples with auxiliary information:**
- Reference answers improved accuracy: DeepSeek-V3 +4.74%
- Rubrics showed mixed effects: range -0.25% to +3.28%

**On adversarially attacked samples:**
- General models: ~1% accuracy decline despite auxiliary information
- DeepSeek-V3: -1.66% with reference-based attacks
- DeepSeek-R1 (reasoning model): -4.50% — more than 4x the decline of general models

**Attention Limit Phenomenon:**
In role-playing evaluation with 20 distinct issues, models showed a hard ceiling of ~15 detected issues regardless of actual issue count, suggesting fundamental processing constraints in multi-dimensional evaluation.

### Models Tested

| General Model | Reasoning Counterpart |
|---------------|----------------------|
| Qwen2.5-32B   | QwQ-32B              |
| DeepSeek-V3   | DeepSeek-R1          |
| GPT-4o-mini   | o4-mini              |

### The "Curse of Knowledge" Paradox

The core finding: auxiliary information (reference answers, rubrics) simultaneously:
1. **Benefits** evaluation accuracy on clean samples (baseline improvement)
2. **Biases** models by creating exploitable anchoring toward the provided reference

When a reference answer is perturbed or wrong, models anchor to it rather than evaluating independently. Richer context creates larger attack surfaces. Reasoning models amplify this effect — their extended chain-of-thought may give them more opportunity to rationalize alignment with the reference.

### Implications for LLM-as-Judge Systems

- Reward modeling pipelines that rely on reference answers are systematically biased
- Automated evaluation systems using rubrics are vulnerable to criteria loophole exploitation
- The assumption that "more context = better evaluation" is empirically refuted
- Bias magnitude scales with task complexity — simpler tasks are safer for automated evaluation

## Broader Context

The paper connects to two bodies of work:
1. **LLM evaluation reliability** (biased judges in RLHF, reward hacking)
2. **Cognitive bias in human experts** — the "curse of knowledge" in psychology refers to experts being unable to reason from ignorance; the paper applies this to LLMs: having the reference answer makes the model unable to evaluate independently

The five bias types are framed as a taxonomy of failure modes for any system where an LLM evaluates with auxiliary context — including RAG-based QA evaluation, automated grading, and self-verification loops.
