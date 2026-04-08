---
title: "GPT Labor Market Exposure (Eloundou et al.)"
sources:
  - path: raw/papers/eloundou-et-al-2024-gpts-are-gpts-labor-market.pdf
    type: paper
    quality: primary
    stance: neutral
created: 2026-04-08
updated: 2026-04-08
tags: [labor-economics, llm, gpt, automation, general-purpose-technology, occupational-exposure]
source_quality: high
interpretation_confidence: high
resolved_patches: []
provenance: source
---

## Resumo

Eloundou et al. (2024) aplicam análise de exposição ocupacional a LLMs usando O*NET (19.265 tarefas × 1.016 ocupações). Achado central: ~80% dos trabalhadores americanos têm ≥10% de suas tarefas expostas a LLMs; ~19% têm ≥50% expostas. Ao contrário de ondas anteriores de automação, empregos de maior renda mostram maior exposição. Com ferramentas e software complementares, 47–56% de todas as tarefas são afetadas.

## Conteúdo

### Definição: LLMs como Tecnologia de Uso Geral (GPT)

O título é um trocadilho: "GPTs are GPTs" — *large language models* (GPTs) são *general-purpose technologies* (GPTs). Tecnologias de uso geral têm três características:
1. **Pervasividade:** aplicáveis em muitos setores e tarefas
2. **Melhoria contínua:** performance aumenta ao longo do tempo
3. **Inovações complementares:** geram novas tecnologias e usos que amplificam impacto

LLMs satisfazem as três características, segundo os autores *(⚠️ Gate 3: essa é uma hipótese dos autores sobre trajetória futura, não fato estabelecido — o enquadramento como GPT é argumento analítico, não empiricamente verificado)*.

### Metodologia

- **Rubrica de exposição:** Avalia se LLM pode completar, reduzir o tempo de, ou aumentar a qualidade de cada tarefa O*NET
- **Anotadores:** Combinação de anotadores humanos + GPT-4 para classificar exposição
- **Base:** 19.265 tarefas × 2.087 atividades de trabalho detalhadas × 1.016 ocupações
- **Dados de emprego/salário:** BLS 2020–2021
- **Validação:** Correlação com medidas de exposição tecnológica anteriores (Acemoglu-Autor, Felten) — explica 60–72% da variância nessas medidas *(⚠️ Gate 3: essa é correlação entre medidas de exposição, não validação contra resultados históricos de emprego reais)*

### Medidas de Exposição

**Nível 1 — Acesso direto ao LLM:**
| Grupo | % workforce |
|-------|-------------|
| ≥10% das tarefas expostas | ~80% |
| ≥50% das tarefas expostas | ~19% |
| ~15% *das tarefas* (não da workforce) completas 2× mais rápido com LLM | *(⚠️ Gate 3: unidade = tarefas, não trabalhadores)* |

**Nível 2 — LLM + ferramentas/software complementares:**
| Medida | Resultado |
|--------|-----------|
| % de todas as tarefas afetadas | 47–56% |

### Padrões por Salário (Inversão de Tendência)

**Achado contrastante com automação anterior:**
- Automação industrial/robôs: deslocou principalmente trabalhadores de menor renda e tarefas rotineiras manuais
- LLMs: exposição é MAIOR em ocupações de maior renda

Isso implica que LLMs têm potencial de afetar trabalho cognitivo e profissional de forma mais intensa que trabalho manual — padrão diferente da automação industrial anterior *(⚠️ Gate 3: "reversão do padrão histórico" seria afirmação forte; o paper documenta exposição técnica, não deslocamento realizado)*.

### Padrões por Habilidade

| Habilidade | Correlação com exposição |
|------------|--------------------------|
| Programação | Positiva |
| Escrita | Positiva |
| Ciências | Negativa |
| Pensamento crítico | Negativa |

Ocupações com maiores barreiras de entrada mostram *fraca* maior exposição.

### Variação por Indústria

- **Alta exposição:** processamento de informação, serviços financeiros, consultoria
- **Baixa exposição:** manufatura, agricultura, mineração

### O que Este Estudo Mede e o que Não Mede

**Mede:**
- Viabilidade técnica de LLMs para completar tarefas
- Potencial de exposição laboral

**NÃO mede:**
- Deslocamento real de trabalhadores (distinção entre augmentação e substituição)
- Timelines de adoção
- Efeitos de equilíbrio geral (novos empregos criados)
- Fatores regulatórios, organizacionais, políticos que determinam adoção real

## Verificação adversarial

**Claim mais fraco:** A rubrica de exposição é construída por anotadores humanos + GPT-4 — o modelo sendo avaliado também participa da avaliação. Isso cria potencial de viés de auto-avaliação (self-enhancement bias, documentado na literatura de LLM-as-judge). Os autores usam validação externa, mas o viés não é totalmente eliminado.

**O que o paper NÃO diz:**
1. Não prevê desemprego em massa — exposição técnica ≠ substituição real
2. Não quantifica se LLMs serão labor-augmenting ou labor-displacing por ocupação
3. Não modela criação de novas tarefas e ocupações que LLMs podem gerar

## Interpretação

(⚠️ Zone 3 — domínio lateral. Interpretação intencionalmente vazia no ingest. Conexões com a KB emergem no /ask.)

## Conexões

## Fontes
- [Eloundou et al. (2024)](../../raw/papers/eloundou-et-al-2024-gpts-are-gpts-labor-market.md) — OpenAI/UPenn; O*NET rubric; 80% workforce ≥10% exposed; inversão salarial vs. automação anterior

## Quality Gate
- [x] Wikilinks tipados: nenhum — Zone 3
- [x] Instance→class: achados qualificados como medida de viabilidade técnica, não deslocamento real
- [x] Meta-KB separado: nenhuma referência ao metaxon
- [x] Resumo calibrado: source_quality:high — paper publicado, metodologia validada
