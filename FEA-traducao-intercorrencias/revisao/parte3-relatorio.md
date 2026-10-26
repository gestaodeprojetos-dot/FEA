# FEA · Revisão da tradução ES · Livro Intercorrências · Parte 3 (p. 75 a 111)

REVISÃO — parte3-pt-es.json (492 ids, p. 75 a 111: fim de 1.x Amaurose e fechamento do cap. 1, abertura do cap. 2, 2.1 Hematomas, 2.2 Dor, 2.3 Edema agudo leve a moderado, angioedema, 2.4 Eritema, 2.5 Anafilaxia, 2.6 Síndrome vasovagal, início de 2.7 Convulsão até "Diagnóstico diferencial") · 05/10/2026

Cobertura: os 492 pares PT/ES foram conferidos id a id contra o original. Camadas 1, 2, 3 e 4 executadas. Camada 3b feita contra a planilha `FEA-Traducao-ES-Intercorrencias-Aulas-e-QR.xlsx` (inventário de mídia), sem rodar `inventario_midia.py` sobre o PDF. Texto embutido em arte (figuras 34 a 39) não verificado, porque exige o PDF e OCR.

Não são achados (restrições de extração e decisões registradas): blocos partidos entre ids, inclusive no meio de palavra hifenizada; setas "→" do original trocadas por ":" ou conectores; ausência de ¿ ¡ « »; numeração "2.1" com ponto; ausência de "•" e de `<b>` no JSON de revisão (conferi: estão presentes em `traducao/parte3-es.json`, 244 ids com bullet, igual ao PT); omissão de números de página e de "JOÃO PITHON".

## VEREDITO: LIBERADO

| Item | Resultado |
|---|---|
| Classe A (barreira clínica) | **0** |
| Classe B (índice editorial) | **99,6 %** (489 de 491 segmentos limpos) |
| Densidade | 0,36 achado por mil palavras (2 achados em 5.614 palavras ES) |
| Achados por severidade | 0 BLOQUEANTE · 0 GRAVE · 2 MENOR |
| Questões ao autor | 5 (não afetam o veredito) |

### Camada 1 (auditar.py)

Exit 0, 0 BLOQUEANTE, 7 GRAVE. Os 7 são **falsos positivos** (regra "decimal com ponto" disparando na numeração de seção "2.1 HEMATOMAS" a "2.7 CONVULSIÓN"). Ver bloco AJUSTES NO AUDITOR.

### Camada 2 (segurança clínica), conferido um a um

- Doses e unidades: prednisona 20 a 40 mg durante 1 a 3 días (p91_21); prednisona 40 mg/día (p95_18); prednisona 40 mg VO, hidrocortisona 200 mg IV, metilprednisolona 125 mg IV (p104_07); adrenalina IM 0,3 a 0,5 mg, 1:1000 (p95_19); adrenalina IM no vasto lateral del muslo, 0,3 a 0,5 mg (0,3 a 0,5 mL da solução 1:1000), repetir cada 5 a 15 minutos (p103_18, p104_02); hialuronidasa en dosis baja 10 a 30 UTR (p92_05); atropina 0,5 mg IV/IM (p109_10). Todos idênticos ao PT.
- Vias: todas as ocorrências de EV viraram IV (p95_17, p104_06, p104_07, p104_11, p105_12, p109_11). Diprospan IM mantido (decisão registrada).
- Tempos e cifras: 90 minutos, menos de 1 h (p75_06/07); 24 % (p81_06); 40 % (p86_09); 20 % (p106_04); 2 a 5 min, 10 a 15 min, 24 h, 48 h, 7 a 14 días, 7 a 10 días, 48 a 72 h, 5 a 7 días, 8 a 24 h, 8 a 12 h, 1 a 2 min. A checagem automática de números por id não encontrou nenhuma divergência PT/ES.
- Fármacos: AAS glosado na 1ª ocorrência do cap. 2 (p82_15), clopidogrel, heparina, rivaroxabán, warfarina, dipirona, paracetamol, ibuprofeno, naproxeno, gabapentina, pregabalina, loratadina, fexofenadina, difenhidramina, icatibant, inhibidor de C1, salbutamol. Grafias corretas.
- Negações e alertas preservados: "Evitar el masaje excesivo" (p84_08); "no responde bien a antihistamínicos ni a corticoides" (p94_05); "No actúan de inmediato, pero previenen la reacción bifásica" (p104_07); "solo en un entorno hospitalario monitorizado" (p104_11); "no debe retrasar el manejo" (p104_14); "salvo contraindicación" (p104_03); "sin depender de estudios complementarios" (p102_17); critérios de derivação de emergência (p95_13) e de intubação (p104_12) intactos.
- Planos e lados: planos superficiais (p82_10, p90_07, p92_15), sistemas carotídeos externo e interno (p76_04), tampão proximal com expansão anterógrada/retrógrada (p75_04), membros inferiores elevados (p104_03, p108_17). Sem inversão.
- Omissão: nenhuma. Os dois blocos de vídeo em duas colunas (p79_07 a p79_22) foram remontados e cada coluna lê completa em ES.

