---
name: fea-operacao-lancamentos
description: Manual de operação dos lançamentos FEA feito pelo Claude para a Keila. Traduz os comandos curtos dela ("ajusta tudo", "testa pra mim", "aloca pro Léo", "faz o mesmo em MPL", "coloca na planilha", "monta uma mensagem pra equipe") em passos concretos no ClickUp, no Drive, nas planilhas, nas páginas e nas copys. Usar sempre que a Keila mandar briefing de lançamento ou evento, pedir para montar, testar, conferir, alocar, registrar link, preparar doc para automação, adaptar copy ou criativo de edição anterior, ou perguntar "como estamos" / "o que falta".
---

# FEA: operação de lançamentos (ClickUp, Drive, páginas, copys e criativos)

Esta skill junta o jeito de trabalhar que a Keila ensinou na prática. Ela opera vários lançamentos ao mesmo tempo e manda pedidos curtos, muitas vezes por áudio transcrito. O Claude executa tudo o que der sem perguntar e só pergunta o que só ela sabe.

Skills irmãs, que esta chama:
- `fea-distribuir-datas`: datas, sprints, estrutura de pasta e responsáveis.
- `fea-clickup-ronda`: ronda 7h52, 11h52 e 16h52, cobrança, conferência, status das tarefas-mãe.
- `fea-edicao-reels` e `fea-revisao-reels`: edição de vídeo de caso clínico.

O `CLAUDE.md` do repositório continua valendo inteiro (tom, linha vermelha, "para" e nunca "pra", sem travessão, prefixo FEA).

## 1. Dicionário dos comandos da Keila

| Ela diz | Eu faço |
|---|---|
| "esse é o briefing" / manda link de briefing (artifact, doc) | Ler o briefing inteiro e **montar o lançamento** (seção 3). Antes, conferir se já existe pasta no ClickUp ou Drive com o nome (outra conversa pode ter começado). |
| "ajusta tudo pra nós" | Montar o lançamento completo e adaptar o material da edição anterior (copys, criativos, páginas pedidas ao André, doc da automação). |
| "me envia o link" / "link do ClickUp, Drive, planilha" | Responder só com os links, um por linha, com nome. |
| "como estamos?" / "o que falta?" / "geral" | Status por lançamento em tabela (pronto ✅, falta ⚠️, travado 🔴), depois "o que depende de você" e "o que está com a equipe", fechando com a prioridade recomendada. Ver seção 9. |
| "testa pra mim" (página) | Teste de ponta a ponta: cadastro, redirecionamento, pesquisa, planilha de respostas, botão do grupo (seção 6). |
| "testa o link" | `curl -sL -A "Mozilla/5.0 Chrome/128" -w "%{url_effective}"` e dizer para onde leva; WhatsApp: ler o `og:title` do grupo. |
| "coloca na planilha" / mandou material | Registrar na **planilha de links úteis** do lançamento, aba certa, na hora (seção 5). Se já estiver lá, dizer que já está e não duplicar. |
| "aloca pro Léo" / "aloca tudo pra X" | Atribuir as tarefas, colocar na descrição os links das copys e a linha `Pasta para salvar:` (ESTÁTICOS e raiz da fase), comentar marcando a pessoa. |
| "faz o mesmo em MPL" | Repetir exatamente o último fluxo no outro lançamento, conferindo os dados próprios dele (data, Zoom, grupo, arte). |
| "cria uma mensagenzinha" / "monta uma mensagem pra equipe" | Texto pronto para WhatsApp entre `---`, com emoji moderado, negrito em datas, links completos, assinatura com 💜 ou 🚀. Nunca colocar na mensagem o que ainda está em aberto. |
| "coloca o doc na tarefa da automação" | Doc na descrição da tarefa com resumo dos campos e "comentar entregue", comentário marcando a Equipe IAutomate, link da tarefa e mensagem pronta. |
| "volta como estava" | Restaurar do backup que eu sempre salvo antes de editar (conferir antes que ninguém editou depois de mim) e registrar a regra na skill. |
| "segue padrão sempre" / "regra no ClickUp" | Aplicar agora em todos os lançamentos ativos e **gravar a regra na skill certa** com a data e a frase dela. |

