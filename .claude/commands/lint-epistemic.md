# /lint-epistemic

Audita saúde epistêmica da KB. Computa 4 métricas e gera relatório.

## Passo 1 — Stance ratio por mês

Leia `wiki/_registry.md`. Para cada linha com `| processed |`:
- Extraia data (coluna 2) e stance (coluna 5)
- Agrupe por mês (YYYY-MM)
- Compute: confirming / neutral / challenging por mês e total

**Threshold de alerta:** se challenging < 20% em qualquer mês com ≥5 fontes ingeridas → marcar `⚠️ ALERTA`.

Nota: fontes laterais (domínios não-AI/ML) tendem a ser neutral por construção — não confundir com ausência de adversarial sourcing. Se a proporção de neutral for alta num mês, verifique se é por ingestão lateral (Bradford Zone 3) antes de alertar.

## Passo 2 — Synthesis ratio

Para cada artigo em `wiki/concepts/*.md` (excluindo `_index*.md`):
- Conte itens em seção `### Especulação` (linhas começando com `-` dentro dessa seção)
- Conte itens em `### Descrição` + `### Interpretação` como proxy de claims totais
- Compute: speculation_items / total_items por artigo

Agregue: % de artigos com speculation_ratio > 50% (sinal de over-synthesis estrutural).

Não leia todos os arquivos de uma vez. Use Glob para listar, depois leia em lotes.
Circuit breaker: se ≥10 artigos sem seções epistêmicas (sem `### Especulação` nem `### Descrição`), note como "artigos sem níveis epistêmicos" — não tente inferir.

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

## Stance Ratio

[tabela por mês]
[alerta se < 20% challenging]

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
