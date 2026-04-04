---
source: https://arxiv.org/abs/2603.24639
authors: Marc-Antoine Allard, Arnaud Teinturier, Victor Xing, Gautier Viaud
date: 2026-03-25
type: paper
arxiv: "2603.24639"
---

# ERL: Experiential Reflective Learning for Self-Improving LLM Agents

## Abstract

Agents struggle to adapt to specialized environments and don't leverage past interactions. ERL enables improvement through experience: reflect on outcomes → generate reusable heuristics → retrieve and apply to future tasks. +7.8% over ReAct on Gaia2. Selective heuristic retrieval outperforms reusing trajectories.

## Framework (2 Stages)

### 1. Heuristic Generation (post-task)

After execution, agents reflect on trajectories and outcomes to create structured heuristics:
- Analysis identifying success/failure causes
- Actionable guidelines with explicit trigger conditions and recommended actions

Example: "When sending emails to calendar attendees, first resolve names to email addresses via the Contacts tool"

### 2. Retrieval-Augmented Execution (new tasks)

LLM scores stored heuristics for relevance, injects top-k into system prompt.

## Heuristics vs. Trajectories (Critical Finding)

| Approach | Execution | Search | Overall |
|----------|-----------|--------|---------|
| Raw trajectories (few-shot) | -1.9% vs baseline | — | Worse |
| Heuristics (ERL) | +5.5% | +23.8% | +7.8% |

Heuristics provide "distilled strategic principles that generalize across tasks" rather than task-specific examples. Raw trajectories fail to improve and can hurt performance.

## Gaia2 Benchmark Results

| Method | Execution | Search | Overall |
|--------|-----------|--------|---------|
| Baseline (ReAct) | 43.1% | 53.6% | 48.3% |
| Few-shot | 41.7% | 51.2% | 46.4% |
| ExpeL | 45.8% | 56.0% | 50.9% |
| **ERL** | **51.4%** | **60.7%** | **56.1%** |

## Selective Retrieval Findings

- Random selection peaks at 40-60 heuristics then degrades — indiscriminate inclusion is counterproductive
- LLM-based retrieval (k=20): 56.1% — best
- Embedding-based retrieval (k=20): 53.3%
- Failure-derived heuristics excel on Search (+14.3%)
- Success-derived heuristics optimize Execution (+9.0%)

## Cost

ERL incurs 40% increased API costs due to ~20k tokens of heuristics appended per turn. Prompt caching partially mitigates.

## Relevance to Knowledge Bases

ERL's heuristic generation is the academic formalization of our /review reescrita ativa: reflect on wiki state → generate actionable guidelines → apply to future /ask and /ingest. The finding that heuristics > trajectories validates our design choice of concept-based articles over raw source dumps.
