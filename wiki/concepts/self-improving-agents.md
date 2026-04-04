---
title: "Self-Improving Agents"
sources:
  - path: raw/papers/reflexion-verbal-reinforcement-learning.md
    type: paper
    quality: primary
  - path: raw/papers/erl-experiential-reflective-learning.md
    type: paper
    quality: primary
  - path: raw/papers/self-evolving-agents-survey.md
    type: paper
    quality: primary
  - path: raw/papers/textgrad-automatic-differentiation-text.md
    type: paper
    quality: primary
  - path: raw/papers/promptbreeder-self-referential-improvement.md
    type: paper
    quality: primary
  - path: raw/papers/absolute-zero-reinforced-self-play.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [agent-architecture, self-improvement, reflection, learning]
confidence: high
resolved_patches: []
---

## Resumo

Self-improving agents learn from experience without weight updates, using verbal reflection, heuristic generation, or feedback loops to improve future performance. Two foundational approaches: Reflexion (reflect on failures → store in episodic memory → retry) and ERL (reflect on outcomes → generate reusable heuristics → retrieve for future tasks). A critical finding: abstracted heuristics transfer better than raw trajectories.

## Conteúdo

### The Core Problem

LLM agents make the same mistakes repeatedly across sessions. Traditional RL requires weight updates (expensive, unstable). Self-improving agents use the LLM's own language capabilities to learn from experience within the context window.

### Reflexion: Learning from Failure via Verbal Reflection

**Architecture (3 components):**
- **Actor**: LLM generates actions
- **Evaluator**: scores outputs (exact match, heuristics, or LLM-based)
- **Self-Reflection**: generates verbal feedback analyzing failures → actionable insights

**Loop:** trajectory → evaluation → verbal reflection → memory update → retry

**Memory:**
- Short-term: current trajectory (fine-grained)
- Long-term: stored self-reflections (1-3 experiences, bounded by context)

**Key insight:** Converts scalar/binary feedback into verbal feedback — "action A_i led to incorrect A_{i+1}" with suggested alternatives. Mimics human learning from mistakes.

**Results:**
- HumanEval Python: 80.1% (GPT-4) → 91.0% (Reflexion)
- AlfWorld: +22% absolute over ReAct (130/134 tasks in 12 iterations)
- HotPotQA: CoT 0.61 → 0.75 (+14%)

**Ablation:** Self-reflection without grounded feedback (tests) degrades to 52%. Trajectory replay without reflection: no improvement. Verbal reflection outperforms episodic memory by 8%.

### ERL: Heuristics > Trajectories

**Framework (2 stages):**
1. Post-task: reflect on outcomes → generate structured heuristics with trigger conditions
2. New task: LLM-based retrieval of relevant heuristics → inject into system prompt

**Critical finding:**

| Approach | Performance |
|----------|------------|
| Raw trajectories (few-shot) | -1.9% vs baseline (WORSE) |
| Heuristics (ERL) | +7.8% vs baseline |

Heuristics provide "distilled strategic principles that generalize across tasks." Trajectories are too specific and can hurt. Example heuristic: "When sending emails to attendees, first resolve names to email addresses via Contacts tool."

**Selective retrieval matters:**
- Random inclusion peaks at 40-60 heuristics then degrades
- LLM-based retrieval (k=20): 56.1% — best
- Failure-derived heuristics excel on Search (+14.3%)
- Success-derived heuristics optimize Execution (+9.0%)

### The Spectrum of Self-Improvement

| Method | What's stored | Granularity | Transfer |
|--------|--------------|-------------|----------|
| Reflexion | Verbal self-reflections | Per-failure | Same task (retry) |
| ERL | Abstracted heuristics | Per-outcome | Cross-task |
| Agent KB | Structured experiences | Per-trajectory | Cross-framework |
| Agent KB | Structured experiences | Per-trajectory | Cross-framework |
| KAIROS/Dream | Memory consolidation | Per-session | Cross-session |

### TextGrad: Optimizing via Textual Feedback

TextGrad treats LLM-generated textual feedback as "gradients" flowing backward through a computational graph. Each component (prompt, code, molecule) receives targeted natural language criticism and improves iteratively. Follows PyTorch conventions (Variable, loss function, optimizer).

| PyTorch | TextGrad |
|---------|----------|
| Tensor | Variable (text string) |
| Loss function | Evaluation prompt |
| Gradient | Textual feedback from LLM |
| Optimizer.step() | Apply feedback to update variable |

