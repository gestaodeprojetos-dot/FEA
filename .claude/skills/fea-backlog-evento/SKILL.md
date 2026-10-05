---
name: fea-backlog-evento
description: Monta a estrutura operacional de um novo evento ou produto FEA (Dr. João Pithon) a partir de um evento modelo - pastas no Drive, documentos padrão de copy/design/tráfego, planilha de links úteis preenchida, planilha de criativos para tráfego, backlog no ClickUp com responsável (sem datas e sem comentários soltos) e um comentário em cada tarefa com o link da pasta para salvar e o link da copy para desenvolver. Usar quando a Keila pedir para "criar o backlog do próximo evento", "modelar pelo lançamento anterior", "replicar a estrutura de X para Y", "montar pastas, planilhas e ClickUp" de um ebook, perpétuo, masterclass, imersão ou versão LATAM.
---

# FEA: backlog completo de novo evento

Replica a operação de um evento modelo (Drive + ClickUp) para um evento novo, deixando cada pessoa do time com tarefa, pasta e copy no lugar certo. Primeira execução: Ebook Olheiras LATAM (05/10/2026), modelado no Ebook Olheiras [Perpétuo] Brasil. Exemplo completo de configuração em `FEA-config-ebook-olheiras-latam.json`.

Critério de sucesso (conferir item por item antes de entregar): toda subpasta do modelo existe no destino; todo documento de copy citado no backlog existe e está linkado; as duas planilhas estão no Drive; toda tarefa folha do ClickUp tem responsável (ou está listada como pendente de decisão), não tem data e tem exatamente 1 comentário com pasta + copy.

## Entradas (pedir só o que faltar)

| Entrada | Exemplo |
|---|---|
| Drive modelo | pasta do evento anterior |
| Drive destino | pasta do evento novo (pode já ter as pastas 0 a 7) |
| ClickUp modelo | URL `app.clickup.com/<workspace>/v/f/<folder_id>/<space_id>` |
| ClickUp destino | idem; o `<folder_id>` é o número depois de `/v/f/` |
| Nome do evento | "Ebook Olheiras LATAM" |

Workspace FEA no ClickUp: `9013080622` (há outro workspace na conta, sempre passar `workspace_id`).

## Regras fixas

- **Sem datas** no backlog (pedido explícito da Keila para este fluxo; é a exceção registrada à regra de ouro do ClickUp). Datas entram depois, no sprint.
- **Sem comentários** além do comentário padrão de 2 linhas. Formato exato:
  ```
  📁 **Pasta para salvar:** [nome da pasta](url)
  📝 **Copy para desenvolver a demanda:** [nome do doc](url)
  ```
  Para tarefas que não são de copy, o segundo link aponta para o documento de referência da demanda (briefing, planilha de tráfego, doc de automação).
- **Só responsável**: manter o responsável do modelo para a mesma função. Nunca inventar responsável; tarefa sem dono óbvio fica sem e entra na lista de pendências do relatório.
- **Nunca apagar** tarefa, pasta ou arquivo que já exista no destino. Se o destino já tiver backlog (cópia de outro template), complementar com o que falta do modelo e listar no relatório o que parece fora de escopo.
- Nome de todo arquivo criado começa com `FEA-` (regra do CLAUDE.md). Docs do LATAM: `FEA-LATAM ...`.
- Copy do LATAM: espanhol neutro, tom médico-científico, linha vermelha FEA. Os docs criados são **estruturas** para o time escrever, não copy pronta.
- Nunca inventar preço, link de checkout, domínio ou URL de página: célula fica `pendente: <responsável>`.

## Passo a passo

### 1. Mapear (só leitura)
1. Drive modelo e destino: `search_files` com `parentId = '<id>'`, descendo 2 níveis. Anotar subpastas e documentos-chave (copys, briefings, legendas, listboss, planilhas).
2. Ler os docs-chave do modelo com `read_file_content` (briefing de criativos, edição de vídeo, legendas, listboss) para copiar a estrutura.
3. Planilha de links do modelo: procurar `title contains 'Links úteis'`. A aba do produto mostra as linhas padrão (Copys, Artes, Links).
4. ClickUp: `clickup_get_workspace_hierarchy` com os dois `space_ids` para achar as listas; `clickup_filter_tasks` com `folder_ids` e `include_closed: true` nos dois folders; `clickup_get_task` com `include: ["subtasks"]` nos pais (Copy, Design, Webdesigner, Gestão, Automação, Gestão de tráfego, Suporte/CS, Configurações).
5. Comparar demandas modelo × destino e listar as que faltam.

### 2. Drive: subpastas
Criar no destino só o que falta, espelhando o modelo (`create_file` com `contentMimeType: application/vnd.google-apps.folder`). Padrão usado:

