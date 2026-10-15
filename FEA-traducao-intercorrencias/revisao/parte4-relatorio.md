# FEA · Revisão da tradução ES · Livro Intercorrências · Parte 4 (p. 112 a 148)

REVISÃO — parte4-pt-es.json (459 ids, p. 112 a 148: fim de 2.7 Convulsão, 2.8 Crise de pânico, 2.9 Crise hipertensiva, 2.10 Trauma arterial, fechamento do cap. 2, cap. 3 completo, início do cap. 4 até 4.1 Conduta imediata) · 05/10/2026

Cobertura: os 459 pares PT/ES foram conferidos id a id contra o original. As camadas 1, 2, 3 e 4 foram executadas. A camada 3b (inventário de mídia e QR) **não foi coberta**, porque esta parte não traz QR nem vídeo no texto extraído e não recebi o PDF nem o inventário. Também não verifiquei texto embutido em arte (a tabela da Fig. 40, por exemplo), porque isso exige o PDF.

## VEREDITO: LIBERADO

| Item | Resultado |
|---|---|
| Classe A (barreira clínica) | **0** |
| Classe B (índice editorial) | **98,5 %** (450 de 457 segmentos limpos) |
| Densidade | 1,28 achado por mil palavras (7 achados em 5.480 palavras ES) |
| Achados por severidade | 0 BLOQUEANTE · 4 GRAVE · 3 MENOR |
| Questões ao autor | 5 (não afetam o veredito) |

