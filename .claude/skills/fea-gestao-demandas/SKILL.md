---
name: fea-gestao-demandas
description: Gestão de demandas da FEA (Dr. João Pithon) no ClickUp e nos grupos de WhatsApp. Usar sempre que for criar, atualizar, arquivar ou conferir task no ClickUp, operar a linha de produção (entrega que dispara a próxima etapa), montar rascunho de mensagem ao time no Gestão FEA, cobrar ou lembrar alguém, fazer ronda de pendências ou responder pedido de demanda. Gatilhos: "cria a task", "sobe no ClickUp", "demanda nova", "a Adri entregou", "o Leo entregou", "cobra o André", "ronda", "pendências", "rascunho para o time", "envia para a automação", "mensagem ao Luca", "quem aprova", "linha de produção".
---

# FEA · Gestão de demandas

Fonte das regras: `CLAUDE.md` do repositório FEA (seções "Gestão de projetos e ClickUp", "Guia de operações de lançamentos" e "Regras fixas") e `FEA-regras-em-vigor.md`. Esta skill é o "como fazer" da gestão. Se houver conflito, vale a regra mais recente com data.

## Objetivo

Nenhuma demanda fica parada, nenhuma task nasce sem pedido, e toda mensagem ao time sai validada, completa e com o link certo do ClickUp.

## Regra de condução (Keila, 26/11, vale acima das antigas)

Eu conduzo o projeto e não espero a gestão perguntar. Entrega recebida = conferir, atualizar ClickUp e docs e passar direto ao próximo responsável, avisando quem precisa, sem rascunho (exceto Grazi, Carol, Luca e assunto sensível). Nunca deduzir: sem a informação na mão, perguntar à pessoa. Detalhe em fea-agente-gestao, seção "Agente condutor do projeto".

## Quando usar

- Qualquer criação, atualização, arquivamento ou conferência de task no ClickUp da FEA.
- Quando alguém do time entrega algo (copy, arte, vídeo, página, automação, link): dispara a linha de produção.
- Quando for preciso cobrar, lembrar ou fazer ronda de pendências.
- Quando for montar rascunho de mensagem ao time, ao Luca, ao Leo, ao André ou à Automação.
- Quando chegar pedido de demanda em qualquer grupo ou no privado.

## Passo a passo

### 1. Antes de criar qualquer coisa

1. Confirmar **quem pediu, onde e quando** (pessoa, grupo, horário). Sem pedido de ninguém e sem estar no briefing ou no ClickUp, **não cria** (Keila, 26/11 14h12).
2. Procurar antes de criar: uma demanda, uma task. Informação nova atualiza a task existente.
3. Conferir se o pedido veio de grupo com a gestão. Pedido feito no privado, no grupo "Solicitaçao de demanda" ou em grupo sem Keila e Gabi não vira task: responder com a mensagem padrão (seção "Mensagens fixas").
4. Demanda de outra pessoa: a dona da demanda coloca no ClickUp; o Claude cria quando o pedido chegou no grupo com a gestão ou com autorização da Keila ou da Gabi. Pedido do Luca a qualquer colaborador vira task na hora (ou atualiza a existente).

### 2. Criar a task no ClickUp

1. Sempre **subtarefa da mãe da área na sprint certa**. Mães: Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego, Suporte/CS, Operação do dia.
2. **Datas obrigatórias**: início e vencimento antes de criar. Padrão de subtarefa: início 8h, prazo 18h. Copy: vencimento 23h59 do dia de entrega (Adri, 23/11). Sem vencimento definido: perguntar antes, nunca inventar data. Se `start_date` conflitar com `due_date` no passado, parar e perguntar.
3. **Responsável** definido.
4. **Descrição** com: lançamento (produto ou evento, Brasil ou Latam), link do briefing, link do Drive e o que é a entrega. Task do Leo leva a linha **"Pasta para salvar:"** com a pasta ESTÁTICOS da fase (4. TRÁFEGO / CRIATIVOS PRONTOS / fase / ESTÁTICOS).
5. Copy: tarefa de comunicação de evento dividida em subtarefas por etapa (onboarding, captação, lembrete, vendas), cada uma com API, WhatsApp e e-mail; responsáveis Matheus van der Ham e Adri. SLA: copy nova 4 dias úteis; revisão 48h quando não urgente; urgente com prioridade marcada.
6. Comentário do Claude no ClickUp começa com **"🤖 Claude:"**.
7. Executar direto, sem perguntar "posso criar?" (Keila, 24/11). Se a cota do conector acabar, usar a API direta (api.clickup.com).

