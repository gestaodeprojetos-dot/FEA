# FEA · Motion da tela de descanso (Elite Injectors Congress 2026)

Transforma a arte estática do painel de LED (4032x1344) em loop de vídeo de 15 s, sem IA generativa: os pixels dos palestrantes e do logo são os originais, só a animação é feita por código.

## Pipeline

1. `fea_seg.py`: gera a máscara de recorte dos palestrantes (modelo BiRefNet via `rembg`, só máscara, não altera pixels).
2. `fea_layers.py`: separa 3 camadas (palestrantes, logo, fundo) e preenche o fundo atrás das pessoas (inpaint OpenCV clássico).
3. `fea_motion.py`: anima e exporta. `preview` gera quadros de teste, `render <saida.mp4>` gera o vídeo.

```bash
python3 fea_seg.py <pasta_trabalho>
python3 fea_layers.py <pasta_trabalho>
python3 fea_motion.py <pasta_trabalho> render saida.mp4
```

A pasta de trabalho precisa de `src/descanso.png` (arte original 4032x1344).

## Animação

| Camada | Movimento |
|---|---|
| Fundo | zoom lento de respiração, deriva lateral, pulso de luz no T de neon, varredura de luz diagonal por loop |
| Partículas | poeira de luz azul subindo, atrás e na frente dos palestrantes |
| Palestrantes | contra-paralaxe sutil (profundidade) ancorada na base |
| Logo | fixo, halo suave e brilho especular passando pelas letras |

Todos os movimentos são periódicos em 15 s: o loop repete sem corte visível.

Saída: MP4 H.264, 4032x1344, 30 fps, yuv420p (o vídeo não vai para o Git, fica no Drive na pasta MOTION do evento).
