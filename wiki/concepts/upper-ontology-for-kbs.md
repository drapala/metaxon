---
title: "Upper Ontology for Epistemic Knowledge Bases"
sources:
  - path: wiki/concepts/formal-ontology-for-kbs.md
    type: article
    quality: primary
    stance: confirming
  - path: wiki/concepts/single-brain-data-ontology.md
    type: article
    quality: primary
    stance: confirming
created: 2026-04-06
updated: 2026-04-06
tags: [ontology, class-hierarchy, epistemic-kb, bfo, dolce, upper-ontology]
source_quality: high
interpretation_confidence: low
resolved_patches: []
reads: 0
retrievals_correct: 0
retrievals_gap: 0
last_read: null
provenance: synthesis
synthesis_sources:
  - wiki/concepts/formal-ontology-for-kbs.md
  - wiki/concepts/single-brain-data-ontology.md
quarantine: true
quarantine_created: 2026-04-06
quarantine_reason: "artigo de síntese — hierarquia de classes é interpretação do compilador, não claim direto de nenhuma fonte; requer 24h + challenge adversarial"
quarantine_promoted: null
quarantine_criteria_met:
  tempo: false
  review_frio: false
  adversarial_or_scout_or_prediction: null
---

## Resumo

Este artigo sintetiza dois artigos wiki — [[formal-ontology-for-kbs]] (BFO/DOLCE/OWL2 aplicados a KBs) e [[single-brain-data-ontology]] (4 redes epistêmicas de Hindsight) — para propor uma upper ontology de KBs epistêmicos: uma hierarquia de classes que separa entidades, artefatos de conhecimento, claims e sua proveniência epistêmica. A hierarquia resolve o gap identificado em formal-ontology-for-kbs (ausência de class hierarchy), aplicando as 4 redes de Hindsight como eixo epistêmico ortogonal à tipologia BFO.

## Conteúdo

### O gap que esta síntese resolve

[[formal-ontology-for-kbs]] identificou como gap central: "ALL articles are peers in concepts/ — No hierarchy." Sem hierarquia, o retrieval não distingue um artigo que *é instância* de outro que o *generaliza*, e o agente não pode raciocinar sobre o que seria afetado se um artigo fosse removido.

[[single-brain-data-ontology]] resolve o eixo epistêmico ortogonal: não apenas *o que* é uma entidade, mas *qual o status epistêmico* do conhecimento sobre ela — fato verificado, opinião com confiança, síntese derivada, observação emergida.

A upper ontology combina os dois eixos.

### Hierarquia de Classes Proposta

```
Entity (BFO: tudo que existe no domínio)
├── Continuant (BFO: persiste como um todo em qualquer instante)
│   ├── KnowledgeArtifact
│   │   ├── Source          ← raw/ files (imutáveis)
│   │   │   ├── PrimarySource    (quality: primary — dados originais)
│   │   │   └── SecondarySource  (quality: secondary | tertiary)
│   │   └── Article         ← wiki/concepts/ files
│   │       ├── SourceArticle    (provenance: source — resume 1 raw/)
│   │       ├── SynthesisArticle (provenance: synthesis — combina 2+ raw/)
│   │       └── EmergenceArticle (provenance: emergence — conceito novo)
│   └── Claim               ← afirmações dentro de artigos
│       ├── FactualClaim     (rastreável diretamente a Source)
│       ├── VerifiedClaim    (sobreviveu Gate 3 + challenge adversarial)
│       ├── InterpretedClaim (⚠️ nossa interpretação — synthesis/analogy)
│       └── EmergentClaim    (sem fonte individual — emergiu de /ask cross-domain)
└── Occurrent (BFO: desenrola-se no tempo, tem partes temporais)
    ├── Session             ← /ask, /challenge, /ingest runs
    │   ├── RetrievalSession (/ask)
    │   ├── ChallengeSession (/challenge, Gate 3)
    │   └── IngestSession    (/ingest)
    └── DisturbanceEvent    ← algedonic channel (DisturbanceEvent canônico)
        ├── RetrievalFailure
        ├── L1Contradiction
        ├── QuarantineRepeat
        └── GateFailure
```

### Mapeamento às 4 Redes de Hindsight

[[single-brain-data-ontology]] propõe que agentes separem epistemicamente os dados em 4 redes. Mapeamento à upper ontology:

| Hindsight Network | Upper Ontology | Regime de atualização |
|-------------------|----------------|-----------------------|
| World (𝒲) — fatos objetivos | VerifiedClaim + SourceArticle promovido | Append-only + bi-temporal |
| Experience (ℬ) — log de ações | Session (Occurrent) + DisturbanceEvent | Append-only, imutável |
| Opinion (𝒪) — julgamentos com confiança | InterpretedClaim + EmergentClaim + artigos em quarentena | Update com confidence decay |
| Observation (𝒮) — sínteses derivadas | SynthesisArticle + _index.md | Rebuild periódico |

**Por que o mapeamento importa:** o /ask deveria consultar redes diferentes dependendo do tipo de pergunta. Uma pergunta factual ("o que os dados dizem sobre X?") consulta World+Experience (VerifiedClaims + Sessions). Uma pergunta especulativa ("que conexões emergem de X?") consulta Opinion+Observation (EmergentClaims + SynthesisArticles).

