---
title: "Autonomous Emergence Pipeline Risks"
sources:
  - path: wiki/concepts/judgment-aggregation.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autoresearch-reliability-triad.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/autonomous-kb-failure-modes.md
    type: synthesis
    quality: primary
  - path: wiki/concepts/llm-as-judge.md
    type: synthesis
    quality: primary
created: 2026-04-05
updated: 2026-04-05
tags: [meta-kb, autoresearch, emergence, pipeline, failure-modes]
source_quality: medium
interpretation_confidence: low
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
quarantine: true
quarantine_created: 2026-04-05
quarantine_reason: "artigo emergido de /ask — aguarda confirmação adversarial"
provenance: emergence
emergence_trigger:
  pair: [judgment-aggregation, autoresearch-reliability-triad, autonomous-kb-failure-modes]
  ask_session: outputs/logs/sessions/2026-04-05/ask-circular-oracle.md
  connection_type: EMERGE-DE
  pearl_level: L2
emerged_on: 2026-04-05
---

## Resumo

Um pipeline /emerge → /ask → /challenge sem humano expõe dois riscos estruturais independentes. Primeiro: o doctrinal paradox (List & Pettit) não piora — colapsa em consenso espúrio porque GPT e Gemini avaliam a proposta que geraram juntos, violando de facto a condição de Systematicity. Segundo: artigos emergence promovidos autonomamente não têm raw/ correspondente, tornando a verificação Layer 3 circular por definição, e cada artigo inválido promovido multiplica conexões espúrias ao habilitar novos /emerges — custo composto, não linear.

## Conteúdo

### Contexto: o que muda num pipeline totalmente autônomo

No pipeline com humano, o /emerge produz pares candidatos que um oracle externo avalia (GPT + Gemini em sessões independentes), e o humano decide promoção. No pipeline autônomo, a mesma sequência ocorre sem intervenção: /emerge propõe → /ask avalia → /challenge executa → promoção automática se score passa threshold.

Os dois riscos documentados abaixo emergem especificamente desta configuração circular — não são riscos do /emerge isolado nem do oracle isolado.

### Risco 1 — Convergência artificial do oracle (colapso do doctrinal paradox)

#### Mecanismo adversarial no oracle normal

No oracle do /emerge com humano, GPT e Gemini divergem (SPLIT) porque operam com critérios diferentes: GPT tende a avaliar isomorfismo estrutural; Gemini tende a avaliar novelty e emergence genuína. Essa divergência é sinal de qualidade — o mecanismo adversarial funciona precisamente porque os modelos discordam sobre propostas fracas.

List & Pettit (2002, Theorem 1) formaliza a condição necessária: a Systematicity exige que cada modelo vote sobre cada proposição independentemente, baseado apenas nos julgamentos individuais sobre aquela proposição. No oracle normal, essa condição é aproximadamente satisfeita — GPT e Gemini recebem o par de artigos e julgam sem histórico compartilhado de geração.

#### O colapso no pipeline circular

No pipeline autônomo, GPT e Gemini geraram a proposta de conexão conjuntamente no /emerge. Quando o /ask chama o oracle para avaliar, ambos avaliam a proposta que eles mesmos co-geraram.

(⚠️ nossa interpretação) O self-enhancement bias (CALM: 16.1% de erro em Qwen2; varia por modelo) opera aqui de forma assimétrica: cada modelo confirma o ângulo da proposta que *pesa mais para si*, não a proposta como um todo. GPT confirma porque detecta isomorfismo (o critério que ele privilegia na geração). Gemini confirma porque detecta novelty (o critério que ele privilegia). A conclusão "promover" passa porque ambos concordam — mas por razões incompatíveis.

(⚠️ nossa interpretação) Isso viola de facto a condição de Systematicity do Theorem 1: os votos não são mais independentes porque foram contaminados pela geração conjunta. O resultado não é inconsistência lógica (o problema clássico do doctrinal paradox) — é o oposto: consenso espúrio gerado por auto-confirmação. O artigo resultante pode não satisfazer nem o critério de isomorfismo do GPT nem o de emergence do Gemini; passou porque cada um validou apenas o ângulo que co-gerou.

#### Por que isso é invisível nas métricas

O oracle reporta aprovação bilateral. Não há sinal de que os votos "sim" são por razões incompatíveis. A divergência que detectaria fraqueza (SPLIT no oracle normal) foi suprimida pelo viés de co-autoria — exatamente o sinal que o mecanismo adversarial usa para rejeitar propostas fracas.

### Risco 2 — Falso positivo composto em emergence

#### Comparação com ingestão normal de artigo externo inválido

Um artigo ingerido via /ingest normal (fonte em raw/) tem âncora imutável. Se a interpretação wiki estiver errada:
- Layer 3 pode verificar o claim contra a fonte original
- Um patch humano pode corrigir com rastreabilidade
- O erro é linear: afeta os artigos que citam esse artigo

(⚠️ nossa interpretação) Um artigo emergence inválido promovido autonomamente tem estrutura diferente: *não existe raw/ correspondente*. O artigo wiki é ele mesmo a única fonte. Layer 3 verification não pode verificar o que não existe em fonte primária — a verificação recai sobre outros artigos wiki, que são sínteses LLM, que confirmam o artigo, que confirma os artigos.

#### O multiplicador via novos /emerges

Artigos emergence promovidos entram no corpus e tornam-se candidatos para novos /emerges. Um artigo emergence inválido habilita conexões espúrias com outros artigos legítimos — conexões que a KB nunca geraria sem ele como nó.

