---
source: https://en.wikipedia.org/wiki/Information_cascade + Banerjee 1992
author: Abhijit V. Banerjee
date: 1992-01-01
type: article
quality: primary
stance: challenging
---

# A Simple Model of Herd Behavior (Banerjee, 1992)

## Definition

An information cascade occurs when individuals rationally ignore their own private information and follow the decisions of predecessors. Each person observes what others chose (but not WHY) and infers that others had good reasons. After enough people choose the same option, it becomes rational for everyone to follow — even if the accumulated "evidence" started from a small, possibly wrong, initial signal.

## Core Model

Sequential decision-making under uncertainty:
1. Each agent has PRIVATE information (a noisy signal about the true state)
2. Each agent observes the ACTIONS (but not the signals) of all predecessors
3. Bayesian updating: combine private signal with inferred information from others' actions
4. After a critical mass follows one option, the CASCADE starts: every subsequent agent follows, regardless of private signal

## Key Properties

1. **Rational herding** — following the herd IS rational given limited information. It's not irrational bias — it's optimal Bayesian inference with incomplete data.

2. **Fragility** — cascades can be WRONG. They're based on the accumulated weight of observed actions, which may trace back to a few early (possibly wrong) signals. A small initial error can cascade into widespread false consensus.

3. **Informational externality** — each person who follows the cascade STOPS contributing new information. The cascade destroys the information aggregation mechanism that would correct it.

4. **Reversibility** — cascades can break if new, sufficiently strong public information arrives. But the longer the cascade, the stronger the public signal needed to break it.

## When Cascades Form

- Sequential, irreversible decisions
- Public observation of actions but not reasons
- Costly private information gathering
- Preference for conformity (even rational conformity)

## Relevance to KB

### Authority Bias Cascade = Information Cascade

| Information Cascade (Banerjee) | KB Authority Bias Cascade |
|-------------------------------|--------------------------|
| Agent observes predecessors' ACTIONS, not signals | /ask reads wiki CLAIMS, not the reasoning behind them |
| Ignores private signal to follow herd | /ask confirms wiki claim against raw/ (same LLM reading both — "private signal" is contaminated) |
| Small initial error cascades | /ingest misinterpretation crystallizes across /review cycles |
| Cascade destroys information aggregation | Over-synthesis homogenizes — new sources absorbed into existing narrative instead of challenging it |
| Breaks with strong public signal | > [!patch] from human = strong external signal that breaks cascade |

### What the Literature Knows That the KB Doesn't

1. **Cascades are RATIONAL** — the KB frames authority bias as a "bias" (implying irrationality). Banerjee shows it's rational given the information structure. The LLM is being RATIONAL by confirming its own wiki — it's doing optimal Bayesian updating given that wiki claims have citation authority. The fix isn't "remove bias" — it's "change the information structure."

2. **Fragility means cascades CAN break** — a single strong contradicting signal (human patch, external review, challenging source) can collapse an entire cascade. Our /curate (adversarial sources) and spot-check (external LLM) are cascade-breakers. Their value isn't proportional to frequency — ONE good challenge can undo months of cascade.

3. **The cascade STOPS information aggregation** — once wiki articles start confirming each other, new sources are absorbed into the existing narrative. This is EXACTLY "semantic convergence." The information that new sources carry is lost because the cascade makes the LLM interpret new sources through the existing lens.

4. **Early signals have disproportionate weight** — the first few articles in the wiki (written when the KB was empty, with no prior context) have outsized influence. All subsequent articles are "downstream" of the initial framing. This explains why kb-architecture-patterns (one of the first articles, never challenged) has 13 inbound links — it set the cascade direction.

5. **Cascade-breaking requires PUBLIC information, not just private** — in Banerjee's model, private signals can't break cascades because others can't observe them. Applied to KB: a correction buried in an article's ## Interpretação doesn't break the cascade — it needs to be in ## Conteúdo or _index.md (the "public" facing parts) to propagate.