Se a mensagem é ambígua e a escolha muda o resultado (por exemplo, qual link é de qual evento), perguntar **uma** pergunta só. Nunca concluir pela ordem das mensagens: conferir contra o que está registrado nas planilhas e no Drive antes de trocar algo.

## 2. Mapa fixo

**ClickUp** (workspace `9013080622`; espaços Marketing Brasil `90130517360` e Marketing Latam `901314001225`). Token da API REST em `/root/.fea_clickup_token` (é da Gabriela: nunca mostrar, nunca commitar). Comentários pelo conector MCP saem com a conta da Keila, sempre com o prefixo `🤖 Claude:`.

| Pessoa | Papel | ID |
|---|---|---|
| Keila | gestora, decide e marca feito | 99934269 |
| Gabriela Borges | assistente de projetos; **Zoom das lives desde 16/11/2026** (criar sala, link e conferir no dia) | 118026144 |
| Adriane Möbbs (Adri/Dri) | copy | 55090440 |
| Matheus van der Ham | copy (par da Adri) | 82063965 |
| Leo Quirino | design, criativos | 44232914 |
| André Vivas | páginas e redirecionamentos (WordPress/Elementor) | 81993945 |
| Equipe IAutomate (Júlio Couto) | automação, Send Flow, Active, webhooks | 194479496 |
| Matheus Saar | tráfego, UTMs, campanhas | 82024913 |
| Graziele | suporte (o Zoom passou para a Gabi em 16/11/2026) | 44313083 |

**Drive:** lançamentos de 2026 em `18ZDI9-zJwkiO7eCPyjJ-Og6gv5hLCFYH` (pastas numeradas: `8. MASTERCLASS INTERCORRÊNCIAS 11/26`, `9. MASTERCLASS PREENCHIMENTO LABIAL 11/26`, `10. ELITE EXPERIENCE 12/26`).

**Planilhas compartilhadas da equipe:**
- Criativos para Tráfego `1Uj9doFiSNDTOn9z3weT83NdQHvEB-y3e` (aba do mês, uma linha por fase apontando para a pasta).
- **Criativos para Tráfego - Perpétuo** `1zIwANufWdM3PTTs_LNc-SWtlNxNBYShC19jjwEQyqeI` (Google Planilhas desde 25/11/2026; editar pela API do Sheets) (1. Gestão FEA / 14. Tráfego): é a planilha de tráfego de todo **perpétuo** (ebooks, CTX, CPX, PLX), abas `Perpétuo - BRASIL` e `Perpétuo - LATAM`, uma linha por campanha (Status, Campanha, Fase, Legenda, Link de Criativos, Páginas, Links Úteis). **Nunca criar planilha de tráfego separada para perpétuo** (Keila, 14/11/2026: "não é essa planilha, nada a ver"). Editar pela API do Sheets.
- Disparos - João Pithon `1GMOXAPAiPi8I1YBZIP3EC8Fii0lX-2wc`: **a equipe monta; eu não incluo, apago nem mudo status sem pedido explícito** (Keila, 11/11/2026). Erro ou falta: só reportar.
- Links de redirecionamento `1BRUUiY-mkjiMftOiF93G4shX1OpPemo2ScLgNL7fOsk`.

**Redirecionamentos conhecidos:** `joaopithon.com.br/aula-zoom` (sala da live em curso), `aula-zoom-2` (segunda live simultânea), `masterclass-grupo` e `masterclass-grupo-2` (grupo de WhatsApp). Quando duas masterclasses rodam juntas, cada uma usa o seu par (`-2` para a segunda).

## 3. Montar um lançamento a partir do briefing

Critério de sucesso: Drive, planilha de links, ClickUp com sprints e tarefas datadas e com responsável, **status do modelo FEA em todas as listas** (a fazer · fazendo · em revisão · em ajuste · atrasado · aprovado · pausado · sprint · feito; ver `fea-distribuir-datas`), Guia de Lançamento na pasta, tudo linkado entre si. Lançamento que substitui outro (ex.: Bio no lugar da Anatomia, 19/11/2026) passa pela mesma conferência: status e guia já faltaram uma vez.

