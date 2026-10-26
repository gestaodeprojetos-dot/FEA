# FEA · Tradução ES · Parte 5 (p. 149 a 185) · Relatório

Entrada: `parte5-pt.json` (567 blocos). Saída: `parte5-es.json` (430 ids traduzidos, 137 omitidos).

Omitidos: números de página, "JOÃO P I T HO N" / "JOÃO PITHON", bullets "•" isolados, letras de painel de figura "A", "B", "C", "D" (p158_03 a p158_06).

## (a) Termos novos, fora dos glossários

| PT | ES escolhido | Observação |
|---|---|---|
| abscesso / abscesso estéril | absceso / absceso estéril | consistente com módulo 15 |
| necrose liquefativa | necrosis licuefactiva | |
| coleção purulenta | colección purulenta | |
| flutuação / flutuante | fluctuación / fluctuante | |
| sinais flogísticos | signos flogísticos | |
| multisseptado | multitabicado | uso radiológico em ES |
| partes moles | partes blandas | |
| ultrassom / ultrassonográfico (exame) | ecografía / ecográfico | uso clínico LatAm; o glossário cobre só "ultrassom microfocado" (tecnologia), que é outra coisa |
| exame de cultura e antibiograma | cultivo y antibiograma | |
| AINEs | AINE | sigla invariável em ES |
| MRSA | MRSA | mantido (SARM também existe em ES, preferi não alterar sigla) |
| TNF- (α perdido) | TNF-alfa | ver (b) |
| BDDE (1,4-butanediol diglycidyl ether), DVS (divinyl sulfone) | BDDE (1,4-butanodiol diglicidil éter) y DVS (divinilsulfona) | nomes químicos em nomenclatura ES; siglas mantidas |
| chave-fechadura | “llave-cerradura” | |
| compressas mornas / geladas | compresas tibias / frías | |
| bochecho | enjuagues | |
| aguardo expectante | conducta expectante | |
| retrabalho planejado | retratamiento planificado | |
| festoon | “festoon” | mantido em inglês, como no PT |
| swelling factor / swelling | swelling factor / swelling | mantido, conforme 90-decisiones |
| sulco naso-jugal | surco nasoyugal | glossário núcleo |
| ligamento de retenção orbitário | ligamento retenedor orbitario | glossário núcleo |
| tecido orbital | tejido orbitario | |
| 3x/dia, 2x/dia, 5x/dia, 2x ao dia | 3x/día, 2x/día, 5x/día, 2x al día | notação mantida (não é conversão autorizada) |
| 7–10 dias | 7 a 10 días | convenção de faixa do núcleo §9; números idênticos |
| 12/12 horas, 8/8h, 6/6h | cada 12 h, cada 8 h, cada 6 h | conversão autorizada |

## (b) Erros de digitação e ambiguidades do original PT

