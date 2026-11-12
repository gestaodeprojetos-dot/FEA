---
name: fea-distribuir-datas
description: Distribui datas e sprints das tarefas de um lançamento FEA no ClickUp pelo padrão D-menos (dias antes da captação e do evento), medido nos lançamentos reais. Usar quando a Keila copiar as tarefas de um lançamento anterior para um novo, pedir para "distribuir as datas", "colocar data nas tarefas", "montar as sprints", "organizar as semanas" ou quando houver tarefas abertas sem prazo num lançamento.
---

# FEA: distribuir datas e sprints de lançamento

A Keila monta um lançamento novo copiando as tarefas de um lançamento parecido. Esta skill dá data, sprint e responsável a cada tarefa, seguindo a ordem que os lançamentos reais seguiram.

## O que eu preciso dela (só isso)

1. **Início da captação** (data).
2. **Data do evento ou live** (se houver duas lives, por exemplo alunos e geral, a da abertura geral é a régua).
3. Qual pasta do ClickUp é o lançamento.

Sem essas duas datas eu não distribuo: perguntar antes, nunca assumir.

## Duas réguas

O padrão está em `FEA-gestao-clickup/FEA-padrao-d-menos.csv`, medido na BF Brasil 2026 (87 tarefas concluídas) e completado na BF Latam 2026.

- **Régua captação:** tarefas que montam a captação (páginas de captura, UTMs, criativos de captação, webhook, comunidade, decisões comerciais) contam em dias a partir do início da captação.
- **Régua evento:** setup inicial, vendas e reta final (slides, QR, página de vendas, Zoom) contam a partir do evento.

Por que duas: na Brasil a captação começou 20 dias antes da live e na Latam só 14. Uma régua só empurraria a montagem da captação para depois da abertura.

**Ordem dentro de cada entrega:** Gestão decide → Copy → Design → Web → Automação → Tráfego → Gestão confere. Tarefa sem par na tabela recebe data por essa corrente (depois de quem ela depende, antes de quem depende dela).

## Passo a passo

1. **Exportar** as tarefas do lançamento (só leitura): `clickup_filter_tasks` com `folder_ids`, `include_closed=true`, paginando até `has_more=false`, e depois `task.get_many` via `clickup_execute_operator` para pegar a tarefa-mãe, as datas e os responsáveis. Gerar um CSV com `id, name, parent_name, status, assignees, due_date`.
2. **Calcular:**
   ```
   python3 FEA-gestao-clickup/fea_distribuir_datas.py tarefas.csv --captacao AAAA-MM-DD --evento AAAA-MM-DD --hoje AAAA-MM-DD --saida FEA-proposta-datas.csv
   ```
   Regras do script: fim de semana vai para a sexta anterior; quando o padrão cai antes de hoje, a tarefa vira **RECUPERAR** com prazo no próximo dia útil; tarefa sem par fica marcada **SEM PAR**.
3. **Revisar à mão**, em cima do resultado do script:
   - SEM PAR: decidir pela corrente.
   - Tarefas que dependem de outra precisam vencer depois dela (por exemplo, a arte das imagens de API vem depois da copy delas).
   - Carga por pessoa: mais de 5 entregas de uma pessoa na mesma semana é risco, sinalizar.
   - Duplicadas: juntar com `clickup_merge_tasks`, que leva comentários e anexos.
   - Nome com "pra": corrigir para "para" (regra de escrita FEA).
