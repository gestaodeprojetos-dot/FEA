# FEA · Tradução ES · Parte 6 (pp. 186 a 220) · Relatório

Entrada: `parte6-pt.json` (430 blocos). Saída: `parte6-es.json` (290 ids traduzidos, 140 omitidos).

Os 140 ids omitidos se dividem assim: números de página, "JOÃO P I T HO N" e todos os itens da lista de REFERÊNCIAS (pp. 208 a 220, inclusive as continuações de item partidas entre páginas e o "Disponível em / Acesso em" do item AMERICAN SOCIETY OF PLASTIC SURGEONS). Os blocos que são só "•" foram incluídos como "•", para o bullet ficar na mesma posição. O cabeçalho corrido vai em todas as páginas como "INTERCURRENCIAS EN EL RELLENO CON ÁCIDO HIALURÓNICO".

## (a) Termos novos fora dos glossários e a escolha feita

| PT | ES escolhido | Observação |
|---|---|---|
| festoons | festones | Forma usual em ES clínico |
| ultrassom (Doppler / de partes moles / guiado por) | ecografía (Doppler / de partes blandas) | Uso clínico LatAm; uniformizar com as outras partes se elas tiverem usado "ultrasonido" |
| luz intensa pulsada (LIP) | luz pulsada intensa (LPI) | Sigla recalculada para a forma consolidada em ES |
| microagulhamento | microagujado | Alternativa: "microneedling" |
| clareadores (ativos / tópicos) | aclaradores | "Agentes despigmentantes" mantido onde o PT diz despigmentantes |
| turn-over celular | recambio celular | |
| associação tripla (Kligman modificada) | asociación triple (fórmula de Kligman modificada) | |
| arbutin | arbutina | |
| ácido kójico | ácido kójico | |
| picnogenol / polypodium leucotomos | picnogenol / Polypodium leucotomos | Nome de espécie com maiúscula no gênero |
| ocronose exógena | ocronosis exógena | |
| tatuagem traumática | tatuaje traumático | |
| dismorfofobia / transtorno dismórfico corporal | dismorfofobia / trastorno dismórfico corporal | |
| síndrome do retoque | síndrome del retoque | |
| escuta ativa e acolhimento | escucha activa y acogida | |
| encaminhamento psicológico | derivación psicológica | Falso amigo, conforme 01-voz-y-estilo |
| supraperiostal | supraperióstico | Núcleo |
| swelling factor | swelling factor (minúsculo, como no PT) | Conforme 90-decisiones |
| médico injetor | médico inyector | |
| faixas de valor (2–4%, 3–6 meses, IV–VI, 10–30 UTR, 1–2, 2–3) | "2 a 4 %", "3 a 6 meses", "IV a VI", "10 a 30 UTR", "1 a 2", "2 a 3" | Só a notação mudou (núcleo §9); os números são idênticos |

## (b) Erros de digitação e ambiguidades do original PT

| id | No original | O que foi feito |
|---|---|---|
| p187_10 | "Estimulação dos melanócitos aumento da síntese de melanina": falta um conector (provavelmente uma seta "→" perdida na exportação) | ES: "Estimulación de los melanocitos y mayor síntesis de melanina" |
| p200_15 | "procedimentos repetidos desnecessários fibrose, irregularidades permanentes": mesma seta perdida | ES: "Riesgo de procedimientos repetidos innecesarios, con fibrosis e irregularidades permanentes" |
| p194_14 / p194_15 | Na seção 5.6 (efeito Tyndall), o título e a legenda repetem os da FIGURA 62 (neovascularização no mento). Provavelmente deveria ser a FIGURA 63, sobre Tyndall | Traduzido fielmente como FIGURA 62. **O autor precisa corrigir o título e a legenda** |
| p188_11, p192_09 (e p194_15) | Legenda "Fonte: Imagem gerada/criada por IA" em figura clínica | Traduzido fielmente. **Atenção:** isso conflita com a linha vermelha nº 7 do projeto (nada de imagem de IA generativa em entregável final). Sinalizar ao autor antes de publicar |
| p192_05 vs p192_13 | "Teleangiectasias" e "telangiectasias" no mesmo trecho | Uniformizado em "telangiectasias" |
| p190_07 | "fracionados não ablativos (Er:YAG, ...)": o Er:YAG é em geral um laser ablativo | Traduzido fielmente, sem corrigir a clínica. Fica para o autor avaliar |
| p193_10 | "refração seletiva da luz": o efeito Tyndall é dispersão (espalhamento), não refração | Traduzido fielmente ("refracción selectiva"). Fica para o autor avaliar |
| p186_02, p196_17 | Travessões (—) no PT | No ES viraram parênteses (p186_02) e dois-pontos (p196_17) |
| p186_02 | "naso-jugal" | "nasoyugal" |
| p190_09 | "polypodium" com minúscula | "Polypodium" |
| p187_06 | Faixa "IV–VI" com meia-risca (–) | "IV a VI" |
| p189_21/p190_02 ("turn-/over") e p204_05/p205_02 ("ini-/cial") | Palavra hifenizada pelo InDesign na quebra de página | Junção feita sem hífen: "acelerar el" + "recambio celular"; "después del período" + "inicial del procedimiento". O sentido de cada id continua o mesmo; só a palavra partida inteira passou para um id |
| p205_05/p206_02 | "Mais" + "do que dominar" | "Más" + "que dominar" |

