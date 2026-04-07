# Sessão de Construção do llm-kb — Documentação Parte 20
**Data:** 2026-04-06
**Contexto:** Autopoiese, telemetria metabólica, self-healing loop com retrieval validation, challenge adversarial de artigo de emergência, e extensão do meta-harness com sensor de friction.

---

## Resumo das Partes Anteriores
*Ver documentações anteriores para detalhes completos.*
- Part 1-10: Stack construída (LanceDB, embeddings, API, MCP, hybrid search, stance classifier, bradford gate)
- Part 11-14: Pipeline de promoção autônoma (4 gates, Gate 3∥challenge paralelo, veto hierárquico, /auto-promote)
- Part 15: Oracle threshold assimétrico (GPT≥5 AND Gemini≥8 para /emerge)
- Part 16: wiki/strategy/, /foresight, 3 artigos de estratégia
- Part 17: Sessão 6 /emerge — 3 GENUINE (zelox-vsm×VSM, epistemic-merge×FM, APV×CLS)
- Part 18: AI Coordination ingerido; ai-coordination-compressing-capital quarentenado (Gate 3: 3 invalidated)
- Part 19: 2 papers harness (NLAH, meta-harness) ingeridos e promovidos; emerge sessão 7: NLAH×CLS (INSTANCIA) e meta-harness×RI (ANÁLOGO-A)

---

## Fases desta Sessão

### Fase 1 — Automação do meta-harness via remote trigger

**O que foi feito:**
Configurado remote Claude Code trigger (CCR) para rodar o pipeline meta-harness diariamente às 8h Brasília (11h UTC). O trigger roda na infraestrutura Anthropic com checkout do repositório GitHub — não é cron local. Criado arquivo `.claude/triggers/meta-harness-daily.md` com ID do trigger, instruções de recriação e observações sobre o que o CCR não tem acesso (friction files locais — workaround: commit automático às 19h).

**Resultado:**
- Trigger ativo: `trig_01XeqJMQdGryevqQoM8Kh9g9`
- Cron: `0 11 * * *` (UTC) = 8h Brasília
- Modelo: claude-sonnet-4-6
- Repo: `https://github.com/drapala/llm-kb`

**Decisão importante:**
O CCR não tem acesso ao filesystem local — friction files em `raw/meta/ops/` só ficam visíveis para o trigger depois do commit das 19h. Isso foi aceito como limitação de design, não como bug.

---

### Fase 2 — Paralelização de embed() no ingest.py

**O que foi feito:**
Identificado que `embed()` em `scripts/single-brain/ingest.py` usava `ThreadPoolExecutor` mas com imports faltantes (`ThreadPoolExecutor`, `as_completed` não estavam no topo do arquivo). Corrigido e ajustado `EMBED_WORKERS = 6 → 10` baseado em ratio I/O:CPU de 38:1 medido em profiling anterior.

**Resultado:**
- Import adicionado: `from concurrent.futures import ThreadPoolExecutor, as_completed`
- Workers: 6 → 10
- Validação: 4/4 chunks idênticos entre sequencial e paralelo
- Speedup esperado: ~2.8x (benchmark anterior: 7.26s → 2.56s em 87 chunks)

**Insight chave:**
O bug de import existia silenciosamente — Python teria lançado `NameError` na primeira execução paralela real. A validação de identidade de chunks (não só ausência de erro) é o teste certo para paralelização de embedding.

---

### Fase 3 — Sensor de synthesis ratio quebrado no lint-epistemic

**O que foi feito:**
Rodei `/lint-epistemic`. Circuit breaker ativou: 86/100 artigos sem seções epistêmicas detectáveis. Root cause: o comando procurava `### Especulação` e `### Descrição` (template antigo) mas artigos atuais usam `## Conteúdo` e `## Interpretação` (template corrente). Fix aplicado no `.claude/commands/lint-epistemic.md`: detecção por template atual primeiro, legacy como fallback, contagem por palavras (não bullets).

