---
title: "KalshiBench: Evaluating Epistemic Calibration of LLMs via Prediction Markets"
arxiv: "2512.16030"
year: 2025
type: paper
quality: primary
created: 2026-04-07
---

# KalshiBench: Evaluating Epistemic Calibration of LLMs via Prediction Markets

**Referência:** arXiv:2512.16030 (2025)

## Resumo do Paper

KalshiBench é um benchmark de calibração epistêmica que usa questões de mercados de predição (Kalshi) como ground truth verificável para avaliar se LLMs "sabem o que não sabem". O paper documenta sobreconfiança sistemática em todos os frontier models testados, com reasoning-enhanced models apresentando pior calibração apesar de accuracy comparável.

## Metodologia

### Dataset

- **300 questões** extraídas do mercado de predição Kalshi
- Questões com outcomes verificáveis (eventos passados com resolução binária)
- Cobertura de domínios: política, economia, esportes, eventos climáticos, mercados financeiros
- Formato: questão + data de resolução + outcome ground truth

### Por que Prediction Markets como Ground Truth

- Mercados de predição oferecem outcomes binários verificáveis (sim/não)
- Questões têm datas de resolução explícitas — elimina ambiguidade temporal
- Preços de mercado refletem probabilidades agregadas por crowd com incentivo financeiro
- Permite comparar calibração do modelo vs. calibração do mercado como baseline

### Protocolo de Avaliação

- Modelos respondem questões com probabilidade numérica (0.0–1.0)
- Calibração medida por Expected Calibration Error (ECE) e Brier score
- Overconfidence gap = mean_confidence − accuracy observada
- Accuracy medida como % predições corretas (probabilidade > 0.5 vs. outcome)

## Métricas Usadas

| Métrica | Definição |
|---------|-----------|
| **ECE** (Expected Calibration Error) | Diferença entre confiança declarada e accuracy observada por bin de confiança |
| **Brier Score** | Quadratic scoring rule: Σ(p_i − o_i)² / N; 0 = perfeito, 1 = pior |
| **BSS** (Brier Skill Score) | Brier score normalizado vs. baseline climatológico |
| **Accuracy** | % de predições binárias corretas (threshold 0.5) |
| **Mean Confidence** | Probabilidade média declarada pelo modelo |
| **Overconfidence Gap** | mean_confidence − accuracy observada |

## Achados Principais

### Sobreconfiança Sistemática

- **Todos os frontier models testados apresentam overconfidence sistemático** — nenhum modelo está bem-calibrado em questões de predição de eventos reais
- Modelos tipicamente declaram confiança de ~0.7–0.8 em questões onde accuracy observada é ~0.55–0.65
- O overconfidence gap varia por modelo mas é consistentemente positivo (nunca negativo em média)

### Ranking de Calibração

- **Claude Opus 4.5** apresentou melhor calibração (menor ECE) entre os modelos testados
- Melhor calibração não significa ausência de erros — erros substanciais persistem mesmo no modelo mais calibrado
- Claude Opus 4.5 ainda exibe overconfidence, apenas em menor grau comparado aos demais

### Reasoning-Enhanced Models: Pior Calibração

- **GPT-5.2** (reasoning-enhanced) apresentou pior calibração (ECE mais alto) apesar de accuracy comparável ou superior
- Padrão observado: raciocínio estendido → aumento de confiança declarada sem aumento proporcional de accuracy
- Este é o achado mais contraintuitivo do paper: "pensar mais" não implica "saber melhor o quanto sabe"
- Hipótese dos autores: chain-of-thought pode ancorar o modelo em raciocínios que aumentam a confiança subjetiva sem base empírica adequada

### ECE por Domínio

- Domínios com maior ECE: política, geopolítica (eventos mais imprevisíveis)
- Domínios com menor ECE: eventos com base estatística clara (resultados esportivos, dados econômicos recorrentes)
- Calibração intra-domínio varia mais do que calibração inter-modelo para certos domínios

## Implicações

### Para Design de Sistemas LLM

- Calibração é propriedade distinta de accuracy — modelos podem ser precisos mas mal-calibrados
- Não assume que modelos maiores ou mais capazes de raciocinar são mais confiáveis em termos de confiança declarada
- Sistemas que dependem de probabilidades declaradas por LLMs devem incluir mecanismo de calibração pós-hoc (temperature scaling, Platt scaling)

### Para Avaliação de Modelos

- Benchmarks de accuracy não capturam degradação de calibração em modelos com reasoning-enhancement
- ECE e Brier score devem ser métricas padrão junto com accuracy em avaliações de frontier models
- Prediction markets como fonte de ground truth verificável é metodologia replicável

### Para Epistemic AI

- O paper evidencia que sobreconfiança é emergente da arquitetura/treinamento, não apenas da ausência de informação
- Implicação: dar mais contexto ao modelo pode aumentar accuracy sem melhorar (ou piorando) calibração
- Abstention honesta ("não sei") é comportamento subrepresentado em todos os modelos testados

## Limitações

- 300 questões é dataset relativamente pequeno para conclusões robustas por domínio
- Foco em questões binárias — calibração em espaços de probabilidade mais ricos pode diferir
- Resultados dependem de como o modelo é promovido a declarar probabilidade (prompt engineering afeta ECE)
- Janela temporal das questões não especificada em detalhe — possível viés por recência

## Conexão com Literatura

- Conecta-se a literatura de calibration em NLP (Guo et al. 2017 — temperature scaling)
- Relaciona-se a trabalhos sobre overconfidence em LLMs (Kadavath et al. 2022 — "I Know" benchmark)
- Prediction markets como ground truth: abordagem distinta de benchmarks sintéticos
