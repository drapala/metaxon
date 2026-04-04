---
source: https://plato.stanford.edu/entries/lakatos/
author: Imre Lakatos (SEP entry by Alan Musgrave & Charles Pigden)
date: 1970-01-01
type: article
quality: primary
stance: neutral
---

# Lakatos: Methodology of Scientific Research Programmes

## Core Innovation: Evaluate Programmes, Not Individual Theories

Rather than evaluating individual theories (Popper), assess entire sequences of related theories as unified systems. Scientists rationally persist with theories that appear falsified — contradicting Popper's strict falsificationism.

## Hard Core vs Protective Belt

**Hard Core**: central, irrefutable theses that define the programme. Protected from direct refutation.

**Protective Belt**: auxiliary hypotheses that absorb empirical challenges. When predictions fail, modify the belt, not the core.

"The negative heuristic forbids directing criticism at the hard core. Instead, scientists create auxiliary hypotheses forming a protective belt around this core, with the belt bearing the brunt of tests."

## Progressive vs Degenerating Research Programmes

**Progressive** (2 conditions):
- Theoretically progressive: each new theory predicts NOVEL facts previously unexpected
- Empirically progressive: some novel predictions gain support

**Degenerating**:
- Predicts nothing new, or novel predictions systematically fail
- Explains failures only AFTER they occur (ad hoc adjustments)
- Example: Marxism predicted working-class impoverishment → falsified → ad hoc explanations constructed after each failure

## Evaluation Criteria

- Does the programme yield predictions unprecedented in rivals?
- Do predictions become empirically confirmed?
- Are anomalies addressed through genuine theoretical development or ad-hoc patches?

Newton: predicted Halley's Comet return 72 years later — genuinely novel, spectacularly confirmed.

## Relationship to Popper and Kuhn

- vs Popper: accepts falsifiability but rejects immediacy. Permits rational persistence with hard core while modifying protective belt.
- vs Kuhn: substitutes logico-methodological criteria for socio-psychological factors. Competing programmes, not single paradigms.

## Relevance to LLM Knowledge Bases

Lakatos's framework maps directly to KB architecture:

1. **Hard core = blueprint principles** (raw/ immutable, wiki as hint, retrieval is skeptical). These are methodologically protected — we don't question them.

2. **Protective belt = commands and heuristics** (/ingest steps, /review checks, confidence scoring). These are modified when predictions fail.

3. **Progressive vs degenerating** applies to the KB itself:
   - Progressive: each new source generates novel predictions (insights not in existing articles) and some predictions corroborate (/ask answers that prove correct)
   - Degenerating: new sources only confirm what we already "knew," novel synthesis fails when tested (RWKG subsumed by prior work)

4. **Ad hoc adjustments** = our "qualifying numbers after the fact" (16.1% → "on Qwen2," 52% → "on HumanEval"). Are these genuine refinements (protective belt strengthened) or ad hoc patches (programme degenerating)?

5. **When to abandon**: Lakatos says a programme degenerates when it stops producing novel predictions. If /ask keeps generating the same types of insights regardless of new sources, the KB is degenerating — it's confirming itself, not discovering.