| Pasta | Subpastas |
|---|---|
| 00. EDITÁVEL | (arquivos InDesign) |
| 1. COPY | 1. Páginas · 2. Criativos (listboss, grupo e comunicações ficam na raiz da pasta, como no modelo) |
| 2. ARTES | 1. Banner checkout · 2. Capas plataforma · 3. Capas grupo e formulários · Referências |
| 4. TRÁFEGO | BRUTOS · CRIATIVOS PRONTOS / 1. Vendas · 2. Remarketing |

### 3. Documentos padrão
Criar com `create_file`, `contentMimeType: text/html` (vira Google Doc). Cada doc tem: tabela com Demanda (nome exato da tarefa no ClickUp), Responsável, Quem usa depois, Pasta para salvar, Referência do modelo (link), Material base; depois Regras e Estrutura com seções vazias para escrever.

Conjunto padrão de um ebook/perpétuo: Página de vendas · Obrigado e pesquisa · Checkout personalizado · Criativos de vendas · Criativos de remarketing · Legendas · Listboss API · Listboss E-mail · Onboarding + grupo · Pesquisa e presente · Comunicações · Briefing de design · Briefing de criativos e edição de vídeo.

Atenção: o Drive MCP não edita o conteúdo de um doc depois de criado. Montar todos os links internos antes de criar; se errar, mandar para a lixeira (`trash_file`) e recriar.

### 4. Planilhas
1. Escrever o `FEA-config-<evento>.json` (modelo neste diretório) com os links de tudo que foi criado.
2. `python3 fea_planilhas_evento.py FEA-config-<evento>.json <scratchpad>` gera os dois xlsx (precisa de `pip install openpyxl`).
3. Planilha de tráfego: subir o xlsx em base64 (`create_file`, `contentMimeType` xlsx) na pasta 4. TRÁFEGO; vira Google Sheets com formatação e 2 abas.
4. Atualizar o link da planilha de tráfego no JSON e subir a planilha de links úteis na raiz do evento. Se o base64 ficar grande demais (acima de ~10 KB o risco de erro de transcrição sobe), subir como CSV (`contentMimeType: text/csv`): perde a cor, mantém as URLs clicáveis.

### 5. ClickUp
1. Criar as demandas que faltam como subtarefa do pai certo (`clickup_create_task` com `parent`), só nome e `assignees`, sem data.
2. Comentar cada tarefa folha (`clickup_create_task_comment`) no formato fixo. Mapa padrão:

| Tipo de tarefa | Pasta para salvar | Copy / referência |
|---|---|---|
| Copy de página | 1. COPY / 1. Páginas | doc da página |
| Copy de criativo e legenda | 1. COPY / 2. Criativos | doc de criativos ou legendas |
| Listboss, grupo, pesquisa, comunicações | 1. COPY | doc correspondente |
| Arte de checkout | 2. ARTES / 1. Banner checkout | copy de checkout |
| Capas (grupo, formulário, pesquisa) | 2. ARTES / 3. Capas grupo e formulários | copy de onboarding ou de pesquisa |
| Banner área de membros | 2. ARTES / 2. Capas plataforma | briefing de design |
| Criativos (arte e vídeo) | 4. TRÁFEGO / CRIATIVOS PRONTOS / Vendas ou Remarketing | copy de criativos |
| Webdesigner | 1. COPY / 1. Páginas (+ link no ar vai para Links úteis) | doc da página |
| UTMs, pixels, links de checkout | planilha de Links úteis | planilha de tráfego ou copy de checkout |
| Automação | 6. AUTOMAÇÃO | listboss, onboarding ou doc de automação |
| Área de membros, tradução de aulas | Aulas traduzidas / 7. PDF | inventário de vídeos, PDF |
| Pesquisa de mercado | 3. PESQUISA | briefing |
| Estratégia, oferta, configurações | 0. PLANEJAMENTO | briefing |

Não comentar tarefas-pai que só agrupam (Copy, Design, Webdesigner, Gestão, Automação, Estratégia, Operação) nem tarefas já concluídas.

### 6. Relatório para a Keila
Português, tabela com o que foi criado (links), lista de pendências que só ela decide (tarefas sem responsável, duplicadas, fora de escopo, links que dependem de publicação) e o veredito do critério de sucesso.

## Erros comuns

| Erro | Como evitar |
|---|---|
| `Multiple workspaces available` no ClickUp | sempre passar `workspace_id: 9013080622` |
| Base64 inválido ao subir xlsx | xlsx pequeno ou CSV; gerar e copiar direto da saída do `base64 -w0` |
| Link placeholder dentro de doc | doc não é editável pelo MCP: criar na ordem de dependência (copys antes dos briefings) |
| Planilha de links do modelo vem sem URL no `read_file_content` (só rótulo) | usar a planilha Google "Links úteis \| Perpétuo", que expõe as URLs; xlsx perde hyperlink na leitura |
| Backlog destino já criado a partir de template de webinário | não apagar; listar no relatório tarefas de Hotwebinar e afins para a Keila decidir |
