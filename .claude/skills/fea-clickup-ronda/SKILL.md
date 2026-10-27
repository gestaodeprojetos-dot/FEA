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
- Demandas contínuas, fora de lançamento: pasta **Redes Sociais** (`1400270000003670`) no espaço Marketing Brasil, uma lista por canal (hoje só **YouTube**, `1400270000004568`). Não tem sprint: a ronda olha a lista inteira, pelo prazo de cada tarefa (Keila, 27/10/2026).
- Dentro de cada pasta de lançamento, a **sprint atual** é a lista cujo intervalo no nome contém a data de hoje. A Brasil usa `dd/mm`, a Latam usa `m/d`.
- Incluir pasta nova só com o ok da Keila (regra do CLAUDE.md).

## Em cada rodada (dias úteis: 7h52, 11h52 e 16h52, horário de Brasília)

Cobrança e lembrete acontecem uma vez por dia, na rodada das 7h52. As outras duas rodadas existem para a entrega da equipe não esperar até o dia seguinte para andar.

1. **Entregas comentadas.** Em toda subtarefa aberta da sprint atual, ler os comentários desde a última rodada. Comentário da equipe com link, anexo ou a palavra "entregue": mudar para `em revisão` e responder "Recebido, vou conferir.".
2. **Conferência** de cada tarefa em `em revisão`:
   - Objetiva (link abre, página no ar com HTTP 200, UTM presente, arquivo no Drive com o nome certo, QR abre a URL certa): se passou, mudar para `aprovado` e comentar o que foi conferido. Se não passou, mudar para `em ajuste` com a lista exata do que corrigir.
   - Copy: conferir as regras FEA ("para", sem travessão, linha vermelha) e comentar a nota. Copy, conteúdo médico e peça de anúncio vão para `aprovado` só como pré-revisão: a Keila dá o ok final.
   - **`feito` é só a Keila quem marca.** Até ela autorizar outra coisa, eu nunca fecho tarefa.
   - **Web (André não atualiza o ClickUp, Keila 20/10/2026):** não esperar o status. Em toda rodada, para cada tarefa de Webdesigner aberta, abrir a URL da página, que vem da **planilha de links úteis** do lançamento (Keila, 20/10/2026: não pedir URL na descrição). Caminho: na pasta do lançamento, o doc do ClickUp **Guia de Lançamento** (`clickup_search` por "Guia de Lançamento" com a pasta, depois `clickup_get_document_pages`) tem os links do Drive, da planilha de links úteis e do briefing. Na planilha, a aba WEB DESIGNER lista as páginas, a aba COPY lista a copy de cada página e a aba TRÁFEGO lista as UTMs. Para ler: `curl -sL "https://drive.google.com/uc?export=download&id={ID}"` e openpyxl (os links reais estão em `cell.hyperlink.target`, o texto da célula pode estar diferente); se o download pedir login, usar `mcp__Google_Drive__read_file_content`, que traz o texto (aí o doc de copy se acha pelo título com `search_files`). Ligar cada tarefa à página pelo nome. Abrir a página, com `curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"` (sem esse agente de navegador o site responde 403). Conferir: HTTP 200; frases-chave da copy (linha `Copy:` da descrição, lida com `curl -sL "https://docs.google.com/document/d/{ID}/export?format=txt"`) presentes na página; botões e links de CTA abrindo; quando a tarefa pede, código da VK Metrics no HTML e UTM nos links. Se a página já está no ar com a copy certa, mudar para `aprovado` e comentar para o André o que foi conferido ("🤖 Claude: conferi no ar, está certo, marquei como aprovado."). Se está no ar mas diferente da copy, mudar para `em ajuste` com a lista. Se ainda não mudou, não fazer nada. Página que não está na planilha: listar no relatório para a Keila.
   - **Design (Leo coloca `em revisão`):** conferir contra o briefing da descrição. Ler a copy (`Copy:`, export txt do Google Doc), listar a pasta (`Pasta para salvar:`) com `mcp__Google_Drive__search_files` (`parentId = 'ID'`) e baixar cada arte com `curl -sL "https://drive.google.com/uc?export=download&id={ID}"` para uma pasta nova no scratchpad (nunca baixar em base64 pela ferramenta do Drive, estoura o contexto). Abrir cada imagem com Read e conferir peça por peça:
     1. todas as peças pedidas existem (inclusive as versões COM e SEM CTA quando a copy pede);
     2. o texto da arte bate com a copy, palavra por palavra (data, horário, nome do produto, CTA, acento);
     3. a ordem e a hierarquia pedidas;
     4. a medida e o formato (`file` mostra a resolução);
     5. o nome do arquivo no padrão da pasta;
     6. as regras FEA (sem "pra", sem promessa de resultado, sem marca de ácido ou toxina).

     Passou em tudo: `aprovado` e comentário com o checklist conferido. Faltou algo: `em ajuste` e comentário para o Leo com a lista exata ("peça 01 não está na pasta", "na 03 falta o acento em ..."). Julgamento estético (se ficou bonito, se a foto é a melhor) fica com a Keila: só sinalizar, nunca reprovar por gosto. Cada lançamento tem identidade visual própria (a Black Friday Vitalícia é preto e dourado): conferir a arte contra a identidade da campanha, nunca contra a paleta FEA institucional.
