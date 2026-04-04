---
source: https://arxiv.org/abs/2503.02879
authors: Siming Huang, Yuliang Xu, Mingmeng Geng, Yao Wan, Dongping Chen
date: 2025-03-04
type: paper
arxiv: "2503.02879"
stance: challenging
---

# Wikipedia in the Era of LLMs: Evolution and Risks

## Abstract

Comprehensive analysis of how LLMs affect Wikipedia. Articles show ~1% impact in certain categories. Contaminated training data could inflate benchmarks and compromise RAG effectiveness. "LLMs have not yet fully changed Wikipedia's language and knowledge structures" but future risks warrant careful consideration.

## Key Findings Relevant to LLM KBs

1. **AI-revised Wikipedia content lowered RAG performance, particularly in factual accuracy.** If our wiki articles are LLM-compiled and later used as retrieval context for /ask, the same degradation applies.

2. **Feedback loop risk:** "RAG systems could end up retrieving AI-generated information to fact-check AI-generated responses." Our Layer 3 verification (wiki → check against raw/) is designed to break this loop, but only if raw/ stays human-authored.

3. **Stylistic homogenization detected:** Wikipedia sentences becoming "more AI-like, with longer, more complex sentences but fewer auxiliary verbs." Our semantic convergence concern is validated at Wikipedia scale.

4. **Human contributor decline:** "once more than half of online activity is transacted by AI, human users may decide to leave." For a personal KB, this translates to: if the wiki feels too synthetic, the human stops engaging with it.

## Direct Challenge

This paper argues that LLM-compiled knowledge systems degrade the quality of the very knowledge they compile. Our KB is a micro-scale Wikipedia compiled by LLM — the same risks apply, perhaps more acutely because we have one compiler (not many) and no community review process.
