---
title: "Multiagent Debate for Factuality and Reasoning (Du et al. 2023)"
sources:
  - path: raw/papers/multiagent-debate-factuality.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-05
updated: 2026-04-05
tags: [multiagent, evaluation, factuality, reasoning, llm-judge, autoresearch]
source_quality: medium
interpretation_confidence: medium
resolved_patches:
  - date: 2026-04-05
    patch: "Claim 'avaliadores mutuamente independentes' qualificado: independência é de histórico de conversação, não de priors epistêmicos — suportado por arXiv:2505.19184 e OpenReview:sy7eSEXdPC"
    source: challenge-multiagent-debate-du-2023-hook
  - date: 2026-04-05
    patch: "Claim 'melhora significativamente' qualificado: válido nos benchmarks originais Du et al. 2023; evidência pós-2023 (arXiv:2509.05396, ICLR Blogpost 2025) mostra resultados mistos em comparação com CoT/self-consistency"
    source: challenge-multiagent-debate-du-2023-hook
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: true
quarantine_created: 2026-04-05
quarantine_reason: "novo ingest — aguarda review frio"
provenance: source
---

## Resumo

Du et al. (2023) propõem substituir o padrão de geração-e-auto-avaliação por um protocolo em que múltiplas instâncias do mesmo LLM geram respostas independentes, leem as respostas dos demais e debatem por múltiplos rounds até convergência. O resultado é melhoria significativa em raciocínio matemático e estratégico, além de redução de respostas falaciosas e alucinações. O mecanismo é uma resposta de sistemas distribuídos ao self-enhancement bias documentado em avaliações single-agent.

## Conteúdo

### Mecanismo central

O protocolo de debate multi-agente opera em três etapas repetidas por múltiplos rounds:

1. **Geração independente:** cada instância do LLM produz uma resposta sem acesso às respostas das demais
2. **Leitura cruzada:** cada instância lê as respostas de todas as outras instâncias
3. **Debate e convergência:** as instâncias atualizam suas respostas considerando as divergências — o processo converge para consenso ao longo dos rounds

O contraste central com o paradigma single-agent: em vez de um LLM gerar e auto-avaliar (com self-enhancement bias documentado), múltiplas instâncias com históricos de conversação distintos funcionam como avaliadores com independência de contexto — embora compartilhem priors epistêmicos do mesmo corpus de treinamento (limitação documentada em trabalho subsequente).

### Resultados

Nos benchmarks originais do paper, o método melhora:
- **Raciocínio matemático e estratégico**
- **Validade factual** (redução de respostas falaciosas)
- **Taxa de alucinações**

*Nota: o paper completo (arXiv:2305.14325) contém benchmark results detalhados e especificações do protocolo de debate. O conteúdo acima é baseado no abstract e conteúdo disponível em raw/. Evidência pós-2023 (incluindo avaliações ICLR 2025) mostra resultados mistos: muitos frameworks MAD não superam consistentemente chain-of-thought ou self-consistency em benchmarks independentes.*

### Distinção do paradigma single-agent

O design single-agent com self-enhancement cria um loop: o mesmo modelo que gerou o conteúdo é o que avalia se está correto. Du et al. quebram esse loop estruturalmente — o "avaliador" (outra instância) não tem acesso ao histórico de geração da instância avaliada na rodada inicial, produzindo um sinal de feedback com maior independência epistêmica do que self-reflection pura.

### Tensão com coordenação multi-agente

Cognition (documentado por Tim Kellogg) critica sistemas multi-agente por criarem "sistemas frágeis" com "decision-making disperso". Multiagent debate resolve o problema de bias mas introduz custo de coordenação e fragmentação de contexto. Nenhuma das abordagens domina a outra — a escolha depende se o risco de bias (single-agent) ou de fragilidade de coordenação (multi-agent) é maior para o caso de uso específico.

## Interpretação

(⚠️ nossa interpretação) **Multiagent debate como middle ground para /review autônomo:** A KB opera com o mesmo LLM ingerindo e revisando artigos — exatamente o padrão single-agent com self-enhancement bias que CALM documenta em 16.1% de erro. Multiagent debate propõe o fix estrutural: múltiplas instâncias com contextos distintos avaliando cada artigo de forma independente, debatendo divergências antes de convergir. Isso satisfaz parcialmente o Pilar 1 do [[autoresearch-reliability-triad]] (grounded test via oracle externo) sem requerer human-in-the-loop permanente.

(⚠️ nossa interpretação) **"Parcialmente" é a caveata crítica:** instâncias do mesmo modelo treinadas no mesmo corpus compartilham priors. Se o erro original é de viés sistêmico do modelo (e não de viés do histórico de conversação), múltiplas instâncias convergirão para o mesmo erro. [[autonomous-kb-failure-modes]] documenta esta limitação: independência epistêmica decresce com overlap de training data. A opção mais robusta continua sendo validação computacionalmente executável (testes, queries SQL, APIs com resultado determinístico).

(⚠️ nossa interpretação) **Relação com evaluation-order-independence:** o protocolo de debate gera julgamentos independentes *antes* da leitura cruzada — equivalente estrutural ao sequestro-de-referência proposto em [[evaluation-order-independence]]. A rodada de debate subsequente é análoga ao momento de revisão após julgamento independente formado. O design de Du et al. empiricamente implementa o princípio que [[evaluation-order-independence]] derivou por análise causal (Pearl L2).

## Conexões

- [[autonomous-kb-failure-modes]] — "Multiagent Debate as Middle Ground": Du et al. citado como quarta opção de mitigação, ao lado de modelo diferente para /review, human spot-checks e validação executável
- [[autoresearch-reliability-triad]] — Pilar 1 (grounded test): multiagent debate como instância de oracle não-humano para hipóteses KB-teóricas; equivalência com oracle externo não verificada empiricamente
- [[llm-as-judge]] — self-enhancement bias (16.1%) é o problema que multiagent debate resolve estruturalmente; debate multi-instância como antídoto ao single-evaluator circular
- [[groupthink-and-cascades]] — tensão: múltiplos agentes do mesmo modelo podem convergir para groupthink se compartilharem priors; Janis prescreve devil's advocate como estrutura separada, não apenas maioria
- [[evaluation-order-independence]] — design do protocolo (geração independente → leitura cruzada) implementa empiricamente o princípio de sequestro-de-referência derivado por análise causal
- [[curation-anti-bias]] — multiagent spot-check é um dos 5 melhoramentos propostos; Du et al. fornece o substrato empírico para essa recomendação

## Fontes

- [Du et al. 2023](../../raw/papers/multiagent-debate-factuality.md) — arXiv:2305.14325. Protocolo de debate multi-round entre instâncias LLM; melhoria em raciocínio matemático/estratégico e redução de alucinações
