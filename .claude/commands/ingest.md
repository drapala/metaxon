# /ingest

Compare raw/ com wiki/_registry.md. Para cada fonte nova:

1. Leia o conteúdo (para PDFs, extraia texto; para imagens, descreva;
   para transcrições de áudio/vídeo, processe o texto transcrito)
2. Identifique conceitos-chave (max 3 por fonte)
3. Para cada conceito:
   - Se artigo existe em wiki/concepts/: ATUALIZE adicionando informação nova
   - Se não existe E o conceito provavelmente será referenciado de outros artigos:
     CRIE seguindo o template (use as heurísticas de granularidade do CLAUDE.md)
   - Se não justifica artigo próprio: mencione como seção em artigo existente mais próximo
4. Classifique a fonte: type (article/paper/repo/note/dataset) e quality (primary/secondary/tertiary)
5. Verifique: algum artigo existente agora tem overlap >60% com outro? Se sim, sugira merge
6. Processe quaisquer blocos > [!patch] encontrados nos artigos tocados
7. Ao criar/atualizar artigos, atribua confidence no frontmatter:
   - **high** = 2+ fontes primary concordam
   - **medium** = 1 fonte primary ou 2+ secondary
   - **low** = apenas fontes tertiary ou claim não verificado em raw/
8. DEPOIS de todos os artigos escritos/atualizados, atualize:
   - _registry.md: path | data | type | quality | conceitos | status
   - _index.md: 1 ponteiro por artigo (~150 chars: título + contexto mínimo)
   Ordem importa: artigo primeiro → índice depois. Nunca o contrário.

Reporte: X fontes processadas, Y artigos criados, Z atualizados, W patches resolvidos.
Se encontrar fontes com problemas (vazio, ilegível, duplicata exata): reporte sem processar.
