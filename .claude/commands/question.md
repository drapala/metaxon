# /question [tópico]

Antes de rodar /ask, sugere qual tipo de pergunta geraria o insight mais fértil.

## Processo

1. **Leia wiki/_index.md** e identifique artigos relevantes para [tópico]

2. **Diagnostique o estado do conhecimento** sobre o tópico:
   - Quantos artigos cobrem? (cobertura)
   - Há tensões documentadas? (contradições)
   - Qual a interpretation_confidence média? (certeza)
   - Há fontes challenging sobre o tema? (adversarial coverage)

3. **Selecione tipo de pergunta** baseado no diagnóstico:

   | Estado | Tipo recomendado | Por quê |
   |--------|-----------------|---------|
   | 0 artigos | AUSÊNCIA | Nada na KB — identifique o que falta |
   | 1 artigo, confidence:high | ESCALA ou FRONTEIRA | Conhecimento existe, explore limites |
   | 1 artigo, confidence:low | EMPÍRICA | Claim sem evidência, teste-o |
   | 2+ artigos concordam | MECANISMO OCULTO | Consenso existe, pergunte por quê |
   | 2+ artigos discordam | CONTRADIÇÃO | Tensão existe, resolva-a |
   | Só fontes confirming | TRANSFERÊNCIA | Aplique conceito a domínio diferente |
   | Só fontes challenging | ESCALA | Busque onde o desafio quebra |

4. **Gere 3 perguntas candidatas** usando o tipo selecionado:
   - Uma pergunta direta (o que parece óbvio)
   - Uma pergunta oblíqua (reframe: "e se o oposto fosse verdade?")
   - Uma pergunta de ausência ("o que ninguém perguntou?")

5. **Apresente ao usuário** com justificativa:
   ```
   TÓPICO: [tópico]
   ESTADO: [diagnóstico em 1 linha]
   TIPO RECOMENDADO: [tipo + justificativa]

   PERGUNTA DIRETA: "..."
   PERGUNTA OBLÍQUA: "..."
   PERGUNTA DE AUSÊNCIA: "..."

   Qual quer rodar como /ask?
   ```

## Perguntas proibidas (não sugerir)

- "Is X better than Y?" → binary, mata nuance
- "What is X?" → definitional, sem insight
- "Summarize X" → compressão, não descoberta
- "Do you agree with X?" → self-enhancement bias
