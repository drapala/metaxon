---
title: "KB Auto-Promote Protocol"
sources:
  - path: outputs/logs/sessions/2026-04-05/ask-autoresearch-lakatos.md
    type: note
    quality: primary
    stance: neutral
  - path: wiki/concepts/autoresearch-reliability-triad.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/evaluation-order-independence.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autoresearch-programme-vitality.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [meta-kb, protocol, promote, quarantine, auto-promote]
source_quality: medium
interpretation_confidence: medium
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: false
provenance: synthesis
synthesis_sources:
  - wiki/concepts/autoresearch-reliability-triad.md
  - wiki/concepts/evaluation-order-independence.md
  - wiki/concepts/autoresearch-programme-vitality.md
  - wiki/concepts/autonomous-kb-failure-modes.md
---

## Resumo

O pipeline padrão `/ingest → quarentena 24h → /review humano → /challenge humano → /promote` tem o humano como gargalo na maioria dos casos. O auto-promote protocol substitui os passos humanos por gates computáveis e cross-model challenge, reservando revisão humana para casos onde a automação detecta risco real.

## Conteúdo

### Decisão central: quem decide a promoção?

O humano adiciona valor em duas situações: (1) detecta erros semânticos que o LLM não detecta na mesma sessão de ingest (reference-anchoring bias, [[evaluation-order-independence]]); (2) decide se um artigo hard core deve ser challengeado, com plena consciência das implicações de design ([[autoresearch-programme-vitality]]).

Em todos os outros casos, a promoção pode ser automatizada se as seguintes condições forem satisfeitas: ausência de falhas estruturais + oracle semanticamente independente (cross-model) + nenhum prior work invalidante encontrado.

### Gate 1 — Nunca auto-promote (filtro categórico)

Artigos nas categorias abaixo vão **sempre** para quarentena humana, independente de qualquer outro critério:

| Categoria | Critério | Razão |
|---|---|---|
| Meta-KB | arquivo em `programme_health.hard_core[]` em kb-state.yaml | Refutação implica redesenho do sistema |
| Emergence | `provenance: emergence` no frontmatter | Síntese cross-domain tem interpretation_confidence: low por padrão |
| Baixa confiança | `interpretation_confidence: low` | Claim especulativo precisa de olhos externos |
| Baixa qualidade | `source_quality: low` | Sem fonte primary ou secondary concordante |
| Zona degenerativa + confirming | `confirming_ratio > 0.8` E artigo classificado como `confirming` | Auto-promote aceleraria degeneração do programa ([[autoresearch-programme-vitality]]) |

### Gate 2 — Verificação estrutural (computável)

Checks executáveis no próprio arquivo, sem LLM:

| Check | O que verifica | Script |
|---|---|---|
| Citações raw | Todo claim tem link `../../raw/` | `structural-promote-gate.sh` |
| Marcadores ⚠️ | Claims interpretativos marcados se ## Interpretação existe | `structural-promote-gate.sh` |
| Seções separadas | ## Interpretação não misturada com ## Conteúdo | `structural-promote-gate.sh` |
| Wikilinks tipados | Conexões têm tipo (contradicts, instancia, emerge-de, etc.) | `structural-promote-gate.sh` |
| Predição falsificável | Presente para artigos de emergence (opcional para source) | `structural-promote-gate.sh` |
| Coerência de scores | source_quality:high + interpretation_confidence:low → ⚠️ flag | `structural-promote-gate.sh` |

Falha em qualquer check → quarentena com razão documentada. O check é barato — roda em < 1s.

### Gate 3 — Challenge semântico cross-model

Do Pilar 1 do [[autoresearch-reliability-triad]]: o oracle de grounding precisa ser *computacionalmente independente* do compilador. /challenge na mesma sessão de /ingest viola [[evaluation-order-independence]] — o modelo não consegue "desver" a wiki que escreveu.

Solução: cross-model challenge via `scripts/cross-model-challenge.py` (já existente para /emerge), com modelo diferente do que fez o ingest:

```bash
python scripts/cross-model-challenge.py \
  --article wiki/concepts/[artigo].md \
  --mode auto-challenge \
  --models gemini-3.1-pro-preview  # diferente do compilador padrão
```

Output esperado: lista de claims com `status: survived|weakened|invalidated`.