### 2b. Modelo de backlog de lançamento: itens fixos

- **Desabilitar fluxos de aula (Keila, 26/11 17h42):** para cada CPL, masterclass ou aula ao vivo do lançamento, criar a subtarefa "Desabilitar fluxos que citam aula/aulão · [evento]" embaixo da mãe **Automação** da sprint que contém o dia seguinte à aula (se a sprint não tiver a mãe Automação, criar a mãe no padrão das outras: sem responsável, datas da sprint). Início 8h e prazo 18h do dia seguinte à aula; aulas em dias seguidos (ex.: Desafio de 3 dias) podem ficar numa task só, do dia seguinte à 1ª aula até o dia seguinte à última, com a ordem de desabilitar aula por aula. Responsável: Equipe IAutomate (Vivi e Dani não têm usuário próprio no ClickUp). Descrição: lançamento, data da aula, o que fazer (desabilitar no ActiveCampaign, API, WhatsApp/SendFlow, e-mail, URA e SMS tudo o que fala de aula, aulão, ao vivo, masterclass ou Zoom do evento, inclusive gatilhos de inscrição tardia e lembretes agendados), entrega (comentar os fluxos desabilitados e mudar para "em revisão") e a origem. Sem data da aula no backlog ou no briefing: não inventar, levar como pendência.
- Procurar antes de criar (uma demanda, uma task) e conferir se a mãe da sprint já existe antes de criar outra.

### 3. Status

- Status FEA: a fazer · fazendo · em revisão · em ajuste · atrasado · aprovado · pausado · sprint · feito.
- **Nunca marcar "feito"** (Keila, 19/11). Entrega conferida vai para "aprovado" ou "em revisão", inclusive em tarefa agendada que diga "concluir".
- Copy só vira "aprovado" depois do ok da Adri ou do Matheus (Adri, 25/11).
- Criativo novo de produto antes de haver dado de performance do primeiro lote: task fica "pausado" com o motivo (Keila, 26/11).
- **Nunca apagar** task, lista, comentário ou linha de planilha. O que foi criado sem pedido é **arquivado** com o comentário: "🤖 Claude: criada sem solicitação, arquivada por orientação da Keila".
- Nunca mexer em permissão, automação nativa ou configuração do workspace.

### 4. Linha de produção (toda entrega dispara a próxima etapa)

Quando alguém entrega, comenta ou valida, na mesma rodada:

1. Agradecer na hora, marcando a pessoa, no mesmo grupo ("obrigada" + @).
2. Conferir a entrega (abrir o link, ver o arquivo).
3. Atualizar a task (aprovado ou em revisão), docs, briefing, planilha de Links úteis e ClickUp. Mostrar no Gestão FEA **onde** atualizou, com os links.
4. Criar a task da próxima etapa (ex.: copy de criativos entregue pela Adri → task do Leo embaixo da mãe Design da sprint certa, com datas, responsável, link da copy e "Pasta para salvar:").
5. Trazer ao Gestão FEA o rascunho para o próximo setor.

Cadeia: copy → artes (Leo) ou vídeo (Gabriela, Edição) → páginas (André) → automação → tráfego (Saar) → teste do caminho do lead (Gabi, só com grupo, páginas, automação e UTMs 100% prontos).

### 5. Conferir antes de cobrar ou afirmar status

- Olhar **todos os lugares**: grupos, privado, Drive (arquivos e revisões, pastas do evento), ClickUp e planilhas. Ausência de registro no ClickUp não prova que não foi feito.
- Antes de afirmar no grupo que algo foi ou não foi feito, pedir para a Gabi conferir.
- Só lembra ou cobra quem de fato não entregou.
- Prazo é nosso: com data já definida, não perguntar "quando vai entregar"; confirmar se a pessoa consegue até a data ("precisamos até amanhã, 26/11, consegue?").

### 6. Rascunho no Gestão FEA antes de mensagem ao time