4. **Mostrar a tabela para a Keila aprovar** antes de gravar: tarefa, prazo, responsável e o que está atrasado pelo padrão. Ela pode mudar uma data só, e a equipe vê na hora.
5. **Gravar**, depois do ok:
   - Datas: `task.update_many` agrupando as tarefas que têm o mesmo patch (início e prazo em ms, com `start_date_time` e `due_date_time` true). Horário padrão: início 8h e prazo 18h, horário de Brasília.
   - **Nenhuma tarefa fica sem responsável** (Keila, 12/11/2026: "tem várias tarefas que não têm responsáveis, precisa tomar cuidado"). Padrão por área, igual aos lançamentos de novembro: Copy → Adriane Möbbs + Matheus van der Ham · Design → Leo Quirino · Webdesigner → André Vivas · Automação → Equipe IAutomate · Gestão de Tráfego → Matheus Saar. Gestão, Comercial, Produção de Evento e qualquer caso fora desse padrão: perguntar à Keila antes, nunca atribuir por palpite.
6. **Sprints**, quando ela pedir ou quando faltarem semanas até o evento:
   - Uma lista por semana, de segunda a sexta, criada com `clickup_create_list_in_folder`, seguindo o formato de nome que a pasta já usa. Exemplos: Brasil `Sprint 10 (19/10 - 25/10)`, Latam `Sprint 10 (11/2 - 11/6)`. A última sprint termina no evento.
   - O ClickUp não move subtarefa sozinha (o recurso "Subtasks in Multiple Lists" está desligado). Então eu crio as tarefas-mãe da área (Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego) na sprint de destino, com as datas da sprint, recrio as subtarefas com `task.create_many` (`parent_task_id`, responsável e datas) e **arquivo** as originais com `task.archive`. Arquivar dá para desfazer; apagar, nunca.
   - Antes de recriar, conferir se a original tem descrição, anexo ou checklist. Se tiver, copiar a descrição e avisar a Keila do anexo.
7. **Conferir** com `clickup_filter_tasks` nas listas mexidas: toda subtarefa aberta com prazo e responsável, nada esquecido na sprint antiga.

## Organização das pastas por ano (Keila, 28/10/2026)

