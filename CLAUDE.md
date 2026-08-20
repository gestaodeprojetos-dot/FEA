# FEA — Instruções do projeto

## REGRA ABSOLUTA: tudo é commitado no git

Nenhum trabalho neste repositório fica apenas no disco. **Todo** arquivo criado
ou modificado deve terminar commitado e enviado ao remoto — sem exceção, sem
precisar de pedido explícito do usuário.

Isso vale para qualquer tipo de arquivo, não só código:

- código-fonte, configuração, scripts
- documentação, notas, README
- skills (`.claude/skills/`), hooks, settings do Claude Code
- assets, planilhas, documentos gerados
- correções pequenas, "one-liners", ajustes de formatação

### Fluxo obrigatório ao final de qualquer tarefa

1. `git add` dos arquivos da tarefa
2. `git commit` com mensagem descritiva explicando **o quê** e **por quê**
3. `git push -u origin <branch>`
4. Abrir pull request **draft** se ainda não houver um PR aberto para a branch

Terminar um turno com mudanças não commitadas no working tree é considerado
trabalho incompleto. Antes de reportar uma tarefa como concluída, rode
`git status` e confirme que a árvore está limpa.

### Exceções

Só ficam fora do commit:

- arquivos temporários de scratchpad (fora do repositório)
- segredos, tokens, credenciais e `.env` — estes **nunca** são commitados; se
  aparecerem, avise o usuário em vez de commitar
- artefatos de build e dependências já cobertos por `.gitignore`

Se algo não puder ser commitado por um motivo legítimo, diga isso
explicitamente ao usuário — não deixe passar em silêncio.

## Branches

Desenvolver na branch designada para a sessão. Nunca fazer push direto em
`main` sem permissão explícita.
