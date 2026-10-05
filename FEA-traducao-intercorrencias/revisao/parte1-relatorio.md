# FEA · Revisão ES · Livro Intercorrências · Parte 1

REVISÃO: Intercurrencias en el relleno con ácido hialurónico, parte 1 (págs. 3 a 37, 250 ids) · 05/10/2026
Cobertura: 250 pares PT/ES de `parte1-pt-es.json`, revisados id a id contra o original PT. Camadas 1 (auditar.py), 2 (segurança clínica), 3 (back-translation dos trechos técnicos: mecanismos, sinais, áreas de risco, conduta imediata, terapia adjuvante, antibioticoterapia, prevenção) e 4 (voz nativa e consistência). Camada 3b (inventário de mídia e QR) **não coberta**: o PDF original e o inventário não fizeram parte do insumo desta revisão.

## VEREDITO: LIBERADO COM RESSALVAS

- **Classe A (barreira clínica): 0.** Nenhuma divergência de dose, unidade, concentração, posologia, via, fármaco, plano, lado, negação ou omissão imputável à tradução. Os 2 BLOQUEANTES do auditor são falsos positivos (ver «Ajustes no auditor»).
- **Classe B (índice editorial): 88,1 %** (215 de 244 segmentos limpos; denominador = 244 segmentos contados pelo auditor)
  - 4,01 achados por mil palavras (29 achados / 7.236 palavras ES)
  - 2 GRAVE · 27 MENOR
- **Questões ao autor: 7** (não afetam o veredito)

Leitura do número: 25 dos 29 segmentos sujos são um único defeito sistemático e mecânico (bullets «•» removidos). Corrigido esse ponto, o índice sobe para 98,4 % (240/244), faixa LIBERADO.

### Conferência de segurança clínica (camada 2), itens verificados