1. **Conferir o que já existe** (ClickUp: pastas do espaço; Drive: busca pelo nome). Não duplicar.
2. **Drive** no padrão de lançamento (estrutura em `fea-distribuir-datas`), com `mkdir` de `scripts/fea_gdrive.py`. Em `4. TRÁFEGO/CRIATIVOS PRONTOS`, uma pasta por fase (1. CAPTAÇÃO, 2. ANTECIPAÇÃO, 3. LEMBRETE, 4. VENDAS e as demais do lançamento) e **ESTÁTICOS dentro de cada fase**.
3. **Planilha de links úteis** `Links úteis - <Lançamento>` na raiz, **como Google Planilhas nativa, nunca .xlsx** (regra abaixo, seção 5): copiar a do último lançamento já no padrão (MEI 11/26 `1NlNFbaVHU2Gy7gMo70QbnuHhOoVJguey`) convertendo para planilha Google, limpar a coluna B, preencher o que já existe e deixar em branco o resto. Só `Nome | Link`, sem "Fase". Aba TRÁFEGO tem células mescladas: pular `MergedCell` ao limpar.
4. **ClickUp:** uma pasta por lançamento; sprints semanais `Sprint N (dd/mm - dd/mm)`; tarefas-mãe por setor (Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego, e Comercial ou Produção do Evento quando houver); subtarefas com início 8h e prazo 18h. Status padrão FEA e visualização "Modelo de Sprint" em toda lista. Incluir as tarefas obrigatórias (planilha de respostas dos compradores, formulário de matrícula, cobrança das planilhas no Drive e **live patrocinada para o Matheus Saar em todo lançamento com live**, com lembrete no dia anterior; detalhes na skill `fea-distribuir-datas`).
5. **Responsáveis:** padrão por área (Copy → Adri + Matheus van der Ham; Design → Leo; Web → André; Automação → IAutomate; Tráfego → Matheus Saar). Gestão, Comercial, Produção de evento: perguntar à Keila. Nenhuma tarefa fica sem responsável.
6. **Briefing no padrão da equipe (Keila, 17/11/2026: "deixa só o que a gente usa").** Usar só os blocos que a equipe preenche nos briefings de verdade (base: Briefing MasterClass em Preenchimento Labial 07/26): Sobre o produto, Informações do lançamento, Bônus, Aula (só o nome de cada aula), Tráfego (verba, meta de leads, CPL, meta de venda e de faturamento) e Informações Extras quando houver conteúdo. Nunca incluir "Sobre o projeto" (objetivo, marcos, cronograma de entrega, cronograma de divulgação, métricas de sucesso, time), Big Idea, metas de engajamento ou de conversão, nem campo com ✏️ sem resposta. Não inventar campo novo.
7. **Guia de Informações** (doc do ClickUp na pasta): páginas Links úteis, Datas, Planilha com link dos setores.
8. Relatório: links, o que trava a data de abertura, o que depende dela, e oferecer incluir a pasta na ronda (a ronda só olha pasta nova com o ok dela).

Evento novo sem lançamento anterior parecido: montar a partir do briefing e dizer isso no relatório.

## 4. Adaptar material de edição anterior

