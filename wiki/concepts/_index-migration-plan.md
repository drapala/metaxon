---
title: "_index.md Migration Plan"
type: meta-kb
created: 2026-04-04
updated: 2026-04-04
status: draft
trigger_condition: "Layer 1 /ask misses ≥2-3 relevant articles observably"
last_cluster_analysis: 2026-04-04
tags: [meta-kb, index, architecture, migration]
interpretation_confidence: medium
source_quality: medium
quarantine: false
---

## Resumo

Plano para dividir `_index.md` (51 entradas) em sub-índices temáticos quando o trigger for atingido. Baseado em análise empírica do grafo de wikilinks — não em intuição de domínio ou Bradford zones. **Não executar este plano até observar falhas reais de Layer 1.**

---

## Estado atual (2026-04-04)

51 artigos. Sem evidência observável de degradação de Layer 1 até o momento.

Comentário do `_index.md`: degradação de seleção esperada em ~50-80 entradas. Esse número é **extrapolação não validada** de ERL (seleção de heurísticas em Gaia2 agent tasks, domínio-transfer não testado). O sinal confiável é comportamental, não um threshold numérico.

---

## Metodologia: grafo real, não intuição

Antes de propor qualquer divisão, mapeamos o grafo de citações:

```bash
grep -roh '\[\[[^]]*\]\]' wiki/concepts/ | sed 's/\[\[//;s/\]\]//;s/|.*//' | sort | uniq -c | sort -rn
```

### In-degree real (citações recebidas por artigo)

**Top hubs (≥10 citações)**:

| Artigo | Citações | Cluster natural |
|--------|---------|----------------|
| agent-memory-architectures | 16 | Agents |
| self-improving-agents | 15 | Agents |
| kb-architecture-patterns | 15 | Meta-KB |
| autonomous-kb-failure-modes | 15 | Meta-KB |
| curation-anti-bias | 13 | Meta-KB |
| requisite-variety | 12 | Meta-KB |
| hybrid-search | 12 | Retrieval |
| memory-consolidation | 11 | Retrieval |
| llm-as-judge | 11 | Agents |
| information-theory-shannon ⚠️quarentena | 11 | Info-Theory |
| reflexion-weighted-knowledge-graphs | 10 | Agents |
| multi-agent-orchestration | 10 | Agents |
| context-management | 10 | Retrieval |
| tension-resolution | 9 | Agents |
| retrieval-augmented-generation | 9 | Retrieval |

**Medium (4-8 citações)**:

| Artigo | Citações | Cluster |
|--------|---------|---------|
| rate-distortion-theory | 7 | Info-Theory |
| llm-knowledge-base | 7 | Meta-KB |
| autonomous-research-agents | 7 | Agents |
| raptor-vs-flat-retrieval | 6 | Retrieval |
| groupthink-and-cascades | 6 | Meta-KB |
| team-decision-theory ⚠️quarentena | 5 | Info-Theory |
| question-taxonomy | 5 | Meta-KB |
| judgment-aggregation | 5 | Info-Theory |
| partial-information-decomposition | 4 | Info-Theory |
| network-information-theory | 4 | Info-Theory |
| fast-frugal-heuristics | 4 | Meta-KB |
| bradford-law-scattering | 4 | Meta-KB |

**Periferia (1-3 citações)** — maioria lateral domain:

| Artigo | Citações |
|--------|---------|
| variety-gap-analysis | 3 |
| information-bottleneck | 3 |
| formal-ontology-for-kbs | 3 |
| complexity-emergence | 3 |
| prospect-theory | 2 |
| immune-inspired-credit-assignment | 2 |
| complexity-stability-tradeoff | 2 |
| complementary-learning-systems | 2 |
| ceo-problem | 2 |
| causal-reasoning-pearl | 2 |
| viable-system-model-beer | 1 |
| scientific-research-programmes | 1 |
| resource-competition-coexistence | 1 |
| rational-inattention | 1 |
| obsidian-agent-workflow | 1 |
| heuristics-and-biases | 1 |
| falsificationism-demarcation | 1 |
| episodic-semantic-memory | 1 |

**Zero citações** (~10 artigos): lateral recém-ingeridos (social-choice-aggregation, zipf-law-power-laws, stigmergic-coordination, predictive-processing, pac-bayes-bounds, bibliometrics, etc.)

---

## Findings: o que o grafo revela

### 1. Os clusters intuitivos do /ask foram confirmados

Os 5 clusters propostos (Agents, Retrieval, Meta-KB, Info-Theory, Lateral) correspondem aos clusters reais de in-degree. As fronteiras são:

