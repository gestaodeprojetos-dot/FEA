# FEA · Roteiro URA "Ao vivo" MTB (Black Friday Vitalícia)

Disparo: URA às 20h, dia da Masterclass em Toxina Botulínica (doc "MTB 11/26 URA + SMS").
Voz: clone HeyGen "FEA Dr João Pithon (Black 2026)", engine padrão (HeyGen Voice).
Versão vigente: **v6** (100% voz real do Dr. João), 29,0 s. Ver seção v6 no fim.

## Original (AO-VIVO-MTB.mp3, 28,7 s)

> Masterclass em Toxina Botulínica. Estou ao vivo agora ensinando as novas técnicas de Toxina Botulínica, abordando as diferenças entre as marcas e trazendo todas as atualizações que eu tenho visto aí nos principais congressos do mundo. Então não fique de fora, eu estou ao vivo no Zoom. Para você entrar nessa aula agora, você vai clicar no link da minha bio que está disponível. São somente 3 mil vagas disponíveis no Zoom. Então esteja lá agora antes que as vagas se esgotem.

## Copy aprovada (v3 e v4)

> Masterclass em Toxina Botulínica. Eu estou ao vivo agora, ensinando nove técnicas avançadas de toxina, as diferenças entre as marcas e as atualizações que eu tenho visto nos principais congressos do mundo. E quem estiver comigo ao vivo vai ter acesso a uma oferta exclusiva da Black Friday Vitalícia, só para quem estiver na aula. Para entrar, clique no link da minha bio. São somente três mil vagas no Zoom, então entre agora, antes que elas se esgotem.

Ajustes pedidos pela Keila (06/11/2026) sobre a v2: o Dr. João não fala tão empolgado, e numa ligação pausa longa faz a pessoa desligar.

- Sem exclamações e sem pausas forçadas: tom firme, de autoridade, no registro do áudio original.
- Frases ligadas por vírgula, fala a 1,05x e silêncio entre frases encurtado para no máximo 0,15 s na edição.
- Mesmo conteúdo da v2, com a Black Friday Vitalícia antes do CTA.

## v4: tratamento de voz (substituída)

Pedido da Keila (06/11/2026): voz do Dr. João pouco presente e áudio abafado. Medição com `fea_espectro_voz.py`: energia concentrada em 300 a 1000 Hz e faixa de clareza da fala (1 a 3,4 kHz) 13 a 21 dB abaixo; na versão de URA, o MP3 a 24 kbps tirava ainda mais nitidez.

- Equalização: corte de grave abaixo de 90 Hz, -3 dB em 220 Hz e 450 Hz (embolado), +3 dB em 1,5 kHz, +6 dB em 2,8 kHz (presença), +3 dB acima de 5 kHz (ar).
- Compressão leve (3:1) para a voz ficar na frente e constante, volume final a -14 LUFS (2 dB acima da v3).
- Versão de telefone: banda de 250 a 3700 Hz com +2 dB em 3 kHz, 8 kHz mono, MP3 a 64 kbps (antes 24 kbps) e WAV sem compressão.
- Resultado medido: faixa de 2 a 3,4 kHz subiu de -21 dB para -10 dB; cortes idênticos aos da v3.

## Histórico

- **v3** (substituída): copy e cortes aprovados, mas voz abafada.
- **v2** (descartada): exclamações e pausas de 0,3 a 0,8 s. Ficou eufórica e lenta para uma ligação. Arquivos no histórico do git.

## Arquivos

| Arquivo | Uso |
|---|---|
| `FEA-AO-VIVO-MTB-v4-BlackVitalicia.mp3` | Master 44,1 kHz, 192 kbps, para ouvir e aprovar |
| `FEA-AO-VIVO-MTB-v4-BlackVitalicia-URA-8kHz.mp3` | Para a URA: 8 kHz mono, 64 kbps |
| `FEA-AO-VIVO-MTB-v4-BlackVitalicia-URA-8kHz.wav` | Para a URA, se a plataforma aceitar WAV (melhor qualidade em 8 kHz) |

## v5: semelhança com a voz do Dr. João (substituída)

Retorno da Keila (06/11/2026): a v4 não ficou mais parecida com a voz dele. A equalização mexe só em brilho, não em timbre.

Medições (`fea_similaridade_voz.py` para timbre, pYIN para tom), sempre contra o áudio original da URA:

| Versão | Tom mediano | Semelhança de timbre |
|---|---|---|
| Voz real (original) | 133 Hz | referência |
| Clone, motor padrão, sem tratamento (v3) | 188 Hz | 0,865 |
| v4 (com equalização) | 188 Hz | 0,806 |
| Clone, motor Starfish | 182 Hz | 0,848 |
| Clone, motor ElevenLabs | 165 Hz | 0,765 |
| Clone com tom -3 semitons | 158 Hz | 0,769 |
| Clone com tom -5 semitons | 142 Hz | 0,734 |

Conclusão: o clone "Black 2026" fala cerca de 5 semitons acima da voz real em todos os motores. Baixar o tom aproxima a altura, mas o processamento piora o timbre.

Opções em `FEA-opcoes-v5/` para escolha de ouvido:

- **A, voz real do Dr. João (29,1 s, 8 kHz):** trechos do áudio original + só a frase da Black Friday Vitalícia gerada pelo clone, com tom ajustado (139 Hz) e passada pelo mesmo filtro de telefone. Volta à copy original nos trechos reais ("novas técnicas", "Para você entrar nessa aula agora, você vai clicar no link da minha bio"). Cerca de 75% do áudio é a voz real.
- **B, clone com tom médio (-3 semitons, 23,7 s):** copy e cortes da v3.
- **C, clone com tom grave (-5 semitons, 23,7 s):** copy e cortes da v3.

## v6: 100% voz real do Dr. João (vigente)

Retorno da Keila (06/11/2026) sobre a v5: a opção A agradou, mas a frase do clone soou "bizarra". Quer só a voz real.

Montagem com `fea_montar_voz_real.py` e `FEA-plano-v6.json`, todos os trechos gravados por ele:

> Masterclass em Toxina Botulínica. Estou ao vivo agora ensinando as novas técnicas de toxina botulínica, abordando as diferenças entre as marcas e trazendo todas as atualizações que eu tenho visto aí nos principais congressos do mundo. **[Ads 028 - BFV] Essa é a tua oportunidade de participar da Black Friday Vitalícia.** Eu estou ao vivo no Zoom. Para você entrar nessa aula agora, você vai clicar no link da minha bio. São somente 3 mil vagas disponíveis no Zoom. Então esteja lá agora antes que as vagas se esgotem.

- Fonte da frase nova: Ads 028 - BFV (gravação crua, ruído de fundo -51 dB). Ads 014 e 016 têm "você precisa estar ao vivo", mas com trilha por baixo.
- Trecho novo passado pela mesma cadeia de telefone (8 kHz, MP3 24 kbps), com equalização casada ao espectro do original e volume igualado.
- Semelhança de timbre da frase nova com a voz original: 0,78 (o clone da v5 dava 0,675).
- 29,0 s. Transcrição do arquivo final confere palavra por palavra.
- Busca em 22 gravações da campanha BFV: nenhuma tem "oferta exclusiva para quem estiver ao vivo". Para deixar explícito, o Dr. João precisa gravar a frase.
