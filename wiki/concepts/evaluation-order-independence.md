---
title: "Evaluation Order Independence"
sources:
  - path: wiki/concepts/curse-of-knowledge-llm-judge.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/causal-reasoning-pearl.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [evaluation, llm-judge, causality, protocol-design, reference-anchoring, pearl]
source_quality: medium
interpretation_confidence: low
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: true
quarantine_created: 2026-04-05
quarantine_reason: "Artigo emergido de /ask cross-domain — aguarda confirmação adversarial e review frio"
quarantine_promoted: null
quarantine_criteria_met:
  tempo: false
  review_frio: false
  adversarial_or_scout_or_prediction: "predição L2 adicionada 2026-04-05 + confirmação externa Shi et al. (arXiv:2406.07791)"
provenance: emergence
emergence_trigger:
  pair: [curse-of-knowledge-llm-judge, causal-reasoning-pearl]
  ask_session: outputs/logs/sessions/2026-04-05/ask-curse-knowledge-pearl.md
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-05
---

## Resumo

Quando um LLM judge recebe uma referência antes de formar julgamento independente, cria-se reference-anchoring bias — um failure de raciocínio contrafactual (Pearl L3) impossível de corrigir internamente. A única solução robusta é uma intervenção de design (Pearl L2): sequestrar a referência até o julgamento independente estar formado. Este princípio — evaluation order independence — afirma que a ordem em que evidências chegam ao avaliador é uma variável causal, não uma decisão de UX.

## Conteúdo

### O que curse-of-knowledge-llm-judge contribui

Reference-anchoring bias ocorre quando um LLM judge recebe a resposta-referência antes de avaliar a resposta candidata. O modelo passa a avaliar a candidata *contra* a referência — não de forma independente. O mecanismo é empírico: DeepSeek-R1 sofre decline 4× maior que o modelo geral equivalente sob ataque adversarial, pois sua cadeia-de-raciocínio estendida cria mais oportunidade de racionalizar alinhamento com a referência.

**Chave:** a referência melhora accuracy em inputs limpos E degrada accuracy em inputs perturbados. Auxiliary information é simultaneamente útil e exploitável — dependendo de *quando* chega.

### O que causal-reasoning-pearl contribui

Pearl's L3 (contrafactual) requer que o sistema consiga responder "o que teria acontecido se X não tivesse ocorrido?" — o que exige construir um mundo counterfactual explícito. Para LLMs com referência já presente no contexto, essa operação é impossível: não há mecanismo interno para "desver" a referência e reconstituir julgamento autêntico.

Crucialmente, Pearl estabelece que **dados L1/L2 não podem responder perguntas L3**. "Treinar mais" ou "raciocinar mais" não resolve: é uma impossibilidade formal, não uma limitação de capacidade.

**Chave:** quando L3 é impossível internamente, a única saída é uma intervenção L2 no sistema externo — mudar *o que o agente vê* e *quando vê*.

### O que emerge da combinação

(⚠️ nossa interpretação) Reference-anchoring bias é, na linguagem de Pearl, um **failure de L3 induzido pela ordem de apresentação**. O judge não *consegue* fazer raciocínio contrafactual sobre a referência porque ela já está no contexto. Isso não é fraqueza do modelo — é uma impossibilidade arquitetural válida para qualquer sistema de raciocínio.

A implicação é o princípio **evaluation order independence**: para que julgamento seja epistemicamente válido, a referência deve chegar **depois** do julgamento independente formado — não antes. Isso transforma a ordem de apresentação em uma variável de design causal (L2), não uma questão de interface.

