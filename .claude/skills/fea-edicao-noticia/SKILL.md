---
name: fea-edicao-noticia
description: Edita Reels verticais da FEA (Dr. João Pithon) no "modelo notícia": título que sai de trás de uma barra dourada como faixa de telejornal, tela dividida com esfumaçado no meio (imagem em cima, Dr. embaixo), legenda sobre o esfumaçado, cartões de produto ou tratamento, artigo científico rolando com destaque roxo e música baixa. Usar quando pedirem para editar vídeo do Dr. no modelo notícia, "igual esse que você faz", vídeo de lista ("3 melhores produtos", "3 melhores tratamentos"), vídeo de artigo científico ("o que diz o artigo") ou "edição estilo notícia/Volpe".
---

# FEA: edição de Reels no modelo notícia

Quem pede e aprova as edições é a **Gabi (Gabriela Costa, editora da FEA)**. Responder em português, sem travessão, sempre "para" e nunca "pra".

Este estilo foi construído em revisões com a Gabi e a Keila entre outubro e novembro de 2026. Cada regra abaixo veio de um pedido delas; o histórico completo, vídeo a vídeo, está em `references/historico-videos.md`.

## Três formatos

| Formato | Painel de cima mostra | Exemplo de projeto |
|---|---|---|
| **Melhores produtos** | takes do procedimento + foto oficial do produto sem fundo, com etiqueta roxa, na hora em que o Dr. fala o nome; grade numerada no resumo | `references/projetos-exemplo/FEA-projeto-noticia-mandibula.json` |
| **Melhores tratamentos** | takes do procedimento + cartão branco com número em círculo roxo ("1 Ácido hialurônico"); os 3 cartões empilhados no fim | `references/projetos-exemplo/FEA-projeto-tratamento-codigo-barras.json` |
| **Vídeo de artigo** | fotos e figuras do artigo, página rolando com destaque roxo nos trechos que o Dr. comenta, takes clínicos do tema | `references/projetos-exemplo/FEA-projeto-artigo-palpebra.json` |

## Padrão visual (não mudar sem pedido)

| Item | Regra |
|---|---|
| Formato | 1080x1920, 30 fps, H.264 CRF 18, AAC 192k. Nunca HEVC |
| Tela dividida | painel de cima de 1000 px; esfumaçado de 820 a 1000 px; o Dr. desce 480 px |
| Transição | deslizante de 0,38 s, o painel novo empurra o antigo pela direita |
| **Título** | Sora Bold 60, caixas brancas por linha, barra dourada `#DBD093` à esquerda. **No meio do vídeo** (linha do meio em y=960, bloco centrado na horizontal) **com as linhas alinhadas à esquerda**, encostadas na barra. Até 3 linhas curtas (~15 caracteres). Fica ~5 s (`headline_fim` 4,6). Nunca subir o título para o topo |
| Legenda | padrão FEA (Montserrat Bold 56, contorno preto). **Na tela dividida fica no meio, sobre o esfumaçado** (nunca no rosto do Dr.); em tela cheia, na altura padrão. **Sem legenda enquanto o título está na tela** |
| Título x tela cheia | se a cena vira `cheio` antes do fim do título, o título sai antes (automático), para não passar pelo rosto do Dr. |
| Produto | foto oficial (pasta do Drive `2. Produtos > REOLOGY MAP > 30. Imagens de produtos` ou site do fabricante), recortada sem fundo (`scripts/fea_recortar_produto.py`), etiqueta roxa `#5B4599` com o nome oficial. **Mostrar todos os produtos que o Dr. cita**: a grade tem o mesmo número que ele fala |
| Cartão de tratamento | `scripts/fea_cartoes_tratamento.py` (número em círculo roxo, texto Sora azul-escuro) |
| Fundo do painel de produto | quadro do próprio bruto, desfocado, com 35% de lavanda `#D0D1E9` |
| Música | só licença livre (Mixkit, CC0). Produtos e tratamentos: "Cat Walk" (Mixkit 371, a partir de 12 s, 28 dB abaixo da voz, `nivelar`). **Tema tenso (intercorrência, nódulo, necrose) e vídeos de artigo: música neutra estilo notícia, baixa**: "Relaxation 03" (Mixkit 747, 30 dB abaixo da voz). Nunca música alegre em tema tenso, nunca trilha de terror |

