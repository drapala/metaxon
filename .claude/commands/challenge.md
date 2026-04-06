# /challenge [artigo]

Avaliação adversarial de um artigo wiki antes de usá-lo como fonte ou publicar.

## Processo

1. **Leia o artigo** indicado pelo usuário (wiki/concepts/nome.md)

2. **Identifique os 3 claims mais fortes** — as afirmações centrais que o artigo faz.

3. **Para cada claim, avalie:**

   a. **Evidência mais fraca:** qual a fonte mais frágil que suporta este claim?
      Se depende de uma única fonte tertiary (tweet, opinião), flag.

   b. **Prior work:** existe trabalho anterior que já cobre isso?
      Verificar nos raw/ sources disponíveis. Se não souber, escrever
      "não verificado — buscar antes de publicar."

   c. **Cenário de falha:** descreva um cenário concreto e plausível onde
      este claim não se sustenta. Se não conseguir imaginar um, o claim
      pode estar excessivamente vago.

   d. **Citação raw verificada:** o claim tem citação rastreável em raw/?
      Se não, marcar como INTERPRETAÇÃO ou ESPECULAÇÃO.

4. **Classifique cada claim:**
   - **SÓLIDO** — 2+ fontes primary concordam, cenário de falha é edge case
   - **PRECISA REVISÃO** — 1 fonte ou interpretação não marcada
   - **ESPECULAÇÃO NÃO MARCADA** — apresentado como fato sem evidência empírica

5. **Verifique seção ## Interpretação:**
   - Existe? Está separada de ## Conteúdo?
   - Claims interpretativos estão na seção certa?

6. **Web search por prior work:**
   Para cada claim central, busque:
   - "[conceito central] agent memory 2024 2025 2026 arxiv"
   - "[conceito central] limitations OR criticism"
   - "[conceito central] benchmark OR evaluation"
   Liste os 3-5 papers mais relevantes que a KB NÃO contém.
   Para cada um: título, URL, qual claim do artigo afeta.
   Se encontrar paper que invalida um claim, marcar como RISCO ALTO.

## Formato de report

```
ARTIGO: [nome]

CLAIM 1: "[texto do claim]"
  Evidência: [fonte mais fraca]
  Prior work: [existe? onde?]
  Cenário de falha: [descrição]
  Citação raw: [confirmada / não encontrada]
  VEREDICTO: SÓLIDO / PRECISA REVISÃO / ESPECULAÇÃO NÃO MARCADA

CLAIM 2: ...

CLAIM 3: ...

CLASSIFICAÇÃO GERAL: PUBLICÁVEL / PRECISA CORREÇÃO / RISCO ALTO
AÇÃO RECOMENDADA: [o que fazer antes de usar como fonte]

PRIOR WORK (web search):
  1. [Título] — URL — afeta claim N — INVALIDA/REFINA/CONFIRMA
  2. ...

CHAIN CONTROL (SPRT):
  Chain depth atual: [leia kb-state.yaml → ingest_chain.depth, default 0]
  Ação por tipo de prior work encontrado:
    INVALIDA → ingest_action: AUTO (1 paper máximo, chain encerra)
    REFINA   → ingest_action: QUEUE (entra em ingest_queue, sem auto-trigger)
    CONFIRMA → ingest_action: IGNORE
  Resultado: CHAIN_CLOSED | CHAIN_QUEUED | CHAIN_IGNORED
```

## Quando rodar

- Antes de citar um artigo de síntese em outputs/ (reports, LinkedIn posts)
- Antes de usar um artigo como base pra novo artigo
- Quando interpretation_confidence é medium ou low
- Quando /review flagga over-synthesis

## Log de occurrent

Salve resultado em `outputs/logs/sessions/YYYY-MM-DD/challenge-[artigo]-HH-MM.md`
segundo schema em `wiki/meta/process-log.md`.
Campos: claims_challenged, claims_survived, claims_weakened, claims_invalidated,
prior_work_found, verdict.

---

## Pipeline — kb-state.yaml

### Lê (início)
- `corpus.quarantined_list` — se artigo está em quarentena, o challenge pode satisfazer critério 3 do /promote
- `active_triggers` — imprima qualquer trigger `priority: high` antes de começar

### Escreve (final)
```yaml
updated: YYYY-MM-DD
challenge:
  challenged_since_last_promote:
    - artigo: [nome]
      verdict: PUBLICÁVEL | PRECISA_CORREÇÃO | RISCO_ALTO
      data: YYYY-MM-DD
      claims_survived: N
      claims_total: N
```

