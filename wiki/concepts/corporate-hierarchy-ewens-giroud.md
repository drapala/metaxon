---
title: "Corporate Hierarchy — Ewens & Giroud (2025)"
sources:
  - path: raw/papers/ewens-giroud-2025-corporate-hierarchy.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-06
updated: 2026-04-06
tags: [organization-design, hierarchy, ai-coordination, empirical, span-of-control, knowledge-hierarchy]
source_quality: high
interpretation_confidence: high
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: source
quarantine: false
quarantine_promoted: 2026-04-06
quarantine_criteria_met:
  auto_promote: true
  gates_passed: [1, 2, 3, 4]
  gate3_models: [gpt-5.4, gemini-3.1-pro-preview]
  gate3_claims_challenged: 8
  gate3_claims_survived: 3
  gate3_claims_weakened: 5
  gate3_claims_invalidated: 0
  gate3_correction_applied: "industry ordering inconsistency fixed"
  challenge_verdict: PUBLICÁVEL
---

## Resumo

Ewens & Giroud (2025) introduzem a primeira medida abrangente de hierarquia corporativa para firmas públicas americanas, construída a partir de 7 milhões de currículos no LinkedIn de 3.128 empresas (2016–2023). Documentam que firmas têm em média 9,5 camadas hierárquicas, estrutura piramidal, e que hierarquias se achataram após adoção de AI. Resultados são correlacionais, não causais.

## Conteúdo

### Dados e Metodologia

- **Amostra:** 3.128 firmas públicas U.S. (Compustat 2015+, excluindo utilities, varejo, companhias aéreas por cobertura inadequada no LinkedIn)
- **Fonte:** CoreSignal — dados de LinkedIn; 7M+ workers únicos, 8,7M transições de cargo 2017–2023
- **Cobertura:** LinkedIn cobre 49% do headcount Compustat para firma mediana (viés em favor de perfis gerenciais e profissionais com perfil público)
- **Algoritmo:** Huitfeldt, Kostøl, Nimczik & Weber (2023) — Minimum Violation Ranking (MVR): infere ranking de cargos a partir de padrões de promoção e movimentos laterais; k-means para clustering em camadas
- **Limitação estrutural:** Hierarquias são estáveis — apenas 18% das firmas mudaram de número de camadas durante 2016–2023; 3,9% das observações firma-ano apresentam mudança. Quando mudam, 75% das vezes é aumento (mediana: +1 camada). Isso limita poder estatístico de testes com firm fixed effects.

### Fatos Descritivos sobre Hierarquias

- Média de **9,5 camadas hierárquicas** por firma (mediana 8) — substancialmente acima dos 4 camadas máximas da literatura anterior baseada em occupation codes
- Estrutura **piramidal** confirmada: mais trabalhadores nas camadas inferiores em todos os setores
- **Tendência secular de achatamento:** média caiu de ~10,4 em 2015 para ~10,1 em 2023; mediana caiu de 9 para 8 em torno de 2017 (Figura 1)
- Variação setorial: Manufacturing (~13–14 camadas) > IT (~12) > Instruments (~10) > Finance (~8) > Construction/Chemicals (~6–7) — variação dentro de setores é maior que variação ao longo do tempo
- Tamanho de firma explica >70% da variação em camadas (R² em regressões); mas variação residual é substancial e é o que os autores exploram

### Outcomes Correlacionados com Hierarquia (Seção 7)

**Autores avisam explicitamente: resultados são correlacionais — não causais.**

Mais camadas associadas com:
- Maior ROA, margem bruta, margem líquida (+performance operacional)
- Maior SG&A (custo administrativo de manter hierarquia)
- Mais patentes, mesmo número de patentes de alta qualidade (sem diferença em citações)
- Mais aquisições (não diversificantes)
- Menor volatilidade de retorno de ações (menor risco operacional, não financeiro)
- CEO pay ratio maior (maior desigualdade salarial interna)
- Workforce mais educada, maior taxa de promoção interna, tenure mais longa

### Determinantes de Hierarquia (Seção 8)

**8.2 — Pandemia Covid:**
Firmas farmacêuticas (SIC 2834) aumentaram camadas em ~4% no período pós-Covid (choque de demanda + complexidade). Difference-in-differences com firm e year fixed effects; pre-trends insignificantes.

