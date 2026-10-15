# FEA · Revisão ES · Parte 6 (pp. 186 a 220) · Relatório do revisor

REVISÃO: Livro *Intercorrências no preenchimento com ácido hialurônico*, parte 6 · 05/10/2026
Revisor: skill `fea-revision-es` (leitura de par especialista, separada do tradutor)

**Cobertura:** os 284 pares {id, pt, es} de `revisao/parte6-pt-es.json` (245 segmentos com mais de dois caracteres, 2.967 palavras ES), revisados id a id contra o PT. Conferi também `traducao/parte6-es.json`, que é o arquivo que vai para a produção: o texto ES dele é idêntico ao do arquivo de revisão em todos os 284 ids (0 divergências depois de tirar `<b>` e `•`). Os bullets `•` e as marcas `<b>` estão presentes no `parte6-es.json` exatamente onde o PT os tem; o arquivo de revisão só os removeu. Os 6 ids de display que não estão no arquivo de revisão (p203_00 a p203_02 "CON CLU / '' / SIÓN" e p207_00 a p207_02 "RE FE / '' / REN CIAS") foram conferidos direto no `parte6-es.json` e estão corretos. REFERÊNCIAS (pp. 208 a 220) não traduzidas, de propósito.

---

## VEREDITO: LIBERADO

| Nível | Resultado |
|---|---|
| **Classe A (barreira clínica)** | **0** |
| **Classe B (índice editorial)** | **99,2 %** (243 de 245 segmentos limpos) · 0,67 achado por mil palavras · 1 GRAVE · 1 MENOR |
| Questões ao autor | 5 (não afetam o veredito) |

Contagem: BLOQUEANTE 0 · GRAVE 1 · MENOR 1.

