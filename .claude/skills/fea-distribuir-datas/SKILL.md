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
   - Tarefa sem responsável: perguntar quem fica, nunca atribuir por palpite.
6. **Sprints**, quando ela pedir ou quando faltarem semanas até o evento:
   - Uma lista por semana, de segunda a sexta, criada com `clickup_create_list_in_folder`, seguindo o formato de nome que a pasta já usa. Exemplos: Brasil `Sprint 10 (19/10 - 25/10)`, Latam `Sprint 10 (11/2 - 11/6)`. A última sprint termina no evento.
   - O ClickUp não move subtarefa sozinha (o recurso "Subtasks in Multiple Lists" está desligado). Então eu crio as tarefas-mãe da área (Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego) na sprint de destino, com as datas da sprint, recrio as subtarefas com `task.create_many` (`parent_task_id`, responsável e datas) e **arquivo** as originais com `task.archive`. Arquivar dá para desfazer; apagar, nunca.
   - Antes de recriar, conferir se a original tem descrição, anexo ou checklist. Se tiver, copiar a descrição e avisar a Keila do anexo.
7. **Conferir** com `clickup_filter_tasks` nas listas mexidas: toda subtarefa aberta com prazo e responsável, nada esquecido na sprint antiga.

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
