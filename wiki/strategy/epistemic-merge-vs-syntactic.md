---
title: "Merge epistêmico ≠ merge sintático"
created: 2026-04-05
updated: 2026-04-05
tags: [strategy, multi-agent, kb, merge, contradiction-detection, git-worktrees]
source_quality: low
interpretation_confidence: low
provenance: conjecture
epistemic_status: hypothesis
testable_prediction: "dois agentes ingerindo papers contraditórios sobre o mesmo claim chegam a beliefs divergentes que git merge não detecta"
conjecture_trigger:
  session: outputs/logs/sessions/2026-04-05/foresight-23-00.md
  context: "Sessão de captura de hipóteses estratégicas — Fork-Join de instâncias Prometheus em git worktrees"
conjectured_on: 2026-04-05
lifecycle_state: active
---

## Hipótese

Fork-Join de instâncias KB em git worktrees requer contradiction detection no plano epistêmico, não só diff de arquivos. Dois agentes ingerindo papers contraditórios sobre o mesmo claim podem produzir artigos wiki textualmente compatíveis (sem conflito git) mas epistemicamente divergentes. Git merge não detecta isso.

## Premissas

- Dois agentes com acesso a fontes diferentes sobre o mesmo domínio vão construir representações divergentes do mesmo conceito
- A divergência pode ser expressível em texto que não gera conflito git (diferentes seções, diferentes formulações do mesmo claim com polaridades opostas)
- Contradiction detection requer operar em espaço semântico, não textual
- O mecanismo de belief revision da KB (raw/ como âncora + /challenge) não foi projetado para reconciliar dois branches epistêmicos, apenas para avaliar um artigo individualmente

## Mecanismo proposto

Num sistema de git worktrees Fork-Join:
1. Agente A ingere paper X (claim: "método Y funciona em domínio D")
2. Agente B ingere paper Z (claim: "método Y falha em domínio D com condição C")
3. Ambos produzem artigos wiki coerentes com suas fontes
4. Git merge aceita ambos os textos sem conflito (seções diferentes, sem sobreposição literal)
5. O wiki resultante contém dois claims contraditórios sobre Y em D — invisível para git, visível para um leitor com contexto

O problema não é de diff — é de consistency checking em grafo de claims. Dois nós no wiki podem cada um ser internamente coerentes com suas fontes e juntos serem inconsistentes.

Isso é análogo ao problema de atualização de crenças em sistemas distribuídos: as transações são localmente consistentes, mas sem coordenação global, o estado global pode ser inconsistente.

## Consequências arquiteturais

- Merge de KB requer um passo de "belief reconciliation" pós-git, antes de tornar o branch canônico
- Belief reconciliation precisa: (a) identificar claims sobre os mesmos objetos; (b) detectar polaridade oposta; (c) invocar /challenge cruzado entre as fontes divergentes
- O merge semântico pode ser implementado como: embeddings dos claims → clustering por objeto → polaridade check → flag para /challenge
- O namespace raw/ como fonte imutável é crucial aqui: as fontes permanecem divergentes, o wiki deve DOCUMENTAR a contradição, não silenciá-la
- Implicação para multi-agent KB: o /challenge precisa de um modo "cross-branch" que compare dois artigos sobre o mesmo claim, não só um artigo vs evidência nova

## Predição testável

Experimento: dois agentes em worktrees separados. Agente A ingere paper que afirma "X → Y em contexto C". Agente B ingere paper que afirma "X → ¬Y em contexto C'". Ambos produzem artigos sobre o mesmo conceito. Git merge: sem conflito. Embedding similarity check entre os claims centrais: divergência detectável. Se o embedding check não detectar divergência onde um humano veria contradição, a hipótese de contradiction detection via embeddings está errada.

## Conexões tentativas

- [[autonomous-kb-failure-modes]] — este failure mode é FM1 (semantic convergence) invertido: em vez de convergência por echo chamber, divergência por fork sem reconciliação
- [[complementary-learning-systems]] — CLS distingue consolidação lenta (neocórtex) de aprendizado rápido (hipocampo); analogia: branch fast-ingest (hipocampo) precisa de reconciliação com trunk lento (neocórtex) — sem replay, os dois divergem
- [[multi-agent-memory-consistency]] — Yu et al. 2026 define consistency como problema não resolvido; este é o caso concreto de inconsistência cross-agent em KB baseada em git
- [[falsificationism-demarcation]] — o merge semântico como operação de demarcação: claims inconsistentes precisam de falsificador, não de conciliação ad hoc

## Histórico

- 2026-04-05 — hipótese capturada em sessão de foresight (devaneio sobre Fork-Join de instâncias Prometheus)
