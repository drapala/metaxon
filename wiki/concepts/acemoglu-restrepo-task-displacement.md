---
title: "Task Displacement and Wage Inequality (Acemoglu & Restrepo)"
sources:
  - path: raw/papers/acemoglu-restrepo-2022-tasks-automation-wage-inequality.pdf
    type: paper
    quality: primary
    stance: neutral
created: 2026-04-08
updated: 2026-04-08
tags: [labor-economics, automation, wage-inequality, task-displacement, acemoglu, econometrica]
source_quality: high
interpretation_confidence: high
resolved_patches: []
provenance: source
---

## Resumo

Acemoglu & Restrepo (Econometrica, 2022) demonstram que deslocamento de tarefas por automação — não mudança tecnológica enviesada para habilidades (SBTC) — explica 50–70% das mudanças na estrutura salarial nos EUA entre 1980 e 2016. Automação reduziu salários reais de trabalhadores sem diploma em até 8.8%, ao mesmo tempo que o ganho de produtividade agregada foi modesto (3.4% de TFP). O paper introduz o conceito de "ripple effects" que propagam o impacto salarial além dos diretamente deslocados.

## Conteúdo

### Framework: Deslocamento de Tarefas vs. SBTC

A literatura anterior explicava a desigualdade salarial crescente pela hipótese SBTC (*skill-biased technological change*): tecnologia aumenta a demanda relativa por trabalhadores qualificados, elevando o prêmio de qualificação. Acemoglu & Restrepo propõem que o mecanismo é diferente:

**Deslocamento de tarefas:** quando tecnologias de automação assumem tarefas antes executadas por um grupo de trabalhadores, a demanda por esse grupo cai — mesmo que a tecnologia aumente a produtividade agregada.

Distinção crítica:
- SBTC: muda a produtividade relativa dos trabalhadores → altera salários via demanda por habilidades
- Deslocamento: elimina tarefas do grupo deslocado → reduz salários *independentemente* da produtividade

### Achados Principais

**Contribuição do deslocamento de tarefas:**
- 50–70% das mudanças na estrutura salarial (1980–2016) explicadas por deslocamento de tarefas via automação *(⚠️ Gate 3: estimativa dependente do modelo — não consenso da literatura)*
- Prêmio universitário (college premium): ~80% explicado por automação *(⚠️ Gate 3: estimativa específica a este framework, não estabelecida como fato em outros estudos)*

**Efeitos sobre salários reais (1980–2016):**
- Homens sem ensino médio completo: −8.8% *(contribuição modelada da automação, não variação salarial total observada)*
- Mulheres sem ensino médio completo: −2.3%

**Ganho de produtividade:**
- Crescimento cumulativo de TFP atribuível à automação: ~3.4% (1980–2016) *(⚠️ Gate 3: dependente de medição e modelo)*
- Contraste: grandes perdas distributivas para modestos ganhos agregados

**Robustez a controles alternativos:** A relação entre deslocamento de tarefas e mudanças salariais permanece forte após incluir simultaneamente:
- Poder de mercado das firmas
- Desindicialização
- Importações da China
- Outros tipos de aprofundamento de capital

*(⚠️ Gate 3: esses fatores explicam parte da variância da desigualdade — a afirmação é que o deslocamento de tarefas domina e é robusto a eles como controles, não que eles sejam irrelevantes.)*

### Metodologia

**Framework conceitual:**
- 500 grupos demográficos (educação × gênero × idade × raça × natividade)
- Medida de deslocamento: declínio na participação do trabalho industrial + proxies de automação
- Proxies de automação: adoção de robôs, software especializado, maquinário dedicado

**Identificação:**
- Relaciona medidas de deslocamento de tarefas a mudanças salariais por grupo demográfico
- Simulação de equilíbrio geral com efeitos de composição setorial e ripple effects

**Dados:** 1980–2016, múltiplas fontes (Census, CPS, IFR para robôs)

### Ripple Effects

Automação afeta não apenas os trabalhadores diretamente deslocados:
- Trabalhadores em indústrias adjacentes enfrentam maior oferta de trabalhadores deslocados
- Pressão descendente sobre salários se propaga através de mercados de trabalho relacionados
- Efeito total sobre desigualdade é maior que o efeito direto isolado

### Relação com Offshoring

- Offshoring tem efeitos similares ao deslocamento por automação, mas menores em magnitude
- Automação é o canal predominante de deslocamento de tarefas nos EUA 1980–2016

## Verificação adversarial

**Claim mais forte (e mais discutido):** 50–70% da mudança na estrutura salarial explicada por automação. Esse número é alto e requer que deslocamento de tarefas seja o mecanismo dominante — acima de poder de mercado, desindicialização e China, todos incluídos como controles. O paper usa robustez extensiva, mas as proxies de automação (robôs, software, maquinário) podem capturar outros aspectos de mudança tecnológica.

**O que o paper NÃO diz:**
1. Não modela criação de novos empregos e tarefas por novas tecnologias
2. Não prevê trajetória futura — é análise histórica 1980–2016
3. Não implica que automação é indesejável — modesto TFP growth + grandes ganhos de lucro das firmas não são quantificados

**Simplificações:** A medida de deslocamento é construída a partir de declínios observados na participação do trabalho industrial — assume que esses declínios refletem automação, não outros fatores. Robustez com proxies alternativas é apresentada.

## Interpretação

(⚠️ Zone 3 — domínio lateral. Interpretação intencionalmente vazia no ingest. Conexões com a KB emergem no /ask.)

## Conexões

## Fontes
- [Acemoglu & Restrepo (2022)](../../raw/papers/acemoglu-restrepo-2022-tasks-automation-wage-inequality.md) — Econometrica 90(5); task displacement framework; 500 demographic groups; ripple effects

## Quality Gate
- [x] Wikilinks tipados: nenhum — Zone 3
- [x] Instance→class: achados qualificados como análise histórica EUA 1980–2016
- [x] Meta-KB separado: nenhuma referência ao metaxon
- [x] Resumo calibrado: source_quality:high — Econometrica, peer-reviewed
