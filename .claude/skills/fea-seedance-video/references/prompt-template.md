# Template de composição — prompt de vídeo Seedance 2.5

Um prompt, um bloco de código, em inglês, em seções rotuladas dentro de um texto corrido. Sem
negative prompt, sem campos auxiliares. As falas ficam em PT-BR entre aspas.

**Antes de usar este template, procure um aprovado parecido em `../prompts-aprovados/`.** Partir
das palavras de um prompt que já funcionou rende mais do que montar do zero. Os exemplos reais
estão lá; este arquivo explica cada bloco.

## Por que esta ordem

1. **Anexos amarrados primeiro.** O Seedance decide o que cada imagem faz logo no começo. Sem a
   função de `@Image1` dita antes de tudo, ele trata a imagem como frame inicial e as fotos de
   rosto como "mais uma pessoa parecida".
2. **Identidade antes da cena, e de novo no fim.** O que vem no meio (look, movimento, ação)
   empurra o rosto para a média.
3. **Regra visual no topo (LOOK), regra sonora no fim (AUDIO), takes no meio.** É o formato do
   guia oficial do Higgsfield.

## Ordem dos blocos

```
REFERENCES
IDENTITY LOCK
WARDROBE
LOOK
BLOCKING
CAMERA        (opcional: convenção de câmera do projeto, quando vale para todos os takes)
SHOT / SHOTS
PERFORMANCE
AUDIO
MUST HOLD
```

Não reordene. REFERENCES, IDENTITY LOCK, WARDROBE, AUDIO e MUST HOLD vão sempre. Os outros podem
encurtar.

---

## Bloco a bloco

### REFERENCES

A função de cada anexo, chamado por `@ImageN` **e** por uma descrição visível curta (se a menção
quebrar na plataforma, a descrição ainda amarra). Cada menção separada por vírgula, nunca
"`@Image6 and @Image7`" colado.

Esquema atual (ambiente vazio + fotos reais + roupa), na forma que foi aprovada na cena 4 do ep. 2:

> `@Image1 — the empty [ambiente e móveis principais] — is the LOCATION REFERENCE: it defines the
> room, its furniture, its layout, the light and the colour. Nobody is in it; [A] and [B] are
> placed into it as described below, and it is not the opening frame.`
>
> `@Image3, @Image4, … and @Image10 — the photographs of [traço visível forte] — are the sole
> source of [A]'s face, hair, skin and build; all [N] show one single [person], who appears once.
> From these photographs only the face, hair and build are taken; everything else in them is
> ignored and is not part of this clip — [as roupas e objetos de cada foto, nomeados uma vez:
> "the pink blazer, black lace top, layered necklaces…, the headset microphone, slide clicker…"],
> and all their backgrounds and lighting.`
>
> `@Image11 — [descrição da foto de roupa, sem rosto] — is the sole source of [A]'s clothing and
> body proportions; it shows no face.`
>
> `Each face comes only from its own references and is never blended with the other.`

Anexos especiais, cada um com a função escrita:

- **Still de posição/estado** (quadro de uma cena aprovada): `is a POSITION AND STATE REFERENCE
  ONLY: it fixes where both of them are in the room… It is not the opening frame, and it is not a
  source of [A]'s face.` Se o still tem uma expressão que não deve passar: `her face, expression
  and posture in that still are replaced by what this clip describes` (sem nomear a expressão).
- **Referência de enquadramento e olhar:** `is a FRAMING AND GAZE REFERENCE ONLY for this shot: it
  fixes the shot size (…) and her gaze direction (…); it is not a source of identity, wardrobe or
  mood.`
- **Foto de pose:** `the shape she is moving through — never frozen in it`.
- **Áudio:** função escrita conforme `audio-dialogo.md` → "Que função dar ao áudio".
- **Start Frame:** ele é `@Image1` e os outros sobem uma posição. Diga quem manda em quê: o frame
  manda em pose, enquadramento, luz e cor; as fotos mandam em rosto, corpo e roupa.

Esquema antigo (imagem de cena com pessoas): use só se o usuário não tiver o ambiente vazio, e
avise que o modelo tende a copiar os dublês. A imagem vira `aesthetic reference only… the people
in it are stand-ins… their faces are not copied`, e nenhum take repete o enquadramento dela.

### IDENTITY LOCK

Campos do Identity Card do `card.md`, **copiados literalmente**. Encurtar é escolher campos
inteiros, nunca reescrever frases.

