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

16. **Log de occurrent:** Salve log da sessão em
    `outputs/logs/sessions/YYYY-MM-DD/ingest-[source-slug]-HH-MM.md`
    segundo schema em `wiki/meta/process-log.md`.

Reporte: X fontes processadas, Y artigos criados, Z atualizados, W patches resolvidos.
Se encontrar fontes com problemas (vazio, ilegível, duplicata exata): reporte sem processar.

## Após processar (antes do log de occurrent)

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
