# /review

Duas passadas sobre o wiki:

## Passada 1 — Diagnóstico (reportar)
1. Artigos sem fontes citadas em raw/
2. Wikilinks quebrados (referência a artigo que não existe)
3. Fontes em raw/ ausentes do _registry.md
4. Artigos com >1500 palavras (candidatos a split)
5. Artigos com overlap alto (candidatos a merge)
6. Patches pendentes (blocos > [!patch] não resolvidos)
7. Top 3 conceitos mencionados em múltiplos artigos que merecem artigo próprio
8. Backlinks assimétricos: se A linka B, B deve linkar A (shared source = bidirectional link)
9. **Tensões:** para artigos que compartilham 2+ fontes raw/, comparar claims-chave.
   Se detectar contradição:
   a. Verificar contra raw/ qual claim é suportado (Layer 3 obrigatório — Reflexion
      mostra que self-reflection sem feedback fundamentado degrada a 52%)
   b. Se apenas um suportado: gerar > [!patch] com correção + fonte
   c. Se ambos suportados: documentar como "Tensão Conhecida" no artigo mais geral
      com critérios dinâmicos (CARMO-style) explicando quando cada claim se aplica
   d. NUNCA resolver forçando consistência artificial — tensões reais são knowledge
   e. Cuidado com self-enhancement bias (CALM: até 16.1% error) — o LLM que escreveu
      os artigos tende a preferir sua própria formulação. Sempre verificar contra raw/

## Passada 2 — Reescrita ativa (executar)
Para cada artigo tocado:
- Converter afirmações vagas em precisas (datas, números, nomes)
- Deduplicar informação repetida entre artigos
- Remover contradições internas (se encontrar, preferir raw/ como fonte de verdade)
- Podar conteúdo derivável (stats, contagens que podem ser recalculados)
- **Heurística de compressão:** verificar que cada artigo tem resumo de 2-3 frases
  que funcione como "nó intermediário" de retrieval. Se o resumo é fraco, genérico,
  ou não captura o insight principal do artigo, reescrever. Bom resumo = Layer 1
  (_index.md) → Layer 2 (resumo) transition eficiente.
- **Tensões resolvidas → heurísticas:** para cada tensão documentada na passada 1,
  gerar heurística ERL-style com trigger conditions:
  "Quando [condição A], [claim X] se aplica; quando [condição B], [claim Y] se aplica."
  Heurísticas (+7.8%) superam patches pontuais (-1.9%) em transferência cross-task.
- Atualizar _index.md se títulos/contexto mudaram

## Formato de report (terminal)
- ⚠️ Sem fontes: [lista]
- 🔗 Links quebrados: [lista]
- 📥 Não processadas: [lista]
- 📏 Artigos longos: [lista]
- 🔀 Overlap alto: [lista]
- 🩹 Patches pendentes: [lista]
- 💡 Artigos sugeridos: [lista]
- ↔️ Backlinks assimétricos: [lista]
- ⚡ Tensões detectadas: [lista com artigos + claims + resolução proposta]
- ✏️ Reescritas feitas: [lista de artigos + o que mudou]
