# /lint-epistemic

Audita saúde epistêmica da KB. Computa 4 métricas e gera relatório.

## Passo 1 — Stance ratio por tipo de fonte

O threshold adversarial se aplica diferentemente a fontes core vs. laterais.

### Classificação core vs. lateral

Fonte é **lateral** se seus concepts no _registry.md mapeiam para qualquer artigo
da lista de domínios Zone 3:

```
heuristics-and-biases, prospect-theory, social-choice-aggregation,
complexity-stability-tradeoff, resource-competition-coexistence,
zipf-law-power-laws, falsificationism-demarcation, scientific-research-programmes,
episodic-semantic-memory, complementary-learning-systems, stigmergic-coordination,
complexity-emergence, predictive-processing, requisite-variety,
viable-system-model-beer, bibliometrics, bradford-law-scattering,
fast-frugal-heuristics, groupthink-and-cascades, immune-inspired-credit-assignment,
causal-reasoning-pearl, formal-ontology-for-kbs
```

Tudo que não mapeiar para essa lista é **core** (AI/ML + Info Theory + Meta-KB).

Quando ambíguo (e.g., fonte que alimentou tanto artigo core quanto lateral): classifique como core.

### Cálculo separado

**Fontes core:**
- Compute challenging / total_core por mês
- **Threshold de alerta:** challenging < 20% em mês com ≥5 fontes core → `⚠️ ALERTA adversarial`

**Fontes laterais:**
- Threshold de stance NÃO se aplica
- Compute Bradford Zone3/Zone2: `(fontes laterais acumuladas) / (fontes Zone 2 acumuladas)`
- **Threshold de alerta:** Zone3/Zone2 < 0.8 → `⚠️ ALERTA cobertura lateral`
- Atual referência: Zone3/Zone2 = 1.05 → pausa (não expandir Zone 3)

### Output desta seção

```
## Stance Ratio

### Fontes Core
| Mês | Confirming | Neutral | Challenging | Total | % Challenging | Status |
...

### Fontes Laterais (Bradford)
Zone3/Zone2 atual: X.XX → [expandir / pausa / ok]
```

## Passo 2 — Synthesis ratio

O template atual usa `## Conteúdo` (claims factuais) e `## Interpretação` (síntese, analogias, "therefore" claims).
Formatos legados com `### Especulação` / `### Descrição` também devem ser detectados.

Para cada artigo em `wiki/concepts/*.md` (excluindo `_index*.md`):

**Detecção de seções (em ordem de prioridade):**
1. Se tem `## Interpretação` → é o proxy de síntese (template atual)
   Se tem `## Conteúdo` → é o proxy de claims factuais
2. Se tem `### Especulação` → formato legado para síntese
   Se tem `### Descrição` → formato legado para claims factuais
3. Se nenhum dos dois formatos → artigo sem seções epistêmicas mensuráveis

**Cômputo por artigo:**
- `conteudo_items` = linhas começando com `-` em `## Conteúdo` (ou `### Descrição`)
- `interpretacao_items` = linhas começando com `-` em `## Interpretação` (ou `### Especulação`)
- `synthesis_ratio` = interpretacao_items / (conteudo_items + interpretacao_items)
- Artigos onde `## Interpretação` está vazia têm ratio = 0 (puramente factuais — bom sinal)

**Agregação:**
- % de artigos com synthesis_ratio > 50% (sinal de over-synthesis estrutural)
- % de artigos com `## Interpretação` vazia (puramente factuais)
- Lista dos 3 com maior ratio

Não leia todos os arquivos de uma vez. Use Bash com python3 para processar em lote.

Circuit breaker: se ≥10 artigos sem NENHUMA seção epistêmica detectável (nem formato atual nem legado),
note como "artigos sem seções epistêmicas" E reporte o formato encontrado como evidência —
o problema pode ser de detecção, não de ausência real. Não tente inferir ratio nesses artigos.

## Passo 3 — Quarantine rate

Da lista de artigos, conte:
- `quarantine: true` → em quarentena
- `quarantine: false` + `quarantine_promoted` preenchido → promovidos
- sem campo quarantine → não aplicável (artigos antigos)

Compute: quarantine_rate = quarentena_ativa / total_artigos

Liste artigos em quarentena com suas razões.

## Passo 4 — Hub health

