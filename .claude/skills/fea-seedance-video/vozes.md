# Vozes

Uma linha por personagem com o descritor de voz que entra literal no bloco AUDIO (veja
`references/audio-dialogo.md`).

| Personagem | Descritor de voz (em inglês) | Observação |
|---|---|---|
| *(ex.: Ana)* | *(ex.: a warm, mid-pitched female voice, relaxed and slightly dry)* | *(ex.: usar o áudio gravado como referência de entonação)* |
| Dr. João Pithon | voz clonada no HeyGen "FEA Dr João Pithon (Black 2026)", voice_id 636c7858aeca4ea494ae6e2c722617ad (instant, pt) | Ele não grava áudio. Toda fala sai do clone: `create_speech` (mp3, `language: pt`, com timestamps), medir com ffprobe, subir no Drive do projeto e anexar como `@Audio1` no Seedance. Na edição, a voz do vídeo é trocada pelo mesmo mp3 |

Tom do Dr. João (Keila, 19/11/2026): o padrão do clone sai "animado demais". Aprovado: `expressivenessBoost: 0` (clipe 1 v3). Para tom de autoridade em frase com várias orações, gerar uma oração por vez e juntar com pausa de ~0,6 s no ffmpeg. Baixar o tom 1,5 semitom com rubberband foi reprovado (deixa de parecer ele). Speech to speech (gravação da Keila convertida no HeyGen) foi reprovado em 19/11: "ruim". Aprovado em 19/11: frase inteira de uma vez com `expressivenessBoost: 0`; montar frase a frase com pausa deixou lento demais ("não precisa falar lento").