## (c) Ids de display

- **p203_00 / p203_01 / p203_02**: CONCLUSÃO ("CON CLU" / "˜" / "SAO"). Em ES ficou "<b>CON CLU</b>" / "" / "<b>SIÓN</b>". O til avulso (p203_01) virou string vazia, para apagar o glifo, porque o acento de "SIÓN" já vem no próprio texto.
- **p207_00 / p207_01 / p207_02**: REFERÊNCIAS ("RE FE" / "ˆ" / "REN CIAS"). Em ES ficou "<b>RE FE</b>" / "" / "<b>REN CIAS</b>". "REFERENCIAS" não leva acento, então o circunflexo avulso virou string vazia.
- **p204_00 / p204_03**: capitular da conclusão. O "A" + "s intercorrências..." do PT virou "<b>L</b>" + "as intercurrencias...".
- Na produção, confirmar que `traduzir_pdf.py` trata o valor "" como "apagar o original". Se não tratar, usar um espaço.

## (d) Resultado da auditoria

- **auditar.py** (`p6es.txt`, 3.075 palavras): **LIBERADO**, índice de 98,4 %, **0 achados de classe A**, exit code 0.
- Os 4 achados GRAVE de classe B são **falsos positivos**: números de seção "5.4", "5.5", "5.6" e "5.7", lidos como decimal com ponto. Numeração de seção não é decimal, então ficou como está. Sugestão para o script: ignorar o padrão `^\d\.\d+ [A-ZÁÉÍÓÚ]`.
- Termos que a cobertura dá como ausentes ("cigomátic", "retenedor", "grasa", "posprocedimiento"): esses temas não aparecem nesta parte. Não é falha.
- Varredura extra: nenhum travessão (—), nenhum « », ¡, ¿ ou aspa reta; aspas curvas “ ” como no PT; nenhuma faixa com meia-risca; o JSON carrega com `json.load`.
- Nenhum bloco passa de 15 % do comprimento do PT, salvo blocos curtíssimos de lista (p. ex. "Ácido azelaico 10 a 20 %. •", com 4 caracteres a mais).
- **Back-translation (passagem 3)**, sem nenhuma divergência:
  - **Concentrações e doses:** hidroquinona 2 a 4 %, ciclos de 3 a 6 meses, ácido azelaico 10 a 20 %, tretinoína 0,025 a 0,05 %, FPS 50+, Nd:YAG 1064 nm, hialuronidase 10 a 30 UTR, 1 a 2 sessões, 2 a 3 semanas, Fitzpatrick IV a VI.
  - **Planos:** supraperióstico ou submuscular nas olheiras; evitar o subdérmico imediato; HPI epidérmica (camada basal) versus dérmica.
  - **Negações:** "sin dolor ni signos inflamatorios", "no ablativos", "no asociado a traumatismo", "no azuladas", "sin relación con el producto", "puede haber o no", "puede identificar o no", "salvo ante complicaciones claras", "no representa riesgo funcional".
  - **Condutas:** hialuronidase como primeira escolha e tratamento de escolha; evitar massagem e punções repetidas; corticoide sistêmico em ciclo curto. Tudo idêntico ao PT.
- Nenhuma via (EV) nem posologia (x/x h) aparece nesta parte.
