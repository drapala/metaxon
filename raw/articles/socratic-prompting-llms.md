---
source: https://arxiv.org/abs/2303.08769
author: Edward Y. Chang
date: 2023-02-17
type: paper
arxiv: "2303.08769"
stance: neutral
---

# Prompting Large Language Models With the Socratic Method

## Abstract

Applies classical Socratic dialogue techniques to prompt engineering. Examines definition, elenchus, dialectic, maieutics, generalization, and counterfactual reasoning. Conveying task goals and user intent upfront enables model to perform more effectively.

## 6 Socratic Techniques Applied to LLMs

### 1. Definition (τί ἐστι — "What is it?")
Clarify concepts before reasoning about them.
**LLM application:** "Before answering, define what [concept] means in this context."
**KB application:** Force /ask to define terms before synthesizing. Prevents semantic drift.

### 2. Elenchus (Cross-examination)
Challenge claims by finding contradictions.
**LLM application:** "What's the strongest counterargument to this claim?"
**KB application:** The /challenge command IS elenchus applied to wiki articles.

### 3. Dialectic (Thesis → Antithesis → Synthesis)
Present opposing views, then find higher truth.
**LLM application:** "Article A says X. Article B says Y. What's the synthesis that resolves both?"
**KB application:** Tension resolution is dialectic. Our Known Tensions table is the thesis-antithesis; the resolution column is the synthesis.

### 4. Maieutics (Intellectual midwifery)
Help the questioner discover what they already know through guided questions.
**LLM application:** "Given what you know about [topic], what conclusion follows?"
**KB application:** /ask should follow wikilinks from known articles to discover connections the user hasn't explicitly asked about.

### 5. Generalization (Induction)
Move from specific examples to general principles.
**LLM application:** "These 3 papers each describe [specific]. What general principle unifies them?"
**KB application:** This is how taxonomy articles (kb-architecture-patterns) are generated.

### 6. Counterfactual Reasoning
"What if the opposite were true?"
**LLM application:** "If [key assumption] were false, how would the conclusion change?"
**KB application:** The most powerful question for /challenge: "Under what conditions does this claim fail?"

## Connection to Reasoning Types

| Socratic Method | Reasoning Type |
|----------------|---------------|
| Definition | Clarification |
| Elenchus | Deductive (find contradiction) |
| Dialectic | Abductive (best explanation) |
| Maieutics | Inductive (guided discovery) |
| Generalization | Inductive (specific → general) |
| Counterfactual | Abductive (alternative explanations) |
