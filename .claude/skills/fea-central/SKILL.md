---
name: fea-central
description: Central de tudo o que o Claude sabe fazer para a FEA (Dr. João Pithon) e para a Keila. Índice que leva cada pedido à skill certa (ronda do ClickUp, datas e sprints, operação de lançamento, edição e revisão de Reels, WordPress) e guarda as receitas que não estão em outra skill, com scripts prontos para Drive, Planilhas Google, teste de páginas e links rastreados, renomear criativos, transcrever vídeo, achar artigo científico de conteúdo, montar áudio de URA, imagem de API, checkout e auditoria de lançamento ("o que falta?", "testa tudo"). Usar no começo de qualquer pedido da FEA quando não estiver claro qual skill usar, quando a Keila perguntar o que o Claude sabe fazer, ou quando o pedido for uma das receitas abaixo.
---

# FEA: central de capacidades do Claude

Esta skill é o mapa. Primeiro ache o pedido na tabela; se ele tem skill própria, carregue essa skill e siga por ela. Se a receita está aqui, siga a receita. As regras do `CLAUDE.md` (autonomia, estilo, linha vermelha, prefixo FEA, "para" e nunca "pra", sem travessão) valem sempre.

Scripts desta skill: `.claude/skills/fea-central/scripts/`. Todos usam o token do Google de `FEA-edicao-videos/fea_drive.py` (variáveis `FEA_GDRIVE_*` do ambiente) e o ClickUp pelo proxy (`Authorization: x`, nunca mostrar nem gravar token).

## 1. Qual skill usar

| Pedido da Keila (como ela fala) | Onde está o como fazer |
|---|---|
| ronda, cobra, "o que venceu", virar sprint, thumbs da semana, URA + SMS do lançamento | skill `fea-clickup-ronda` |
| "distribui as datas", montar sprints, tarefas sem prazo | skill `fea-distribuir-datas` |
| briefing de lançamento, "ajusta tudo", "testa pra mim", "aloca pro Léo", "faz o mesmo em MPL", "coloca na planilha", doc para automação, adaptar copy ou criativo de edição anterior, "o que falta", "como estamos" | skill `fea-operacao-lancamentos` |
| editar Reels, cortes, legenda, "editar a pasta" de brutos | skill `fea-edicao-reels` e depois, sempre, `fea-revisao-reels` |
| site, LP, título, Yoast, WP Rocket, Elementor, credencial de WordPress | skill `fea-wordpress` |
| traduzir vídeo, depoimento em espanhol | `CLAUDE.md` (HeyGen, Spanish, precision, sem legenda) e seção 4 de `fea-operacao-lancamentos` |
| documentar processo, checklist, SOP | template de SOP do `CLAUDE.md` |
| qualquer receita da seção 3 abaixo | esta skill |

## 2. Fontes que sempre resolvem

- **Planilha de links úteis do lançamento** (uma por lançamento, sempre Google Planilhas nativa, nunca .xlsx): abas GERAL, COPY, ARTES, WEB DESIGNER, TRÁFEGO, CPL. É o primeiro lugar para achar link de grupo, Zoom, checkout, página, lista e tag do Active.
- **Criativos para Tráfego** (Google, `1Zx5c1vNUqUqQBJyq7m5_9oYpex9mdePhLhL8qHUIGP8`, abas por mês) e **Perpétuo** (`1zIwANufWdM3PTTs_LNc-SWtlNxNBYShC19jjwEQyqeI`).
- **Drive do lançamento**: `1. COPY`, `2. ARTES`, `4. TRÁFEGO` (BRUTOS, CRIATIVOS PRONTOS por fase), `7. SLIDES`, `9. URA + SMS`.
- **Drive de produto** (ebooks, cursos): `2. Produtos / <produto> / 4. Tráfego / CRIATIVOS / 1. BRUTOS, 2. EDITADOS, 3. ESTÁTICOS`. O que está em `8. Internacionalização` é LATAM, não Brasil.
- **Conteúdo do Instagram**: `3. Conteúdos / 2. INSTAGRAM / 0 2026 / <mês>` (uma pasta por post, brutos em `00 - Brutos`).
- **Artigos científicos**: pasta `Artigos Científicos` (`1Rw1cPA9-yqgtFkNRcbo0vfqEqYBkYXRR`, cerca de 60 PDFs).
- **Calendário**: `FEA-gestao-clickup/FEA-calendario-2026-2027.md`. **Padrões para outros Claudes**: `FEA-gestao-clickup/FEA-padroes-operacao-equipe.md`, espelhado no Doc `1NkbIawRhO-oWpVTz-6o1JImPcU_cKHFZzM7QliDDhLQ` (toda regra nova entra no .md e no Doc no mesmo dia; reenviar por PATCH com upload `text/markdown`).