Formulação prática para protocolo /review e /verify:
1. Ler raw/ ou conteúdo candidato **sem contexto wiki**
2. Formar julgamento independente
3. Comparar com referência (wiki/concepts/*.md)

A sequência atual dos comandos da KB (Layer 1 → Layer 2 → Layer 3) é a sequência **invertida**: o LLM já está ancorado antes de ver a fonte primária.

## Especulação

- A magnitude do efeito de order dependence pode ser maior em Large Reasoning Models — a cadeia-de-raciocínio estendida dá mais oportunidade para rationalização da referência já vista (dados: DeepSeek-R1 −4.50% vs geral −1.66% sob ataque)
- O princípio pode generalizar além de LLM judges: qualquer processo de verificação onde o verificador vê o "gabarito" antes de avaliar de forma independente está sujeito à mesma impossibilidade L3
- Protocolo de inversão ("raw/ first") pode ser menos eficaz em artigos com alta interpretation_confidence (wiki já internalizou a fonte) vs artigos novos (wiki ainda é síntese fresca)

## Predição falsificável

**(L2, externa — confirmada empiricamente)** Se evaluation order é uma variável causal, então permutar a ordem de apresentação de candidatos — mantendo o conteúdo constante — deve produzir julgamentos inconsistentes com frequência mensurável. Shi et al. (2024) testaram exatamente isso via position-swapping protocol (do-operator explícito) em 150k+ instâncias.

**Resultado:** PC (Position Consistency) varia de 0.57 a 0.82 entre juízes, confirmando que ordem causa inconsistência. Pior nos casos de qualidade similar — exatamente onde o efeito de ancoragem seria máximo.

Referência externa: [Judging the Judges arXiv:2406.07791](../../raw/papers/judging-judges-position-bias-llm-2406.07791.md) — evidência L2 direta para evaluation order independence.

**Predição interna (testável na KB):** Um protocolo de /review que lê raw/ antes de wiki/ detecta mais conflitos entre wiki e fonte primária do que o protocolo atual (wiki/ antes de raw/). Teste: N≥5 artigos revisados com ambos os protocolos, contagem de discrepâncias detectadas.

## Verificação adversarial

**Pergunta falsificável:** Um protocolo de /review que lê raw/ antes de wiki/ produz discrepâncias detectáveis mais frequentemente do que o protocolo atual (wiki/ antes de raw/)?

**Evidência que confirmaria:** Em N revisões pareadas (mesmo artigo, protocolos invertidos), o protocolo "raw/ first" detecta mais conflitos entre wiki e fonte primária.

**Evidência que refutaria:** Nenhuma diferença na taxa de detecção de conflitos — o que indicaria que a anchoring bias é compensada por algum outro mecanismo, ou que os artigos da KB têm alta fidelidade à fonte independentemente de ordem.

## Conexões

- emerge-de: [[curse-of-knowledge-llm-judge]] ON "reference-anchoring bias degrada julgamento quando referência precede avaliação"
- emerge-de: [[causal-reasoning-pearl]] ON "L3 impossível internamente → única solução é intervenção L2 no design externo"
- instancia: [[autonomous-kb-failure-modes]] — Layer 3 Circularity Problem é uma instância de evaluation order dependence: wiki lida antes de raw/ ancora o revisor
- implica-em: [[autoresearch-reliability-triad]] — sequestro de referência é um safeguard adicional ao triad
- validates: [[position-bias-llm-judge]] ON "position-swapping protocol (L2) confirma empiricamente que ordem de apresentação é variável causal em julgamentos LLM"

## Fontes

- [[curse-of-knowledge-llm-judge]] — reference-anchoring bias: mecanismo empírico, dados quantitativos (DeepSeek-R1 −4.50%), cinco bias types
- [[causal-reasoning-pearl]] — ladder of causation: L3 impossibilidade formal, do-operator como única solução para L3 bloqueado
- [Log /ask](../../outputs/logs/sessions/2026-04-05/ask-curse-knowledge-pearl.md) — sessão que resolveu o SPLIT oracle e identificou evaluation-order-independence como conceito emergido

> ⚠️ QUARENTENA: artigo emergido de /ask cross-domain. Critérios pendentes: tempo (24h), review frio, adversarial.
