# FEA · Padrões de operação de lançamentos (para todo Claude que mexe no ClickUp, Drive e planilhas)

Versão de 24/11/2026. Fonte: regras que a Keila definiu e que o Claude Code segue (skills `fea-operacao-lancamentos`, `fea-distribuir-datas` e `fea-clickup-ronda`). Quando houver dúvida entre este documento e o que já está feito, **copiar o padrão de um lançamento recente que está certo** (modelo atual: FEA-MTB 11/26) em vez de inventar.

## 0. Regras de ouro

1. **Antes de criar qualquer coisa, procurar se já existe** (ClickUp, Drive, planilha). Uma demanda, uma tarefa. Informação nova de demanda que já existe atualiza a tarefa existente, nunca cria outra.
2. **Copiar o padrão, não inventar.** Pasta, planilha, status e nomes seguem o último lançamento certo. Nada de pasta, aba, coluna ou status novo.
3. **Nunca apagar** tarefa, lista, comentário ou linha de planilha. Nunca mexer em permissão, automação nativa ou configuração do workspace. Nunca **mover planilha** (quebra formulário, webhook e automação).
4. **Nunca marcar `feito`** no ClickUp sem a Keila mandar. Entrega conferida vai para `aprovado` ou `em revisão`.
5. Escrita: sempre "para", nunca "pra"; sem travessão (em-dash); português.
6. Ao terminar, avisar a Keila do que foi feito, com links. Se algo ficou fora do padrão, dizer.

## 1. ClickUp

**Estrutura de um lançamento:** uma pasta por lançamento no espaço Marketing Brasil ou Marketing Latam, com mês e ano no nome (ex.: `Masterclass Bioestimuladores 12/26`). Dentro: lista `Backlog` e sprints semanais `Sprint N (dd/mm - dd/mm)`.

**Status (modelo FEA, em todas as listas):** a fazer · fazendo · em revisão · em ajuste · atrasado · aprovado · pausado · sprint · feito. Pasta ou lista com outros status (brifado, revisao, ajustar, complete) está errada: corrigir para o modelo FEA.

**Tarefas-mãe por área em cada sprint:** Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego, Suporte/CS, Operação do dia. Datas da mãe: início e fim da sprint, sem responsável.

**Toda tarefa é subtarefa da mãe da área, na sprint certa.** Nunca deixar tarefa solta no topo da lista. Se a sprint não tem a mãe daquela área, criar a mãe primeiro e depois a subtarefa.

**Toda subtarefa precisa de:** data de início (8h) e prazo (18h), responsável e descrição **enxuta**, só com três linhas: `Briefing:` (link), `Referência:` (peça ou pasta específica do lançamento anterior, se houver) e `Pasta para salvar:` com a **subpasta exata** da entrega, nunca a pasta geral (ingresso em 2. ARTES > 6. INGRESSO, capa do grupo em 2. ARTES > 1. WHATSAPP, imagens de API em 1. WHATSAPP > IMAGENS API, capa de formulário em 5. FORMS, estáticos em 4. TRÁFEGO > CRIATIVOS PRONTOS > fase > ESTÁTICOS, links na aba certa da planilha de links úteis). Nada de parágrafo de contexto, "espelhado de", datas a confirmar ou Drive geral.

**Responsáveis padrão:** Copy: Adriane Möbbs e Matheus van der Ham · Design: Leo Quirino (só criativo novo, criado do zero; ajuste de data em criativo reaproveitado é do Claude) · Páginas e redirecionamentos: André Vivas · Automação: Equipe IAutomate · Tráfego e UTMs: Matheus Saar · Zoom das lives: Gabriela Borges · Gestão: Gabriela Borges ou Keila (perguntar).

**Tarefas obrigatórias em todo lançamento:** planilha de respostas dos compradores no Drive (Automação), formulário de matrícula (Automação), cobrar as planilhas dentro do Drive da empresa (Gabi), e **Live patrocinada para o Matheus Saar em todo lançamento com live**, com lembrete no dia anterior.

**Guia de Lançamento:** todo lançamento tem, dentro da pasta do ClickUp, o doc `Guia de Lançamento` com: Drive, Links úteis, Briefing, Planilha de criativos para tráfego (aba do mês), as DATAS (captação, evento, carrinho) e o QR code para abrir no celular. Modelo: o Guia de Lançamento do FEA-MTB 11/26.

**Comentários do Claude** começam com `🤖 Claude:`.

## 2. Drive do lançamento

Estrutura fixa (modelo: pasta do lançamento atual):

- `0. PLANEJAMENTO` (briefing)
- `1. COPY` com `1. PÁGINAS`, `2. CRIATIVOS`, `3. COMUNICAÇÃO` (API, WHATSAPP, EMAIL), `4. LEGENDAS`, `5. EVENTO`
- `2. ARTES` com `1. WHATSAPP` (capa do grupo e a subpasta `IMAGENS API`), `2. THUMB YOUTUBE`, `3. CAPAS`, `4. PERFIL`, `5. FORMS`, `6. INGRESSO`, `7. SLIDES`, `8. QR CODE`
- `3. PESQUISA`
- `4. TRÁFEGO` com `BRUTOS` e `CRIATIVOS PRONTOS` (uma pasta por fase: 1. CAPTAÇÃO, 2. ANTECIPAÇÃO, 3. LEMBRETE, 4. VENDAS, 5. VENDAS RMK; dentro de cada fase a pasta `ESTÁTICOS`; vídeos ficam na raiz da fase)
- `5. LOGO`, `6. PÁGINA DE VENDAS`, `7. URA + SMS`, `8. AUTOMAÇÃO`
- Planilha `Links úteis - <lançamento>` na raiz, em Google Planilhas (nunca .xlsx)

