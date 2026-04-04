---
title: "Information Theory (Shannon)"
sources:
  - path: raw/papers/shannon-mathematical-theory-communication.md
    type: paper
    quality: primary
    stance: neutral
created: 2026-04-04
updated: 2026-04-04
tags: [information-theory, entropy, channel-capacity, bits, foundational, lateral]
source_quality: high
interpretation_confidence: low
quarantine: false
quarantine_created: 2026-04-04
quarantine_reason: "4 especulações em ## Níveis epistêmicos: aplicação de entropia a V(LLM) é interpretação não testada"
quarantine_promoted: 2026-04-04
quarantine_criteria_met:
  tempo: override_by_user
  review_frio: override_by_user
  adversarial_or_scout_or_prediction: "Predição L1→L2 explícita: error floor ≈ H(raw)−H(wiki) via embedding diversity. IB e rate-distortion são derivados de Shannon (prior work confirma autoridade, não subsume). 11 artigos já citavam como hub fundacional do cluster info-theory — evidência de utilidade estrutural."
resolved_patches: []
---

## Resumo

Shannon (1948) define informação matematicamente como redução de incerteza, formaliza entropia como H = −Σ pᵢ log pᵢ, e prova os teoremas fundamentais do canal com e sem ruído. O bit emerge como unidade natural de informação (base 2). A teoria trata exclusivamente do problema de transmissão fiel — semântica é explicitamente excluída. Aplicação a sistemas linguísticos como LLMs é post-hoc à teoria original; as pontes estão no nível de proxy de medição, não de dedução direta.

## Conteúdo

### O problema fundamental (Shannon, 1948, Introdução)

"The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point."

Shannon define explicitamente que **aspectos semânticos são irrelevantes ao problema de engenharia**: "These semantic aspects of communication are irrelevant to the engineering problem. The significant aspect is that the actual message is one selected from a set of possible messages."

O sistema de comunicação tem cinco partes: information source → transmitter → channel → receiver → destination. O canal pode ser perturbado por noise source.

### O bit como unidade de informação

O bit é definido pelo uso de log na base 2. Shannon atribui a J.W. Tukey a palavra "bit" (binary digit). Justificativa para a escala logarítmica (três razões dadas na fonte):

1. Parâmetros de engenharia variam linearmente com o logaritmo do número de possibilidades
2. É mais intuitivo — dois canais idênticos têm o dobro da capacidade
3. É matematicamente mais tratável (operações de limite são simples)

Mudança de base = multiplicação por constante: log₂ M = log₁₀ M / log₁₀ 2 ≈ 3.32 log₁₀ M.

### Entropia como medida de informação (Seção 6 do paper)

Shannon deriva que a única função satisfazendo três propriedades razoáveis é:

**H = −K Σ pᵢ log pᵢ** (Teorema 2)

As três propriedades que levam a essa forma única:
1. H deve ser contínua nas pᵢ
2. Para pᵢ = 1/n equiprováveis, H cresce monotonicamente com n
3. Decomposição consistente: H deve ser a soma ponderada de escolhas sucessivas

K é constante positiva que define a unidade. Para base 2, K = 1, unidade = bits.

Shannon identifica explicitamente: "The form of H will be recognized as that of entropy as defined in certain formulations of statistical mechanics where pᵢ is the probability of a system being in cell i of its phase space. H is then, for example, the H in Boltzmann's famous H theorem."

**Propriedades verificadas no paper:**
- H = 0 quando resultado é certo (uma pᵢ = 1, restantes = 0)
- H máximo quando distribuição é uniforme
- H é sempre ≥ 0

### Capacidade de canal discreto sem ruído (Parte I)

Definição (Seção 1): C = lim(T→∞) [log N(T)] / T, onde N(T) = número de sinais permitidos de duração T.

**Teorema 9 (Teorema Fundamental para Canal sem Ruído):** Com fonte de entropia H (bits/símbolo) e canal de capacidade C (bits/segundo), é possível codificar a saída da fonte para transmitir a taxa média C/H (−ε) símbolos/segundo para qualquer ε > 0. A taxa C/H não pode ser excedida.

Significado: a entropia da fonte define o mínimo teórico de bits necessários para representá-la. Qualquer compressão além de H bits/símbolo implica perda de informação.

### Entropia relativa e redundância (Seção 7)

A razão entre a entropia de uma fonte e o máximo possível para o mesmo alfabeto = **entropia relativa**. Um menos a entropia relativa = **redundância**.

Do paper: "The redundancy of ordinary English, not considering statistical structure over greater distances than about eight letters, is roughly 50%. This means that when we write English half of what we write is determined by the structure of the language."

Redundância existe porque a língua tem estrutura estatística — permite compressão e correção de erros.

### Canal com ruído e capacidade (Parte II — Teorema Fundamental)

Para canal com ruído com capacidade C e source com entropia H:
- Se H ≤ C: é possível codificar a fonte de modo que a taxa de erro seja arbitrariamente baixa
- Se H > C: não é possível — taxa de erro tem floor irredutível

**Informação mútua:** I(X;Y) = H(X) − H(X|Y) — redução de incerteza sobre X causada pelo conhecimento de Y.

Capacidade do canal: C = max[I(X;Y)] sobre todas as distribuições de entrada possíveis.

### O que Shannon NÃO resolve (verificado no paper)

- Como medir a entropia de sistemas com vocabulário aberto e distribuição desconhecida (como LLMs)
- Semântica: Shannon exclui explicitamente o significado do formalismo
- Aprendizado: teoria é estática — não modela sistemas que mudam sua distribuição de probabilidades
- "Variety" de Ashby: Shannon trata estados de um canal, não estados gerais de um sistema de controle

## Interpretação

