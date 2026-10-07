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

## Cenas restantes (2, 3, 4, 5, 6, 7 e 9)

Consistência de rosto: na primeira aparição do promotor (cena 2) e do juiz (cena 1), tirar um print do rosto e usar como "ingrediente" nas cenas seguintes deles. Custo estimado: cerca de 140 créditos no Fast.

### Cena 2 · Promotor acusa (Ingredientes: fotos 4, 6 e 7 do Dr. João)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain, realistic skin texture. Old courtroom with dark wood paneling, warm daylight through tall arched windows, dust in the air. The man from the reference images, wearing a plain black dress shirt, sits still at the defendant's bench, silent, mouth closed. A Brazilian prosecutor, around 50, charcoal grey suit, burgundy tie, walks into frame and points at him, saying in Brazilian Portuguese with an indignant voice: "Meritíssimo, ele vai vender todos os cursos por um preço só!" The audience reacts with surprise. Only the prosecutor speaks. No subtitles, no music.
```

### Cena 3 · Testemunha 1 (Texto para vídeo)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain, realistic skin texture. Old courtroom with dark wood paneling, warm daylight through tall arched windows. A Brazilian woman around 30, brown hair tied back, beige blazer, sits on the witness stand, slightly embarrassed but sincere. She says in Brazilian Portuguese: "Eu fiz curso de fim de semana. Saí com certificado e sem saber em que camada estava a minha cânula." Medium close-up. No subtitles, no music.
```

### Cena 4 · Testemunha 2 (Texto para vídeo)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain, realistic skin texture. Old courtroom with dark wood paneling, warm daylight through tall arched windows. A Brazilian woman around 35, short black hair, crisp white shirt, firm and confident, on the witness stand. She says in Brazilian Portuguese: "Com ele, eu aprendi anatomia em cadáver fresco. Hoje eu planejo antes de injetar." Medium close-up. No subtitles, no music.
```

### Cena 5 · Promotor, pós-graduação (Ingredientes: print do promotor)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain. The prosecutor from the reference image walks in front of the judge's bench in the same old courtroom, gesturing with indignation, and says in Brazilian Portuguese: "E não para aí, Meritíssimo. Ele vai incluir a pós-graduação!" In the background, the judge takes off his glasses, surprised. No subtitles, no music.
```

### Cena 6 · Promotor, cursos futuros (Ingredientes: print do promotor)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain. Close-up of the prosecutor from the reference image turning toward the audience in the same old courtroom, voice rising, saying in Brazilian Portuguese: "E os cursos que ele ainda nem gravou!" The audience stirs, someone stands up in the shadows. No subtitles, no music.
```

### Cena 7 · Juiz pergunta (Ingredientes: print do juiz da cena 1)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain. Low-angle shot of the judge from the reference image at the bench in the same old courtroom, serious. He says in Brazilian Portuguese: "O réu tem algo a declarar?" Then total silence, dust floating in the warm light. No subtitles, no music.
```

### Cena 9 · Sentença (Ingredientes: print do juiz da cena 1)
```
Vertical 9:16. Live-action cinematic footage, shot on ARRI Alexa, natural film grain. The judge from the reference image looks toward the defendant, pauses, and says in Brazilian Portuguese: "Sentença: vinte de outubro." He strikes the wooden gavel. Final close-up of the gavel in slow motion as the warm light fades to black. No subtitles, no music.
```