**Resultado:**
- Antes: 86/100 no circuit breaker, synthesis ratio indetectável
- Depois: 99/99 artigos detectados, 0 stubs de conteúdo
- Crítico: a regex `(?=^##|\Z)` para em `###` porque `###` começa com `##`. Fix: `(?=^## |\Z)` com espaço força match apenas em headings de nível 2

**Insight chave:**
O sensor estava morto desde que o template evoluiu. A KB cresceu para 100 artigos com um dos seus 4 healthchecks silenciosamente desativado. Nenhum alerta — o circuit breaker registrou "não mensurável" mas não escalou. Isso é exatamente o failure mode FM1 (metrics stay green while quality erodes) em miniatura, no próprio sistema de detecção.

---

### Fase 4 — Self-healing loop: autopoiese via Fase 0 + Fase 0.5 no /dream

**O que foi feito:**
Longa fase de design e implementação do ciclo de autopoiese para artigos incompletos.

**Problema identificado:**
O sistema podia criar artigos (via /ingest + stub-wiki), mas não tinha mecanismo para:
1. Detectar quais ficaram incompletos
2. Completá-los automaticamente com verificação adversarial
3. Verificar se os completados são recuperados pelo retrieval

**Design aprovado:**
```
/ingest → stub-wiki → stub_completion_queue
              ↓
/dream Fase 0 → detecta stubs → Option B eligibility → auto-complete → GPT/Gemini challenge
              ↓
/dream Fase 0.5 → 7 dias depois → session logs como sensor primário → retrieval_confirmed
              ↓
não-recuperado → volta para stub_completion_queue com razão "retrieval_failure"
```

**Distinção crítica (autopoiese vs monitoramento):**
Monitoramento passivo: observa estado, reporta. Autopoiese: a observação alimenta o próximo ciclo de produção. A Fase 0.5 fecha o loop — o artigo que não é recuperado re-entra na fila de completude, é reescrito, e observado novamente. O sistema se corrige sem intervenção.

**Sensor primário escolhido: session logs (opção B):**
Razão: `reads` no frontmatter depende do utility-tracker ser executado (não append-only, pode ser falho). Session logs são append-only, não dependem de nenhum hook, e a presença do slug do artigo no log é evidência direta de retrieval bem-sucedido.

**Resultado:**
- Fase 0 adicionada ao `/dream` (seções 0.1-0.4): detecção de stubs, Option B eligibility, stub_completion_queue em kb-state.yaml, auto-complete com challenge externo + validation
- Fase 0.5 adicionada ao `/dream`: retrieval validation com janela 7 dias, `completion_tracking` schema em kb-state.yaml
- Step 15.5 adicionado ao `/ingest`: ao registrar stub-wiki, computa `completion_priority = in_degree × 2 + reads` e atualiza stub_completion_queue
- `stub_completion_queue` bootstrapped em kb-state.yaml com 9 entradas do domínio B2G/procurement (fontes ingeridas mas artigos ainda incompletos)

**Insight chave:**
O critério de elegibilidade Option B (`in_degree < 5` + sem dep L1 + tem raw/ sources) é o firewall que protege artigos hub de completude automática. Um artigo como `autonomous-kb-failure-modes` (in_degree ≥ 5) nunca seria auto-completado — só revisão humana. A Fase 0 tem blast radius limitado por design.

---

### Fase 5 — /challenge raw-design-constraints

**O que foi feito:**
Challenge adversarial no artigo emergido de /ask cross-domain (knowledge-collapse-llm × complementary-learning-systems). Artigo em quarentena há 24h+ com todos os critérios de saída satisfeitos. Primeiro challenge de um artigo com `provenance: emergence` nesta KB.

**Claims avaliados:**