### (⚠️ nossa interpretação) Por que Shannon operacionaliza V(LLM) em bits

O artigo [[requisite-variety]] identifica como gap crítico que V(LLM) não tem unidade de medida. Shannon oferece um caminho: se V(sistema) = número de estados possíveis (Ashby), então H = −Σ pᵢ log pᵢ (Shannon) operacionaliza essa medida como *entropia da distribuição de estados*.

Proxy proposto: V(LLM) ≈ entropia da distribuição de outputs sobre um corpus de prompts padronizados. Mede diversidade de estados acessíveis ao compilador. V(raw) ≈ entropia da distribuição de conceitos distintos nas fontes (medida por embedding diversity). Error floor estimável como diferença.

**Caveats críticos:**
- Shannon trabalhou com canais discretos de comprimento finito, não com LLMs de vocabulário contínuo
- A ponte de V(Ashby) para H(Shannon) é nossa interpretação, não derivação direta de nenhum paper
- Entropia de outputs de LLM depende fortemente dos prompts escolhidos — não há consenso sobre proxy canônico

### (⚠️ nossa interpretação) Redundância como sinal de variety attenuation

Beer/Ashby: variety attenuation = redutor de estados. Shannon: redundância = estrutura que restringe sequências válidas. Possível isomorfismo: um compilador com alta redundância de outputs (repete padrões, parafraseia similarmente) tem V(R) efetivo menor do que V(output space) nominal. Redundância de escrita do compilador ≈ proxy de V(R) abaixo do máximo teórico.

### (⚠️ nossa interpretação) Separação semântica como gap estrutural

Shannon exclui semântica por design. KB compilation é fundamentalmente semântica — o que o artigo diz, não apenas que foi transmitido. A teoria de Shannon cobre o canal (fidelidade de cópia) mas não a transformação (compilation, synthesis, interpretation). A distinção é importante: error floor de Shannon ≠ error floor de Ashby para compilação. São layers complementares, não equivalentes.

## Verificação adversarial

**a. Claim mais fraco:** "V(LLM) pode ser operacionalizado como entropia H" — esta analogia não é derivada de Shannon, não é derivada de Ashby, e não está em nenhuma fonte primária. É especulação editorial.

**b. O que o paper NÃO diz:**
- Shannon não menciona LLMs, knowledge bases, ou compilação de conhecimento
- Shannon não relaciona entropia H com variety V de Ashby — essa conexão é nossa
- Shannon não afirma que semântica é irrelevante *para todos os fins* — apenas para o problema de engenharia de transmissão

**c. Simplificações feitas:**
- O paper cobre canais discretos E contínuos; este artigo focou apenas em discretos (mais relevantes para a analogia com tokens)
- Os teoremas do canal com ruído (Parte II do paper) foram resumidos sem demonstração — detalhes matemáticos omitidos
- A relação entre redundância de Shannon e variety attenuation de Ashby é apresentada como possível isomorfismo, não como equivalência provada

**d. Prior work:**
- Shannon cita Nyquist (1924, 1928) e Hartley (1928) como base para a teoria logarítmica de informação
- Boltzmann: Shannon identifica explicitamente a conexão com entropia termodinâmica (H theorem)
- Nenhum prior work de Shannon conecta a teoria à cybernetics de Ashby (desenvolvida simultaneamente, 1948–1956)

## Níveis epistêmicos

### Descrição (verificado em raw/)
- H = −K Σ pᵢ log pᵢ é a única função satisfazendo as três propriedades de Shannon (Teorema 2)
- Bit = unidade para base 2; nap = base e; digit = base 10
- Capacidade C = lim log N(T) / T (canal discreto)
- Redundância do inglês ≈ 50% (estimativa de Shannon para estrutura até 8 letras)
- Shannon exclui semântica explicitamente do escopo da teoria

### Interpretação (aplicação à KB — não de Shannon)
- V(LLM) ≈ H(distribuição de outputs) como proxy de variety
- Redundância de escrita do compilador como proxy de V(R) efetivo
- Separação dos layers: Shannon cobre canal, Ashby cobre controle, KB compilation é semântica

### Especulação (predições não testadas)
- Error floor de Ashby ≈ H(raw) − H(wiki) mensurável por embedding diversity
- Compilador com alta redundância de outputs tem V(R) efetivo abaixo do máximo
- V(LLM + contexto) > V(LLM solo) — mas quanto?
- Dois compiladores com distribuições de saída orthogonais = V(total) ≈ soma vs união?

## Conexões

- derivedFrom: [[requisite-variety]] ON "gap crítico: V(LLM) sem unidade de medida" — Shannon oferece H como candidato a proxy
- complementsAt: [[requisite-variety]] ON "operacionalização de V" — Ashby define variety como contagem de estados; Shannon define entropia como medida da distribuição sobre esses estados. Complementares, não redundantes.
- partOf: [[variety-gap-analysis]] — H(raw) − H(wiki) como operacionalização do V gap da KB

## Fontes

- [Shannon — A Mathematical Theory of Communication (1948)](../../raw/papers/shannon-mathematical-theory-communication.md) — definição formal de entropia (Seção 6, Teorema 2), teoremas do canal noiseless (Teorema 9), redundância, e o framework completo de five-part communication system

## Quality Gate
- [x] Wikilinks tipados: 3 (derivedFrom, complementsAt, partOf)
- [x] Instance→class: claims numéricos qualificados ("redundância ≈ 50% em inglês para estrutura até 8 letras — estimativa de Shannon, 1948")
- [x] Meta-KB separado: todas as referências à KB em ## Interpretação e ## Verificação adversarial, zero em ## Conteúdo
- [x] Resumo calibrado: inclui caveat "aplicação a LLMs é post-hoc à teoria original"

