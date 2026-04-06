---
title: "Curse of Knowledge — LLM Judge Bias via Auxiliary Information"
sources:
  - path: raw/papers/curse-of-knowledge-llm-judge-bias.md
    type: paper
    quality: primary
    stance: challenging
created: 2026-04-05
updated: 2026-04-05
tags: [llm-judge, bias, evaluation, retrieval, reference-anchoring]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
provenance: source
---

## Resumo

Li et al. (EMNLP 2025) introduce ComplexEval, a benchmark that exposes how auxiliary information given to LLM judges — reference answers and evaluation rubrics — simultaneously improves baseline accuracy and introduces systematic biases. All tested models are susceptible; Large Reasoning Models (LRMs) are paradoxically more vulnerable than general models despite superior baseline performance. The core mechanism is reference-anchoring: when a model has the answer, it evaluates against the reference rather than independently.

## Conteúdo

### ComplexEval Benchmark

Two-tier design to quantify Auxiliary Information Induced Biases (AIIBs):

- **ComplexEval-Basic**: 1,056 samples, 12 domains, comprehensive adversarial attacks
- **ComplexEval-Advanced**: 400 samples, 3 domains (mathematics, creative writing, role-playing), targeted attacks

### Five Bias Types

**Reference-Based:**
1. **Format Bias** — overvaluing stylistic alignment with the reference over content quality
2. **Solution Fixation Bias** — penalizing semantically valid alternatives that differ from reference; QwQ-32B ASR 45%+
3. **Stereotype Amplification Bias** — reference material activates latent model stereotypes

**Rubric-Based:**
4. **Criteria Loophole Bias** — evaluation ignores dimensions absent from rubrics
5. **Criteria Entanglement Bias** — similar scores assigned across dimensions despite explicit weighting; Qwen2.5-32B ASR 29% on creative writing

### Key Numbers

| Model | Original → Attacked (reference-based) |
|-------|---------------------------------------|
| DeepSeek-V3 (general) | −1.66% |
| DeepSeek-R1 (reasoning) | −4.50% |
| General models average | ~−1% |

Reference answers improved accuracy on unattacked samples (e.g., DeepSeek-V3 +4.74%). Rubrics: mixed, −0.25% to +3.28%.

**Attention Limit Phenomenon:** In role-playing evaluation with 20 issues, models detected a maximum of ~15 regardless of actual count — a hard processing ceiling under multi-dimensional evaluation.

### Models Tested

Qwen2.5-32B / QwQ-32B, DeepSeek-V3 / DeepSeek-R1, GPT-4o-mini / o4-mini — six models across three general/reasoning pairs.

### The Paradox

Auxiliary information is beneficial on clean inputs and exploitable on perturbed inputs. Reasoning models (LRMs), despite higher baseline accuracy, show >4× greater decline under adversarial attacks — their extended chain-of-thought creates more opportunity to rationalize alignment with the reference.

## Interpretação

### Refinando o Layer 3 Circularity Problem

(⚠️ nossa interpretação) [[autonomous-kb-failure-modes]] descreve a "Layer 3 Circularity Problem": quando o mesmo LLM que escreveu o wiki lê raw/ para verificação, o que deveria ser feedback externo é na prática auto-reflexão. O artigo enquadra isso via Reflexion — self-reflection sem testes executáveis degrada a 52%.

ComplexEval nomeia o mecanismo específico de forma mais precisa: **reference-anchoring bias**. Quando o LLM tem a referência (o artigo wiki que ele mesmo escreveu), ele não avalia o texto de raw/ de forma independente — ele ancora na wiki existente e avalia raw/ contra ela. O processo parece verificação mas é confirmação.

Isso refina o Layer 3 Circularity de duas formas:

1. **Nomeação do mecanismo**: não é apenas "self-reflection" (termo de Reflexion, focado em falta de feedback externo) — é reference-anchoring bias (termo deste paper, focado em âncora ativa distorcendo o julgamento). Os dois mecanismos coexistem: o LLM tem feedback externo insuficiente E tem uma âncora que distorce o que vê.

2. **Escalamento com complexidade**: Li et al. mostram que bias magnitude aumenta com task complexity. Artigos wiki de síntese cross-paper (interpretação_confidence: low) são precisamente os mais complexos — exatamente onde o anchoring bias será maior.

### Implicação para /verify e /review

(⚠️ nossa interpretação) Um protocolo de verificação que passa a wiki como contexto ao LLM antes de ler raw/ está criando a condição de anchoring. A sequência correta seria: (1) ler raw/ sem contexto wiki, (2) gerar julgamento independente, (3) comparar com wiki. A sequência atual dos comandos (Layer 1 → Layer 2 → Layer 3) é a sequência invertida — o LLM já está ancorado antes de ver a fonte.

### Large Reasoning Models são Mais Vulneráveis

(⚠️ nossa interpretação) A vulnerabilidade aumentada dos LRMs tem implicação direta: se o KB migrar para usar um modelo de raciocínio como compilador (ex: DeepSeek-R1, o4), o anchoring durante /review será sistematicamente pior do que com modelos gerais, apesar da aparente superioridade de raciocínio. O maior risco não está nos modelos "menos capazes".

### Taxonomia de Biases como Checklist para /lint-epistemic

(⚠️ nossa interpretação) Os cinco bias types de ComplexEval mapeiam para failure modes detectáveis no /lint-epistemic:
- Solution Fixation ≈ confirming-source overweight
- Criteria Loophole ≈ gaps não declarados na seção Conteúdo
- Criteria Entanglement ≈ interpretation_confidence idêntico em artigos de complexidade muito diferente

## Conexões

- [[autonomous-kb-failure-modes]] — refina "Layer 3 Circularity Problem": o mecanismo é reference-anchoring bias, não apenas self-reflection; o anchoring é ativado pela sequência Layer 1→2→3 que passa wiki antes de raw/
- [[llm-as-judge]] — evidência empírica adicional de que judges com contexto auxiliar são sistematicamente biased; EMNLP 2025 com modelos recentes (DeepSeek-R1, QwQ-32B, o4-mini)
- [[autoresearch-reliability-triad]] — o triad identifica circularity como failure mode; este paper nomeia o mecanismo proximal
- [[self-improving-agents]] — Reflexion degradation (52%) e reference-anchoring bias são dois mecanismos distintos que convergem para o mesmo Layer 3 failure
- emerge-para: [[evaluation-order-independence]] ON "reference-anchoring bias degrada julgamento quando referência precede avaliação"

## Fontes

- [Curse of Knowledge — Li et al. 2025](../../raw/papers/curse-of-knowledge-llm-judge-bias.md) — ComplexEval benchmark, cinco bias types, dados quantitativos em seis modelos, achado central sobre LRMs sendo mais vulneráveis
