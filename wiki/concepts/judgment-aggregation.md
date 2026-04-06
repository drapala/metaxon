---
title: "Judgment Aggregation (List & Pettit 2002)"
sources:
  - path: raw/papers/list-pettit-judgment-aggregation.md
    type: paper
    quality: primary
    stance: challenging
created: 2026-04-04
updated: 2026-04-04
tags: [decision-theory, social-choice, impossibility, multi-agent, collective-rationality, lateral]
source_quality: high
interpretation_confidence: high
quarantine: false
resolved_patches: []
reads: 1
retrievals_correct: 1
retrievals_gap: 0
last_read: 2026-04-05
provenance: source
---

## Resumo

List & Pettit (2002): Theorem 1 (impossibilidade) — não existe função de agregação de julgamentos que satisfaça simultaneamente Universal Domain + Anonymity + Systematicity e gere julgamentos coletivos completos, consistentes e dedutivamente fechados. Análogo a Arrow para preferências, mas para **julgamentos lógicos interconectados**. Escape routes: restringir domínio (alinhamento unidimensional) ou abrir mão de anonymity/systematicity. Desafio direto a qualquer KB que usa votação majoritária para agregar claims.

## Conteúdo

### O problema de agregação de julgamentos

Grupos frequentemente precisam formar julgamentos coletivos sobre questões interconectadas logicamente. Diferente de agregar preferências (Arrow): aqui os itens são proposições lógicas, não opções independentes.

**Distinção central** (List & Pettit 2002, §1):
- **Agregação de preferências** (Arrow): ranqueamento de alternativas independentes → impossibilidade de Condorcet
- **Agregação de julgamentos**: aceitação/rejeição de proposições **logicamente conectadas** → paradoxo distinto

### O paradoxo doutrinário (§2)

**Caso jurídico** (Kornhauser & Sager 1993, citado em List & Pettit):

| Juiz | Contrato válido? | Violação? | Responsável? |
|------|-----------------|-----------|--------------|
| 1    | sim             | não       | não          |
| 2    | não             | sim       | não          |
| 3    | sim             | sim       | **sim**      |
| **Maioria** | **sim** | **sim** | **não** |

**Paradoxo**: A maioria aceita cada premissa (contrato válido: 2-1; violação: 2-1), mas a conclusão lógica (responsável = premissa₁ ∧ premissa₂) não tem maioria (1-2).

Dois procedimentos possíveis:
- **Conclusion-driven**: vota na conclusão diretamente → réu absolvido (sem maioria)
- **Premise-driven**: vota nas premissas, deriva conclusão logicamente → réu condenado

Os dois procedimentos **geram resultados opostos** com os mesmos votos individuais.

### Teorema de impossibilidade (§3, Theorem 1)

**Condições** (List & Pettit 2002, §3):

**Universal Domain (U)**: F aceita qualquer perfil de julgamentos individuais completos, consistentes e dedutivamente fechados.

**Anonymity (A)**: O julgamento coletivo F({Σᵢ}) é invariante sob permutações de indivíduos. (Nenhum indivíduo tem peso especial.)

**Systematicity (S)**: Para quaisquer duas proposições φ e ψ, se cada indivíduo faz o mesmo julgamento sobre φ que sobre ψ, então o coletivo também. (Proposições tratadas igualmente; o julgamento coletivo sobre φ depende só dos julgamentos individuais sobre φ.)

**Theorem 1** (List & Pettit 2002):

> Não existe função de agregação de julgamentos F que: (a) gere julgamentos coletivos completos, consistentes e dedutivamente fechados, e (b) satisfaça Universal Domain, Anonymity e Systematicity.

**Prova (sketch)**: Com votação majoritária sob U+A+S, o paradoxo doutrinário é construtível em qualquer domínio com proposições logicamente interconectadas (P, Q, P∧Q). A "maioria" em cada proposição pode divergir da "maioria" na conjunção. Qualquer outra função satisfazendo U+A+S cai no mesmo problema.

### Teorema de possibilidade (Theorem 2 — escape route)

**Unidimensional Alignment** (List 2001, citado em List & Pettit):

Uma profile é unidimensionalmente alinhada se os indivíduos podem ser ordenados linearmente tal que, para cada proposição, os que aceitam estão todos à direita (ou todos à esquerda) dos que rejeitam.

**Theorem 2** (List 2001, via List & Pettit):

> No domínio de profiles unidimensionalmente alinhados com número ímpar de indivíduos, existe F satisfazendo A + S e gerando julgamentos coletivos completos, consistentes e dedutivamente fechados.

Isso é análogo à condição de Single-Peaked Preferences de Black (1948) para Arrow.

### Escape routes (§4)

1. **Restringir domínio (U)**: aceitar apenas profiles unidimensionalmente alinhados. Requer convergência prévia de visões. Factível com deliberação estruturada.

2. **Abrir mão de Anonymity**: dar peso diferente a indivíduos (especialistas, hierarquia). Introduz assimetrias desejáveis mas perde igualdade epistémica.

