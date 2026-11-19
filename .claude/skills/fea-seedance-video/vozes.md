# Vozes

Uma linha por personagem com o descritor de voz que entra literal no bloco AUDIO (veja
`references/audio-dialogo.md`).

| Personagem | Descritor de voz (em inglês) | Observação |
|---|---|---|
| *(ex.: Ana)* | *(ex.: a warm, mid-pitched female voice, relaxed and slightly dry)* | *(ex.: usar o áudio gravado como referência de entonação)* |
| Dr. João Pithon | voz clonada no HeyGen "FEA Dr João Pithon (Black 2026)", voice_id 636c7858aeca4ea494ae6e2c722617ad (instant, pt) | Ele não grava áudio. Toda fala sai do clone: `create_speech` (mp3, `language: pt`, com timestamps), medir com ffprobe, subir no Drive do projeto e anexar como `@Audio1` no Seedance. Na edição, a voz do vídeo é trocada pelo mesmo mp3 |
