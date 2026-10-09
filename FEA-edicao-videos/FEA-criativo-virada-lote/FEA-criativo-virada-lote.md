# FEA: criativos de virada de lote (Elite Injectors Congress)

Lote de 09/10/2026: 8 vídeos do Dr. João (pasta de brutos `1Q4ladeqsLvecjVwZ2_weQrytd7-fG98J`), um para cada dia
até a virada do 1º lote (quarta, 14/10). Teste aprovado pela Keila ("amei, pode seguir"), com trilha de fundo baixa
pedida depois. Entrega na pasta `1D8P1wSqZcKqbWRAePG3fwYln7_fZCg_j`. O teste original (`FEA-editados-TESTE`) fica
como está, não apagar.

| Bruto | Fala de abertura | Arquivo entregue |
|---|---|---|
| IMG_7584 | Faltam 4 dias | FEA-Elite-virada-de-lote-4-dias-A.mp4 |
| IMG_7586 | Em 4 dias | FEA-Elite-virada-de-lote-4-dias-B.mp4 |
| IMG_7587 | Em três dias | FEA-Elite-virada-de-lote-3-dias.mp4 |
| IMG_7588 | Dois dias para ficar mais caro | FEA-Elite-virada-de-lote-2-dias-A.mp4 |
| IMG_7589 | Dois dias, tendências científicas | FEA-Elite-virada-de-lote-2-dias-B.mp4 |
| IMG_7590 | Dois dias, sold out | FEA-Elite-virada-de-lote-2-dias-C.mp4 |
| IMG_7591 | Amanhã | FEA-Elite-virada-de-lote-amanha.mp4 |
| IMG_7593 | Hoje | FEA-Elite-virada-de-lote-hoje.mp4 |

## Estilo

Referência: Reel enviado pela Keila (doutor falando alternado com telas cheias animadas, legenda palavra a palavra
com a palavra da vez em dourado). Visual da página de vendas, por continuidade anúncio → página:
fundo `#050C0F` com brilho `#7FB3C6`, dourado do botão (`#E9D68E` → `#D4B760` → `#A58036`), vermelho só em
"valor sobe", "última chance" e "restam poucas vagas". Fraunces no lugar da Canela Deck (paga) e Montserrat no lugar
da Galano Grotesque. Logo e cards dos palestrantes baixados do próprio site.

Todo número na tela vem da página de vendas: 14/10 ("Dia 14/10 o valor sobe"), 87% das vagas, 01 e 02/11,
WTC Sheraton. A cartela final diz "O 1º lote vira em 14/10" (e não "preço até 14/10", porque no dia 14 já é o
valor novo).

## Cenas disponíveis (`fea_configs.py`)

| Tipo | O que mostra |
|---|---|
| `gancho` | cartão no topo: número virando (5 → 4 dias) ou calendário (13 → 14 "amanhã", 14 pulsando "hoje") |
| `logo` | tela cheia com o logo Elite, brilho passando e "Tendências Globais. Evidências Reais." |
| `celular` | a página de vendas real num celular, rolando, com contador e selos (data, local, menor valor) |
| `palestrantes` | 6 cards de palestrantes da página + itens com check sincronizados com a fala |
| `lote` | barra do 1º lote até 87% (`barato`) ou "restam poucas vagas" pulsando em vermelho (`poucas`) |
| `saiba` | seta e botão "Saiba Mais" com toque, quando ele fala "clica em Saiba Mais" |
| `virada` | calendário virando as folhas até 14 (quarta), ingresso "1º lote" vira "2º lote", carimbo |
| `final` | cartela com logo, data, local, "o 1º lote vira em 14/10", botão e "Toque em Saiba Mais" |

`zoom` são os trechos com zoom no rosto do doutor (contraste de ritmo). Legendas: agrupadas por frase, sem
quebrar "Elite Injectors Congress", "São Paulo", "sold out", "te vejo lá"; "pra" vira "para", "Sabamais" vira
"Saiba Mais", "mediano" vira "mediando", "ó" sai.

## Áudio (`fea_audio.py`)

Efeitos discretos (whoosh nas telas cheias, tique nas folhas do calendário, impacto no carimbo, pop nos selos) e
trilha sintetizada no próprio script (sem banco de música, sem risco de direito autoral): pulso grave tipo batida de
coração, relógio, pad em lá menor e ostinato, com subida e impacto na virada do lote e na cartela final. Na montagem a
trilha entra a 20% e abaixa sozinha quando o doutor fala (`sidechaincompress`).

## Como rodar

1. Transcrever (`../fea_transcrever.py`) e capturar a página (`node fea_capturar_pagina.js PASTA`, recortar o topo
   de `full.png` em `pagina.jpg`).
2. Ajustar os tempos em `fea_configs.py` e gerar os JSON: `python3 fea_configs.py PASTA_TR PASTA_TRABALHO/cfg`.
3. `bash fea_lote.sh PASTA_TRABALHO IMG_7584 ...` (quadros, áudio e montagem; uns 4 min por vídeo, rodar em 3
   processos paralelos).

A pasta `comp/` precisa de `FEA-composicao-virada-lote.html`, `logo.png`, `pagina.jpg`, `card-*.png` e `../fonts`
(Montserrat + Fraunces).