## Regras de edição (todas vieram de revisões da Gabi e da Keila)

**Imagens**
- O B-roll mostra **exatamente o que o Dr. está falando** (falou de lábio, aparece lábio). Nada de B-roll genérico.
- **Primeiros inserts de impacto**: o take mais forte abre o vídeo; nos 2 primeiros, só a região do tema, bem evidente (zoom 1,4 a 1,7 recortando os olhos fora).
- Cada insert dura de 2 a 4 s; nunca trocas de 1 s. No máximo 2 inserts seguidos da mesma paciente.
- **Quando o Dr. cita intercorrência, mostrar imagem de intercorrência do tema** (banco da equipe `3. Conteúdos/5. INSERTS VIDEOS/Intercorrências`: necrose nasal, edema periorbital, ptose por toxina).
- Antes e depois entra **sem aviso de "imagem ilustrativa"** (o público é profissional).
- Insert de procedimento = agulha ou cânula trabalhando dentro da região; não serve anestesia, agulha só se aproximando, sangue escorrendo ou cara de dor.
- Vídeo já editado (com legenda gravada) só serve recortado com `cy`/`zoom` para a legenda gravada ficar fora do quadro.
- Fontes permitidas: brutos da FEA (pacientes com autorização), bancos de licença livre (Pexels, Mixkit, Wikimedia Commons com crédito) e figuras de artigo de acesso aberto (CC BY, citando). **Nunca foto de paciente achada no Google** e **nunca imagem gerada por IA**. Nunca pastas "NÃO AUTORIZADO".
- Imagem que pareça estranha ou fora de contexto sai (ex.: câmara hiperbárica com fileiras de poltronas "parecia um avião"; cápsulas e central de controle "pareciam coisa de astronauta").

**Vídeo de artigo**
- **O artigo sempre aparece rolando na tela nos trechos em que o Dr. fala do estudo** (título, métodos, resultado, conclusão), com destaque roxo no trecho que ele cita. Imagens clínicas ficam no começo, nos trechos de explicação.
- Usar o PDF que veio na pasta do bruto. Conferir a licença (selo CC BY ou "open access"). Renderizar a 220 dpi (`pdftoppm -r 220 -png artigo.pdf p`) e achar as coordenadas do destaque com `pdftotext -bbox-layout` (pontos x 220/72).
- Clipes com `scripts/fea_artigo_lib.py` (página rolando, figura inteira, foto cheia, figura em faixa A|B|C deslizando, vídeo de baixa resolução recortado). O clipe de rolagem tem que durar mais que a cena, senão reinicia.
- Figura de baixa resolução que fica borrada ao ampliar: trocar por take do tema.
- Na entrega, colocar o PDF do artigo na mesma pasta do vídeo (o CTA é "comenta QUERO e eu te mando o artigo").

**Cortes e áudio**
- **Começo**: o vídeo abre com o Dr. já falando. O `manter` começa na primeira sílaba de verdade (energia acima de ~-30 dB), não num clique ou respiro antes dela.
- **Fim**: termina ~0,15 s depois do fim da última palavra (o render soma 0,4 s de folga). Colado na palavra fica "rápido"; mais de 1 s fica "espaçado". Se a gravação para no meio da palavra, terminar na frase inteira anterior.
- **Tropeços**: retranscrever com `vad_filter=False`, `condition_on_previous_text=False` e olhar palavras com probabilidade < 0,6; frase sem sentido sai do `manter` (bordas `"exato"`). Nunca cortar no meio da palavra.
- **Ritmo**: `"tirar_silencios": {"minimo": 0.18, "folga": 0.06, "limiar_db": 50}`.
- **Chiado**: medir o bruto **inteiro** com `scripts/fea_medir_chiado.py` (pausas e durante a fala). Se der chiado: `"limpar_ruido": "<pasta>/models/sh.rnnn"` + `"limpar_ruido_forte": true`. Se o filtro forte apagar a pergunta final falada baixo: `"limpar_ruido_suave_depois": <s do vídeo final>`. Não medir chiado no vídeo pronto (os silêncios foram cortados).
- **Legenda**: corrigir pelas `correcoes` do projeto: "pra" vira "para", nomes técnicos (ácido hialurônico, hidroxiapatita, câmara hiperbárica), CTA em maiúsculas ("QUERO").
- Grafias oficiais de produtos já estão em `CORRECOES` do `scripts/fea_editar_video.py`.