### Camada 3 (back-translation)

Retraduzidos sem o original: legenda da Fig. 34 (tipos I a IV de oclusão), fechamento do cap. 1 (p76_03 a p77_03), fisiopatologia e conduta de hematoma, dor, edema, angioedema, anafilaxia (critérios, conduta imediata e avançada, kit de emergência) e vasovagal. Nenhuma troca de estrutura, ordem de passo ou negação. Os acréscimos "aislado o combinado" (p101_17) e "o de ambas" (p103_04) são a forma espanhola de "e/ou" e não mudam o sentido.

### Camada 3b (mídia e QR)

Os dois vídeos desta parte (VIDEO 10, p79; VIDEO 11, p80) têm linha na planilha, nas abas "Aulas para traduzir" e "QR para ajustar", com rótulo ES coincidente com o texto traduzido e ação "regerar QR para a aula dublada quando o link ES existir". Não há QR de artigo nesta parte. Nada a apontar como achado.

### Camada 4 (voz nativa)

Texto com registro de docente: passiva refleja nas descrições, infinitivo nas listas de conduta, sem tuteo, sem "el mismo" pronominal, sem "a nivel de", "en base a" ou "donde" sem lugar. Conectores variados ("además" só 2 vezes em 5.614 palavras). "Signo" usado em todas as 20 ocorrências de "sinal" clínico; "vía aérea" uniforme (7 ocorrências); "derivar/derivación" para "encaminhar". Duas passagens com arestas, listadas abaixo.

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id)`

### BLOQUEANTE

Nenhum.

### GRAVE

Nenhum.

### MENOR

1. `p106_04 | MENOR | "puede ocurrir hasta en el 20 % de los casos: necesidad de observación hospitalaria." | A seta do original virou um segundo dois-pontos na mesma frase (o primeiro já vem depois de "Reacción bifásica"). A leitura fica entrecortada e "necesidad de..." solto soa como resto de esquema, não como prosa. | Reacción bifásica: puede ocurrir hasta en el 20 % de los casos, lo que hace necesaria la observación hospitalaria.`

2. `p97_09 | MENOR | "ANGIOEDEMA EN LABIO SUPERIOR POSHIALURONIDASA" | Prefixo "pos-" colado a nome de fármaco não é formação usual em espanhol clínico ("posprocedimiento" sim, "poshialuronidasa" não); o leitor tropeça no título da figura. A própria legenda (p97_10) já usa "tras la aplicación de hialuronidasa". | FIGURA 37. ANGIOEDEMA EN EL LABIO SUPERIOR TRAS LA APLICACIÓN DE HIALURONIDASA`

## PONTOS PARA ANÁLISE (por custo de não corrigir)

1. **Questões ao autor p86_03 e p93_04** (abaixo): são erros do original que vão aparecer iguais no ES. Custo maior que os dois MENOR, porque o leitor atento percebe a legenda incoerente nas duas línguas.
2. **Linha vermelha nº 7 (p97_10, p106_07):** figuras clínicas assinadas como imagem gerada por IA. Não é defeito de tradução, mas trava publicação pela regra do projeto.
3. p106_04 (MENOR, legibilidade de um critério de observação em anafilaxia).
4. p97_09 (MENOR, título de figura).

## QUESTÃO AO AUTOR

1. **p86_03** · A legenda da FIGURA 35 cita "região periorbital" duas vezes; a lista da seção (p83_04 a p83_07) é periorbital, lábios, **malar** e sulco nasolabial. A segunda ocorrência deveria ser "malar"? A tradução espelhou o original ("región periorbitaria" duas vezes), o que está correto como tradução.
2. **p93_04** · O título "TESTE CLÍNICO DE REPERFUSÃO CAPILAR NA AVALIAÇÃO DE ISQUEMIA CUTÂNEA FACIAL" não corresponde à Figura 36 (edema agudo transitório 24 h após o procedimento). Parece título reaproveitado da Fig. 5 (parte 1). O autor precisa dar o título certo nas duas línguas.
3. **p94** · A seção de angioedema começa direto em FISIOPATOLOGIA, sem título "2.x ANGIOEDEMA" na camada de texto, e a numeração vai de 2.3 (edema) para 2.4 (eritema). Confirmar no PDF se o título está em arte ou foi esquecido; se faltar, a numeração das seções 2.4 em diante muda.
4. **p97_10 e p106_07** · "Imagem recriada com IA" e "Fonte: IA, Gemini" em figuras clínicas. Conflita com a linha vermelha nº 7 do projeto (sem imagem de IA generativa em entregável final; propor designer da equipe). Traduzido fielmente; decisão editorial do autor.
5. **Planilha de mídia** · Para os vídeos 10 e 11 (complicações agudas **não** isquêmicas), a coluna "Aula no catálogo" aponta para "Complicações isquêmicas agudas". Conferir se o mapeamento para a aula dublada está certo antes de regerar os QR.

## PROPOSTAS DE GLOSSÁRIO

- **preenchedor:** o núcleo fixa "producto de relleno", mas esta parte usa "relleno(s)" para o produto na maioria das ocorrências ("rellenos dérmicos", "rellenos faciales") e "producto de relleno" em 3. As duas formas são correntes na literatura em espanhol e o contexto desfaz a ambiguidade com "relleno" (procedimento) em todos os ids desta parte, por isso não contei como achado. Recomendo registrar em `90-decisiones.md`: "preenchedores dérmicos/faciais → rellenos dérmicos/faciales; producto de relleno quando houver risco de confusão com o procedimento".
- **reperfusão capilar:** o PT usa "reperfusão capilar" (p88_07, p93_04) e a tradução manteve "reperfusión capilar"; o glossário 15 só tem "llenado capilar" para "enchimento capilar". Registrar os dois como termos distintos, espelhando o original.
- **teste de contato → prueba de contacto** (p96_20) e **dosagem de triptase → determinación de triptasa** (p104_14): incluir no módulo 15.
- **equimose arroxeada → equimosis violácea; colagenoses → colagenopatías; zumbido → acúfenos:** incluir no módulo 15.

## AJUSTES NO AUDITOR

- **Falso positivo (7 ocorrências):** regra "decimal com ponto" casa com numeração de seção no início da linha (`2.1 HEMATOMAS`, `2.2 DOLOR` ... `2.7 CONVULSIÓN`). Proposta: ignorar o padrão `^\d+(\.\d+)+\s+[A-ZÁÉÍÓÚÑ]` (número com ponto no início da linha seguido de palavra em maiúscula), ou exigir que o "decimal" esteja seguido de unidade ou precedido de espaço no meio da frase. Mesmo falso positivo já relatado nas outras partes; vale corrigir a regra de vez.
- **Cobertura de termos obrigatórios:** "cigomátic", "nasoyugal", "retenedor" e "grasa" aparecem como ausentes, mas nenhum desses conceitos ocorre no PT desta parte. Proposta: a lista de cobertura deveria ser por módulo de glossário (ou comparada com a presença do termo PT correspondente), senão gera alerta sem sentido em todo capítulo que não trata de olheiras.
