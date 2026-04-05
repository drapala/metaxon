# /retro

Consolida telemetria automática + friction events manuais em padrões observáveis.
Só observa e classifica — não propõe.

## Fontes de evidência

Duas fontes, separadas:
- **Telemetria automática**: `raw/meta/ops/events/YYYY-MM-DD.jsonl` — comportamento observado
- **Friction manual**: `raw/meta/ops/friction-*.md` — dor confirmada pelo operador

Regra: telemetria gera *suspeita*. Friction manual gera *confirmação*.
Nunca elevar suspeita a fato sem friction correspondente.

## Quando rodar

- Quando acumular 10+ friction events manuais, OU 5+ dias de telemetria
- Mensalmente como manutenção
- Antes de rodar `/propose` pela primeira vez

## Processo

### Passo 0 — Lê telemetria automática

Lê arquivos `raw/meta/ops/events/*.jsonl` não processados ainda.

Roda os **5 detectores de suspeita** sobre os eventos:

#### Detector 1: Recall burden
**Condição**: `doc_opened` com `signal: recall_burden_proxy` aparece 2+ vezes em janela de 30 minutos.
**Suspeita**: operador precisou consultar documentação de processo no meio de uma tarefa.
**Sinal positivo necessário para confirmar**: friction manual do tipo `memory-load` ou `next-action-missing` na mesma surface.

#### Detector 2: Sequencing ambiguity
**Condição**: 3+ `command_finished` em surfaces diferentes em janela de 20 minutos sem progressão material (nenhum `article_written` ou `state_written` entre eles).
**Suspeita**: operador não sabia o próximo passo e tentou múltiplos caminhos.
**Sinal positivo necessário**: friction manual do tipo `sequence-unclear` ou `too-many-options`.

#### Detector 3: Manual state burden
**Condição**: `state_written` em `kb-state` que NÃO foi precedido por `command_finished` em janela de 5 minutos.
**Suspeita**: edição manual de estado fora do protocolo normal.
**Sinal positivo necessário**: friction do tipo `manual-overhead` ou `protocol-gap`.

#### Detector 4: Stalled flow
**Condição**: `command_finished` para `surface: promote` ou `surface: challenge` seguido de nenhum `command_finished` por > 48h, mas kb-state mostra itens em quarentena.
**Suspeita**: quarentena estagnada — itens travados sem progressão.
**Sinal positivo necessário**: friction do tipo `state-ambiguity` ou wish "isso devia lembrar automaticamente".

#### Detector 5: Excessive surface hopping
**Condição**: 5+ surfaces distintas tocadas em janela de 60 minutos com < 3 `article_written` ou `command_finished` de conclusão.
**Suspeita**: muitos arquivos tocados para completar uma tarefa simples.
**Sinal positivo necessário**: friction do tipo `manual-overhead` ou `protocol-gap`.

**Output do Passo 0**: lista de suspeitas com grau de evidência (eventos que as sustentam).
Salva em `raw/meta/ops/derived/YYYY-MM-DD-suspected.md`.

### Passo 1 — Lê friction events manuais

Lê todos os arquivos em `raw/meta/ops/friction-*.md` que ainda não foram incluídos em um retro anterior.
(Verifica `wiki/meta/friction-log.md` para identificar quais já foram consolidados.)

Circuit breaker: se houver > 50 eventos não consolidados, processa em lotes de 20 e reporta parcialmente.

### Passo 2 — Classifica cada evento

Para cada evento, identifica:
- **Surface**: onde no workflow ocorreu
- **Tipo de problema** (escolha exatamente um):
  - `estado-invisível` — o sistema não mostrava em que estado estava
  - `próxima-ação-ausente` — não estava claro o que fazer depois
  - `sequencing` — a ordem correta dependia de memória, não de estrutura
  - `nomenclatura` — nome do comando/arquivo/conceito era ambíguo
  - `excesso-de-opções` — muitas possibilidades sem critério visível
  - `overhead-manual` — passo que devia ser automático ou assistido

**Não infira causa.** Se o evento não encaixa em nenhuma categoria, classifica como `não-classificado` e continua.

### Passo 2b — Cruza suspeitas com confirmações

Para cada suspeita do Passo 0, verifica se existe friction manual correspondente:
- Mesma surface + tag compatível → **confirmado** (entra no log como padrão)
- Suspeita sem friction correspondente → **suspeita não-confirmada** (entra no log como proxy, não como padrão)
- Friction sem suspeita telimétrica → **confirmado por declaração** (entra no log normalmente)

Isso garante que telemetria permanece proxy, não verdade.

### Passo 3 — Identifica padrões

Agrupa eventos por `(surface, tipo-de-problema)`. Um padrão existe quando:
- ≥2 eventos do mesmo tipo na mesma surface, OU
- ≥3 eventos do mesmo tipo em surfaces diferentes (problema sistêmico)

Para cada padrão, verifica se há princípio externo em `raw/meta/ux/` que sustenta a classificação.
Se não houver fonte em `raw/meta/ux/` ainda, registra como "sem sustentação externa — candidato a ingestão".

**Não busca solução.** Só verifica se o padrão está sustentado por evidência externa.

### Passo 4 — Atualiza `wiki/meta/friction-log.md`

Atualiza o arquivo com:

```markdown
# Friction Log

Última consolidação: YYYY-MM-DD
Eventos processados: N (total acumulado: N)

## Padrões ativos

### [surface] × [tipo-de-problema]
- Eventos: N (datas: YYYY-MM-DD, ...)
- Descrição do padrão: [2-3 linhas do que os eventos têm em comum]
- Sustentação externa: [artigo em raw/meta/ux/ ou "pendente — ingerir [tema]"]
- Status: ativo | em-teste | resolvido

...

## Eventos não-classificados
- [lista de eventos que não encaixaram]

## Candidatos a ingestão (UX)
- [temas sem cobertura em raw/meta/ux/ mas com padrão identificado]
```

### Passo 5 — Relatório terminal

```
/retro completo — YYYY-MM-DD

Eventos processados: N
Padrões identificados: N
  - N com sustentação externa
  - N sem sustentação (candidatos a ingestão)
Eventos não-classificados: N

Próximos passos:
  - Se padrão com sustentação: /propose [padrão]
  - Se candidato a ingestão: ingira raw/meta/ux/ sobre [tema]
  - Se muitos não-classificados: revise schema de tags em /friction
```

## O que /retro NÃO faz

- Não propõe mudanças de workflow
- Não modifica nenhum comando
- Não avalia se a mudança seria boa ou ruim
- Não lê kb-state.yaml como base primária (pode ler como contexto auxiliar se relevante)

## kb-state.yaml

### Escreve (ao final)
```yaml
slow_cycle:
  retro:
    last_run: YYYY-MM-DD
    events_processed: N
    patterns_active: N
    patterns_with_evidence: N
```