| Cena | Campos por personagem |
|---|---|
| Um personagem | ANCHORS, PROPORTIONS, FACE, HAIR, MOUTH, BUILD, AGE READ |
| Dois ou mais | ANCHORS, HAIR, MOUTH, BUILD, AGE READ + TELLING THEM APART |

Exceções documentadas à cópia literal:
- **Frase de sorriso no MOUTH só quando a cena tem sorriso** (Lucas, Ana, Pedro). Em cena sem
  sorriso ela vira lábio apertado ou boca estranha.
- **Altura relativa** entre personagens vem do projeto, não do card.
- **Comentários em português** do card não entram.
- **Traço que se mostrou falso** (a pinta da Ana): corrija o card e avise; nunca copie.

Abra com `Preserve exactly, with no reinterpretation, in every frame and every shot:` e feche com:

> `The face stays identical to its reference photographs in every frame and every shot, through
> movement, speech, expression changes and head turns, and never drifts toward a different or
> more generic face as the clip progresses.`

TELLING THEM APART: 3 traços de silhueta de
cada um, opostos entre si.

### WARDROBE

A roupa vem da foto de roupa do personagem (esquema atual) — nunca das fotos de rosto:

> `[A], exactly as in @Image11, unchanged for the whole clip — never the clothes from @Image3 to
> @Image10: [peça por peça, com cor, tecido, manga, comprimento]. [Unhas, anéis, relógio: o que
> ele usa e o que não usa].`

Se a foto de roupa e o figurino do projeto divergirem, vale a foto. O bloco ARMS AND HANDS do
projeto entra quando braço ou mão podem aparecer.

### LOOK

Literal, igual em todo clipe do mesmo projeto (o texto de cada projeto fica em
`../projetos/<projeto>.md`). A base:

```
LOOK: Match the colour grade, contrast, exposure and light direction of @Image1 exactly and keep
them constant for the whole clip, including across cuts. Photorealistic live-action footage shot
on a large-sensor cinema camera: 24 fps with a 180-degree shutter and natural motion blur on
movement, fine organic film grain, shallow depth of field with focus held on the nearest eye of
the person the shot is about, the background softly out of focus throughout. The camera has
physical weight: every move starts and stops with gentle easing, never snapping or floating.
Skin keeps its real texture in motion — visible pores, natural sheen, fine lines — with no
smoothing. [PROPORÇÃO] frame.
```

A proporção muda por projeto (4:3, 9:16 vertical…). Confirme no primeiro prompt do projeto.
Quer mais "cara de cinema"? Lente, abertura e plano de foco por take, grão de 35 mm, bloom — mas
`no lens flare of any colour` (flare colorido vaza para outras luzes).

### BLOCKING

Onde cada um está e para onde está virado **quando o clipe começa**: posição no espaço, distância,
o que as mãos seguram. Descrito em palavras, com base no ambiente e nos stills de posição.

