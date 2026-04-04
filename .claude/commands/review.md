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
10. **Adversarial balance:** contar fontes por stance no _registry.md.
    Se ratio confirming:challenging > 5:1, reportar gap adversarial.
11. **Confidence divergence:** listar artigos onde source_quality ≠ interpretation_confidence.
    Esses são candidatos prioritários pra revisão humana.

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
- **Style preservation:** para cada artigo, comparar formulações-chave com as fontes
  raw/ citadas. Se o artigo usa linguagem que NÃO aparece em nenhuma fonte original
  (ex: tweet informal virou prosa acadêmica), flag como potencial semantic convergence.
  Preservar o tom original — diversidade estilística é sinal de saúde, não de inconsistência.
- **Tensões resolvidas → heurísticas:** para cada tensão documentada na passada 1,
  gerar heurística ERL-style com trigger conditions:
  "Quando [condição A], [claim X] se aplica; quando [condição B], [claim Y] se aplica."
  Heurísticas (+7.8%) superam patches pontuais (-1.9%) em transferência cross-task.
- **Multiagent spot-check:** para 2-3 artigos aleatórios, gerar avaliação com 2
  system prompts diferentes ("critical reviewer" vs "supportive reviewer").
  Se divergem substancialmente, flag pra revisão humana.
- **Over-synthesis check:** para cada artigo, verificar se claims na seção
  ## Conteúdo são rastreáveis a fontes raw/. Se encontrar claims interpretativos
  (analogias, "therefore", cross-paper synthesis) fora da seção ## Interpretação,
  mover pra lá. Artigos sem ## Interpretação que contêm interpretação estão em
  violação do template.
- **External spot-check periódico:** a cada /review, regenerar o prompt de
  spot-check (outputs/prompts/spot-check-full-prompt.md) com 3 artigos
  diferentes dos da última vez. Escolher artigos com interpretation_confidence:medium
  ou low prioritariamente. O prompt está pronto pra ser colado em outro modelo.
  Reportar: "🔬 Spot-check prompt atualizado com artigos: [lista]. Cole em outro LLM."
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
- 🎭 Adversarial balance: confirming:challenging ratio + gap alert se > 5:1
- 🔍 Confidence divergence: [artigos onde source_quality ≠ interpretation_confidence]
- 🎨 Style convergence: [artigos cujo estilo divergiu das fontes raw/]
- 👥 Multiagent divergence: [artigos onde reviewer crítico e supportive discordam]
- 📐 Over-synthesis: [artigos com interpretação na seção Conteúdo]
- 🔬 Spot-check prompt: atualizado com artigos [lista] → colar em outro LLM
- ✏️ Reescritas feitas: [lista de artigos + o que mudou]
