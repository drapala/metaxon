---
title: "LLM-as-Judge"
sources:
  - path: raw/papers/llms-as-judges-survey.md
    type: paper
    quality: primary
  - path: raw/papers/calm-llm-judge-biases.md
    type: paper
    quality: primary
  - path: raw/papers/judgebench-evaluating-llm-judges.md
    type: paper
    quality: primary
  - path: raw/papers/carmo-context-aware-reward-modelling.md
    type: paper
    quality: primary
created: 2026-04-03
updated: 2026-04-03
tags: [evaluation, bias, reliability, quality]
confidence: high
resolved_patches: []
---

## Resumo

LLM-as-Judge is the paradigm of using LLMs to evaluate other LLM outputs. A comprehensive survey identifies three evaluation modes (pointwise, pairwise, listwise), while bias research reveals 12 systematic biases — most critically self-enhancement (models prefer own outputs) and position bias. JudgeBench shows that even GPT-4o performs near random on genuinely difficult evaluation tasks. CARMO/SALC demonstrates that dynamic criteria generation outperforms static rubrics.

## Conteúdo

### Three Evaluation Modes

| Mode | Description | Use in KB |
|------|-------------|-----------|
| **Pointwise** | Score individual items independently | /ask confidence scoring (high/medium/low) |
| **Pairwise** | Compare two candidates directly | wiki vs raw/ verification (Layer 3) |
| **Listwise** | Rank multiple items collectively | /ask selecting top 5-10 relevant articles |

Modes exhibit inconsistencies: pointwise scores don't consistently yield equivalent pairwise comparisons. Transitivity doesn't always hold.

### The 12 Biases (CALM Framework)

| Bias | Description | Impact on KB |
|------|-------------|-------------|
| **Self-Enhancement** | Favors own outputs (up to 16.1% error) | LLM prefers its own wiki articles in /review |
| **Position** | Favors answers at certain positions | /ask may prefer articles listed first in _index.md |
| **Verbosity** | Prefers longer responses | /ingest may over-value verbose sources |
| **Authority** | Favors cited answers (even fake citations) | /ask may over-trust wiki claims with raw/ links |
| **Fallacy-Oversight** | Overlooks logical errors | /review may miss contradictions in articles |
| **Sentiment** | Prefers certain emotional tones (fear = most impact) | — |
| **Bandwagon** | Influenced by majority opinion | — |
| **Distraction** | Distracted by irrelevant details | /ask may be derailed by tangential wiki content |
| **Compassion-Fade** | Responds differently to known vs anonymous models | — |
| **Diversity** | Demographic bias | — |
| **Chain-of-Thought** | Performance varies with reasoning prompts | /ask benefits from explicit Layer 1→2→3 structure |
| **Refinement-Aware** | Scores differently when aware of revision history | /review may treat patched articles differently |

**Most severe for KBs:** self-enhancement (same LLM writes and judges) and authority bias (citations create false confidence).

### Judge Reliability is Inflated (JudgeBench)

JudgeBench (ICLR 2025) tested LLM judges on genuinely difficult problems:
- GPT-4o: "just slightly better than random guessing"
- Gap between easy benchmarks (judges appear reliable) and hard benchmarks (near random) suggests reported reliability is inflated by benchmark difficulty

**Implication:** Our /ask confidence scoring may be unreliable for complex queries. The 3-layer retrieval with raw/ verification is more robust than self-assessment alone.

### Dynamic Criteria > Static Rubrics (CARMO/SALC)

CARMO/SALC generates evaluation criteria dynamically per query instead of using fixed rubrics:

1. Autonomously generate context-specific criteria
2. Assess using generated criteria
3. Fine-tuned 13B model outperforms GPT-4o (Pearson 0.924 vs 0.896)

**Results on alignment training:**

| Model | Improvement |
|-------|------------|
| Mistral-7b | +12.58% |
| Phi-2 | +9.69% |
| Phi-3-Mini | +3.41% |

**Implication:** Our /review could generate dynamic assessment criteria per article instead of applying uniform heuristics. The blueprint's fixed 5-point validation checklist could be replaced with context-aware criteria.

### Model Robustness Comparison

| Model | Fact-Related RR | Alignment RR | Overall |
|-------|----------------|--------------|---------|
| GPT-4o | 0.977 | 0.776 | Strong on facts |
| Claude-3.5 | 0.952 | 0.832 | Best overall resilience |
| GPT-4-Turbo | 0.915 | 0.818 | Good alignment |
| ChatGPT | 0.900 | 0.566 | Worst alignment |

Claude-3.5 shows greatest overall bias resilience. Advanced models don't automatically resist bias better.

### Mitigations for Knowledge Bases

1. **Don't use same model for generation and evaluation.** Self-enhancement bias makes this unreliable. Consider different model for /review vs /ingest.
2. **Verify against raw/ (Layer 3).** External ground truth beats self-assessment. Our architecture already does this — principle 9 ("retrieval is skeptical") directly addresses authority bias.
3. **Human patches as external signal.** The `> [!patch]` system provides bias-free corrections.
4. **Chain-of-Thought for evaluation.** CoT improves accuracy 0.7-7%. Our /ask's explicit Layer 1→2→3 structure provides this.
5. **Dynamic criteria for /review.** Instead of fixed checklist, generate per-article assessment criteria.

## Conexões

- [[self-improving-agents]] — Reflexion uses self-evaluation; biases documented here affect that loop
- [[kb-architecture-patterns]] — our confidence scoring and validation criteria are LLM-as-judge systems
- [[context-management]] — position bias means _index.md ordering may affect /ask article selection
- [[memory-consolidation]] — /review (LLM judging wiki quality) is susceptible to self-enhancement bias
- [[tension-resolution]] — bias-aware resolution protocol informed by CALM and JudgeBench findings

## Fontes

- [LLMs-as-Judges Survey](../../raw/papers/llms-as-judges-survey.md) — comprehensive framework: 5 perspectives, 3 evaluation modes, 4 bias categories, domain applications
- [CALM — LLM Judge Biases](../../raw/papers/calm-llm-judge-biases.md) — 12 bias types quantified, self-enhancement up to 16.1% error, Claude-3.5 most resilient
- [JudgeBench](../../raw/papers/judgebench-evaluating-llm-judges.md) — GPT-4o near random on hard tasks, reliability inflated by benchmark difficulty
- [CARMO/SALC](../../raw/papers/carmo-context-aware-reward-modelling.md) — dynamic criteria > static rubrics, 13B model outperforms GPT-4o, +12.58% alignment gains
