# FEA: criativo de virada de lote (Elite Injectors Congress)

Teste de 09/10/2026: vídeo IMG_7584 ("Faltam 4 dias"), pasta de brutos `1Q4ladeqsLvecjVwZ2_weQrytd7-fG98J`.
Saída no Drive: subpasta `FEA-editados-TESTE` da mesma pasta. Referência de estilo: Reel enviado pela Keila
(talking head alternando com telas cheias animadas, legenda palavra a palavra com destaque).

## Identidade

Visual da página de vendas do congresso (escolhido por continuidade anúncio → página):
fundo `#050C0F` com brilho `#7FB3C6`, dourado do botão (`#E9D68E` → `#D4B760` → `#A58036`),
vermelho só no "valor sobe" e no ponto de "restam poucas vagas". Serifada Fraunces (no lugar da Canela Deck,
que é paga) e Montserrat (no lugar da Galano Grotesque). Logo: `ELITE-3D_imagotipo-copiar.webp` do site.

## Roteiro do teste (tempos do bruto)

| Trecho | Fala | Gráfico |
|---|---|---|
| 0 a 2,5 s | "Faltam 4 dias para virada de lote" | cartão com número flip 5 → 4 "dias para a virada de lote" |
| 2,5 a 4,3 | "do Elite Injectors Congress" | tela cheia: logo com brilho, "Tendências Globais. Evidências Reais." |
| 4,4 a 7,2 | "o maior congresso..." | zoom no rosto |
| 7,3 a 10,8 | "1 e 2 de novembro, aqui em São Paulo" | celular com a página real rolando, contador correndo, chips de data e local |
| 10,8 a 15 | "primeiro lote, lote mais barato" | barra do 1º lote enchendo até 87% (dado da página) |
| 15 a 16,6 | "clicar aqui em Saiba Mais" | seta + botão "Saiba Mais" com toque |
| 16,6 a 19,6 | "em 4 dias vira o lote, vai ficar mais caro" | calendário 10 → 14 (quarta), ingresso 1º lote vira para 2º lote, carimbo "valor sobe" |
| 19,7 a 22,7 | "sold out, encerramos as inscrições" | "restam poucas vagas no lote atual", 87%, pulso vermelho |
| 22,7 a 26 | "espero vocês lá" | cartela final: logo, 01 e 02/11, WTC Sheraton, "preço do 1º lote até 14/10", botão |

Todo número na tela vem da página de vendas (14/10, 87%, 01 e 02/11, WTC Sheraton). Nada inventado.

## Como refazer para outro vídeo

1. Transcrever (`fea_transcrever.py`) e montar `legendas.json` agrupando por frase ("pra" vira "para").
2. Capturar a página: `node fea_capturar_pagina.js PASTA` (gera `full.png`; recortar o topo em `pagina.jpg`).
3. Ajustar os tempos das cenas em `FEA-composicao-virada-lote.html` (função `render(t)`) e no `fea_sfx.py`.
   Para "3 dias", "amanhã" e "hoje", trocar o número do flip e os dias do calendário.
4. `node fea_render_quadros.js PASTA_COMP PASTA_QUADROS "all:DURACAO"` (cerca de 3 min para 26 s).
5. `python3 fea_sfx.py sfx.wav DURACAO` e `bash fea_montar.sh BRUTO QUADROS sfx.wav SAIDA.mp4 DURACAO "ZOOM"`.

A pasta de composição precisa de `logo.png`, `pagina.jpg` e da pasta `../fonts` (Montserrat + Fraunces).
