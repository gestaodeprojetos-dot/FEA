# FEA · Revisão ES · Parte 2 (p. 38 a 74) · Relatório do revisor

REVISÃO: Livro *Intercorrências no preenchimento com ácido hialurônico*, parte 2 · 05/10/2026
Skill: `fea-revision-es` (rubrica em `references/rubrica.md`). Glossários: `00-nucleo.md`, `01-voz-y-estilo.md`, `15-intercurrencias.md`, `90-decisiones.md`, além de `traducao/FEA-decisoes-comuns.md`.

**Cobertura:** os 339 ids de `revisao/parte2-pt-es.json`, com o original PT ao lado (cobertura total). As camadas 1, 2, 3 e 4 rodaram completas. A camada 3b (mídia e QR) foi conferida só contra a planilha `FEA-Traducao-ES-Intercorrencias-Aulas-e-QR.xlsx`: os 4 vídeos da parte 2 (p. 43, 45, 63 e 74) e os 3 QR de artigo (p. 61, 64 e 68) estão inventariados. O script `inventario_midia.py` não foi rodado de novo.

**O que não conta como achado (combinado com quem pediu e com as decisões registradas):** ids partidos por coluna ou no meio de palavra hifenizada; setas "→" trocadas por ":"; ausência de ¿ ¡ « » e de "%" por limitação da fonte; numeração "1.2" e "1.3" com ponto; tudo o que está em `FEA-decisoes-comuns.md`. Observação de processo: o arquivo de revisão vem sem "•" e sem `<b>`. Conferi contra `traducao/parte2-es.json` e os dois estão lá (109 ids com "•", como no PT), então não é achado. As correções abaixo estão escritas no formato do arquivo de revisão; ao aplicar em `parte2-es.json`, mantenha o "•" e o `<b>` que já existem em cada id.

---

## VEREDITO: LIBERADO

| Nível | Resultado |
|---|---|
| Classe A (barreira clínica) | **0**. Nenhuma divergência de dose, unidade, concentração, posologia, via, fármaco, plano, lado, negação, alerta ou omissão |
| Classe B (índice editorial) | **97,3 %** (329 de 338 segmentos limpos) |
| Densidade | 1,14 achados por mil palavras (9 achados em 7.861 palavras) |
| Distribuição | 0 BLOQUEANTE · 1 GRAVE · 8 MENOR |
| Questões ao autor | 9 (não afetam o veredito) |

Denominador: os 338 segmentos que o `auditar.py` contou (o id de uma letra só, p55_07 "C", fica de fora). Se o mesmo achado ocupa dois ids (p49_02 e p49_03), conto os dois.

Ressalva: o veredito vale para a parte 2 isolada. O ponto 1 de "Pontos para análise" (preenchedor traduzido como *relleno* aqui e como *producto de relleno* na parte 3) é inconsistência **entre partes do mesmo livro** e precisa de decisão antes da montagem final.

---

## Camada 1: mecânica (`auditar.py`)

Comando: `python3 .../fea-traduccion-es/scripts/auditar.py p2es.txt` (339 linhas, um valor `es` por linha). Saída: LIBERADO, 0 BLOQUEANTE, 2 GRAVE, 0 MENOR, índice 99,4 %.

Os 2 achados GRAVE do script são **falsos positivos** e não entram na conta:

| Linha | id | Regra disparada | Por que é falso positivo |
|---|---|---|---|
| 64 | p45_06 | decimal com ponto ("1.2") | Numeração de seção "1.2 NECROSIS TISULAR AGUDA…", que leva ponto |
| 189 | p56_02 | decimal com ponto ("1.3") | Numeração de seção "1.3 AMAUROSIS AGUDA…" |

A cobertura de termos dá ausentes *cigomático, nasoyugal, retenedor, ojera, posprocedimiento*. Nada disso aparece no PT desta parte, então a ausência está correta. *Cigomático* aparece só dentro das siglas ZF/ZT (p60_10, "cigomaticofacial", "cigomaticotemporal"), e está certo.