3. **Abrir mão de Systematicity**: usar procedimentos diferentes para proposições diferentes (e.g., maioria para premissas, supermaioria para conclusões). Permite consistência mas requer regras de meta-procedimento.

4. **Conclusion-driven vs premise-driven**: aceitar que grupos decidem *ora* pela premissa *ora* pela conclusão, não pela combinação. Abdica da deductive closure.

5. **Abrir mão de Completeness/Consistency**: abstain em alguns casos. Gera julgamentos coletivos incompletos mas evita inconsistência.

## Interpretação

### Desafio direto a KBs com votação de claims

⚠️ Interpretação nossa — não está em List & Pettit.

Em KBs multi-agent onde múltiplos LLMs votam em claims:
- Cada LLM produz julgamentos completos, consistentes e fechados individualmente
- Mas a KB resultante pode ser logicamente inconsistente se usa votação por claim isolado (systematicity sem deductive closure coletiva)
- O paradoxo doutrinário é concretamente: LLM₁ aceita "X implica Y", LLM₂ aceita "X", mas a maioria rejeita "Y"

**Implicação de design**: um KB multi-agent que usa votação majoritária claim-by-claim viola Theorem 1 — o resultado coletivo pode ser logicamente inconsistente mesmo que cada compilador seja internamente consistente.

### Relação com groupthink e cascades

List & Pettit (2002) é um problema estrutural/lógico; Janis (1972) é um problema social/psicológico. São complementares:
- Groupthink: agentes convergem socialmente para um consenso errado (pressão)
- Judgment aggregation: mesmo sem pressão social, a agregação de julgamentos lógicos tem impossibilidade estrutural

A solução de Janis (devil's advocate, voto secreto) não resolve o impossibility theorem — mesmo com votos independentes e honestos, o paradoxo persiste.

## Verificação adversarial

**Claim mais fraco:** A condição de Systematicity é "somewhat controversial" (List & Pettit 2002, §3) — requer que a dependência coletivo→individual seja idêntica para todos os pares de proposições. Esta é uma condição muito forte que procedimentos práticos geralmente não satisfazem.

**O que o paper NÃO diz:**
- Não afirma que grupos *não podem* agregar julgamentos — afirma que qualquer F que satisfaça U+A+S falha
- Não discute grupos com expertise heterogênea (a solução "abrir mão de A" pode ser normativa)
- Não trata de proposições probabilísticas (credences) — apenas julgamentos binárias

**Simplificações:** O modelo assume proposições com lógica proposicional clássica; julgamentos em domínios com lógica fuzzy ou incerteza requerem extensões.

**Prior work:** Arrow (1963) — impossibility para preferências. Kondorcet (séc XVIII) — paradoxo do Condorcet para votação em alternativas. Kornhauser & Sager (1986, 1993) — doctrinal paradox em jurisprudência. List & Pettit (2002) é a formulação geral e prova formal.

## Quality Gate
- [x] Wikilinks tipados: `contradicts: [[multi-agent-orchestration]] ON "votação majoritária claim-by-claim pode gerar inconsistência coletiva"`; `complementsAt: [[groupthink-and-cascades]] ON "impossibility estrutural vs pressão social"`; `complementsAt: [[curation-anti-bias]] ON "anonymity = tratamento igual de compiladores é necessário para fairness mas não suficiente para consistência"`
- [x] Instance→class: Theorem 1 é sobre U+A+S — não é afirmação geral de que grupos não agregam julgamentos
- [x] Meta-KB separado: implicações para KB multi-agent em ## Interpretação
- [x] Resumo calibrado: "desafio direto" qualificado como interpretação nossa

## Níveis epistêmicos

### Descrição (verificado)
- Paradoxo doutrinário com exemplo 3-juízes — do paper
- Theorem 1 (impossibilidade U+A+S) — provado no appendix do paper
- Theorem 2 (possibilidade com unidimensional alignment) — citado de List 2001
- 5 escape routes — discutidas no paper

### Interpretação (nossa aplicação)
- Aplicação a KB multi-agent com votação de claims — nossa interpretação
- Relação com groupthink: complementar, não idêntico — nossa síntese

### Especulação
- (nenhuma)

## Conexões

- emerge-para: [[modular-escape-principle]] ON "premise-based procedure como escape de impossibilidade U+A+S — isomorfismo com escapes de May e Bradford"
- contradicts: [[multi-agent-orchestration]] ON "voting por claim isolado viola deductive closure coletiva (⚠️ nossa interpretação de Theorem 1)"
- complementsAt: [[groupthink-and-cascades]] ON "impossibility estrutural (List & Pettit) vs pressão social (Janis) — mesmo sem pressão, agregação de julgamentos lógicos é problemática"
- complementsAt: [[curation-anti-bias]] ON "anonymity preserva fairness mas não garante consistência lógica coletiva"

## Fontes

- [List & Pettit (2002) — Aggregating Sets of Judgments: An Impossibility Result](../../raw/papers/list-pettit-judgment-aggregation.md) — paradoxo doutrinário, Theorem 1 (impossibilidade), Theorem 2 (unidimensional alignment), escape routes
