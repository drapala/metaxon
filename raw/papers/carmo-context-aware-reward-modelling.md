---
source: https://arxiv.org/abs/2410.21545
authors: Taneesh Gupta, Shivam Shandilya, Xuchao Zhang, Rahul Madhavan, Supriyo Ghosh, Chetan Bansal, Huaxiu Yao, Saravan Rajmohan
date: 2024-10-28
type: paper
arxiv: "2410.21545"
---

# CARMO / SALC: Dynamic Criteria Generation for Context-Aware Reward Modelling

## Abstract

Addresses reward hacking where models exploit superficial features (list-generation, unnecessary length). SALC generates dynamic, context-relevant evaluation criteria before producing scores. Unlike static rubrics, uses LLMs to adaptively create criteria per query. +2.1% on Reward Bench zero-shot. Alignment training with SALC preferences: +22.5% and +21.1% on Mistral-Base 7B.

## Architecture (3 Stages)

### 1. Autonomous Criteria Generation
Model generates evaluation criteria based on instruction, reference answer, and response — no predefined human rubrics.

### 2. Response Assessment
Using generated criteria, model evaluates with detailed feedback and 1-5 scores.

### 3. Knowledge Distillation
Fine-tuned 7B/13B models using GPT-4-generated criteria. 13B model outperforms GPT-4o on correlation metrics despite 13× fewer parameters.

## Key Results

### Fine-Tuned Model Performance
| Model | Pearson | Kendall-Tau | Spearman |
|-------|---------|-------------|----------|
| FT-Judge-13b | **0.924** | **0.807** | **0.871** |
| GPT-4-Turbo | 0.910 | 0.791 | 0.856 |
| GPT-4o | 0.896 | 0.789 | 0.858 |

### DPO Alignment Gains
| Model | LC-WR Improvement |
|-------|-------------------|
| Mistral-7b | +12.58% vs Default |
| Phi-3-Mini | +3.41% vs Default |
| Phi-2 | +9.69% vs Default |

## Static vs Dynamic Criteria

Static rubrics (Flask, Prometheus) use predefined skill sets — limited adaptability. SALC dynamically adjusts by examining task requirements, reference quality, and context nuances. Example: for a polar bear climate question, static checks surface accuracy; SALC generates criteria about habitat loss specifics and survival impacts.

## Relevance to Knowledge Bases

SALC's dynamic criteria generation directly applies to our /ask quality evaluation. Instead of fixed validation criteria (the 5-point checklist in the blueprint), we could generate context-specific criteria per query. Also relevant for /review: dynamically generate assessment criteria per article instead of applying uniform heuristics.