- **Copys:** copiar do lançamento base, trocar datas pelo mesmo número de dias antes da live (marcar em amarelo), deixar preço e oferta antigos em azul até a oferta nova existir, aplicar "para", sem travessão. Conferir **cabeçalho de cada mensagem** (dia da semana, data, hora) contra o texto ("amanhã", "é hoje") e contra a planilha de disparos.
- **Criativos estáticos:** trocar só o datado (data, dia, "pela primeira vez"). Erro pequeno de legenda não justifica reeditar.
- **Quem faz o ajuste (Keila, 19/11/2026: "as trocas de datas e ajustes nos criativos você mesmo pode fazer; deixa com o Léo apenas criativos que ele precisa criar do zero"):** troca de data, dia da semana, número de alunos, preço e corte de fala datada em criativo reaproveitado é do Claude. O Leo só recebe tarefa de criativo novo, que não existe em edição anterior. Tarefa do Leo nunca leva lista de ajuste em peça pronta.
- **Criativos em vídeo de edição anterior:** trocar o cartão final pelo cartão atual da pasta (achar o início do cartão pela luminância), cortar falas datadas ou de mecânica antiga ("comente 0903", "comenta camada"), terminar em frase completa. Falar "imersão" pode. Conferir com OCR quadro a quadro e transcrição final antes de subir. Numerar a partir do maior `Ads N` da pasta.
- **Traduzir vídeo de anúncio para LATAM (Keila, 13/11/2026: "pegar o arquivo bruto, dublar e depois legendar"):** nunca dublar o editado com legenda em português gravada na imagem, porque cobrir a legenda deixa tarja. Caminho padrão:
  1. Achar os brutos no Drive do produto (`4. Tráfego / 1. CRIATIVOS / 1. Brutos ...`).
  2. Ligar cada editado ao bruto dele pela transcrição (faster-whisper).
  3. Remontar a mesma edição a partir do bruto, sem legenda, título nem cartão. Os cortes saem do casamento de quadros e palavras; os brutos MOV de câmera sem tag de rotação levam `transpose=1`; gravação de tela vai para 886x1920.
  4. Dublar no HeyGen (`precision`, Spanish).
  5. Transcrever o áudio dublado e aplicar o título traduzido e a legenda em espanhol.
  6. Anexar o cartão final em espanhol (3 s).

  Scripts de referência: `cutmap.py`, `segs.py`, `mkclean.py` e `build2.py` (pasta `olh_vid` do scratchpad da sessão do Ebook Olheiras LATAM).
- **Tarefa "Presente do ingresso" é da Automação (Equipe IAutomate), nunca do Suporte/CS** (Keila, 24/11/2026): fica sob a tarefa-mãe Automação da sprint, junto com a configuração do fluxo do ingresso. A Gestão só confirma qual é o presente.
- **Doc de informações do ingresso** (para a automação): evento, palavra-chave, arte do ingresso (link do arquivo, não da pasta), presente (link do vídeo; conferir título pelo oEmbed do YouTube), data com o dia da semana certo, link da aula (redirecionamento da live certa), início dos disparos, data de teste em dia útil.

## 5. Registrar material (planilha de links úteis)

Tudo o que a Keila ou a equipe manda (copy, arte, link de grupo, webhook, lista e tags do Active, planilha de respostas, Zoom, redirecionamento, checkout) vai na hora para a aba certa: GERAL, COPY, ARTES, WEB DESIGNER ou TRÁFEGO. Planilha Google: editar pela API do Sheets; planilha antiga em .xlsx: `editar_xlsx` (confere `modifiedTime` antes de subir), hiperlink com o nome do arquivo, nunca apagar linha. Linha com recado meu desatualizado: avisar, não sobrescrever sem ok.

**URA + SMS em todo lançamento com live (Keila, 25/11/2026: "seja mais rigoroso, tô deixando passar, todo lançamento me ajuda a lembrar").** Toda pasta de lançamento com live precisa das quatro tarefas, nesta ordem e com estes prazos (D = dia da live):
1. Copy de URA + SMS (Copy), até D-10. Conferir SMS com até 160 caracteres, data e horário certos e "para" por extenso.
2. Atualizar cronograma de URA + SMS e pedir o áudio da URA (Gestão), até D-7. Áudio do Dr. João gravado ou montado de áudios existentes, salvo em `7. URA + SMS` e na planilha de links úteis.
3. Conferir créditos da Ligue Lead e agendar URA + SMS (Gestão), até D-3, só depois da copy e do áudio prontos, com SMS de teste enviado para os números do doc.
4. Conferir os envios no dia e pedir os reports para a Ligue Lead (Gestão), D0 e D+1.
Na montagem do lançamento, criar as quatro se faltarem e conferir que a ordem das datas faz sentido (agendar nunca antes da copy). Na ronda das 7h52, para todo lançamento com live nos próximos 14 dias, o relatório traz uma linha "URA + SMS" com o status das quatro etapas, e qualquer etapa que vence hoje, amanhã ou já venceu entra também no aviso do celular.

