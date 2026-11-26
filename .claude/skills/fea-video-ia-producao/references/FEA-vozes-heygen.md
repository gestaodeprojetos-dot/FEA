# Vozes no HeyGen (etapa 5)

## Vozes
| Voz | voice_id | Uso |
|---|---|---|
| Dr. João Pithon (clone instant, pt) "FEA Dr João Pithon (Black 2026)" | `636c7858aeca4ea494ae6e2c722617ad` | Todas as falas dele |
| Afonso - Warm & Resonant (pública, pt-BR, masculina) | `9ce5f601f9e04382bb26141d5a3f839d` | Voz de terceiro grave e neutra ("voz da missão") |
| Murilo - Bright & Articulate (pública, pt-BR, masculina) | `d703f08d1ef34302a36945aa3efc7b3f` | Alternativa mais clara |
Só existem essas duas vozes masculinas públicas em português (nov/2026). Conferir com
`list_voices` (type public, language pt, gender male).

## Receita aprovada pela Keila (19/11/2026)
- `create_speech_without_player` (ou `create_speech` quando ela quer ouvir no player)
- `voiceId` do clone, `language: "pt"`, **`expressivenessBoost: 0`**
- **frase inteira de uma vez**, ritmo normal
- `outputFormat: {"encoding":"mp3","sample_rate_hertz":44100}`; `withTimestamps: true` quando
  precisar marcar o tempo da fala no prompt
- Baixar com curl, medir com `ffprobe`, mandar com `SendUserFile` para ela ouvir, e só subir no
  Drive e usar no prompt depois de aprovado

## O que foi reprovado (não repetir)
| Tentativa | Resultado |
|---|---|
| Expressividade padrão (0,5) | "muito animado" |
| `expressivenessBoost: 0.1` | ainda animado |
| Baixar 1,5 semitom e 6% mais lento com rubberband | deixa de parecer ele |
| Frase a frase com pausa de 0,6 s | "não precisa falar lento" |
| Tag `[serious]` | no texto curto a tag foi falada; não usar |
| Speech to speech (gravação da Keila convertida, `convert_speech`) | "ruim" |
| Pergunta com "?" no fim do CTA | soou animado; afirmação com ponto final |

## Uso no vídeo
- Falas com boca em quadro: anexar o mp3 como `@Audio1` no Seedance (função de ritmo e timbre,
  ver `../../fea-seedance-video/references/audio-dialogo.md`) e trocar a voz pelo mesmo mp3 na
  edição. Duração do take = áudio + ~2 s.
- Narração e voz de terceiro sem boca em quadro: só na edição, nunca no prompt.
- Áudios recebidos do WhatsApp (.ogg): converter com `scripts/fea_preparar_audio.sh`.

## Comandos úteis
- Preparar áudio (corta silêncio, deixa folga, normaliza): `scripts/fea_preparar_audio.sh entrada saida.mp3`
- Upload de áudio local para o HeyGen: `create_asset_upload` → `curl -X PUT` com os headers
  devolvidos → `complete_asset_upload`.
