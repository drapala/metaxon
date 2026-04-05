# /document-session

## Propósito
Gerar documentação estruturada de uma sessão de trabalho
para preservar contexto, decisões, e insights para
sessões futuras. Substitui o processo manual de pedir
"documente para a posterioridade" repetidamente.

## Quando rodar
- Quando contexto estiver em 50%+ (ver /context)
- Ao final de qualquer sessão com >= 3 fases de trabalho
- Antes de /dream (consolida antes de compactar)
- Quando kb-state.yaml indicar sessions_since_last_dream >= 3

## O que captura

### 1. Lê o estado atual
- outputs/state/kb-state.yaml
- outputs/logs/sessions/ (últimas sessões)
- Histórico da conversa atual (o que foi feito nesta sessão)
- Qualquer report em outputs/reports/ gerado nesta sessão

### 2. Identifica automaticamente o número da parte
```bash
ls outputs/ | grep "session-documentation-part" | sort -V | tail -1
```
Se não existe nenhum: parte 1
Se existe part8: parte 9

### 3. Gera o documento

Salve em `outputs/session-documentation-part[N].md`
com esta estrutura:

---

# Sessão de Construção do llm-kb — Documentação Parte [N]
**Data:** [data atual]
**Contexto:** [resumo em 1 linha do que foi feito]

---

## Resumo das Partes Anteriores
*Ver documentações anteriores para detalhes completos.*
[Lista de 1 linha por parte anterior, do que foi feito]

---

## Fases desta Sessão

Para cada fase identificada no histórico:

### Fase [N] — [Nome descritivo]

**O que foi feito:**
[Descrição concisa — o que aconteceu]

**Resultado:**
[Output concreto — artigo criado, comando implementado,
insight gerado, predição formulada]

**Insight chave (se houver):**
[O que não era óbvio antes desta fase]

**Implicações (se houver):**
[O que isso muda em outras partes do sistema]

---

## Estado Final desta Sessão

### Métricas
| Métrica | Valor |
[lê de kb-state.yaml e frontmatters dos artigos]

### Insights gerados
[Lista numerada dos insights não-óbvios desta sessão]

### Pendências prioritárias
| Prioridade | Item |
[O que ficou pendente, ordenado por urgência]

---

## A Frase que Resume esta Sessão
[Uma frase que captura o arco da sessão —
o que mudou de antes para depois]

---

*Documentado em [data]. [N] fases. [X] horas estimadas.*

---

## Regras de geração

### O que INCLUIR
- Decisões tomadas e por que (não só o que foi feito)
- Insights que não eram óbvios antes da sessão
- Predições falsificáveis geradas
- Conexões cross-domain descobertas
- O que foi descartado e por que
- Erros encontrados e como foram corrigidos

### O que NÃO incluir
- Conteúdo verbatim de /ask responses (resumir em 2-3 linhas)
- Código completo (referenciar o arquivo, não reproduzir)
- Debates que não chegaram a conclusão
- Listas de tarefas que já existem no kb-state.yaml

### Tom
- Factual, não narrativo
- Terceira pessoa para a KB, primeira para decisões suas
- Sem "Documentado com sucesso" ou frases de encerramento genéricas
- A frase final deve ser genuinamente descritiva, não motivacional

## Após gerar

Atualiza kb-state.yaml:
```yaml
sessions_since_last_dream: +1
last_session_documented: YYYY-MM-DD
```

Se o documento ficou > 200 linhas:
Avise: "Sessão densa — considere /dream antes de continuar"

## O que NÃO faz
- Não commita nada
- Não modifica artigos wiki
- Não roda outros commands automaticamente
- Apenas documenta e atualiza kb-state
