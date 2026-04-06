# /roadmap

Executa o item de maior prioridade não-bloqueado do roadmap de autonomia.

## Processo

1. **Leia o roadmap**
   ```
   outputs/roadmap.md
   ```

2. **Identifique o próximo item executável**
   - Status: `pending`
   - `Bloqueado por:` nada OU todos os bloqueadores com status `done`
   - Se múltiplos elegíveis: menor complexidade primeiro (baixa > média > alta)

3. **Anuncie o item selecionado**
   ```
   Executando: [P1/P2/P3/P4] — [título]
   Justificativa: [por que este e não outro]
   ```

4. **Execute**
   Cada item tem um "Arquivo alvo" e "Critério de done" no roadmap.
   Implemente o critério de done conforme descrito.

5. **Atualize o roadmap**
   - Mude `Status: pending` → `Status: done`
   - Adicione linha no `## Log de execuções` com data e resultado
   - Se o item desbloqueou outro, verifique se o próximo pode ser executado na mesma sessão

## Regras

- Nunca pule um item bloqueador — se P2 está pending, P3 não é executável
- Se o item requer API externa não disponível, marque como `blocked: sem-credencial` e passe para o próximo
- Se execução parcial: marque `Status: in_progress` com nota do que falta
- Após execução, sugira: "Próximo item: [P?] — [título]. Executar agora?"

## Output

```
ROADMAP — ITEM EXECUTADO: [P?]
Título: ...
Critério de done: ...
Resultado: ...
Próximo item elegível: [P?] — [título]
```

## Log de occurrent

Atualize `outputs/roadmap.md` com data e resultado de cada execução.
