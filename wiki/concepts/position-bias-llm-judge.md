---
title: "Position Bias in LLM-as-a-Judge"
quarantine: false
quarantine_created: 2026-04-05
quarantine_promoted: 2026-04-05
quarantine_criteria_met:
  auto_promote: false
  gates_passed: [1, 2, 3]
  gate3_run: 2026-04-05
  gate3_models: [gpt-5.4, gemini-3.1-pro-preview]
  gate3_claims_challenged: 9
  gate3_claims_survived: 4
  gate3_claims_weakened: 5
  gate3_claims_invalidated: 0
  challenge_verdict: PUBLICÁVEL
  challenge_type: clean
  challenge_log: outputs/logs/sessions/2026-04-05/challenge-position-bias-llm-judge-17-30.md
  prior_work_found: 5
  promoted_by: manual_promote
  pipeline_note: "primeiro artigo promovido com Gate 3 ∥ challenge paralelos — template de referência"
sources:
  - path: raw/papers/judging-judges-position-bias-llm-2406.07791.md
    type: paper
    quality: primary
    stance: confirming
created: 2026-04-05
updated: 2026-04-05
challenge_applied: 2026-04-05
tags: [llm-judge, bias, evaluation, position-bias, intervention]
source_quality: high
interpretation_confidence: high
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: source
---

## Resumo

Shi et al. (AACL-IJCNLP 2025) establish via position-swapping intervention (Level 2 causal evidence) that position bias in LLM judges is systematic, not random. The effect is worst when candidate quality is similar — precisely where accurate evaluation matters most. Claude-3.5-Sonnet and GPT-4 show highest position consistency (PC=0.82); Claude-3-Haiku is most biased (PC=0.57).

## Conteúdo

### Três Métricas de Viés Posicional

**Repetition Stability (RS)** — percentual de seleções mais frequentes em múltiplas tentativas. Mede se julgamentos são estáveis ou aleatórios. Juízes capazes: RS > 0.95, confirmando que o viés é sistemático, não ruído. (⚠️ caveat: RS mede reprodutibilidade, não ausência de viés — um juiz pode ser simultaneamente estável e sistematicamente enviesado)

**Position Consistency (PC)** — fração de instâncias onde o juiz escolhe o mesmo candidato independentemente da posição. Medido via permutação explícita de ordem (do-operator).

| Juiz | PC (MTBench) |
|------|-------------|
| Claude-3.5-Sonnet | 0.82 |
| GPT-4 | 0.82 |
| Claude-3-Haiku | 0.57 |
| Gemini-1.0-pro | baixo |

(⚠️ snapshot MTBench; JudgeBench mostra degradação em tarefas difíceis — PC pode ser substancialmente menor em domínios especializados e versões futuras dos modelos)

**Preference Fairness (PF)** — escala −1 a +1 capturando viés de primacy (−1) vs recency (+1). Zero = julgamento sem posição preferida.
- Claude-3.5-Sonnet: PF = 0.01 (sem preferência direcional líquida em média; PF~0 não implica ausência de viés em nível de instância)

### Protocolo de Intervenção (Evidência L2)

O estudo usa position-swapping: mantém todo o conteúdo constante, altera apenas a ordem de apresentação dos candidatos. Isso é um do-operator explícito — do(posição=A_primeiro) vs do(posição=B_primeiro). 150.000+ instâncias, 15 juízes, 22 tarefas (MTBench e DevBench).

Resultado: viés posicional é causal (sistemático, não aleatório). A posição *causa* o julgamento em casos de qualidade similar — não apenas correlaciona.

### Relação Quality Gap × Position Consistency

Quando o gap de qualidade entre candidatos é **grande** → PC alto (juiz identifica o melhor independente de posição).  
Quando o gap é **pequeno** (candidatos similares) → PC mínimo (juiz recorre à heurística de posição).

A relação é **monotonicamente crescente com o gap absoluto** — o paper usa o termo "parabólica" para descrever o comportamento assimétrico em torno de gaps próximos de zero, não uma curva em U invertido. (⚠️ formalização quantitativa da curva não fornecida; evidência qualitativa)

