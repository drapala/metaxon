# /auto-promote [artigo]

Executa o pipeline de promoção automática conforme [[kb-auto-promote-protocol]].
Substitui o ciclo manual quarentena → /review → /challenge → /promote.

Reserva revisão humana apenas quando risco real é detectado.

**Princípio de independência:** Gate 3 e /challenge rodam em paralelo sobre o
artigo limpo. O verdict do Gate 3 NÃO é escrito no artigo antes do /challenge —
isso garante três revisores genuinamente independentes (ingest model, Gate 3
ensemble, adversarial challenger). Quarantine block só é escrito na reconciliação.

---

## Gate 1 — Filtro categórico (nunca auto-promote)

Leia o frontmatter do artigo e `programme_health.hard_core` de `outputs/state/kb-state.yaml`.

```
1. arquivo em hard_core[]?              → QUARENTENA [Gate 1 — meta-KB]
2. provenance: emergence?               → QUARENTENA [Gate 1 — emergence]
3. interpretation_confidence: low?      → QUARENTENA [Gate 1 — low confidence]
4. source_quality: low?                 → QUARENTENA [Gate 1 — low quality]
5. confirming_ratio > 0.8 E confirming? → QUARENTENA [Gate 1 — degenerative zone]
```

Se qualquer condição for verdadeira: defina `quarantine: true`,
`quarantine_reason: "[motivo Gate 1]"` no frontmatter e **pare aqui**.
Não escreva quarantine block no corpo do artigo neste estágio.

---

## Gate 2 — Verificação estrutural

```bash
./scripts/structural-promote-gate.sh wiki/concepts/[artigo].md
```

Parse o JSON de output:
- `pass: true` → prossegue para Gate 3 ∥ /challenge
- `pass: false` → QUARENTENA com `quarantine_reason: "Gate 2 — [failures[]]"`

---

## Gate 3 ∥ /challenge — Revisão independente paralela

**Os dois rodam sobre o artigo limpo (sem verdict um do outro). Não escreva
nada no artigo entre Gate 2 e a reconciliação.**

### Gate 3 — Challenge cross-model semântico

```bash
source .venv/bin/activate
python scripts/cross-model-challenge.py \
  --mode article-challenge \
  --article wiki/concepts/[artigo].md
```

Salve o output em `outputs/gates/gate3-[artigo].yaml` — **não** no artigo.

Se o script falhar (API indisponível, timeout, exit code 1): trate como
`claims_weakened: 1` com `quarantine_reason: "Gate 3 — cross-model unavailable"`.

### /challenge — Revisão adversarial

Execute `/challenge [artigo]` lendo **apenas** o artigo limpo.
O /challenge não deve ter acesso ao arquivo `outputs/gates/gate3-[artigo].yaml`.

---

## Reconciliação — Critério hierárquico

Compare os outputs de Gate 3 e /challenge usando esta ordem de precedência:

```
1. /challenge = RISCO_ALTO
   → QUARENTENA (veto absoluto, independente do Gate 3)
   → quarantine_reason: "Gate 3∥challenge — /challenge RISCO_ALTO: [motivo]"

2. /challenge ≠ RISCO_ALTO + Gate 3 claims_invalidated >= 1
   → QUARENTENA
   → quarantine_reason: "Gate 3∥challenge — invalidated: [claim]"

3. /challenge ≠ RISCO_ALTO + Gate 3 claims_weakened >= 1
   → QUARENTENA com lista de correções
   → quarantine_reason: "Gate 3∥challenge — weakened: [claims]"
   → Escreva o quarantine block no final do artigo com a lista das correções
     (agora com os dois inputs consolidados)

4. /challenge ≠ RISCO_ALTO + Gate 3 all survived (claims_weakened: 0, claims_invalidated: 0)
   → elegível para Gate 4
```

**Regra de desempate:** /challenge tem veto power. Se não levantou RISCO_ALTO,
o Gate 3 é determinante. Discordância qualitativa (challenge PRECISA_CORREÇÃO +
Gate 3 all survived) → trate como caso 3 (quarentena com correções).

---

## Gate 4 — Programme health