De `wiki/_registry.md`, identifique artigos com `reads: 0`:
- Se `last_read` é nulo ou data < (hoje - 30 dias) → hub não utilizado

Compare com in-degree do grafo (se disponível de análise anterior).
Artigos com in-degree ≥ 5 e reads = 0 são candidatos a revisão: muito linkados mas nunca lidos diretamente via /ask.

## Passo 5 — Output

Salve em `outputs/reports/epistemic-lint-YYYY-MM-DD.md` com:

```markdown
---
date: YYYY-MM-DD
---

## Stance Ratio — Fontes Core
[tabela por mês: confirming/neutral/challenging/total/% challenging/status]
[⚠️ ALERTA se challenging < 20% em mês com ≥5 fontes core]

## Bradford Coverage — Fontes Laterais
Zone3/Zone2: X.XX → expandir (<0.8) | pausa (0.8–1.2) | ok (>1.2)
[lista de domínios Zone 3 cobertos e descobertos]

## Synthesis Ratio

[% artigos com speculation_ratio > 50%]
[lista dos 3 mais especulativos]

## Quarantine Rate

[N quarentenados / N total = X%]
[lista artigos em quarentena com razão]

## Hub Health

[N artigos com reads=0]
[destaque: hubs in-degree ≥5 com reads=0]

## Ações recomendadas

[lista priorizada baseada nos alertas]
```

## Notas

- Circuit breaker: se _registry.md tiver > 200 linhas, não leia inteiro — use Bash/awk para extrair stances
- Não modifique nenhum artigo durante o lint — é operação read-only
- Se algum metric não for computável (dados ausentes), reporte como "não mensurável" em vez de estimar

---

## Pipeline — kb-state.yaml

### Lê (início)
- `fast_cycle.ingest_count_since_last_lint` — para contextualizar quantas fontes foram adicionadas desde o último lint
- `promote.promoted_since_last_lint` — artigos promovidos desde o último lint (podem afetar quarantine_rate)

### Escreve (final)
```yaml
updated: YYYY-MM-DD
fast_cycle:
  ingest_count_since_last_lint: 0   # reset
promote:
  promoted_since_last_lint: []      # reset
slow_cycle:
  lint:
    last_run: YYYY-MM-DD
    alerts:
      # se challenging < 20% em mês com ≥5 fontes core:
      - type: adversarial_gap
        value: X%
        threshold: 20%
        message: "Mês YYYY-MM: X% challenging (abaixo de 20%)"
      # se Zone3/Zone2 < 0.8:
      - type: bradford_coverage
        value: X.XX
        threshold: 0.8
        message: "Zone3/Zone2=X.XX abaixo de 0.8: expandir fontes laterais"
      # se quarantine_rate > 15%:
      - type: quarantine_rate
        value: X%
        threshold: 15%
        message: "X% dos artigos em quarentena (acima de 15%)"
```

Atualize também `corpus.quarantined_articles` se o lint revelou discrepância com o valor atual.

### Gatilhos — verifique ao final

| Condição | Gatilho |
|----------|---------|
| `alerts` contém `adversarial_gap` | `⚠️ /curate ou /ingest — déficit adversarial em fontes core. Busque fonte challenging.` |
| `alerts` contém `quarantine_rate` alto | `⚠️ /challenge ou /promote — muitos artigos em quarentena. Priorize autonomous-kb-failure-modes.` |
| Hubs com `reads=0` e in-degree ≥5 detectados | `💡 /ask — hubs nunca lidos diretamente: [lista]. Rode /ask para validar utilidade.` |
| synthesis_ratio > 50% em ≥3 artigos | `⚠️ Over-synthesis estrutural. /review com foco em seção Especulação desses artigos.` |

Adicione alertas e gatilhos a `active_triggers` com prioridades correspondentes.

Atualize também `readiness_signal` com base nos resultados do lint:
- `can_ingest`: true se nenhum alerta crítico; false se quarantine_rate > 20% ou adversarial_gap severo
- `stance_status`: valor calculado pelo lint (mais preciso que a estimativa do /ingest)
- `warning`: texto do alerta mais relevante, ou null se tudo ok
- `next_ingest_candidates`: top 2 da fila com stance compatível com o estado atual

Atualize `next_actions` com base nos gatilhos disparados.
