# FEA · Tradução ES · Parte 3 (pp. 75 a 111) · Relatório

Entrada: `parte3-pt.json` (625 blocos). Saída: `parte3-es.json` (493 ids traduzidos, 132 omitidos).

Os 132 omitidos são números de página, "JOÃO P I T HO N" / "JOÃO PITHON" e os blocos que são só "•" (padrão das partes 4 e 5; o bullet original fica onde está). O cabeçalho corrido vai em todas as páginas como "INTERCURRENCIAS EN EL RELLENO CON ÁCIDO HIALURÓNICO". Os ids que já são iguais em ES ("2.1 HEMATOMAS", "DIAGNÓSTICO CLÍNICO" etc.) foram incluídos, com o `<b>` do original.

## (a) Termos novos fora dos glossários e a escolha feita

| PT | ES escolhido | Observação |
|---|---|---|
| tampão intravascular | tapón intravascular | |
| anastomoses / sistemas carotídeo externo e interno | anastomosis / sistemas carotídeos externo e interno | |
| oftalmoplegia | oftalmoplejía | |
| equimose / mancha arroxeada | equimosis / mancha violácea | "arroxeado" = violáceo em todo o texto |
| anti-inflamatórios não esteroidais / AINEs | antiinflamatorios no esteroideos / AINE | AINE invariável, igual às partes 4 e 5 |
| anti-histamínicos | antihistamínicos | prefixo colado |
| rivaroxabana, varfarina | rivaroxabán, warfarina | DCI em espanhol |
| difenidramina | difenhidramina | DCI em espanhol |
| alho | ajo | |
| camomila | manzanilla | |
| colagenoses | colagenopatías | |
| idosos | ancianos | |
| ultrassom (avaliação com) | evaluación ecográfica | Igual às partes 4, 5 e 6 ("ecografía") |
| compressas mornas | compresas tibias | |
| reassurar o paciente | tranquilizar al paciente | |
| inibidores da ECA / IECA | inhibidores de la ECA / IECA | sigla idêntica em ES |
| inibidor de C1-esterase / concentrado de C1-inibidor | inhibidor de la C1 esterasa / concentrado de inhibidor de C1 | |
| icatibant | icatibant | DCI igual |
| triptase sérica (dosagem de) | determinación de triptasa sérica | |
| choque anafilático | shock anafiláctico | uso LatAm |
| acesso venoso calibroso / reposição volêmica | acceso venoso de gran calibre / reposición volémica | |
| encaminhamento (especializado, alergista, hospitalar) | derivación (especializada, al alergólogo, hospitalaria) | falso amigo, conforme 01-voz-y-estilo |
| óbito | muerte | |
| zumbido | acúfenos | |
| tontura / visão turva | mareo / visión borrosa | |
| pós-ictal | posictal | |
| hipoglicemia | hipoglucemia | |
| LED terapia | terapia LED | |
| dipirona | dipirona | mantida como no PT (em parte da LatAm se diz metamizol; não acrescentei glosa) |
| faixas de valor (7–14, 0,3–0,5 mg, 10–30 UTR, 48–72h etc.) | "7 a 14", "0,3 a 0,5 mg", "10 a 30 UTR", "48 a 72 h" | Só a notação (núcleo §9, mesmo critério da parte 6); números idênticos |
| 24h, <1h, 24% | 24 h, menos de 1 h, 24 % | espaço antes da unidade e do %; "<1h" virou "menos de 1 h" (ver item b) |

## (b) Erros de digitação e ambiguidades do original PT

| id | No original | O que foi feito |
|---|---|---|
| p75_07 | "a cwhance de reversão" | Corrigido: "la probabilidad de reversión". "(<1h)" virou "(menos de 1 h)" porque o sinal "<" seguido de texto dentro de `<b>` é lido como tag HTML pelo pipeline (o próprio filtro de tags apagou o trecho no teste); o valor não muda |
| p75_02 | O bloco começa com "tre" (resto de "en-" no fim da parte 2, p74_05) | ES começa direto em "anatomía y dinámica…". **O coordenador precisa conferir se a parte 2 terminou p74_05 com "entre" inteiro.** Se ela deixou "en-", trocar o início de p75_02 por "tre anatomía…" |
| p75_07/p75_08, p81_12/p82_02, p101_18/p102_02 | Palavras partidas entre blocos ("parcial-/mente", "es-/verdeado", "profilax-/ia") | Palavra inteira no primeiro id, sem hífen; o sentido de cada id continua o mesmo |
| p81_12/p82_02, p94_04, p96_13, p102_08, p102_09, p106_04, p107_08, p111_03, p111_04 | Seta "→" perdida na extração ("liberação de histamina aumento da permeabilidade capilar edema") | Restaurei "→", igual à parte 4 (p114_11). Em outros pontos da própria parte (p95_03, p102_06) a seta veio no texto. Conferir no render se a seta original era vetor; se for, não pode aparecer duplicada |
| p77_03 | "não são eventos imprevisíveis são complicações possíveis" (falta pontuação) | ES com dois-pontos |
| p94_10 | Travessão (—) | ES com vírgula |
| p75_04 | "Tipo I – o material…" (meia-risca no meio da frase) | ES com dois-pontos ("Tipo I: el material…"). No título "FIGURA 34 –" a meia-risca ficou |
| p86_03 | A legenda da FIGURA 35 cita "região periorbital" duas vezes; a lista da seção é periorbital, lábios, **malar** e sulco nasolabial. A segunda deve ser "malar" | Traduzido fielmente ("región periorbitaria" duas vezes). **O autor decide** |
| p93_04 | O título "TESTE CLÍNICO DE REPERFUSÃO CAPILAR NA AVALIAÇÃO DE ISQUEMIA CUTÂNEA FACIAL" não bate com a legenda da Figura 36 (edema agudo transitório 24 h depois) | Traduzido fielmente. **O autor precisa corrigir o título** |
| p94 | A seção de angioedema começa em FISIOPATOLOGIA sem título "2.x ANGIOEDEMA" na camada de texto; a numeração pula de 2.3 para 2.4 (eritema). O título pode estar em arte ou ter sido esquecido | Nada a traduzir; sinalizar ao autor e conferir no OCR da página 93/94 |
| p97_10, p106_07 | Legendas "Imagem recriada com IA" e "Fonte: IA, Gemini" em figura clínica | Traduzido fielmente. **Atenção:** isso conflita com a linha vermelha nº 7 (nada de imagem de IA generativa em entregável final). Sinalizar ao autor |
| p79_06, p80_04 | Títulos de vídeo dizem "COMPLICAÇÕES agudas não isquêmicas", e o texto diz "intercorrências" | Espelhado ("COMPLICACIONES"), porque o glossário trata os dois como termos distintos |
| p95_18 | "diprospan" em minúscula | "Diprospan" (marca), conforme decisões comuns |
| p82_15 | Primeira ocorrência de AAS no capítulo 2 | "AAS [ácido acetilsalicílico]" com colchete por já estar entre parênteses; depois só AAS (p85_16) |

