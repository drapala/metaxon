---
title: "AI and Economic Growth — Goldman Sachs Projections"
sources:
  - path: raw/papers/goldman-sachs-2023-ai-economic-growth.pdf
    type: paper
    quality: secondary
    stance: neutral
created: 2026-04-08
updated: 2026-04-08
tags: [ai-economics, gdp, productivity, labor-market, generative-ai, goldman-sachs]
source_quality: medium
interpretation_confidence: high
resolved_patches: []
provenance: source
---

## Resumo

Goldman Sachs (Briggs/Kodnani, março 2023) projeta que AI generativa poderia substituir ~25% do trabalho global (equivalente a 300 milhões de empregos), aumentar a produtividade de trabalho nos EUA em +1.5 pp anuais, e adicionar +7% ao PIB global ao longo de um período de 10 anos. É um documento de banco de investimento — não peer-reviewed. As projeções refletem análise técnica de exposição ocupacional + precedentes históricos de tecnologias de uso geral.

## Conteúdo

### Natureza do Documento

Goldman Sachs Global Economics Analyst (26/03/2023). Tipo: análise econômica de banco de investimento — não peer-reviewed, mas citado extensamente em debate público sobre AI e economia. Autores: Joseph Briggs, Devesh Kodnani (Jan Hatzius como supervisor).

### Estimativas de Exposição

**Dois terços dos empregos atuais** estão expostos a "algum grau" de automação por AI.

**AI generativa poderia:**
- Expor ~25% do trabalho atual globalmente a automação potencial *(⚠️ Gate 3: o Goldman Sachs usa "substitute" mas isso é exposição de tarefas — substituição efetiva depende de adoção real e contexto econômico)*
- Equivalente a 300 milhões de empregos em tempo integral em risco de deslocamento

**Comparação com Eloundou et al. (2024):**
- Goldman Sachs: exposição via análise de tarefas ocupacionais (EUA + Europa)
- Eloundou: 80% de workforce com ≥10% de tarefas expostas
- Metodologias diferentes, ordens de magnitude similares

### Projeções de Produtividade e Crescimento

| Métrica | Projeção |
|---------|---------|
| Crescimento de produtividade do trabalho EUA | +1.5 pp/ano (sobre 10 anos pós-adoção) |
| PIB global | +7% eventualmente |
| ChatGPT — adoção (contexto março 2023) | 1 milhão de usuários em 5 dias — recorde ao momento da publicação *(⚠️ Gate 3: não mais válido como "mais rápida da história" — superado por produtos subsequentes)* |

### Características Distintivas de AI Generativa

Goldman Sachs distingue AI generativa de AI analítica/narrowly-focused anterior:
1. **Generalização:** aplicável a casos de uso amplos, não apenas tarefas específicas
2. **Geração:** produz outputs novos e criativos (texto, código, imagens)
3. **Acessibilidade:** interfaces em linguagem natural — barreira de uso muito menor

### Referências Históricas

- Padrão histórico: deslocamento de trabalhadores foi compensado por criação de empregos em novas ocupações
- Novas ocupações explicam a maioria do crescimento de emprego no longo prazo
- Comparação: adoção de MS-DOS → Windows como precedente de aceleração de adoção

### Dados Técnicos

- GPT-4 vs. GPT-3.5: +150 pontos no SAT, 40% mais preciso, aceita input visual
- Compute de treinamento: dobra a cada ~6 meses desde a década de 2010 (vs. Lei de Moore: ~18 meses)

### Qualificações Explícitas dos Autores

- "Significativa incerteza" em torno de capacidades de AI e implementação real
- Resultados dependem fortemente da dificuldade das tarefas que AI eventualmente realiza
- Timeline de adoção é altamente incerta
- Condições econômicas/políticas determinam adoção real (não só viabilidade técnica)

## Verificação adversarial

**Source_quality: medium** — não é peer-reviewed; é análise de banco de investimento com potencial incentivo para projeções otimistas (advocacy para AI como tese de investimento).

**Contraste com Acemoglu (2021):** usando dados similares sobre automação, Acemoglu chega a conclusão pessimista (danos, desigualdade), enquanto Goldman Sachs chega a conclusão otimista (produtividade, crescimento). A diferença está em: (1) quais efeitos de equilíbrio geral se assume; (2) se novos empregos compensarão deslocamento; (3) como se pondera efeitos distributivos.

**O que o relatório NÃO diz:**
1. Não modela efeitos distributivos — quem ganha e quem perde no +7% de PIB
2. Não tem modelo formal — é análise qualitativa + projeções baseadas em exposição ocupacional
3. Não tem horizonte temporal preciso para as projeções
4. Não foi submetido a peer review

## Interpretação

(⚠️ Zone 3 — domínio lateral. Interpretação intencionalmente vazia no ingest. Conexões com a KB emergem no /ask.)

## Conexões

## Fontes
- [Goldman Sachs (2023)](../../raw/papers/goldman-sachs-2023-ai-economic-growth.md) — Briggs/Kodnani; 300M empregos, +7% PIB global, +1.5pp produtividade; não peer-reviewed

## Quality Gate
- [x] Wikilinks tipados: nenhum — Zone 3
- [x] Instance→class: projeções qualificadas como estimativas de banco de investimento, não peer-reviewed
- [x] Meta-KB separado: nenhuma referência ao metaxon
- [x] Resumo calibrado: source_quality:medium reflete ausência de peer review
