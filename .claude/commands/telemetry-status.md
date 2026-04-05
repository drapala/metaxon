# /telemetry-status

Health check visível para o sistema de telemetria automática.
Responde: "está instrumentado? está funcionando?"

## O que verifica

### 1. Infraestrutura

- `scripts/kb-telemetry.sh` existe e é executável
- `raw/meta/ops/events/` existe

### 2. Atividade recente

Lê o arquivo de eventos de hoje: `raw/meta/ops/events/YYYY-MM-DD.jsonl`

Se existir, reporta:
- Total de eventos hoje
- Último evento (timestamp + tipo)
- Breakdown por tipo: `command_started`, `command_finished`, `state_read`, `state_written`, `article_written`, `doc_opened`, `friction_recorded`

Se não existir: avisa que nenhum evento foi registrado hoje.

### 3. Detector de ausência (meta-problema)

Verifica os últimos 7 dias de eventos (todos os arquivos em `raw/meta/ops/events/`).

**Condição de alerta**: em qualquer janela de sessão (definida por `session` ID), há `article_written` mas zero `command_started` ou `command_finished`.

Isso indica que artigos foram escritos mas telemetria não capturou o início/fim dos comandos — provável sinal de que os hooks não estavam ativos naquela sessão.

### 4. Cobertura de hooks

Informa o operador:

```
Hooks necessários (configurar manualmente em settings.local.json):
  PreToolUse  → matcher: Read  → scripts/kb-telemetry.sh
  PostToolUse → matcher: Write → scripts/kb-telemetry.sh
  PostToolUse → matcher: Edit  → scripts/kb-telemetry.sh
  PostToolUse → matcher: Read  → scripts/kb-telemetry.sh
```

Não tenta verificar se os hooks estão configurados (settings.local.json é gitignored e não está disponível em runtime). O operador confirma manualmente.

## Output terminal

```
/telemetry-status — YYYY-MM-DD HH:MM

Infraestrutura:
  ✓ scripts/kb-telemetry.sh — existe e executável
  ✓ raw/meta/ops/events/ — diretório presente

Eventos hoje (YYYY-MM-DD):
  Total: N
  Último: HH:MM — command_finished (surface: ingest)
  Breakdown:
    command_started:   N
    command_finished:  N
    state_read:        N
    state_written:     N
    article_written:   N
    doc_opened:        N
    friction_recorded: N

Detector de ausência (últimos 7 dias):
  ✓ Nenhum sinal de sessão não-instrumentada detectado
  — OU —
  ⚠ ATENÇÃO: sessão XXXXXXXX tinha article_written mas nenhum command_started/finished
    Data: YYYY-MM-DD. Artigo: nome-do-arquivo.md
    Causa provável: hooks não estavam ativos nessa sessão.

Hooks necessários (confirme em settings.local.json):
  PreToolUse  → Read  → kb-telemetry.sh
  PostToolUse → Write → kb-telemetry.sh
  PostToolUse → Edit  → kb-telemetry.sh
  PostToolUse → Read  → kb-telemetry.sh
```

## O que /telemetry-status NÃO faz

- Não modifica nenhum arquivo
- Não corrige configuração de hooks (requer edição manual)
- Não processa eventos (isso é /retro)
- Não escreve em kb-state.yaml