Hoje o /ask trata todos os artigos como equivalentes. A upper ontology tornaria esse roteamento explícito.

### O que Prometheus adiciona que Beer não previu

Beer (VSM, 1972) modelou organizações como sistemas que absorvem variety do ambiente. S1-S5 descrevem como a organização regula a si mesma. Mas Beer assumiu informação *homogênea* — toda informação no sistema tem o mesmo status epistêmico.

(⚠️ nossa interpretação) [[prometheus-as-nlah-substrate]] adiciona o que Beer não previu: **claims têm tipos epistêmicos diferentes**, e o sistema precisa de meta-cognição sobre esses tipos para não colapsar epistemicamente. Beer descreveu o canal algedônico como sinal de distúrbio; mas não distinguiu entre distúrbio causado por fato externo (VerifiedClaim que contradiz o modelo) e distúrbio causado por emergência interna (EmergentClaim que ainda não foi validado).

A upper ontology formaliza essa distinção que Beer deixou implícita. Em termos de VSM:
- S1-S3 operam sobre FactualClaim e VerifiedClaim (operação cotidiana)
- S4 opera sobre InterpretedClaim e EmergentClaim (planejamento com incerteza)
- S5 recebe DisturbanceEvent quando qualquer claim muda de tipo inesperadamente (algedônico)

### Relações tipadas relevantes (de [[formal-ontology-for-kbs]])

A upper ontology habilita as relações tipadas que os wikilinks não-tipados atuais não expressam:

| Relação | Entre classes | Exemplo |
|---------|--------------|---------|
| `derivedFrom` (assimétrica) | Article → Source | SynthesisArticle derivedFrom 2+ PrimarySources |
| `instanceOf` (N-1) | SourceArticle → EmergenceArticle | stigmergic-coordination instanceOf coordination-patterns |
| `contradicts` (simétrica) | Claim ↔ Claim | VerifiedClaim contradicts InterpretedClaim |
| `supersedes` (temporal + assimétrica) | VerifiedClaim → InterpretedClaim | Após Gate 3, VerifiedClaim supersedes claim anterior |
| `partOf` (transitiva) | Article → Article | neurosymbolic-ai-for-kbs partOf formal-ontology-for-kbs |

### Property Characteristics (OWL) aplicadas à hierarquia

- `contradicts`: **simétrica** — se EmergentClaim A contradiz VerifiedClaim B, B contradiz A
- `partOf`: **transitiva** — se neurosymbolic partOf formal-ontology, e formal-ontology partOf kb-design, então neurosymbolic partOf kb-design
- `derivedFrom`: **assimétrica** — A deriva de B não implica B deriva de A
- `supersedes`: **assimétrica + temporal** — só funciona em uma direção no tempo

## Interpretação

(⚠️ nossa interpretação) A hierarquia de classes proposta aqui é design, não fato das fontes. [[formal-ontology-for-kbs]] identifica o gap (ausência de hierarquia); [[single-brain-data-ontology]] fornece o eixo epistêmico. A síntese que combina os dois em uma upper ontology unificada é gerada por este artigo — não está em nenhuma das fontes.

(⚠️ nossa interpretação) O mapeamento Beer VSM → upper ontology (S1-S3 operam sobre VerifiedClaim, S4 sobre EmergentClaim, S5 recebe DisturbanceEvent) é analógico, não derivado. Beer não usou linguagem de ontologia formal. A analogia é plausível — mas requer validação contra uma implementação real, não apenas coerência conceitual.

**Claim mais fraco:** a distinção FactualClaim/VerifiedClaim/InterpretedClaim/EmergentClaim pressupõe que o agente LLM consegue classificar claims individuais de forma confiável. Isso não está validado — a granularidade pode ser muito fina para classificação automática confiável.

## Conexões

- [[formal-ontology-for-kbs]] — BFO/DOLCE como fundação; typed relations; continuant vs occurrent
- [[single-brain-data-ontology]] — 4 epistemic networks como eixo ortogonal da hierarquia
- [[neurosymbolic-ai-for-kbs]] — inverse parametric effect justifica onde aplicar a hierarquia (clusters Zone 3 primeiro)
- [[viable-system-model-beer]] — S1-S5 mapeados a classes da upper ontology
- [[structural-coupling-maturana]] — cada nível da hierarquia preserva autopoiese distinta
- [[algedonic-channel-vsm]] — DisturbanceEvent é Occurrent na upper ontology; já implementado
- [[autonomous-kb-failure-modes]] — authority bias cascade = falha de separação epistêmica (Opinion escrito como World)

## Fontes

- [Formal Ontology for KBs](../concepts/formal-ontology-for-kbs.md) — BFO continuant/occurrent, typed relations RO, OWL open-world assumption, gap: ausência de class hierarchy
- [Single Brain Data Ontology](../concepts/single-brain-data-ontology.md) — 4 redes epistêmicas (World/Experience/Opinion/Observation), mapeamento ao Single Brain, regimes de atualização por rede
