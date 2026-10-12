---
name: fea-criativo-animado
description: Edita criativos de anúncio da FEA (Dr. João Pithon falando para a câmera) com edição elaborada de motion - animações em tela cheia sincronizadas com a fala, legenda palavra a palavra com destaque dourado, página de vendas real num celular, palestrantes, barra de lote, virada de lote, cartela final, efeitos sonoros e trilha de tensão baixa. Usar quando a Keila pedir criativo animado, "edição top/elaborada", vídeo de virada de lote, escassez ou urgência, contagem regressiva, "aquele modelo do Elite", ou anúncio de evento, congresso, imersão ou lançamento com o doutor falando.
---

# FEA: criativo animado (modelo "virada de lote")

Modelo aprovado pela Keila em 09 e 10/10/2026 nos 8 criativos de virada de lote do Elite Injectors Congress
("amei, pode seguir", "gostei muito"). Scripts, roteiros e histórico em
`FEA-edicao-videos/FEA-criativo-virada-lote/` (ler o `FEA-criativo-virada-lote.md` de lá antes de começar).

## O que a Keila manda (pedir só o que faltar, numa mensagem)

1. **Pasta do Drive com os brutos** (vídeos verticais do doutor falando).
2. **Link da página de vendas** do evento ou produto: é a fonte de todo número, data, local, preço e palestrante.
3. **Pasta de destino** no Drive.
4. Opcional: Reel de referência de estilo (baixar com `yt-dlp` e montar folha de contato para estudar).

Se ela mandar só a pasta e a página, seguir: data, prazo e escassez saem da página e da fala do doutor.

## Fluxo

1. **Ambiente**: `bash FEA-edicao-videos/fea_preparar_ambiente.sh SCRATCH` e `pip install "av>=11,<14"`
   (o PyAV 19 quebra o faster-whisper: `unexpected keyword argument 'metadata_errors'`). Fraunces:
   `raw.githubusercontent.com/google/fonts/main/ofl/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf` em `SCRATCH/fonts`.
2. **Brutos e transcrição**: `fea_drive.py baixar`, WAV 16 kHz, `fea_transcrever.py` (tempo de cada palavra).
3. **Página de vendas**: `curl` do HTML para tirar fatos (datas, %, local, preços, nomes dos palestrantes em
   `data-title`), cores (`#hex` e gradientes) e imagens (`wp-content/uploads`, logo, cards). Capturar a página no
   celular com `node fea_capturar_pagina.js PASTA` e recortar o topo do `full.png` em `pagina.jpg`.
   Não usar `recordVideo` do Playwright: grava o celular pequeno num canto cinza.
4. **Teste primeiro**: editar 1 vídeo, subir numa subpasta `FEA-editados-TESTE` e esperar a Keila aprovar o estilo
   antes do lote. **Nunca apagar nem substituir o teste depois** (pedido dela, 10/10/2026).
5. **Roteiro por vídeo** em `fea_configs.py` (dicionário `VIDEOS`): para cada fala, escolher a cena que ilustra o que
   o doutor está dizendo, com os tempos das palavras. Alternar doutor e tela cheia, nunca duas telas cheias longas
   seguidas; zoom no rosto (`zoom`) nos trechos de doutor sem gráfico, para dar ritmo.
6. **Prévia**: `node fea_render_quadros.js COMP CFG.json PREV "stills:t1,t2,..."` num momento de cada cena,
   compor sobre o quadro do bruto e olhar a folha de contato de todos os vídeos antes de renderizar.
7. **Lote**: `bash fea_lote.sh SCRATCH NOME1 NOME2 ...` em 3 processos paralelos (cerca de 1 quadro por segundo
   por processo; 8 vídeos de 25 a 35 s levam uns 35 min). Acompanhar com Monitor no `FEITO`.
8. **Conferir cada vídeo pronto** (duração, folha de contato a 1 fps, volume) e subir com
   `fea_drive.py upload DESTINO arquivo --substituir` assim que fica pronto, sem esperar o lote inteiro.
   Nome: `FEA-<Evento>-<tema>-<variação>.mp4` (ex.: `FEA-Elite-virada-de-lote-2-dias-A.mp4`).
9. Commitar roteiros e ajustes em `FEA-edicao-videos/FEA-criativo-virada-lote/`.