## 3. Receitas

### 3.1 Drive e Planilhas (`scripts/fea_google.py`)
`arvore`, `buscar`, `caminho`, `copiar`, `xlsx2sheet`, `lixeira`, `planilha`, `doc`. Exemplos:
```bash
python3 .claude/skills/fea-central/scripts/fea_google.py buscar "name contains 'Links úteis' and name contains 'Bioestim'"
python3 .claude/skills/fea-central/scripts/fea_google.py planilha 1IAYTOhIyBQFbecLUkAgETGrDpmko771EOSIO6Ke3_Pc GERAL
```
- Busca por nome casa por **início de palavra**: `'Links úteis'` acha, `'inks'` não.
- Para "coloca na pasta X": **copiar** (não mover) e conferir md5; dizer no relatório que os originais ficaram.
- Converter xlsx: `xlsx2sheet`, trocar os links que apontavam para o xlsx, depois mandar o xlsx para a lixeira (Keila: "precisa sempre apagar as que não usamos mais"). Nunca mover planilha da equipe; a de Disparos só com pedido explícito.
- Antes de sobrescrever arquivo, conferir `modifiedTime` ou md5.

### 3.2 "Testa tudo" de um lançamento (auditoria ponta a ponta)
1. Ler a planilha de links úteis inteira (todas as abas).
2. Rodar `node .claude/skills/fea-central/scripts/fea_testar_links.js <urls>` em: captura, obrigado/check-in, página do Zoom, vendas, onboarding, obrigado de compra, os redirecionamentos de `joaopithon.com.br` usados nas copys (`masterclass-grupo`, `aula-zoom`) e todos os links rastreados `bio.joaopithon.com.br/<canal>` e `/<produto>-<canal>`. O script mostra a URL final, a campanha da UTM, as datas que aparecem e os **botões sem link**.
3. Conferir: destino é a página do lançamento atual (não a da edição anterior), `utm_campaign` do lançamento atual, sala do Zoom igual à da planilha, grupo igual ao link do Send Flow, página de vendas com botão indo para o checkout, checkout abrindo o produto certo na Hotmart.
4. ClickUp: tarefas abertas por sprint, vencidas, sem responsável, tarefa esquecida no Backlog, sprint vazia perto do fim do carrinho.
5. Relatório em 3 blocos: 🔴 bloqueia a próxima fase · 🟡 precisa até as vendas · ✅ funcionando. Mandar o que for de outra pessoa como comentário na tarefa dela, com o link certo pronto para aplicar (e `assignee` para notificar).
- Curl leva 406 em `bio.joaopithon.com.br`: usar o script (Playwright).
- Grupo de WhatsApp: o convite não mostra o nome sem login e `info_convite` da uazapi falha; comparar o código do convite com o do Send Flow.

### 3.3 Renomear criativos em vídeo (`scripts/fea_renomear_criativos.py`)
Padrão `VID_[MMAA]_[TAG]_[NNN]_[FORMATO].mp4` (Keila, 26/11/2026). Rodar sem `--aplicar` para ver o plano, depois com `--aplicar`. Se a Keila der horário ("depois das 13h30"), agendar com `send_later` e executar na hora. Avisar o tráfego que o nome mudou (o link não muda).

