# Seedance 2.5 — comportamento do modelo e das plataformas

Modelo de vídeo da ByteDance, lançado em 2026. Pesquisa inicial em 2026-09-22 (blog da ByteDance,
guias do Higgsfield, Mitte, Kapwing e PixVerse), corrigida pelo que aconteceu nas 212 gerações do
usuário entre 22/09 e 09/10.

## Capacidades

- **4 a 30 s por geração**, em segundos inteiros, com extensão (Extend) que mantém personagem,
  ambiente e ritmo.
- **Multi-shot nativo:** vários planos com lógica de montagem numa passada. Os takes vão num
  prompt só, com `Hard cut.` entre eles.
- **Referências multimodais:** até 30 imagens, 10 vídeos e 10 áudios por pedido (o limite real
  depende do wrapper; no Higgsfield o usuário confirmou em 20/10 que dá para anexar **até 20 imagens**,
  então não corte anexo útil para "caber em 8"). No texto, cada anexo é `@Image1`, `@Image2`… na ordem do upload.
- **Áudio e vídeo gerados juntos:** diálogo com lip sync, efeitos e ambiente. Ainda precisa do
  fecho de AUDIO explícito para não pôr música.

## O que o modelo faz, na prática

Quatro comportamentos explicam quase todas as gerações reprovadas:

1. **Mostra tudo o que está escrito.** Verbo vira ação, substantivo vira objeto, negativa traz o
   que nega, adjetivo de intensidade vira exagero. Detalhes em `frases.md`.
2. **Imagem vence texto.** Quando a imagem e o texto discordam, ganha a imagem: o rosto dos
   dublês, o ângulo da câmera, a porta do ambiente, a escala do objeto no close, a roupa da foto
   de rosto, a expressão do still de posição. Para algo que tem que sair exato, conserte a
   **imagem** (recorte, still novo, Start Frame), não o texto.
3. **Cada geração é um sorteio novo.** O mesmo texto já deu um gato pequeno e um gato gigante.
   Mudar três frases muda o vídeo todo. O texto não "guarda" o que saiu bom.
4. **Prompt que cresce, piora.** Correções somadas diluem as regras que já funcionavam. Das 36
   gerações com prompt de 15 mil caracteres ou mais, nenhuma foi aprovada; os aprovados têm de
   ~1.000 a ~15.000. Guias de terceiros mostram prompts longos funcionando — o problema aqui é
   prompt que **inchou** com correções e com gente demais.

## Referência × frame inicial

| Modo | Nomes comuns | O que faz com a imagem |
|---|---|---|
| **Referência** | Reference, Omni-reference, Multi-reference, Elements | Usa a imagem como fonte de conteúdo. A composição é livre — **não trava pose nem enquadramento** |
| **Frame** | Image-to-video, First/Start frame | A imagem **é** o primeiro quadro |
| **Extend** | Extend, video extension | Continua um vídeo pronto |
| **Video Edit** | Edit, video_edit | Edita um vídeo pronto por texto |

- O padrão do usuário é **Reference/Omni**. Texto não vence o modo: em Start Frame o clipe começa
  na imagem, diga o prompt o que disser.
- **Frame bom que tem que ser mantido** (pose, luz, enquadramento): Start Frame **com as
  referências de rosto, corpo e roupa ainda anexadas** — é a combinação que o usuário escolheu
  ("as outras referências são importantes", Pedro). Start Frame sozinho só se as referências
  estiverem estragando a imagem.
- Descrever em texto um frame bom **não** o reproduz (muda luz, pose e rosto).
- Escolha do modo por situação: `estrategia.md`.

## Regras de referência confirmadas

