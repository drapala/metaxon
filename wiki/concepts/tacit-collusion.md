---
title: "Tacit Collusion"
sources:
  - path: raw/papers/tirole-1988-ch6-dynamic-price-competition-tacit-collusion.md
    type: paper
    quality: primary
    stance: neutral
  - path: raw/papers/ivaldi-et-al-2003-economics-tacit-collusion.pdf
    type: paper
    quality: primary
    stance: neutral
  - path: raw/articles/stigler-1964-theory-of-oligopoly.md
    type: article
    quality: secondary
    stance: challenging
    challenging_type: content
  - path: raw/papers/stigler-1964-theory-of-oligopoly.pdf
    type: paper
    quality: primary
    stance: challenging
    challenging_type: content
created: 2026-04-08
updated: 2026-04-08
tags: [economics, industrial-organization, game-theory, oligopoly, antitrust]
source_quality: high
interpretation_confidence: high
resolved_patches: []
provenance: synthesis
synthesis_sources:
  - raw/papers/tirole-1988-ch6-dynamic-price-competition-tacit-collusion.md
  - raw/papers/ivaldi-et-al-2003-economics-tacit-collusion.pdf
quarantine: false
---

## Resumo

Conluio tácito é a manutenção de preços supra-competitivos por firmas oligopolistas sem acordo explícito — apenas pela ameaça implícita de retaliação em jogos repetidos. Tirole (1988, Ch.6) fornece o tratamento teórico fundamental: Folk Theorem, estratégia grim trigger, três abordagens de tacit collusion. Ivaldi et al. (2003) aplicam o framework à política antitruste europeia, identificando 13 fatores estruturais e implicações para controle de fusões.

## Conteúdo

### Definição

"Tacit collusion need not involve any 'collusion' in the legal sense, and in particular need involve no communication between the parties." O termo descreve situações onde o resultado de mercado (preços ou quantidades) se assemelha ao de cartel explícito, obtido unicamente pela dinâmica estratégica de jogos repetidos. Sinônimo legal preferível: *tacit coordination*.

### Mecanismo: jogos repetidos e fator de desconto

O conluio tácito emerge quando firmas interagem repetidamente e podem condicionar sua conduta futura ao comportamento passado dos rivais. O mecanismo central é a estratégia *grim trigger*: qualquer desvio do preço collusivo desencadeia guerra de preços permanente.

**Condição necessária — threshold de desconto:**

Para 2 firmas com produto homogêneo e custo unitário `c`, o preço collusivo `p^C` é sustentável se e somente se o fator de desconto `δ` satisfaz:

```
δ ≥ δ* = 1/2
```

Intuição: cada firma compara o ganho de curto prazo do desvio (capturar todo o mercado por um período) contra a perda futura (eliminação de lucros collusivos para sempre). Se `δ < 1/2`, o futuro não vale o suficiente — desviar é racional.

O fator de desconto captura tanto a taxa de juros (`δ = 1/(1+R)`) quanto a frequência de interação. Interação mais frequente aumenta δ efetivo.

### Três abordagens de tacit collusion (Tirole, 1988)

Tirole identifica três mecanismos distintos pelos quais o conluio tácito pode emergir em jogos repetidos:

1. **Supergame / Bootstrap:** guerra de preços é fenômeno auto-realizador. Uma firma cobra preço baixo porque *espera* que a rival o faça (motivado por desvio passado). Fundação: Friedman (1971) + Folk Theorem (Fudenberg & Maskin, 1986).

2. **Rigidez de preços de curto prazo:** a reação de uma firma a um price cut é motivada pela preservação de market share que continua sendo corroído pela estratégia agressiva da rival.

3. **Reputação:** links intertemporais não-físicos emergem do aprendizado mútuo. Uma firma reage a um price cut porque o desvio *revelou informação* — o rival tem custo baixo ou não pode ser confiado para sustentar o conluio.

"These should be thought of as describing complementary aspects of repeated price interaction" (Tirole, 1988).

### Folk Theorem — formulação formal (Tirole, 1988 / Fudenberg & Maskin, 1986)

Para o jogo de preço repetido com 2 firmas simétricas, o Folk Theorem afirma que **qualquer par de lucros `(π¹, π²)` com `π¹ > 0`, `π² > 0`, e `π¹ + π² < π^M`** é um per-period payoff de equilíbrio perfeito para δ suficientemente próximo de 1.