**8.3 — Adoção de AI (achado central para a KB):**
- AI mensurada via Babina, Fedyk, He & Hodson (2024): 4 métricas baseadas em job postings com requisitos AI (broad/narrow) e AI skills
- **Firmas com maior adoção de AI têm menos camadas hierárquicas**
- Significativo a **10%** em todas as 4 métricas de AI adoption
- Testes são "**under-powered**" (own description): firm fixed effects reduzem poder por causa da estabilidade das camadas dentro de firmas
- Mecanismo proposto (teórico): AI reduz custo de aquisição de conhecimento → menos "problem solvers" (gestores de médio escalão) necessários → achatamento
- Robusto a long differences: regredindo Δlog(camadas) sobre ΔAI confirma resultados de Table 12

### Relação com Literatura

- Primeira medida abrangente de hierarquia para firmas públicas U.S. (literatura anterior: ~300 firmas via surveys Hewitt Associates)
- Confirma "flattening firm" de Rajan & Wulf (2006) e Guadalupe & Wulf (2010), agora com hierarquia completa (não apenas topo)
- Consistente com Garicano (2000): AI como redução de custo de conhecimento → menos camadas
- Consistente com Bolton & Dewatripont (1994): melhor processamento de informação → menos delegação

## Interpretação

(⚠️ nossa interpretação) O paper fornece a âncora empírica que o manifesto Block pressupõe ("hierarquia = protocolo de roteamento que AI substitui") mas não documenta. Ewens & Giroud confirmam correlacionalmente o achatamento hierárquico pós-AI para 3.128 firmas reais — não apenas uma newsroom simulada como Farach.

(⚠️ nossa interpretação) O caveat "under-powered / 10% significance" é importante: a limitação não é o dado mas a variação observável. Hierarquias mudam lentamente (3,9% firma-ano). O efeito existe mas é de difícil detecção precisamente porque a variável dependente é quase categórica entre observações.

(⚠️ nossa interpretação) A cobertura bias do LinkedIn é preocupante para interpretações sobre trabalhadores de base: se 49% do headcount vem de perfis de LinkedIn, e esses perfis são maioritariamente gerenciais, o achatamento medido pode estar capturando apenas o topo da hierarquia — exatamente o que Rajan & Wulf (2006) já documentavam. A contribuição empírica sobre AI pode ser mais fraca do que parece.

## Verificação Adversarial

**Claim mais fraco:** AI adoption → hierarchy flattening. Apenas 10% de significância com testes "under-powered". Correlação não causal: firmas que adotam AI mais agressivamente podem ter outras características que predizem achatamento (seleção).

**O que o paper NÃO diz:**
- Não afirma que AI causa achatamento hierárquico — só que há correlação
- Não identifica se o achatamento beneficia mais o topo ou a base da hierarquia
- Não testa o mecanismo (compressão de coordenação vs. automação de tarefas)

**Simplificações feitas:** O resumo deste artigo não captura a extensão das limitações de cobertura do LinkedIn para inferir hierarquia de firmas reais. A amostra tilts fortemente para firmas grandes.

**Prior work:** Rajan & Wulf (2006), Guadalupe & Wulf (2010), Caliendo et al. (2015) — todos cobrem flattening, mas para amostras menores ou aspectos parciais da hierarquia.

## Quality Gate
- [x] Wikilinks tipados: 3 substituições
- [x] Instance→class: claims quantitativos qualificados (9,5 camadas = média da amostra, não lei)
- [x] Meta-KB separado: interpretações em seção própria
- [x] Resumo calibrado: "correlacionais, não causais" explícito

## Conexões

- validates: [[block-organization-as-intelligence]] — confirma empiricamente o achatamento hierárquico pós-AI que o manifesto Block propõe como tese design; 3.128 firmas vs. argumento retórico
- validates: [[ai-coordination-compressing-capital]] — fornece base empírica para P3 de Farach (redução de gestores com AI adoption); resolve o caveat "Ewens & Giroud é evidência emergente"
- derivedFrom: [[requisite-variety]] — hierarquia existe para resolver gap V(gestor) < V(equipe); AI reduz esse gap direto
- complementa: [[viable-system-model-beer]] — 9,5 camadas médias são o VSM real antes de AI; tendência de achatamento é S3/S4 sendo absorvidos por AI

## Fontes

- [Ewens & Giroud (2025) — Corporate Hierarchy](../../raw/papers/ewens-giroud-2025-corporate-hierarchy.md) — medida de hierarquia para 3.128 firmas U.S. via LinkedIn; achado principal: AI adoption → hierarchy flattening (corr. 10%)