| Claim | Descrição | Veredicto |
|-------|-----------|-----------|
| 1 | Source primacy: raw/ como "dado real" que ancora sínteses | PRECISA REVISÃO |
| 2 | Topical diversity: diversidade de raw/ como interleaving CLS | PRECISA REVISÃO |
| 3 | Compound failure (violar ambos) = mais perigoso e invisível | SÓLIDO |

**Problema encontrado:**
Dois parágrafos de "Implicação para raw/:" em `## Conteúdo` não tinham marcador `(⚠️ nossa interpretação)`, apesar de serem analogias interpretativas. O frontmatter declarava `interpretation_confidence: low` mas o corpo não era consistente. As implicações (LLM training → KB design) são válidas como heurística de design, não como mecanismo demonstrado — a analogia CLS→KB não é mecanisticamente tight porque catastrophic interference ocorre em backpropagation, não em curadoria de arquivos.

**Correções aplicadas:**
Prefixo `(⚠️ nossa interpretação)` adicionado nos dois parágrafos de implicação em `## Conteúdo`.

**Prior work encontrado:**
- arXiv:2410.02825 (Ingest-And-Ground): REFINA Claim 1 — RAG grounding é mitigação ativa de colapso, não apenas preventiva. Adicionado a ingest_queue_priority.
- arXiv:2510.24476 (Hallucination Survey): CONFIRMA Claim 1
- arXiv:2402.07867 (PoisonedRAG): REFINA Claim 3 — degradação silenciosa de KB documentada em contexto de ataque

SPRT: CHAIN_IGNORED (nenhum INVALIDA encontrado).

**Post-challenge hook → /auto-promote → Gate 1:**
`provenance: emergence` bloqueia auto-promote por design — artigos emergidos requerem `/promote` manual. Esta é a decisão correta: `provenance: emergence` significa que o artigo propõe um conceito não presente em nenhuma fonte individual. Esse tipo de claim deve entrar no grafo por decisão humana explícita.

Todos os critérios de quarentena agora satisfeitos (tempo ✓, review_frio ✓, adversarial ✓). Artigo pronto para `/promote raw-design-constraints`.

**Insight chave:**
Gate 1 do /auto-promote para emergence não é bug — é a separação correta entre promoção automática (claims derivados de fontes) e promoção deliberada (claims emergidos de combinação). O post-challenge hook disparou corretamente, chegou no limite correto, e produziu a ação correta (adicionar /promote manual ao next_actions).

---

### Fase 6 — Friction sensor no meta-harness

**O que foi feito:**
Dois friction events foram registrados nesta sessão:
- `friction-2026-04-06-23-00.md`: pós-sessão longa, next_actions invisíveis sob volume de outputs
- `friction-2026-04-06-23-12.md`: artigo raw-design-constraints pronto há >24h sem surfaceamento como evento prioritário

Isso levou ao design e implementação do **friction sensor no meta-harness**: a Step 1B do SCAN agora lê todos os `raw/meta/ops/friction-*.md`, extrai tipo/surface/severity/tags, e monta lista B. A Step 2B computa padrões com `weight = (friction_count × 2) + sum(severity_scores)` e threshold ≥ 4. Step 2C aplica cross-signal boost (+2) quando friction confirma pattern de session log no mesmo surface.

**Resultado:**
O meta-harness agora tem dois canais de sinal:
- **Canal A (session logs):** padrões comportamentais do sistema ao longo do tempo
- **Canal B (friction files):** percepção direta do operador de onde há atrito

Quando os dois convergem no mesmo surface, o peso do padrão A é aumentado — sinal cruzado como evidência mais forte.

**Insight chave:**
Os dois friction events desta sessão têm o mesmo padrão: `invisible-state` + `next-action-missing` no surface `quarantine`. Isso é exatamente o tipo de sinal que o meta-harness vai capturar nas próximas execuções e propor um patch — provavelmente um evento `quarantine_stale` no session-start quando artigo está pronto há >24h sem ação.

---