| id | PT | ES | Status |
|---|---|---|---|
| p13_07 | 60 a 90 min / 4 a 6 h / 24 h | sesenta a noventa minutos / cuatro y seis horas / veinticuatro horas | OK |
| p21_06 | 58 % · 48 % · 39 % vs. 0,8 % · 8 % vs. 0,8 % | idênticos | OK |
| p23_06 | 60 e 90 minutos; massagem ocular, compressas mornas, AAS, corticoide, OHB | idênticos | OK |
| p31_08/09 | 1000 UTR/mL; repetir a cada 15–30 min | 1000 UTR/mL; cada 15 a 30 min | OK clínico (formato, ver achado) |
| p33_08 | AAS 300 mg/dia | AAS (ácido acetilsalicílico) 300 mg/día (1ª ocorrência da sigla no capítulo) | OK |
| p33_09 | Sildenafil 50 mg | Sildenafil 50 mg | OK |
| p33_10 | prednisona 40 mg vo; diprospan IM | prednisona 40 mg VO; Diprospan IM | OK |
| p33_13 | OHB 5-10 sessões | 5 a 10 sesiones | OK |
| p33_15 | após 6h | tras 6 h | OK |
| p33_17 | amoxicilina + clavulanato 875/125 mg 12/12h | amoxicilina + ácido clavulánico 875/125 mg cada 12 h | OK |
| p34_03 | metronidazol 400mg 8/8h | metronidazol 400 mg cada 8 h | OK |
| p34_04 | ceftriaxona 1–2 g/dia; pip/tazo 3,375 g 6/6h; meropenem 1 g 8/8h | 1 a 2 g/día; 3,375 g cada 6 h; 1 g cada 8 h | OK |
| p14_03, p24_04 a p24_11, p29_14, p29_15 | artérias, territórios, superior/inferior, medial | sem inversão | OK |
| p6_03, p14_02, p36_04 | negações («não deve», «não reconhecidos», «e não restrita») | preservadas | OK |

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id)`. Ordem por custo de não corrigir.

### GRAVE

p31_08 | GRAVE | «Hialuronidasa: inyectar 1000 UTR/mL en la región afectada,» | Milhar sem ponto num valor de dose. Convenção travada no glossário (00-nucleo §9 e 15-intercurrencias §6: `1.000 UTR/mL`). Número correto, formato fora do padrão num trecho de conduta de emergência. | 1. Interrumpir la aplicación de inmediato. 2. Masaje vigoroso del área comprometida. 3. Compresas tibias para vasodilatación. 4. Hialuronidasa: inyectar 1.000 UTR/mL en la región afectada,

p20_04 | GRAVE | «con destaque para la participación de los angiosomas» | Calco do português «com destaque para»; não é construção nativa em espanhol técnico (lusismo). | Figura 4. Representación gráfica de la distribución de las áreas faciales tratadas que evolucionaron con isquemia cutánea, eventos isquémicos graves y compromiso visual. Se observa una mayor concentración de casos en regiones como el surco nasolabial, el dorso nasal y la glabela, con especial participación de los angiosomas relacionados con la arteria facial y la arteria oftálmica. La afectación del territorio oftálmico se asocia a un mayor riesgo de complicaciones neurooftalmológicas, incluidas la pérdida visual y los eventos cerebrovasculares, lo que refuerza la necesidad de cautela en áreas con anastomosis vasculares críticas.

### MENOR

**Defeito sistemático (25 ocorrências, prioridade 1 por volume):** todos os ids cujo PT termina em « •» perderam o bullet no ES. As decisões comuns do projeto mandam preservar o bullet na mesma posição. Correção mecânica: acrescentar « •» ao fim de cada valor ES listado abaixo.

p24_04 | MENOR | «Arteria facial: irriga la región perioral; su obstrucción puede com-» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Arteria facial: irriga la región perioral; su obstrucción puede com- •
p24_05 | MENOR | «prometer los labios y la región paranasal. Arterias labiales (superior e inferior): irrigan los labios; pueden cau-» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | prometer los labios y la región paranasal. Arterias labiales (superior e inferior): irrigan los labios; pueden cau- •
p24_06 | MENOR | «sar palidez, dolor, riesgo de ulceración y evolución hacia necrosis. Arteria columelar: puede causar necrosis de la columela y de la punta» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | sar palidez, dolor, riesgo de ulceración y evolución hacia necrosis. Arteria columelar: puede causar necrosis de la columela y de la punta •
p24_07 | MENOR | «nasal. Arteria angular: discurre cerca del canto medial del ojo y se comu-» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | nasal. Arteria angular: discurre cerca del canto medial del ojo y se comu- •
p24_08 | MENOR | «nica con la oftálmica, por lo que puede causar amaurosis. Además, por sus variaciones anatómicas, se considera una vía crítica para la necrosis nasal.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | nica con la oftálmica, por lo que puede causar amaurosis. Además, por sus variaciones anatómicas, se considera una vía crítica para la necrosis nasal. •
p24_09 | MENOR | «Arterias nasales (alar inferior, subalar, nasal lateral y nasal dorsal): riesgo elevado de necrosis nasal y, dada la proximidad con la circulación oftálmica, de complicaciones oculares. Arterias supratroclear y supraorbitaria: irrigan la frente y la gla-» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Arterias nasales (alar inferior, subalar, nasal lateral y nasal dorsal): riesgo elevado de necrosis nasal y, dada la proximidad con la circulación oftálmica, de complicaciones oculares. Arterias supratroclear y supraorbitaria: irrigan la frente y la gla- •
p24_10 | MENOR | «bela; su obstrucción puede provocar necrosis cutánea y amaurosis. Arteria temporal superficial: irriga la región temporal, el cuero ca-» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | bela; su obstrucción puede provocar necrosis cutánea y amaurosis. Arteria temporal superficial: irriga la región temporal, el cuero ca- •
p26_11 | MENOR | «Dolor súbito e intenso en el sitio de aplicación.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Dolor súbito e intenso en el sitio de aplicación. •
p26_12 | MENOR | «Palidez inmediata o livedo reticular.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Palidez inmediata o livedo reticular. •
p26_13 | MENOR | «Cianosis progresiva.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Cianosis progresiva. •
p27_03 | MENOR | «Reducción o ausencia del tiempo de reperfusión capilar.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Reducción o ausencia del tiempo de reperfusión capilar. •
p33_08 | MENOR | «AAS (ácido acetilsalicílico) 300 mg/día.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | AAS (ácido acetilsalicílico) 300 mg/día. •
p33_09 | MENOR | «Sildenafil 50 mg (vasodilatación).» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Sildenafil 50 mg (vasodilatación). •
p33_12 | MENOR | «Ultrasonido con Doppler: para localizar obstrucciones y guiar» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Ultrasonido con Doppler: para localizar obstrucciones y guiar •
p33_13 | MENOR | «aplicación de hialuronidasa. Oxigenoterapia hiperbárica: 5 a 10 sesiones en días seguidos,» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | aplicación de hialuronidasa. Oxigenoterapia hiperbárica: 5 a 10 sesiones en días seguidos, •
p33_14 | MENOR | «mejora la oxigenación tisular y la cicatrización.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | mejora la oxigenación tisular y la cicatrización. •
p34_03 | MENOR | «Asociar metronidazol 400 mg cada 8 h para cobertura anaerobia.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Asociar metronidazol 400 mg cada 8 h para cobertura anaerobia. •
p34_14 | MENOR | «Necrosis cutánea.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Necrosis cutánea. •
p34_15 | MENOR | «Infección bacteriana secundaria.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Infección bacteriana secundaria. •
p34_16 | MENOR | «Cicatrización inadecuada.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Cicatrización inadecuada. •
p34_17 | MENOR | «Hiperpigmentación posinflamatoria.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Hiperpigmentación posinflamatoria. •
p36_08 | MENOR | «Conocimiento anatómico detallado.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Conocimiento anatómico detallado. •
p36_09 | MENOR | «Uso de cánulas romas en áreas críticas.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Uso de cánulas romas en áreas críticas. •
p36_10 | MENOR | «Aspiración lenta antes de inyectar con aguja.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Aspiración lenta antes de inyectar con aguja. •
p36_11 | MENOR | «Inyecciones de bajo volumen y presión controlada.» | Bullet «•» presente no fim da linha do PT foi eliminado (regra fixa das decisões comuns: preservar bullets na mesma posição). Sem impacto de sentido, mas a lista perde a marcação na diagramação. | Inyecciones de bajo volumen y presión controlada. •

p6_03 | MENOR | «con alto “swelling factor” tienden a atraer» | 1ª aparição de *swelling factor* no livro sem a glosa prevista em 90-decisiones.md («Swelling Factor, glosado na 1ª aparição»). | La literatura reciente también llama la atención sobre el papel de la técnica en la seguridad del procedimiento. La velocidad y la presión de inyección, el tipo de instrumento utilizado (agujas frente a cánulas), la profundidad elegida y el volumen aplicado son determinantes en el riesgo de intercurrencias. Las técnicas cuidadosas, con inyecciones lentas y depósitos fraccionados en múltiples puntos, se asocian a una reducción significativa de las complicaciones. La aspiración previa puede utilizarse como recurso adicional, pero no debe considerarse un método de seguridad aislado, ya que su precisión es limitada en la práctica clínica. Del mismo modo, la selección adecuada del producto es esencial: los geles más densos y con alto “swelling factor” (capacidad de expansión por absorción de agua) tienden a atraer mayor volumen de agua y a prolongar los edemas en determinadas áreas, mientras que las formulaciones con grado de reticulación elevado pueden aumentar la incidencia de reacciones inflamatorias tardías, nódulos y granulomas.

p21_06 | MENOR | «fueron los angiosomas afectados con mayor frecuencia, y que los segmentos frontonasal y angulonasal fueron las regiones cutáneas más afectadas» | Repetição «afectados… más afectadas» na mesma frase (o PT varia: «envolvidos… acometidas»). | Los resultados demuestran que la arteria facial (58 %) y la arteria oftálmica (48 %) fueron los angiosomas implicados con mayor frecuencia, y que los segmentos frontonasal y angulonasal fueron las regiones cutáneas más afectadas. La afectación del territorio oftálmico se asoció significativamente a complicaciones neurooftalmológicas graves, incluidas la pérdida visual (39 % vs. 0,8 %) y el accidente cerebrovascular (8 % vs. 0,8 %), lo que refuerza la necesidad de cautela en las áreas de alto riesgo anatómico.

## Questões ao autor (não afetam o veredito)

1. **p27_03 vs. p14_02 (prioridade alta, sentido clínico).** O PT lista como sinal clássico «Redução ou ausência do tempo de reperfusão capilar», mas p14_02 descreve corretamente «lentificação do tempo de preenchimento capilar». Na isquemia o tempo de enchimento capilar **aumenta**; «redução do tempo» diz o oposto. A tradução espelhou fielmente («Reducción o ausencia del tiempo de reperfusión capilar»). Sugestão para os dois idiomas: «Aumento del tiempo de llenado capilar o ausencia de reperfusión» / «Aumento do tempo de enchimento capilar ou ausência de reperfusão».
2. **p31_08 (prioridade alta).** «Hialuronidase: injetar 1000 UTR/mL na região afetada» informa concentração, não dose nem volume. O leitor pode ler «1.000 UTR» como dose total. Confirmar se o pretendido é a concentração de preparo e qual a dose/volume por área (o próprio livro cita o HDPH com dose por volume de tecido isquêmico, p18_04).
3. **p23_06.** «vasodilatadores (como ácido acetilsalicílico)»: AAS é antiagregante, não vasodilatador. Trecho resume artigo de terceiros; confirmar se a classificação vem do artigo ou se deve ser «antiagregantes (como el ácido acetilsalicílico)».
4. **p19_09.** O PT escreve «Protocolo de Diagnóstico **de** Reperfusão Rápida»; a forma registrada da sigla PDRR é «Diagnóstico **e** Reperfusão Rápida». O ES seguiu a forma registrada (correto pelo glossário); sugerir corrigir também o PT.
5. **p22_03.** Título «TESTE CLÍNICO DE REPERFUSÃO CAPILAR…» repetido da Figura 2 sobre a Figura 5, que mostra progressão de lesão isquêmica malar/perinasal. Provável título trocado no original.
6. **p28_04/p28_06.** O PT contém um resto de legenda («Esquema ilustrativo dos dois principais mecanismos envolvidos na oclusão vascular induzida por ácido hialu…», cópia truncada da legenda da Figura 8) antes de «Histologia de oclusão vascular…». O ES eliminou o resto e entregou só a legenda correta da Figura 10. Decisão editorial acertada se o texto é sobra invisível de diagramação; conferir no PDF se ele aparece impresso.
7. **p13_04 e p13_05 (HA) vs. restante (AH).** O original alterna «HA» e «AH»; o ES espelhou. Decidir se uniformiza para AH fora de títulos de artigo em inglês.

## Pontos para análise (ordem por custo de não corrigir)

1. Reinserir « •» nos 25 ids da lista (mecânico, 1 passada de script; sozinho leva o índice de 88,1 % para 98,4 %).
2. p31_08: `1000` para `1.000` (formato de dose em conduta de emergência).
3. p20_04: eliminar o calco «con destaque para».
4. p6_03: glosa de *swelling factor* na 1ª aparição.
5. p21_06: repetição «afectados/afectadas».
6. Encaminhar as questões 1 e 2 ao Dr. João antes de fechar a diagramação: não são defeito de tradução, mas são o tipo de ponto que um docente hispano-hablante apontaria em público.

## Voz nativa (camada 4), observações sem achado

Registro usted estável em todo o material (p35_04 «usted revisará»), sem tuteo. Passiva refleja e conectores variados (no obstante, cabe señalar, en este sentido, por consiguiente); «además» aparece 11 vezes em 7.236 palavras, espelhando «além disso» do PT, sem caracterizar repetição. Terminologia consistente: relleno, intercurrencia/complicación (espelha a distinção do autor), lumen, compromiso, afectación, arteria dorsal de la nariz, surco nasolabial (o PT usa nasolabial), hialuronidasa, código QR, clase, «Para saber más», «En la práctica». Gotas capitulares bem resolvidas (p5_00 «E» + «l uso…»; p11_02 «L» + «as intercurrencias…»). Erro de digitação do original corrigido em silêncio no ES: p20_03 «COMPLICAÇÕESOCULARES».

## Propostas de glossário

- `com destaque para` → `con especial participación de` / `destacando` (lista de calcos em 01-voz-y-estilo §1.7).
- `tempo de enchimento/preenchimento capilar` → `tiempo de llenado capilar` (já em 15-intercurrencias como «llenado capilar lento»; acrescentar a forma com «tiempo»).
- `teste de reperfusão capilar` → `prueba de reperfusión capilar` (15-intercurrencias §4).
- `sistema de escore FOEM` → `sistema de puntuación FOEM` (15-intercurrencias §4).
- `angiossoma / angiossomal` → `angiosoma / angiosómico`.
- `compressas mornas` → `compresas tibias` (15-intercurrencias §6).
- `box “Saiba Mais”` → `recuadro “Para saber más”` (FEA-decisoes-comuns).

## Ajustes no auditor

1. **2 BLOQUEANTES falsos (ênclise), linhas 83 e 204 (p18_03, p33_03).** A regra de ênclise casa a palavra inglesa *Hyaluronidase* (terminação «-ase»), dentro de nome de protocolo/título de artigo que corretamente ficou em inglês. Proposta: excluir tokens iniciados por maiúscula que não existem no léxico ES, ou ignorar trechos entre o nome em inglês de artigo/protocolo (heurística: sequência de 3+ palavras capitalizadas em inglês); no mínimo, lista de exceção `Hyaluronidase|Hyaluronic|Release|Phase|Case|Base`.
2. **31 GRAVES falsos (decimal com ponto), linhas 3, 5, 7, 9, 11, 42, 73, 180.** São numerações de seção (`1.1`, `2.10`, `1.1.1`), corretas com ponto. Proposta: não aplicar a regra quando o número está no início da linha ou após « / » e é seguido de espaço + letra (`(?:^|/\s)\d+(?:\.\d+)+\s+\p{L}`), nem a padrões com dois pontos (`\d+\.\d+\.\d+`).
3. **Regra nova sugerida:** sinalizar `\b\d{4,}\s?(UTR|U|mg|mL)\b` sem ponto de milhar (pegaria p31_08), e comparar contagem de « •» entre PT e ES quando o par estiver disponível (pegaria os 25 bullets).
