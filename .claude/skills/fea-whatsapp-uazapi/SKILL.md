---
name: fea-whatsapp-uazapi
description: Opera o WhatsApp da FEA (Dr. João Pithon) pelo conector "WhatsApp FEA (uazapi)": vigia dos grupos, respostas no grupo Gestão FEA, alertas do Luca, mensagens prontas para encaminhar, envio validado ao time, leitura de áudio, imagem e vídeo, e manutenção do conector no Cloudflare. Usar sempre que a tarefa envolver ler, responder, monitorar ou enviar mensagem nos grupos de WhatsApp da FEA, montar a rotina de vigia/ronda, ou mexer no Worker do conector uazapi.
---

# FEA: WhatsApp pelo conector uazapi

Tudo o que foi aprendido operando o número da FEA (Atendimento FEA) entre 17 e 18/11/2026. Regras de negócio completas ficam no `CLAUDE.md` do repositório FEA; aqui está o "como fazer" técnico e operacional.

## 1. O que é o conector

- **uazapi:** API não oficial de WhatsApp. Instância da FEA: `https://feagrupos.uazapi.com` (as mídias ficam em `/files/<hash>.mp3|jpg|mp4`, links válidos por cerca de 2 dias).
- **MCP remoto no Cloudflare Workers:** o conector "WhatsApp FEA (uazapi)" do claude.ai é um Worker que traduz as ferramentas abaixo em chamadas da uazapi. URL e token da uazapi ficam como **variáveis/segredos do Worker** (nunca no chat, nunca no código).
- **Transcrição:** feita no próprio Worker com **Cloudflare Workers AI** (`@cf/openai/whisper`). Cerca de 214 minutos de áudio por dia são grátis; no plano grátis, passando disso, pausa até o dia seguinte (sem cobrança); no pago, US$ 0,0005 por minuto.
- **Carregar as ferramentas** (são diferidas): `ToolSearch` com `select:mcp__WhatsApp_FEA_uazapi__novidades,mcp__WhatsApp_FEA_uazapi__ler_mensagens,mcp__WhatsApp_FEA_uazapi__enviar_texto,mcp__WhatsApp_FEA_uazapi__baixar_midia` (acrescentar as outras quando precisar).

## 2. Ferramentas e como usar

| Ferramenta | Uso | Detalhes que importam |
|---|---|---|
| `novidades` | Checagem periódica | `minutos=4` na vigia, ou `desde` em ISO (ex. `2026-11-18T20:12:10Z`). Melhor usar `desde` = horário da última mensagem vista, para não perder nada entre rodadas. Áudios já vêm **transcritos** (até 5 por chamada). Traz também as mensagens enviadas pelo próprio número (`de: "eu (FEA)"`). |
| `ler_mensagens` | Histórico de um grupo | `chatid` + `limite` + `offset` (offset anda para trás no tempo). Útil para achar a resposta de alguém a uma pergunta antiga. |
| `buscar_mensagens` | Achar um assunto em vários grupos | `texto` sem diferenciar maiúsculas; aumentar `conversas` e `por_conversa` se não achar. `somente_grupos=false` inclui conversas privadas. |
| `enviar_texto` | Enviar | `destino` = JID do grupo; `mencionar` = números com DDI só dígitos. O `@número` entra no texto sozinho se faltar. Status `Pending` na resposta é normal (foi enviado). |
| `editar_mensagem` | Corrigir texto enviado | Só por cerca de 15 minutos. **Atenção:** a edição pode aparecer para o grupo como uma mensagem nova, deixando a antiga visível; conferir no `novidades` e, se duplicou, perguntar antes de apagar. |
| `apagar_mensagem` | Apagar para todos | Sempre confirmar com a gestão antes. |
| `baixar_midia` | Imagem, vídeo, PDF, figurinha | Pelo `id` da mensagem; devolve link e tipo. `transcrever=true` em vídeo com fala. Depois baixar o link com `curl` e abrir com `Read` (imagem) ou `ffmpeg` (quadros/áudio do vídeo). |
| `transcrever_audio` | Áudio que não veio transcrito | Tratar a transcrição como texto normal da pessoa. |
| `listar_grupos` | Descobrir JIDs | `busca` filtra pelo nome. Só lista grupos em que o número da FEA **está**. |
| `info_grupo`, `link_convite_grupo`, `editar_grupo`, `criar_enquete`, `reagir`, `responder_mensagem`, `marcar_como_lida`, `listar_conversas` | Apoio | Usar quando o pedido exigir. |

