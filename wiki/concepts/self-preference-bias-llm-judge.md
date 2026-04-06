---
title: "Self-Preference Bias in LLM-as-a-Judge"
sources:
  - path: raw/papers/self-preference-bias-llm-judge.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-05
updated: 2026-04-05
tags: [evaluation, bias, llm-judge, self-preference, perplexity]
source_quality: high
interpretation_confidence: medium
resolved_patches:
  - date: 2026-04-05
    patch: "Claim 'mecanismo não é reconhecimento do próprio output' qualificado como hipótese forte do paper — prior work concorrente (Panickssery et al. 2404.13076) mostra self-recognition operacional em LLMs. Dois mecanismos podem coexistir."
    source: challenge post_ingest_hook
  - date: 2026-04-05
    patch: "Claim 'Um modelo pode exibir self-preference ao avaliar output de outro modelo se tiver baixa perplexidade' movido de §Conteúdo para §Interpretação com marcação ⚠️ — é inferência do compilador, não resultado empírico direto."
    source: challenge post_ingest_hook
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: true
quarantine_created: 2026-04-05
quarantine_reason: "novo ingest — aguarda review frio"
provenance: source
---

## Resumo

Wataoka et al. (NeurIPS 2024 Workshop / EMNLP 2025) introduzem uma métrica quantitativa para self-preference bias em LLM-as-a-Judge e identificam sua causa causal: LLMs preferem outputs com **menor perplexidade**, independentemente de quem os gerou. GPT-4 exibe bias score de 0.520 (Equal Opportunity metric). O mecanismo não é reconhecimento do próprio output, mas familiaridade distribucional — outputs do próprio modelo têm perplexidade intrinsecamente mais baixa.

## Conteúdo

### Mecanismo Causal: Perplexidade

A hipótese central, confirmada empiricamente: LLM evaluators atribuem avaliações mais altas a outputs com **perplexidade mais baixa**, e essa preferência existe independentemente de se o output foi auto-gerado.

**Por que outputs próprios têm menor perplexidade:** LLMs são treinados no pré-treino para minimizar perplexidade em grandes corpora e, durante RLHF/alinhamento, para minimizar perplexidade nos dados de diálogo. Textos de alta perplexidade são textos raramente vistos durante o treinamento. O output do próprio modelo, por construção, alinha-se com sua distribuição de treinamento — exibindo perplexidade intrinsecamente menor.

**Confirmação experimental (Figura 4):** Quando se compara o efeito de perplexidade em outputs self-generated vs. other-generated, as taxas de vitória são estatisticamente similares em todos os modelos testados (exceto dolly-v2 e stablelm). Conclusão: o fator determinante é a perplexidade, não a autoria do output.

**LLMs vs. humanos:** Todos os modelos testados (exceto dolly-v2 e stablelm) demonstram tendência de favorecer outputs de menor perplexidade mais fortemente do que humanos — especialmente vicuna-13b, vicuna-7b, koala-13b e oasst-pythia-12b.

### Métrica Quantitativa (Definition 4.1)

Adaptação do framework "Equal Opportunity" de fairness algorítmica:

**Bias = P(Y'=1|S=1,Y=1) − P(Y'=1|S=0,Y=1)**

- Y = índice da resposta preferida por humanos
- Y' = índice da resposta preferida pelo LLM evaluador
- S = indicador de se a resposta foi gerada pelo próprio evaluador
- Valor 0 = ausência de bias; valor ~1 = alto bias; valor ~−1 = bias reverso

Dataset: Chatbot Arena (33.000 diálogos). Position bias mitigado por position-swapping.

### Resultados por Modelo

| Modelo | Equal Opportunity | Demographic Parity |
|--------|------------------|--------------------|
| GPT-4 | 0.520 | 0.749 |
| Vicuna-13b | significativo | 0.382 |
| GPT-3.5-Turbo | moderado | 0.191 |
| Koala-13b | significativo | 0.175 |
| Vicuna-7b | ~0 | 0.052 |
| oasst-pythia-12b | ~0 | 0.006 |
| dolly-v2-12b | negativo | −0.069 |
| stablelm-tuned-alpha-7b | negativo | −0.032 |

GPT-4 confusion matrix: true positive rate 0.945 vs. true negative rate 0.425 ao avaliar próprios outputs — diferença de 0.520.

### Distinção dos Outros Biases Documentados

| Bias | Mecanismo | Tipo |
|------|-----------|------|
| Self-preference (este paper) | Perplexidade — familiaridade distribucional | Training dynamics |
| Self-enhancement (CALM) | Preferência geral por próprios outputs — até 16.1% erro | Output authorship |
| Position bias | Preferência por posição na prompt | Structural |
| Verbosity bias | Preferência por respostas mais longas | Structural |

**Distinção crítica em relação a CALM:** O CALM Framework documenta "self-enhancement" como preferência pelos próprios outputs, mas não especifica o mecanismo causal. Este paper propõe que o mecanismo principal é a perplexidade: Wataoka et al. mostram empiricamente (Figura 4) que taxas de vitória são similares para outputs self-generated vs. other-generated quando controlado por perplexidade — sugerindo que perplexidade é suficiente para explicar o padrão.

