---
source: https://arxiv.org/abs/2305.17493
authors: Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Yarin Gal, Nicolas Papernot, Ross Anderson
date: 2023-05-27
type: paper
arxiv: "2305.17493"
venue: Nature 2024
stance: challenging
---

# The Curse of Recursion: Training on Generated Data Makes Models Forget (Model Collapse)

## Abstract

Use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. This "Model Collapse" occurs across multiple architectures (VAEs, GMMs, LLMs). As AI-generated text populates the internet, data quality concerns become critical. Data collected about genuine human interactions will be increasingly valuable.

## Key Finding

Model collapse = recursive self-consumption destroys distributional diversity. Tails disappear first — rare but important information is lost. The model converges to a narrow, homogeneous output.

## Direct Challenge to LLM-KB Architecture

This is the academic formalization of our "semantic convergence" failure mode (autonomous-kb-failure-modes). When an LLM writes wiki articles, then reads those articles to write more articles or answer questions, and the answers feed back into the wiki — this is recursive self-consumption on knowledge, not weights.

The analogy:
- Model collapse (weights): train on own output → distribution narrows → tails disappear
- Wiki collapse (knowledge): compile from own synthesis → diversity narrows → nuance disappears

Our raw/ immutability principle is the mitigation: raw/ is "real data" (human-written sources), wiki/ is "generated data" (LLM-compiled). As long as /ingest always reads raw/ (not wiki/) to generate articles, the recursive loop is broken. But /review reads wiki/ to improve wiki/ — that's the recursive path.

## Mitigation from the Paper

"If data accumulates and models train on a mixture of real and synthetic data, model collapse no longer occurs." Applied to KB: always mix raw/ sources (real) with existing wiki (synthetic) when doing /review. Never let /review operate only on wiki/ without re-reading raw/.
