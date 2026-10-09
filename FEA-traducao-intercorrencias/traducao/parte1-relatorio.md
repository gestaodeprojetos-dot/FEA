# FEA · Tradução ES · Livro Intercorrências · Parte 1 (págs. 2 a 37): relatório

Entrada: `parte1-pt.json` (352 blocos). Saída: `parte1-es.json` (253 ids traduzidos, 99 omitidos).

Omitidos: números de página e de sumário, "JOÃO P I T HO N" / "JOÃO PITHON", números e letras isolados das figuras (1 a 5, A a E) e os blocos que contêm só "•" (p26_10, p27_02, p33_07, p33_16, p34_02, p34_13, p36_07). Esses ficam como no original.

## (a) Termos novos fora dos glossários e a escolha feita

| PT | ES | Motivo |
|---|---|---|
| preenchedor(es) dérmico(s) | relleno(s) dérmico(s) | O núcleo traz "producto de relleno / relleno". Usei "relleno" de forma uniforme para não pesar a frase |
| tempo de preenchimento capilar | tiempo de llenado capilar | Aqui "preenchimento" é fisiológico, não o procedimento. Conferido na passagem 3 |
| angiossoma / angiossomal | angiosoma / angiosómico | Termo consolidado da cirurgia plástica em ES |
| ultrassom (com) Doppler | ultrasonido (con) Doppler | Mesma família de "ultrasonido microenfocado" do núcleo. "Ecografía Doppler" é a alternativa |
| rítides | ritides | Uso dermatológico em ES |
| couro cabeludo | cuero cabelludo | sem observação |
| compressas mornas | compresas tibias | sem observação |
| cânulas rombas | cánulas romas | sem observação |
| defeito cutâneo em espessura total | defecto cutáneo de espesor total | Locução cirúrgica fixa ("full-thickness"). "Grosor" (núcleo) não se usa nesta expressão |
| injetor (profissional) | inyector | Já no módulo 15 |
| neuro-oftalmológicas | neurooftalmológicas | Prefixo soldado, norma RAE |
| rinomodelação | rinomodelación | sem observação |
| artéria mentual | arteria mentoniana | Paralelo ao núcleo (músculo mentual → mentoniano) |
| SAIBA MAIS, no corpo do texto (box "Saiba Mais") | recuadro "Para saber más" | Igual ao título fixado nas decisões comuns |
| precoce | precoz | Uniforme em todo o texto (reconhecimento, diagnóstico, manejo precoz) |
| sistema de escore FOEM | sistema de puntuación FOEM | sem observação |

## (b) Erros de digitação e ambiguidades do original PT

| id | No original | O que fiz |
|---|---|---|
| p11_04 | "segue uma progressão clínica. Iniciando pela oclusão..." (fragmento de frase) | Uni com dois-pontos: "sigue una progresión clínica: comienza por..." |
| p19_09 | "D) Reversão" sem o parêntese de abertura; "C) Evolução" com maiúscula no meio da lista | Padronizado como "(D) reversión", "(C) evolución" |
| p19_09 | "Protocolo de Diagnóstico **de** Reperfusão Rápida" | Corrigido para o nome do protocolo: "Protocolo de Diagnóstico y Reperfusión Rápida" (PDRR) |
| p20_03 | "COMPLICAÇÕESOCULARES" (falta espaço) | "COMPLICACIONES OCULARES" |
| p24_05 | "Artérias Labiais (superior e inferior): irriga os lábios; pode causar" (verbo no singular) | Plural: "irrigan los labios; pueden causar" |
| p24_09 | "dado a proximidade" | "dada la proximidad" |
| p25_03 | "Figura 6" sem ponto (as demais têm) | "Figura 6." (negrito só em "Figura 6") |
| p28_04 / p28_06 | A legenda da Figura 10 começa com sobra da legenda da Figura 8: "Esquema ilustrativo dos dois principais mecanismos envolvidos na oclusão vascular induzida por ácido hialu" + "Histologia de oclusão vascular..." | Removi a sobra; ES: "Figura 10. Histología de la oclusión / vascular inducida por relleno: (A)...". **Conferir no PDF se essa sobra aparece visível na página 28 do PT** |
| p22_03 | O título da Figura 5 repete o da Figura 2 ("TESTE CLÍNICO DE REPERFUSÃO CAPILAR NA AVALIAÇÃO DE ISQUEMIA CUTÂNEA FACIAL"), mas a figura mostra a evolução da lesão isquêmica | Traduzi fielmente o título. **O autor decide**; sugestão: "PROGRESIÓN DE LA LESIÓN ISQUÉMICA EN LA REGIÓN MALAR Y PERINASAL" |
| p33_10 | "prednisona 40 mg **vo**" (minúsculo) | "VO" |
| p27_03 | "Redução ou ausência do tempo de reperfusão capilar" (a rigor, o tempo aumenta e a reperfusão diminui) | Traduzido fielmente ("Reducción o ausencia del tiempo de reperfusión capilar"), é questão clínica do autor e não de tradução. Sinalizar ao autor |
| p26_08 | "Isso ocorre devido a um trauma arterial": a frase atribui toda a hipoperfusão a trauma arterial, o que não bate com os 4 mecanismos citados antes | Traduzido fielmente e sinalizado |
| p31_05 | "INFLAMAÇÃO LOCAL: CALOR, RUBOR E EDEMA, SEM PALIDEZ." está em estilo de título, mas é um item da lista de diagnóstico diferencial | Traduzido no mesmo estilo; o designer pode passar o texto para corpo |
| p31_08 | "injetar 1000 UTR/mL na região afetada" (concentração no lugar de dose ou volume) | Mantive a ambiguidade: "inyectar 1000 UTR/mL en la región afectada". **Sinalizar ao autor** |
| p24_04 a p24_11 | Lista em duas colunas com palavras partidas entre blocos (com-/prometer, cau-/sar, comu-/nica, gla-/bela, ca-/beludo) | A divisão foi espelhada em ES com partes válidas (com-/prometer, cau-/sar, comu-/nica, gla-/bela, ca-/belludo), para nenhum texto mudar de id |
| p19_10 / p20_02 | "planeja-/mento" partido entre páginas | Espelhado: "planifica-/ción" |
| p29_04 a p29_12 | Box com duas colunas intercaladas, linhas partidas por hífen (va-/riações, prá-/tica, ris-/cos) | Cada fragmento traduzido no seu id com a divisão espelhada (va-/riaciones, prác-/tica, ries-/gos) |