1. Toda mensagem ao time (fora do Gestão FEA) vai antes como rascunho e só sai com ok da Keila ou da Gabi, ou de quem solicitou a mensagem ou é responsável pela task. Texto mudou depois do ok: volta para validação.
2. Cabeçalho do rascunho em negrito: número, assunto (nome completo, com Brasil ou Latam quando houver as duas versões) e setor. Numeração única e sequencial; a Keila aprova com "ok N" (Keila, 25/11 18h52: sem siglas genéricas tipo GERAL-n ou CS-A).
3. Texto a ser validado vai sozinho numa mensagem; o contexto vai em outra. Um assunto por mensagem; nunca juntar dois rascunhos, rascunho e status, ou pessoas diferentes.
4. Só trazer rascunho executável: se a demanda ainda depende de outra entrega, fica no ClickUp.
5. Enviou: reagir com ✅ no rascunho e confirmar citando o número ("13a enviada").
6. Rascunho vivo: se um fato muda, nova versão dizendo o que mudou.
7. Pendente de ok: lembrar no Gestão FEA a cada 5 minutos até sair (lista em `FEA-pendencias-resposta.md`).

Saem sem rascunho: recebido, agradecimento, link ou material existente com a fonte, atualização de ClickUp, planilha e briefing, lembrete de prazo padrão depois de conferir a entrega, dúvida sobre onde está cada coisa, Daily FEA, respostas simples ao Matheus no grupo Copy e no privado dele, pergunta ao responsável quando o pedido de alguém depende dele. Continuam com ok: demanda nova ao time, Luca, preço, oferta, datas, aprovações, cobrança dura e privado não liberado.

### 7. Pendências e rondas

Cada item leva: produto ou evento (ex.: "Master Bio 12/26 · página do Zoom"), código, quem pediu (pessoa, grupo, horário), quem está aguardando, **há quanto tempo espera** ("esperando há 3h20", "desde ontem 15h38"), linha "Impacto:" e o link da task daquela entrega. Um item por entrega. Se ninguém pediu (divergência encontrada por mim), dizer isso. Antes de trazer ronda, conferir Drive, ClickUp, Links úteis e grupos e atualizar o que já foi entregue.

## Formatos fixos de mensagem

**Regras gerais**: curta, cordial, linha em branco entre blocos, rótulo de link em negrito numa linha e o link na de baixo, datas em negrito, links numerados quando forem vários, "envio" e nunca "mando", nunca "pra", sem "Obrigada!" no fechamento, sem título nem código para o time (só @ e texto), @ da pessoa no ponto em que o nome aparece, 🏻 nos grupos, saudação só na primeira mensagem do dia. Toda demanda leva um link de task do ClickUp por entrega, com data final. Produto com Brasil e Latam: 🇧🇷 / 🇪🇸 em cada bloco.

**Leo (artes, só estático)**:
```
@Leo, demanda nova · [evento]

*[Nome da entrega]*
[link da task no ClickUp]

Entrega: *dd/mm*
```
Mais nada (sem contexto, sem pendências, sem "pode começar").

**André (páginas)**: demanda com o link da task, o link do doc de copy revisado e da página, e as divergências entre copy e página como observação. Junto, o rascunho de aviso ao Luca com o doc revisado e a página.

**Luca**: sem saudação inicial e sem "Obrigada!". Abre com "Ainda precisamos de:", nome do lançamento em negrito, a frase do que fecha ("Para fechar a página de vendas e os criativos, faltam estas definições:"), itens com emoji e negrito, link do doc para ele preencher e "Consegue preencher até amanhã?". **Nunca link do ClickUp para o Luca.** Vários links: numerados, com linha em branco entre eles. Pedido do Luca: "ok, vou verificar" na hora, prioridade máxima, máximo de agentes em paralelo. Quando a Keila também for mandar, entregar a versão no tom dela (título = o pedido dele, links só com linha em branco, sem número).

**Automação (Vivi, Dani Agrela 5514996197964)**: pedido de grupo sai com o "Doc para captação - Automação" do evento preenchido (modelo MPL 11/26). Entregas da automação ficam no ClickUp e na planilha: não pedir link no WhatsApp; agradecer só com "obrigada" marcando a pessoa. Agendamento de disparos é da Automação, não da Copy. Pedido de inclusão do número da FEA nos grupos de evento sempre como membro, nunca admin, com o número completo +55 11 3280-4911.

## Quem autoriza o quê