## Cenas prontas (`FEA-composicao-virada-lote.html`)

| Cena | Quando usar |
|---|---|
| `gancho` | primeiros 2 a 3 s: número virando ("faltam 4 dias") ou calendário ("amanhã", "hoje" pulsando) |
| `logo` | quando ele fala o nome do evento |
| `celular` | página real no celular com contador e selos (data, local, "menor valor") |
| `palestrantes` | "principais palestrantes", "casos clínicos ao vivo": **todos** os palestrantes da página, com nome (pedido de 10/10/2026), grade 4, 3 e 4 com o Dr. João no centro, e itens com check no ritmo da fala |
| `lote` | "lote mais barato" (barra até o % da página) ou "restam poucas vagas" (pulso vermelho) |
| `saiba` | "clica em Saiba Mais": seta e botão na parte de baixo, onde fica o botão do anúncio |
| `virada` | "vai virar o lote", "vai ficar mais caro": calendário até o dia, ingresso 1º lote vira 2º lote, carimbo |
| `final` | últimos 2 a 3 s: logo, data, local, prazo e botão |

Para outro evento: trocar logo, `pagina.jpg`, cards, textos fixos (nome do evento, datas, local, rótulo da cartela)
e as cores no `:root` da composição, sempre tiradas da página.

## Padrão visual e de áudio

- **Identidade**: a da página de vendas do evento (continuidade anúncio → página). Se a peça for da FEA
  institucional ou do curso, usar a identidade do CLAUDE.md. Na dúvida, perguntar.
- Legenda: Montserrat ExtraBold 70 px maiúscula, branca com contorno preto, palavra da vez em dourado, em y ≈ 1290
  (abaixo do rosto, acima da interface do Instagram). Grupos por frase, sem quebrar nomes ("Elite Injectors
  Congress", "São Paulo", "sold out", "te vejo lá", "4 dias"). "pra" vira "para", "Sabamais"/"Saba Mais" vira
  "Saiba Mais", tira o "ó".
- Cartões no topo (y 120 a 450), sem cobrir o rosto. Tela cheia deixa a faixa da legenda livre.
- **Trilha**: sintetizada no `fea_audio.py` (sem banco de música, sem risco de direitos), a 20% e abaixando sozinha
  quando o doutor fala. Efeitos a 50%. Pedido da Keila: "de leve, não precisa ser tão alto".
- H.264 CRF 18, AAC 192k, 1080x1920 30 fps. Nunca HEVC.

## Regras que não mudam

- **Todo número na tela vem da página** (prazo, %, data, local, preço). Nunca inventar % de vagas, "últimas vagas"
  ou contador falso: é escassez fabricada, proibida pela linha vermelha da FEA.
- Fala do doutor que promete mais do que a página mostra ("vai dar sold out", "quase lotado", "o anúncio pode não
  aparecer mais"): não cortar por conta própria, **listar para a Keila decidir** no resumo da entrega.
- Prazo: seguir a frase exata da página ("Dia 14/10 o valor sobe" virou "o 1º lote vira em 14/10", e não
  "preço até 14/10").
- Imagens só do site do cliente ou dos brutos. Nada de imagem gerada por IA.
- Nome de palestrante: usar o `data-title` da página. Se o nome do arquivo da foto não bater com o nome mostrado
  (ex.: `card-Jessica.webp` = "Dra. Patrícia Andrade"), avisar a Keila.

## Armadilhas já resolvidas

- PNG do Chromium sai **RGB** quando o quadro é todo opaco: o FFmpeg parava a sequência no primeiro (vídeo de 10 s).
  O `fea_montar.sh` já converte tudo para RGBA.
- `show()` com `display=''` apagava o `display:flex` do cartão: usar container interno para flex.
- No celular, o cabeçalho com contador fica abaixo da ilha (notch), senão o texto some atrás dela.
- Nome longo no card ("Dra. Vanessa Defelícibus") cortava: fonte menor só nesse nome.
- `sleep` longo é bloqueado: esperar render com `run_in_background` + `until grep FEITO` ou Monitor.

## Como a Keila pede

"Faz aquele criativo animado com estes vídeos: [pasta dos brutos], página [link], sobe em [pasta]."