- **Uma pasta por lançamento** (cada masterclass, desafio, evento ou Black Friday é uma pasta própria), no espaço Marketing Brasil ou Marketing Latam, com o mês e o ano no nome: `Masterclass Toxina 01/27`, `Masterclass Bioestimulador Latam 02/27`.
- O plano do ClickUp **não deixa criar espaço novo** (limite de 5, contando os arquivados), então não existe "Marketing 2027" separado: o ano vai no nome da pasta.
- **No ClickUp ficam só os lançamentos do ano corrente e os de janeiro do ano seguinte** (Keila, 10/11/2026: "para não atrapalhar a cabeça de ninguém"). No Drive pode ficar tudo criado. Pasta de lançamento posterior a janeiro que já exista: arquivar as listas e renomear a pasta com o prefixo `ARQUIVAR ·` para a Keila arquivar na interface.
- **Férias coletivas a partir de 15/12/2026** (Keila, 10/11/2026): o lançamento de dezembro (Masterclass Anatomia 12/26) e os de janeiro (Toxina 01/27, Preenchimento Labial 01/27 + Desafio Full Face) precisam estar com tudo produzido antes de 15/12. Ao distribuir datas desses lançamentos, o prazo máximo de qualquer entrega da equipe é 11/12/2026.
- **A pasta só nasce quando o lançamento se aproxima:** cerca de 45 dias antes do início da captação, a partir do calendário `FEA-gestao-clickup/FEA-calendario-2026-2027.md`. Assim o espaço mostra só o que está em uso. Ao criar, avisar a Keila no relatório e montar o backlog copiando o lançamento anterior parecido.
- **Fim do lançamento:** a API não arquiva pasta. Listar no relatório as pastas encerradas para a Keila arquivar na interface (três pontinhos da pasta > Arquivar).
- **Perpétuos** ficam com o prefixo `Perpétuo ·` no nome, em cada espaço.
- **Toda pasta nova (lançamento ou perpétuo) nasce com** (Keila, 09/11/2026): o doc **Guia de Informações** dentro da pasta do ClickUp, copiando o `Template Guia de Informações` (`8ckhche-3353`, páginas Links úteis, Datas e Planilha com link dos setores) com o Drive, o briefing e a planilha de links; e a **planilha de links úteis no padrão de lançamento** (modelo: Links úteis do MTB 11/26, `1Psxwt2QCTgqeOf7pU5NvSbNq3R8bEhwp`: abas GERAL, COPY, ARTES, WEB DESIGNER e TRÁFEGO, nome do produto no A1 da GERAL, linhas zebradas, link com o nome do arquivo). Nunca usar o modelo do PLX. **Colunas sempre só `Nome | Link`, sem coluna "Fase"** (Keila, 11/11/2026: "tira aquilo, segue padrão sempre"); se a planilha nascer de cópia de um lançamento antigo que tinha "Fase", apagar a coluna antes de entregar. Rótulos da GERAL iguais aos do MEI 11/26: Link grupo WhatsApp, Nome da Lista do active, Nome da Tag de Inscritos do active, Tag Active pesquisa, Resposta dos Leads, Link de webhook, Link do Zoom.
- **Pasta do Drive de lançamento ou perpétuo segue o padrão de lançamento** (Keila, 09/11/2026: "é para seguir padrão lançamento"; modelo `7. MASTERCLASS ANATOMIA 12/26`): 0. PLANEJAMENTO · 1. COPY (1. PÁGINAS, 2. CRIATIVOS, 3. COMUNICAÇÃO com API/WHATSAPP/EMAIL, 4. LEGENDAS, 5. EVENTO) · 2. ARTES (1. WHATSAPP, 2. THUMB YOUTUBE, 3. CAPAS, 4. PERFIL, 5. FORMS, 6. INGRESSO, 7. SLIDES, 8. QR CODE) · 3. PESQUISA · 4. TRÁFEGO (BRUTOS, CRIATIVOS PRONTOS com uma pasta por fase do tráfego: 1. CAPTAÇÃO, 2. ANTECIPAÇÃO, 3. LEMBRETE, 4. VENDAS e as demais fases do lançamento, como upgrade; **dentro de cada fase, a pasta ESTÁTICOS**, onde o Leo sobe os estáticos, e os vídeos ficam na raiz da fase; Keila, 12/11/2026) · 5. LOGO · 6. PÁGINA DE VENDAS · 7. URA + SMS · 8. AUTOMAÇÃO · planilha de links na raiz. **Criativos prontos ficam em 4. TRÁFEGO, nunca em ARTES.** Toda tarefa de criativo para o Leo leva a linha `Pasta para salvar:` com o link da ESTÁTICOS e o da fase (vídeos). Não inventar pasta fora desse padrão.
- **Toda lista nova (backlog ou sprint) nasce com o padrão FEA** (Keila, 29/10/2026):
  - status do modelo **FEA**: a fazer · fazendo · em revisão · em ajuste · atrasado · aprovado · pausado · sprint · feito. Aplicar com `list.update` (`clickup_execute_operator`), `override_statuses: true` e a lista de status copiada da Sprint 10 da Black Brasil (`1400270000002473`); mapear `brifado`→a fazer, `revisao`→em revisão, `ajustar`→em ajuste, `complete`→feito, `to do`→a fazer, `in progress`→fazendo.
  - visualização **Modelo de Sprint**: `view.create` tipo `list`, agrupada por status, colunas visíveis responsável, data de início, prazo e comentários, mostrando tarefas fechadas.
  - Ficam fora do padrão só a lista de produção do Elite Injectors (status próprios do evento) e o Webinário FEB Latam (encerrado).

## Tarefas obrigatórias em todo backlog de lançamento

