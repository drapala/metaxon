---
source: https://arxiv.org/abs/2303.11366
authors: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
date: 2023-03-20
type: paper
arxiv: "2303.11366"
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

## Abstract

Introduces Reflexion, which reinforces language agents through linguistic feedback rather than weight updates. Agents verbally reflect on task feedback signals and maintain reflective text in memory to improve future decisions. Achieves 91% pass@1 on HumanEval (surpassing GPT-4's 80%).

## Core Architecture (3 Components)

- **Actor (M_a)**: LLM that generates text/actions conditioned on state observations + memory
- **Evaluator (M_e)**: Scores outputs using task-specific metrics (exact match, heuristics, LLM-based)
- **Self-Reflection (M_sr)**: Generates verbal feedback analyzing trajectory failures → actionable insights

### Memory Structure

- **Short-term**: current trajectory history (fine-grained recent details)
- **Long-term**: stored self-reflections from prior trials (bounded to 1-3 experiences)

### Iterative Loop

trajectory generation → evaluation → verbal reflection → memory update → retry

When evaluator deems performance inadequate, agent generates reflection analyzing failure, stores as linguistic experience, attempts task again with augmented context.

## Verbal Reinforcement Mechanism

Converts binary/scalar feedback into verbal feedback as textual summary. Provides concrete improvement directions: "action A_i led to incorrect A_{i+1} and A_{i+2}" → suggests alternatives. Mimics human learning: reflecting on failures to form improved plan of attack.

## Results

### HumanEval Programming

| Benchmark | GPT-4 | Reflexion |
|-----------|-------|-----------|
| HumanEval Python | 80.1% | **91.0%** |
| HumanEval Rust | 60.0% | **68.0%** |

### AlfWorld (Sequential Decision-Making)

130/134 tasks completed within 12 iterative steps (+22% over ReAct baseline). ReAct plateaued at 78% after 6-7 trials; Reflexion showed continuous learning.

### HotPotQA Reasoning

CoT accuracy: 0.61 → 0.75 (+14% absolute). ReAct: 0.39 → 0.51.

## Ablation Findings

- Self-reflection alone (without test generation) degrades performance to 52%
- Test generation without self-reflection: no improvement (agent can't determine correctness without tests)
- Self-reflection outperformed episodic memory-only by 8% — verbal explanation provides stronger learning than trajectory replay

## Limitations

- Susceptible to local minima on tasks requiring significant diversity/exploration
- Relies on LLM self-evaluation quality without formal guarantees
- Non-deterministic functions challenge test-driven approaches

## Relevance to Knowledge Bases

Reflexion's verbal reflection → memory → retry loop is structurally analogous to our patch system: identify error → `> [!patch]` → /review incorporates fix. The key insight: linguistic feedback (not just scalar scores) enables more targeted improvement. Our /review's "reescrita ativa" is essentially Reflexion applied to wiki articles.
