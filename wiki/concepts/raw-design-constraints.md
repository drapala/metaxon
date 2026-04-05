---
title: "Raw/ Design Constraints: Topical Diversity and Source Primacy"
sources:
  - path: wiki/concepts/knowledge-collapse-llm.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/complementary-learning-systems.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [kb-design, raw, knowledge-collapse, catastrophic-interference, data-quality]
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
  pair: [knowledge-collapse-llm, complementary-learning-systems]
  ask_session: outputs/logs/sessions/2026-04-05/ask-oracle-split-cls.md
  connection_type: ANÁLOGO-A
  pearl_level: L2
emerged_on: 2026-04-05
---

## Resumo

O design ótimo de raw/ em um KB autônomo deve satisfazer dois constraints mecanisticamente independentes: diversidade tópica (derivado de CLS / McClelland 1995) e primazia de fontes (derivado de Knowledge Collapse / Keisha et al. 2025). Nenhuma das duas teorias individualmente define ambos os constraints — eles emergem da combinação. O failure mode mais perigoso ocorre quando os dois são violados simultaneamente.

## Conteúdo

### O que knowledge-collapse-llm contribui

Keisha et al. (2025) demonstram que misturar dados reais com dados sintéticos funciona como **regularizador** que atrasa o Stage B de colapso. Mesmo 25% de dados reais produz trajetória U-shaped de perplexidade (dado real ancora a distribuição). A mitigação de 15× por domain-specific training funciona porque mantém a distribuição próxima do ground truth factual — é um problema de **qualidade de fonte**, não de arquitetura.

Implicação para raw/: se /review passa a operar majoritariamente sobre wiki/ (sínteses da própria KB) em vez de raw/ (fontes primárias), o mecanismo de regularização desaparece. A função de raw/ neste modelo é ser o "dado real" que ancora as sínteses geradas pelo compilador.

### O que complementary-learning-systems contribui

McClelland et al. (1995) demonstram que aprendizado focalizado (focused learning — treinar repetidamente em um único conjunto de items sem interleaving) produz aprendizado mais rápido daquele conjunto mas destrói o conhecimento de outros conceitos no neocórtex. Interleaved learning (misturar o novo com toda a base existente) é mais lento mas preserva a estrutura global.

Implicação para raw/: se raw/ acumula predominantemente fontes de um único cluster (ex: AI/ML/agentic systems), /review opera como "focused learning" — aprende bem um cluster, potencialmente degradando integração com outros. A diversidade tópica de raw/ é o equivalente do interleaving hipocampal que previne interferência catastrófica.

### O que emerge da combinação

(⚠️ interpretação do compilador) Os dois constraints são **independentes** — cada um protege contra um mecanismo distinto de degradação:

| Constraint | Derivado de | Mecanismo protegido | O que viola |
|---|---|---|---|
| **Diversidade tópica** | CLS / McClelland | Interferência catastrófica por focused learning | Acumular só fontes do mesmo cluster |
| **Primazia de fontes** | Knowledge Collapse / Keisha | Distributional drift por treinamento sintético recursivo | Usar wiki/ como fonte de /review em vez de raw/ |

A violação isolada de cada constraint produz degradações distintas:
- Violar só diversidade tópica → KB aprende bem o cluster dominante mas perde integração cross-domain
- Violar só primazia → KB mantém diversidade tópica mas fluência diverge de acurácia factual (Stage B)

O failure mode composto — violar os dois simultaneamente — é o mais perigoso e o menos visível: raw/ acumulando sínteses do mesmo cluster. Neste cenário, /review não encontra nem diversidade (CLS violation) nem dados primários (KC violation), e os dois mecanismos de degradação operam em paralelo sem nenhum sinal de alerta nas métricas superficiais.

## Especulação

- A proporção ótima de raw/ vs. wiki/ em um ciclo de /review pode ser estimável a partir dos dados de Keisha et al.: 25% de dados reais foi suficiente para regularização — o que sugere que /review deveria forçar leitura de raw/ em pelo menos 1 de cada 4 claims verificados.
- O efeito de "blocked learning" por cluster pode ter um limiar: abaixo de N fontes do mesmo cluster, o efeito é desprezível; acima, a interferência com outros clusters se torna mensurável.
- Existe um terceiro constraint implícito (não derivado destes dois artigos): **frequência de refresh** — raw/ deve receber novas fontes com regularidade suficiente para que o interleaving não se degrade com o tempo (analogia ao sleep replay no CLS).

## Verificação adversarial

**Pergunta falsificável:** Se raw/ com diversidade tópica + fontes primárias previne ambas as degradações, então uma KB com raw/ exclusivamente de AI/ML primário (alta primazia, baixa diversidade) deveria mostrar degradação de integração cross-domain detectável em /ask, enquanto uma KB com raw/ de múltiplos domínios mas com sínteses internas como fontes (alta diversidade, baixa primazia) deveria mostrar drift factual detectável no /challenge.

**Evidência que confirmaria:** Comparação de /ask logs em KBs com os dois perfis distintos de raw/ mostrando os padrões de falha previstos por cada constraint.

**Evidência que refutaria:** Uma KB com raw/ exclusivamente de um domínio mas com alta primazia de fontes que não mostra degradação cross-domain após muitos ciclos de /review — indicaria que diversidade tópica não é necessária se primazia for mantida.

## Conexões

- emerge-de: [[knowledge-collapse-llm]] ON "real data as regularizer — domain-specific training delays Stage B 15×"
- emerge-de: [[complementary-learning-systems]] ON "focused learning destroys other concepts — interleaved learning preserves global structure"
- applies-to: [[autonomous-kb-failure-modes]] ON "FM1 + FM3 prevention mechanisms have independent structural requirements"
- applies-to: [[autoresearch-reliability-triad]] ON "Pilar 1 (external oracle) implicitly requires source primacy to prevent oracle anchoring on wiki/ content"

## Fontes

- [[knowledge-collapse-llm]] — mecanismo de regularização por dados reais; 15× domain-specific mitigation; 25% real data threshold
- [[complementary-learning-systems]] — focused vs. interleaved learning; catastrophic interference com blocked learning (experimento pinguim)
- [Log /ask 2026-04-05](../../outputs/logs/sessions/2026-04-05/ask-oracle-split-cls.md) — sessão que descobriu a independência dos dois constraints

> ⚠️ QUARENTENA: artigo emergido de /ask cross-domain. Critérios pendentes: tempo (24h), review frio, adversarial.
