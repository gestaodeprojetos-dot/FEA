---
name: fea-edicao-noticia
description: Edita vídeos verticais da FEA (Dr. João Pithon) no modelo "notícia" - headline que desliza da barra dourada como faixa de telejornal, tela dividida com esfumaçado no meio (B-roll ou produto em cima, Dr. embaixo), foto do produto sem fundo quando ele cita o produto, música calma baixa e legenda padrão FEA. Usar quando a Keila pedir vídeo de opinião ou lista ("melhores produtos", "melhores tratamentos", "mito ou verdade") com B-roll, tela dividida, produtos na tela ou "edição estilo notícia/Volpe".
---

# FEA: edição de Reels no modelo notícia

Teste pedido pela Keila em 26/10/2026 (vídeo IMG_7934, "Os 3 melhores preenchedores para os lábios"), **ainda em validação**: só replicar nos próximos vídeos depois do OK dela. Script: `FEA-edicao-videos/fea_editar_noticia.py` (usa as funções de corte e legenda do `fea_editar_video.py`). Projeto de exemplo: `FEA-edicao-videos/FEA-projeto-noticia-melhores-labios.json`.

## Entrada

- Bruto no Drive (pasta `00 - Brutos/Melhores produtos` ou `Melhores tratamentos`).
- Referência da headline: `1- Olheiras` na pasta `20- Entrevistas mito ou verdade` (barra dourada `#DBD093` à esquerda, texto preto em caixas brancas, uma por linha, que sai de trás da barra deslizando para a direita).
- Banco de B-roll: pasta `FEA-B-roll pele flácida e envelhecida (face)` (`11xqr4MAiTQz6nVptRl0FbvcCtxcJXsLX`), arquivos `FEA-broll-NN-...`. Só usar quando os brutos não tiverem imagem do tema (ver regras abaixo).
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
| Música | **estilo moda/passarela** (Keila, 26/10: trocar o piano por "musiquinha tipo moda"): "Cat Walk" (Arulo, house) do Mixkit, licença gratuita para vídeo em rede social, sem atribuição (`https://assets.mixkit.co/music/371/371.mp3`, a partir de 12 s). **~28 dB abaixo da voz** (volume aprovado), `"nivelar": true` (compressor + dynaudnorm: a faixa varia 9 dB entre a parte calma e o refrão). Só faixa de licença livre (Mixkit ou CC0); nunca música comercial |

## Regras da Keila (26/10/2026, revisão do primeiro teste)

- **B-roll ilustra o que o Dr. está falando.** Falou de lábios, a tela mostra lábios: nada de B-roll genérico (massagem facial, pele envelhecida) que não combina com a fala. Fonte principal: os brutos do próprio Dr. (`00 - Brutos`: "36OK- Preenchimento labial e revisão toxina", "Toxina e lábios", "29.OK- Paciente Leonard - lábio"). Exemplo: "baixo G' com alto tan delta" = cânula entrando no lábio; "volumizações maiores" = lábio pronto; "cada perfil de paciente" = pacientes diferentes; "diferenças reológicas de cada produto" = seringa injetando o produto.
- **Insert de procedimento = agulha trabalhando DENTRO do lábio** (Keila, 26/10/2026): retroinjeção lateral no lábio inferior (IMG_7468 14,5-24,5 s; IMG_2608 296-308 s) ou agulha no lábio superior (IMG_7464 8-10,5 s). Não serve: anestesia, agulha ou cânula entrando perto do queixo (IMG_2608 55 s e 280 s), seringa por baixo com a boca aberta (IMG_7463). Takes de lábio sorrindo ou lábio pronto continuam valendo. Também não serve: agulha ainda fora do lábio, só se aproximando (IMG_2608 296 s, reprovado no print de 26/10), nem seringa de êmbolo amarelo, que é a de anestesia (aparece dentro da boca no IMG_2504). Aprovados na versão final: IMG_7468 14,5-23 s, 41,5-46,2 s e 56,5-60,9 s, e IMG_7464 8-10,5 s.
- **Primeiro insert tem que ser "bem tchan"** (feedback de 26/10/2026): o close mais forte do material abre o vídeo (ex.: dedos segurando o lábio com a agulha preenchendo, IMG_7468 41,5 s). **Variar pacientes**: não deixar todos os inserts da mesma paciente; buscar outros casos de preenchimento labial nos brutos (ex.: paciente masculino IMG_2505 0-2,4 s, pasta "29.OK- Paciente Leonard"). Vídeos já editados (Dr. no quadrinho + legenda gravada, pastas "07 - Julho") não servem de insert. Reprovados por sangue visível: IMG_2609 90-94 s.
- Conferir cada trecho a 2 quadros/s antes de usar: sem sangue escorrendo, sem cara de dor e sem troca de plano no meio (o IMG_7468 abre o plano em 1:32,5). Nunca usar pastas "NÃO AUTORIZADO".
- **Não cortar o diálogo com quem está atrás da câmera** quando o corte fica perceptível ("vou colocar uns extras" / "posso colocar?" / "pode, pode"): manter a conversa inteira.
- **Testar a fala da moça que provoca o Dr. no começo** ("Ei, só vale três. Produtos para os lábios."): o vídeo começa nela, com a headline por cima.

## Fluxo

1. Ambiente e transcrição como na skill `fea-edicao-reels` (passos 1 a 3). Se o `faster-whisper` falhar com `metadata_errors`, instalar `pip install --only-binary :all: "av>=12,<15"`.
2. Cortes (`manter`, segundos do bruto): começar na fala de quem provoca o Dr. (se houver) ou na primeira fala dele; manter o diálogo com quem está atrás da câmera; fechar na pergunta de engajamento do fim ("e aí, quais são os top 3 da sua prática clínica?").
3. Cenas (`cenas`, segundos do bruto, cada uma vai até a próxima): `broll` (trecho dos brutos que mostra o que ele fala, `cx`/`cy`/`zoom` centrando os lábios), `produto` em cada nome falado (entrar ~0,1 s antes da palavra), `produtos` para o resumo da lista, `cheio` quando o Dr. fala direto para a câmera.
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
