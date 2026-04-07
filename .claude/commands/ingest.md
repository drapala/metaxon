# /ingest

## Pre-check de contexto

Execute este script bash e leia o resultado:

```bash
SESSION=$(ls -t ~/.claude/projects/-Users-drapala-projects-llm-kb/*.jsonl 2>/dev/null | head -1)
python3 -c "
import json
entries = []
try:
    with open('$SESSION') as f:
        for line in f:
            try:
                obj = json.loads(line)
                u = obj.get('message',{}).get('usage',{})
                if u: entries.append(u)
            except: pass
except: pass
if entries:
    u = entries[-1]
    t = u.get('input_tokens',0)+u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0)
    print(round(t/200000*100,1))
else:
    print('0')
"
```

Se resultado >= 70%:
  Imprima: `⚠️ Contexto em [N]%. /ingest pode causar auto-compact durante processamento. /dream recomendado primeiro.`
  Não processa automaticamente — aguarda confirmação explícita do usuário.

Se resultado < 70%: silêncio — processa normalmente.

---

## Modo especial: Ontologia Formal

Se a fonte é um paper de ontologia formal (BFO, DOLCE, OWL, Relation Ontology,
ou similar), aplique estas regras EM VEZ do resumo padrão:
- NÃO resuma o paper — extraia primitivos aplicáveis à KB
- Para cada categoria ontológica: dê exemplo de como se aplica a conceitos
  já existentes em wiki/concepts/
- Para cada tipo de relação: mostre como substituiria um wikilink plano existente
- Seção obrigatória: "Perguntas que este framework habilita na KB que antes
  não eram formuláveis"

---

**SPRT chain guard** (verifique antes de processar qualquer fonte):
```bash
yq '.ingest_chain.status' outputs/state/kb-state.yaml
```
- Se `closed` E este ingest é `chain_triggered: true`: **PARE.**
  Reporte: `🚫 SPRT CHAIN CLOSED — chain de ingest encerrada. Este paper deve ser revisado manualmente.`
  Adicione à `ingest_queue_priority` com `auto_trigger: false` e aguarde ingest manual.
- Se `closed` E ingest é manual: reset chain (depth: 0, status: open) e prossiga.
- Se `open`: prossiga normalmente.

---

Compare raw/ com wiki/_registry.md. Para cada fonte nova:

1. Leia o conteúdo (para PDFs, extraia texto; para imagens, descreva;
   para transcrições de áudio/vídeo, processe o texto transcrito)
2. Identifique conceitos-chave (max 3 por fonte)
3. Para cada conceito:
   - Se artigo existe em wiki/concepts/: ATUALIZE adicionando informação nova
   - Se não existe E o conceito provavelmente será referenciado de outros artigos:
     CRIE seguindo o template (use as heurísticas de granularidade do CLAUDE.md)
   - Se não justifica artigo próprio: mencione como seção em artigo existente mais próximo
4. Classifique a fonte:
   - type: article | paper | repo | note | dataset
   - quality: primary | secondary | tertiary
   - **stance: confirming | challenging | neutral** — a fonte CONFIRMA, DESAFIA,
     ou é NEUTRA em relação às premissas existentes no wiki?

   **Stance auto-classification (P4):** para fontes em inglês com arquivo em raw/,
   execute o classifier como sugestão inicial (requer venv + .env):
   ```bash
   python3 scripts/stance-classify.py --source <path>
   ```
   - Se `needs_human_review: false` e confidence ≥ 0.70: use a stance sugerida
   - Se `needs_human_review: true` ou confidence < 0.70: classifique manualmente
   - O script detecta apenas `challenging_type: content` (contradição direta por dado)
   - Se você identifica conexão analógica/implicação: `stance: challenging, challenging_type: implication`
   - Stance sugerida pode sempre ser overridden: você tem contexto do wiki que o script não tem

   **Quando stance = challenging: defina obrigatoriamente `challenging_type`:**
   - `content` — paper contradiz claim com dado diferente (detectável automaticamente)
   - `implication` — conexão analógica, prática questionável (requer julgamento humano)

4.5. **Bradford hard gate** (imediato após classificar stance):
   Se stance = `challenging`, execute:
   ```bash
   bash scripts/bradford-gate.sh --stance challenging
   ```
   - Exit 0: prossiga normalmente
   - Exit 1: **PARE.** Não crie artigo, não registre no _registry.md.
     Reporte: `🚫 BRADFORD GATE: quota de fontes challenging excedida. Fonte não ingerida.`
     A fonte pode ser salva em `raw/` para ingestão futura, mas não é processada agora.
     Informe qual ratio atual e quanto falta para a quota reabrir.

