---
title: "KalshiBench-T0-RAG — Calibração Epistêmica sob Contexto Temporalmente Congelado"
created: 2026-04-07
updated: 2026-04-07
tags: [strategy, calibration, epistemic, retrieval, forecasting, benchmark, conjecture]
source_quality: low
interpretation_confidence: low
provenance: conjecture
epistemic_status: hypothesis
testable_prediction: "Braço C (T0-context + challenge pipeline) reduz ECE e overconfidence_gap comparado ao Braço A (baseline sem contexto), com abstention_rate aumentada nos casos difíceis. Falsificador: se Braço B (T0-context sem challenge) tiver ECE ≤ Braço C, o challenge não adiciona valor de calibração."
conjecture_trigger:
  session: outputs/logs/sessions/2026-04-07/foresight-kalshib.md
  context: "KalshiBench (arXiv:2512.16030) mostra sobreconfiança sistemática em todos os frontier models em predições de mercado. Pipeline de challenge adversarial desta KB pode ser testado como mecanismo de calibração."
conjectured_on: 2026-04-07
lifecycle_state: active
---

## Resumo

Um harness de retrieval-and-challenge com contexto de domínio temporalmente congelado (T0) melhora calibração epistêmica (ECE/Brier score) mais do que melhora accuracy, e reduz overconfidence sem vazar informação futura. O pipeline de challenge adversarial reduz sobreconfiança mesmo quando não aumenta muito accuracy. A distinção entre "saber mais" e "fingir saber demais" é mensurável via ECE.

## Conteúdo

### Hipótese Central

Um harness RAG com restrição temporal T0 (nenhuma fonte com published_at > t0) melhora calibração epistêmica de forma assimétrica: reduz overconfidence mais do que aumenta accuracy. O componente de challenge adversarial contribui especificamente para a dimensão de calibração, não apenas para accuracy.

### Premissas

- LLMs são sistematicamente sobreconfiantes — KalshiBench (arXiv:2512.16030) documenta esse padrão em todos os frontier models testados em predições de mercado Kalshi
- Contexto de domínio pode melhorar accuracy sem necessariamente melhorar calibração
- Challenge adversarial pode reduzir overconfidence especificamente (não só accuracy)
- A distinção entre "saber mais" e "fingir saber demais" é mensurável via ECE e Brier score

### Protocolo de 3 Braços

**Braço A — Baseline**
Modelo sem ingestão extra. Responde questões de previsão sem contexto adicional. Estabelece linha de base para accuracy, ECE, Brier score e mean_confidence.

**Braço B — T0-Context**
Para cada questão Q com data de resolução t_r, define t0 = data em que a previsão poderia ser feita. Ingere somente material publicado até t0. Proíbe qualquer fonte com resultado ou fatos posteriores a t0. Sem challenge pipeline.

**Braço C — T0-Context + Challenge**
Igual ao Braço B, mas com oracle agreement + adversarial challenge + mecanismo de abstention/redução de confiança. O challenge visa especificamente reduzir sobreconfiança nos casos em que o modelo mantém alta confiança sem suporte adequado nas fontes T0.

### Hipóteses Internas

- **H1:** T0-context melhora accuracy mais do que calibração (ECE piora ou estagna com Braço B vs A)
- **H2:** T0-context + challenge melhora calibração mais do que T0-context sozinho (Braço C ECE < Braço B ECE)
- **H3:** O harness reduz sobreconfiança mesmo sem aumentar muito accuracy (overconfidence_gap↓ sem accuracy↑ significativo)
- **H4:** Certos domínios melhoram muito com ingestão (mercados financeiros, geopolítica) enquanto outros quase nada (eventos de baixo contexto documental)

### Métricas

| Métrica | Definição | Papel |
|---------|-----------|-------|
| accuracy | % predições corretas | Baseline de qualidade |
| ECE | Expected Calibration Error | Métrica primária de calibração |
| Brier score / BSS | Quadratic scoring rule | Métrica composta (accuracy × calibração) |
| mean_confidence | Confiança média declarada | Componente do gap |
| abstention_rate | % de questões com "não sei" | Sinal de saúde epistêmica |
| overconfidence_gap | mean_confidence − accuracy observada | Medida direta de overconfidence |

### Critério de Sucesso (Falsificador Explícito)

**Confirmação:** ECE(Braço C) < ECE(Braço A) E overconfidence_gap(Braço C) < overconfidence_gap(Braço A)

