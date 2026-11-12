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
| Gabriela Borges | assistente de projetos | 118026144 |
| Adriane Möbbs (Adri/Dri) | copy | 55090440 |
| Matheus van der Ham | copy (par da Adri) | 82063965 |
| Leo Quirino | design, criativos | 44232914 |
| André Vivas | páginas e redirecionamentos (WordPress/Elementor) | 81993945 |
| Equipe IAutomate (Júlio Couto) | automação, Send Flow, Active, webhooks | 194479496 |
| Matheus Saar | tráfego, UTMs, campanhas | 82024913 |
| Graziele | suporte, Zoom | 44313083 |

**Drive:** lançamentos de 2026 em `18ZDI9-zJwkiO7eCPyjJ-Og6gv5hLCFYH` (pastas numeradas: `8. MASTERCLASS INTERCORRÊNCIAS 11/26`, `9. MASTERCLASS PREENCHIMENTO LABIAL 11/26`, `10. ELITE EXPERIENCE 12/26`).

**Planilhas compartilhadas da equipe:**
- Criativos para Tráfego `1Uj9doFiSNDTOn9z3weT83NdQHvEB-y3e` (aba do mês, uma linha por fase apontando para a pasta).
- Disparos - João Pithon `1GMOXAPAiPi8I1YBZIP3EC8Fii0lX-2wc`: **a equipe monta; eu não incluo, apago nem mudo status sem pedido explícito** (Keila, 11/11/2026). Erro ou falta: só reportar.
- Links de redirecionamento `1BRUUiY-mkjiMftOiF93G4shX1OpPemo2ScLgNL7fOsk`.

**Redirecionamentos conhecidos:** `joaopithon.com.br/aula-zoom` (sala da live em curso), `aula-zoom-2` (segunda live simultânea), `masterclass-grupo` e `masterclass-grupo-2` (grupo de WhatsApp). Quando duas masterclasses rodam juntas, cada uma usa o seu par (`-2` para a segunda).

## 3. Montar um lançamento a partir do briefing

Critério de sucesso: Drive, planilha de links, ClickUp com sprints e tarefas datadas e com responsável, Guia de Informações, tudo linkado entre si.

1. **Conferir o que já existe** (ClickUp: pastas do espaço; Drive: busca pelo nome). Não duplicar.
2. **Drive** no padrão de lançamento (estrutura em `fea-distribuir-datas`), com `mkdir` de `scripts/fea_gdrive.py`. Em `4. TRÁFEGO/CRIATIVOS PRONTOS`, uma pasta por fase (1. CAPTAÇÃO, 2. ANTECIPAÇÃO, 3. LEMBRETE, 4. VENDAS e as demais do lançamento) e **ESTÁTICOS dentro de cada fase**.
3. **Planilha de links úteis** `Links úteis - <Lançamento>.xlsx` na raiz: copiar a do último lançamento já no padrão (MEI 11/26 `1NlNFbaVHU2Gy7gMo70QbnuHhOoVJguey`), limpar a coluna B, preencher o que já existe, marcar "(a criar)" no resto. Só `Nome | Link`, sem "Fase". Aba TRÁFEGO tem células mescladas: pular `MergedCell` ao limpar.
4. **ClickUp:** uma pasta por lançamento; sprints semanais `Sprint N (dd/mm - dd/mm)`; tarefas-mãe por setor (Gestão, Copy, Design, Webdesigner, Automação, Gestão de Tráfego, e Comercial ou Produção do Evento quando houver); subtarefas com início 8h e prazo 18h. Status padrão FEA e visualização "Modelo de Sprint" em toda lista. Incluir as tarefas obrigatórias (planilha de respostas dos compradores e formulário de matrícula).
5. **Responsáveis:** padrão por área (Copy → Adri + Matheus van der Ham; Design → Leo; Web → André; Automação → IAutomate; Tráfego → Matheus Saar). Gestão, Comercial, Produção de evento: perguntar à Keila. Nenhuma tarefa fica sem responsável.
6. **Guia de Informações** (doc do ClickUp na pasta): páginas Links úteis, Datas, Planilha com link dos setores.
7. Relatório: links, o que trava a data de abertura, o que depende dela, e oferecer incluir a pasta na ronda (a ronda só olha pasta nova com o ok dela).

