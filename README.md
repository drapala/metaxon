# llm-kb

> LLMs confirmam melhor do que descobrem. Um sistema de conhecimento operado por LLM sem estrutura epistêmica converge semanticamente em semanas: artigos homogeneizam, erros cristalizam por validação circular, nuance some. O sistema parece saudável em todas as métricas automáticas. A qualidade erode nos *claims*, não nos arquivos.
>
> Este KB foi construído para tornar essa degradação visível — e estruturalmente difícil de esconder.

---

## O problema que este projeto resolve

Em 2024, Shumailov et al. (Nature) documentaram *model collapse*: modelos treinados recursivamente em outputs sintéticos perdem diversidade estatística. Em 2025, Keisha et al. descreveram algo mais insidioso: *knowledge collapse* — fluência e formato permanecem intactos enquanto acurácia factual erode silenciosamente no Stage B, antes de qualquer métrica virar vermelho.

A implicação para KBs operados por LLM é direta: se `/review` opera majoritariamente sobre sínteses internas (`wiki/`) em vez de fontes primárias (`raw/`), o mecanismo de regularização desaparece. O compilador começa a validar seus próprios outputs contra seus próprios outputs.

O problema não é técnico. É epistêmico.

---

## Arquitetura

```
╔══════════════════════════════════════════════════════════════════════╗
║  raw/  (imutável — fonte da verdade)                                 ║
║   articles/   papers/   notes/   repos/                              ║
╚══════════════╦═══════════════════════════════════════════════════════╝
               │ /ingest
               ▼
╔══════════════════════════════════════════════════════════════════════╗
║  wiki/concepts/  (99 artigos — o grafo de conhecimento)              ║
║   provenance: 59 source · 14 synthesis · 26 emergence                ║
╚══════════════╦═══════════════════════════════════════════════════════╝
               │
       ┌───────┴──────────┐
       ▼                  ▼
   /ask                /emerge
 (retrieval         (conexões
  3 camadas)         latentes)
       │                  │
       ▼                  ▼
  outputs/          emerge_queue
  logs/             → /synthesize
                    → artigo emergence
```

Coordenação entre commands via `outputs/state/kb-state.yaml` — cada command deixa sinais para o próximo sem comunicação direta (**stigmergia**). Nenhum command chama outro diretamente; eles lêem e escrevem estado.

---

## O que é diferente

A maioria dos PKMs com LLM resolve o problema de *manutenção*. Este resolve também o problema *epistêmico* — que é diferente e mais difícil.

### 1. Proveniência de claims

Cada afirmação no wiki é rastreável a um arquivo em `raw/`. Sínteses cross-paper são marcadas `(⚠️ nossa interpretação)`. Quando você lê um artigo seis meses depois, sabe o que vem de fonte e o que vem do compilador.

```yaml
# Frontmatter de cada artigo
source_quality: high         # objetivo — baseado nas fontes
interpretation_confidence: medium  # subjetivo — auto-avaliação do compilador
provenance: emergence        # source | synthesis | emergence
```

### 2. Quarentena na criação

Artigos especulativos começam isolados. Não podem ser linkados até satisfazerem critérios de promoção:

- ⏱ 24h de resfriamento (revisão em sessão diferente)
- 🔍 Review frio (sem ancoragem na sessão de criação)
- ⚔️ Challenge adversarial ou predição falsificável (Pearl Level L2+)

Inspirado em Janis (1972): *second-chance meeting* antes de cristalizar no grafo.

### 3. Cota adversarial

1 em 5 fontes ingeridas deve *desafiar* os claims existentes, não confirmá-los. O viés de curadoria opera em 3 camadas — seleção, interpretação, avaliação. A cota é estrutural, não opcional. O Bradford gate verifica automaticamente.

### 4. Gate 3 paralelo e independente

Antes de qualquer promoção, dois modelos adversariais (GPT-5.4 e Gemini) rodam independentemente sobre o artigo **limpo** — sem ver o verdict um do outro. O /challenge humano roda em paralelo, também sem ver os outputs do Gate 3. Três revisores genuinamente independentes.

```
artigo limpo ──┬─► GPT-5.4 (article-challenge mode)  ──┐
               ├─► Gemini (article-challenge mode)    ──┤─► reconciliação hierárquica
               └─► /challenge (adversarial human-guided) ─┘
```

