---
source: https://arxiv.org/abs/2412.05579
authors: Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yujia Zhou, Qingyao Ai, Ziyi Ye, Yiqun Liu
date: 2024-12-07
type: paper
arxiv: "2412.05579"
---

# LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods

## Abstract

Survey examining LLMs as evaluators from five angles: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.

## Five Perspectives

### 1. Functionality — Why use LLM judges
- Performance evaluation (response quality, model benchmarking)
- Model enhancement (reward modeling, verification during inference, iterative refinement)
- Data construction (annotation, synthetic data generation)

### 2. Methodology — How to construct
**Evaluation types:**

| Type | Description | Use Cases |
|------|-------------|-----------|
| Pointwise | Assess items independently | Summarization quality |
| Pairwise | Compare two candidates | Preference ranking, A/B testing |
| Listwise | Rank multiple items | Search results, document retrieval |

**Systems:** Single-LLM (prompt-based, tuning-based, post-processing), Multi-LLM (cooperation, competition, ensemble), Human-AI collaboration.

### 3. Applications
General NLP, multimodal, medical, legal, financial, education, information retrieval, code generation.

### 4. Meta-evaluation — How to assess judges
Benchmarks: HumanEval, MT-Bench, AlpacaEval, Chatbot Arena. Metrics: accuracy, Pearson, Spearman, Kendall's Tau, Cohen's Kappa.

### 5. Limitations

**Bias categories:**

| Category | Examples |
|----------|---------|
| Presentation-Related | Position bias, verbosity bias |
| Social-Related | Authority bias, bandwagon effect |
| Content-Related | Sentiment bias, token bias, contextual bias |
| Cognitive-Related | Overconfidence, self-enhancement, distraction |

Critical: "LLM judges are often influenced by the prompt template, which can lead to biased or inconsistent assessments."

## Key Finding

Despite advantages, LLMs-as-judges remain unreliable for specialized tasks requiring logical reasoning or deep domain knowledge, particularly in professional contexts like academic peer review.

## Relevance to Knowledge Bases

Our /ask confidence scoring (high/medium/low) is a simple LLM-as-judge system. This survey provides the theoretical framework for making it more robust: use pairwise comparison (wiki vs raw/ for verification), be aware of self-enhancement bias (the LLM preferring its own wiki articles), and implement meta-evaluation (periodically test /ask answers against known-good questions).