Intuição da estratégia grim trigger com preço collusivo `p`:
- Conforme: cada firma ganha `π(p)/2 × 1/(1−δ)` (fluxo perpétuo)
- Desvio: ganha no máximo `π(p)` no período do desvio, depois lucro zero para sempre
- Condição para conformidade: `δ ≥ 1/2` (caso base duopólio Bertrand)

A estratégia ótima de punição não é grim trigger mas *maximal punishment* (Bertrand competitivo para sempre), que sustenta prices mais altos com δ menor.

**Lacuna documental:** Fudenberg & Maskin (1986, Econometrica 54:533–554) — paper fundacional que generaliza o Folk Theorem para jogos com desconto e informação incompleta — não disponível fora de paywall. Os resultados estão cobertos por Tirole (1988) seção 6.3 e Ivaldi et al. (2003) seção II.

### Fatores que facilitam o conluio

| Fator | Mecanismo |
|-------|-----------|
| Poucos competidores | Maior share individual → maior payoff collusivo por firma |
| Barreiras de entrada | Elimina a ameaça de novos entrantes que quebrariam o equilíbrio |
| Interação frequente | Aumenta o peso do futuro → δ efetivo maior |
| Transparência de mercado | Desvios detectados rapidamente → punição mais crível |
| Simetria de custos | Preço collusivo ótimo é o mesmo para todas as firmas |
| Contato multi-mercado | Ameaça de retaliação em múltiplos mercados expande o espaço de punições |
| Crescimento sustentado da demanda | "Today's profits are small compared with tomorrow's ones" → punição futura mais valiosa → δ* efetivo = 1/(2(1+g)) cai com g > 0 |

### Fatores que dificultam o conluio

| Fator | Mecanismo |
|-------|-----------|
| Flutuações de demanda (booms) | Rotemberg-Saloner: em booms, ganho de curto prazo do desvio é proporcionalmente maior → guerra de preços pró-cíclica |
| Declínio do mercado | "Tomorrow's profits will be small anyway" → punição perde eficácia → collusion inviável em mercados à beira do colapso |
| Assimetria de custos | Preço collusivo ótimo diverge entre firmas → desacordo sobre ponto focal |
| Alta intensidade de inovação | Incentivo a desviar para capturar patentes ou liderança tecnológica |
| Diferenciação vertical de produtos | Firma com produto superior tem mais a ganhar do desvio e menos a temer da retaliação — efeito de diferenciação horizontal é ambíguo |

### Mercados de licitação (bidding markets)

Em leilões, o conluio tácito assume formas específicas: *rotation schemes* (cada firma ganha sua vez), divisão geográfica de mercado, e supressão de lances. A detecção é mais difícil porque não há "preço de mercado" observável — apenas lances individuais.

### Desafio de Stigler (1964): O Problema de Detecção

Stigler (1964) — paper fundacional anterior ao Folk Theorem — oferece o principal desafio *prático* à sustentabilidade de conluio: mesmo quando firmas querem coludir, **o problema central é detectar trapaça**, não a disposição de cooperar.

**A assimetria de informação central:**
- Compradores que recebem desconto secreto de um rival não têm incentivo para revelar isso aos demais
- A firma que perde vendas não sabe se é porque: (a) um rival está fazendo price cuts secretos, ou (b) ocorreu choque de demanda — os dois casos são observacionalmente equivalentes
- Detecção, mesmo quando eventual, ocorre com lag — e durante o lag o traidor lucra

**Número de membros e estabilidade:**
- Com **poucos membros:** cada firma rastreia rivais facilmente; desvios detectados rapidamente; conluio mais estável
- Com **muitos membros:** cada firma é fração menor do mercado; price cuts de qualquer firma têm impacto detectável menor; detecção mais lenta; trapaça mais lucrativa em relação ao custo de detecção

Formulação implícita: se p é a probabilidade de um rival específico ouvir sobre redução de preço, então 1-(1-p)^n é a probabilidade de que *ao menos um* rival descubra dado que o desconto foi concedido a n clientes. Isso sobe com n — mas o que importa para dissuasão é que *o rival certo* descubra, não *qualquer* rival.

**O argumento challeng-ador:** O Folk Theorem assume que desvios são detectados (possivelmente com lag). Stigler mostra que na prática, **falha de detecção é o caso típico**, especialmente em escala. O threshold δ* teórico é necessário mas não suficiente — é necessário que o mecanismo de detecção também funcione, o que requer transparência de mercado, poucos compradores grandes, e produto padronizado. Na maioria dos mercados reais, essas condições não se sustentam com muitos participantes.