- Agents: hubs agent-memory(16), self-improving(15), llm-as-judge(11), reflexion(10), multi-agent(10)
- Retrieval: hubs hybrid-search(12), memory-consolidation(11), context-management(10), RAG(9)
- Meta-KB: hubs kb-architecture-patterns(15), autonomous-kb-failure-modes(15), curation-anti-bias(13), requisite-variety(12)
- Info-Theory: information-theory-shannon(11), rate-distortion(7), parcialmente team-decision(5)
- Lateral: periferia uniforme (0-3 citações)

### 2. information-theory-shannon é hub apesar de quarentenado

11 artigos citam shannon como referência fundacional do cluster info-theory. A quarentena impede novas conexões, mas 11 referências preexistentes já existem. Isso cria um **hub isolado**: o nó mais central do cluster está inacessível. Se shannon for promovido (critérios: L2 prediction ou prior work support), o cluster info-theory ganha coesão imediata.

⚠️ Implicação para promoção: shannon é o único caso onde a promoção teria impacto estrutural grande no grafo — não apenas "habilitar um artigo" mas "desbloquear um cluster".

### 3. Lateral domain é periferia uniforme — por enquanto

Os artigos da ingestão lateral (K&T, Arrow, May, Tilman, Popper, Lakatos, Tulving, McClelland) têm 0-2 citações. Isso é esperado: as conexões ainda não foram descobertas via /ask. À medida que sessões /ask acontecerem sobre os domínios laterais, os in-degrees aumentarão. A periferia de hoje é o middleware de amanhã.

**Sinal de quando o lateral maduro**: quando artigos como `complexity-stability-tradeoff` ou `episodic-semantic-memory` atingirem ≥4 citações, eles se tornaram bridges reais e devem aparecer nos sub-índices funcionais (não apenas no _index-lateral).

### 4. kb-architecture-patterns: hub com baixa qualidade factual

Score 26 no challenge, 0 claims survived. Ainda tem 15 citações. Isso significa que o artigo é estruturalmente central mas epistemicamente frágil. Na migração, deve estar no sub-índice — mas com aviso de qualidade baixa no pointer do _index.

---

## Proposta de sub-índices (a executar quando trigger atingido)

### _index-agents.md (~10 artigos)

Hubs: agent-memory-architectures, self-improving-agents, llm-as-judge, reflexion-weighted-knowledge-graphs, multi-agent-orchestration

Satélites: autonomous-research-agents, tension-resolution, immune-inspired-credit-assignment

### _index-retrieval.md (~7 artigos)

Hubs: memory-consolidation, hybrid-search, context-management, retrieval-augmented-generation

Satélites: raptor-vs-flat-retrieval, obsidian-agent-workflow, question-taxonomy

### _index-meta-kb.md (~12 artigos)

Hubs: autonomous-kb-failure-modes, curation-anti-bias, kb-architecture-patterns, requisite-variety

Satélites: llm-knowledge-base, groupthink-and-cascades, variety-gap-analysis, fast-frugal-heuristics, bradford-law-scattering, formal-ontology-for-kbs, causal-reasoning-pearl, bibliometrics

### _index-info-theory.md (~10 artigos)

Hub bloqueado: information-theory-shannon (quarentena — promover antes de migrar)

Satélites: rate-distortion-theory, information-bottleneck, partial-information-decomposition, network-information-theory, ceo-problem, team-decision-theory, rational-inattention, judgment-aggregation, pac-bayes-bounds

### _index-lateral.md (~15 artigos, cresce com expansão Zone 3)

Artigos com ≤3 citações que representam domínios distantes do core:
complexity-stability-tradeoff, resource-competition-coexistence, heuristics-and-biases, prospect-theory, social-choice-aggregation, zipf-law-power-laws, falsificationism-demarcation, scientific-research-programmes, episodic-semantic-memory, complementary-learning-systems, stigmergic-coordination, complexity-emergence, predictive-processing, viable-system-model-beer, obsidian-agent-workflow

**Regra de graduação**: quando artigo lateral atingir ≥4 citações, mover para o sub-índice funcional correspondente. O _index-lateral é um "viveiro", não uma categoria permanente.

---

## O _index.md principal pós-migração

Após a divisão, o `_index.md` principal vira:

```markdown
# Wiki Index

- [→ Agents](concepts/_index-agents.md) — agent memory, self-improvement, LLM-as-judge, RWKG
- [→ Retrieval & Architecture](concepts/_index-retrieval.md) — RAG, hybrid search, context management
- [→ Meta-KB](concepts/_index-meta-kb.md) — failure modes, curation, variety, epistemics
- [→ Information Theory](concepts/_index-info-theory.md) — Shannon, rate distortion, CEO, PID
- [→ Lateral Domains](concepts/_index-lateral.md) — ecology, behavioral econ, neuroscience, philosophy
```