5. Verifique: algum artigo existente agora tem overlap >60% com outro? Se sim, sugira merge
6. Processe quaisquer blocos > [!patch] encontrados nos artigos tocados
7. Ao criar/atualizar artigos, atribua no frontmatter:
   - **source_quality: high|medium|low** — baseado em fontes:
     high = 2+ fontes primary concordam, medium = 1 primary ou 2+ secondary,
     low = apenas tertiary
   - **interpretation_confidence: high|medium|low** — auto-avaliação da síntese:
     high = claim factual direto das fontes, medium = síntese moderada,
     low = interpretação novel ou cross-paper insight
   - Quando source_quality e interpretation_confidence divergem, flag com ⚠️
     no report pra revisão humana
8. **Adversarial quota:** após processar, conte fontes no _registry.md por stance.
   Se as últimas 5+ fontes são todas "confirming", reporte:
   "⚠️ Adversarial gap: últimas N fontes são confirming. Considere buscar
   fonte challenging. Rode /curate pra discovery automático."
9. **Ingest threshold** (quando wiki > 40 artigos): exigir que fonte nova
   contribua conceito não coberto OU contradiga claim existente.
   Quando wiki > 80 artigos: exigir sub-índices antes de continuar crescendo.
10. **Verificação adversarial** (antes de finalizar cada artigo):
    Para cada artigo criado ou significativamente atualizado, responda:
    a. **Claim mais fraco:** qual afirmação seria mais fácil de refutar?
    b. **O que o paper NÃO diz:** 2-3 coisas que o resumo poderia sugerir
       mas a fonte não afirma
    c. **Simplificações feitas:** onde o artigo perdeu nuance importante?
    d. **Prior work:** a fonte cita trabalhos anteriores no mesmo terreno?
    Salve como seção `## Verificação adversarial` no artigo wiki gerado.
    Se o claim mais fraco é uma ESPECULAÇÃO não marcada, mova pra
    ## Interpretação antes de publicar.
11. **Cross-reference com artigos de síntese** (após verificação adversarial):
    Antes de finalizar, rode /ask com esta pergunta:
    "O artigo que acabei de ingerir ([TÍTULO]) cobre terreno similar
    a algum artigo de síntese existente na KB? Se sim, quais claims
    dos artigos de síntese esse paper invalida, confirma ou refina?"
    Salve o output em outputs/reports/prior-work-[slug].md e adicione
    uma linha na seção `## Prior work que pode invalidar` de cada
    artigo de síntese afetado. Se o artigo de síntese não tem essa
    seção, adicione-a.
12. **ONTOLOGICAL QUALITY GATE** (antes de salvar o artigo final):

    **CHECK 1 — WIKILINKS TIPADOS**
    Para cada [[wikilink]] no artigo, substitua por relação tipada:
    `[conceito] [TIPO] [[artigo]]`
    Tipos: partOf, contradicts, derivedFrom, validates, supersedes.
    Se o tipo não existe em wiki/meta/ontology.md, proponha em
    outputs/inbox/ontology-proposals.md e use o mais próximo com ⚠️.
    Wikilinks planos são proibidos no artigo final.

    **CHECK 2 — INSTANCE→CLASS ESCALATION**
    Para cada claim numérico/estatístico: de qual paper? qual dataset?
    está apresentado como verdade geral ou dado pontual?
    ❌ "self-enhancement bias causa 16.1% de erro"
    ✅ "self-enhancement bias causa até 16.1% de erro em Qwen2 (CALM benchmark)"

    **CHECK 3 — META-KB SEPARATION**
    Referências a /ask, /ingest, /challenge, /scout, /review, "nosso KB",
    "nossa arquitetura" NUNCA pertencem a ## Conteúdo.
    Mova para ## Aplicação à KB ou ## Interpretação.

    **CHECK 4 — RESUMO CALIBRADO**
    O resumo (_index.md, ~150 chars) não pode ser mais confiante que o corpo.
    Se o corpo tem gaps, especulações, ou caveats significativos, o resumo
    deve refletir.
    ❌ "HippoRAG + Reflexion + MemGPT = adaptive retrieval"
    ✅ "Síntese especulativa: feedback de falha poderia modificar topologia — não implementado"

    Salve no final do artigo:
    ```
    ## Quality Gate
    - [ ] Wikilinks tipados: [N substituições, N tipos novos]
    - [ ] Instance→class: [N claims verificados, N qualificados]
    - [ ] Meta-KB separado: [sim/não — N referências movidas]
    - [ ] Resumo calibrado: [sim/não — alterado/mantido]
    ```

13. **Auto-Promote** (após Quality Gate):
    Invoque `/auto-promote [artigo]` imediatamente.
    O comando executa 4 gates automáticos e decide: promover ou quarentenar com razão específica.
    Não defina `quarantine:` manualmente — o /auto-promote define.
    Se o artigo for quarentenado, adicione ao final:
      `> ⚠️ QUARENTENA: [motivo do gate]. Revisão humana necessária.`