- **Automação: "Disponibilizar no Drive a planilha de respostas dos compradores"** (Keila, 06/11/2026: "nunca está no nosso Drive"). Responsável: Equipe IAutomate (`194479496`). Dentro da tarefa-mãe Automação. Prazo: o dia em que as vendas abrem, 18h; início 5 dias úteis antes. Descrição: garantir que a pesquisa de quem compra grave numa planilha Google, salvar na pasta AUTOMAÇÃO do lançamento com o nome "[lançamento] - RESPOSTAS DOS COMPRADORES" e comentar o link com "entregue"; o Claude registra na aba GERAL da planilha de links úteis. Hoje o Drive só tem a planilha de captação e a de respostas dos inscritos no evento.
- **Automação: "Criar formulário de matrícula"** (Keila, 06/11/2026), a pesquisa que o comprador responde depois de comprar e que alimenta a planilha acima. Responsável: Equipe IAutomate. Prazo: 5 dias úteis antes da abertura das vendas, 18h. Modelos no Drive: Brasil, `Formulário de Matrícula FEP 2.0` (`1PuiNRY-N28aEQuOdDtO_ahOF9sIUXM8C6rG30fjr1Go`, FEP > 1. Curso > 2. Pesquisas); Latam, `Formulario de Matrícula - Black Friday Total Latam` (`1TbiR7GzVK9G9Tdc-yo97vbin1FXCH4W0a3LNYoDCSM8`). O Claude pode criar a cópia pela API do Drive (`files/{id}/copy` para a pasta 3. PESQUISA); editar perguntas e vincular a planilha só pelo editor do Forms (o acesso do Claude não tem o escopo do Forms).
- Cada produto tem o seu formulário de matrícula: **FEP não é a mesma coisa que a Black** (Keila, 06/11/2026). O `Formulário de Matrícula FEP 2.0` é só dos alunos da FEP; a Black usa o próprio (`Formulário de Matrícula - Black Friday Vitalícia 10/26`, `1aG08O2aBYC4lPz4iJyFaUpm5SC2hq_UYMq_Sx2MTwbw`), com a capa da campanha.
- Ao copiar o backlog de um lançamento anterior, conferir se essas duas tarefas vieram junto; se não, criar.

## Referências fixas (workspace 9013080622)

| Pessoa | ID ClickUp |
|---|---|
| Keila Gestão | 99934269 |
| Gabriela Borges | 118026144 |
| André Vivas | 81993945 |
| Leo Quirino | 44232914 |
| Adriane Möbbs | 55090440 |
| Matheus van der Ham | 82063965 |
| Matheus Saar | 82024913 |
| Equipe IAutomate | 194479496 |
| Suporte Caroline | 82160391 |

Confirmar se a pessoa ainda está na função antes de atribuir (a equipe muda).

## Manter o padrão vivo

Ao fim de cada lançamento, recalcular a tabela com as datas reais: para cada subtarefa concluída, o dia mais cedo entre o prazo e a conclusão, medido em dias desde a captação (se ficou entre D-30 e D-18 do evento) ou desde o evento. Acrescentar as tarefas novas que surgiram, com `origem` dizendo de qual lançamento vieram.

## Reaproveitar criativos de edição anterior (Keila, 10/11/2026)

- Ao copiar criativos de uma edição anterior, trocar só o que está **datado** (data, dia da semana, "pela primeira vez", "em setembro"). Erros pequenos de legenda não justificam reeditar vídeo.
- **Nome do evento nos vídeos:** a Masterclass em Preenchimento Labial já rodou com vídeos falando "imersão avançada" e página dizendo "Masterclass". Isso não é problema: os vídeos podem rodar assim. Nos estáticos e nas copys, usar o nome atual do evento.
- Copys adaptadas podem ir sem a revisão da Adriane quando não há tempo (decisão da Keila): aplicar a regra de escrita FEA ("para" por extenso, sem travessão) antes de liberar.

## Planilha de disparos (Keila, 11/11/2026)

A planilha "Disparos - João Pithon .xlsx" (aba do mês) é montada pela equipe. O Claude não inclui, apaga nem muda status de linhas nela sem pedido explícito da Keila ("volta como estava antes, estava tudo ok"). Se achar erro ou falta, só reportar.