Conferências extras feitas por script: os dígitos do PT e do ES batem em todos os ids (a única diferença é o "12/12h" que virou "cada 12 h" em p50_17, como manda a decisão). Também conferi a contagem de negações (não/nunca/nem/sem contra no/nunca/ni/sin) id a id; as 4 diferenças são só de forma ("No entanto" virou "Sin embargo", "desvinculada" virou "sin relación", "nunca… e" virou "nunca… ni") e nenhuma negação se perdeu.

## Camada 2: segurança clínica (id a id contra o PT)

Nenhuma divergência. Itens conferidos um a um:

- **Hialuronidase:** 1000 UTR/mL (p41_06, p50_04) e 1.000 UTR/mL (p68_09), mantidos como no PT; repetição a cada 15 a 30 min (p41_07, p50_05); repetição por 2 a 3 dias consecutivos (p54_06); flush no trajeto das supraorbitárias, supratrocleares, nasal dorsal, angular/facial e temporal superficial (p68_10); punção com aspiração para refluxo positivo seguida de flush (p69_02/03); retrobulbar ou peribulbar "de eficácia ainda controversa" (p71_04/05), com a ressalva preservada.
- **Fármacos e doses:** AAS 300 mg/día (p41_08, p50_08); sildenafil 50 mg (p41_09), 50 mg VO (p50_09, p70_02); prednisona 40 mg por la mañana (p50_09) e 40 mg/día VO respeitando o ciclo circadiano (p70_03); Diprospan IM (p50_10, p70_04); amoxicilina/ácido clavulánico 875/125 mg VO cada 12 h (p50_17); metronidazol (p50_18); ceftriaxona, piperacilina/tazobactam, carbapenémicos (p50_19); acetazolamida oral o IV, com EV virando IV (p69_07); timolol tópico (p69_08); colagenasa, papaína (p51_10).
- **Tempos:** < 4 h e > 24 h (p40_06/07); 30 min e até 4 h (p40_09); 6 h para o antibiótico (p41_14, p50_16); 6 a 48 h (p45_07, p54_05); 48 a 72 h (p53_08); 3 a 5 dias (p54_05); 4 a 15 min (p57_02); 90 min ou menos (p59_03); 30 a 90 min (p68_07); OHB 5 sessões em 5 dias e até 12 h (p41_15, p50_15, p70_05); compressão de 5 a 10 s (p69_04); dias 17 a 23 (p47); 1, 2, 6, 8 e 19 dias (Fig. 30).
- **Anatomia e lado:** as 11 legendas da Fig. 25 e as 18 siglas da Fig. 26 conferem uma a uma; a oftálmica continua como "rama de la carótida interna" (p58_08); a migração continua "retrógrada contra el flujo" (p56_05, p58_08); oclusão proximal para a gordura e distal para o HA (p66_03, p67_06, p68_05, p69_11) sem inversão; "lábio superior e inferior" (p46_15); "paracentese somente em ambiente especializado" (p69_09).
- **Negações e alertas:** "no es inexistente" (p38_06), "no permanece intraluminal" (p39_03), "sin palidez" (p49_02), "nunca sustituir" (p52_05), "no aparece segundos después" (p66_06), "el déficit no es permanente" (p67_04), "no puede perder tiempo" (p68_07), "(aunque con fiabilidad limitada)" (p53_14). Todos preservados, nenhum suavizado.

## Camada 3: back-translation

Retraduzi para o PT, sem olhar o original, os blocos de protocolo (p41_03 a p41_15, p50_02 a p50_19, p68_07 a p70_05, p71_02 a p71_05), de fisiopatologia (p46_04 a p46_10, p53_03 a p53_08, p56_03 a p59_07), de diagnóstico diferencial (p48_14 a p49_04, p62_05 a p67_05) e as legendas técnicas (Fig. 14, 20, 25, 26, 28, 29, 30). Comparei com o PT. A ordem dos passos do PDRR (1 a 6), a sequência do continuum isquêmico e a sequência das condutas na amaurose saíram idênticas. Não apareceu nenhum ligamento ou artéria trocado, nenhum passo invertido e nenhum "não" perdido.