## Fluxo

1. **Ambiente** (uma vez por máquina): `bash scripts/fea_preparar_ambiente.sh TRABALHO` baixa as fontes (Sora e Montserrat), o modelo de ruído RNNoise, as duas músicas e instala as bibliotecas. Anotar o caminho do ffmpeg que ele imprime.
2. **Bruto**: baixar o vídeo (e o PDF, se for artigo) para `TRABALHO/dl/`. Extrair o áudio: `ffmpeg -i bruto.MOV -ac 1 -ar 16000 TRABALHO/an/X.wav` e `-ar 48000` para a medição.
3. **Transcrever**: `FEA_MODELOS=TRABALHO/models python3 scripts/fea_transcrever.py TRABALHO/tr TRABALHO/an/X.wav` (o modelo Whisper tem 1,6 GB e é baixado na primeira vez; a variável `FEA_MODELOS` faz ele ficar na pasta de trabalho, nunca dentro da skill). Ler a fala inteira e marcar os tempos de cada assunto.
4. **Medir o chiado** no bruto inteiro (`scripts/fea_medir_chiado.py`).
5. **Procurar takes** para cada trecho da fala (brutos do Dr., banco de inserts, B-roll livre). Conferir cada take a 1 quadro/s antes de usar.
6. **Montar o projeto JSON** copiando o exemplo do formato (`references/projetos-exemplo/`): `headline`, `manter`, `correcoes`, `fundo_produto` (quadro do bruto), `musica`, `cenas` (tempos em segundos do BRUTO; tipos `broll`, `produto`, `produtos`, `cheio`). Trocar `TRABALHO` e `ffmpeg` pelos caminhos reais.
7. **Conferir quadros** sem renderizar: `python3 scripts/fea_editar_noticia.py projeto.json --quadros 1,3,6,12,20`.
8. **Render**: `python3 scripts/fea_editar_noticia.py projeto.json` (~1 min a cada 20 s de vídeo).
9. **Revisão obrigatória antes de entregar**:
   - mosaico 1 quadro a cada 2-3 s (`ffmpeg -i out.mp4 -vf "fps=1/2.5,scale=150:-2,tile=14x2" -frames:v 1 mosaico.png`);
   - transcrever o MP4 pronto: começo na primeira palavra, fim inteiro, nenhuma palavra cortada, pergunta final audível;
   - conferir que o título não cobre o ponto importante do insert (ajustar `cx`/`cy` do take, não o título).
10. **Entregar** no Drive (pasta do mês indicada pela Gabi, numeração `1-`, `2-`...), com o mesmo link ao corrigir (substituir o arquivo), registrar na planilha de edições e avisar a Gabi com uma tabela "fala do Dr. / o que aparece".

## Scripts

| Script | Função |
|---|---|
| `scripts/fea_preparar_ambiente.sh` | fontes, modelo RNNoise, músicas e bibliotecas |
| `scripts/fea_transcrever.py` | transcrição com tempo por palavra (faster-whisper) |
| `scripts/fea_medir_chiado.py` | decide se o bruto precisa de filtro de voz |
| `scripts/fea_editar_noticia.py` | render do modelo notícia (usa `fea_editar_video.py` para cortes e legenda) |
| `scripts/fea_cartoes_tratamento.py` | cartões numerados dos tratamentos e resumo dos 3 |
| `scripts/fea_recortar_produto.py` | foto de produto sem fundo |
| `scripts/fea_cartao_foto.py`, `scripts/fea_antes_depois.py` | cartão de foto e quadro de antes e depois |
| `scripts/fea_artigo_lib.py` | clipes de artigo (rolagem com destaque, figuras, fotos, faixa) |
| `references/exemplos-clipes-artigo/` | scripts reais dos vídeos de artigo já aprovados |

Requisitos: Python 3 com numpy, pillow, scipy, faster-whisper (PyAV entre 12 e 14), ffmpeg com `arnndn` e `libass`, poppler-utils (pdftoppm, pdftotext) para artigos.
