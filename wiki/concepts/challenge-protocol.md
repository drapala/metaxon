---
title: "Challenge Protocol — REFINA Sub-tipos e Auto-trigger"
sources:
  - path: wiki/concepts/sequential-hypothesis-testing.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autonomous-kb-failure-modes.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autoresearch-programme-vitality.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [meta-kb, challenge, protocol, SPRT, prior-work, auto-trigger]
source_quality: medium
interpretation_confidence: low
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: synthesis
synthesis_sources:
  - wiki/concepts/sequential-hypothesis-testing.md
  - wiki/concepts/autonomous-kb-failure-modes.md
  - wiki/concepts/autoresearch-programme-vitality.md
quarantine: true
quarantine_created: 2026-04-05
quarantine_reason: "Artigo de síntese derivado de /ask — sem fonte raw/ externa. Aguarda validação adversarial e fonte primária (arXiv:2602.16078 ou similar para seção auto-trigger)."
quarantine_criteria_met:
  tempo: false
  review_frio: false
  adversarial_or_scout_or_prediction: false
---

## Resumo

O /challenge classifica prior work como INVALIDA / REFINA / CONFIRMA, mas "REFINA" colapsa sub-tipos com valores epistêmicos e riscos de auto-trigger muito distintos. Esta taxonomia operacional distingue 4 sub-tipos de REFINA derivados de /ask sobre segurança de auto-trigger, e propõe um critério de auto-trigger seguro que Bradford gate não cobre.

## Conteúdo

### O problema: REFINA não é uniforme

O SPRT chain control atual trata REFINA como atômico: todo prior work REFINA vai para `ingest_queue` com `auto_trigger: false`. Isso é conservador e correto como default — mas ignora que um paper que âncora empiricamente um claim especulativo (interpretation_confidence: low → medium) tem valor epistêmico fundamentalmente diferente de um paper que adiciona um caveat a um número já qualificado.

Bradford gate não cobre os riscos de REFINA auto-trigger porque:
1. Bradford opera no eixo `challenging/non-challenging`. REFINA papers são quase sempre `neutral` ou `confirming`.
2. Bradford não limita crescimento quantitativo — apenas ratio de stance.
3. Bradford não tem stopping criterion para chains de refinamento.

O risco real de REFINA auto-trigger não é Bradford — é FM3 (index bloat) + FM1 (confirming bias acceleration) de [[autonomous-kb-failure-modes]].

### Taxonomia de REFINA sub-tipos

| Sub-tipo | Definição | Efeito no frontmatter | Valor para auto-trigger |
|----------|-----------|----------------------|------------------------|
| **marginal** | Adiciona caveat ou nuance a um número já qualificado; não muda a interpretação central | Nenhuma mudança em source_quality ou interpretation_confidence | Baixo → queue sem trigger |
| **empírica** | Âncora claim especulativo em dados empíricos primários | `source_quality: medium → high` ou `interpretation_confidence: low → medium` | Alto → candidato a auto-trigger |
| **scope** | Delimita condições de validade de um claim ("funciona em contexto X, não em Y") | Possível mudança em `interpretation_confidence` | Médio → queue prioritária |
| **causal** | Adiciona mecanismo que explica por que o claim funciona (de correlação para causalidade) | Possível mudança em `interpretation_confidence` | Médio-alto |

**Como classificar automaticamente:** o /challenge já identifica qual claim está sendo refinado. Para determinar o sub-tipo sem LLM call adicional, verificar se o paper muda algum campo de qualidade do artigo:
- Se nenhuma mudança em `source_quality` ou `interpretation_confidence` → marginal
- Se `source_quality` sobe ou `interpretation_confidence` sobe → empírica
- Se o claim ganhou condições de validade → scope
- Se o claim ganhou mecanismo causal → causal

Essa derivação é computável sobre o frontmatter existente.

### Critério de auto-trigger para REFINA empírica

(⚠️ nossa proposta — não validada empiricamente)

```
REFINA auto-trigger IF:
  artigo.source_quality IN [low, medium]           # artigo se beneficia da âncora
  AND paper.quality == primary                     # paper deve ser fonte primária (não secondary)
  AND ingest_chain.depth == 0                      # não dentro de chain INVALIDA ativa
  AND confirming_count_last_5 < 3                  # não quando em run de confirming
```