### Fase 7 — Telemetria metabólica

**O que foi feito:**
Implementação completa de pipeline de cost tracking para todas as invocações de skill.

**Por que "metabólico":**
A KB já tinha dois eixos de saúde: epistêmico (lint-epistemic) e vitalidade de programa (programme_health.confirming_ratio). O terceiro eixo — eficiência metabólica — estava ausente. Em termos VSM: S3 (otimização) precisava de sinal de custo além do sinal epistêmico. O cost report fecha o canal algedônico financeiro.

**O que foi construído:**

| Componente | O que faz |
|------------|-----------|
| `config/pricing.yaml` | Preços dos 3 modelos (claude-sonnet-4-6, gpt-4o, gemini-2.0-flash) |
| `scripts/track-skill-usage.py` | PostToolUse hook: lê stdin JSON, calcula cost_usd via pricing.yaml, detecta oracle costs de gate3-*.yaml, append em skill-usage.jsonl |
| `scripts/parse-session-logs.py` | Fallback: lê session JSONL do Claude Code, reconstrói token deltas por Skill invocation sem duplicar registros do hook |
| `.claude/settings.local.json` | PostToolUse Skill hook → track-skill-usage.py (best-effort, timeout 10s) |
| `/dream` Fase X (Passo 4.5) | 3 tabelas: custo por skill, capital allocation, custo oracle; salva pipeline-cost-YYYY-MM-DD.md |

**Schema de registro:**
```json
{
  "skill": "challenge",
  "model": "claude-sonnet-4-6",
  "input_tokens": 5000,
  "output_tokens": 800,
  "cost_usd": 0.0306,
  "oracle": {"models": ["gpt-4o"], "cost_usd": 0.001, "verdict": "APPROVED", "agreement": true}
}
```

**Insight chave:**
O ratio `oracle_cost / claude_cost` é o número mais revelador da capital allocation table. Um ratio alto (>50%) significa que o sistema está em modo defensivo — gastando mais em validação do que em exploração. Um ratio baixo pode significar sub-validação. O ponto ótimo varia com o estado do programa (zona degenerativa → mais validação; zona progressiva → mais exploração).

**Limitação de design conhecida:**
Usage tokens não estão disponíveis no hook PostToolUse de Skill (o hook não tem acesso ao uso de tokens da invocação de skill em si). O `parse-session-logs.py` resolve isso como fallback — lê o JSONL da sessão e reconstrói os deltas. Registros do hook têm `source: "hook"`, do fallback têm `source: "parsed"`.

---

## Estado Final desta Sessão

### Métricas

| Métrica | Valor |
|---------|-------|
| Wiki concepts (total) | ~100 |
| Artigos desafiados esta sessão | 1 (raw-design-constraints) |
| Artigos prontos para /promote | 1 (raw-design-constraints — todos critérios ✓) |
| Friction files registrados hoje | 2 (surface: quarantine × 2, invisible-state pattern) |
| Commits esta sessão | 4 |
| Novos scripts criados | 2 (track-skill-usage.py, parse-session-logs.py) |
| Novos arquivos de config | 1 (config/pricing.yaml) |
| Comandos modificados | 3 (lint-epistemic, dream, meta-harness) |
| Hooks adicionados | 1 (PostToolUse Skill) |
| quarantine_rate | 18% (18/100, ⚠️ acima de 15%) |
| Remote triggers ativos | 1 (meta-harness, 8h Brasília) |

### Insights gerados

1. **Circuit breaker morto é FM1 em miniatura:** O sensor de synthesis ratio estava silenciosamente desativado por template drift. A KB cresceu para 100 artigos com healthcheck inoperante sem nenhum alerta. O próprio sistema de detecção de degradação epistêmica exibiu degradação epistêmica.

