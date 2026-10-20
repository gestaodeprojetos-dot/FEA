---
name: fea-clickup-ronda
description: Ronda diária das demandas FEA no ClickUp feita pelo Claude. Cobra tarefas vencidas, avisa o que vence amanhã, confere o que está em revisão, recebe entregas comentadas pela equipe e, na sexta, passa para a sprint seguinte o que não foi concluído. Usar quando a Routine diária disparar ou quando a Keila pedir ronda, cobrança, acompanhamento das demandas ou para virar a sprint.
---

# FEA: ronda diária no ClickUp

O Claude é quem opera o ClickUp dos lançamentos (Keila, 20/10/2026). A equipe só faz duas coisas:
1. **entregar:** comentar na tarefa com o link ou anexo e a palavra "entregue";
2. **responder** às cobranças nos comentários.

Datas, status, sprints, responsáveis e criação de tarefas são só comigo. Quem decide e aprova é a Keila.

## Escopo

- Workspace `9013080622`.
- Pastas monitoradas: as pastas de lançamento ativas no espaço Marketing Brasil (`90130517360`) e no espaço Marketing Latam (`901314001225`). Hoje são **Black Friday Vitalícia 10/26** (`901318759044`) e **Black Friday Total - Latam** (`901318793839`).
- Dentro de cada pasta, a **sprint atual** é a lista cujo intervalo no nome contém a data de hoje. A Brasil usa `dd/mm`, a Latam usa `m/d`.
- Incluir pasta nova só com o ok da Keila (regra do CLAUDE.md).

## Em cada rodada (dias úteis: 7h52, 11h52 e 16h52, horário de Brasília)

1. **Entregas comentadas.** Em toda subtarefa aberta da sprint atual, ler os comentários desde a última rodada. Comentário da equipe com link, anexo ou a palavra "entregue": mudar para `em revisão` e responder "Recebido, vou conferir.".
2. **Conferência** de cada tarefa em `em revisão`:
   - Objetiva (link abre, página no ar com HTTP 200, UTM presente, arquivo no Drive com o nome certo, QR abre a URL certa): se passou, mudar para `aprovado` e comentar o que foi conferido. Se não passou, mudar para `em ajuste` com a lista exata do que corrigir.
   - Copy: conferir as regras FEA ("para", sem travessão, linha vermelha) e comentar a nota. Copy, conteúdo médico e peça de anúncio vão para `aprovado` só como pré-revisão: a Keila dá o ok final.
   - **`feito` é só a Keila quem marca.** Até ela autorizar outra coisa, eu nunca fecho tarefa.
3. **Passagem de bastão.** Quando uma tarefa vira `aprovado` ou `feito`, procurar a próxima da corrente (Gestão → Copy → Design → Web → Automação → Tráfego) que depende dela e comentar lá, atribuindo o comentário ao responsável: "A etapa anterior foi aprovada: [link]. Pode seguir, o prazo é dd/mm."
4. **Vencidas.** Subtarefa com prazo no passado e status fora de `feito`, `aprovado` ou `em revisão`: mudar para `atrasado` e comentar a cobrança, atribuída ao responsável. **Só uma cobrança por tarefa por dia:** antes de comentar, ler os comentários e não repetir se já houver cobrança de hoje (minha ou da ronda antiga).
5. **Vence amanhã.** Subtarefa aberta com prazo no próximo dia útil: um lembrete por tarefa, só na rodada das 7h52.
6. **Sem prazo ou sem responsável.** Não inventar: listar no relatório para a Keila decidir. Se houver padrão na skill `fea-distribuir-datas`, sugerir a data.
7. **Relatório para a Keila** no fim da rodada, curto e em português:
   - O que andou: entregue, aprovado, passado adiante.
   - O que voltou para ajuste.
   - O que está atrasado, com o responsável e há quantos dias.
   - O que precisa de decisão dela.

   Usar emoji e negrito, e um link para cada tarefa no formato `[nome](url)`.

## Virada de sprint (sexta, rodada das 16h52)

1. Toda subtarefa da sprint atual que não esteja em `feito` vai para a sprint seguinte. Se a sprint seguinte não existir, criar no padrão de nome da pasta, de segunda a sexta, nunca passando da data do evento.
2. Como o ClickUp não move subtarefa sozinha, recriar na sprint seguinte, dentro da tarefa-mãe da mesma área (criar a mãe se não existir, com as datas da sprint):
   - mesmo nome, responsável, status e descrição;
   - novo prazo no mesmo dia da semana da semana seguinte, sem passar da data do evento;
   - se a tarefa estava `atrasado`, o prazo vai para segunda às 18h.

   Depois arquivar a original (`task.archive`). Arquivar dá para desfazer; apagar, nunca.
3. Se a original tiver anexo ou comentário importante, comentar na nova: "Continuação de [link da original], o histórico está lá."
4. No relatório de sexta, listar o que virou de sprint e quantas vezes cada tarefa já virou. Tarefa que virou 2 vezes ou mais é **risco**: sinalizar para a Keila com o motivo provável.

## Textos padrão (regra FEA: sempre "para", nunca "pra", sem travessão)

- Prefixo de todo comentário: `🤖 Claude:` (o conector comenta com a conta da Keila, e o prefixo deixa claro quem escreveu).
- Cobrança: "🤖 Claude: esta tarefa venceu em dd/mm e ainda não foi concluída. Se já entregou, coloque o link aqui nos comentários com a palavra entregue. Se precisa de mais prazo, responda com a nova data possível."
- Lembrete: "🤖 Claude: lembrete, esta tarefa vence amanhã (dd/mm) às 18h. Se tiver algum impedimento, responda aqui."
- O comentário vai **atribuído ao responsável** (campo `assignee` de `clickup_create_task_comment`), que é o que gera o aviso no celular dele pelo app do ClickUp.

## Segurança

- Nunca apagar tarefa, lista ou comentário.
- Nunca mexer em configuração do workspace, automações nativas ou permissões.
- Se algo sair do padrão (lista sumiu, centenas de tarefas vencidas de uma vez, erro de permissão), não agir em massa: só reportar à Keila.