| id | No PT | O que fiz |
|---|---|---|
| p151_07, p151_09, p161_03, p169_12, p154_07 | Seta "→" ausente na camada de texto do PDF ("Inflamação aguda recrutamento de neutrófilos"); conferido no original.pdf: não há glifo nem espaço reservado, a seta se perdeu na fonte | Substituí por conector textual (":", "y", vírgulas, ";"), sem inserir "→" (risco de glifo ausente) |
| p161_04 | "TNF-" (α perdido) | "TNF-alfa" (forma ES válida; evita glifo α que a fonte não tem) |
| p166_03 | Lista sem conjunção: "BDDE (...), DVS (...)" | "el BDDE (...) y la DVS (...)" |
| p176_13 | Parêntese de fechamento sobrando: "...associado)" | Removido |
| p184_03 | "podese" | "puede realizarse" |
| p165_14 | "Corticóides" (acento antigo) | "Corticoides" |
| p166_05 | "auto-limitada" | "autolimitada" |
| p174_11 | "mandíbulas" (plural) | "mandíbula" |
| p181_05 | Sujeito ausente: "realizou uma perfuração" | "se realizó una perforación" |
| p159_06 | Triancinolona sem dose (o PT não traz) | Mantido sem dose; não inventei |
| p149_12 / p154_05 | Piperacilina/tazobactam 4,5 g cada 6 h; o glossário 15 cita 3,375 g de outro trecho do livro | Mantido 4,5 g, idêntico ao PT. Sinalizar ao autor se a diferença entre capítulos é intencional |
| p175_12 | "sombra sob os olhos (Tyndall effect)": efeito Tyndall costuma ser descrito como coloração azulada, não sombra | Traduzido fielmente; ponto clínico para o autor |
| p185_03 | Referência com páginas "218-2222" (provável 218-222) | Referência não traduzida nem corrigida (regra de citação); sinalizar ao autor |
| p168_03, p185_03 | Fonte bibliográfica em PT (livro Neville; artigo Cavallieri) | Título da obra/artigo mantido no original; só "Fonte:" e "Adaptado de/por IA" traduzidos |
| p150_20 / p151_02, p163_08 / p164_02, p173_07 / p174_02 | Hifenização do InDesign entre páginas ("encap-/sulada", "alopuri-/nol", "significa-/tivamente") | Palavra juntada inteira no primeiro bloco; o bloco seguinte começa na palavra seguinte. Nenhum outro texto foi movido entre ids |
| p167_06 a p167_13 | Linha justificada partida palavra a palavra ("pela", "reativação", "do", "vírus", "Herpes", "simplex") | 1:1 mantido: "por la", "reactivación", "del", "virus", "herpes", "simple" |

## (c) Ids de display

- **p173_02 / p173_03**: capitular de abertura do capítulo 5. PT "A" + "s intercorrências..." → ES "<b>L</b>" + "as intercurrencias...". **display**.

## (d) Auditoria

Passagem 2: `auditar.py` sobre os 430 valores ES (tags removidas).

- 1ª rodada: RETIDO, 1 classe A ("sugiere" capturado pela regra de futuro do subjuntivo, falso positivo). Reescrito para "es sugestivo de" (mais fiel ao PT).
- **Rodada final: LIBERADO, 0 classe A, índice 97,2 % (417/429), 12 GRAVE + 1 MENOR, todos falsos positivos:**
  - "decimal com ponto" em numeração de seção (4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3): é numeração, não decimal.
  - "decimal com ponto" e "aspas retas" na linha p185_03: dentro da referência bibliográfica (volume 9.3, título entre aspas), que não se traduz.
  - "el mismo pronome" em "en el mismo sitio" (p161_07, p169_13, p175_15): uso adjetival correto; a lista de exceções da regra não inclui "sitio". Sugestão: acrescentar `sitio|lugar` à exceção no auditar.py.

Checagens extras: JSON carrega com `json.load`; zero em-dash; zero «», ¡, ¿; aspas curvas “ ” mantidas; bullets "•" na mesma posição em todos os ids; todo bloco com negrito tem `<b>`.

Comprimento: 11 blocos curtos ficam entre 16 % e 22 % acima do PT, todos com diferença absoluta de 5 a 12 caracteres (termos impostos pelo glossário, p. ej. "ácido clavulánico", ou artigo obrigatório em ES). Nenhum parágrafo longo passa de 15 %.

Passagem 3 (back-translation de doses, unidades, vias, posologia, planos, lados e negações): comparação automática de todos os números PT × ES (única diferença: 12/12h → cada 12 h e equivalentes, autorizada) e revisão manual de todas as negações ("no isquémica", "no presenta", "no fluctuante", "no nodular", "que no responden", "no fue/es necesaria", "no haya riesgo", "(no afectada)"), lados (p185_03 esquerda/direita, p183_04 acima/abaixo, p174_14 e p175_03/05 direções de migração) e vias (EV → IV em p149_11, p149_12, p154_03, p170_11). Nenhuma divergência.
