# FEA: pasta 21 de novembro (3mL, bio e toxina), vídeos 7 a 13 com o CTA MPL "Comente AULA" (18/11/2026)

Pedido da Keila (18/11): nos vídeos 7 a 13, trocar o CTA da Masterclass em Intercorrências (MTI, PR #117) pelo CTA novo da Masterclass em Preenchimento Labial. Os vídeos 1 a 6 já foram postados e ficaram como estavam.

CTA: `Ads 55 - MPL - CTA Comente AULA.mp4` (Drive `1dtLtRVSeSUFdIT57Q0xmuf4s-fxnHQX5`, pasta de criativos `138Q-yhMe7i5VaALx6bQlOvzZ0j70kJv4`, MD5 `0ed25b26e377d1646ba51ba9982ce975`, 25,87 s, H.264 1080x1920 30 fps, AAC 48 kHz), produzido na branch `claude/fea-cta-masterclass-labial`.

Fonte: as versões SEM CTA do PR #111 (estavam na lixeira, baixadas pelo ID; MD5 conferido com o Drive), com a legenda aprovada já queimada. Aplicado com `fea_aplicar_cta_entregue.py` (fade final removido, transição de 0,5 s depois do fim da voz, conteúdo por stream copy até o último quadro-chave e só a cauda recodificada em x264 CRF 18, áudio AAC 192k 48 kHz). Como a fonte não tinha CTA nenhum, não sobra resto do CTA MTI. Todos no modo cauda, PSNR do conteúdo recodificado 48 a 50 dB, do CTA 54 dB, sincronia do áudio ±0,3 ms.

Revisora: `fea_revisar.py --so-formato --folhas` com 0 erro nos 7. Emendas olhadas nos quadros (7, 8 e 9): conteúdo, fusão e card MPL, sem nada do MTI. Upload com MD5 igual ao local em todos; as versões MTI foram para a lixeira depois da conferência.

| Vídeo | ID novo (MPL) | ID antigo (MTI, lixeira) | Conteúdo (s) | Total (s) |
|---|---|---|---|---|
| 7- Por que ninguém paralisa o nasal dela? | `1xqtQ-AnTjtbMRCR7GLJ8u3N2fJNW1ckC` | `1a5hgi559v1bmtZbx9ct0qmhRU5KGS83Q` | 33.57 | 59.54 |
| 8- Planejamento 3mL | `1bGTb47O6XCy4AF2MtVa9CtPEWH8rUu1s` | `1xkCUNHjEcVlItdDh35Z73moizeXCy-kw` | 24.37 | 50.34 |
| 9- Anestesia sem dor | `1jtNGILGkRTYoba4TRiWaZMRHeV0NzA91` | `1dZFq28v9iSn3qMQraMzdZPU0pskcXYzm` | 102.57 | 128.54 |
| 10- Comissura labial | `1JKwJfR-cYhmE3yq5iAPr7hiidweC0a6t` | `1gI4Eps5cwOekUHFStEVs0Re_GqjH4yxJ` | 54.47 | 80.44 |
| 11- Bigode chinês | `1pDFbQDsxG4gDl293joa5N1CBu0Bk29B8` | `17vlVJYcWvwj47-J8q4Mgy2k4N3CnX10n` | 32.57 | 58.58 |
| 12- Mento com cânula | `1mBNLLYHXTSqlPOVXsK5Xkx-zsLW2K7di` | `1ZxRK8zQwwyy9Ew-CRpJwU6Y7mGyX7JCA` | 38.07 | 63.98 |
| 13- Volumax na mandíbula | `1l5VilnW5EUdQCZRZgVKdh0hra49Kc2hV` | `1nauNOM5wH3_SiKcDA8XV9BUxnFlpiTOs` | 34.00 | 59.98 |

Observações:
- A legenda queimada no próprio Ads 55 diz "Existe uma técnica ideal pro preenchimento labial?" ("pro", não "para"). Vem do criativo, não da edição; levar para a Keila se ela quiser trocar no CTA.
- Na pasta 21, o vídeo 2 está hoje como `2- Hidroxiapatita para face` (sem `.mp4`, 133,0 s, ID `1XHNCoUn7zVKiEZ6DzD9JsbWSqaZ7unrD`), diferente do entregue no PR #117 (`1H9OWCN...`, 145,73 s). Não foi mexido aqui.
- Revisora sem a fonte Montserrat ExtraBold na máquina mede a headline por estimativa de caracteres e acusa ERRO falso de margem (vídeo 7: 1404 px). Com a fonte em `/tmp/claude-0/.../fonts/Montserrat-ExtraBold.ttf` a medida volta ao normal.