Ambiguidades do PT que a tradução manteve de propósito, e corretamente: p54_05 ("después de 6 a 48 horas"), p70_05 ("hasta 12 h después del evento"), p40_09 ("el cuadro puede revertirse").

## Camada 4: voz nativa e consistência

O texto lê como espanhol técnico de docente: passiva refleja nas descrições, usted e imperativo formal ("Acceda", "escanee"), conectores variados (*asimismo, por su parte, de ahí*), nenhum `el mismo` pronominal, nenhum `a nivel de`, `donde` sem lugar já resolvido ("fase intermedia, en la que", p46_10; "en los que", p63_03). Falsos amigos tratados: *signo* (nunca *señal*), *derivado* (p71_02), *seguimiento* (p41_04, p54_05), *historia clínica* (p52_05), *apósitos*, *reportes*.

Consistência interna da parte 2 conferida: preenchedor = *relleno* (em todas as ocorrências); ultrassom = *ultrasonido*, ultrassonografia = *ultrasonografía*; supraorbital/supraorbitária = *supraorbitaria*; fronte = *frente*; têmpora = *sien*; conduta = *conducta*; sinais = *signos*; angiossomo = *angiosoma*; angiografia fluoresceínica = *angiografía con fluoresceína*. *Arteria dorsal nasal* e *arteria nasal dorsal* convivem porque o PT também varia (ver Questão ao autor 8).

