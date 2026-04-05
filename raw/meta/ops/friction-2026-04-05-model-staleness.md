---
type: friction
date: 2026-04-05
surface: other
severity: medium
tags: [staleness, configuration, model-names]
---

cross-model-challenge.py estava configurado com gpt-4o (aposentado) e gemini-1.5-pro (removido). Ambos falharam silenciosamente na sessão anterior — o oracle retornou "chave inválida" mas o erro real era modelo inexistente. Detectado manualmente porque o oracle não rodou. Configuração de modelo hardcoded em scripts não tem mecanismo de staleness — vai degradar a cada geração de LLM sem aviso.