Essa análise é anterior e independente do Folk Theorem. Tirole (1988) a cita explicitamente ao introduzir o modelo Green-Porter como resposta: conluio com monitoramento imperfeito implica *guerras de preços periódicas* como equilíbrio racional (não como colapso do conluio).

### Implicações para controle de fusões

Fusões que aumentam simetria entre firmas facilitam conluio tácito. A análise antitruste distingue dois efeitos:
- **Efeitos unilaterais:** poder de mercado individual da firma pós-fusão
- **Efeitos coordenados:** maior probabilidade de conluio tácito por redução de assimetrias

O modelo prevê que fusões em mercados com produto homogêneo, poucos competidores, e alta transparência merecem escrutínio adicional de "coordinated effects" mesmo quando nenhuma firma se torna individualmente dominante.

## Verificação adversarial

**Claim mais fraco:** O threshold δ* = 1/2 é derivado do caso-base Bertrand com 2 firmas e produto homogêneo — não é universalmente aplicável. Com N firmas, δ* = (N-1)/N → 1 conforme N → ∞, tornando conluio inviável.

**O que o paper NÃO diz:**
1. Não fornece evidência empírica de conluio tácito — é framework teórico e policy guide
2. Não trata conluio tácito como necessariamente presente em oligopólios — é possibilidade condicional
3. Não especifica como identificar conluio tácito vs. *parallel conduct* em investigações reais

**Simplificações:** O modelo base assume informação perfeita (desvios detectados imediatamente). Na prática, detecção com lag altera o threshold de forma não-trivial. O efeito da diferenciação de produtos é ambíguo: diferenciação horizontal pode facilitar ou dificultar dependendo das funções de demanda — o artigo qualifica apenas o caso de diferenciação vertical.

**Claim mais fraco (Stigler):** Stigler (1964) argumenta que falha de detecção é o caso típico — mas Tirole (1988) e o modelo Green-Porter oferecem uma resposta: monitoramento imperfeito não elimina conluio, apenas o transforma em equilíbrio com guerras de preços periódicas. O conluio pode persistir mesmo com detecção imperfeita se as guerras de preços forem suficientemente custosas. O debate entre os dois frameworks está em aberto empiricamente.

**Prior work:** Friedman (1971) fornece a formalização original do folk theorem para superjogos — citado explicitamente como fundação formal (footnote 6 do paper). Stigler (1964) fornece o argumento de detecção anterior e independente do folk theorem.

## Interpretação

(⚠️ Zone 3 — domínio lateral. Interpretação intencionalmente vazia no ingest. Conexões com a KB emergem no /ask.)

## Conexões
- complementsAt: [[procurement-renegotiation]] — ambos trabalhos de Tirole, domínios distintos (IO dinâmica vs. contratos incompletos)
- complementsAt: [[incentive-theory-procurement]] — mesmo contexto teórico, mecanismos diferentes

## Fontes
- [Tirole (1988) Cap. 6](../../raw/papers/tirole-1988-ch6-dynamic-price-competition-tacit-collusion.md) — *The Theory of Industrial Organization*, MIT Press; três abordagens de tacit collusion, Folk Theorem formal, grim trigger, maximal punishment, supergames
- [Ivaldi, Jullien, Rey, Seabright, Tirole (2003)](../../raw/papers/ivaldi-et-al-2003-economics-tacit-collusion.pdf) — relatório para DG Competition da Comissão Europeia; 13 fatores facilitadores/inibidores, implicações para merger control
- [Stigler (1964) — nota secundária](../../raw/articles/stigler-1964-theory-of-oligopoly.md) — *JPE* 72(1); argumento de detecção como barreira prática ao conluio; desafia a premissa de detecção viável que o Folk Theorem pressupõe
- [Stigler (1964) — PDF](../../raw/papers/stigler-1964-theory-of-oligopoly.pdf) — texto primário; escaneado sem OCR, verificado visualmente

## Quality Gate
- [x] Wikilinks tipados: 2 relações (complementsAt ×2)
- [x] Instance→class: threshold δ* = 1/2 qualificado como caso-base 2-firma Bertrand homogêneo
- [x] Meta-KB separado: nenhuma referência ao metaxon no Conteúdo
- [x] Resumo calibrado: reflete escopo do paper (framework teórico + policy guide)
- [x] Challenging source integrado: Stigler (1964) adicionado com stance:challenging, challenging_type:content; seção própria com argumento de detecção; resposta Tirole documentada