**Condição de auto-promote:** 0 claims `invalidated` + prior web search sem invalidações.

**Condição de quarentena:** ≥ 1 claim `weakened` (humano decide se é correção menor) OU ≥ 1 claim `invalidated`.

### Gate 4 — Programme health gating

| confirming_ratio | Artigo confirming | Artigo novel_prediction |
|---|---|---|
| < 0.5 | auto-promote elegível | auto-promote elegível |
| 0.5–0.8 | cross-model obrigatório | auto-promote elegível |
| > 0.8 | nunca auto-promote | cross-model obrigatório |

### Árvore de decisão

```
/ingest completo
  │
  ├─ Gate 1: é meta-KB / emergence / low confidence / low quality / degenerative+confirming?
  │    └─ SIM → quarentena humana [razão: Gate 1 — categoria]
  │
  ├─ Gate 2: falha estrutural?
  │    └─ SIM → quarentena humana [razão: Gate 2 — check específico]
  │
  ├─ Gate 3: cross-model challenge → claim invalidado?
  │    └─ SIM → quarentena humana [razão: Gate 3 — [claim]]
  │    └─ claim weakened → quarentena humana [razão: Gate 3 — weakened, humano decide]
  │
  └─ Todos os gates passaram → AUTO-PROMOTE
       quarantine: false
       quarantine_promoted: [data]
       quarantine_criteria_met:
         auto_promote: true
         gates_passed: [1, 2, 3]
```

### O que o auto-promote NÃO resolve

**Ausência de evidência vs. evidência de ausência:** o auto-promote promove artigos estruturalmente corretos — não detecta se o artigo trata ausência de citação como ausência de fenômeno. Esse gap permanece e exige disciplina de escrita no /ingest.

**Demoção de verdades antigas:** artigos auto-promoted são unidirecionais. Se evidência contrária surgir depois, o protocolo de patch/recall é manual. Cascade-repair não existe.

**Bias do espaço de busca:** o auto-promote promove o que foi ingerido — não audita o que não foi. Se /emerge gera apenas pares internos ao corpus, artigos trivialmente confirming podem ser auto-promoted corretamente mas epistemicamente vazios.

## Interpretação

(⚠️ nossa síntese) O auto-promote não elimina a necessidade de humano — move o humano para onde seu julgamento é insubstituível: artigos hard core, artigos de emergence com conexões genuinamente novas, e casos onde o cross-model challenge detecta conflito real. Em todos os outros casos, o humano era gargalo sem adicionar valor detectável.

A condição de suficiência para confiança: verificação estrutural computável + oracle semanticamente independente (cross-model, sessão diferente de treinamento). Não é equivalente a peer review humano, mas é melhor que auto-reflexão na mesma sessão.

## Verificação adversarial

**Pergunta falsificável (L2):** Artigos auto-promoted têm taxa de error descoberto em challenges posteriores (feitos por humano ou cross-model em sessão futura) inferior a 20%? Se a taxa for > 20%, o Gate 3 está insuficiente.

**Evidência que refutaria:** N≥10 artigos auto-promoted → challenge retrospectivo → > 20% com claims invalidados. Indicaria que cross-model na mesma sessão não é suficientemente independente.

## Conexões

- instancia: [[autoresearch-reliability-triad]] ON "Pilar 1 (oracle independente) implementado via cross-model; Pilar 3 (stopping criterion) implementado via Gate 3 threshold"
- instancia: [[evaluation-order-independence]] ON "cross-model challenge separa sessão de escrita da sessão de julgamento"
- instancia: [[autoresearch-programme-vitality]] ON "Gate 1 protege hard core; Gate 4 gata por confirming_ratio"
- instancia: [[autonomous-kb-failure-modes]] ON "Gate 1 previne authority cascade em hard core implícito"

## Fontes

- [[autoresearch-reliability-triad]] — Pilar 1: oracle computacionalmente independente; Pilar 3: stopping criterion
- [[evaluation-order-independence]] — /challenge na mesma sessão viola L3; cross-model como mitigação
- [[autoresearch-programme-vitality]] — Gate 1 (hard core) e Gate 4 (programme health)
- [[autonomous-kb-failure-modes]] — failure mode de authority cascade pós-promote silencioso