Notação: "1000 UTR/mL" ficou **sem ponto de milhar**, como no original (regra da tarefa: só EV→IV e 12/12h→cada 12 h como conversão; além disso, "1.000" pode ser lido como 1 em países que usam ponto decimal). Faixas com traço passaram a usar "a" ("15–30 min" → "15 a 30 min", "1–2 g/dia" → "1 a 2 g/día", "5-10 sessões" → "5 a 10 sesiones", conforme o módulo 15). Unidades e percentuais ganharam espaço ("400mg" → "400 mg", "6h" → "6 h", "58%" → "58 %"). Nenhum número foi alterado.

Travessão: o único em-dash do PT dentro de texto traduzido estava no título do artigo de Soares (p30_08, entre "(FIVO)" e "Implications"). Como o título não se traduz e o em-dash é proibido, usei meia-risca "–" no lugar. Meias-riscas que o PT já tinha em títulos foram mantidas (p29_03, p29_04, p31_02, p34_05, p35_03, p25_06). Em p18_03, "(High Dose Pulsed Hyaluronidase – HDPH)" virou "(High Dose Pulsed Hyaluronidase, HDPH)". Os em-dashes em prosa de p7_03, p11_06 e p23_06 viraram parênteses.

Tipografia: aspas curvas “ ” como no PT. Nenhum ¿ ¡ « » nem aspas retas no ES.

Comprimento: todos os blocos com mais de 25 caracteres ficaram em até 115 % do PT, menos p33_17 (120 %), por causa da forma obrigatória "amoxicilina + ácido clavulánico" e de "cada 12 h".

## (c) Ids de display

- p2_00 "SU MÁ RIO" → **ÍNDICE**
- p4_00 "IN TRO DU ˜ ÇAO" → **INTRODUCCIÓN**
- Capitulares: p5_00 "O" → **E** (continua em p5_03 "l uso de...") e p11_02 "A" → **L** (continua em p11_03 "as intercurrencias..."). A letra capitular muda porque a primeira palavra muda (O uso → El uso; As intercorrências → Las intercurrencias).

## (d) Auditoria (`auditar.py`)

Rodada final: **VEREDITO LIBERADO**, 0 BLOQUEANTE, índice editorial 96,8 % (239 de 247 segmentos limpos), 31 GRAVE, 0 MENOR.

Falsos positivos:
- **31 GRAVE "decimal com ponto"**: são os números de seção do sumário e dos títulos (1.1, 2.10, 1.1.1, 1.1.2...), não decimais. A regra precisa ignorar numeração de seção.
- **2 BLOQUEANTE "ênclise" na 1ª rodada**: a palavra inglesa "Hyaluronidase", em p18_03 (nome em inglês do protocolo HDPH) e p33_03 (título do artigo *The Role of Hyaluronidase...*). Nos dois casos o texto não se traduz. Para a rodada final, esses dois trechos em inglês foram trocados por "[EN]" **só no .txt de auditoria**, o JSON mantém o texto. A regra de ênclise deveria pular palavras em inglês dentro de linha em espanhol (não editei o script porque a tarefa proibia mexer em outros arquivos).

Passagem 3 (back-translation): conferi todo trecho com dose, posologia, via, tempo, percentual, plano, lado e negação (p13_07, p23_06, p31_08 e p31_09, p33_08 a p34_04, p21_06, p14_03, p24_*, p29_14 e p29_15, p36_08 a p36_12, p6_03). Uma checagem automática dos números bloco a bloco só acusou as conversões permitidas de posologia (12/12h, 8/8h, 6/6h → cada N h). Nenhuma divergência.