### 3.4 Transcrever e identificar vídeo (`scripts/fea_transcrever_trecho.py`)
Para: achar de que artigo o vídeo fala, achar take ("ele fala que está ao vivo"), conferir fala antes de entregar. Baixar o vídeo com a API do Drive (`?alt=media`) para o scratchpad e apagar depois. O faster-whisper daqui só funciona com entrada numpy (o script já faz).

### 3.5 Conteúdo de artigo científico ("me envia os links do artigo")
Série "o que diz o artigo" fica em `3. Conteúdos / 2. INSTAGRAM / 0 2026 / <mês>` com pastas "Artigo: ...". Para cada uma: link do vídeo e link do PDF (na própria pasta, em `00 - Brutos/<tema> artigo` ou em `Artigos Científicos`). Confirmar o par ouvindo o vídeo (3.4); se o vídeo não citar o artigo, dizer "provável" e pedir confirmação. Vídeo que pede "comenta eu quero" precisa de automação que entregue aquele artigo: conferir a tarefa de automação "eu quero" no ClickUp.

### 3.6 Áudio de URA a partir de gravações do Dr. João (`scripts/fea_ura_montar_referencia.py`)
Pedido típico: "pega um áudio que já existe e junta com ...", até 30 s, mesmo tom, sem cortar palavra, pouca pausa.
1. Extrair o áudio das fontes (vídeos de WhatsApp, URAs antigas em `9. URA + SMS`), 44,1 kHz mono.
2. Transcrever com tempo de palavra para achar cada frase.
3. Montar pelas peças: corte por energia (nunca no meio da sílaba), equalização para o timbre de uma fonte de referência, nível pelo RMS da fala ativa, pausa curta com ruído de sala, compressor leve e loudnorm linear no final.
4. Pico antes da EQ normalizado (pico em 0 dB gera estalo). Frase longa ("do primeiro lote") sai de uma fonte só.
5. Ouvir, transcrever o resultado e conferir a duração antes de subir em `9. URA + SMS` com prefixo FEA.

### 3.7 Imagem de API e ajuste de arte
Editar arte existente (trocar data, texto, foto do Dr. João de outra peça aprovada) com PIL e OpenCV, fonte Montserrat ExtraBold e Medium, com a mesma altura de letra da arte original. Nunca gerar imagem final com IA generativa (linha vermelha 7). Subir na pasta `IMAGENS API` do lançamento e pôr o link na tarefa; marcar feito só com o ok da Keila.

### 3.8 Checkout e oferta
Hotmart MCP: `hotmart_products_list` funciona; `product_offers_list` devolve 500. Testar o link do checkout com o script de links (abre em dólar fora do Brasil, é normal). Checkout que não existe (ex.: PLX Latam em USD): dizer que não existe e onde as copys apontam hoje. Nunca inventar preço.

### 3.9 Confirmar evento, data e modelo antes de produzir
Pedido de outro Claude ou da equipe tipo "é para a Masterclass X?": conferir no calendário (data da live, captação, vendas, produto vendido), nas pastas do Drive e do ClickUp, e se o evento-modelo existe. Avisar diferença de formato entre o modelo e o novo (ex.: masterclass emendada em Desafio que vende FEP). Devolver a resposta pronta para colar.

### 3.10 Agendar para depois
"Faz isso às 13h30", "me lembra amanhã": `send_later` com a mensagem completa do que fazer (script e IDs), porque a sessão pode reiniciar. Rotinas fixas (ronda 7h52, 11h52, 16h52; virada de sprint sexta 20h52) são scheduled tasks próprias.

## 4. Antes de dizer "pronto"
- Conferi no destino (Drive listado de novo, página aberta de novo, tarefa relida)?
- Regra nova que a Keila deu hoje foi gravada na skill certa, no `FEA-padroes-operacao-equipe.md` e no Doc espelho, e commitada?
- Relatório em português, com emoji, negrito e tabela, link `[nome](url)` de cada tarefa, decisões que tomei em "decidi X, me avisa se preferir Y" e no máximo uma pergunta, a que mais destrava.