**Onde salvar cada coisa:**
- Criativos de tráfego prontos: `4. TRÁFEGO / CRIATIVOS PRONTOS / <fase>` (estáticos em ESTÁTICOS). **Nunca em 2. ARTES.**
- Brutos, originais de edição anterior e cópias: `4. TRÁFEGO / BRUTOS`.
- Criativo que não pode ir ao ar (data antiga, preço que não vale): `4. TRÁFEGO / BRUTOS / FORA DO TRÁFEGO (não usar nos anúncios)`. Na pasta de criativos prontos só fica o que o tráfego pode subir.
- Imagens de API: `2. ARTES / 1. WHATSAPP / IMAGENS API`.
- Nunca criar pasta solta fora dessa estrutura (ex.: "Captação · atualizadas", "BRUTOS" dentro de ARTES).

- **Presente do ingresso é tarefa da Automação (Equipe IAutomate), nunca do Suporte/CS** (Keila, 24/11/2026). A Gestão só confirma qual é o presente.

- **URA + SMS em todo lançamento com live** (Keila, 25/11/2026): copy até D-10, cronograma e áudio da URA até D-7, créditos da Ligue Lead e agendamento até D-3 (sempre depois da copy e do áudio, com SMS de teste), conferência dos envios e report em D0 e D+1. SMS com no máximo 160 caracteres.

## 3. Planilha de links úteis (uma por lançamento)

- **Toda planilha nova de lançamento é Google Planilhas nativa, nunca arquivo .xlsx** (Keila, 24/11/2026), para todo mundo conseguir editar no navegador. As planilhas antigas em .xlsx ficam como estão, sem converter nem trocar o arquivo.
- Modelo: `Links úteis` do FEA-MTB 11/26. Abas **GERAL, COPY, ARTES, WEB DESIGNER, TRÁFEGO, CPL**. Colunas só `Nome | Link`. Nome do produto (sigla) no A1 da GERAL. Linhas zebradas. Link sempre com o nome do arquivo como texto.
- **Do lançamento anterior entra só o Drive anterior, para referência** (primeira linha da GERAL). Nada de copy, checkout, planilha, lista ou observação do lançamento anterior.
- O que ainda não existe fica **em branco** (link do Zoom, coisas da automação, copy que falta). Nada de "(a criar...)" ou observação na célula.
- Todo material que chega (copy, arte, link de grupo, webhook, lista e tags do Active, Zoom, checkout) vai na hora para a aba certa.
- Sem observações longas dentro das células.

## 4. Planilha Criativos para Tráfego (compartilhada)

- Uma aba por mês (ex.: `Dezembro26`), montada a partir da aba do mês anterior: cabeçalho igual, uma faixa por dia (fórmula `=A anterior +1`, mesclada de A a G), linhas até o fim do mês.
- **O lançamento inteiro fica na aba do mês do evento, num bloco só**: todas as fases (Captação, Antecipação, Lembrete, Vendas, RMKT Vendas) juntas, logo abaixo do dia em que a captação começa, cada uma com o próprio Deadline. Nunca espalhar uma fase por dia. Se a captação começa no fim do mês anterior, a aba do mês do evento abre com esse dia.
- Status só com a lista suspensa: Criar copy ✍️ · Revisar 👀 · Corrigir 🚫 · Agendar 📅 · Agendado 👍 · Publicado ✅. Nunca texto livre ou observação na célula.
- Campanha nas colunas B e C mescladas, escolhida pela lista suspensa (`[BR] MBC - Masterclass em Bioestimuladores 12/26`).
- Colunas: Legenda (link da pasta de legendas), Link de Criativos (link da pasta da fase), Links Úteis (só na linha de captação).
- Lançamento cancelado sai da planilha para não confundir o gestor de tráfego.
- Planilha de perpétuo é outra (Criativos para Tráfego - Perpétuo). Planilha de Disparos é da equipe: não incluir, apagar nem mudar status sem pedido da Keila.

## 5. Criativos e copys de edição anterior

- Trocar só o que está datado: data, dia da semana, mês, número de alunos, "pela primeira vez". Conferir o dia da semana no calendário.
- Fala datada em vídeo ("teve Anvisa essa semana"): cortar o trecho, com a legenda junto.
- Marca comercial (ácido hialurônico, toxina, bioestimulador) só com aprovação da Keila ou do Luca.
- Nunca gerar imagem final com IA generativa.
- Copy: "para" por extenso, sem travessão, tom médico-científico.

## 6. Antes de dizer "pronto"

- [ ] Procurei se já existia antes de criar?
- [ ] Está na pasta, aba ou lista certa, com o nome no padrão?
- [ ] Tarefa com mãe, datas, responsável e descrição?
- [ ] Status no modelo FEA?
- [ ] Planilha de links úteis e de tráfego atualizadas, no formato padrão?
- [ ] Nada apagado, nada movido que não podia?
- [ ] Avisei a Keila com os links?