- Se o clipe continua outro, descreva o **estado** em que as pessoas estão (posição, o que
  seguram, para onde olham), não a ação que aconteceu no clipe anterior ("não precisa dizer que a
  Luna abaixou a caneca… a IA pode se confundir").
- Conte os objetos que já duplicaram ou que importam (`The room has exactly one rug`).
- Grupo: liste da esquerda para a direita por traço visível.

### CAMERA (opcional)

A convenção do projeto, quando vale para vários takes. Exemplo aprovado (sitcom ep. 2): `Framed
like a classic 1990s multi-camera TV studio set. Every shot in this clip is a dialogue shot,
locked-off on a tripod, perfectly still — no handheld drift, no push-in, no zoom.` Só escreva
"every shot" quando for mesmo todo take; se alguém anda, diga a exceção.

### SHOT / SHOTS

**Um take:**

> `SHOT (0–N s, one continuous take): [tamanho do plano por partes do corpo], [lente], [altura e
> lado da câmera], [movimento e quanto anda]. [Ação com sinais observáveis]. End state: [como
> termina].`

**Vários takes:**

> `SHOT 1 (0–2.8 s): … End state: … Hard cut.`
> `SHOT 2 (2.8–5.6 s): Continuing from the previous shot: [estado de cada pessoa visível e de quem
> está fora de quadro]. …`

Regras:
- **Uma ação principal por take.** Os tempos são orçamento e somam a duração pedida.
- **Tamanho do plano por partes do corpo**, não só "close": `head-and-shoulders, headroom above
  her hair, both shoulders in frame, never a tight face-fill close-up`. Para Instagram, rosto no
  terço de cima e terço de baixo livre para legenda.
- **Olhar sempre dito**: para onde a pessoa olha (`her gaze down and to the side toward LUNA…
  never toward camera`).
- **Lado da câmera sempre dito** quando houver dois lados possíveis.
- **Fala dentro do take**: quem fala e quando; o texto exato no AUDIO.
- **End state** sempre. No fim de uma fala, a pessoa volta ao neutro (sem gesto inventado).
- **Raccord dentro do clipe:** a partir do 2º take, `Continuing from the previous shot:` e a ação
  em andamento de cada pessoa visível; quem saiu de quadro continua fazendo o que fazia.
- **Movimento de câmera é dentro do take**, com magnitude (`slow push-in of about half a metre`,
  `slow lateral tracking of about one metre`), nunca "dynamic camera". Entre takes, `Hard cut.`
- **Rosto grande = rosto fiel.** Plano aberto é para estabelecer, com rosto pequeno assumido.
- **Conversa:** singles e over-the-shoulder em vez de two-shot simétrico; o take vai para quem
  fala. Two-shot "tem que mostrar os dois" — over-the-shoulder que esconde um deles foi recusado.
- **Close de um personagem só: centralizado** (preferência do usuário), com o olhar dito.

### PERFORMANCE

Parágrafo curto com a atuação desta cena e os traços do elenco que valem aqui (de
`../projetos/<projeto>.md` → "Elenco"). Ver `atuacao-natural.md`. Comportamento observável, nunca
adjetivo de emoção; nada de gesto que o usuário não pediu.

### AUDIO

Sempre presente. Ambiente → falas → (sitcom: `No studio audience and no laugh track.`) → fecho
fixo. Ver `audio-dialogo.md`.

### MUST HOLD

Três a seis linhas: âncoras de cada rosto em poucas palavras, a roupa (de onde vem), contagens
(pessoas, objetos que duplicaram), posições fixas, nenhuma música.

> `Fixed across every frame and every shot: [âncoras de A]; [âncoras de B]; each face reads as
> unmistakably the same individual as its references; wardrobe exactly as in @ImageN, never the
> clothes from the photographs; exactly [N] people, never a duplicate; no music at any moment.`

---

## Comprimento

- **Alvo: até ~12 mil caracteres (~2.000 palavras). Teto: 15 mil.** Nenhuma das 36 gerações com
  prompt de 15 mil caracteres ou mais foi aprovada. Os aprovados com duas personagens, 4 takes e
  fala ficaram entre 13 e 15 mil; os de um take, entre 6 e 10 mil.
- Conte antes de entregar (`wc -m` num arquivo do scratchpad).
- Passou do alvo: corte primeiro o som ambiente e o BLOCKING, depois micro-ações da PERFORMANCE,
  depois as repetições entre blocos, depois divida o clipe. Nunca corte IDENTITY LOCK, REFERENCES
  nem o fecho do AUDIO.
- **Correção não pode inchar o prompt.** A frase nova substitui a antiga.

---

## Modo compacto — plataformas com limite de caracteres (Magnific: 1000)

Quando a plataforma limita o prompt, o Identity Card não cabe: **as fotos carregam a identidade**
e o texto só amarra cada anexo, dirige câmera e ação e trava o som. Alvo: **≤ 950 caracteres**,
contados com `wc -m` antes de entregar.

Ordem e prioridade (corte de baixo para cima, nunca as três primeiras):

1. **Anexos:** `@Image1: location, light only; never recreate its framing, faces or poses.` + uma
   linha por personagem com lado, roupa em 2–3 palavras, 1–2 âncoras curtas e o temperamento:
   `MAN A (black tee, prominent ears, calm) = @Image2 @Image3 @Image4 @Image5` — cada anexo por
   extenso. Fecha com `Never blend faces.`
2. **Travas do projeto numa frase:** proporção, `Bare forearms, no rings.`
3. **Takes:** `SHOT N (a-bs): [plano, lente], [câmera]. [ação em 1–2 frases]` — fala entre aspas
   dentro do take.
4. **Atuação** numa frase: `Natural, unhurried; nobody looks at lens.`
5. **Áudio** numa frase, por último: `Audio: [2–3 sons]. No music, no subtitles.`

Negativas curtas são aceitáveis aqui — não há espaço para a fórmula afirmativa longa.

Exemplo: um prompt compacto aprovado tinha 954
caracteres, "ficou ótimo!").
