# Áudio e diálogo

O usuário decidiu:
- **Música: nunca.** Nem trilha, nem score, nem "sting", nem melodia de fundo, em nenhum clipe.
- **Som ambiente: sim.** Silêncio absoluto soa falso e o modelo tende a preencher com música.
- **Diálogo:** só onde o usuário pedir. Às vezes a voz gerada vai para o corte final; às vezes
  (Lucas, Pedro) ele troca na edição e a fala do prompt serve só para a boca e o ritmo.
- **Legenda:** nunca.

## Estrutura do bloco AUDIO

Sempre nesta ordem:

1. **Ambiente**, com 3 a 5 fontes concretas da locação. Bases por locação ficam no arquivo do
   projeto (`../projetos/`).
2. **Falas**, se houver, cada uma com: tempo aproximado → quem → como fala → `in Brazilian
   Portuguese` → a fala entre aspas duplas → a voz (descritor literal de `../vozes.md`, ou `voice
   matching @AudioN`). Depois: `These are the only spoken words in the clip.` Sem fala: `Nobody
   speaks in this clip.`
3. **Em sitcom ou qualquer cena com cara de programa de TV:** `No studio audience and no laugh
   track.` (e não escreva a palavra "sitcom" no prompt — ela chama claque).
4. **Fecho fixo** (literal):

```
The soundtrack consists only of the diegetic sound of the scene. No music, no score, no
soundtrack, no melody or musical sting at any moment from the first frame to the last; no
narration or voice-over; no subtitles, captions or on-screen text.
```

É o único lugar do prompt em que a negativa crua fica: no áudio ela funciona, e vem junto da
afirmação positiva ("only the diegetic sound").

Formato de fala:

> `At about 0.6 s ANA says in Brazilian Portuguese, light and mock-offended, at a natural,
> unhurried pace, following the intonation and pacing of @Audio1: "Você tá me chamando de
> gorda?" — voice matching @Audio1.`

**A fala também aparece no take.** No SHOT em que a pessoa fala, diga quem fala e quando (`At
about 0.6 s she says her line, following @Audio1…`). O texto exato fica no AUDIO. Fala escondida
só no AUDIO já fez o usuário perguntar "cadê a fala?" ao revisar.

## Vozes de fundo

- Sempre `indistinct` / `too distant to understand` **e com idioma**: `an indistinct murmur in
  Brazilian Portuguese`. Murmúrio sem idioma saiu em chinês.
- Voz de fundo com palavras compreensíveis compete com o diálogo e costuma gerar legenda.
- Sistema de som ou palestrante ao fundo: só "hum" ou "murmur", nunca alguém falando — o modelo
  inventa frases e às vezes põe música de evento.

## Falas

- **Idioma:** português do Brasil, escrito exatamente como o usuário mandou (ou como está no
  áudio), com acento e pontuação. Não traduza nem "corrija".
- **Duração:** ver `estrategia.md` — com áudio real, duração do áudio + ~2 s; sem áudio, ~2,5
  palavras/s (pessoas calmas ou "sábias", ~2/s) + folga.
- **Uma fala por take**, no take em que o falante está em quadro e em foco. Fala longa: corte para
  quem escuta no meio (aprovado na cena 4 do ep. 2).
- **Lip sync só funciona com rosto grande.** Fala em plano aberto sai com a boca desencontrada —
  a não ser que a voz vá ser trocada na edição e a boca apareça pequena.
- **Jeito de falar** em poucas palavras concretas: `low and dry`, `warm and a little teasing`,
  `almost under his breath`. Evite "emotional", "dramatic".
- **Risada, suspiro, "hum":** som da ação, sem aspas, e só se o usuário pediu. Se ele pediu um
  suspiro, confirme se vem **antes ou depois** da fala (já custou uma geração).
- **Nome próprio** pode sair errado na voz sintetizada ("Lunna", "Lúnia"). Negativa com as
  formas erradas não resolve; ancore a pronúncia num áudio de referência (abaixo).

## Áudio de referência (`@AudioN`)

### O que o Seedance faz com ele (pesquisado em 2026-09-25)

O Seedance **não dubla** uma gravação pronta. O áudio anexado guia timbre, sotaque e ritmo; a voz
do vídeo é sempre sintetizada. Não existe "cola o áudio e a boca dubla". Se a entonação tem que
ser exatamente a da gravação, o único jeito garantido é **trocar o áudio na edição** — funciona
bem em fala curta e em plano aberto.

### Numeração

A numeração de áudio é independente da de imagem: o primeiro áudio é `@Audio1` mesmo com
`@Image1`–`@Image13` na mesma geração.

### Que função dar ao áudio

| Situação | Frase | Resultado |
|---|---|---|
| Padrão | No REFERENCES: `@Audio1 is a recording of ANA's line in this clip — it anchors her voice, accent, intonation and the exact pacing of the line; the synthesized voice in the video is not a literal copy of this recording.` No AUDIO: `following the intonation and pacing of @Audio1 … — voice matching @Audio1` | Aprovado (sitcom ep. 2, cenas 4 e 5) |
| O tom da gravação é diferente do que a cena pede, ou só uma palavra importa (nome, marca) | `It is used narrowly, for one thing only: the exact vowel sounds of how LUNA's name is pronounced in it.` + `the emotional colour of the whole line comes from this description, not from the reference recording's own tone` | Aprovado (sitcom ep. 1, refação "Não, Luna" e cena 7 "Craft Black/Blue") |
| — | `matching @Audio1 exactly, syllable for syllable` | Reprovado: passou o tom triste da gravação para o rosto |
| — | `reproducing exactly the intonation… the same melody, word by word` | Reprovado: a fala saiu mais estranha |

Quando o áudio dá a entonação, tire da fala os adjetivos de entrega que competem com ele. Quando
o texto dá o tom, diga que o tom não vem do áudio.

### Medir o áudio real

Duração: `ffprobe -v error -show_entries format=duration -of csv=p=0 audio.mp3`.
Pausas (para cortar no lugar certo): `ffmpeg -i audio.mp3 -af "silencedetect=noise=-35dB:d=0.08"
-f null -`. Pausas de ~0,3 s batem com vírgulas. A fala começa ~0,2 s depois do início do arquivo.
Amarre cada corte à palavra e ao tempo: `Hard cut exactly in the short pause after "tempo,"`.

Onde ficam os áudios de cada projeto: no arquivo do projeto.

## Consistência de voz sem áudio de referência

O que mantém a voz parecida de um clipe para outro é **o mesmo descritor, palavra por palavra**,
de `../vozes.md`. Nunca reescreva "para variar". Se mesmo assim variar demais, proponha gerar uma
fala boa, extrair o áudio e passar a anexá-lo como `@AudioN` com função de timbre.

Voz clonada numa ferramenta de áudio do wrapper (Higgsfield Audio) é outro caminho, ainda não
testado por este usuário: a clonagem roda fora do Seedance e a fala de cada cena continua sendo
digitada.