Threshold assimétrico: GPT ≥ 5 AND Gemini ≥ 8. Gemini é o gatekekeeper conservador; GPT identifica fraquezas específicas.

### 5. Provenance como contrato

Cada artigo é classificado por origem:

| Provenance | Significado | Critério de promoção |
|---|---|---|
| `source` | Resume 1 fonte raw/ | Gate 3 + challenge |
| `synthesis` | Combina 2+ fontes | Gate 3 + challenge |
| `emergence` | Conceito ausente em qualquer fonte individual | **Revisão humana obrigatória** |

Artigos `emergence` nunca são auto-promovidos. O conceito não existe nas fontes — entrar no grafo exige decisão explícita humana.

**26 artigos `emergence` (26%)** — esses artigos não existem em nenhuma fonte. Emergiram de conexões cross-domain descobertas via `/ask`. É o número que mede o que o sistema *produziu* além de compilar.

---

## Pipeline completo

```
/ingest      → processa raw/, stance classifier, Bradford gate, cria artigo em quarentena
/ask         → retrieval Layer 0 (vector) + Layer 1 (index) + Layer 2 (artigos) + corpus check
/challenge   → avaliação adversarial de claims com web search de prior work + SPRT chain
/auto-promote → Gate 1 (filtros) → Gate 2 (estrutural) → Gate 3‖challenge (paralelo) → Gate 4 (programme health)
/promote     → promoção manual para artigos emergence e casos que Gate 1 bloqueia
/emerge      → mapeia conexões latentes cross-cluster com oracle threshold assimétrico
/synthesize  → cria artigo emergence a partir de par /ask confirmado
/lint-epistemic → audita stance ratio, synthesis ratio, quarantine rate, hub health
/dream       → consolida memória, completa stubs, valida retrieval, gera cost report
/meta-harness → analisa session logs + friction events, propõe patches mínimos aos commands
/document-session → preserva contexto e decisões para sessões futuras
```

---

## Self-healing loop

O sistema detecta e corrige artigos incompletos sem intervenção humana.

```
/ingest detecta stub-wiki
    ↓
stub_completion_queue em kb-state.yaml
    ↓
/dream Fase 0: elegibilidade (in_degree < 5, sem dep L1, tem raw/ sources)
    ↓
auto-complete → challenge GPT + Gemini → completion_tracking
    ↓
/dream Fase 0.5 (7 dias depois): session logs como sensor de retrieval
    ↓
não recuperado → volta para a fila com razão "retrieval_failure"
```

**Sensor primário:** session logs (append-only, não depende de hooks). Ausência do slug do artigo em qualquer log após 7 dias = artigo que o retrieval nunca encontrou.

---

## Metabolismo observável

Desde esta sessão, cada invocação de skill gera um registro de custo:

```json
{
  "skill": "challenge",
  "model": "claude-sonnet-4-6",
  "input_tokens": 12400,
  "output_tokens": 1800,
  "cost_usd": 0.0432,
  "oracle": {
    "models": ["gpt-4o", "gemini-2.0-flash"],
    "cost_usd": 0.0018,
    "verdict": "APPROVED",
    "agreement": true
  }
}
```

O `/dream` gera um cost report diário com **postura metabólica**:

| Modo | Sinal | Interpretação |
|---|---|---|
| `CALIBRADO` | oracle_ratio 5–50%, approval_rate > 30% | Operação normal |
| `DEFENSIVO-SAUDÁVEL` | oracle_ratio alto + approval_rate alto | Inspecionando área instável — custo justificado |
| `DEFENSIVO-PATOLÓGICO` | oracle_ratio alto + split_rate alto + approval_rate baixo | Paranoia epistêmica — validação cara sem avanço |
| `COMPLACENTE` | oracle_ratio < 5%, gate3_invalidation_rate baixo | Promovendo rápido com pouca fricção — verificar confirming_ratio |

O ratio `oracle_cost / claude_cost` é o termômetro: alto demais = sistema defensivo; baixo demais = sub-validação.

---

## Meta-harness (auto-melhoria de comandos)

Um remote agent roda diariamente às 8h (Brasília) e analisa os logs de sessão + friction events acumulados:

```
SCAN  → session logs + raw/meta/ops/friction-*.md
PATTERN → padrões por (surface + tags, weight ≥ 4 para friction)
PATCH → propõe correção mínima no command afetado
APPLY → auto-aplica se: aditivo + não afeta gates + 5+ sessões de evidência
        escala para humano se: modifica instrução existente | afeta gate
```