| Assunto | Quem |
|---|---|
| Ok de mensagem ao time | Keila ou Gabi, ou quem solicitou a mensagem ou é responsável pela task |
| Demanda de outra pessoa no ClickUp | dona da demanda; ou Keila/Gabi |
| Regra nova | só Keila ou Gabi (pedido do time é sugestão: "Ok, vamos verificar internamente com a gestão e retorno.") |
| Criativos (tráfego, diagnóstico, anúncio) | Gabi (nunca a Grazi) |
| Demais artes (capa de formulário, banner de checkout, cordão, crachá, credencial, material de evento) | Grazi |
| Copy aprovada | Adri ou Matheus |
| Depoimentos | Grazi (o que já está nas pastas do Drive conta como autorizado) |
| Página publicada | André libera; Luca aprova |
| Clint e Hotmart (ação) | Keila, Gabi ou Sabrina |
| Oferta, página, vagas, preço e checkout do Elite Mentoring | Sabrina, no Claude comercial |
| Operacional (ronda de entregas, atrasos) | Gabi, marcada |

## Mensagens fixas

Pedido de demanda em grupo sem a gestão (Keila, ok 630, 26/11):
```
@[pessoa], recebido! 😊 Para eu conseguir executar, as solicitações de demanda são feitas no grupo do setor, onde a gestão acompanha: 🎨 Artes: grupo Artes | FEA · 💻 Páginas: grupo Web | FEA · ✍️ Copy: grupo Copy | FEA · ⚙️ Automação: grupo Automações. Pode enviar lá, com o que precisa e o prazo, que eu já pego por lá 💜
```
Recebido imediato (sem validação, para todos): "Recebido! Já estou verificando X e te envio por aqui." Prazo só realista: nunca "em instantes" se depende de validação.

## Erros já cometidos

- Tasks de folheto premium e crachá "Mentorada Elite" criadas a partir do briefing sem pedido de ninguém (26/11): arquivadas com comentário. Nunca criar o que ninguém pediu.
- Cobrança à Adri (17/11): a parte dela estava pronta; a pendência era a revisão da Grazi. Conferir em todos os lugares e passar pela Gabi antes.
- Listboss da Master Bio marcado como aprovado antes do ok da Adri (25/11).
- Carol mandou o link do grupo do Combo (24/11): atualizei o doc mas não agradeci nem preparei a mensagem à automação. Entrega recebida = agradecer + atualizar + próximo setor na mesma rodada.
- Leo esperou 40 min por um recebido no privado (24/11); Erika ficou de 9h39 a 10h16 sem retorno sobre o CMYK do cordão.
- Mensagem 30 ao André (19/11): texto mudou depois do ok e saiu sem nova validação.
- Criativos levados à Grazi para aprovação (erro repetido 2 a 3 vezes, 25/11): criativo é com a Gabi.
- Confusão entre as duas Danis (25/11): Daniela Dantas (CS) 5511996804277 e Danielly Agrela (Automação) 5514996197964.
- Alerta 🚨 de página fora do ar na captura Master Bio (25/11): era página ainda não publicada. Conferir se já foi publicada antes de alertar.
- Assuntos juntos na mesma mensagem (erro repetido, 21/11): dividir sempre.

### Erros registrados em 26/11 (Keila)
- **Mãe Automação em duplicidade (26/11, tarefa dos fluxos de aula):** o script de criação foi importado por outro script e rodou de novo, criando duas mães "Automação" em Master Bio Sprint 4 e MTB Sprint 5. As vazias foram arquivadas com comentário. Script de criação nunca é importado: cada criação roda uma vez só, e a lista é conferida logo depois.
- **PROW:** registrei "PROW confirmada" na task e na planilha a partir de uma mensagem das 11h08, mas o Luca já tinha cancelado às 13h22. Antes de registrar uma decisão, ler o grupo até a última mensagem do assunto.
- **Números 500/501:** numerei rascunhos sem pedir o número à vigia, e esses números já estavam em uso. O número de rascunho vem sempre da vigia (numeração única).
- **Crachá e folheto:** tasks criadas a partir do briefing, sem pedido de ninguém. O crachá ficou duplicado com o cordão já aprovado. Arquivadas por orientação da Keila.

## Atualização

Toda regra nova, erro apontado ou padrão aprovado sobre gestão de demandas entra aqui na hora, com data e autor (ex.: "Keila, 26/11 15h09"), e também no `CLAUDE.md`, com commit. Regra nova que substitui outra: dizer qual substitui.
