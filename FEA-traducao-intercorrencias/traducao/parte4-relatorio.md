# FEA · Tradução ES · Parte 4 (p. 112 a 148) · Relatório

Entrada: `parte4-pt.json` (598 blocos). Saída: `parte4-es.json` (461 ids traduzidos, 137 omitidos).

Omitidos: 46 blocos só com "•", 37 "JOÃO P I T HO N" / "JOÃO PITHON", 46 números de página e 8 letras isoladas de figura (A, B, C, D em p131 e p140). Os cabeçalhos corridos (legenda/cabecalho "INTERCORRÊNCIAS NO PREENCHIMENTO...") foram traduzidos pela forma fixa.

## (a) Termos novos fora dos glossários e escolha feita

| PT | ES escolhido | Observação |
|---|---|---|
| Síndrome do pânico (título 2.8) | Crisis de pánico / crisis de ansiedad | Segui o módulo 15. No corpo, quando o PT fala do transtorno ("histórico de síndrome do pânico"), usei **trastorno de pánico** |
| Síndrome hipertensiva (título 2.9 e corpo) | Crisis hipertensiva | Segui o módulo 15. O PT distingue depois "crise hipertensiva verdadeira (>180/120 mmHg)": ficou "crisis hipertensiva verdadera", e o adjetivo mantém a distinção. Autor pode querer revisar |
| Trauma arterial | Traumatismo arterial | Módulo 15 |
| hipoglicemia / glicemia capilar | hipoglucemia / glucemia capilar | Forma RAE, corrente na literatura médica LatAm |
| benzodiazepínicos (adjetivo) | benzodiacepínicos | Coerente com "benzodiacepinas" do módulo 15 |
| HAS (hipertensão arterial sistêmica) | HTA | Sigla usual em ES; vem expandida no próprio texto |
| AVC | ACV | Sigla usual em ES (accidente cerebrovascular) |
| ultrassom (Doppler colorido) | ecografía Doppler (color) | Uniforme em todo o trecho |
| curativo | apósito | Uniforme ("apósito compresivo estéril", "apósitos oclusivos/bioactivos") |
| pronto-socorro | servicio de urgencias | |
| sintomas-alvo | síntomas de órgano blanco | |
| semi-recumbente | semisentado | |
| nitroprussiato | nitroprusiato | Grafia ES do fármaco |
| zumbido | acúfenos | |
| clareadores tópicos | despigmentantes tópicos | Coerente com o módulo 15 |
| coleta de cultura | toma de cultivo | |
| AINEs / AGE / PRP | AINE / AGE / PRP | Siglas iguais em ES (AINE invariável) |
| dipirona | dipirona | Mantido (nome do fármaco; em parte da LatAm é "metamizol", não alterei) |
| complacência / pouco complacente | complacencia / poco complaciente | |
| Sociedade Brasileira de Cardiologia | mantido em PT | Nome próprio de instituição |
| antibioticoprofilaxia | profilaxis antibiótica | |

## (b) Erros de digitação e ambiguidades do original PT

| id | Original | O que fiz |
|---|---|---|
| p123_07, p123_08, p124_04, p124_05, p124_06, p136_04 | Setas (→) ausentes na camada de texto: "Lesão parcial da parede extravasamento sanguíneo hematoma pulsátil" | Inseri "→" no ES (mesmo padrão de p114_11, onde a seta foi extraída). **Conferir no render se a seta original continua visível ou se ficou duplicada** |
| p136_08, p140_09 | Título "FIGURA 43. COMPROMETIMENTO ISQUÊMICO EM REGIÃO PERIORAL..." repetido sobre as figuras 44 e 45 (legendas dizem Figura 44 e Figura 45) | Traduzi como está, não inventei título. **Autor deve fornecer os títulos corretos das figuras 44 e 45** |
| p140_14 | "seguida por regressiva progressiva das lesões" | Corrigido: "seguida de regresión progresiva de las lesiones" |
| p140_14 | Rótulo "Figura 45" sem ponto | ES com ponto ("Figura 45."), como as demais |
| p139_06 | "Debridamento" | "Desbridamiento" |
| p134_04 | "Corticóides" (acento) | "Corticoides" |
| p122_04 | "anti hipertensivos" (separado) | "antihipertensivos" |
| p133_15 | "1000 UTR/mL" | "1.000 UTR/mL" (só separador de milhar, convenção do núcleo; valor idêntico) |
| p133_02 | "pela ausência de dor súbita e livedo reticular progressivo, ao invés de imediato" (ambíguo: pode ler-se como ausência também de livedo) | Traduzi pelo sentido clínico evidente (livedo presente, porém progressivo): "por la ausencia de dolor súbito y por un livedo reticular progresivo, en lugar de inmediato". Sinalizar ao autor |
| p118_14 / p119_02 | Palavra "liberação" hifenizada entre páginas ("lib-" / "eração") | Mantida a divisão no mesmo ponto em ES ("li-" / "beración"), sem mover texto entre ids |
| p126_04 | AAS sem expansão | Mantido "AAS": o capítulo 2 já o usou antes (p82_15, p85_16). Em p133_18 (1ª ocorrência do capítulo 3) expandi "AAS (ácido acetilsalicílico)" |