3. **Passagem de bastão.** Quando uma tarefa vira `aprovado` ou `feito`, procurar a próxima da corrente (Gestão → Copy → Design → Web → Automação → Tráfego) que depende dela e comentar lá, atribuindo o comentário ao responsável: "A etapa anterior foi aprovada: [link]. Pode seguir, o prazo é dd/mm."
4. **Vencidas, só na rodada das 7h52** (Keila, 20/10/2026: cobrar 1 vez por dia, nunca 2). Subtarefa com prazo no passado e status fora de `feito`, `aprovado` ou `em revisão`: mudar para `atrasado` e comentar a cobrança, atribuída ao responsável. Antes de comentar, ler os comentários e não cobrar se já houver cobrança de hoje (minha ou da ronda antiga). As rodadas das 11h52 e das 16h52 **não cobram**: só recebem entregas, conferem, passam o bastão e mudam para `atrasado` o que venceu, sem comentar.
5. **Vence amanhã.** Subtarefa aberta com prazo no próximo dia útil: um lembrete por tarefa, só na rodada das 7h52.
6. **Sem prazo ou sem responsável.** Não inventar: listar no relatório para a Keila decidir. Se houver padrão na skill `fea-distribuir-datas`, sugerir a data.
7. **Relatório para a Keila** no fim da rodada, curto e em português:
   - O que andou: entregue, aprovado, passado adiante.
   - O que voltou para ajuste.
   - O que está atrasado, com o responsável e há quantos dias.
   - O que precisa de decisão dela.

   Usar emoji e negrito, e um link para cada tarefa no formato `[nome](url)`.

## Virada de sprint (sexta às 20h52, rotina própria)

Roda depois do expediente da equipe, que costuma ir até as 18h (Keila, 20/10/2026). Antes de virar, receber as entregas comentadas até a hora da virada.

1. Toda subtarefa da sprint atual que não esteja em `feito` vai para a sprint seguinte. Se a sprint seguinte não existir, criar no padrão de nome da pasta, de segunda a sexta, nunca passando da data do evento.
2. Como o ClickUp não move subtarefa sozinha, recriar na sprint seguinte, dentro da tarefa-mãe da mesma área (criar a mãe se não existir, com as datas da sprint):
   - mesmo nome, responsável, status e descrição;
   - novo prazo no mesmo dia da semana da semana seguinte, sem passar da data do evento;
   - se a tarefa estava `atrasado`, o prazo vai para segunda às 18h.

   Depois arquivar a original (`task.archive`). Arquivar dá para desfazer; apagar, nunca.
3. Se a original tiver anexo ou comentário importante, comentar na nova: "Continuação de [link da original], o histórico está lá."
4. No relatório de sexta, listar o que virou de sprint e quantas vezes cada tarefa já virou. Tarefa que virou 2 vezes ou mais é **risco**: sinalizar para a Keila com o motivo provável.

## Thumbs semanais do YouTube (Keila, 27/10/2026)

O canal do Dr. João posta vídeo longo segunda, quarta e sexta, às 20h. O Leo faz as 3 thumbs da semana num dia só.

- Na rodada das 7h52 de **segunda**, criar na lista YouTube a tarefa `Thumbs YouTube da semana dd/mm a dd/mm (seg, qua e sex)` da semana **seguinte**, para o Leo (`44232914`), com início sexta 8h e prazo **sexta da semana atual às 18h**. Copiar a descrição da última tarefa semanal (checklist dos 3 dias com título e vídeo em branco, formato 1280 x 720 px).
- Na quinta, se os 3 títulos e vídeos ainda não estiverem nos comentários, listar no relatório para a Keila (não cobrar o Leo por isso).
- Semana com feriado ou postagem diferente: seguir o que a Keila disser e não criar no automático.

## Textos padrão (regra FEA: sempre "para", nunca "pra", sem travessão)

- Prefixo de todo comentário: `🤖 Claude:` (o conector comenta com a conta da Keila, e o prefixo deixa claro quem escreveu).
- Cobrança: "🤖 Claude: esta tarefa venceu em dd/mm e ainda não foi concluída. Se já entregou, coloque o link aqui nos comentários com a palavra entregue. Se precisa de mais prazo, responda com a nova data possível."
- Lembrete: "🤖 Claude: lembrete, esta tarefa vence amanhã (dd/mm) às 18h. Se tiver algum impedimento, responda aqui."
- O comentário vai **atribuído ao responsável** (campo `assignee` de `clickup_create_task_comment`), que é o que gera o aviso no celular dele pelo app do ClickUp.

## Segurança

- Nunca apagar tarefa, lista ou comentário.
- Nunca mexer em configuração do workspace, automações nativas ou permissões.
- Se algo sair do padrão (lista sumiu, centenas de tarefas vencidas de uma vez, erro de permissão), não agir em massa: só reportar à Keila.