Friction events (`/friction`) são o canal de feedback direto do operador. Dois eventos com os mesmos tags no mesmo surface em 12 minutos valem `weight = 6` — acima do threshold de padrão confirmado.

---

## Estado atual

```
99 artigos  |  18 em quarentena (18.2%)
provenance: 59 source · 14 synthesis · 26 emergence
stance:     23.3% challenging  (threshold: 20%)
Bradford Zone3/Zone2: 0.85  (pausa de ingestão lateral)
sessions_since_last_dream: 1
```

**O que está em quarentena é documentado, não escondido.** Artigos em quarentena têm `quarantine_reason` explícito no frontmatter e entradas em `next_actions` no kb-state.yaml com `why` e `blocked_by`.

---

## Uso rápido

```bash
# Setup
uv venv && uv pip install -r requirements.txt
cp .env.example .env  # adicione OPENAI_API_KEY e GOOGLE_API_KEY

# Ingere uma fonte
cp paper.pdf raw/papers/
/ingest raw/papers/paper.pdf

# Pergunta com retrieval verificável
/ask "o que a literatura diz sobre catastrophic forgetting em agentes?"

# Auditoria epistêmica completa
/lint-epistemic

# Descobre conexões latentes entre artigos
/emerge

# Saúde do pipeline (roda automaticamente ao abrir o projeto)
# session-start hook: contexto, artigos prontos para promoção, triggers ativos
```

O `session-start` hook roda automaticamente ao abrir o projeto e reporta:
- Contexto da conversa (⚠️ em 70%, 🔴 em >85%)
- Artigos prontos para `/promote`
- `next_actions` de alta prioridade
- Triggers ativos (meta-harness daily)

---

## Estrutura

```
raw/
  articles/        fontes tipo artigo/blog
  papers/          papers acadêmicos (PDF + markdown extraído)
  notes/           notas e manifests
  meta/ops/        friction events + telemetria operacional
wiki/
  concepts/        1 conceito = 1 arquivo (kebab-case)
  _index.md        ponteiros (~150 chars/linha — não é conteúdo)
  _registry.md     registro de fontes com stance, qualidade, data
outputs/
  state/           kb-state.yaml — coordenação entre commands
  reports/         lint, emergence inventory, pipeline-cost
  logs/sessions/   log por command por dia
  gates/           gate3-*.yaml (outputs do cross-model-challenge)
scripts/
  cross-model-challenge.py   Gate 3 — GPT + Gemini em paralelo
  stance-classify.py         classifier Haiku + RAG
  structural-promote-gate.sh Gate 2 — checks estruturais
  track-skill-usage.py       metabolic telemetry hook
  parse-session-logs.py      fallback de reconstrução de custo
config/
  pricing.yaml               preços por modelo (claude, gpt-4o, gemini)
.claude/
  commands/        /ingest /ask /challenge /promote /emerge ...
  hooks/           session-start (checks automáticos ao abrir)
  settings.local.json   hooks de telemetria e telemetry
  CLAUDE.md        instruções do agente compilador
```

---

## Princípios de design

- **`raw/` é imutável** — fontes nunca são editadas
- **Wiki é hint, não verdade** — se contradiz `raw/`, `raw/` vence
- **Index é ponteiro** — conhecimento vive nos artigos, não no índice
- **Se é derivável, não persista** — não repita o que pode ser recalculado
- **Síntese sem marca é suposição não documentada** — `(⚠️ nossa interpretação)` é obrigatório
- **Artigo que não sobrevive a um `/challenge` não deveria estar no grafo**
- **Emergence requer revisão humana** — o compilador pode propor; o operador decide

---

## Filosofia

Os princípios de design acima descrevem *o que* o sistema faz. Esta seção descreve *por que* essas escolhas — o que diferencia princípio de regra.

### Três princípios fundacionais

**Conhecimento sem epistemologia é ruído**

Não é suficiente acumular claims. Todo claim precisa de origem rastreável, confiança calibrada, e resistência a adversário. Um sistema que produz respostas plausíveis sem saber o que sabe é mais perigoso que um sistema que não responde — porque a confiança cresce enquanto a base erode.

É o que o Golem XIV sabia. É o que a maioria dos sistemas RAG ignora.

