# /ingest

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
12. DEPOIS de todos os artigos escritos/atualizados, atualize:
    - _registry.md: path | data | type | quality | stance | conceitos | status
    - _index.md: 1 ponteiro por artigo (~150 chars: título + contexto mínimo)
    Ordem importa: artigo primeiro → índice depois. Nunca o contrário.

Reporte: X fontes processadas, Y artigos criados, Z atualizados, W patches resolvidos.
Se encontrar fontes com problemas (vazio, ilegível, duplicata exata): reporte sem processar.