## (c) Ids de display

- **p79_02 / p79_03**: capitular de abertura do capítulo 2. "A" + "s intercorrências…" virou "<b>L</b>" + "as intercurrencias…", igual à parte 6 (p204).

## (d) Resultado da auditoria

- **auditar.py** (493 linhas, 5.876 palavras): **LIBERADO**, índice de 98,6 %, **0 achados de classe A**, exit code 0.
- Os 7 achados GRAVE são **falsos positivos**: números de seção "2.1" a "2.7" lidos como decimal com ponto (já registrado na parte 6; sugestão para o script: ignorar `^\d\.\d+ [A-ZÁÉÍÓÚ]`). O achado de "la misma base" (pronome) foi corrigido para "una base fisiopatológica común", mesmo sendo falso positivo, para limpar o relatório.
- Cobertura dá como ausentes "cigomátic", "nasoyugal", "retenedor" e "grasa": esses temas não aparecem nesta parte.
- Varredura extra: nenhum travessão (—), nenhum « », ¡, ¿ ou aspa reta; `<b>` balanceado em todos os ids; bullets finais "•" na mesma posição do PT; o JSON carrega com `json.load`; os números de cada id batem com o PT, um a um (checagem automática).
- **Comprimento**: só 5 ids passam de 15 % do PT. p82_15 (+21 %, a glosa obrigatória do AAS), p106_04 (+17 %, a seta restaurada), p75_07 (+14 % depois do ajuste) e as linhas da coluna dupla do VÍDEO 10 (p79_16, p79_18), que o script junta num parágrafo só e refluí; no total da coluna o ES fica dentro da folga.
- **Back-translation (passagem 3)**, sem nenhuma divergência:
  - **Doses e vias**: prednisona 20 a 40 mg durante 1 a 3 dias; prednisona 40 mg/dia ou Diprospan IM; prednisona 40 mg VO, hidrocortisona 200 mg IV, metilprednisolona 125 mg IV; adrenalina IM 0,3 a 0,5 mg (0,3 a 0,5 mL da solução 1:1000) no vasto lateral da coxa, repetir a cada 5 a 15 min; adrenalina IV em infusão contínua só em ambiente hospitalar monitorizado; atropina 0,5 mg IV/IM; anti-histamínico oral ou IV; hialuronidase em dose baixa 10 a 30 UTR, e em doses altas no PDRR.
  - **Tempos**: retina 90 min; menos de 1 h; compressão 2 a 5 min; gelo 10 a 15 min nas primeiras 24 h; suspender 7 a 10 dias antes; resolução em 7 a 14 dias; 24 a 48 h, 48 a 72 h, 5 a 7 dias, 24 a 72 h; observação 8 a 24 h; reação bifásica após 8 a 12 h, em até 20 %; crise de 1 a 2 min; incidências de 24 % e 40 %.
  - **Planos e anatomia**: planos superficiais como fator de risco; evitar planos muito superficiais; região infraorbital; sistemas carotídeos externo e interno; artéria oftálmica; tipos I a IV com expansão anterógrada e retrógrada.
  - **Negações**: "no responde bien a antihistamínicos ni a corticoides"; "sin urticaria ni broncoespasmo"; "sin depender de estudios complementarios"; "no debe retrasar el manejo"; "no actúan de inmediato, pero previenen"; "sin extravasación"; "(no edema difuso)", "(no rubor)"; "sin la bradicardia típica"; "salvo contraindicación"; "sin evaluación alergológica previa".
  - **Condutas**: derivar a emergência diante de obstrução; suspender o agente suspeito; intubação precoce diante de edema de glote ou estridor; Trendelenburg na síncope. Tudo idêntico ao PT.