### Gatilhos — verifique ao final

| Condição | Gatilho |
|----------|---------|
| Artigo está em quarentena E verdict ≠ RISCO_ALTO | `💡 /promote [artigo] — critério 3 satisfeito pelo challenge. Verifique critérios 1 e 2.` |
| Verdict = RISCO_ALTO em artigo com in-degree alto | `⚠️ Propagação — [artigo] tem alto in-degree e claims em risco. Verifique artigos que o citam.` |
| Prior work INVALIDA claim central E chain_depth = 0 | `💡 /ingest [paper] — paper invalida claim. SPRT: 1 ingest permitido, chain encerra após.` |
| Prior work INVALIDA claim central E chain_depth ≥ 1 | `🚫 SPRT CHAIN CLOSED — já ingerimos 1 paper contraditório nesta chain. Adicione à ingest_queue manual.` |
| Prior work REFINA claim | `📥 Queue — paper refina claim. Adicione a ingest_queue_priority (sem auto-trigger).` |
| Prior work CONFIRMA claim | `— IGNORE — paper confirma claim existente. Não ingira.` |

### SPRT Chain Control — kb-state.yaml

Ao final do challenge, atualize o bloco `ingest_chain` em kb-state.yaml:

```yaml
ingest_chain:
  depth: N              # incrementado a cada auto-ingest por challenge
  origin_article: [artigo que iniciou a chain]
  last_challenge: YYYY-MM-DD
  status: open | closed  # closed após 1 INVALIDA auto-ingested
```

Regras:
- `depth = 0` → chain não iniciada (challenge manual ou pós-ingest-hook)
- `depth = 1, status: closed` → chain encerrada após 1 INVALIDA ingerido
- Ao iniciar novo /ingest manual: resete `depth: 0, status: open`
- Nunca auto-ingeste se `status: closed`

### Atualiza `next_actions` em kb-state.yaml

Após o challenge, atualize o bloco `next_actions`:
- Se artigo em quarentena E verdict ≠ RISCO_ALTO: adicione entrada `/promote [artigo]`
  com `why: "critério 3 satisfeito pelo challenge"`, `added_by: challenge`
- Se prior work INVALIDA E chain_depth = 0: adicione entrada `/ingest [paper mais relevante]`
  com `why: "[claim que invalida] — SPRT: auto-ingest único permitido"`, `added_by: challenge`
  Marque o ingest com `chain_triggered: true` para que /ingest incremente `ingest_chain.depth`
- Se prior work REFINA: adicione à `ingest_queue_priority` com `auto_trigger: false`
  (nunca dispara challenge automático)
- Se verdict = RISCO_ALTO: adicione entrada `/review [artigos que citam este]`
  com `why: "propagação de claim em risco"`, `added_by: challenge`

Atribua `priority` de forma que ações de correção (RISCO_ALTO) sempre precedam
ações de avanço (/promote, /ingest).

## Post-challenge: trigger /auto-promote (condicional)

Executar após next_actions atualizado e challenge log salvo.

**Condição de disparo** — todos os três devem ser verdade:
1. Artigo tem `quarantine: true`
2. verdict ≠ RISCO_ALTO
3. Critério 3 satisfeito neste challenge:
   - `prior_work_found >= 3` (web search realizado com resultado), **OU**
   - Artigo tem seção `## Verificação adversarial` ou `## Predição falsificável` com pearl_level L2+

Se condição satisfeita:
1. Imprimir: `🔄 post-challenge hook: critérios 2+3 satisfeitos. Rodando /auto-promote automaticamente em [artigo].`
2. Executar `/auto-promote [artigo]` com metadata:
   - `triggered_by: post_challenge_hook`
   - `challenge_log: outputs/logs/sessions/YYYY-MM-DD/challenge-[artigo]-HH-MM.md`
3. **Guard de aninhamento:** se o contexto atual já tiver `triggered_by` presente → NÃO disparar. Imprimir: `⚠️ post-challenge hook: contexto aninhado detectado — /auto-promote suprimido.`

Se `/auto-promote` falhar:
- Imprimir: `⚠️ post-challenge hook: /auto-promote falhou — [motivo]. Artigo permanece em quarentena.`
- NÃO silenciar. Entrada `/promote [artigo]` já está em next_actions como fallback manual.