A camada 2 conferiu todas as doses, unidades, vias e posologias: diazepam 10 mg / midazolam 5 mg IV; diazepam 5 a 10 mg VO / midazolam 3 a 5 mg VO/SL; captopril 25 mg VO/SL; clonidina 0,1 a 0,2 mg VO; >180/120 mmHg e ≥180/110 mmHg; AAS 300 mg/día (por 7 días); sildenafil 50 mg e 50 mg/día; prednisona 40 mg/día, 40 mg/día por 3 a 5 días e 20 a 40 mg/día; hialuronidasa 1.000 UTR/mL repetível em 12 a 24 h; amoxicilina/ácido clavulánico 875/125 mg cada 12 h por 7 a 10 días; compressão de 10 a 15 min; repetição em 5 a 10 min; crise de 2 e de 5 min; cicatrização em 2 a 4 semanas; correção depois de 6 meses. Todas as vias EV viraram IV. Todas as negações e contraindicações estão preservadas ("No sujetar...", "No colocar objetos en la boca", "Evitar la nifedipina sublingual", "Evitar los corticoides sistémicos en esta fase", "No manipular en exceso"). Lados e estruturas (canto medial, nasal lateral e dorsal, labiais superior e inferior, lado contralateral) conferem. Não há trecho omitido: a checagem automática de números e de razão de comprimento por id não encontrou divergência.

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id)`

### BLOQUEANTE

Nenhum.

### GRAVE

1. `p124_20 | GRAVE | "ausencia de relleno capilar" | Inconsistência interna e ambiguidade. A parte 1 usa "tiempo de llenado capilar" e o glossário 15 fixa "llenado capilar". Num livro sobre relleno (filler), "relleno capilar" pode ser lido como produto injetado nos capilares. | Signos de isquemia distal en casos de trombosis o compresión (palidez, livedo, ausencia de llenado capilar).`

2. `p132_06 | GRAVE | "piel densa y menos complaciente" | Falso amigo. "Complaciente" em ES descreve temperamento (condescendente), não complacência tecidual. O próprio material usa "complacencia" corretamente em p131_08 e p139_20, o que gera inconsistência. | Glabela (piel densa y de menor complacencia).`

3. `p137_07 | GRAVE | "piel gruesa, poco complaciente" | Mesmo falso amigo do item anterior (segunda ocorrência). | Glabela: piel gruesa, de baja complacencia y de difícil revascularización.`

4. `p147_05 | GRAVE | "Contaminación secundaria por manipulación del paciente" | Ambiguidade de agente. O PT diz manipulação feita PELO paciente, depois do procedimento. "Manipulación del paciente" se lê também como manipulação DO paciente (pela equipe), e o "após" temporal virou "por" causal. Muda quem é o vetor de contaminação, relevante para a orientação pós-procedimento. | Contaminación secundaria tras la manipulación de la zona por parte del paciente.`

### MENOR

5. `p112_11 | MENOR | "No sujetar los movimientos" | Calco de "conter os movimentos"; em ES se sujeta al paciente, não os movimentos. Sentido preservado. | No restringir los movimientos del paciente, solo proteger la cabeza.`

6. `p117_09 | MENOR | "Recurrencia en atenciones futuras" | Calco de "atendimentos"; o natural em ES clínico é consulta ou sesión. | Recurrencia en sesiones futuras (condicionamiento psicológico negativo).`

7. `p135_04 | MENOR | "lo que hace el diagnóstico más difícil y a menudo se confunde con infección" | Troca implícita de sujeito: gramaticalmente quem "se confunde" é o diagnóstico; no PT é o quadro. Lê-se, mas o docente tropeça. | La necrosis tisular tardía es una complicación derivada de la progresión no reconocida o no tratada de un cuadro isquémico subclínico (como una isquemia compresiva no resuelta), o bien de necrosis parciales que evolucionan lentamente después del procedimiento. A diferencia de la necrosis aguda, aquí los signos aparecen días después de la aplicación, lo que dificulta el diagnóstico; a menudo el cuadro se confunde con una infección o con una reacción inflamatoria persistente.`

## PONTOS PARA ANÁLISE (ordenados por custo de não corrigir)

1. **"complaciente" (p132_06, p137_07):** é o achado que um docente hispano notaria primeiro, e fere a consistência com "complacencia" do mesmo capítulo. Rodar `grep -n complaciente` nas partes 5 e 6 antes de fechar.
2. **"relleno capilar" (p124_20):** inconsistência com a parte 1 e ambiguidade com o tema do livro. Proponho entrada no auditor (ver abaixo).
3. **p147_05:** agente da contaminação ambíguo; correção de uma linha.
4. **Bullets "•" (ponto de produção, não contado no índice):** o PT traz "•" em 234 ids e o ES em nenhum. As decisões fixas mandam preservar bullets na mesma posição. As partes 1 a 3 têm o mesmo padrão (0 bullets no ES), o que sugere escolha do pipeline (bullet redesenhado a partir do PDF original). Não contei como achado de tradução, mas **conferir no PDF montado se os marcadores de lista aparecem**: se o bullet estiver dentro da caixa substituída, 234 itens de lista perdem o marcador.
5. Os três MENOR (p112_11, p117_09, p135_04), se houver tempo.

## QUESTÕES AO AUTOR (não afetam o veredito)

1. **p136_08 e p140_09:** o original repete o título "FIGURA 43. COMPROMETIMENTO ISQUÊMICO EM REGIÃO PERIORAL..." sobre as Figuras 44 (nariz e região perinasal) e 45 (sequência de necrose após rinomodelação). A tradução espelhou o erro. Sugestão: títulos próprios para 44 e 45 nos dois idiomas.
2. **p112_06:** "Hipoglicemia grave: ... mas geralmente sem atividade clínica típica". No contexto do diagnóstico diferencial de convulsão, provavelmente o autor quis dizer "atividade convulsiva típica". A tradução manteve "actividad clínica típica", fiel ao PT.
3. **p140_14:** o PT diz "regressiva progressiva das lesões" (erro de digitação). O ES corrigiu em silêncio para "regresión progresiva", correção correta e conforme a regra das decisões fixas.
4. **p123_10:** a Fig. 41 declara "Fonte: Imagem criada com IA". A linha vermelha 7 do projeto FEA proíbe imagem gerada por IA em entregável final. Não é defeito de tradução, mas a edição ES vai replicar a imagem: confirmar com o autor se ela permanece.
5. **p121_05:** "sintomas-alvo" foi interpretado como "síntomas de órgano blanco", leitura clinicamente correta (crise hipertensiva com lesão de órgão-alvo). Confirmar se era essa a intenção do autor.

## PROPOSTAS DE GLOSSÁRIO

| PT | ES | Módulo |
|---|---|---|
| perfusão / reperfusão / enchimento capilar | llenado capilar (nunca "relleno capilar") | 15-intercurrencias §4 |
| complacência (tecidual), pouco complacente | complacencia, de baja/menor complacencia (nunca "complaciente") | 01-voz-y-estilo §2 (falsos amigos) |
| síndrome do pânico (transtorno) | trastorno de pánico (título do capítulo segue "crisis de pánico") | 15-intercurrencias §3 |
| HAS | HTA | 15-intercurrencias §4 |
| AVC | ACV | 15-intercurrencias §4 |
| pronto-socorro | servicio de urgencias | 15-intercurrencias §6 |
| zumbido (otológico) | acúfenos | 15-intercurrencias §4 |
| sintomas-alvo / lesão de órgão-alvo | síntomas / daño de órgano blanco | 15-intercurrencias §4 |
| dipirona | dipirona (alt.: metamizol, uso no México e na América Central); decisão a registrar em 90-decisiones | 15-intercurrencias §6 |

## AJUSTES NO AUDITOR

O `auditar.py` saiu com exit 1 (1 BLOQUEANTE, 6 GRAVE). **Os 7 achados são falsos positivos:**

1. **[BLOQUEANTE] ênclise em "Hyaluronidase" (p131_12):** é o título em inglês de um artigo citado ("Ultrasound-Guided Hyaluronidase Injections..."), que não se traduz. A regra de ignorar linhas em inglês falhou porque a linha mistura "Fuente: adaptada de" (ES) com a referência em inglês. Regra proposta: ignorar tudo o que vem depois de `Fuente: adaptad[oa] de` até o fim do segmento, ou aplicar a detecção de inglês por trecho, não por linha.
2. **[GRAVE] "decimal com ponto" em 2.8, 2.9, 3.1, 3.2, 3.3, 4.1:** é numeração de seção ("2.8 CRISIS DE PÁNICO"), correta por decisão do projeto. Regra proposta: não marcar `^\d+\.\d+\s+[A-ZÁÉÍÓÚÑ]` (número no início do segmento seguido de título em caixa alta).
3. **Regra nova sugerida:** marcar como GRAVE `relleno capilar` e `complaciente`, os dois achados reais desta parte que o script não pegou.