- **Uma função por anexo**, dita por escrito, com o que ignorar nele.
- **Vincular personagem a foto por traço visível**, nunca por ordem ("@Images 1 to 4 are the
  characters" embaralha rostos). Texto escrito dentro da imagem não serve.
- **Várias fotos da mesma pessoa:** todas definem uma única pessoa, que aparece uma vez.
- **Nunca imagem gerada como fonte de rosto:** folha de rosto gerada, frame de vídeo, rosto
  recortado de baixa resolução. Confirmado três vezes (Ana ep. 2, Pedro, POV da plenária).
- **Ambiente vazio** como `@Image1`. Imagem de cena com pessoas faz o modelo copiar os dublês.
- **Foto de roupa sem rosto** (de preferência foto de produto ou corpo do queixo para baixo).
- **Foto de corpo** quando o porte importa — sem ela o modelo engorda.
- **Still de posição** (de uma cena aprovada) como referência de "onde cada um está": diga que só
  as posições vêm dele, não o rosto nem a expressão.

## Orçamento de anexos

| Cena | O que funcionou |
|---|---|
| Uma ou duas pessoas | Ambiente + até 8 fotos reais da protagonista + folha do outro personagem + roupa + 1–2 stills de posição/enquadramento. **Até 13 imagens e 2 áudios, aprovado** (sitcom) |
| Três ou mais pessoas com rosto | Uma foto de cada pessoa **já vestida** com a roupa da cena. Com 7 pessoas e 13–14 anexos, a roupa vazou e os rostos diluíram (Pedro). Acima de ~5 rostos, divida em clipes ou use singles curtos |
| Personagem de costas ou desfocado | 1–2 fotos bastam |
| Clipe só de objeto/mãos | Só o ambiente (e uma foto de rosto **sem mãos** se o tom de pele importar) |

Menos e melhor: um conjunto enxuto rende mais que o limite cheio.

## Estrutura de prompt que funciona

Seções rotuladas num bloco corrido: uma regra visual no topo (LOOK), uma regra sonora no fim
(AUDIO), os takes no meio — o formato do guia oficial do Higgsfield. Detalhes em
`prompt-template.md`.

Falhas comuns, segundo os guias e o histórico:
- Sem blocking inicial → confusão espacial.
- Transição vaga entre takes → perda de consistência. Sempre `Hard cut.` + plano novo definido.
- Tempos tratados como exatos → são orçamento, não edição frame a frame.
- Grupo sem contagem → pessoas a mais ou a menos. Liste cada pessoa por traço (`frases.md`).

## Texto na tela

- Texto com mais de ~3 palavras, letreiro em perspectiva, logo: **sai errado**. Gerar sem o texto
  e aplicar na edição. Para o usuário, explique o porquê numa linha.
- Para tela de computador digitando: página em branco, sem cursor, tela paralela à lente, câmera
  parada, mãos digitando e som de teclado; o texto (máquina de escrever), o zoom e o movimento
  entram na edição. Câmera parada no vídeo = texto sobreposto sem tracking.
- Quando o texto na tela é diegético e pedido, o prompt diz `the only text in the clip is the
  [neon sign "LIBERDADE"]; no subtitles or captions`.
- **Letreiro de 4 palavras saiu certo** (num vídeo em estilo desenho) com: recorte só
  da placa anexado como `TEXT REFERENCE` (proporção até 2,5 — o Higgsfield recusa anexo mais largo),
  o texto entre aspas no prompt sempre que a placa aparece, câmera parada e de frente, e no AUDIO
  `no subtitles or captions. The only text in the clip is the painted sign "…"`. Saiu legível nos
  dois planos em que aparece, inclusive no aberto. Ao que parece o cenário anexado era o da placa
  em branco, e as letras vieram do recorte.
- Sem foto de rosto anexada, não use rótulo de personagem (`MAN A`): o modelo procura alguém que
  não foi definido. Use `the typist`.

## Notas por plataforma

Registre aqui o que for descoberto no uso real.

### Higgsfield (principal, desde 2026-09)

- **Modos do Seedance 2.5:** `t2v`, `omni_reference` (o que usamos), `video_edit` (edita um vídeo;
  cobrado pela duração dele) e `video_extension` (Extend). Duração 4–30 s, **só número inteiro**.
- **Quadro inicial e quadro final** (`start_image` e `end_image`, confirmado no catálogo do Higgsfield
  em 21/10): o Seedance 2.5 aceita os dois no mesmo clipe, junto com imagens de referência. Serve
  para transição gerada por IA entre dois clipes prontos: o início é o último quadro de um, o fim é
  o primeiro quadro do outro, e o modelo só inventa o meio. O Extend também anda **para trás**
  (`extension_mode: backward`), não só para a frente.
- **Draft:** rascunho 480p barato (~33 créditos por ~10 s), finalizável em 1080p (~132) em até 7
  dias. O usuário testa em Draft e finaliza o que ficou bom. Vídeos 480x854 são rascunhos.
- **Video Edit** precisa do vídeo finalizado (~132) e custa mais ~132. Compensa para tirar ou
  trocar um objeto isolado (tirou o tapete extra, "ficou perfeito"). FLUX Video Edit custa 1
  crédito/s, mas o usuário prefere não arriscar.
- **Extend:** só com o vídeo anexado e prompt curto de continuação (aprovado). **No Higgsfield o Extend não tem Draft**: sai no preço cheio. Para testar barato, estenda em pedaços curtos (mínimo 4 s) e só continue se o primeiro der certo. **Imagem anexada no Extend não troca quem já está no vídeo** ("O relógio", 21/10): o menino de 8 do vídeo voltou no lugar da folha de 15 e o Pedro manteve o rosto do vídeo; só o personagem que não estava no vídeo saiu da folha. A emenda e o movimento de câmera, esses saíram perfeitos. Para mudar idade ou rosto na continuação, use Reference com o último quadro como Start Frame, escolhendo um quadro sem o rosto a trocar. Extend com imagens
  de referência junto foi reprovado. O registro do Extend pode aparecer como 16:9.
- **Start Frame conta como `@Image1`** e empurra os outros anexos uma posição. Numere já com esse
  deslocamento e mostre a lista na ordem real.
- **Anexo acrescentado depois de colar o prompt não se vincula:** na animação dos anos 80 (cena 2 v2) o
  `@Image6` ficou como texto puro no registro e só 5 imagens foram enviadas, e a referência de posição
  não chegou ao modelo. Ao mandar o prompt, diga quantas imagens devem aparecer anexadas. Se o usuário
  disser que o resultado ignorou um anexo, confira no registro (`show_generations`) se o `<<<image_N>>>`
  existe e se a lista de mídias tem N itens.
- **Menções `@ImageN` são vínculos:** trocar um anexo apaga a menção dele no texto; acrescentar
  Start Frame renumera. Depois de mexer nos anexos, cole o prompt inteiro de novo. Escreva cada
  menção separada (`@Image6, @Image7`) — `@Image6 and @Image7` já chegou quebrado.
- **"Rejected due to copyright restrictions":** marca no texto (iPhone, nome de empresa), foto de
  produto com logo, foto de roupa com rosto de pessoa famosa. Objeto genérico, logo na edição.
- Não há modelo de lipsync dedicado no catálogo.

### Magnific (usado em 2026-09-23 e 24)

- **Limite de 1000 caracteres** no prompt (contam espaços e quebras). Modo compacto de
  `prompt-template.md`, contado com `wc -m` antes de entregar.
- **Duração mínima 4 s.**
- **Aceita `@Image1` no texto.** Cada anexo por extenso (`@Image2 @Image3`), nunca intervalo.
- O prompt chama o anexo por `@ImageN` **e** por descrição visível — funciona nos dois casos.