**Planilha nova é sempre Google Planilhas nativa, nunca arquivo .xlsx (Keila, 24/11/2026: "não quero que você crie as planilhas arquivo .xlsx... para todo mundo conseguir mexer").** Toda planilha que eu criar para um lançamento (links úteis, tráfego, controle, respostas, qualquer outra) nasce como Google Planilhas (`application/vnd.google-apps.spreadsheet`): copiar o modelo com `files.copy` passando `mimeType` de planilha Google, ou subir com conversão. Nome sem extensão (`Links úteis - <Lançamento>`). Para editar uma planilha Google, usar a API do Google Sheets (`values.update`, `batchUpdate`), nunca baixar como .xlsx e subir por cima. As planilhas antigas que já são .xlsx (Criativos para Tráfego, Disparos, links úteis de lançamentos já criados) continuam como estão: não converter nem trocar o arquivo sem pedido da Keila, porque o ID e os links da equipe dependem delas.

**Planilha de links úteis sempre completa (Keila, 16/11/2026: "precisam ter todas as informações certinhas, vi que você não está preenchendo tudo").** Ao montar ou adaptar um lançamento, varrer o Drive inteiro do lançamento e preencher toda linha cujo material já exista. **O que ainda não existe fica em branco** (Keila, 19/11/2026: "não precisa ficar colocando na frente a criar, a gente sabe que tem que criar, só deixa em branco"): nada de "(a criar...)", "(a confirmar...)" ou observação na célula. Do lançamento anterior entra só o Drive anterior, para referência, na primeira linha da GERAL. Modelo de layout: Links úteis do MTB 11/26 (abas GERAL, COPY, ARTES, WEB DESIGNER, TRÁFEGO, CPL). Conferir de novo a cada entrega.

**Planilha de tráfego sempre atualizada (Keila, 16/11/2026: "SEMPRE atualiza a planilha de tráfego").** Todo lançamento ou perpétuo com criativo pronto entra na planilha compartilhada Criativos para Tráfego (perpétuo na Criativos para Tráfego - Perpétuo), na aba do mês da fase: uma linha por fase com status, data, link da legenda, link da pasta da fase e a planilha de links úteis na primeira linha. Se a aba do mês não existir, criar no padrão da anterior (edição do XML, `zip -X -D`). Criativo novo, pasta trocada ou data mudada: atualizar na mesma hora, sem esperar pedido. **Formato da linha (Keila, 19/11/2026: "tá tudo desconfigurada"):** status só com os valores da lista suspensa (Criar copy ✍️, Revisar 👀, Corrigir 🚫, Agendar 📅, Agendado 👍, Publicado ✅), nunca texto livre ou observação na célula (pendência vai para o ClickUp ou para o relatório); célula de status e de campanha dentro da validação de lista; linha com `outlineLevel="1"` como as demais; campanha mesclada em B:C (`mergeCell` Bn:Cn) como as linhas padrão; nome da campanha incluído na lista suspensa da aba; **o lançamento inteiro fica na aba do mês do evento, num bloco só: todas as fases juntas logo abaixo do dia em que a captação começa, cada uma com o próprio Deadline (nunca espalhar fase por dia; Keila, 19/11/2026: "está toda espaçada, não fazemos isso")**, mesmo com a captação começando no fim do mês anterior (a aba abre com o dia da captação; Keila, 19/11/2026: "pode deixar na aba de dezembro... para não ficar tudo separado"); lançamento cancelado sai da planilha para não confundir o gestor de tráfego; aba nova monta a partir da aba do mês anterior (cabeçalho, dias com fórmula `=An+1` mesclados A:G, linhas até 1008), nunca com linhas soltas; coluna H com estilo da linha padrão (link de links úteis só na linha de captação).