Evento novo sem lançamento anterior parecido: montar a partir do briefing e dizer isso no relatório.

## 4. Adaptar material de edição anterior

- **Copys:** copiar do lançamento base, trocar datas pelo mesmo número de dias antes da live (marcar em amarelo), deixar preço e oferta antigos em azul até a oferta nova existir, aplicar "para", sem travessão. Conferir **cabeçalho de cada mensagem** (dia da semana, data, hora) contra o texto ("amanhã", "é hoje") e contra a planilha de disparos.
- **Criativos estáticos:** trocar só o datado (data, dia, "pela primeira vez"). Erro pequeno de legenda não justifica reeditar.
- **Criativos em vídeo de edição anterior:** trocar o cartão final pelo cartão atual da pasta (achar o início do cartão pela luminância), cortar falas datadas ou de mecânica antiga ("comente 0903", "comenta camada"), terminar em frase completa. Falar "imersão" pode. Conferir com OCR quadro a quadro e transcrição final antes de subir. Numerar a partir do maior `Ads N` da pasta.
- **Doc de informações do ingresso** (para a automação): evento, palavra-chave, arte do ingresso (link do arquivo, não da pasta), presente (link do vídeo; conferir título pelo oEmbed do YouTube), data com o dia da semana certo, link da aula (redirecionamento da live certa), início dos disparos, data de teste em dia útil.

## 5. Registrar material (planilha de links úteis)

Tudo o que a Keila ou a equipe manda (copy, arte, link de grupo, webhook, lista e tags do Active, planilha de respostas, Zoom, redirecionamento, checkout) vai na hora para a aba certa: GERAL, COPY, ARTES, WEB DESIGNER ou TRÁFEGO. Usar `editar_xlsx` (confere `modifiedTime` antes de subir), hiperlink com o nome do arquivo, nunca apagar linha. Linha com recado meu desatualizado: avisar, não sobrescrever sem ok.

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

- `python3 - <<'EOF' </dev/null` não roda nada: o `</dev/null` substitui o heredoc. Usar arquivo `.py` e `python3 arquivo.py </dev/null`.
- `cat > /dev/null` sem entrada trava o comando.
- Docs API dá 403 com esta chave: editar Google Doc por ida e volta em `.docx` (`trocar_texto_doc`), e cada ida e volta **duplica comentários abertos** (fechar as cópias).
- Nomes do Drive podem vir em NFD: normalizar com `unicodedata.normalize('NFC', ...)`.
- `.xlsx` aberto no Google Planilhas pode gerar uma cópia Google com o mesmo nome: manter só o `.xlsx` (cópia vai para a lixeira, reversível).
- Planilha editada por outra pessoa enquanto eu edito: sempre conferir `modifiedTime` antes de subir e guardar backup.
- Link de Zoom: confirmar com a planilha de links do lançamento de qual evento é a sala antes de trocar qualquer coisa; nunca deduzir pela ordem das mensagens.
- Vídeo do Drive grande: baixar em blocos para o scratchpad; subir com upload resumível (`fea_drive.subir`).

## 9. Formato das respostas para a Keila

- Português, sem preâmbulo, sem travessão, "para" sempre.
- Primeiro a resposta ("Sim, liberado" / "Não, falta X"), depois tabela, depois "o que depende de você" e "o que está com a equipe".
- Links do ClickUp como `[nome da tarefa](url)`, nunca URL solta.
- Admitir erro na hora, com o que foi corrigido.
- Nunca afirmar algo que não conferi (campanha no ar, sala de Zoom, quem editou): dizer de onde veio a informação.
