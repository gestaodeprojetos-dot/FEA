# FEA: tradução de criativos com legenda queimada (PT para ES)

Pedido da Keila em 07/10/2026: pasta de anúncios FEP (`Ads 1 FEP` a `Ads 25 FEP`, Drive `11u328RycUMV-ENo4286nA3VTSD7nnJWI`) para tradução, **tirando a legenda em português e deixando só a do espanhol**.

## Diagnóstico do material

- Os vídeos vêm do editor com **legenda e letreiros gravados na imagem** (não existe faixa de legenda separada nem versão em espanhol no arquivo). Áudio em português (Dr. João, alunos e pacientes); no Ads 19 há pacientes do Chile falando espanhol, com legenda PT.
- Formato de origem: 2160x3840 HEVC 30 fps. **Entrega: 1080x1920 H.264 CRF 18**, áudio AAC 192k (HEVC não abre no computador da Keila).
- Tipos de texto PT encontrados: legenda branca com contorno; letreiro grande condensado ("PROCEDIMENTOS ISOLADOS", "APENAS 2 MESES"); caixa branca estilo story ("Técnicas seguras e replicáveis da FEP"); caixinha de pergunta do Instagram; cartela final "Toque em SAIBA MAIS".
- Texto que **fica como está** (é da cena, não da edição): story do paciente gravado na tela ("@drjoaopithon / Muito muito muito natural"), rótulos de produto, logo FEP, textos já em espanhol ou inglês.

## Fluxo

1. Baixar: `python3 fea_drive.py baixar PASTA_ID brutos/`
2. Versão de trabalho 1080p (decodificar 4K HEVC é o que mais pesa): `ffmpeg -nostdin -i bruto.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 12 -preset veryfast -an mid/N.mp4`
3. OCR (3 quadros por segundo; ~1 min de vídeo leva ~10 min por núcleo): `python3 fea_ocr_criativo.py ocr FFMPEG bruto.mp4 ocr/N.json`
4. Blocos: `python3 fea_ocr_criativo.py blocos ocr/N.json grupos/N.json` lista `id, tempo, posição | texto PT`.
5. Tradução em `es/N.json` (`{id: "texto ES" | null | ""}`, ver docstring). O OCR perde acentos e às vezes junta palavras; traduzir pelo sentido, conferindo o quadro quando houver dúvida de marca.
6. `python3 fea_ocr_criativo.py montar grupos/N.json es/N.json cfg/N.json`
7. Render: `python3 fea_traduzir_criativo.py FFMPEG mid/N.mp4 cfg/N.json bruto.mp4 saida/N.mp4` (gera também `saida/N.mp4.relatorio.json` com tipo, fonte, tamanho e tempo de cada bloco). Para testar um trecho: acrescentar `INICIO DURACAO`.
8. Conferir folha de contato e, nos pontos de letreiro, quadro em resolução cheia lado a lado (original x traduzido).
9. Subir na subpasta de entrega com `fea_drive.py upload`.

## Ajustes por bloco (`_ajustes` no es/N.json)

| Ajuste | Quando usar | Exemplo do lote |
|---|---|---|
| `"tipo": "caixa"` | texto preto em caixa branca colada em fundo branco (parede, blusa) | Ads 12 título, Ads 16 e 19 caixinhas do Instagram |
| `"tipo": "caixa_escura"` | painel preto com texto branco, estilo story (uma caixa por linha) | Ads 15 "Em breve na FEP" |
| `"tipo": "branco"` + `"limiar": 246` | legenda branca fina, sem contorno, sobre roupa branca | Ads 14 (depoimento de jaleco) |
| `"largura": 1.8` | letreiro que não pode quebrar em 2 linhas | "MÁS INFORMACIÓN" nos Ads 5, 6, 7 |
| `"fonte": "Medium"` | texto original mais fino que Bold | Ads 16 |
| `"cor_texto": [r, g, b]` | texto colorido em caixa | Ads 14 "Resultados de los alumnos" (azul) |
| `"t1": 44.67` | OCR partiu a mesma linha em dois pedaços de tempo | Ads 16 |

Título de duas caixas com cores alternadas (branca em cima, preta embaixo, Ads 22 a 25): dividir o bloco em dois (um `caixa`, outro `caixa_escura`).