14. **Quarantine cross-check:** Após gerar artigo novo, verifique:
    "Algum artigo em quarentena tem claims que este novo paper confirma?"
    Se sim: atualize `quarantine_criteria_met` do artigo em quarentena
    e notifique via `outputs/inbox/quarantine-update-[artigo].md`.

15. DEPOIS de todos os artigos escritos/atualizados, atualize:
    - _registry.md: path | data | type | quality | stance | conceitos | status
    - _index.md: 1 ponteiro por artigo (~150 chars: título + contexto mínimo)
    Ordem importa: artigo primeiro → índice depois. Nunca o contrário.

15.5. **Stub-wiki queue** — para cada fonte registrada com status `stub-wiki`:

    Compute `completion_priority` para o(s) conceito(s) da fonte:
    ```bash
    python3 - <<'EOF'
    import re, sys
    from pathlib import Path
    from collections import Counter

    concept_slugs = sys.argv[1:]  # slugs dos concepts da fonte stub-wiki
    wiki_dir = Path("wiki/concepts")
    in_degree = Counter()
    reads_map = {}
    for f in wiki_dir.glob("*.md"):
        if f.stem.startswith("_"): continue
        text = f.read_text()
        for link in re.findall(r'\[\[([^\]|#]+)', text):
            in_degree[link.strip().lower().replace(' ', '-')] += 1
        m = re.search(r'^reads:\s*(\d+)', text, re.MULTILINE)
        reads_map[f.stem] = int(m.group(1)) if m else 0

    for slug in concept_slugs:
        deg = in_degree.get(slug, 0)
        reads = reads_map.get(slug, 0)
        print(f"{slug}  in_degree={deg}  reads={reads}  priority={deg*2+reads}")
    EOF
    ```
    Passe os slugs dos concepts como argv (ex: `python3 - procurement-renegotiation incentive-theory-procurement`).

    Adicione cada conceito a `stub_completion_queue` em `outputs/state/kb-state.yaml`:
    ```yaml
    stub_completion_queue:
      updated: YYYY-MM-DD
      entries:
        - stem: concept-slug
          source: raw/papers/fonte.md   # fonte raw/ que gerou o stub
          in_degree: N
          reads: N
          completion_priority: N
          option_b_eligible: true|false  # false se in_degree >= 5 ou sem fontes raw/
          ineligibility_reason: null | "in_degree=N >= 5"
    ```
    Se o conceito já está na fila: atualize `in_degree`, `reads`, `completion_priority`.
    Não duplicar entradas — use o stem como chave.

16. **Log de occurrent:** Salve log da sessão em
    `outputs/logs/sessions/YYYY-MM-DD/ingest-[source-slug]-HH-MM.md`
    segundo schema em `wiki/meta/process-log.md`.

Reporte: X fontes processadas, Y artigos criados, Z atualizados, W patches resolvidos.
Se encontrar fontes com problemas (vazio, ilegível, duplicata exata): reporte sem processar.

## Após processar (antes do log de occurrent)

**SPRT chain update** (se este ingest foi `chain_triggered: true`):
```yaml
ingest_chain:
  depth: [depth + 1]
  status: closed          # SEMPRE closed após auto-ingest de INVALIDA
  last_challenge: YYYY-MM-DD
```
Se este ingest foi manual (chain_triggered: false ou ausente):
```yaml
ingest_chain:
  depth: 0
  status: open
  origin_article: null
```

Atualize `outputs/state/kb-state.yaml`:
1. `ingest_count_since_last_lint += 1`
2. `sessions_since_last_dream += 1`
3. `last_updated` com data atual
4. Atualize `readiness_signal`:
   - Recalcule `stance_status` com base no total atual de fontes por stance no _registry.md
   - Se stance challenging < 20%: `can_ingest: true`, `warning: "stance baixo — busque fonte challenging"`
   - Se stance challenging 20-25%: `can_ingest: true`, `warning: null` (ou "marginal" se próximo de 25%)
   - Se stance challenging > 25%: `can_ingest: true`, `stance_status: "saudável"`
   - Atualize `next_ingest_candidates` com os itens do topo de `ingest_queue_priority` e `ingest_queue_autoresearch`
5. Atualize `next_actions`:
   - Se artigo entrou em quarentena por Gate 1/2: adicione `/review [artigo]` (humano necessário)
   - Se artigo entrou em quarentena por Gate 3 (weakened): adicione `/challenge [artigo]` para humano decidir se correção é menor
   - Se artigo foi auto-promoted: nenhuma entrada de promoção necessária
   - Se `ingest_count_since_last_lint >= 5`: adicione `/lint-epistemic`
   - Remova da fila `ingest_queue_priority` o item que acabou de ser ingerido
