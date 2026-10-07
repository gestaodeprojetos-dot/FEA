# FEA · Black Vitalícia · Teste do Ep. 01 "O Julgamento" no Google Flow (Veo 3.1)

Versão 1.0 · 07/10/2026 · Objetivo: testar se o Veo 3.1 alcança a qualidade dos vídeos publicados (sequestro e viagem no tempo), gastando no máximo os 50 créditos disponíveis.

## Configuração do Flow (antes de gerar)

| Ajuste | Valor |
|--------|-------|
| Modelo | Veo 3.1 **Fast** (cerca de 20 créditos por cena; o Quality custa cerca de 100 e não cabe) |
| Proporção | 9:16 (vertical) |
| Saídas por comando | **1** (com 2, cada cena custa o dobro) |

## Cena 8 · Dr. João (modo "Ingredientes para vídeo")

Fotos de referência: `FEA-testes-voz/FEA-foto-ref-joao-4.jpg` (frontal), `-6.jpg` e `-7.jpg` (closes). As fotos ficam só na sessão de trabalho e não vão para o GitHub.

```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa with a 50mm lens, natural film grain, realistic skin texture with pores. An old courtroom with dark wood paneling, warm daylight through tall arched windows, dust floating in the air, the audience in soft focus. The man from the reference images, wearing a plain black dress shirt, sits at the defendant's bench and slowly stands up. Slow push-in to a medium close-up. Calm, firm expression. He says in Brazilian Portuguese, with a calm deep voice: "Tenho... Anatomia não deveria ter prazo de validade." No subtitles, no music.
```

## Cena 1 · Juiz (modo "Texto para vídeo", sem fotos)

```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain. Extreme close-up of a wooden judge's gavel striking the bench in slow motion, dust rising in warm window light, in an old courtroom with dark wood paneling. Cut to a Brazilian judge, around 65 years old, grey hair, black judicial robe, thin-rimmed glasses, solemn. He says in Brazilian Portuguese, with a deep serious voice: "O réu, Doutor João Pithon, é acusado de entregar tudo o que sabe. Para sempre." Murmurs from the audience. No subtitles, no music.
```

## Depois de gerar

1. Baixar as duas cenas em 1080p.
2. Trocar o áudio do Dr. João pela voz clonada no HeyGen ("FEA Dr João Pithon (Black 2026)") e refazer a sincronia de boca (lipsync em modo precision; o áudio precisa ter duração até 15% diferente da cena).
3. Montar com `fea_montar_episodio.py` (legenda amarela, `acabamento_filme`, card oficial).
4. Se a qualidade bater com os vídeos publicados: o episódio inteiro tem 9 cenas, cerca de 180 créditos no Fast.
