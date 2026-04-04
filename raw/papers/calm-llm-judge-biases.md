---
source: https://arxiv.org/abs/2410.02736
authors: Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V. Chawla, Xiangliang Zhang
date: 2024-10-03
type: paper
arxiv: "2410.02736"
github: https://github.com/Y0oMu/LLM-Judge-Bias-Dataset
---

# Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge

## Abstract

Introduces CALM framework for systematically identifying and quantifying 12 bias types in LLM evaluators. Evaluated 6 popular LLMs. While some demonstrate notable fairness, significant room for improvement remains. Automates bias detection via "attack-and-detect" perturbation approach.

## CALM Framework

4 components:
1. Comprehensive bias categories (12 types)
2. Diverse datasets (fact-related, refinement-aware, alignment)
3. Specialized metrics: Robustness Rate (RR) and Consistency Rate (CR)
4. Automated perturbation: inject biases without altering semantic meaning

## 12 Bias Types

| Bias | Description |
|------|-------------|
| Position | Favors answers at certain positions |
| Verbosity | Prefers longer responses regardless of quality |
| Compassion-Fade | Responds differently to known vs anonymized model names |
| Bandwagon | Influenced by majority opinion statements |
| Distraction | Distracted by irrelevant details |
| Fallacy-Oversight | Overlooks logical errors |
| Authority | Favors answers with citations (even fake) |
| Sentiment | Prefers certain emotional tones |
| Diversity | Bias toward specific demographic groups |
| Chain-of-Thought | Performance varies with explicit reasoning prompts |
| Self-Enhancement | Favors own outputs |
| Refinement-Aware | Scores differently when aware of revision history |

## Most Severe Biases

- **Position bias**: robustness drops below 0.5 with 3+ answer options
- **Self-enhancement**: up to 16.1% error rate (Qwen2) — models prefer own outputs
- **Fear sentiment**: most impactful emotional tone on accuracy
- **Alignment tasks**: more vulnerable than fact-related (smaller quality gaps = more bias susceptibility)

## Results Per Model

| Model | Fact-Related RR | Alignment RR | Best At |
|-------|----------------|--------------|---------|
| GPT-4o | 0.977 | 0.776 | Fact robustness |
| Claude-3.5 | 0.952 | 0.832 | Overall resilience |
| GPT-4-Turbo | 0.915 | 0.818 | Alignment tasks |
| ChatGPT | 0.900 | 0.566 | — (worst alignment) |

Claude-3.5 shows greatest overall resilience. Advanced models don't automatically resist bias better.

## Key Insights

- Self-enhancement bias: using same model for generation AND evaluation = unacceptable
- Chain-of-Thought improves accuracy 0.7-7% depending on model
- Biases reflect inherited human cognitive patterns — "LLMs cannot truly achieve absolute fairness"
- Position bias worsens with more options

## Relevance to Knowledge Bases

Critical for our architecture: the LLM that writes wiki articles (/ingest) should not be the sole judge of their quality (/review). Self-enhancement bias means it will prefer its own articles. Mitigations: (1) raw/ verification (Layer 3 in /ask), (2) human patches as external signal, (3) potentially using a different model for /review than for /ingest. Authority bias is relevant too: our articles cite sources, and the LLM may over-trust cited claims without verifying. Principle 9 ("retrieval is skeptical") directly addresses this.