Leia `programme_health.confirming_ratio.ratio` de `kb-state.yaml`.

```
confirming_ratio < 0.5                          → elegível (prossegue)
confirming_ratio 0.5–0.8 E artigo confirming    → elegível (Gate 3 já validou)
confirming_ratio > 0.8 E artigo confirming      → QUARENTENA [Gate 4 — degenerative zone]
```

---

## Promoção

Se todos os gates passaram (incluindo reconciliação caso 4):

1. No frontmatter do artigo:
   ```yaml
   quarantine: false
   quarantine_promoted: YYYY-MM-DD
   quarantine_criteria_met:
     auto_promote: true
     gates_passed: [1, 2, 3, 4]
     gate3_models: [gpt-5.4, gemini-3.1-pro-preview]
     challenge_verdict: PUBLICÁVEL
   ```
2. Nenhum quarantine block no corpo (nunca foi escrito)
3. Imprima: `✓ [artigo] auto-promoted. Gates: 1✓ 2✓ 3∥challenge✓ 4✓`

---

## Quarentena com motivo

Se qualquer gate falhou:

1. No frontmatter:
   ```yaml
   quarantine: true
   quarantine_created: YYYY-MM-DD
   quarantine_reason: "[Gate N — motivo específico]"
   quarantine_criteria_met:
     gates_passed: [gates que passaram]
     gates_failed: [gates que falharam]
     gate3_run: YYYY-MM-DD
     gate3_models: [modelos usados]
     gate3_claims_challenged: N
     gate3_claims_survived: N
     gate3_claims_weakened: N
     gate3_claims_invalidated: N
   ```
2. Se reconciliação caso 3 (weakened): adicione ao final do artigo:
   ```
   > ⚠️ QUARENTENA: Gate 3∥challenge — [N] claims weakened. Correções necessárias antes de /promote:
   > 1. [claim weakened — descrição da correção]
   > ...
   ```
   Este é o único momento em que o verdict é escrito no artigo.
3. Imprima: `⚠️ [artigo] em quarentena — [Gate N: motivo]. Rode /challenge para satisfazer critério 3 do /promote.`

---

## Após execução — atualiza kb-state.yaml

```yaml
last_updated: YYYY-MM-DD
```

Se auto-promoted:
- Remove artigo de `synthesize.pending_from_ask[]` (se presente)
- Adiciona artigo a `emerge_queue`
- Atualiza `next_actions`: remove entrada `/promote [artigo]` se existir

Se quarentena (weakened): adiciona a `next_actions`:
```yaml
- priority: 1
  action: "/challenge [artigo] (corrigir N claims weakened pelo Gate 3)"
  why: "Gate 3∥challenge: N claims weakened — [lista]. Correções menores, humano decide."
  added_by: auto-promote
```

---

## Post-promote: trigger /emerge (condicional)

Executar após kb-state.yaml atualizado (apenas se auto-promoted; quarentena = NO-OP).

Se `emerge_queue` vazia → NO-OP silencioso. Não imprimir nada.

Se `emerge_queue` >= 1 item:
1. Imprimir: `🔄 post-promote hook: emerge_queue com N itens. Rodando /emerge automaticamente em [top item].`
2. Executar `/emerge` com metadata:
   - `triggered_by: post_promote_hook`
   - `promoted_article: [artigo recém-promovido]`
3. Pares emergidos que envolvam o artigo recém-promovido → marcar `stability: tentative` no report
4. **Guard de aninhamento:** se o contexto atual já tiver `triggered_by` presente (ex: este /auto-promote foi chamado por outro hook) → NÃO disparar /emerge. Imprimir: `⚠️ post-promote hook: contexto aninhado detectado — /emerge suprimido para evitar loop.`

Se `/emerge` falhar (timeout, API down):
- Imprimir: `⚠️ post-promote hook: /emerge falhou — [motivo]. emerge_queue intacta.`
- NÃO silenciar. NÃO remover item da queue.

---

## Quando chamar

O `/ingest` chama `/auto-promote` automaticamente ao final de cada artigo criado.
Pode ser chamado manualmente para artigos já em quarentena (re-avalia os gates).
