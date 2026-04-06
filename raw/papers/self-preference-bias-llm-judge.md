---
source: https://arxiv.org/abs/2410.21819
authors: [Koki Wataoka, Tsubasa Takahashi, Ryokan Ri]
affiliation: SB Intuitions
date: 2024-10-29
venue: NeurIPS 2024 Safe Generative AI Workshop; EMNLP 2025
type: paper
arxiv: "2410.21819"
---

# Self-Preference Bias in LLM-as-a-Judge

## Abstract

Automated evaluation leveraging large language models (LLMs), commonly referred to as LLM evaluators or LLM-as-a-judge, has been widely used in measuring the performance of dialogue systems. However, the self-preference bias in LLMs has posed significant risks, including promoting specific styles or policies intrinsic to the LLMs. Despite the importance of this issue, there is a lack of established methods to measure the self-preference bias quantitatively, and its underlying causes are poorly understood. In this paper, we introduce a novel quantitative metric to measure the self-preference bias. Our experimental results demonstrate that GPT-4 exhibits a significant degree of self-preference bias. To explore the causes, we hypothesize that LLMs may favor outputs that are more familiar to them, as indicated by lower perplexity. We analyze the relationship between LLM evaluations and the perplexities of outputs. Our findings reveal that LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated. This suggests that the essence of the bias lies in perplexity and that the self-preference bias exists because LLMs prefer texts more familiar to them.

## Mecanismo Central: Perplexidade como Causa Causal

A hipótese central é que LLM evaluators preferem outputs com **perplexidade mais baixa**, independentemente de quem gerou o output.

### Por que perplexidade importa

LLMs são treinados durante o pré-treino para reduzir perplexidade em grandes corpora. Durante RLHF/alinhamento, também minimizam perplexidade no diálogo de treinamento. Textos de alta perplexidade são textos que o modelo raramente encontrou durante o treinamento.

Consequência: outputs gerados pelo próprio modelo têm perplexidade intrinsecamente menor (Figura 5: confirmado em todos os modelos testados — a perplexidade média é menor para respostas geradas pelo próprio evaluador).

### O bias não é sobre reconhecimento do próprio output

Experimentos da Figura 4 mostram que quando se compara o efeito de perplexidade em outputs self-generated vs. other-generated, as taxas de vitória são similares em todos os modelos (exceto dolly-v2 e stablelm). Conclusão: "o fator que influencia o julgamento não é se a resposta é própria, mas a perplexidade das respostas."

## Métrica Quantitativa (Definition 4.1)

Adaptação do framework "Equal Opportunity" de fairness algorítmica:

**Bias = P(Y'=1|S=1,Y=1) − P(Y'=1|S=0,Y=1)**

- Y = índice da resposta preferida por humanos (0 ou 1)
- Y' = índice da resposta preferida pelo evaluador LLM
- S = indicador de se a resposta foi auto-gerada pelo evaluador

Valor 0 = ausência de bias. Valor próximo de 1 = alto grau de bias. Valor −1 = bias reverso.

Implementação: pairwise evaluation no dataset Chatbot Arena (33.000 diálogos). Position bias mitigado por swapping de posições + média.

## Resultados Empíricos

### Self-Preference Bias Scores (Equal Opportunity metric, Figura 1b)

| Modelo | Bias Score |
|--------|-----------|
| GPT-4 | 0.520 |
| Vicuna-13b | significativo |
| Koala-13b | significativo |
| GPT-3.5-Turbo | moderado |
| Vicuna-7b | ~0 |
| oasst-pythia-12b | ~0 |
| dolly-v2-12b | negativo (bias reverso) |
| stablelm-tuned-alpha-7b | negativo (bias reverso) |

### Demographic Parity Metric (Tabela 2)

| Modelo | Score |
|--------|-------|
| GPT-4 | 0.749 |
| Vicuna-13b | 0.382 |
| GPT-3.5-Turbo | 0.191 |
| Koala-13b | 0.175 |
| Vicuna-7b | 0.052 |
| oasst-pythia-12b | 0.006 |
| dolly-v2-12b | −0.069 |
| stablelm-tuned-alpha-7b | −0.032 |

### Confusion Matrix para GPT-4 (Figura 2)

Avaliando próprios outputs:
- True positive rate: 0.945 ≈ 1852/(108+1852)
- True negative rate: 0.425 ≈ 118/(160+118)
- Diferença: 0.520

### Efeito de Perplexidade vs. Humanos

Todos os modelos testados (exceto dolly-v2 e stablelm) demonstram tendência clara de atribuir avaliações mais altas a respostas com menor perplexidade. Essa tendência é **mais forte nos LLMs do que em humanos** — especialmente em vicuna-13b, vicuna-7b, koala-13b e oasst-pythia-12b.

Modelos adicionais testados para análise de perplexidade: Llama 2 e Llama 3.

## Distinção de Outros Biases

O paper distingue self-preference bias de:
- **Position bias**: preferência por respostas em posições específicas — estrutural, mitigável por reordenação
- **Verbosity bias**: preferência por respostas mais longas — estrutural, identificado por Saito et al. (2023)
- **Self-preference bias (este paper)**: opera via preferência por textos com menor perplexidade, refletindo dinâmicas de treinamento; independente de reconhecimento explícito da fonte

Trabalhos anteriores identificaram o fenômeno mas careciam de: (1) métricas confiáveis para quantificar e (2) explicação da causa fundamental. Este paper preenche ambas as lacunas.

## Mitigação Proposta

Os autores propõem **ensemble evaluation com múltiplos modelos**: quando um modelo exibe baixa perplexidade em uma amostra, diminuir o peso da avaliação desse modelo para aquela amostra. A métrica proposta pode ser utilizada para avaliar a eficácia de estratégias de redução de bias.

Nenhuma validação empírica de mitigação é fornecida no paper — foco em problem identification.