### Limites conhecidos (não tentar contornar)
- **Não cria grupo nem promove admin.** Criar grupo e definir admins fica com a Keila ou a Gabi (ou a Vivi, da automação).
- **Não lê histórico anterior à entrada** do número num grupo: logo depois de ser adicionado, `ler_mensagens` volta vazio.
- **`enviar_midia` exige URL pública.** O Drive compartilhado da FEA não aceita "qualquer pessoa com o link"; solução: subir uma cópia no Meu Drive, compartilhar e enviar `https://drive.google.com/uc?export=download&id=<ID>`.
- **Menções aparecem como LID** (`@162092216795158`, `@7262840049830`) no texto lido; isso é normal. Para marcar alguém, usar sempre o número com DDI no `mencionar`.
- Se `enviar_texto` não existir na sessão, **não improvisar**: acumular as mensagens em arquivo `FEA-gestao-whatsapp/FEA-mensagens-pendentes-AAAA-MM-DD.md` e avisar.

## 3. Contatos e grupos

| Quem / grupo | Número ou JID |
|---|---|
| Gestão FEA (Keila, Gabi e o número da FEA) | `120363432442225090@g.us` |
| Gestão Keila | `120363311670705900@g.us` |
| Copy | `120363192317276002@g.us` |
| The Tracker (tráfego) | `120363253818986127@g.us` |
| Web | `120363176440560812@g.us` |
| Artes | `120363190886613616@g.us` |
| Edição | `120363305330696158@g.us` |
| Coordenação | `120363205506344232@g.us` |
| Automações (API) | `120363259883567437@g.us` |
| Comercial | `120363193065080741@g.us` |
| Elite Experience 04 e 05/12 | `120363429697865091@g.us` |
| Keila | `553191581433` |
| Gabi | `5514991278094` |
| Luca Yu (urgente em qualquer grupo) | `5511960759355` |
| Saar (tráfego) | `555191521964` |
| Matheus van der Ham (Copy) | `555481097142` |
| Adri (Copy) | `555384841867` |
| Vivianne (Automações) | `558182309754` |
| Júlio Couto | `5521999284987` |

Confirmar com a lista do time antes de contato novo: números foram deduzidos das marcações.

## 4. Regras de operação (combinadas com a Keila em 17 e 18/11)

1. **Responder rápido no Gestão FEA:** primeiro um retorno curto ("certo, buscando agora"), depois o trabalho. Marcar Keila e/ou Gabi com `mencionar`.
2. **Prioridade do Luca:**
   - mencionou Keila ou Gabi, em qualquer grupo: 🚨 alerta na hora marcando as duas;
   - pedido dele em Coordenação, Edição, Artes, Web ou The Tracker: ⚠️ alerta sem marcar;
   - demais grupos: só reportar se ninguém responder em uns 30 minutos.