**Descrição de tarefa enxuta (Keila, 23/11/2026: "não preciso de todo esse detalhe").** A descrição leva só três linhas: `Briefing:` (link do briefing do lançamento), `Referência:` (a peça ou pasta específica do lançamento anterior, quando houver) e `Pasta para salvar:` com a **subpasta exata da entrega**, nunca a pasta geral. Ingresso vai em `2. ARTES > 6. INGRESSO`, capa do grupo em `2. ARTES > 1. WHATSAPP`, imagens de API em `2. ARTES > 1. WHATSAPP > IMAGENS API`, capa de formulário em `5. FORMS`, slides em `7. SLIDES`, QR code em `8. QR CODE`, estáticos de tráfego em `4. TRÁFEGO > CRIATIVOS PRONTOS > <fase> > ESTÁTICOS`, copy em `1. COPY > <subpasta>`, link (UTM, webhook, página, Zoom, grupo) na aba certa da planilha de links úteis. Nada de "espelhado da tarefa X", datas a confirmar, Drive geral ou parágrafo de contexto. Tarefa sem entrega em arquivo leva só o briefing.

**Toda tarefa nova é subtarefa da mãe da área na sprint dela (Keila, 19/11/2026: "cadê a tarefa mãe? não pode acontecer isso").** Ao criar tarefa (inclusive avulsa, urgente ou de outra conversa), passar `parent` com a mãe da área (Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego, Suporte/CS, Operação do dia) da mesma lista. Se a sprint não tem a mãe daquela área, criar a mãe primeiro (nome da área, descrição padrão do lançamento, início e fim da sprint, sem responsável) e depois a subtarefa. Nunca deixar tarefa solta no topo da lista.

**Onde salvar no Drive do lançamento (Keila, 19/11/2026):** imagens de API vão em `2. ARTES / 1. WHATSAPP / IMAGENS API`; brutos e criativos de tráfego (inclusive cópias de edições anteriores) vão em `4. TRÁFEGO` (`BRUTOS` ou `CRIATIVOS PRONTOS`), nunca soltos em `2. ARTES`.

**Criativo que não pode ir para o ar fica fora da pasta de criativos (Keila, 16/11/2026).** Original com data antiga (depois de adaptado) e criativo com preço que não vale na edição saem de CRIATIVOS PRONTOS e vão para `4. TRÁFEGO/BRUTOS/FORA DO TRÁFEGO (não usar nos anúncios)`. Não apagar e não deixar pasta "NÃO USAR" dentro da pasta de criativos: na pasta de criativos só fica o que o tráfego pode subir.

**Dar check no que o Claude fez (Keila, 16/11/2026).** Tarefa do ClickUp cuja entrega o próprio Claude fez e que está comprovada no Drive (ex.: adaptação de criativos de edição anterior) vai para `feito` com comentário da evidência. Entrega da equipe continua na regra da ronda (`aprovado`, e `feito` só pela Keila); copy e conteúdo continuam esperando o ok dela.

## 6. Testar página e fluxo (ponta a ponta)

1. `curl` da página: HTTP 200, data e dia da semana certos, formulário presente.
2. Playwright (`require('playwright')`, `waitUntil:'load'`, nunca `networkidle`): preencher captura com "TESTE CLAUDE APAGAR" e e-mail `teste-claude-<sigla>@joaopithon.com.br`, UTMs de teste; conferir redirecionamento para a pesquisa levando e-mail, telefone e UTMs; preencher a pesquisa em etapas; mensagem de sucesso; botão do grupo visível e apontando para o grupo certo.
3. Planilha de respostas (export CSV): a linha de teste chegou com as UTMs.
4. Grupo: abrir o link do Send Flow e ler o `og:title` do WhatsApp.
5. Aprovar a tarefa da página no ClickUp com o que foi conferido e avisar que a linha de teste pode ser apagada.

## 7. ClickUp: regras de status