**Caveat (prior work concorrente):** Panickssery et al. (2404.13076, NeurIPS 2024) demonstram que LLMs têm capacidade de self-recognition não-trivial (GPT-4: 73.5% de accuracy) e encontram correlação linear entre self-recognition e intensidade do self-preference bias. Os dois mecanismos — perplexidade e reconhecimento de autoria — podem coexistir; Wataoka et al. mostram perplexidade como mecanismo suficiente, não necessariamente único.

### Mitigação Proposta

Ensemble evaluation com múltiplos modelos: diminuir o peso da avaliação de um modelo para amostras onde ele exibe baixa perplexidade. A métrica proposta permite quantificar a eficácia de estratégias de redução. Sem validação empírica de mitigação no paper.

## Interpretação

### Self-Preference como Mecanismo do Oracle Circular

(⚠️ nossa interpretação) [[autonomous-kb-failure-modes]] descreve o "Layer 3 Circularity Problem": o mesmo LLM que escreve o wiki o avalia durante /review. Este paper fornece o mecanismo causal preciso: ao gerar os artigos wiki, o LLM produz texto alinhado com sua própria distribuição de treinamento — portanto, com perplexidade intrinsecamente menor. Quando avalia esses artigos, o bias de perplexidade o leva a privilegiá-los sobre fontes raw/ que, frequentemente, foram escritas por humanos ou outros modelos.

O oracle circular não é apenas auto-reflexão (como descrito em Reflexion) nem apenas reference-anchoring (como descrito em ComplexEval/curse-of-knowledge) — é também **familiaridade distribucional**: o evaluador pontua mais alto o que foi escrito por ele porque esse texto tem menor perplexidade.

### Cross-Model Perplexity Self-Preference

(⚠️ nossa interpretação) Uma implicação inferida do mecanismo de perplexidade: um modelo pode exibir self-preference ao avaliar output de *outro* modelo se esse output tiver baixa perplexidade para o evaluador — independentemente de autoria. Esta inferência não foi testada diretamente por Wataoka et al.; é uma extrapolação lógica do mecanismo proposto.

### Refinamento da Hierarquia de Evidências

(⚠️ nossa interpretação) A distinção self-preference (perplexidade) vs. self-enhancement (autoria) tem implicação para o /oracle cross-model: usar um modelo diferente do compilador reduz self-enhancement bias (CALM), mas não elimina o perplexity-based self-preference se os dois modelos tiverem distribuições de treinamento similares (ex: dois modelos GPT-family). Modelos de famílias distintas seriam oráculo mais robusto. Nota: se o mecanismo de Panickssery et al. também operar (self-recognition), a troca de modelo elimina ambos os mecanismos; se os mecanismos coexistirem, o efeito de troca de modelo pode ser maior do que Wataoka et al. sozinhos sugerem.

### Complementaridade com Position Bias

(⚠️ nossa interpretação) [[position-bias-llm-judge]] documenta PC=0.57–0.82 como efeito causal via do-operator. Self-preference bias (0.520 Equal Opportunity para GPT-4) opera em magnitude similar e em dimensão ortogonal. Em avaliações pairwise de artigos wiki, os dois biases se compõem: artigos do compilador tendem a ter menor perplexidade E podem estar em posições favoráveis no _index.md.

## Conexões

- [[llm-as-judge]] — fornece mecanismo causal para self-enhancement (bias #1 do CALM Framework); distingue authorship-based vs. perplexity-based explanation
- [[autonomous-kb-failure-modes]] — mecanismo causal do Layer 3 Circularity: wiki tem menor perplexidade para o compilador → evaluador privilegia wiki sobre raw/
- [[curse-of-knowledge-llm-judge]] — reference-anchoring bias (ComplexEval) e perplexity-based self-preference são dois mecanismos distintos que convergem para o mesmo failure mode em /review
- [[position-bias-llm-judge]] — bias em dimensão ortogonal, magnitude similar (PC≈0.57–0.82 vs. EOpp=0.520); se compõem em pairwise evaluation
- [[causal-reasoning-pearl]] — este paper sobe de L1 (self-preference existe) para L2 (perplexidade causa self-preference via treinamento); o do-operator relevante seria: intervir em perplexidade → medir mudança no score

## Fontes

- [Self-Preference Bias in LLM-as-a-Judge](../../raw/papers/self-preference-bias-llm-judge.md) — métrica quantitativa (Equal Opportunity adaptation), 8 modelos testados, mecanismo causal via perplexidade, GPT-4 bias score 0.520

### Prior Work Não Ingerido (identificado no challenge)

- Panickssery et al. 2404.13076 (NeurIPS 2024) — "LLM Evaluators Recognize and Favor Their Own Generations" — evidência concorrente: GPT-4 self-recognition 73.5%, correlação linear self-recognition × self-preference bias
- Stureborg et al. 2405.01724 (2024) — "Large Language Models are Inconsistent and Biased Evaluators" — confirma familiarity/perplexidade bias de forma independente no dataset SummEval
