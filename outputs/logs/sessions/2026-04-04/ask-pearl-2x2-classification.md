# Ask Session Log
date: 2026-04-04 ~05:30
query: "Usando Pearl, classifique as 4 células do 2x2 (verbal/scalar × ancorado/não-ancorado)"
synthesis_type: MECHANISM
confidence: high

## Articles read
- wiki/concepts/causal-reasoning-pearl.md — usado (framework principal)
- wiki/concepts/self-improving-agents.md — usado (Reflexion data)
- wiki/concepts/llm-as-judge.md — referenciado mas não lido em detalhe

## Raw sources verified
- raw/papers/pearl-book-of-why-ch1-3.md — P(y|do(x)), hierarchy theorem
- raw/papers/reflexion-verbal-reinforcement-learning.md — 91%, 52%, ~83% episodic

## Retrieval gaps
- wiki/concepts/self-improving-agents.md seção TextGrad — deveria ter sido explorada (TextGrad = textual gradients vs numerical, diretamente na fronteira verbal/scalar). Não selecionado porque Layer 1 ponteiro não menciona "verbal vs scalar."

## Response summary
4 células classificadas por Pearl. A vs B = L2 (ancoragem, -39pp). A vs C = L2 parcial (verbalidade, ~-8pp, controle imperfeito). "Epifenômeno" é falsificável em L2 (intervenção), não requer L3. L3 requer SCM + cross-world reasoning. Simon: L2 satisfice.

## Follow-up flags
- TextGrad como ponte verbal↔scalar merece /ask dedicado
- Design experimental 2x2 merece ser salvo como outputs/reports/ pra referência futura
- "L2 basta" é satisficing — deveria ser documentado como design decision, não como fato