Layer 1 = selecionar sub-índice correto (~5 entradas)
Layer 1.5 = ler sub-índice (~10-15 entradas)  
Layer 2 = artigo específico

Esse design evita o problema de selection accuracy — cada step fica dentro do threshold de seleção confiável.

---

---

## Modelo de graduação dinâmica

O sistema não é uma migração estática — é um fluxo contínuo baseado em in-degree:

```
/ingest (Zone 3) → _index-lateral (viveiro, 0-2 citações)
        ↓  via /ask sessions
≥4 citações acumuladas → graduação para sub-índice funcional correspondente
        ↓
Hub do cluster em quarentena? → bloqueio de migração do sub-índice
        ↓
/promote hub → sub-índice pode ser criado
```

**Regra de graduação**: artigo lateral atingindo ≥4 citações via /ask sessions = sinal de que conexões reais emergiram. Mover para sub-índice funcional. O _index-lateral é viveiro, não categoria permanente.

**Regra de bloqueio**: não criar sub-índice enquanto o hub do cluster estiver em quarentena. Um sub-índice com hub bloqueado é uma sala em torno de uma porta trancada.

---

## Estado atual dos clusters (2026-04-04)

Baseado em análise empírica de in-degree via grep do grafo de wikilinks.

| Cluster | Hub principal | Citações hub | Quarentena hub | Outros quarentenados no cluster | Migração |
|---------|--------------|-------------|---------------|-------------------------------|---------|
| **info-theory** | information-theory-shannon | 11 | ~~✅ ativa~~ **promovido** | team-decision-theory (5) | **desbloqueada** |
| **agents** | agent-memory-architectures | 16 | ❌ | reflexion-weighted-knowledge-graphs (10) | possível¹ |
| **retrieval** | hybrid-search | 12 | ❌ | raptor-vs-flat-retrieval (6) | possível² |
| **meta-kb** | autonomous-kb-failure-modes | 15 | ✅ ativa | — | **BLOQUEADA** |
| **lateral** | (viveiro) | 0-2 | causal-reasoning-pearl (2), immune-inspired (2) | N/A |

¹ reflexion-weighted-knowledge-graphs (10 citações) quarentenado = segundo hub do cluster agents bloqueado. Sub-índice agents pode ser criado mas com gap estrutural até RWKG ser promovido.

² raptor-vs-flat-retrieval (6 citações) quarentenado = bridge do cluster retrieval bloqueado. Sub-índice retrieval pode ser criado mas retrieval↔RAPTOR está isolado.

### Sequência recomendada de promoções antes de migrar

```
Prioridade 1: autonomous-kb-failure-modes (15 citações) — desbloqueia meta-kb, o cluster mais denso
Prioridade 2: reflexion-weighted-knowledge-graphs (10 citações) — completa agents  
Prioridade 3: raptor-vs-flat-retrieval (6 citações) — completa retrieval
Prioridade 4: team-decision-theory (5 citações) — completa info-theory (já desbloqueada)
Baixa prioridade: causal-reasoning-pearl (2), immune-inspired (2) — periféricos
```

---

## Trigger e pré-condições

**Não dividir até**:
1. `/ask` Layer 1 falhar observavelmente: respostas incompletas onde artigo correto estava no _index mas não foi selecionado (≥2-3 casos documentados)
2. Hub do cluster alvo promovido (ver tabela acima)
3. Artigos laterais com ≥4 citações identificados — eles determinam fronteiras reais

**Sequência correta**:
1. Observar falha de Layer 1
2. Identificar qual cluster falhou
3. Verificar se hub do cluster está em quarentena
4. Se sim: /promote hub primeiro
5. Criar sub-índice do cluster
6. Mover artigos com ≥4 citações do _index-lateral para o sub-índice

**Não dividir por**:
- Bradford zone (AI/ML vs lateral) — viola estrutura real do grafo
- Tema a priori sem suporte do grafo

---

## Conexões

- implements: [[kb-architecture-patterns]] ON "RAPTOR mid-level nodes via sub-indices"
- operationalizes: [[bradford-law-scattering]] ON "circuit breaker: parar na nucleus, reportar gap"
- applies: [[complexity-stability-tradeoff]] ON "modularity = May's stability solution — sub-índices são os módulos"
- blocked-by: [[information-theory-shannon]] ON "hub isolado bloqueia cluster info-theory"