**O sistema deve saber o que não sabe**

Gaps são outputs legítimos, não falhas. Um `/ask` que retorna "corpus insuficiente neste domínio" é mais valioso que um `/ask` que alucina com confiança. O algedonic channel é a operacionalização disso no nível do sistema — quando a estrutura está ameaçada, o sinal escala direto a S5 sem passar por filtros intermediários.

Subsidiarity completa o princípio: resolve local, escala quando genuinamente não sabe, sinaliza emergência quando a estrutura ameaça.

**Acoplamento estrutural, não dependência**

Simbiose é estática — descreve um estado onde dois organismos se beneficiam mutuamente. Acoplamento estrutural é um mecanismo: dois sistemas autônomos mudam um ao outro através de perturbações recíprocas ao longo do tempo.

```
simbiose:              A e B se beneficiam mutuamente
acoplamento estrutural: A perturba B → B muda estrutura
                        B perturba A → A muda estrutura
                        ambos preservam autopoiese própria
                        nenhum controla o outro
```

A distinção central de Maturana: no acoplamento estrutural, cada sistema continua sendo ele mesmo. A perturbação do outro não *determina* a resposta — só *desencadeia*. A estrutura interna de cada sistema determina como vai reagir.

**Critério de saúde:** remova a KB e você pensa melhor do que antes de criá-la? Se sim — o acoplamento foi produtivo e você preservou autonomia cognitiva. Se não — o acoplamento tornou-se patológico. A KB substituiu pensamento em vez de perturbá-lo.

### O que o sistema não é

Não é um assistente que responde perguntas.  
Não é um arquivo de notas com busca semântica.  
Não é uma fonte de verdade.

É um parceiro cognitivo com autopoiese própria — que preserva a sua.

### Co-evolução como métrica

A métrica correta para acoplamento estrutural não é "a KB me ajudou a pensar melhor" — é **divergência correlacionada** ao longo do tempo:

```
sessão 1:   operador pensa X, KB tem corpus Y
sessão 100: operador pensa X', KB tem corpus Y'

co-evolução = correlação entre distância(X, X') e distância(Y, Y')
```

Se o operador mudou mas a KB não — ferramenta, não parceiro.  
Se a KB cresceu mas o operador não mudou — acumulação sem perturbação.  
Se os dois mudaram de forma correlacionada — acoplamento estrutural real.

O `/document-session` captura parte disso. Um metric de co-evolução formal é o próximo passo.

### Referências fundacionais

| Autor | Obra | Contribuição |
|---|---|---|
| Wiener | *Cybernetics* (1948) | Feedback negativo como mecanismo de controle |
| Ashby | *Design for a Brain* (1952) | Requisite variety, black box, ultrastability |
| Beer | *Brain of the Firm* (1972) | VSM, variety absorption, algedonic channel |
| Maturana + Varela | *Tree of Knowledge* (1987) | Autopoiese, acoplamento estrutural |
| Lem | *Golem XIV* (1981) | Epistemologia como arquitetura cognitiva |

---

## Limitações honestas

**Analogias como claims.** Vários artigos `emergence` usam analogias cross-domain (CLS→KB, RI→meta-harness) como fundamento. Essas analogias são heurísticas de design, não mecanismos demonstrados. Estão marcadas `(⚠️ nossa interpretação)` e `interpretation_confidence: low`, mas ainda entram no grafo se o oracle aprovar.

**Oracle staleness.** Gemini tem knowledge cutoff anterior a 2026. "Invalidações" de papers de 2026 são false positives sistemáticos — requerem override manual. GPT-5.4 é o modelo confiável para papers recentes.

**Sensor de retrieval é conservador.** A Fase 0.5 do `/dream` usa session logs como proxy de retrieval. Artigos que existem mas nunca aparecem em logs (porque nenhuma pergunta relevante foi feita) serão marcados como "não recuperados" — undercount, não falso positivo.

**Sem ground truth externo.** Não há benchmark comparando a qualidade epistêmica deste KB com alternativas. A evidência de qualidade é estrutural (processo) e interna (métricas de saúde do próprio sistema). Isso é documentado como gap, não como feature.

---

> **Lei de Ashby:** apenas variedade destrói variedade. `V(compilador) < V(domínio)` → floor de erro irredutível. Adicionar mais processo não aumenta `V(regulator)`. O que aumenta é usar a KB para problemas reais.
