---
source: https://arxiv.org/abs/2407.13578
authors: Danna Zheng, Mirella Lapata, Jeff Z. Pan
date: 2024-07-18
type: paper
arxiv: "2407.13578"
stance: challenging
---

# How Reliable are LLMs as Knowledge Bases? Re-thinking Factuality and Consistency

## Abstract

Examines whether LLMs can serve as dependable knowledge repositories. Identifies two requirements: factuality (accurate on seen, uninformative on unseen) and consistency (stable answers). Tests 26 LLMs. Introduces UnseenQA dataset. Finds significant limitations requiring more principled evaluation.

## Key Definitions

**Factuality**: accurate on seen knowledge + uninformative (not wrong) on unseen knowledge
**Consistency**: stable answers when questioned repeatedly. BUT:
- High consistency on CORRECT answers = desirable
- Low consistency on WRONG answers = desirable (contradicts traditional metrics)

## UnseenQA Benchmark

3,000 questions created 2024-04-13 to ensure inaccessibility to all models. 5 answer types (number, person, time, location, other). 20 templates including future events and fictional individuals. Paired with SeenQA (3,000 from NQ, TriviaQA, PopQA).

## Critical Findings Across 26 Models

### Larger models are more consistently WRONG
Models with 65-70B parameters:
- Better on seen knowledge
- WORSE on unseen knowledge
- Higher consistency even when providing wrong answers
- Risk: "confidently and consistently spreading misinformation"

### Correlation paradox
Models with high consistency on correct answers ALSO show high consistency on wrong answers (r=0.78-0.81). You can't have one without the other.

### No seen→unseen transfer
"Performance on seen knowledge does not reliably predict performance on unseen knowledge" in standard prompting.

### Fine-tuning trade-off
Improves unseen handling (+UR) but DEGRADES seen performance (-NCR). Doesn't improve consistency.

### In-context learning
Adding "unsure" examples in prompts: UR improves from ~5% to ~95%. Most effective mitigation.

## Metrics
- Net Correct Rate (NCR): CR - WR (distinguishes misleading from accurate)
- Net Consistently Correct Rate (NCCR): accounts for both correctness + consistency
- Inconsistent/Uninformative Rate (IUR): safe handling of unknown info

## Direct Challenge to KB Architecture

This paper EMPIRICALLY grounds our speculative failure modes:
1. **Authority cascade**: larger models are more consistently wrong → our wiki compiled by a large model may contain confident, consistent errors that Layer 3 verification (by the same model) won't catch
2. **Confidence scoring**: our interpretation_confidence self-assessment is exactly what this paper shows is unreliable — the model is more confident when it's wrong, not less
3. **Unseen knowledge**: our wiki articles that synthesize ACROSS papers (cross-paper insights) are "unseen knowledge" to the model — novel combinations not in training data. This is where factuality degrades most.

The "unsure" prompting finding is directly actionable: our /ask should be prompted to say "I don't know" rather than confabulate when wiki coverage is thin.