---

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id)`

`p194_12 | GRAVE | "puede haber o no un pequeño acúmulo de producto" | Inconsistência interna no livro. O PT "acúmulo" foi traduzido como "acumulación" em todas as outras ocorrências (partes 3, 4 e 5, 20 ocorrências: "acumulación de producto", "acumulación de líquido", "acumulación superficial de material"). "Acúmulo" existe em espanhol, mas aqui é a única ocorrência, e o leitor vê dois nomes para o mesmo achado clínico. | Palpación: puede haber o no una pequeña acumulación de producto.`

`p188_11 | MENOR | "con coloración amarronada" | Regionalismo. "Amarronado" é de uso rioplatense (o DLE marca Argentina e Uruguai); destoa do espanhol LatAm neutro definido em 90-decisiones. "Parduzca" é a forma neutra da descrição dermatológica. | Fig. 61: Hiperpigmentación posinflamatoria en región periorbitaria con coloración parduzca, debida al traumatismo causado por la manipulación del tejido tras el relleno. Fuente: imagen generada por IA.`
(No `parte6-es.json`, manter as marcas `<b>Fig. 61:</b>` e `<b>Fuente:</b>`.)

---

## Camada 1: mecânica (auditar.py)

Resultado do script sobre `p6es.txt` (só os valores ES, um por linha): LIBERADO, 98,4 %, 0 BLOQUEANTE, 4 GRAVE, exit code 0.

Os **4 GRAVE são falsos positivos**: "5.4 HIPERPIGMENTACIÓN", "5.5 NEOVASCULARIZACIÓN", "5.6 EFECTO TYNDALL" e "5.7 INSATISFACCIÓN" lidos como decimal com ponto. É numeração de seção, correta com ponto. Não contam no índice (ver AJUSTES NO AUDITOR).

Cobertura de termos obrigatórios: "cigomátic", "retenedor", "grasa" e "posprocedimiento" ausentes, o que é esperado, porque esses temas não aparecem nesta parte.

Varredura extra feita pelo revisor: nenhum travessão `—` (os dois do PT viraram parênteses em p186_02 e dois-pontos em p196_17), nenhuma aspa reta, aspas curvas “ ” como no PT, apóstrofo curvo em G’, nenhuma faixa com meia-risca, percentuais com espaço ("2 a 4 %"), nenhuma unidade colada, nenhum `tú`/`vos`, nenhuma ênclise em verbo finito, nenhum "el mismo" pronominal, nenhum "a nivel de", nenhum "en base a".

## Camada 2: segurança clínica (id a id contra o PT)

Sem divergência. Conferido valor por valor:

| Item | PT | ES |
|---|---|---|
| Hidroquinona | 2–4% (ciclos de 3–6 meses) | 2 a 4 % (ciclos de 3 a 6 meses) |
| Ácido azelaico | 10–20% | 10 a 20 % |
| Tretinoína | 0,025–0,05% | 0,025 a 0,05 % |
| Fotoproteção | FPS 50+ | FPS 50+ |
| Laser | Nd:YAG Q-Switched 1064 nm; Er:YAG; PDL | idem |
| Hialuronidase (Tyndall) | 10–30 UTR, localizadas, guiadas por palpação ou ultrassom | 10 a 30 UTR, localizadas, guiadas por palpación o ecografía |
| Sessões | 1–2 sessões | 1 a 2 sesiones |
| Janela de espera | primeiras 2–3 semanas | primeras 2 a 3 semanas |
| Fototipo | Fitzpatrick IV–VI | Fitzpatrick IV a VI |
| Corticoide | sistêmicos curtos | sistémicos en ciclos cortos |

Planos e camadas preservados: HPI epidérmica na camada basal versus dérmica com melanófagos; "planos más profundos, evitando el plano subdérmico inmediato"; "supraperióstico o plano submuscular en las ojeras"; "depositadas superficialmente"; "plano muy superficial" nos lábios.

Negações e alertas preservados: "no peligrosa desde el punto de vista funcional", "no ablativos", "no asociado a traumatismo", "no azuladas", "sin relación con el producto", "sin dolor ni signos inflamatorios", "puede haber o no", "puede identificar o no", "salvo ante complicaciones claras", "Evitar intentos de masaje o punciones repetidas, que rara vez resuelven el cuadro y pueden agravarlo", "Riesgo de hipopigmentación paradójica con el uso inadecuado de aclaradores".

Fármacos e ativos com grafia correta: hidroquinona, tretinoína, ácido azelaico, ácido kójico, arbutina, niacinamida, minociclina, amiodarona, Polypodium leucotomos, picnogenol, BDDE, DVS. Nenhuma via (EV) nem posologia x/x h nesta parte. Nenhuma sigla de autor quebrada (HPI fecha em ES).

Setas perdidas em p187_10 e p200_15: o tradutor repôs com conector ("y mayor síntesis", "con fibrosis e irregularidades"); o sentido causal fica preservado o suficiente. Não é achado (observação de formato prevista).

## Camada 3: back-translation dos trechos técnicos

Retraduzi para PT, sem olhar o original, os blocos de fisiopatologia da HPI (p187_08 a p188_02), conduta imediata e avançada da HPI (p189_16 a p190_10), fisiopatologia e conduta do Tyndall (p193_09 a p196_07), prevenção do Tyndall (p196_15 a p196_19) e conduta da insatisfação (p199_18 a p200_10). Comparação com o PT: mesma ordem de passos, mesmas indicações, mesmos números, mesmo escopo de cada recomendação. Nenhuma divergência de sentido.

## Camada 3b: mídia e QR Codes

A parte 6 não tem QR Code nem chamada de vídeo ou aula no texto (0 ocorrências de "QR", "vídeo" ou "aula" no PT). As duas figuras (61 e 62) têm título e legenda em camada de texto, traduzidos. Não verifiquei por OCR se há texto embutido na imagem das figuras.

## Camada 4: voz nativa e consistência

O texto lê como espanhol clínico nativo: passiva refleja nas descrições ("puede realizarse", "se deposita"), infinitivo nas recomendações em lista, conectores variados ("sin embargo", "paralelamente", "por su parte", "cabe destacar", "por todo ello"), sem gerúndio de posterioridade (os do PT viraram "lo que da lugar a", "lo que garantiza", "para reducir"). Termos consistentes dentro da parte: hialuronidasa, relleno, swelling factor (minúsculo, como no PT), efecto Tyndall, ecografía, aclaradores, microagujado, intercurrencia/complicación espelhando o PT. Os dois achados acima são os únicos pontos.

---

## PONTOS PARA ANÁLISE (ordenados por custo de não corrigir)

1. **p194_12, "acúmulo" contra "acumulación"** (GRAVE). Correção de uma palavra, alinha a parte 6 com 20 ocorrências das partes 3 a 5.
2. **Inconsistências entre partes do livro, que não são defeito da parte 6** mas o leitor do livro inteiro vai notar. Recomendo uniformizar no volume:
   - *festoons*: parte 5 conserva “festoon” em inglês entre aspas (trecho do sulco malar); parte 6 usa "festones" (p186_02, p186_06). Recomendo "festones" em todo o livro (forma usual na literatura clínica em espanhol) e ajustar a parte 5.
   - *ultrassom*: partes 1 e 2 usam "ultrasonido" e "ultrasonografía"; partes 4, 5 e 6 usam "ecografía" (inclusive "ecografía Doppler" contra "ultrasonido Doppler" da parte 1). Recomendo "ecografía" no corpo do texto em todo o livro; nos títulos de aula da parte 2 ("GUIADO POR ULTRASONIDO") pode ficar, se corresponder ao título do vídeo.
   - *swelling factor*: entre aspas nas partes 1 e 5, sem aspas nas partes 3 e 6. Uniformizar (sugiro sem aspas, em itálico se a produção permitir).
3. **p188_11, "amarronada"** (MENOR). Troca por "parduzca".

## QUESTÕES AO AUTOR (não afetam o veredito)

1. **p194_14 / p194_15, figura duplicada.** Na seção 5.6 (efeito Tyndall), o título e a legenda repetem a FIGURA 62 (neovascularização no mento). Provavelmente deveria ser uma FIGURA 63 sobre Tyndall. O tradutor já sinalizou; confirmo. Precisa de correção no original antes da diagramação ES.
2. **p188_11, p192_09, p194_15, imagem gerada por IA.** As legendas dizem "Fonte: Imagem gerada/criada por IA" em figura clínica. Isso conflita com a linha vermelha nº 7 do projeto FEA (nenhuma imagem de IA generativa em entregável final de conteúdo médico). Decidir antes de publicar: substituir por caso clínico autorizado ou por ilustração com curadoria humana (Gabriela Costa ou André Vivas).
3. **p190_07, laser.** O PT lista "fracionados não ablativos (Er:YAG, Nd:YAG Q-Switched 1064 nm)". O Er:YAG é em geral ablativo, e o Nd:YAG Q-Switched não é um laser fracionado. Traduzido fielmente; o autor deve revisar a frase.
4. **p193_10, física do efeito Tyndall.** O PT diz "refração seletiva da luz"; o fenômeno descrito é dispersão (espalhamento) seletiva, como o próprio p193_09 explica. Em p193_06, "visível sob a derme" também soa invertido (o produto superficial é visto através da pele). Traduzido fielmente.
5. **p186_13, seleção de produto para edema persistente.** "Menor grau de reticulação" é apresentado como fator que reduz retenção hídrica, o que tende a ir contra a leitura usual (gel menos reticulado costuma ser mais hidrofílico) e fica em tensão com p186_12 e p196_15 (baixo swelling factor, mais coesivo). Confiança moderada; vale o autor confirmar a intenção.

## PROPOSTAS DE GLOSSÁRIO

Para `15-intercurrencias.md` ou `00-nucleo.md`, já que esta parte introduziu termos ainda fora do glossário:

| PT | ES proposto | Observação |
|---|---|---|
| acúmulo (de produto, de líquido) | acumulación | Fixar para evitar a recaída de p194_12 |
| festoon(s) | festones | Fechar a divergência entre partes 5 e 6 |
| ultrassom (exame) / ultrassom Doppler | ecografía / ecografía Doppler | "ultrasonido" só quando for o equipamento ou título de aula já publicado |
| luz intensa pulsada (LIP) | luz pulsada intensa (LPI) | Sigla recalculada para ES |
| microagulhamento | microagujado `[a confirmar]` | Alternativas em uso: "microneedling", "micropunción". Confirmar qual o público hispano da FEA reconhece |
| clareador (ativo) | aclarador | "despigmentante" onde o PT diz despigmentante |
| turn-over celular | recambio celular | |
| amarronado | parduzco | Evitar o regionalismo rioplatense |

## AJUSTES NO AUDITOR

- **Falso positivo em série: numeração de seção lida como decimal.** Os 4 GRAVE desta parte ("5.4", "5.5", "5.6", "5.7") e os equivalentes nas outras partes vêm daí. Regra proposta para `auditar.py`, na checagem "decimal com ponto": ignorar a coincidência quando a linha casar com `^\s*\d+\.\d+\s+[A-ZÁÉÍÓÚÑ]` (número de seção seguido de título) ou quando o número estiver no início da linha e não for seguido de unidade.
- **Sugestão de nova regra (classe B):** sinalizar regionalismos rioplatenses frequentes em texto clínico (`amarronad`, `celeste` como cor de pele, `remera`, etc.) quando o material for LatAm neutro.

---

O índice de 99,2 % mede limpeza editorial; a fidelidade de sentido foi coberta pelas camadas 2 e 3, sem divergência.
