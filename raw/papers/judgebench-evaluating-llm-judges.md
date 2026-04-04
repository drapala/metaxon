---
source: https://arxiv.org/abs/2410.12784
authors: Sijun Tan, Siyuan Zhuang, Kyle Montgomery, William Y. Tang, Alejandro Cuadron, Chenguang Wang, Raluca Ada Popa, Ion Stoica
date: 2024-10-16
type: paper
arxiv: "2410.12784"
venue: ICLR 2025
---

# JudgeBench: A Benchmark for Evaluating LLM-based Judges

## Abstract

Addresses dependability of LLM-based judges. JudgeBench assesses judges on difficult problems involving knowledge, reasoning, math, and coding. Converts challenging datasets into comparable response pairs with accuracy-based labels. Even GPT-4o performs "just slightly better than random guessing" — JudgeBench poses significantly greater challenge than previous benchmarks.

## Key Finding

Current LLM judges fail on genuinely difficult evaluation tasks. The gap between easy benchmarks (where judges appear reliable) and hard benchmarks (where they approach random guessing) suggests that reported judge reliability is inflated by benchmark difficulty, not actual judge capability.

## Relevance to Knowledge Bases

Our /ask uses the LLM as judge of its own confidence (high/medium/low). JudgeBench warns that this self-assessment may be unreliable for complex queries. The mitigation: our 3-layer retrieval with raw/ verification is more robust than pure self-assessment — we verify claims against sources rather than trusting the LLM's confidence judgment alone.

---

*Nota: conteúdo baseado no abstract + metadados. Consultar PDF para benchmark construction details e per-model results.*
