# Gestão de projetos e ClickUp

## Regra de ouro do ClickUp

**Toda tarefa criada no ClickUp precisa ter data de início e data de vencimento antes de ser criada.** Se faltar vencimento, perguntar antes de criar, nunca assumir data arbitrária. Data de início default é hoje, a menos que o contexto peça outra coisa. Exceção: só pular essa exigência se a Keila pedir explicitamente "cria sem data".

Se `start_date` conflitar com `due_date` no passado (o ClickUp bloqueia isso sem o ClickApp "Duration" ativo): parar e perguntar como proceder, não mexer em configuração de workspace por conta própria se for só teste.

## Padrão para criar backlog de novo lançamento (replicável)

Quando pedido para montar do zero a estrutura de um novo lançamento no ClickUp espelhando um lançamento anterior:

1. **Backlog e sprints no ClickUp:** mesma estrutura de tarefas-mãe e subtarefas do modelo anterior, com datas obrigatórias (início e fim), sem alocar responsáveis na fase de validação, sem inventar informação. Se faltar dado, perguntar antes de assumir.
2. **Planilha de links úteis** (Google Sheets) espelhando o modelo anterior, por setor (tráfego, web, criativos, automação), com UTMs copiados do evento anterior.
3. **Pasta no Google Drive** espelhando a estrutura padrão de lançamento, com doc de briefing preenchido e guia com QR central.
4. Depois de criar a v1, esperar o pedido de "v2 melhorada": mesmas demandas, extras que gestão de projetos sênior julgar necessários, dependências entre tarefas e melhoria visual da planilha.
5. Nome da pasta é o nome do evento. Colunas do backlog: manter "Data de Início" sempre preenchida, adicionar "Comentários", remover "Prioridade".

Existe também o modo **migração** (não criação do zero): pegar demandas de um backlog origem e replicar num backlog destino, removendo datas e comentários.

## Ronda automática de prazos (padrão replicável para qualquer workspace ClickUp)

Sistema que roda por fora das Automações nativas do ClickUp, para contornar a trava do plano Free (5 automações ativas, 100 ações por mês, Conditions só a partir do Business).

**Lógica:**
- Tarefa vencida (due_date no passado), não concluída (status fora de feito/complete) e ainda não marcada como "atrasado": mudar status para `atrasado` e postar comentário fixo de cobrança.
- Tarefa a X dias do vencimento (parametrizável, ajustar por acordo com o time) e não concluída: postar comentário de check-in preventivo.
- Token de API lido de `.env`, nunca hardcoded no script.
- Agendar via Task Scheduler (Windows) em horário fixo, por exemplo 8h.

**Limitação conhecida:** sem controle de "já enviado hoje", rodar mais de 1 vez por dia pode duplicar comentário. Rodando 1 vez por dia via scheduler não é problema.

**A API pública do ClickUp não cria Automações nativas** (só webhooks). Automações visuais (regras "quando X então Y" na interface) só se configuram pela web.

**Específico FEA:** a ronda roda diariamente no workspace FEA seguindo esse mesmo padrão. Antes de expandir listas monitoradas ou tocar em configuração de automação, confirmar com a Keila. Mensagens de cobrança seguem a regra de escrita FEA (nunca "pra", sempre "para").

## Mapeamento e documentação de processos (SOP)

Quando pedido para documentar um processo de negócio, seguir a estrutura de `template-sop.md`:

1. Fluxograma em texto (início, etapas, decisões condicionais, checkpoints, fim, com dependências externas nomeadas).
2. SOP completo (versão, datas, responsável, frequência, tempo total, objetivo, escopo, pré-requisitos, responsáveis, passo a passo com tempo e ferramenta por etapa, checkpoints a cada 3 a 5 etapas).
3. Erros comuns e soluções, mínimo 5.
4. Checklist rápido de 1 página.
5. Métricas do processo.

Técnicas avançadas quando o processo envolver múltiplas pessoas ou áreas: **Swimlane** (raias por responsável) e **SIPOC** (Suppliers, Inputs, Process, Outputs, Customers) para processos complexos.
