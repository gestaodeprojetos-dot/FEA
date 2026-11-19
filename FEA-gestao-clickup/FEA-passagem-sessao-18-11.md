# FEA: passagem de sessão (18/11/2026)

Resumo para a conversa nova continuar de onde a anterior parou. Branch de trabalho: `claude/pensive-curie-fpla7g`.

## 1. Primeira coisa a fazer: mover as rotinas para a conversa nova

As rotinas abaixo disparam na conversa antiga (`session_0125nVqC5NDfivtJj47LCFVf`). Criar iguais na conversa nova (mesmo nome, mesmo horário, mesmo texto, que pode ser lido com `get_trigger`) e depois desligar as antigas (`update_trigger enabled=false`, nunca apagar).

| Rotina | ID antigo | Quando |
|---|---|---|
| FEA · Ronda ClickUp (dias úteis) | `trig_01PDE8E29NDkvo8GqzHWTPBk` | 7h52, 11h52 e 16h52, seg a sex (America/Sao_Paulo) |
| FEA · Virada de sprint (sexta à noite) | `trig_012Dr2vkYh9456LQhAkUeX4C` | sexta 20h52 |
| Conferir aula-zoom MPL | `trig_016gnPsMhrRHmgNb8XW1ixTU` | único, 18/11 10h07 (conferir se já disparou) |

A ronda cobre as pastas BF Vitalícia 10/26, BF Total Latam, Masterclass Anatomia 12/26 (incluída em 16/11), FEA-MTB 11/26 (em espera), lista YouTube e tarefas avulsas (skill `fea-clickup-ronda`).

**Transferência feita em 18/11 (10h26).** Rotinas ativas agora na conversa `session_0117TgWTiNmvkVzC98pJYBHV` (branch `claude/gracious-cray-ctv7wn`):

| Rotina | ID novo |
|---|---|
| FEA · Ronda ClickUp (dias úteis) | `trig_013NE2NcdNRee3XSLH43azRN` |
| FEA · Virada de sprint (sexta à noite) | `trig_012SNDRSoNbvP3T2GqneFDAM` |

As antigas (`trig_01PDE8E29NDkvo8GqzHWTPBk` e `trig_012Dr2vkYh9456LQhAkUeX4C`) estão desligadas, não apagadas. A aula-zoom MPL já disparou em 18/11: a página do MPL usa `joaopithon.com.br/aula-zoom-2`, que leva à sala 858 6669 3966 (certa).

## 2. Permissões

`.claude/settings.json` libera ClickUp, Drive e Sheets sem confirmação (autorização da Keila, 17/11). Só vale em conversa nova.

## 3. Em aberto por lançamento

**Masterclass Anatomia 12/26** (live 15/12, captação 07/12, carrinho FEA 15 a 17/12)
- ClickUp: Sprints 1 a 5 (listas `1400270000007094` a `7098`), Guia de Lançamento criado (doc `8ckhche-22333`).
- Keila: oferta e bônus (checkout é o da Black), briefing (docx em branco, só datas conhecidas), ok nas copys de captação.
- Gabi (atrasadas desde 17/11, cobradas em 18/11): link do Zoom, caminho do lead, briefing de arte.
- Links rastreados de captação ainda com `utm_campaign=MEA0626` (tarefa de UTMs do Matheus Saar, 27/11).
- 3 tarefas do dia 15/12 sem responsável (desborrar preço, bio do TikTok, URA e SMS).

**Elite Experience 12/26 e Elite Mentoring**
- Copy da descrição do grupo dos aprovados (Adri, `17th71za0ha`), doc base no Drive do Elite Experience.
- Copy dos lembretes do check-in (Adri, `17th71z9zfz`); prazo do check-in 48h (pendente decisão final).
- Copy Listboss do Elite Mentoring: boas-vindas e recuperações (Adri, `17th71za14t`, 19/11) e automação (IAutomate, `17th71z9zg1`, 23/11).
- Planilha de captação do perpétuo + Clint (IAutomate, `17th71z9ypt`); página sem formulário, André acionado.
- Oferta do perpétuo do Elite Mentoring em definição com o Luca (página ainda é a do congresso).

**YouTube**
- Thumb de quarta 18/11 "Como preparar hialuronidase" (Leo, `17th71za6ur`). Falta o vídeo de sexta 20/11.

**URA + SMS**
- Doc da Intercorrências 11/26 com o áudio das 20h inserido; faltam os áudios das 9h (MEI) e dos dois horários do MPL (não estão no Drive).

## 4. Regras novas desta semana (já nas skills)
- Antes de cobrar, procurar a entrega na planilha de links úteis e no Drive.
- Nunca mover planilha.
- Planilha de links úteis sem célula vazia; planilha de tráfego sempre atualizada.
- Criativo que não pode ir ao ar fica fora da pasta de criativos.
- Briefing só com os blocos que a equipe usa.
- Zoom das lives é com a Gabi.