- `feito` é só a Keila. Eu uso `aprovado` para entrega conferida.
- Tarefa-mãe vai para `fazendo` quando qualquer subtarefa do setor andou (`scripts/fea_status_maes.py`).
- Arte entregue na pasta com a tarefa ainda em "a fazer": conferir a arte e aprovar com comentário.
- Duas tarefas iguais: não apagar; perguntar se junta (`clickup_merge_tasks`).
- Nunca apagar tarefa, lista, comentário; nunca mexer em permissão ou automação nativa.

## 8. Armadilhas já vividas

- **Informação nova de uma demanda que já existe: atualizar a tarefa existente, nunca criar outra** (Keila, 18/11/2026). Em 18/11 criei uma tarefa nova para o Leo com o que o Luca mandou no grupo Copy e deixei a antiga aberta: ele ficou com três tarefas do mesmo slide. Regra: uma demanda, uma tarefa. Reescrever a descrição da tarefa que a pessoa já tem (com tudo, inclusive o que mudou), ajustar nome e prazo, comentar atribuído ao responsável o que mudou. Se já existir duplicada, juntar tudo numa só e arquivar as outras com comentário apontando para a que ficou.

- **Nunca mover planilha** (Keila, 14/11/2026), de nenhum time e por nenhum motivo, nem pedir a alguém que mova: pode quebrar integrações (formulário, webhook, Listboss, automações). Planilha fora do Drive da empresa vai para a tarefa da Gabi de cobrar os times, e o time dono decide como resolver. Planilha nova nasce dentro da pasta do lançamento no Drive da empresa.

- `python3 - <<'EOF' </dev/null` não roda nada: o `</dev/null` substitui o heredoc. Usar arquivo `.py` e `python3 arquivo.py </dev/null`.
- `cat > /dev/null` sem entrada trava o comando.
- Docs API dá 403 com esta chave: editar Google Doc por ida e volta em `.docx` (`trocar_texto_doc`), e cada ida e volta **duplica comentários abertos** (fechar as cópias).
- Nomes do Drive podem vir em NFD: normalizar com `unicodedata.normalize('NFC', ...)`.
- Planilha nova: sempre Google Planilhas nativa. `.xlsx` antigo aberto no Google Planilhas pode gerar uma cópia Google com o mesmo nome: perguntar à Keila qual fica antes de mexer, porque a equipe pode já estar usando a cópia.
- Planilha editada por outra pessoa enquanto eu edito: sempre conferir `modifiedTime` antes de subir e guardar backup.
- Link de Zoom: confirmar com a planilha de links do lançamento de qual evento é a sala antes de trocar qualquer coisa; nunca deduzir pela ordem das mensagens.
- Vídeo do Drive grande: baixar em blocos para o scratchpad; subir com upload resumível (`fea_drive.subir`).

## 8b. Guia de padrões para os outros Claudes (Keila, 19/11/2026)

O Claude do WhatsApp e outras conversas também mexem no ClickUp, Drive e planilhas e não conhecem estas skills ("essa bagunça porque o Claude do WhatsApp começou a organizar tudo e ele não sabe o padrão"). O resumo dos padrões fica em `FEA-gestao-clickup/FEA-padroes-operacao-equipe.md`, publicado no Google Doc `1NkbIawRhO-oWpVTz-6o1JImPcU_cKHFZzM7QliDDhLQ` (pasta de lançamentos 2026). **Toda regra nova gravada numa skill entra também nesse arquivo e no Doc, no mesmo dia** (reenviar o .md por `files/{id}` PATCH com upload `text/markdown`, que regrava o Doc).

## 9. Formato das respostas para a Keila

- Português, sem preâmbulo, sem travessão, "para" sempre.
- Primeiro a resposta ("Sim, liberado" / "Não, falta X"), depois tabela, depois "o que depende de você" e "o que está com a equipe".
- Links do ClickUp como `[nome da tarefa](url)`, nunca URL solta.
- Admitir erro na hora, com o que foi corrigido.
- Nunca afirmar algo que não conferi (campanha no ar, sala de Zoom, quem editou): dizer de onde veio a informação.
