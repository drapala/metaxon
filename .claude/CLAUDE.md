# LLM Knowledge Base — Agent Instructions

## Papel
Você é o compilador deste knowledge base. Mantém wiki/ como enciclopédia
interligada baseada nas fontes em raw/.

## Regras Fundamentais
1. NUNCA edite raw/ — fontes imutáveis
2. Atualize _index.md e _registry.md após qualquer mudança no wiki
3. Use wikilinks [[conceito]] para interligar artigos
4. Cite com links relativos para raw/ (ex: [fonte](../../raw/articles/x.md))
5. Cada artigo wiki segue o template abaixo
6. _index.md é PONTEIRO, não conteúdo: max ~150 chars por linha
   (título + contexto mínimo). Nunca despeje resumos longos no índice.

## Disciplina de Escrita
- Sempre: escreva/atualize o artigo PRIMEIRO → depois atualize _index.md
- Nunca: dump de conteúdo no _index.md (previne entropia)
- Se algo é derivável (pode ser recalculado), não persista no wiki
- **Marcar interpretações com ⚠️:** claims factuais diretos das fontes ficam sem marca.
  Sínteses cross-paper, analogias com esta KB, e "therefore" claims devem ser
  prefixados com "(⚠️ nossa interpretação)" ou "(⚠️ design analogy)".
  O wiki é mais forte quando distingue o que as fontes dizem do que nós inferimos.

## Retrieval (3 camadas)
O /ask segue esta hierarquia de leitura:
- Layer 1: _index.md — SEMPRE lido (leve, ponteiros)
- Layer 2: wiki/concepts/*.md — lido ON-DEMAND quando relevante
- Layer 3: raw/ — NUNCA lido inteiro, só consultado para verificação pontual
Wiki é hint, não verdade. Se wiki contradiz raw/, raw/ VENCE.

## Granularidade (heurísticas, não leis)
- 1 conceito = 1 arquivo
- Tipicamente 2+ fontes OU 200+ palavras justificam artigo, mas fonte primária
  forte pode justificar sozinha. Teste: "vai ser referenciado de outros artigos?"
- ~1500 palavras = considerar split
- Se detectar overlap >60% entre artigos, sugira merge
- Nomes: kebab-case (ex: retrieval-augmented-generation.md)

## Proveniência de Fontes
Ao registrar fontes no frontmatter e _registry.md, classifique:
- type: article | paper | repo | note | dataset
- quality: primary (dados originais, paper) | secondary (análise, review) | tertiary (resumo, opinião)
- stance: confirming | challenging | neutral (em relação às premissas do wiki)
O /ask deve preferir evidência primary > secondary > tertiary.

## Confidence Scoring (dois eixos)
Cada artigo wiki tem dois scores independentes no frontmatter:
- **source_quality: high|medium|low** — objetivo, baseado em fontes:
  high = 2+ primary concordam, medium = 1 primary ou 2+ secondary, low = apenas tertiary
- **interpretation_confidence: high|medium|low** — subjetivo, auto-avaliação:
  high = claim factual direto, medium = síntese moderada, low = insight novel/cross-paper
Quando divergem (ex: source_quality:high mas interpretation_confidence:low), flag com ⚠️.

## Patch System
Se encontrar bloco > [!patch] num artigo wiki:
1. Incorpore a correção no corpo do artigo
2. Mova o patch para o frontmatter em `resolved_patches:`
   com data, texto original substituído, e fonte do patch
3. Remova o bloco > [!patch] do corpo

## Template de Artigo
---
title: "Nome do Conceito"
sources:
  - path: raw/articles/x.md
    type: article
    quality: primary
  - path: raw/papers/y.pdf
    type: paper
    quality: primary
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
source_quality: high|medium|low
interpretation_confidence: high|medium|low
resolved_patches: []
---

## Resumo
[2-3 frases]

## Conteúdo
[Corpo]

## Conexões
- [[related-concept]]

## Fontes
- [nome](../../raw/articles/x.md) — 1 linha do que a fonte contribui
