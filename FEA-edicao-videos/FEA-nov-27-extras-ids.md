# FEA: pasta 27 de novembro, vídeos 3 a 7 (brutos nunca editados), 23/11/2026

Brutos: pasta "OK. 3mL" (`1K3tRrl5L_u79e4nCZxDNExH8QGEw7OO7`, dentro de BRUTOS `1ikhzNlHAhsVaJ95LGvQ7V3FtwxMmIyO8`). Entrega: pasta "27- 3mL, bigode chinês e lábios" (`1qq0HEvarUr7BGAUBCjnqTUW_oW7WeHKL`). Os vídeos 1- e 2- (IMG_9426 e IMG_9428) não foram tocados. Projeto: `FEA-projeto-nov-27-extras-3-a-7.json`. Regras: estoque SEM CTA (`sem_cta`, `fade_final` 0,3), frase completa no começo e no fim (Keila, 23/11/2026).

Não há imagem de títulos na pasta de brutos: os 5 títulos foram criados pela transcrição e pelos quadros, sem nome de produto. Duplicata conferida pelo MD5 na API do Drive: o outro IMG_9423 do Drive (`20c14ae4...`) é outro arquivo; IMG_9424, 9425, 9427 e 9429 só existem nesta pasta. Nenhuma branch tinha projeto com esses brutos.

| Vídeo | Bruto (MD5 do bruto) | Duração | Drive | MD5 |
|---|---|---|---|---|
| 3- Marcação e assimetria no preenchimento | IMG_9423 (`3bc9c19abc07794dc733c44f6aef0f70`) | 42,5 s | 1jByWeRi0OTAd68QAK447inmeuRD1KiNZ | 3c390fd88df5a75437994d0109cb58f2 |
| 4- Anestesia intraoral com SANEP | IMG_9424 (`8e68500aa1b006527857e51b27ae6443`) | 93,6 s | 1PYUKHWyVKI8STNGqAbWdy7BinXnT3fnO | ec1ac5194b9cfe9c0e3f77c064459380 |
| 5- Terço médio e base da olheira | IMG_9425 (`4f5ebd5d3bd003e8e60fbc30ac296c09`) | 74,8 s | 1-fkDugz3Krst_9Ragu7wC-ZMEWLpfRKp | c66487621edbbe0d266a7708276e109b |
| 6- Preenchimento com cânula 25G | IMG_9427 (`986a55dc8a8a7002a6274bdf471b38b6`) | 56,5 s | 1NqR95rzePCVWlXABS4rzxzIUU2rZ81-k | b3449c9743cb9974fe70283fb9c6261c |
| 7- Preenchimento labial com cânula | IMG_9429 (`f9eca28b5aa87fe33c3e484c17486a3d`) | 98,1 s | 1LGIf8SLajjiXN6qI6mfPZcQJ98RVMGYo | 5abaeb6a20dcc06f57ae3ef24a761995 |

Doc "FEA-Legendas 27- 3mL, bigode chinês e lábios (vídeos 3 a 7)": `1hnwKnawBgE2rhV3nGntMgQmEHeBBOjAhbY3kz1SjmRQ` (o Doc dos vídeos 1 e 2 ficou como estava).

Planilha "🔴 EDIÇÕES", linha 228: quantidade 2 → 7 e observação acrescida (23/11/2026).

## Brutos intermediários (no scratchpad da sessão, refazíveis com os scripts)

- `IMG_9423f.mov`: `fea_pad_fim.sh` corte 71,27 s + 0,35 s ("Perfeito." termina em 71,22 s; depois só estalos até o fim do bruto, 71,9 s).
- `IMG_9424t.mov`: IMG_9424 a partir de 47,45 s (H.264 CRF 10, PCM 48 kHz); `IMG_9424p.mov`: `fea_pad_inicio.sh` 0,37 s sobre ele. Motivo: a respiração antes de "Agora" (46,8 a 47,5 s) emenda no fim de "Perfeito," e não deixava 0,30 s limpos antes da voz (a revisora media a voz em 0,12 s).

## Transcrições corrigidas à mão

As 5 transcrições usadas estão em `FEA-transcricoes-nov-27-extras/` (tempos de palavra medidos no áudio, janelas de 20 ms; texto conferido com o Whisper em trechos curtos com 0,5 s de silêncio em volta). O Whisper da passada longa errava até 1 s no tempo e trocava palavras:
- IMG_9423: diálogo separado por pitch (Dr. ~110 a 130 Hz, paciente ~190 Hz): a paciente diz "Esse lado eu acho um pouco maior do que esse. Esse lado aqui é maior." e "Aí eu não queria, tipo, evidenciar esse maior, porque é o lado que eu durmo, aí fica mais..."; o Dr. diz "Uhum, eu vou equilibrar.", "Deixa comigo.", "Uhum." e "Perfeito." (70,84 s, não 69,87 s). O "Perfeito" de 61,65 s era o "Uhum" do Dr.
- IMG_9424: "Agora no mentoniano" (não "o mentoniano"), "Vira um pouquinho para cá" (faltava "Vira"), "Último botão, o mentoniano direito dela", "anestésico, que é 1,2 mL de lidocaína 2% com vaso" (saiu o "cento" repetido).
- IMG_9425: "já melhorou a olheira dela para a questão que estava incomodando ela", "Essa resistência é colágeno, tá?", "Essa dorzinha, ela é uma dorzinha boa."
- IMG_9427: "Usando a 25... 50... 25G, 50 mm da Vorv." (o Dr. se corrige; marca não confirmada).
- IMG_9429: tempos refeitos de todas as falas mantidas (o Whisper adiantava até 1 s: "Entra no pertuito" está em 43,56 s, não 42,51 s); "Espera um tiquinho, vamos ver como tá." (o "tiquinho" estava esticado de 147 a 160 s).

## Falha de script encontrada (não alterado)

`fea_bordas.py` quebra com `ValueError: too many values to unpack` quando o `manter` já tem `"exato"` (ele passa o `manter` com 3 campos para `checar_frases_borda`, que espera 2). Contornado medindo o ataque e o fim da voz à mão (janelas de 10 a 20 ms) e conferindo com `fea_revisar.py --so-bordas`.