Results: +20% relative gains on coding problems, improved GPT-4o zero-shot QA. Applicable beyond agents — optimizes any text-based component.

**Relevance:** TextGrad automates the evaluate → feedback → update loop. Our patch system is manual TextGrad; a future /lint could implement automated textual gradient feedback on wiki articles.

### The Self-Evolving Agent Taxonomy

The Self-Evolving Agents survey (2025) provides the broadest taxonomy, organizing self-improvement across three dimensions:

**What to evolve:** model parameters, memory, tools/skills, prompts

**When to evolve:**
- Pre-deployment (training-time adaptation)
- During execution (in-context learning, reflection) ← Reflexion
- Post-execution (experience consolidation) ← ERL, KAIROS
- Continuous (ongoing background evolution) ← auto-dream

**How to evolve:**
- Self-reflection (Reflexion, ERL)
- Reinforcement learning (reward-driven)
- Evolutionary methods (Promptbreeder)
- Knowledge transfer (cross-domain, Agent KB)
- Synthetic data generation (Absolute Zero)

Our KB maps to this taxonomy: /ingest = pre-deployment, /ask = during execution, /review = post-execution, /dream = continuous.

### Promptbreeder: Self-Referential Prompt Evolution

Evolutionary approach: population of (task prompt, mutation prompt) pairs. The mutation prompt mutates the task prompt; both are selected by fitness. Self-referential: the system evolves the tools that evolve the prompts, preventing stagnation. Outperforms Chain-of-Thought on reasoning benchmarks.

**Relevance:** Our /ingest and /ask prompts are static (hand-written in CLAUDE.md). Promptbreeder-style evolution could optimize them based on /ask quality metrics. Fase 3 potential.

### Absolute Zero: Self-Play Without Data

Models autonomously generate training tasks and improve reasoning via RL. Code execution provides a cheap, reliable, scalable reward signal — no human annotation needed. Surpasses baselines using tens of thousands of human-annotated examples.

**Relevance:** A self-improving KB could use self-play: agent generates questions about its own wiki → attempts to answer → evaluates against raw/ → uses feedback to improve articles and retrieval. This would automate the /ask → evaluate → /review cycle entirely.

### Relevance to This Knowledge Base

Our pipeline already implements self-improvement patterns:
- **Patch system** (`> [!patch]`) = manual Reflexion: identify error → verbal feedback → incorporate
- **/review reescrita ativa** = automated ERL: reflect on wiki state → generate improvements → apply
- **Heuristics > trajectories** validates our design: concept-based articles (heuristics) > raw source dumps (trajectories)

## Conexões

- [[memory-consolidation]] — KAIROS/Dream is self-improvement across sessions; Reflexion is within-task
- [[kb-architecture-patterns]] — ERL validates Pattern 1 (concept articles > raw sources)
- [[autonomous-research-agents]] — Deep Research pipeline could use Reflexion for iterative query refinement
- [[context-management]] — self-reflection memories compete for context budget
- [[llm-as-judge]] — 12 biases affect self-evaluation loops; self-enhancement (16.1%) is the central risk
- [[agent-memory-architectures]] — memory structures that enable self-improvement
- [[multi-agent-orchestration]] — Agent KB enables cross-framework knowledge transfer

## Fontes

- [Reflexion](../../raw/papers/reflexion-verbal-reinforcement-learning.md) — verbal RL: 91% HumanEval, +22% AlfWorld, reflection > replay by 8%
- [ERL](../../raw/papers/erl-experiential-reflective-learning.md) — heuristics > trajectories: +7.8% Gaia2, selective retrieval critical, failure heuristics excel on search
- [Self-Evolving Agents Survey](../../raw/papers/self-evolving-agents-survey.md) — broadest taxonomy: what/when/how to evolve, covers models, memory, tools, prompts
- [TextGrad](../../raw/papers/textgrad-automatic-differentiation-text.md) — textual gradients as optimization: PyTorch-style feedback loop, +20% coding gains
- [Promptbreeder](../../raw/papers/promptbreeder-self-referential-improvement.md) — self-referential prompt evolution: evolves both task prompts and mutation prompts
- [Absolute Zero](../../raw/papers/absolute-zero-reinforced-self-play.md) — self-play reasoning with zero data: code execution as reward signal, surpasses human-annotated baselines
