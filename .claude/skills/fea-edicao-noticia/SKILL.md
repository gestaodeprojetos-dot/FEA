---
name: fea-edicao-noticia
description: Edita vídeos verticais da FEA (Dr. João Pithon) no modelo "notícia" - headline que desliza da barra dourada como faixa de telejornal, tela dividida com esfumaçado no meio (B-roll ou produto em cima, Dr. embaixo), foto do produto sem fundo quando ele cita o produto, música calma baixa e legenda padrão FEA. Usar quando a Keila pedir vídeo de opinião ou lista ("melhores produtos", "melhores tratamentos", "mito ou verdade") com B-roll, tela dividida, produtos na tela ou "edição estilo notícia/Volpe".
---

# FEA: edição de Reels no modelo notícia

Teste pedido pela Keila em 26/10/2026 (vídeo IMG_7934, "Os 3 melhores preenchedores para os lábios"), aprovado pela Keila em 27/10/2026 com o vídeo "3 passos do skincare" ("esse vamos deixar assim mesmo, vamos para os próximos"). Script: `FEA-edicao-videos/fea_editar_noticia.py` (usa as funções de corte e legenda do `fea_editar_video.py`). Projeto de exemplo: `FEA-edicao-videos/FEA-projeto-noticia-melhores-labios.json`.

## Entrada

- Bruto no Drive (pasta `00 - Brutos/Melhores produtos` ou `Melhores tratamentos`).
- Referência da headline: `1- Olheiras` na pasta `20- Entrevistas mito ou verdade` (barra dourada `#DBD093` à esquerda, texto preto em caixas brancas, uma por linha, que sai de trás da barra deslizando para a direita).
- Banco de B-roll: pasta `FEA-B-roll pele flácida e envelhecida (face)` (`11xqr4MAiTQz6nVptRl0FbvcCtxcJXsLX`), arquivos `FEA-broll-NN-...`. Só usar quando os brutos não tiverem imagem do tema (ver regras abaixo).
- Banco de vídeos de skincare/pele (catálogos `FEA-banco-imagens/FEA-banco-videos-catalogo.csv` e `...-lote2-catalogo.csv` na branch `claude/great-hopper-vt6n13`): Pexels, Coverr e Mixkit, licença de uso comercial, com o link "baixar original" de cada clipe. A pasta do Drive desse banco não abre com a chave da FEA, então baixar direto da fonte pelo link do catálogo. Mixkit: `https://assets.mixkit.co/videos/ID/ID-1080.mp4` (se vier com 111 bytes, tentar `-720`). **Nunca** usar clipe marcado "gerado por IA: sim" (linha vermelha 7) nem os da `FEA-broll-lista.csv`, que foram recortados de reels de outros perfis (direito autoral de terceiros).
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
- Conferir cada trecho a 2 quadros/s antes de usar: sem sangue escorrendo, sem cara de dor e sem troca de plano no meio (o IMG_7468 abre o plano em 1:32,5). Nunca usar pastas "NÃO AUTORIZADO".
- **Não cortar o diálogo com quem está atrás da câmera** quando o corte fica perceptível ("vou colocar uns extras" / "posso colocar?" / "pode, pode"): manter a conversa inteira.
- **Testar a fala da moça que provoca o Dr. no começo** ("Ei, só vale três. Produtos para os lábios."): o vídeo começa nela, com a headline por cima.

## Estilo das referências do Dr. (27/10/2026): `"estilo": "referencia"`