Ads 15 (câmera passando por mesa cheia de caixas de produto): o OCR lê todos os rótulos e mistura com a legenda; o cfg foi montado à mão, só com a faixa da legenda e os painéis.

## Como a remoção funciona (e limites)

- O quadro de referência de cada bloco é o de texto completo (cobre texto que aparece digitando).
- Remoção só nos pixels da letra e do contorno (inpainting), com folga de 10 quadros antes e depois para pegar fade. Fundo chapado (cartela preta) é pintado com a cor do fundo.
- Caixa branca: a caixa nova cobre a antiga (nunca menor que ela).
- O texto ES entra no mesmo lugar, com tamanho medido pela largura da letra PT. Legenda: Montserrat Bold branca com contorno preto. Letreiro em maiúsculas: Anton. Caixa: Montserrat Bold preta em caixa branca arredondada.
- Limite: onde a letra PT passava por cima de detalhe fino (rosto, mão em movimento), o fundo reconstruído pode ficar levemente borrado por baixo da legenda nova. A versão perfeita só sai do projeto do editor sem legenda (pedir à equipe de edição, se existir).

## Padrões de tradução (espanhol neutro latino-americano, tratamento "tú")

| PT | ES |
|---|---|
| preenchimento | relleno |
| intercorrência | complicación |
| bigode chinês | surco nasogeniano |
| injetor(a) de elite | inyector(a) de élite |
| olheira | ojera |
| têmporas | sienes |
| Toque em SAIBA MAIS | Toca en MÁS INFORMACIÓN (nome do botão do Meta em espanhol) |
| retorno (consulta) | control |
| aula | clase |

Nomes de produto e de pessoa ficam como no original (Up Contour, Biogelis Volume, Dr. João, @perfis).

## Decisões da Keila (07/10/2026, lote Ads FEP ES)

- Ads 19 (evento "começa nessa segunda-feira, ao vivo no YouTube"): entregar como está, sem cortar.
- Ads 22 a 25 (dissecção em cadáver): manter como estão.
- Valores (R$) e marcas (Up Contour, Biogelis Volume, Ilikia): manter como no original.
- Não existem projetos de edição sem legenda: a remoção por inpainting é o padrão para esse tipo de pedido.

## Dublagem no HeyGen (voz em espanhol, pedido da Keila em 07/10/2026)

Conta HeyGen da FEA (lucayhi@gmail.com). Voz clonada de todos que falam (Dr. João, alunos e pacientes), autorizado pela Keila.

1. **Vídeo limpo**: `FEA_MODO=limpo python3 fea_traduzir_criativo.py ...` apaga o PT e não escreve legenda (só as caixas). Mandar o vídeo já legendado não funciona: o HeyGen "esvazia" a letra queimada (sobra só o contorno).
2. **Texto da dublagem (SRT)**: a legenda ES com os tempos medidos no render (`saida/N.mp4.relatorio.json`), sem letreiros, caixas e cartela. **Conferir a fala sem legenda**: transcrever o áudio original (Whisper) e acrescentar a tradução de todo trecho falado que não tinha legenda na tela. O HeyGen só dubla o que está no SRT, e o resto fica mudo (13 dos 24 vídeos tinham trechos assim; o Ads 14 tinha 81 s). Os tempos não podem se sobrepor nem por 1 ms (o HeyGen recusa).
3. **HeyGen**: `create_video_translation_batch` com `srt_role: output`, `mode: precision`, `enable_dynamic_duration: false` (mantém a duração e a fala alinhada com a legenda), `keep_the_same_format: true`, idioma `Spanish (Latin America)`. Custo medido: cerca de 10 créditos por minuto.
4. **Legenda por cima**: `FEA_MODO=texto FEA_VIDEO2=dublado.mp4 python3 fea_traduzir_criativo.py FFMPEG mid/N.mp4 cfg/N.json dublado.mp4 final/N.mp4` grava a legenda ES sobre o vídeo dublado, com o áudio dele.
5. **Conferência**: transcrever o final e comparar com o áudio original (nenhuma fala faltando, idioma detectado = es).

Os SRTs usados estão em `FEA-traducao-ads-fep/srt-dublagem/`. O Ads 11 não tem fala, então não passa pelo HeyGen.
