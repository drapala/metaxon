# /promote [artigo]

Verifica se artigo em quarentena pode ser promovido.

**Critérios baseados em independência de revisor, não em tempo.**
Pipeline autônomo não tem cognitive bias temporal — o que importa é que
revisores distintos validaram independentemente.

## Passo 1 — Lê frontmatter
Se `quarantine: false` → "Artigo não está em quarentena."

## Passo 2 — Critério 1 (revisão independente)

Verifica se Gate 3 rodou com ensemble de modelos independentes:
- `quarantine_criteria_met.gate3_run` está preenchido?
- `quarantine_criteria_met.gate3_models` tem 2+ modelos?

Se não → "Critério 1 não satisfeito. Rode /auto-promote para executar Gate 3."

> **Nota:** Este critério substitui o cooldown de 24h original.
> Justificativa: revisores LLM não têm confirmation bias temporal.
> Independência é garantida por ensemble de modelos distintos, não por tempo.

## Passo 3 — Critério 2 (adversarial challenge)

Busca `outputs/logs/sessions/**/challenge-[artigo]-*.md` com
`verdict: PUBLICÁVEL` ou `verdict: PRECISA_CORREÇÃO` (não RISCO_ALTO).

Se não encontra → "Critério 2 não satisfeito. Rode /challenge [artigo]."

Se encontra com `verdict: RISCO_ALTO` → "Critério 2 BLOQUEADO.
/challenge levantou RISCO_ALTO. Corrija os claims antes de tentar novamente."

> **Nota:** Este critério substitui o "review em sessão diferente" original.
> /challenge é o adversarial reviewer independente. Se não levantou RISCO_ALTO,
> a independência de revisão está satisfeita.

## Passo 4 — Critério 3 (profundidade epistêmica — um dos três)

Busca evidência de:
- a) `challenge-[artigo]-*.md` com `prior_work_found >= 3` (web search realizado)
- b) `outputs/reports/scout-*.md` sem `subsumes: true` para este artigo
- c) Seção `## Predição falsificável` no artigo com nível Pearl L2+

Se nenhum encontrado → "Critério 3 não satisfeito. Rode /challenge com web search,
/scout, ou adicione predição falsificável."

## Passo 5 — Promoção

Se TODOS satisfeitos:
1. `quarantine: true` → `quarantine: false`
2. Adiciona `quarantine_promoted: [data]`
3. Atualiza `quarantine_criteria_met`:
   ```yaml
   quarantine_criteria_met:
     auto_promote: false
     gates_passed: [1, 2, 3]
     gate3_run: [data do gate3]
     gate3_models: [modelos]
     challenge_verdict: PUBLICÁVEL
     promoted_by: manual_promote
   ```
4. Remove bloco `> ⚠️ QUARENTENA` ou `> ✅ CORREÇÕES APLICADAS` do final do artigo
5. Log em `outputs/logs/sessions/YYYY-MM-DD/promote-[artigo]-HH-MM.md`
6. "Artigo promovido. Pode ser linkado por outros artigos."

## Após promoção bem-sucedida

Atualize `outputs/state/kb-state.yaml`:
1. Adicione artigo promovido a `emerge_queue`
2. Atualize `last_updated` com data atual
3. Atualize `next_actions`:
   - Remova qualquer entrada que mencionava `/promote [este artigo]`
   - Se houver outros artigos em quarentena prontos: adicione `/promote [próximo]`

## Post-promote: trigger /emerge (condicional)

Executar após kb-state.yaml atualizado e promote log salvo.

Se `emerge_queue` vazia → NO-OP silencioso. Não imprimir nada.

Se `emerge_queue` >= 1 item:
1. Imprimir: `🔄 post-promote hook: emerge_queue com N itens. Rodando /emerge automaticamente em [top item].`
2. Executar `/emerge` com metadata:
   - `triggered_by: post_promote_hook`
   - `promoted_article: [artigo recém-promovido]`
3. Pares emergidos que envolvam o artigo recém-promovido → marcar `stability: tentative` no report
4. **Guard de aninhamento:** se o contexto atual já tiver `triggered_by` presente (ex: este /promote foi chamado por /auto-promote ou outro hook) → NÃO disparar /emerge. Imprimir: `⚠️ post-promote hook: contexto aninhado detectado — /emerge suprimido para evitar loop.`

Se `/emerge` falhar (timeout, API down):
- Imprimir: `⚠️ post-promote hook: /emerge falhou — [motivo]. emerge_queue intacta.`
- NÃO silenciar. NÃO remover item da queue.
