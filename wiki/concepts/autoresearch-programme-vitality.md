---
title: "Autoresearch Programme Vitality"
sources:
  - path: wiki/concepts/autoresearch-reliability-triad.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/scientific-research-programmes.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [meta-kb, autoresearch, lakatos, programme-health, hard-core, protective-belt]
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
  adversarial_or_scout_or_prediction: false
provenance: emergence
emergence_trigger:
  pair: [autoresearch-reliability-triad, scientific-research-programmes]
  ask_session: outputs/logs/sessions/2026-04-05/ask-autoresearch-lakatos.md
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-05
---

## Resumo

O [[autoresearch-reliability-triad]] diagnostica sessões individuais; [[scientific-research-programmes]] diagnostica programas de pesquisa ao longo do tempo. Combinados, expõem um gap: a KB não distingue artigos **hard core** (cujas refutações invalidam o design inteiro) de artigos **protective belt** (que absorvem anomalias e devem ser substituíveis). Sem essa distinção, o `/challenge` opera cegamente — não sabe quando está purgando redundância ou derrubando um pilar.

## Conteúdo

### O que autoresearch-reliability-triad contribui

O triad define três pilares para sessões individuais de autoresearch: (1) oracle externo independente, (2) sinais contraditórios em canal público, (3) stopping criterion pré-definido. O Pilar 3 já referencia Lakatos como meta-regra: se as últimas N hipóteses geraram todos o mesmo tipo de insight (L1, confirming), o autoresearch degenerou — parar a linha.

Mas o triad não vai além disso: não especifica *quais* artigos da KB devem ser prioritariamente challengeados, nem monitora a saúde do programa ao longo de múltiplas sessões.

### O que scientific-research-programmes contribui

Lakatos distingue dois componentes de qualquer programa de pesquisa:

- **Hard core:** proposições fundamentais que os praticantes decidem não falsar. Refutação do hard core = abandono do programa. Proteger o hard core é **racional**, não dogmático — enquanto o programa gera predições novas.
- **Protective belt:** hipóteses auxiliares que absorvem anomalias. Ajustes ao belt são legítimos se geram novas predições; ilegítimos (ad hoc) se apenas acomodam fatos já conhecidos.

O critério de degeneração é longitudinal: um programa degenerativo só acomoda — nunca prediz primeiro.

### O que emerge da combinação

(⚠️ nossa interpretação) Aplicando a estrutura Lakatos à KB:

**Hard core da KB** — claims cuja falsificação exigiria redesenhar o sistema:
- Os três pilares do autoresearch-reliability-triad
- O princípio de fontes imutáveis em raw/ (CLAUDE.md)
- A hierarquia causal de Pearl aplicada a claims da KB

**Protective belt da KB** — artigos que absorvem anomalias:
- Artigos de instância de um domínio específico (ex: `corruption-audits-brazil`)
- Artigos que chegaram por confirmar hipóteses já no hard core (a maioria dos ingest confirming)
- Artigos emergidos de /ask que depois não se propagaram (sem connections de saída)

**O `/challenge` como gestão de protective belt:**
O `/challenge` atual opera em qualquer artigo em quarentena. Lakatos sugere priorização:
- Protective belt: `/challenge` frequente — são substituíveis, devem absorver anomalias sem custo alto
- Hard core: `/challenge` raro, deliberado — um challenge que derruba um artigo hard core não é vitória epistêmica, é crise de design que requer revisão ampla

**Métrica de saúde longitudinal — confirming_ratio:**

(⚠️ nossa métrica, derivada de Lakatos) A proporção de ingest recentes que apenas confirmam vs. que geram predições novas antes de evidência:

```
confirming_ratio = count(ingest confirming últimos N) / N
```

| Ratio | Diagnóstico Lakatos |
|-------|---------------------|
| < 0.5 | Programa progressivo — maioria dos ingest geram predições novas |
| 0.5–0.8 | Zona mista — monitorar tendência |
| > 0.8 | Programa degenerativo — ingest apenas acomoda |

**Calibração atual (⚠️ nossa contagem, 2026-04-05):**
Ingest recentes: `autonomous-kb-failure-modes` (confirming), `curse-of-knowledge-llm-judge` (confirming), `causal-reasoning-pearl` (neutral/preditivo), `multi-agent-memory-consistency` (neutral), `graph-anchored-iterative-retrieval` (neutral).
Estimativa de ratio: ~0.4 — zona progressiva. Mas contagem pequena (N=5); tendência requer monitoramento.

**last_novel_prediction:** o campo que rastreia quando o último ingest gerou uma predição nova antes de evidência — não uma acomodação. Exemplos de predições genuínas no corpus: `autoresearch-reliability-triad` (taxa >80%), `procurement-variety-gap` (error floor preservado por Lei 14.133).

## Especulação

- A distinção hard core/protective belt em KBs pode ser fluida — um artigo começa como protective belt e, se suficientemente referenciado, torna-se hard core implícito. Um mecanismo de detecção automática (por in-degree de wikilinks + age) poderia classificar artigos retrospectivamente
- O threshold de 0.8 para confirming_ratio é arbitrário — derivado da predição do triad (>80% confirmação = circularidade). Pode ser calibrado com dados reais após N≥20 ingest
- Programas que oscilam entre progressivo e degenerativo (em ciclos) podem ser saudáveis se as fases degenerativas são curtas — Lakatos não discute dinamismo temporal, apenas trajetória geral

## Verificação adversarial

**Pergunta falsificável:** Uma KB com confirming_ratio > 0.8 por 10+ ingest consecutivos gera artigos emergidos de /emerge com menor taxa de confirmação por oracle externo do que uma KB com ratio < 0.5?

**Evidência que confirmaria:** Comparar dois períodos da mesma KB (um confirming-heavy, um prediction-heavy) — os /emerge do período prediction-heavy produzem mais conexões genuínas (não SPLIT) por oracle.

**Evidência que refutaria:** Taxa de conexões genuínas no /emerge independe do confirming_ratio dos ingest anteriores — indicaria que a vitality do programa não afeta a qualidade das hipóteses geradas.

## Conexões

- emerge-de: [[autoresearch-reliability-triad]] ON "triad diagnostica sessões; Lakatos diagnostica programas — a distinção hard core/protective belt preenche o gap longitudinal"
- emerge-de: [[scientific-research-programmes]] ON "hard core vs. protective belt + critério progressivo/degenerativo como métrica de saúde de KB"
- instancia: [[autonomous-kb-failure-modes]] ON "KB sem distinção hard core/belt = failure mode silencioso: /challenge derruba pilares sem saber"
- complementa: [[sequential-hypothesis-testing]] ON "SPRT formaliza o stopping criterion por sessão; confirming_ratio formaliza o critério longitudinal de degeneração"
- depende-de: [[falsificationism-demarcation]] ON "Popper fornece o critério de falsificabilidade que o hard core deve satisfazer para ser legítimo"

## Fontes

- [[autoresearch-reliability-triad]] — três pilares session-level; meta-stopping rule Lakatos já mencionado; gap: sem distinção de artigos por tipo
- [[scientific-research-programmes]] — hard core/protective belt, progressivo/degenerativo, racionalidade de proteção
- [Log /ask](../../outputs/logs/sessions/2026-04-05/ask-autoresearch-lakatos.md) — sessão que identificou /challenge como gestão de protective belt e propôs confirming_ratio

> ⚠️ QUARENTENA: artigo emergido de /ask cross-domain. Critérios pendentes: tempo (24h), review frio, adversarial.
