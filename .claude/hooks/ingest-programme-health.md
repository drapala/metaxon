# Ingest — Programme Health Classifier

## Quando ativa

No final de TODA sessão /ingest, após:
- Wiki article criado
- _index.md e _registry.md atualizados
- kb-state.yaml atualizado com `last_updated`

**Antes** de finalizar o /ingest, execute este classificador.

## Classificador LLM (passo final obrigatório)

Faça a seguinte pergunta sobre o artigo recém-criado:

> "Este artigo gera alguma **predição testável** que não existia antes na KB?
> Uma predição testável: claim sobre o mundo que pode ser confirmado ou refutado por experimento, benchmark, ou observação futura — independente de confirmar o que a KB já acredita."

### Exemplos para calibração

**novel_prediction (SIM):**
- `autoresearch-reliability-triad`: "autoresearch KB-internal tem taxa confirmação > 80%"
- `procurement-variety-gap`: "Lei 14.133 aumenta V(R) mas preserva error floor"
- `evaluation-order-independence`: "protocolo raw/-first detecta mais conflitos wiki-vs-raw"

**confirming (NÃO):**
- `autonomous-kb-failure-modes`: confirma convergence/cascade que já eram hipóteses da KB
- `curse-of-knowledge-llm-judge`: confirma reference-anchoring como mecanismo do Layer 3 problem
- `multi-agent-memory-consistency`: neutra, descreve gap sem predição nova para esta KB

### Classificação

Após responder a pergunta, classifique o artigo como:
- `novel_prediction` — faz predição testável nova
- `confirming` — confirma, refina, ou é neutro em relação a claims existentes

## Atualiza kb-state.yaml

```yaml
programme_health:
  confirming_ratio:
    window: +1                  # incrementa sempre
    confirming: +1              # só se confirming
    novel_prediction: +1        # só se novel_prediction
    ratio: confirming / window  # recalcula
    last_updated: YYYY-MM-DD
  last_novel_prediction:        # só atualiza se novel_prediction
    article: wiki/concepts/[artigo].md
    prediction: "[texto da predição identificada]"
    date: YYYY-MM-DD
```

## Quando o hook shell dispara

Se após o Write do wiki article o `check-programme-health.sh` retornar warning:
- Ratio > 0.80 com window ≥ 10 = KB degenerativa
- Neste caso: classifique explicitamente na resposta e informe ao usuário
- Se o artigo é confirming: considere se /challenge seria mais valioso antes de ingerir
- Se o artigo é novel_prediction: prossiga normalmente (ingest progressivo)

## Nota: janela deslizante não implementada

`window` é acumulativo, não janela deslizante real. Com N > 30 ingest, a janela
distorce (eventos antigos pesam igual a recentes). Fix futuro: usar apenas os
últimos 10 registros explícitos. Por ora, resetar `window` e `confirming`
manualmente a cada 20 ingest é suficiente.