## (c) Ids de display

- **p130_02**: "A" → "L" (abre "as intercurrencias tardías isquémicas...", p130_03)
- **p146_02**: "A" → "L" (abre "as intercurrencias tardías infecciosas...", p146_03)

Capitular passa de "A" para "L" porque o artigo ES é "Las".

## (d) Auditoria

- **Passagem 2 (`auditar.py`)**: 1ª rodada com 1 classe A, falso positivo: regra de ênclise disparou em "Hyaluronidase" dentro do título do artigo em inglês (p131_12). Rodada final sobre o texto ES com as 3 referências bibliográficas em inglês substituídas por marcador (p131_12, p140_14, p143_11): **LIBERADO, 0 classe A, índice 98,7 % (453/459), exit 0**.
- Classe B restante, todos falsos positivos: 6 × "decimal com ponto" nos números de seção 2.8, 2.9, 3.1, 3.2, 3.3, 4.1 (numeração, não decimal). Sugestão para o script: ignorar `^\d\.\d+ ` no início de linha.
- Um GRAVE real corrigido: "Acompañamiento de una persona de confianza" (p117_17) reescrito como "Presencia de una persona de confianza" (aqui o sentido é companhia, mas evitei a forma marcada).
- Checagens extras: nenhum em-dash; nenhuma «» nem aspas retas; nenhum ¿¡ (instrução de tipografia); aspas curvas “ ” em p137_15; bullets "•" na mesma posição em todos os ids; tags `<b>` balanceadas e presentes em todo bloco com negrito; JSON carrega com `json.load`.
- Comprimento: 7 ids acima de +15 %, todos curtos ou com expansão obrigatória: p133_18 (expansão AAS exigida), p138_21 (ácido clavulánico + "cada 12 h" exigidos), p124_08, p138_12, p141_09, p142_02, p147_03 (strings curtas, diferença de 2 a 6 caracteres).
- **Passagem 3 (back-translation)**: conferência automática de todos os números por id (única diferença: 12/12h → cada 12 h, prevista) e de vias/unidades (EV→IV em p112_19, p113_04, p121_05; VO, SL, mg, UTR, mmHg idênticos), mais leitura de cada conduta, negação e lado: diazepam 10 mg / midazolam 5 mg IV; diazepam 5 a 10 mg VO / midazolam 3 a 5 mg VO/SL; captopril 25 mg VO/SL; clonidina 0,1 a 0,2 mg VO; ≥ 180/110 e >180/120 mmHg; hialuronidasa 1.000 UTR/mL, repetir em 12 a 24 h; AAS 300 mg/día por 7 días; sildenafil 50 mg/día; prednisona 40 mg/día por 3 a 5 días e 20 a 40 mg/día; amoxicilina/ácido clavulánico 875/125 mg cada 12 h por 7 a 10 días; compressão 10 a 15 min; 2 e 5 min da crise convulsiva; cicatrização 2 a 4 semanas; correções após 6 meses; "lado contralateral" (p132_15); negações ("no sujetar", "no colocar objetos", "no manipular en exceso", "que no masajeen ni duerman", "evitar nifedipina sublingual", "evitar corticoides sistémicos"). **Nenhuma divergência.**
