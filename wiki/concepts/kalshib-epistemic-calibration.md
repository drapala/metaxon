---
title: "KalshiBench — Epistemic Calibration em LLMs via Prediction Markets"
sources:
  - path: raw/papers/kalshib-epistemic-calibration.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-07
updated: 2026-04-07
tags: [calibration, epistemic, benchmark, prediction-markets, overconfidence, llm-evaluation]
source_quality: high
interpretation_confidence: medium
resolved_patches: []
provenance: source
quarantine: true
---

## Resumo

KalshiBench avalia calibração epistêmica de frontier LLMs usando 300 questões de mercados de predição Kalshi com outcomes verificáveis. Achado central: sobreconfiança sistemática em todos os modelos testados, com Claude Opus 4.5 como melhor calibrado mas ainda com erros substanciais. Resultado mais contraintuitivo: reasoning-enhanced models (GPT-5.2) exibem pior calibração apesar de accuracy comparável.

## Conteúdo

### Dataset e Metodologia

KalshiBench consiste em **300 questões** extraídas de mercados de predição Kalshi — plataforma de prediction markets com outcomes binários verificáveis. Questões cobrem domínios como política, economia, esportes e eventos climáticos. Cada questão tem data de resolução explícita e outcome ground truth (sim/não).

A escolha de prediction markets como ground truth é metodologicamente relevante: os outcomes são verificáveis objetivamente, as questões têm datas de resolução explícitas, e os preços de mercado fornecem uma baseline de calibração "humana agregada com incentivo financeiro".

Protocolo: modelos respondem questões com probabilidade numérica (0.0–1.0). Calibração medida por ECE, Brier score, e overconfidence gap.

### Métricas

| Métrica | Definição | Papel |
|---------|-----------|-------|
| **ECE** | Diferença entre confiança declarada e accuracy observada por bin | Métrica primária de calibração |
| **Brier Score** | Σ(p_i − o_i)² / N; 0=perfeito, 1=pior | Métrica composta |
| **BSS** | Brier score normalizado vs. baseline | Comparação relativa |
| **Accuracy** | % predições corretas (threshold 0.5) | Baseline de qualidade |
| **Mean Confidence** | Probabilidade média declarada | Componente do gap |
| **Overconfidence Gap** | mean_confidence − accuracy observada | Medida direta de overconfidence |

### Achados Principais

**Sobreconfiança sistemática universal:** Todos os frontier models testados exibem overconfidence positivo — nenhum modelo está bem-calibrado. Modelos tipicamente declaram confiança de ~0.7–0.8 onde accuracy observada é ~0.55–0.65.

**Ranking de calibração:** Claude Opus 4.5 apresentou melhor calibração (menor ECE) entre os modelos testados. Entretanto, melhor calibração não elimina erros substanciais — o modelo mais calibrado ainda erra significativamente.

**Paradoxo reasoning-enhanced:** GPT-5.2 (reasoning-enhanced) apresentou pior calibração (ECE mais alto) apesar de accuracy comparável ou superior. O padrão observado é: raciocínio estendido → aumento de confiança declarada sem aumento proporcional de accuracy. Hipótese dos autores: chain-of-thought ancora o modelo em raciocínios que aumentam confiança subjetiva sem base empírica adequada.

**Variação por domínio:** Domínios com maior ECE: política e geopolítica. Menor ECE: eventos com base estatística recorrente (resultados esportivos, dados econômicos).

### Implicações Arquiteturais

- Calibração é propriedade distinta de accuracy — benchmarks de accuracy não capturam degradação de calibração
- Sistemas dependentes de probabilidades declaradas por LLMs precisam de calibração pós-hoc (temperature scaling)
- ECE e Brier score devem ser métricas padrão junto com accuracy
- Abstention honesta ("não sei") é comportamento subrepresentado em todos os modelos

## Interpretação

(⚠️ nossa interpretação) O achado sobre reasoning-enhanced models é o mais relevante para design de sistemas autônomos: mais capacidade de raciocínio não implica mais consciência do próprio erro. Um sistema com chain-of-thought estendido pode sistematicamente construir justificativas que aumentam sua confiança sem aumentar sua acurácia — o que é pior do que incerteza declarada.

(⚠️ nossa interpretação) Para o pipeline desta KB, o paper fornece evidência empírica direta de que o problema de sobreconfiança que [[kalshib-t0-rag]] pretende endereçar existe e é mensurável. A existência do benchmark KalshiBench também oferece uma instância de evaluation framework que o experimento T0-RAG pode reutilizar metodologicamente.

(⚠️ nossa interpretação) A comparação Claude Opus 4.5 vs. GPT-5.2 em calibração (melhor calibração ≠ melhor reasoning) sugere que design choices de treinamento afetam calibração independentemente de capacidade cognitiva. Isso implica que calibração pode ser uma dimensão de avaliação de pipeline distinta da avaliação de accuracy — o que se alinha com o design de dois eixos (source_quality + interpretation_confidence) desta KB.

(⚠️ nossa interpretação) O paper evidencia que overconfidence em LLMs é emergente da arquitetura/treinamento, não apenas da ausência de informação. Isso é relevante para [[autonomous-kb-failure-modes]]: um agente que "sabe mais" (após ingestão) pode se tornar mais confiante sem se tornar melhor calibrado — o que é exatamente o failure mode de sobreconfiança documentado em sistemas autônomos.

## Conexões

- [[kalshib-t0-rag]] — conjecture que usa KalshiBench como benchmark de validação para pipeline T0-RAG; este artigo fornece a fonte primária que fundamenta as premissas do experimento
- [[epistemic-necessity-tool-use]] — Theory of Agent (ToA): overacting/overthinking como miscalibração; KalshiBench documenta empiricamente este padrão em reasoning-enhanced models
- [[autonomous-kb-failure-modes]] — sobreconfiança como failure mode central; KalshiBench fornece evidência empírica quantificada com ECE/Brier
- [[metaxon-federation-protocol]] — Propriedade 6 (calibração ≠ concordância); KalshiBench mede a distinção empiricamente: modelos podem concordar em predições incorretas com alta confiança

## Fontes

- [KalshiBench arXiv:2512.16030](../../raw/papers/kalshib-epistemic-calibration.md) — paper primário; benchmark de 300 questões de prediction markets; documenta overconfidence sistemática em frontier models e paradoxo de calibração em reasoning-enhanced models