Implicação: o viés posicional é maximizado em comparações próximas — exatamente onde uma avaliação precisa é mais crítica e onde o juiz deveria ser mais confiável.

### Fontes do Viés (Três Níveis)

| Nível | Variável | Impacto |
|-------|----------|---------|
| **Juiz** | Capacidade e treinamento do modelo | Determina PC e RS baseline |
| **Candidato** | Gap de qualidade entre respostas | Maior gap → menor viés (relação monotônica com gap absoluto) |
| **Tarefa** | Domínio e complexidade | Viés varia substancialmente por task |

Achado contra-intuitivo: comprimento dos componentes do prompt tem **fraca** influência sobre o **viés posicional** especificamente — escopo limitado a este tipo de bias; não generaliza para efeitos de comprimento em geral (cf. Lost in the Middle, que documenta degradação de atenção a tokens distantes em tarefas de recuperação).

## Interpretação

(⚠️ nossa síntese) O position-swapping protocol é o mesmo que o do-operator de Pearl — a posição é tratada como variável de intervenção, não confundidor. Isso eleva o claim de "viés posicional existe" (L1, correlação) para "posição *causa* julgamentos inconsistentes em casos de qualidade similar" (L2, mecanismo).

A relação parabólica tem implicação direta para protocolos de avaliação na KB: quando dois artigos são próximos em qualidade (ambos medium/high confidence), a ordem de apresentação ao /review torna-se variável causal. Protocolo correto: apresentar candidatos sem ordem preferida, ou usar juiz com PC alto (Claude-3.5-Sonnet, GPT-4).

## Verificação adversarial

**Claim mais fraco:** PC=0.82 para Claude-3.5-Sonnet no MTBench. MTBench é benchmark relativamente fácil — JudgeBench mostra degradação em tarefas difíceis. PC pode ser substancialmente menor em tarefas KB-specific (artigos densos com claims técnicos).

**O que o paper NÃO diz:**
1. NÃO testa se mitigações (swapping + voting) eliminam o viés ou apenas o atenuam
2. NÃO afirma que prompt length é irrelevante para outros tipos de viés — apenas para position bias
3. NÃO cobre interações entre position bias e outros biases CALM (ex: se verbosity bias amplifica position bias)

**Simplificações:**
- PC é medido em benchmarks específicos (MTBench, DevBench); generalização para domínios mais especializados não verificada
- "Parabolic relationship" — descrita qualitativamente, formalização quantitativa da curva não fornecida no resumo disponível

**Prior work citado:**
- CALM (Ye et al.) — 12 biases; position bias como um dos itens
- JudgeBench (Tan et al.) — confiabilidade inflada por dificuldade do benchmark

## Conexões

- partOf: [[llm-as-judge]] ON "position bias é um dos 12 biases CALM, agora com evidência L2 de causalidade via position-swapping"
- validates: [[evaluation-order-independence]] ON "L2 evidence: position-swapping do-operator confirma que ordem de apresentação é variável causal em julgamentos LLM"
- complementa: [[curse-of-knowledge-llm-judge]] ON "ambos estudam como informação contextual (referência / posição) distorce julgamento independente; mecanismos distintos, efeito similar"
- instancia: [[causal-reasoning-pearl]] ON "position-swapping = do-operator de Pearl: evidência L2 (intervenção) vs L1 (correlação dos estudos anteriores sobre position bias)"

## Fontes

- [Judging the Judges (arXiv:2406.07791)](../../raw/papers/judging-judges-position-bias-llm-2406.07791.md) — 15 juízes, 150k+ instâncias, três métricas (RS, PC, PF), relação parabólica quality gap × PC, rankings de confiabilidade

## Quality Gate
- [x] Wikilinks tipados: 4 substituições (partOf, validates, complementa, instancia)
- [x] Instance→class: 4 claims numéricos qualificados (PC=0.82 em MTBench, Claude-3.5-Sonnet; PC=0.57 em Claude-3-Haiku; PF=0.01 em Claude-3.5-Sonnet; RS>0.95 em juízes capazes)
- [x] Meta-KB separado: referências a /review em ## Interpretação, não em ## Conteúdo
- [x] Resumo calibrado: cita modelo e benchmark específicos, não afirma generalização

