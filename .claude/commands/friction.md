# /friction

Registra um evento de atrito operacional na KB. Rápido — deve levar menos de 2 minutos.

## Uso

```
/friction
```

O agente faz 3 perguntas e gera o arquivo.

## Processo

1. **Pergunta 1 — O que aconteceu?**
   Descreva o evento em 1-3 linhas. O que estava fazendo, o que não funcionou como esperado.
   Foco no fato observado, não na causa nem na solução.

2. **Pergunta 2 — Tipo:**
   - `friction` — exigiu memória, dúvida ou retrabalho
   - `workaround` — criou atalho fora do protocolo
   - `wish` — "isso devia existir / ser automático"

3. **Pergunta 3 — Surface:**
   Onde no workflow ocorreu?
   `ingest | ask | promote | emerge | quarantine | kb-state | review | challenge | other`

4. **Gera arquivo** em `raw/meta/ops/friction-YYYY-MM-DD-HH-MM.md`:

```yaml
---
type: friction | workaround | wish
date: YYYY-MM-DD
surface: [surface]
severity: low | medium | high
tags: []
---

[evento em 2-3 linhas. O que aconteceu, não o que devia acontecer.]
```

Severidade default: `medium`. Só eleva para `high` se o evento gerou erro real, retrabalho significativo ou estado inconsistente.

Tags sugeridas (não exaustivas):
`memory-load` `state-ambiguity` `sequence-unclear` `naming-confusion` `next-action-missing` `protocol-gap` `too-many-options` `invisible-state` `manual-overhead`

**Emissão algedônica — quarantine_stale:**
Se o evento registrado tem tag `next-action-missing` E surface `quarantine`:
- Pergunta (ou infere do contexto): qual artigo em quarentena gerou o atrito?
- Verifica se o artigo satisfaz critérios de promoção E está em quarentena > 24h
- Se sim E não existe evento `type: quarantine_stale, resolved: false` para o artigo:
  - Emite DisturbanceEvent via `.claude/commands/algedonic.md`
    - `type: quarantine_stale`, `origin: friction`, `evidence: [artigo-slug]`

## O que NÃO fazer

- Não escrever a causa — só o sintoma observado
- Não propor solução — isso é `/propose`
- Não filtrar eventos que parecem "óbvios demais" — o padrão só aparece com volume
- Não consolidar vários eventos em um arquivo

## Quando rodar

- Sempre que pensar "caralho, não sabia que vinha depois"
- Sempre que abrir PROTOCOL.md ou ONBOARDING.md no meio de uma sessão
- Sempre que editar kb-state.yaml manualmente sem ter certeza
- Sempre que criar um atalho fora do protocolo formal
- Sempre que pensar "isso devia ser automático"

O threshold é baixo. A evidência se consolida no `/retro`, não aqui.