(⚠️ nossa interpretação) Isso é estruturalmente análogo ao model collapse (Shumailov et al., Nature 2024): "tail content disappears" porque o modelo recursivamente se alimenta de suas próprias sínteses. Aplicado à KB: o artigo inválido torna-se nó hub para novos pares emergence, amplificando a contaminação a cada ciclo /emerge.

O custo de um falso positivo em emergence é, portanto, composto (multiplicativo via novos /emerges), não linear. O custo não é proporcional ao erro original — é proporcional ao número de artigos emergence subsequentes ancorados nele.

#### Ausência de mecanismo de correção pós-promoção

Para artigos ingeridos normalmente: raw/ imutável + patch system + Layer 3 verification formam um triângulo de contenção. Para artigos emergence promovidos autonomamente: o triângulo colapsa porque o primeiro vértice (raw/ como âncora) não existe. O patch system ainda funciona, mas requer detecção humana de que o artigo é inválido — o que, sem oracle externo, é improvável num pipeline autônomo.

### Relação entre os dois riscos

Os dois riscos operam em etapas diferentes do pipeline:

| Risco | Etapa | Mecanismo | Detecção autônoma? |
|-------|-------|-----------|-------------------|
| Convergência artificial | /emerge → oracle | Self-enhancement suprime divergência adversarial | Não — oracle reporta aprovação bilateral |
| Falso positivo composto | promoção → corpus | Artigo sem âncora raw/ contamina /emerge subsequentes | Não — sem raw/, Layer 3 é circular por definição |

(⚠️ nossa interpretação) A combinação é sinérgica: o Risco 1 aumenta a taxa de promoção de artigos de baixa qualidade; o Risco 2 amplifica o custo de cada promoção indevida. Num pipeline com humano, o Risco 1 é mitigado pelo julgamento humano antes da promoção (o human-in-the-loop é o oracle externo real); o Risco 2 é mitigado pelo humano decidir se o artigo emergence tem substância suficiente para entrar no corpus.

### Mitigações estruturais

| Risco | Mitigação | Implementável autonomamente? |
|-------|-----------|------------------------------|
| Convergência artificial | Oracle com instâncias que NÃO participaram do /emerge (rotação de sessões) | Parcialmente — requer arquitetura de isolamento de contexto |
| Convergência artificial | Exigir que o SPLIT seja improvável antes de considerar válida a aprovação bilateral | Não — threshold de SPLIT requer calibração humana |
| Falso positivo composto | Quarentena obrigatória para artigos emergence (já implementada) | Sim — `quarantine: true` é automático |
| Falso positivo composto | Limitar /emerge a artigos não-emergence como candidatos (sem emergence-sobre-emergence) | Sim — filtro no script /emerge |
| Falso positivo composto | Exigir confirmação adversarial externa antes de artigo emergence entrar como candidato de novos /emerges | Não — requer humano |

## Interpretação

(⚠️ nossa interpretação) O tema unificador dos dois riscos é que o pipeline autônomo de emergence viola o Pilar 1 da autoresearch-reliability-triad (grounded test com oracle externo computacionalmente independente) de duas formas simultâneas: o oracle do /emerge não é independente porque os modelos avaliadores co-geraram a proposta; e o Layer 3 verification não é independente porque não existe raw/ para verificar.

(⚠️ nossa interpretação) A predição derivada: um pipeline autônomo de emergence que viole os dois isolamentos terá taxa de promoção > 80% para pares candidatos — sinal de circularidade, não de hipóteses genuinamente boas (análogo direto à predição da autoresearch-reliability-triad).

(⚠️ nossa interpretação) A solução mínima não é "mais regras no pipeline" — é separação estrutural entre geradores e avaliadores, que em sistemas multi-LLM requer arquitetura de isolamento de contexto (não apenas prompts diferentes).

## Conexões

- emerge-de: [[judgment-aggregation]] ON "Systematicity violada de facto quando geradores e avaliadores são os mesmos — consenso espúrio, não inconsistência lógica"
- emerge-de: [[autoresearch-reliability-triad]] ON "Pilar 1 (oracle externo) violado duas vezes: co-geração do par + ausência de raw/ para verificação"
- emerge-de: [[autonomous-kb-failure-modes]] ON "Layer 3 Circularity + model collapse: artigo emergence sem raw/ torna circularity estrutural, não apenas operacional"
- instancia: [[llm-as-judge]] ON "self-enhancement bias (16.1%) opera assimetricamente no oracle quando modelos avaliaram o que co-geraram"
- complementa: [[curation-anti-bias]] ON "mitigações de bias de curadoria são necessárias mas insuficientes quando o problema é circular por arquitetura"
- instancia: [[autoresearch-programme-vitality]] ON "confirming_ratio > 0.8 como sinal diagnóstico aplica-se ao pipeline emergence autônomo"

## Fontes

- [[judgment-aggregation]] — Theorem 1 (impossibilidade U+A+S); condição de Systematicity; doctrinal paradox como ponto de partida
- [[autoresearch-reliability-triad]] — Pilar 1 (grounded test = oracle computacionalmente independente); predição de confirmação > 80%
- [[autonomous-kb-failure-modes]] — Layer 3 Circularity Problem; model collapse (Shumailov et al., Nature 2024) como análogo estrutural
- [[llm-as-judge]] — self-enhancement bias 16.1% (CALM); independence como requisito de oracle confiável