2. **Autopoiese ≠ monitoramento:** A distinção é que o loop de observação deve alimentar o próximo ciclo de produção, não apenas reportar. A Fase 0.5 fecha o loop: não-recuperado → reescrito → observado novamente. Isso é o que diferencia o self-healing da KB de um dashboard.

3. **Session logs como sensor primário de retrieval:** Mais robusto que `reads` no frontmatter (que depende do utility-tracker ser executado). Logs são append-only e não dependem de nenhum hook. Essa decisão (opção B) tem implicação de design: o sensor é conservador (undercount), mas nunca produz falsos positivos.

4. **Option B eligibility é firewall, não otimização:** Os critérios `in_degree < 5` + `sem dep L1` + `tem raw/ sources` não são para selecionar "os melhores candidatos" — são para excluir "os que não podem ser autocomplete com segurança". Artigos hub ficam fora por design.

5. **provenance: emergence como gate humano:** O /auto-promote bloquear em Gate 1 para emergence não é limitação — é o design correto. Claims que emergem da combinação de fontes (não de nenhuma fonte individual) precisam de validação humana explícita antes de entrar no grafo. O post-challenge hook chegou no limite certo.

6. **Friction cruzado = cross-signal algedônico:** Dois friction events com mesmos tags no mesmo surface em 12 minutos (`quarantine/invisible-state/next-action-missing`) é exatamente o padrão que o meta-harness vai detectar como evidência weight ≥ 4. O sistema registra seu próprio ponto cego para corrigi-lo na próxima execução do harness.

7. **Oracle ratio como métrica de saúde metabólica:** Não existe valor "correto" para oracle_cost/claude_cost — depende do estado do programa. Na zona progressiva, validação externa deve ser mais barata que exploração. Na zona degenerativa (quarantine_rate alto), o ratio deve subir porque o sistema precisa limpar antes de expandir.

8. **Analogia CLS→KB é heurística, não mecanismo:** A afirmação "diversidade tópica previne interferência catastrófica no KB" não tem o mesmo status epistêmico que "interleaved learning > blocked learning em redes neurais". O primeiro é uma analogia de design útil; o segundo é resultado experimental replicado. O /challenge corretamente forçou marcação ⚠️ nos parágrafos de implicação.

### Pendências prioritárias

| Prioridade | Item |
|------------|------|
| P1 | `/promote raw-design-constraints` — todos os critérios satisfeitos |
| P1 | `/challenge evaluation-order-independence` — quarantine_rate ainda em 18% |
| P2 | Sub-índices wiki — CRÍTICO (100 artigos > 80 threshold) |
| P2 | `/ingest Brain of the Firm (Beer 1972)` — VSM S1-S5 formal ausente |
| P3 | `/challenge ai-coordination-compressing-capital` (5 claims weakened Gate 3) |
| P3 | `/challenge deer-flow-concurrency` (3 claims invalidados Gate 3) |
| P3 | `/challenge pressure-field-coordination` (3 invalidated) |
| P3 | `/challenge emergent-coordination-measurement` (1 invalidated + 6 weakened) |
| P4 | `/ingest Epistemic Diversity & Knowledge Collapse (arXiv:2510.04226)` — challenging |
| P4 | `/ingest Ingest-And-Ground (arXiv:2410.02825)` — REFINA raw-design-constraints |
| Monitorar | `outputs/reports/skill-usage.jsonl` — validar que hook captura registros em próximas sessões |

---

## A Frase que Resume esta Sessão

A sessão fechou três loops que estavam abertos: o loop de autopoiese (artigos incompletos agora têm ciclo de completude → validação → observação de retrieval), o loop de observabilidade do sistema (friction events agora alimentam o meta-harness), e o loop de custo (cada invocação de skill agora tem sinal metabólico) — e em todas as três, a descoberta foi a mesma: o que parecia um problema de monitoramento era um problema de fechamento de loop.

---

*Documentado em 2026-04-06. 7 fases. Sessão orientada a loops: autopoiese, friction sensing, telemetria metabólica.*
