---
source: https://plato.stanford.edu/entries/bounded-rationality/
author: Herbert Simon (SEP entry)
date: 1956-01-01
type: article
quality: primary
stance: challenging
---

# Herbert Simon: Bounded Rationality and Satisficing

## Core Principle

Agents don't optimize — they satisfice. Instead of evaluating all alternatives to find the best, they search until finding one that meets a predefined threshold (aspiration level), then STOP.

"Satisficing replaces the optimization objective from expected utility theory of selecting an undominated outcome with the objective of picking an option that meets your aspirations."

## The Stopping Problem

Satisficing inherently embeds a stopping rule: search continues until an option meets or exceeds the aspiration level. Once found, search terminates. The rule is:

```
WHILE no option meets threshold:
  evaluate next option
  IF option >= aspiration_level:
    STOP, accept this option
  IF resources exhausted:
    STOP, lower aspiration_level or accept best seen
```

## Aspiration Levels: How to Set "Good Enough"

**Fixed**: predefined threshold for a given problem. Mathematically captured via ε-efficiency.

**Dynamic** (Selten): maintain a vector of goal variables, each with its own aspiration level. Adjust UP when many options exceed threshold (too easy). Adjust DOWN when no options meet threshold (too hard). Context-dependent, not absolute.

## Relationship to Optimization

Satisficing is NOT failed optimization. It's a deliberate strategy for environments where:
- Computational intractability prevents finding the optimal
- Information is incomplete
- Time/resource costs of further search exceed expected marginal gain

"The rules of rational behavior are costly to operate in both time and effort. Decision-makers have an interest in minimizing those costs."

## Fast and Frugal Heuristics (Gigerenzer)

- **Take-the-Best**: use single most important cue, ignore the rest
- **Tallying**: equal weights for all cues (no regression)
- **Less is more**: these OUTPERFORM linear regression on out-of-sample prediction when training data is limited

The bias-variance trade-off: "a mind can be better off with an adaptive toolbox of biased, specialized heuristics." Deliberately accept bias to reduce variance.

## Direct Challenge to KB Architecture

This is the missing piece. The KB has:
- How to ask questions (question-taxonomy, 9 types)
- How to evaluate answers (/challenge, /review)
- How to improve (/ingest, /curate, /scout)

But NOT:
- **When to stop asking** — when is the answer "good enough" to act on?
- **When to stop ingesting** — when do more sources have negative marginal return?
- **When to stop refining** — when does another /review cycle cost more than it improves?

### Aspiration Levels for the KB

| Activity | Aspiration level (when to stop) |
|----------|-------------------------------|
| /ask | When answer cites 2+ sources AND passes confidence check. Don't pursue "perfect" answer. |
| /ingest | When new sources stop generating novel concepts (Lakatos: programme degenerating). Our feedback says "stop after 42 sources" — that's satisficing. |
| /review | When no CRITICAL issues found. Don't chase minor style improvements (semantic convergence risk from over-reviewing). |
| /challenge | When top 3 claims classified. Don't challenge every sentence. |
| /scout | When 3 candidates found. Don't search exhaustively. |

### The Meta-Stopping Rule

"When the cost of the next improvement exceeds the cost of the error it prevents, stop."

Applied: one more /review cycle costs ~20 min of context. If the expected error it catches is a minor interpretation issue (not a factual error), the cost exceeds the benefit. Stop.

This is why our feedback memory says "stop refining, start using" — it's satisficing applied to KB maintenance.