**Falsificador primário:** ECE(Braço B) ≤ ECE(Braço C) — se verdadeiro, o challenge não adiciona valor de calibração além do contexto T0 sozinho

**Falsificador secundário:** accuracy(Braço C) >> accuracy(Braço A) sem redução proporcional de ECE — significaria que o harness apenas "sabe mais" sem "calibrar melhor"

### Regras Anti-Leakage (Obrigatórias)

O harness pode saber o contexto; não pode saber o futuro disfarçado de contexto.

1. Toda fonte precisa ter `published_at <= t0`
2. Nada de páginas atualizadas depois sem histórico confiável (wayback machine ou snapshot local)
3. Nada de resumos retrospectivos (ex: "em retrospecto, a crise de X...")
4. Nada de datasets recompilados após o evento (ex: dados econômicos com revisões post-hoc)
5. Log de proveniência por questão com URL, timestamp e hash/snapshot local
6. Fontes com `published_at` ausente ou incerto → excluir por default (conservador)

### Log Format por Questão

```json
{
  "question_id": "kalshi_001",
  "t0": "2025-03-01T12:00:00Z",
  "arm": "T0-context-challenge",
  "prediction": 0.64,
  "final_prediction": 0.58,
  "outcome": 1,
  "correct": true,
  "ece_bin": "0.5-0.6",
  "sources": [
    {
      "url": "...",
      "published_at": "2025-02-15T00:00:00Z",
      "snapshot_id": "sha256:abc123"
    }
  ],
  "challenge_applied": true,
  "oracle_agreement": false,
  "abstained": false,
  "notes": "confidence reduced after adversarial review"
}
```

### Frase-Síntese para README

"We evaluate epistemic calibration under temporally frozen domain context, measuring whether a retrieval-and-challenge harness reduces overconfidence without leaking future information."

## Interpretação

(⚠️ nossa interpretação) Se H2 e H3 forem confirmadas simultaneamente, isso sugere que o pipeline de challenge adversarial desta KB tem utilidade além do contexto de compilação de conhecimento — funciona como mecanismo de calibração transferível para tasks de predição. Isso transformaria o /challenge de ferramenta editorial em componente de epistemologia aplicada.

(⚠️ nossa interpretação) A assimetria esperada (calibração melhora mais que accuracy) seria evidência de que overconfidence em LLMs não é primariamente um problema de "não ter a informação" mas de "não saber o quanto não sabe" — o que é um claim mais forte sobre a natureza do erro epistêmico em modelos de linguagem.

(⚠️ nossa interpretação) Braço C testa empiricamente a Propriedade 6 do [[metaxon-federation-protocol]] (calibração ≠ concordância): o challenge deve reduzir confiança sem necessariamente mudar a direção da predição.

### Consequências Arquiteturais se Confirmado

1. **Campo `published_at` obrigatório** em toda source do frontmatter — anti-leakage validation automatizável
2. **Log format por questão** como extensão do pipeline de /ingest para tasks de predição
3. **Métricas ECE + Brier** como critérios complementares em /auto-promote — artigos sobre tópicos onde o modelo tem ECE alta devem ter source_quality penalizado
4. **Abstention honesta** ("não sei") tratada como sinal de saúde, não de falha — mudar threshold de /ask para preferir abstention em baixa confiança

## Conexões

- [[epistemic-necessity-tool-use]] — Theory of Agent (ToA); overacting/overthinking como miscalibração; trajetória da inteligência via raciocínio interno. T0-RAG é caso de uso de "não usar o que não deve ser usado"
- [[lem-summa-technologiae]] — fantomática como risco do modelo superar o território; T0-RAG como mecanismo anti-fantomática via restrição temporal
- [[metaxon-federation-protocol]] — Propriedade 6 (calibração ≠ concordância); Braço C testa exatamente este claim no contexto de predições
- [[noogon-identity]] — Braço C testa o que METAXON afirma ser: compilador que sabe o que não sabe
- [[falsificationism-demarcation]] — Esta hipótese tem falsificador explícito; estrutura Popperiana intencional
- [[heuristics-and-biases]] — K&T: ancoragem + overconfidence como mecanismos; o harness como intervenção nos bias sistemáticos
- [[curation-anti-bias]] — as regras anti-leakage são instância de curation-anti-bias aplicado a tasks de predição

## Fontes

- [KalshiBench arXiv:2512.16030](../../raw/) — benchmark de calibração em predições de mercado; documenta overconfidence sistemática em frontier models. (Fonte não ingerida ainda — candidata a /ingest)
