---
title: "Sequential Hypothesis Testing (SPRT, Wald 1945)"
sources:
  - path: raw/papers/wald-1945-sprt-sequential-tests.md
    type: paper
    quality: primary
    stance: neutral
created: 2026-04-04
updated: 2026-04-04
tags: [statistics, sequential-testing, stopping-criterion, decision-theory]
source_quality: medium
interpretation_confidence: high
resolved_patches: []
reads: 1
retrievals_correct: 1
retrievals_gap: 0
last_read: 2026-04-05
quarantine: false
provenance: source
---

## Resumo

SPRT (Wald, 1945): teste de hipótese sequencial que decide a cada passo se continua coletando evidência ou para. A regra de parada usa o log-likelihood ratio acumulado Sₙ = Σ log Λᵢ comparado a thresholds a = log(β/(1-α)) e b = log((1-β)/α). Teorema central: SPRT minimiza o número esperado de observações (ASN) entre TODOS os testes com os mesmos α e β — é o procedimento sequencial ótimo. Aplicação direta a autoresearch: cada ciclo de teste = uma observação; para quando a evidência acumulada cruza o threshold de confirmação ou rejeição.

## Conteúdo

### Setup e Stopping Rule

**Duas hipóteses:**
- H₀: "hipótese emergida é artefato/circular" (null)
- H₁: "hipótese emergida é robusta/genuína" (alternative)

**Log-likelihood ratio por ciclo:** λᵢ = log P(observação i | H₁) / P(observação i | H₀)

**Acumulado:** Sₙ = Σᵢ λᵢ

**Regra:**
- Sₙ ≥ b → PARA, confirma H₁
- Sₙ ≤ a → PARA, rejeita (refuta hipótese)
- a < Sₙ < b → CONTINUA

### Thresholds

Dado α (falso positivo tolerado) e β (falso negativo tolerado):

```
a = log(β / (1-α))
b = log((1-β) / α)
```

**Exemplo** (α=0.05, β=0.10): a ≈ −2.25, b ≈ 2.89

### Teorema de Optimalidade (Wald & Wolfowitz)

SPRT minimiza E[N | H₀] e E[N | H₁] simultaneamente entre todos os procedimentos sequenciais com mesmos α e β. Não existe procedimento mais eficiente.

**ASN aproximado:**

```
E[N | H₁] ≈ [β·log(β/(1-α)) + (1-β)·log((1-β)/α)] / E[λᵢ | H₁]
```

Onde E[λᵢ | H₁] = KL divergence entre as duas hipóteses.

**Insight crítico:** ASN ∝ 1/KL. Quanto mais discriminativa cada observação, menos ciclos necessários. Hipóteses muito distinguíveis (alto KL) convergem rápido; hipóteses próximas (baixo KL) precisam de mais ciclos.

### Limitações

1. **i.i.d. obrigatório:** observações devem ser independentes. Viola-se quando cada ciclo de teste muda o sistema testado (feedback loop).
2. **H₀ e H₁ pontuais:** hipóteses compostas requerem extensões.
3. **Requer p(observação | Hⱼ):** para calcular λᵢ, precisa de modelo de probabilidade para as hipóteses — difícil quando hipóteses são verbais.

### Extensões para não-i.i.d.

- **e-values e e-processes** (Vovk & Wang 2021): anytime-valid, dispensam i.i.d.
- **Alpha spending functions** (DeMets & Lan): para looks irregulares
- **mSPRT** (mixture-SPRT): prior sobre H₁ em vez de valor pontual

## Interpretação

### Aplicação ao Autoresearch Loop

⚠️ Nossa interpretação — Wald não discute autoresearch.

O SPRT resolve exatamente o problema do Pilar 3 (stopping criterion): dado N ciclos de teste sequenciais de uma hipótese emergida, quando parar com confiança controlada?

**Mapeamento:**
| SPRT | Autoresearch |
|------|-------------|
| Observação xᵢ | Ciclo de teste i (resultado: confirmação parcial/refutação) |
| H₁ | "Hipótese é robusta" |
| H₀ | "Hipótese é circular/artefato" |
| λᵢ | Log-razão P(resultado | H₁) / P(resultado | H₀) |
| Sₙ | Evidência acumulada |
| a, b | Thresholds de confiança pré-definidos |

**Relação com PAC-Bayes:** PAC-Bayes diz que ASN ∝ KL(ρ||π) — quanto mais surpresa a hipótese, mais ciclos. SPRT formaliza isso: E[N] ∝ 1/E[λ] = 1/KL. Os dois convergem na mesma dependência de KL, por caminhos independentes.

**Problema prático:** SPRT requer P(observação | H₁) e P(observação | H₀) — modelo probabilístico para as hipóteses. Em autoresearch verbal (hipóteses de KB), este modelo não é trivial. Possível operacionalização: usar frequência de confirmação histórica de hipóteses similares como proxy para P(confirmar | H₁).

**Problema estrutural:** SPRT assume i.i.d. Ciclos de /ask não são independentes — cada teste pode mudar a KB, que muda os testes seguintes. Extensão via e-processes seria necessária para o caso de autoresearch com feedback.

## Verificação adversarial

**Claim mais fraco:** O teorema de optimalidade de Wald é para o caso de hipóteses simples (H₀ e H₁ pontuais) e observações i.i.d. — as condições mais fortes possíveis. Para o caso autoresearch (hipóteses verbais, ciclos dependentes), SPRT não é aplicável diretamente.

**O que o paper NÃO diz:** Wald não diz que SPRT é ótimo para qualquer procedimento sequencial — apenas para os com mesmo α e β fixos. Se α e β variam ao longo dos ciclos (adaptive), outros procedimentos podem ser superiores.

## Conexões

- instancia: [[question-taxonomy]] ON "Simon stopping criterion (satisficing) tem formalização exata em SPRT: parar quando Sₙ cruza threshold, não quando se alcança N fixo"
- complementsAt: [[pac-bayes-bounds]] ON "PAC-Bayes e SPRT convergem: ambos derivam ASN ∝ 1/KL — quanto mais discriminativa a evidência, menos ciclos. PAC-Bayes é para generalização de ensemble; SPRT é para hipóteses sequenciais"
- formaliza: [[autoresearch-reliability-triad]] ON "Pilar 3 (stopping criterion): SPRT dá o N ótimo como função de α, β, e E[λᵢ | H₁]"
- fundamenta: [[fast-frugal-heuristics]] ON "Take-the-Best usa o primeiro cue discriminante e para — SPRT formaliza quando um cue 'é discriminante o suficiente' via threshold b"

## Fontes

- [Wald 1945 — Sequential Tests](../../raw/papers/wald-1945-sprt-sequential-tests.md) — definição, thresholds, teorema de optimalidade, ASN aproximado, limitações