**Justificativa de cada condição:**
- `source_quality IN [low, medium]`: se artigo já é `high`, a REFINA tem menos impacto — não justifica auto-trigger
- `paper.quality == primary`: REFINA de fonte secondary (análise, review) não garante evidência empírica independente
- `chain.depth == 0`: evitar chains aninhadas (INVALIDA→REFINA→auto-ingest dentro de chain já ativa)
- `confirming_count_last_5 < 3`: se os últimos 3+ ingest foram confirming, auto-trigger de REFINA adicional é FM1 risk — preferir humano aprovar

### Gap — stopping criterion para chains de REFINA

(⚠️ nossa análise, sem fonte primária)

[[sequential-hypothesis-testing]] formaliza stopping criterion para hipóteses binárias (INVALIDA / não-INVALIDA). Para REFINA incremental, o SPRT não se aplica diretamente porque refinamento não é hipótese binária — é uma série contínua de aproximações.

A analogia correta é Lakatos em [[autoresearch-programme-vitality]]: um programa de pesquisa pode degenerar não por falhar em refutar hipóteses, mas por acumular epicycles — ajustes que acomodam cada anomalia sem gerar predições novas. Chains de REFINA sem stopping criterion são o análogo epistêmico de epicycles.

Opção de stopping criterion para REFINA:
- Limitar a 1 REFINA empírica auto-trigger por artigo por janela de 30 dias
- Ou: parar quando `source_quality: high` for atingido (o artigo está ancorado — novas REFINAS têm retorno decrescente)
- Ou: seguir o confirming_ratio de [[autoresearch-programme-vitality]] — se ratio > 0.6 nos últimos N ingest, bloquear REFINA auto-trigger

Nenhuma dessas opções tem validação empírica. A escolha mais conservadora é a atual: nunca auto-trigger REFINA, sempre queue.

## Interpretação

(⚠️ nossa interpretação) A distinção marginal/empírica/scope/causal é operacional, não ontológica — o mesmo paper pode ser classificado de formas diferentes dependendo do estado atual do artigo. Se o artigo tem `interpretation_confidence: low`, um paper que adiciona evidência empírica é REFINA empírica. Se o mesmo artigo já tem `source_quality: high`, o mesmo paper pode ser apenas REFINA marginal.

(⚠️ nossa interpretação) O critério `confirming_count_last_5 < 3` é heurístico e não tem base teórica formal. O número 3 foi escolhido para ser menos restritivo que o threshold degenerativo de Lakatos (confirming_ratio > 0.8 = 4/5), mas mais conservador que nenhum limite.

## Conexões

- depende-de: [[sequential-hypothesis-testing]] ON "SPRT formaliza stopping criterion para hipóteses binárias; gap: não se aplica a refinamento incremental"
- depende-de: [[autonomous-kb-failure-modes]] ON "FM1 (confirming bias) + FM3 (index bloat) são os riscos reais de REFINA auto-trigger; Bradford não os cobre"
- depende-de: [[autoresearch-programme-vitality]] ON "confirming_ratio como proxy para degeneração por epicycles; threshold 0.8 aplica-se como stopping criterion para REFINA chains"
- complementsAt: [[foresight-pipeline-design]] ON "ambos tratam de inserção de conhecimento sem âncora raw/ — foresight via provenance:conjecture, REFINA via prior work empírico"

## Fontes

- [[sequential-hypothesis-testing]] — SPRT stopping criterion; limitação para hipóteses compostas e não-binárias
- [[autonomous-kb-failure-modes]] — FM1 confirming bias acceleration; FM3 index bloat; Bradford gate como proteção insuficiente
- [[autoresearch-programme-vitality]] — confirming_ratio como proxy de degeneração; analogia Lakatos epicycles
- [Sessão /ask REFINA auto-trigger](../../outputs/logs/sessions/2026-04-05/ask-23-15.md) — sessão que originou a taxonomia e o critério de auto-trigger

> ⚠️ QUARENTENA: artigo de síntese emergido de /ask sem fonte raw/ externa. Critérios pendentes: tempo (24h), review frio, adversarial. Para promover: encontrar fonte primária sobre stopping criteria para incremental refinement chains (ex: arXiv:2602.16078 pode ser relevante após ingestão).