---

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id corrigido)`

### BLOQUEANTE

Nenhum.

### GRAVE

**p74_05 | GRAVE | "…dentro del vaso. Esta relación en-" (em `traducao/parte2-es.json`) | O arquivo de produção e o de revisão divergem neste id. O de revisão termina em "Esta relación entre"; o de produção, em "Esta relación en-". A parte 3 já começa o bloco seguinte (p75_02) por "anatomía y dinámica de flujo…", sem o "tre". Do jeito que está na produção, o leitor lê "Esta relación en- anatomía y dinámica…", com uma palavra partida que não fecha. O relatório da tradutora pedia que a parte 3 começasse por "tre", e ela não fez isso. Erro de montagem entre partes, sem efeito clínico, mas visível na página. | La comprensión anatómica del complejo vascular nasoglabelar presentada en la clase práctica cobra aún más relevancia cuando se correlaciona con los distintos patrones de diseminación intravascular del relleno. Al visualizar la disposición tridimensional de las ramas arteriales y sus anastomosis con el sistema oftálmico, es posible entender cómo las variaciones en la presión de inyección, en el plano elegido y en la dirección del instrumento pueden determinar el comportamiento del émbolo dentro del vaso. Esta relación entre**

### MENOR

**p49_02 + p49_03 | MENOR | "sin palidez y, en general, con / mejoría con la compresión local" | Dois "con" seguidos ("con mejoría con la compresión"). O decalque do PT "há melhora com compressão" fica pesado; em espanhol sai mais natural com o verbo. | p49_02: Hematoma: coloración violácea, sin palidez y, en general, · p49_03: mejora con la compresión local. Edema inflamatorio: piel caliente y enrojecida, sin livedo**

**p50_14 | MENOR | "para mapear área y extensión de la obstrucción" | Faltam os artigos, um estilo telegráfico que o PT também tem mas que em espanhol soa a rascunho. | Ultrasonido Doppler para mapear el área y la extensión de la obstrucción.**

**p58_02 | MENOR | "este mecanismo de obstrucción en el plano intraocular" | Num livro de anatomia injetável, *plano* é termo técnico (plano de inyección, plano supraperióstico). Aqui o PT diz "em nível intraocular", e *plano* pode ser lido como plano anatômico. | Las conexiones anatómicas entre los territorios facial y oftálmico explican la vía de acceso del material inyectado al sistema infraorbitario. Cuando se produce una embolización retrógrada hasta la arteria oftálmica, el compromiso puede avanzar hacia sus ramas terminales, en especial la arteria central de la retina, estructura crítica para el mantenimiento de la visión. La figura siguiente ilustra este mecanismo de obstrucción en el interior del ojo.**

**p59_04 | MENOR | "OTROS MECANISMOS CONTRIBUYENTES:" | Em espanhol, *contribuyente* como substantivo e adjetivo corrente remete a quem paga impostos. Em texto clínico usa-se a oração relativa ou *coadyuvantes*. | OTROS MECANISMOS QUE CONTRIBUYEN:**

**p64_02 | MENOR | "Diagnóstico diferencial de la amaurosis aguda posrelleno" | *posrelleno* é formação pouco natural: o prefixo *pos-* em espanhol se cola a adjetivo ou nome de processo consolidado (*posprocedimiento*, *posinflamatoria*), e *posrelleno* não se lê assim. | Diagnóstico diferencial de la amaurosis aguda tras el relleno**

**p68_06 | MENOR | "CONDUCTA ANTE LA AMAUROSIS AGUDA POSRELLENO - CONDUCTA INMEDIATA" | Mesmo problema de p64_02. Corrigir os dois juntos para não abrir inconsistência. | CONDUCTA ANTE LA AMAUROSIS AGUDA TRAS EL RELLENO - CONDUCTA INMEDIATA**

**p67_04 | MENOR | "El paciente suele tener antecedentes previos" | Pleonasmo: *antecedentes* já são prévios. Vem herdado do PT "histórico prévio", e o leitor hispano nota. | El paciente suele referir antecedentes, y el déficit no es permanente. Espasmo vascular transitorio inducido por el procedimiento**

Total MENOR: 8 segmentos (p49_02, p49_03, p50_14, p58_02, p59_04, p64_02, p68_06, p67_04).

---

## PONTOS PARA ANÁLISE (ordem: custo de não corrigir)

1. **Preenchedor como produto: *relleno* (parte 2) ou *producto de relleno* (parte 3).** A parte 2 usa *relleno / rellenos* para o produto em todas as ocorrências (dezenas de ids, por exemplo p39_03, p40_03, p49_05, p56_05, p69_11). Já a parte 3 abre com "inyección de productos de relleno" (p75_04). O núcleo traz "preenchedor / preenchimento → producto de relleno / relleno", sem decisão registrada que permita *relleno* para o produto. *Rellenos de ácido hialurónico* e *rellenos dérmicos* são uso legítimo e corrente em espanhol, por isso não marquei como erro aqui. O problema é o livro sair com dois nomes para o mesmo objeto, que é o defeito que o aluno mais percebe. **Recomendação:** registrar em `FEA-decisoes-comuns.md` a forma única. Minha indicação é *relleno* (mais curto, cabe nas caixas, é a forma da literatura LatAm) e reservar *producto de relleno* para quando houver risco de confundir com o procedimento. Depois, alinhar as partes que divergirem. Esse é o ponto de maior custo do lote, porque cruza todas as partes.
2. **p74_05 (GRAVE acima):** corrigir em `parte2-es.json` antes da montagem, senão a junção entre as páginas 74 e 75 sai com a palavra partida.
3. **Rótulos de vídeo: livro e planilha divergem.** A planilha de aulas e QR propõe "Relleno full face guiado por **ecografía**, en vivo" e "Rinomodelación: **¿aguja o cánula?**", mas o livro diz "ULTRASONIDO" (p45_03) e "AGUJA O CÁNULA" sem interrogação (p43_08). Esses rótulos vão ser o título da aula dublada; vale escolher uma forma e espelhar nos dois. Sugestão: *ultrasonido* (coerente com o resto do livro) e, na planilha, manter o "¿?" só se a arte da aula tiver fonte com "¿".
4. **posrelleno (p64_02, p68_06):** se outras partes usarem *posrelleno*, corrigir em bloco.
5. Os demais MENOR são isolados e podem entrar na mesma rodada de ajuste.

---

## QUESTÕES AO AUTOR (não afetam o veredito)

1. **Janelas de tempo da retina incoerentes no original:** p40_09 (30 min, até 4 h), p57_02 (4 a 15 min), p59_03 (90 min ou menos), p68_07 (30 a 90 min). O leitor atento vai notar quatro números para a mesma janela. Pedir ao Dr. João que uniformize ou explicite a que cada número se refere.
2. **"FIGURA 27" duplicada** (p62_02 e p65_02); a numeração segue 28, 29… Renumerar exige mexer nas referências cruzadas.
3. **Legenda da Figura 31 (p71_07) é cópia da legenda da Figura 30.** O título é "TÉCNICA DE ACCESO RETROBULBAR", mas o texto começa com "Figura 30." e descreve a evolução clínica. Falta a legenda real.
4. **"sistema/ramos infraorbitários" da oftálmica** (p57_06, p58_02): o esperado seria *orbitário*. Tradução espelhada.
5. **Sigla STA = artéria supratroclear** (p60_10): na literatura, STA costuma ser a temporal superficial. O PT diz que segue a imagem original; confirmar.
6. **Imagens declaradas "criadas com IA"** (p38_05, p39_03): a linha vermelha 7 do CLAUDE.md da FEA proíbe imagem gerada por IA em entregável final. A decisão é da Keila e do autor; a tradução está fiel.
7. **p61_03:** o PT repete quase literalmente a primeira frase na segunda. A tradução fundiu as duas sem perder informação; corrigir também no PT.
8. **"artéria dorsal nasal" e "artéria nasal dorsal"** convivem no original (p38_05, p55_08, p56_05 contra p59_09, p60_04, p60_10), e a tradução espelhou. Recomendo uniformizar nos dois idiomas, e no ES preferir *arteria dorsal de la nariz* ou *arteria nasal dorsal* de forma única.
9. **1000 UTR/mL (p41_06, p50_04) e 1.000 UTR/mL (p68_09):** a tradução espelhou o PT, e as duas grafias são aceitas pela RAE para quatro dígitos. Uniformizar é decisão editorial, não de tradução.

---

## PROPOSTAS DE GLOSSÁRIO (para `15-intercurrencias.md` / `90-decisiones.md`)

| PT | ES | Observação |
|---|---|---|
| preenchedor (produto) | **decidir:** *relleno* ou *producto de relleno* | Ver Ponto 1; registrar em `FEA-decisoes-comuns.md` |
| angiossomo | angiosoma | |
| choke vessels | "choke vessels" | conservado em inglês, entre aspas |
| angiografia fluoresceínica | angiografía con fluoresceína | |
| fundoscopia | fondoscopia | |
| sobreposição infecciosa | sobreinfección | |
| curativo (oclusivo, bioativo) | apósito | |
| enzimas lisossômicas | enzimas lisosomales | |
| betabloqueador | betabloqueante | |
| amaurose temporária | amaurosis transitoria | evita confusão com "temporal" |
| moscas volantes | moscas volantes (alt.: miodesopsias) | |
| OACR | OACR (oclusión de la arteria central de la retina) | a sigla fecha em ES |
| pós-preenchimento (adjetivo) | tras el relleno | evitar *posrelleno* |
| mecanismos contribuintes | mecanismos que contribuyen / coadyuvantes | evitar *contribuyentes* |
| em nível intraocular | en el interior del ojo / a nivel intraocular | evitar *plano* fora do sentido anatômico |

## AJUSTES NO AUDITOR

- **Falso positivo "decimal com ponto" em numeração de seção** (p45_06, p56_02). Regra proposta: ignorar o padrão `^\s*\d+\.\d+\s+[A-ZÁÉÍÓÚÑ]` (número de seção no início da linha, seguido de título em maiúscula). Já tinha sido sugerido no relatório da tradução; confirmar a implementação em `auditar.py`.
- **Sugestão de regra nova (MENOR):** sinalizar `\bpos(relleno|inyección|aplicación)\b` e `antecedentes previos`, duas formas que passaram sem alerta nesta parte.
