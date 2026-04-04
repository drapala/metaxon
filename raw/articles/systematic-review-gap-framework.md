---
source: https://www.ncbi.nlm.nih.gov/books/NBK126702/
author: AHRQ (Agency for Healthcare Research and Quality)
date: 2013-01-01
type: article
quality: primary
stance: neutral
---

# Framework for Determining Research Gaps During Systematic Reviews

## Definition

A research gap is "a topic or area for which missing or inadequate information limits the ability of reviewers to reach a conclusion for a given question."

Key distinction: gaps become NEEDS only when addressing them would benefit decision-makers. Not all gaps are worth filling.

## Two-Element Framework

### Element 1: Gap Characterization (PICOS)

Describe the inadequately addressed question using:
- **P**opulation: who/what is studied?
- **I**ntervention: what's being tested?
- **C**omparison: against what?
- **O**utcomes: what's measured?
- **S**etting: where/when?

### Element 2: Why the Gap Exists (4 Reasons)

| Reason | Description |
|--------|-------------|
| **Insufficient or imprecise information** | Not enough data or data lacks clarity |
| **Biased information** | Methodological or systematic distortions |
| **Inconsistent results** | Conflicting findings across studies |
| **Not the right information** | Evidence addresses different question than needed |

## Relevance to LLM Knowledge Bases

The 4 gap reasons map directly to KB quality issues:

1. **Insufficient info** → article has too few sources (source_quality:low)
2. **Biased info** → all sources are confirming (adversarial gap, stance ratio)
3. **Inconsistent results** → documented tensions between articles
4. **Not the right info** → sources don't actually address the concept (over-synthesis — we cited papers that don't say what we claim they say)

The PICOS framework could structure /ask queries:
- P: which concept/article?
- I: what mechanism/approach?
- C: compared to what alternative?
- O: measured by what metric?
- S: in what context/scale?

This forces structured questions instead of vague "what emerges from the intersection?"