O Dr. mandou 2 reels ("Queria umas coisas mais exageradas assim"): "03 cremes fantásticos para sua pele de idosa" e "3 cremes de farmácia barato que toda mulher 40+ precisa usar". A primeira tentativa (painel fixo de 2/3 com close de ruga e pele de idoso) foi **reprovada** pela Keila: "nada a ver com as referências; ele fala depois dos 40, não idoso". O que as referências têm de fato:
- **Gente de 30 a 45 anos com pele bonita e brilhando**, nunca idoso nem close de ruga, poro ou pele doente. Para "depois dos 40", mulher na faixa dos 40 com boa pele.
- **Produto sendo aplicado de forma exagerada**: espuma em espiral com esponja, creme em listras ou pontinhos no rosto, bisnaga encostada na pele, rolinho no rosto. O B-roll mostra a ação do produto de que o Dr. fala (limpeza = espuma, lavar o rosto, algodão; creme = creme espalhado).
- **Tela dividida na metade** no gancho, e o B-roll cresce para baixo (o Dr. vai descendo): `"cresce": [960, 1200]`. Com clipe horizontal, não passar de ~1200 px, senão a imagem fecha demais no rosto. Clipe vertical pode ir até 1650.
- **Headline centralizada na emenda** entre a imagem e o Dr., caixas brancas com letra preta grossa (Montserrat ExtraBold), sem a barra dourada, durante todo o gancho (`headline_fim` ~6 s).
- Depois do gancho, o **Dr. em tela cheia** (`cheio`), com inserção dividida só nos produtos e nos momentos de ação.
- Não copiar a caixa alta integral nem o apelo popular ("pele de idosa", "barato"): a CLAUDE.md proíbe. O "exagero" fica no visual.
- Clipes bons do banco: Mixkit 50408 (espuma com esponja, `c5`), 50426 (creme na bochecha, `c13`), Pexels 7306686 e 7306685 (mulher de 40 aplicando creme, mas com bastão escuro: não usar em limpeza), Mixkit 51181/limpeza com algodão (`c39`, vertical). Não usar: Pexels 5534415, 7298096, 11120960, 7582851 (idosos).
- O B-roll é renderizado na altura máxima da cena e recortado no centro; `PUSH` 0,06.
- **IA reprovada no vídeo (Keila, 28/10/2026: "não gostei das imagens de IA, ficou estranho; usa os vídeos do B-roll de TikTok")**. Ordem de preferência do B-roll: 1) vídeos do próprio Dr.; 2) takes do TikTok da pasta da Keila; 3) banco gratuito. IA só se a Keila pedir de novo.
- **Take do Dr. na pia (IMG_8338): nunca o trecho em que ele ri** (26-34 s); usar só 35-43 s, ele lavando o rosto.
- Histórico (substituído pela regra acima): **"Exagerado" = pessoa se lambuzando** (Keila, 28/10/2026): "vídeos exagerados da pessoa enchendo o rosto de creme, se lambuzando de creme... muito estranho, você vai parar para assistir". Banco gratuito não tem isso. **Fonte aprovada: IA no HeyGen** (exceção registrada na CLAUDE.md, só skincare). `text_to_video`, 9:16, 1080p, 5 s: **4 créditos por clipe**, pronto em ~1 min (conta Pro, créditos renovam todo mês). Prompts que funcionaram (em inglês, sempre "Brazilian woman around 40/45, healthy glowing skin, smartphone UGC style, no text, no logos, no brand"):
  - rosto coberto de espuma com as duas mãos, "almost absurd amount of product" (gancho);
  - enxaguando a espuma com água espirrando, revela pele limpa e sorri;
  - gel bombeado em quantidade na mão, escorrendo, vira espuma (frasco branco sem marca);
  - camada grossa de creme espalhada no rosto inteiro como máscara;
  - secando com toalha e tocando a pele macia.
- **B-roll do próprio Dr. (prioridade sobre IA e banco)**: pasta `1hajwqryVv90nzbOCW1lYTyHYZlmpXNRx` (Keila, 28/10/2026, "vou pegar mais"). Vídeos de celular na vertical (gravados deitados, o FFmpeg gira sozinho). IMG_8338 (53 s): 0-2 s bombeia o CeraVe Gel de Limpeza na mão, 14-26 s espalha a espuma no rosto de frente, 28-40 s enxágua na pia, 42-53 s seca com toalha. IMG_8339: secando com toalha. IMG_8340: passando algodão (tônico). IMG_8341: bisnaga branca na mão e espalhando no rosto. Usar com `"altura": 1100`, `cy` 0,4 a 0,45. Quando a Keila mandar mais, conferir em folha de contato e anotar aqui.
- **Takes do TikTok** (pasta `B roll tiktok`, `1xxDtrIOug_iZp1gM9PWlIpG4woaIujN7`, baixados pela Keila com ssstik.io): liberados por ela em 28/10/2026 ("pode usar esses vídeos, não tem problema"). 576x1024, legenda da criadora sempre no terço de baixo: enquadrar com `"altura": 1100` e `cy` 0,38 a 0,42 (some a legenda); gancho com `"cresce": [960, 1250]`. Nunca o tt08 ("From this, to this": antes e depois). Evitar trecho com embalagem de marca em destaque. Melhores: tt07 14-16 s (rosto cheio de pontinhos de creme, gancho), tt06 2 s e 10 s (pontinhos de protetor), tt13 1 s (espuma cobrindo o rosto, `cy` 0,5 para tirar o "POV" de cima), tt02 5 s (espuma), tt04 8-14 s (máscara com pincel, pele brilhando), tt03 6-10 s (pele glow).
- Clipe vertical da IA vai no painel com `"altura": 1100` e o gancho com `"cresce": [960, 1500]`.

