---
name: fea-edicao-noticia
description: Edita vídeos verticais da FEA (Dr. João Pithon) no modelo "notícia" - headline que desliza da barra dourada como faixa de telejornal, tela dividida com esfumaçado no meio (B-roll ou produto em cima, Dr. embaixo), foto do produto sem fundo quando ele cita o produto, música calma baixa e legenda padrão FEA. Usar quando a Keila pedir vídeo de opinião ou lista ("melhores produtos", "melhores tratamentos", "mito ou verdade") com B-roll, tela dividida, produtos na tela ou "edição estilo notícia/Volpe".
---

# FEA: edição de Reels no modelo notícia

Teste pedido pela Keila em 26/10/2026 (vídeo IMG_7934, "Os 3 melhores preenchedores para os lábios"), **ainda em validação**: só replicar nos próximos vídeos depois do OK dela. Script: `FEA-edicao-videos/fea_editar_noticia.py` (usa as funções de corte e legenda do `fea_editar_video.py`). Projeto de exemplo: `FEA-edicao-videos/FEA-projeto-noticia-melhores-labios.json`.

## Entrada

- Bruto no Drive (pasta `00 - Brutos/Melhores produtos` ou `Melhores tratamentos`).
- Referência da headline: `1- Olheiras` na pasta `20- Entrevistas mito ou verdade` (barra dourada `#DBD093` à esquerda, texto preto em caixas brancas, uma por linha, que sai de trás da barra deslizando para a direita).
- Banco de B-roll: pasta `FEA-B-roll pele flácida e envelhecida (face)` (`11xqr4MAiTQz6nVptRl0FbvcCtxcJXsLX`), arquivos `FEA-broll-NN-...`. Escolher os mais chamativos e ligados ao tema (lábios: 08 idosa com batom e rugas periorais, 02 mulher madura, 14 massagem facial com lábios em close, 16 tratamento em clínica).
- Referência anterior do mesmo modelo (tela dividida): `FEA-teste edição estilo Volpe` dentro de `Melhores produtos`.

## Padrão visual

| Item | Valor |
|---|---|
| Formato | 1080x1920, 30 fps, H.264 CRF 18, AAC 192k (nunca HEVC) |
| Tela dividida | painel de cima com 1000 px; esfumaçado de 820 a 1000 px; Dr. desce 480 px (cabeça logo abaixo do esfumaçado) |
| Transição | deslizante de 0,38 s: o painel novo entra pela direita empurrando o antigo; tela cheia para dividida, o Dr. desce enquanto o painel entra |
| Headline | Sora Bold 60, caixas brancas de 80 px por linha, barra dourada de 18 px em x=143, topo em y=730, até ~4,4 s; quebrar em linhas curtas (3 linhas de até ~15 caracteres) para não passar da tela |
| Legenda | padrão FEA (Montserrat Bold 56, contorno preto, ~80% da altura); neste modelo roda junto com a headline, como na referência |
| Produto | recorte sem fundo e sem borda, sombra suave, etiqueta roxa `#5B4599` com o nome oficial; entra com leve zoom quando o Dr. fala o nome; "top 3" ganha uma cena com os 3 lado a lado numerados |
| Fundo do painel de produto | quadro do próprio bruto (teto e parede, sem o Dr.), desfocado e com 35% de lavanda `#D0D1E9` |
| Música | calma, ~20 dB abaixo da voz, entrada de 1,2 s e saída de 2 s. Só faixa CC0 ou domínio público (ex.: Chopin, Noturno op. 37 nº 2, Olga Gurevich, Musopen/archive.org, CC0) |

## Fluxo

1. Ambiente e transcrição como na skill `fea-edicao-reels` (passos 1 a 3). Se o `faster-whisper` falhar com `metadata_errors`, instalar `pip install --only-binary :all: "av>=12,<15"`.
2. Cortes (`manter`, segundos do bruto): começar na primeira fala do Dr. sobre o tema; tirar a conversa com quem está atrás da câmera ("posso colocar?", "pode, pode"); fechar na pergunta de engajamento do fim ("e aí, quais são os top 3 da sua prática clínica?").
3. Cenas (`cenas`, segundos do bruto, cada uma vai até a próxima): `broll` no gancho e nos trechos de explicação, `produto` em cada nome falado (entrar ~0,1 s antes da palavra), `produtos` para o resumo da lista, `cheio` quando o Dr. fala direto para a câmera.
4. Produtos: foto oficial (distribuidor ou fabricante) com fundo branco, recortada pelo preenchimento a partir da borda (`fea_recortar_produto.py`: limiar de branco + componente ligada à borda + abertura morfológica, alfa erodido 2 px para tirar o halo). Caixa branca em fundo branco (e.p.t.q.): `--limiar 251 --convexo`. Nunca gerar imagem de produto por IA.
5. Conferir quadros antes do render: `python3 fea_editar_noticia.py projeto.json --quadros 0.6,2,6,12,22,30,40`.
6. Render: `python3 fea_editar_noticia.py projeto.json` (~4 min para 45 s). Conferir mosaico 1 quadro/s e as transições a 10 quadros/s.
7. Subir com `fea_drive.py upload` na pasta indicada pela Keila.

## Grafias oficiais conferidas (26/10/2026)

Neuramis Deep (Medytox), Revanesse Kiss (Prollenium, caixa "KISS+"), Restylane Refyne e Restylane Kysse (Galderma), Belotero Intense (Merz), e.p.t.q. S100 (Jetema). Já estão em `CORRECOES` do `fea_editar_video.py`.

## Pontos para levar à Keila

- Marca de ácido hialurônico na tela (linha vermelha 3 do CLAUDE.md): o pedido dela é mostrar os produtos, mas confirmar se pode publicar com as marcas.
- Origem das fotos de produto (site de distribuidor ou quadro de edição anterior da equipe).
- Música escolhida (estilo e volume).