3. **Pedido de link, material ou informação:** procurar antes de perguntar (Drive, ClickUp, briefings, planilhas de Links úteis, histórico dos grupos, abrir a página com `curl` para conferir). Mandar no Gestão FEA uma **mensagem pronta para encaminhar, sozinha**, separada de qualquer comentário. O pedido vira demanda no ClickUp com início e vencimento.
4. **Fora do Gestão FEA, só envia depois do ok:** rascunho numerado no Gestão FEA ("Com o ok 9, eu envio no Artes"), e só sai com "ok N" da Keila ou da Gabi (ou ordem direta delas). Avisos ao time só em **horário comercial**.
5. **Marcações fixas:** no Copy, Matheus e Adri sempre juntos; no The Tracker, o Saar sempre marcado.
6. **Escrita:** português, "para" (nunca "pra"), sem travessão, curta, com respiro entre linhas, cordial, negrito nos pontos principais, "envio" (não "mando"), fecha com "Obrigada!". Sem detalhe técnico (não citar aba de planilha nem número de item para o time).
7. **Nunca afirmar que uma demanda foi ou não feita** só pela falta de registro: pedir para a Gabi conferir.
8. **Nunca inventar dado** (duração de reunião, preço, data). Se não foi definido, não escrever.
9. **Mensagem para a Vivi:** nunca indicar quem será admin de grupo.
10b. **Demanda nunca fica parada** (Keila, 19/11): validou, entregou ou comentou, a próxima etapa sai na hora (correções, ClickUp, Links úteis, demanda e mensagem para o próximo responsável) e vem ao Gestão FEA para validar.
10c. **Todo retorno ganha resposta** (Keila, 19/11): reação 👍🏾 ou "obrigada" quando não pede nada; pedido do próximo passo quando há entrega; ou demanda nova. A pessoa precisa saber que a gestão viu.
10a. **Emoji de mão do Dr. João no tom 🏾** (👇🏾, 👉🏾) e **nunca dois espaços seguidos** (Adri, 18/11). Ler também o grupo Gestão Keila.
10. **Erro de conexão no envio:** reler o grupo antes de reenviar, para não duplicar.
11. **Toda informação nova vai para o lugar certo:** briefing do lançamento, ClickUp (tarefa e caminho citados), planilha. Nada fica só no chat.
12. **Planilhas .xlsx no Drive não são editáveis** pelo conector do Sheets (erro "must not be an Office file"). Mandar à Gabi o bloco pronto para colar; nunca criar planilha nova nem trocar link.
13. **Sem nada novo na rodada:** encerrar em silêncio.

## 5. Rotinas automáticas

- **Vigia rápida (a cada 2 min), 24h por dia, seg a sáb (Keila, 19/11):** `CronCreate` recorrente em UTC, em dois jobs para cobrir Brasília: `*/2 3-23 * * 1-6` e `*/2 0-2 * * 0,2-6`. **CronCreate vive só na sessão**: some quando o worker reinicia ou após 7 dias.
- **Madrugada (22h às 8h):** no Gestão FEA só o urgente (Luca mencionando Keila ou Gabi, ou algo quebrando no ar); o resto vira um resumo único às 8h. Nunca falar com o time de noite.
- **Ronda de reserva (de hora em hora, 24h):** scheduled task do Claude Code Remote (`create_trigger`), `CRON_TZ=America/Sao_Paulo 7 * * * 1-6`, ligada à sessão. Ela sobrevive a reinícios e, no passo 0, confere com `CronList` se os dois jobs da vigia existem; se não, recria. A rodada das 8h07 manda o resumo da madrugada.
- **Avisos com horário marcado** (ex.: aviso ao Saar às 17h, lembrete 1h antes da live): `send_later` (sobrevive a reinício). Se a Keila mandar enviar antes, enviar e **desligar** o agendado com `update_trigger enabled=false`, para não duplicar.
- Quando houver reinício da sessão, avisar a Keila que pode ter havido atraso e recriar a vigia.

## 6. Manutenção do Worker no Cloudflare

- Código de referência da ferramenta `baixar_midia`: `referencias/worker-baixar_midia.js` (rota da uazapi `POST /message/download` com `return_link: true`; com `generate_mp3: true` gera o áudio para transcrever).
- Para adicionar ferramenta: abrir o Worker do conector, colar o `server.tool(...)` no mesmo bloco das outras, usar os **mesmos nomes de variável** de URL e token que o `transcrever_audio` já usa, publicar, **reconectar o conector no claude.ai** e abrir sessão nova para a ferramenta aparecer.
- Segredos (token da uazapi, chaves) só como variável/segredo do Worker. Nunca no código nem no chat.

## 7. Checklist rápido por rodada

1. `novidades` desde a última mensagem vista.
2. Gestão FEA primeiro: Keila ou Gabi pediram algo? Retorno curto e depois executar.
3. Luca em algum grupo? Aplicar a regra de prioridade.
4. Pedido de link ou material? Buscar e mandar mensagem pronta sozinha + ClickUp.
5. Mídia? `baixar_midia`; áudio já vem transcrito.
6. Antes de enviar: reler o Gestão FEA para não duplicar.
7. Nada novo: silêncio.