## Ritmo: corte rápido (Keila, 26/10/2026)

"O corte está ficando muito silêncio... precisa de um corte mais rápido." Neste modelo, **toda pausa de respiração entre frases sai** (corte seco, jump cut): silêncio de 0,2 s ou mais com o áudio abaixo de 45 dB vira corte, deixando 0,06 s depois da última palavra e 0,04 s antes da próxima. Os pontos vão no `manter` com `"exato"` para o encaixe automático não devolver o respiro: `python3 fea_cortes_rapidos.py bruto.mp4 trechos.json > manter.json` (trechos = conteúdo escolhido, sem repetição). A legenda leva para o trecho vizinho a palavra com tempo adiantado que cairia no respiro cortado (antes sumiam "Por", "Depois", "antes"). Exemplo no projeto `FEA-projeto-noticia-3-passos-skincare.json` (52,3 s viraram 48,1 s em 11 trechos). Diferente dos Reels de procedimento, em que silêncio com técnica acontecendo fica.

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

## Vídeo de rotina/categoria sem marca (ex.: "3 passos do skincare", 26/10/2026)

- O Dr. fala categorias (gel de limpeza, creme hidratante, protetor solar), não marcas: o painel mostra B-roll de pessoa fazendo o passo (limpeza com espuma, creme na bochecha, protetor no rosto) e uma etiqueta roxa com o passo (`"rotulo": "1. Limpeza"` na primeira cena de B-roll de cada passo).
- **Foto de produto só quando o Dr. indica o produto claramente no vídeo** (nome falado). Se ele fala só a categoria (gel de limpeza, creme, protetor), **sem foto de produto**: B-roll + etiqueta do passo (Keila, 26/10/2026, revisão do "3 passos": "se o doutor não indica o produto claramente no vídeo, pode tirar as fotos"). Não puxar marca indicada em outro vídeo.
- Onde achar a foto do produto citado (fundo branco ou PNG sem fundo): site oficial do Brasil primeiro; se não tiver, site oficial de outro país da América Latina (Toleriane Dermo-Cleanser: `laroche-posay.com.ar`, arquivo `...-200ml-3433422406599-front.png`, já sem fundo); por último foto de farmácia (Bioderma Sensibio Gel Moussant: Drogasil `product-data.raiadrogasil.io/images/12624490.webp`). Etiqueta numerada quando ele lista ("1. CeraVe Gel de Limpeza") e cena `produtos` com os 3 numerados quando ele fala "esses 3" ou "anota essas três opções".
- Fotos oficiais CeraVe, se ele citar: `https://www.cerave.com.br/-/media/project/loreal/brand-sites/cerave/americas/br/scx/pdp/new-packshots/<produto>/<arquivo>-lg.jpg` (700x875). Recorte: `fea_recortar_produto.py` normal para frasco colorido; pote branco `--limiar 246 --convexo`; bisnaga branca com sombra ao lado precisa de máscara manual limitando a borda.
- Proteção solar: B-roll de praia de biquíni com zoom no rosto (`zoom` 2,0), sem mostrar o corpo.

## Pontos para levar à Keila

- Marca de ácido hialurônico na tela (linha vermelha 3 do CLAUDE.md): o pedido dela é mostrar os produtos, mas confirmar se pode publicar com as marcas.
- Origem das fotos de produto (site de distribuidor ou quadro de edição anterior da equipe).
- Música escolhida (estilo e volume).
