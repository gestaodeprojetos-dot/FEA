# REVISÃO · Intercorrências no Preenchimento com Ácido Hialurônico (ES) · Rodada 2 (delta) · 05/10/2026

Cobertura: 75 segmentos de `rodada2-delta-pt-es.json` (1.904 palavras ES), revisados id a id contra o original PT incluído no próprio arquivo. São só os trechos alterados depois da 1ª revisão: itens de lista separados e reescritos, e correções aplicadas (ecografía, llenado capilar, complacencia, 1.000 UTR/mL, festón, swelling factor). Negrito e marcadores retirados de propósito do PT não foram tratados como achado. O restante do livro não foi relido nesta rodada; a cobertura de consistência interna vale só para o delta.

Referências aplicadas: `FEA-decisoes-comuns.md` (incluindo as decisões da revisão cega de 05/10/2026), `00-nucleo.md`, `01-voz-y-estilo.md`, `15-intercurrencias.md`, `90-decisiones.md`, rubrica da skill.

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 96,0 %  (72 de 75 segmentos limpos)
                               1,58 achados por mil palavras (3 / 1.904)
                               0 GRAVE · 3 MENOR
  Questões ao autor: 4  (não afetam o veredito)
```

## Camada 1 · Mecânica (auditar.py)

`auditar.py` sobre o texto ES do delta: 0 BLOQUEANTE, 0 GRAVE, 0 MENOR, índice 100 %, exit 0. Os avisos de "termo obrigatório ausente" (nasoyugal, retenedor, ojera, grasa, seguimiento, posprocedimiento) são falso positivo de escopo: a lista de cobertura é a do módulo de olheiras e esses termos não ocorrem nos 75 segmentos deste delta. Ver AJUSTES NO AUDITOR.

## Camada 2 · Segurança clínica (id a id)

Conferido e idêntico ao PT, sem conversão, arredondamento nem troca:

| id | PT | ES | Situação |
|---|---|---|---|
| p31_08 | 1000 UTR/mL | 1.000 UTR/mL | OK (milhar com ponto, decisão fixa) |
| p41_06 | altas doses (1000 UTR/ml) | altas dosis (1.000 UTR/mL) | OK (ml normalizado para mL, mesma unidade) |
| p50_04 | 1000 UTR/mL, a cada 15–30 minutos | 1.000 UTR/mL, cada 15 a 30 minutos | OK |
| p68_10 | alta dose (1.000 UTR/mL); flush supraorbitárias, supratrocleares, nasal dorsal, angular/facial, temporal superficial | idem, mesmas 5 artérias, mesma ordem | OK |
| p50_08 / p70_02 | sildenafil 50 mg VO | sildenafil 50 mg VO | OK |
| p50_09 | prednisona 40 mg pela manhã; diprospan IM | prednisona 40 mg por la mañana; Diprospan IM | OK |
| p70_03 | prednisona 40 mg/dia VO, ciclo circadiano, ou diprospan IM | prednisona 40 mg/día VO ... o Diprospan IM | OK |
| p70_04 | uma sessão imediata, até 12h após o evento | una sesión inmediata, hasta 12 h después del evento | OK |
| p33_13 | 5-10 sessões em dias seguidos | 5 a 10 sesiones en días seguidos | OK |
| p40_07 | > 24h | > 24 h | OK |
| p40_08 | 30 minutos; até 4 horas como período máximo | 30 minutos; hasta 4 horas ... como período máximo | OK |
| p75_06 | até 90 minutos sem oxigenação; chance mínima | hasta 90 minutos; probabilidad mínima | OK |
| p75_07 | <1h; recuperar parcialmente | menos de 1 h; recuperar parcialmente | OK |
| p69_04 | 5 a 10 segundos de compressão seguidos de relaxamento | 5 a 10 segundos de compresión seguidos de relajación | OK |
| p21_06 | 58 %, 48 %, 39 % vs. 0,8 %, 8 % vs. 0,8 % | idênticos | OK |
| p106_04 | até 20% dos casos | hasta en el 20 % de los casos | OK (ver Questão 2) |
| p71_04 | retrobulbar ou peribulbar; eficácia controversa | retrobulbar o peribulbar; eficacia controvertida | OK, alerta preservado |

Negações conferidas: p6_03 (aspiração "no debe considerarse" método isolado), p49_02 (sin palidez), p49_03 (sin livedo), p49_04 (sin patrón segmentario), p67_04 (déficit no es permanente), p112_11 (No restringir los movimientos), p61_03 (rellenos que no son a base de AH son irreversibles). Todas preservadas.

Anatomia, planos e sentido: p24_04 a p24_10 (7 artérias, territórios e consequências um a um), p24_07 (canto medial), p58_02 (embolização retrógrada até a oftálmica, ramos terminais, artéria central da retina), p75_04 (Tipos I a IV: distal, proximal, anterógrada, retrógrada), p183_05 (ligamento orbitario y cigomático-cutáneo), p51_12 (indicação cirúrgica: extensas, gruesas o infectadas). Nada invertido.

Fármacos e termos: hialuronidasa, colagenasa, papaína, Diprospan, sildenafil, prednisona, oxigenoterapia hiperbárica, terapia LED. Grafia correta.

Correções da 1ª revisão confirmadas no delta: ecografía Doppler / apoyo ecográfico (p7_02, p33_12, p41_13, p45_04, p50_13, p61_03), llenado capilar (p124_20), de menor / baja complacencia (p132_06, p137_07), 1.000 UTR/mL (p31_08, p41_06, p50_04, p68_10), festón (festoon) na 1ª aparição (p183_05), swelling factor glosado (p6_03), relleno para preenchedor (p41_06, p59_06, p61_03, p75_04). Nenhum resíduo de "ultrasonido", "complaciente", "relleno capilar" ou "1000" sem ponto no delta.

## Fidelidade item a item (listas separadas)

Todos os itens separados correspondem ao item PT do mesmo id, sem perda nem mistura: p24_04 a p24_10, p42_03 a p42_05, p43_03 a p43_05, p43_10, p46_06 a p46_08, p49_02 a p49_04, p51_10 a p51_12, p53_05 e p53_06, p61_10 a p61_13, p68_09 e p68_10, p69_02 a p69_04, p70_02 a p70_04, p75_06 e p75_07. Dois ids ainda trazem dois itens juntos no PT (p49_03: edema inflamatório + infecção precoce; p67_04: fim de um item + rótulo do seguinte); o ES espelha exatamente a mesma fusão e a mesma ordem, e no PDF original não há marcador entre eles, então não é falha de tradução (ver PONTOS PARA ANÁLISE).

## Camada 3 · Back-translation dos trechos técnicos

Retraduzidos sem olhar o PT e depois comparados: p31_08, p41_06, p50_04, p68_10, p69_02 a p69_04, p70_02 a p70_04, p40_08, p75_04, p75_06, p58_02, p51_10 a p51_12. Estrutura, ordem dos passos e números voltam idênticos. Única nuance lógica encontrada está em p7_02 (MENOR [1]).

## Camada 3b · Mídia e QR

Fora do escopo deste delta (nenhum id novo de QR ou vídeo; p45_04 e p61_03 são textos descritivos de QR já inventariados nas partes 1 a 6). Nada a acrescentar ao inventário.

---

## BLOQUEANTE

Nenhum.

## GRAVE

Nenhum.

## MENOR

| # | id | severidade | trecho | problema | correção proposta (texto ES completo do id) |
|---|---|---|---|---|---|
| 1 | p7_02 | MENOR (fidelidade lógica) | "...la detección precoz de áreas comprometidas, ya que guía con mayor precisión la infiltración de la enzima." | O PT lista dois benefícios em sequência ("detecção precoce..., guiando de maneira mais precisa a infiltração"). O "ya que" transforma o segundo em causa do primeiro: a ecografia não é útil na detecção *porque* guia a enzima. | En los últimos años, el desarrollo y la estandarización de protocolos de manejo de emergencia consolidaron la conducta ante eventos graves. El uso precoz y en dosis adecuadas de hialuronidasa sigue siendo la principal estrategia para disolver el producto en situaciones de oclusión vascular o compresión tisular. Estudios recientes también destacan la utilidad de la ecografía Doppler en la detección precoz de áreas comprometidas, y permite guiar con mayor precisión la infiltración de la enzima. Las conductas adyuvantes, como la oxigenoterapia hiperbárica, las terapias de luz y la antibioticoterapia profiláctica en casos de infección asociada, también han demostrado ser relevantes en determinados contextos. |
| 2 | p49_02 | MENOR (voz) | "sin palidez y, en general, con mejoría con la compresión local" | "con ... con" encadeado soa decalque; um docente hispano-hablante escreveria com verbo. | Hematoma: coloración violácea, sin palidez y, en general, mejora con la compresión local. |
| 3 | p50_13 | MENOR (voz) | "para mapear área y extensión de la obstrucción" | Falta de artigo antes de substantivos coordenados, padrão do PT ("mapear área e extensão") que não soa nativo em ES. | Ecografía Doppler para mapear el área y la extensión de la obstrucción. • |

Observação sobre p7_02: se a preferência for manter subordinação, alternativa equivalente: "...en la detección precoz de áreas comprometidas y en la guía más precisa de la infiltración de la enzima."

## Correções silenciosas do original (registradas conforme regra do projeto)

| id | Erro no PT | Tratamento no ES |
|---|---|---|
| p75_06 | "cwhance" (digitação) | "probabilidad", correto |
| p61_03 | frase duplicada ("revisa de forma abrangente as complicações isquêmicas associadas aos preenchedores dérmicos" aparece duas vezes seguidas) e "aspiraçã o" | ES fundiu as duas frases numa só sem perder conteúdo ("desde la necrosis cutánea hasta eventos neurooftalmológicos graves" preservado); "aspiración" correto |
| p24_05 | concordância singular "irriga ... pode causar" com sujeito plural (Artérias Labiais) | ES em plural ("irrigan ... pueden causar"), correto |
| p24_04 a p24_10, p43_05, p50_04, p51_11, p51_12, p53_06, p69_04, p70_02 a p70_04, p71_04, p75_07 | hifenização do InDesign ("com- prometer", "consid- erado") | juntada antes de traduzir, correto |

## QUESTÃO AO AUTOR

1. **p58_02 · "sistema infraorbitário".** O parágrafo descreve embolização retrógrada até a artéria oftálmica e a artéria central da retina, isto é, território intraorbitário. "Infraorbitário" (abaixo da órbita) parece não ser o termo pretendido; o mesmo ocorre em p57_06 ("ramos infraorbitários" da oftálmica). A tradução espelha o original ("sistema infraorbitario"), como deve. Confirmar com o Dr. João se o correto é "intraorbitário"/"orbitário"; se sim, corrigir nos dois idiomas.
2. **p106_04 · sintaxe do PT.** "pode ocorrer em até 20% dos casos necessidade de observação hospitalar" está truncado no original. O ES interpretou como consequência ("lo que hace necesaria la observación hospitalaria"), leitura clinicamente coerente e que não suaviza o alerta. Confirmar a intenção; se o autor quiser dois enunciados separados, ES alternativo: "Reacción bifásica: puede ocurrir hasta en el 20 % de los casos; se requiere observación hospitalaria. •"
3. **p40_08 x p75_06 · janelas de tempo.** O livro fala em 30 minutos como tempo para melhor prognóstico, 90 minutos de tolerância retiniana e até 4 horas como período máximo de reversão. As três cifras estão fiéis ao PT; vale o autor conferir se a convivência delas está clara para o leitor.
4. **p188_11 · "Fonte: Imagem gerada por IA".** Tradução fiel. Não é questão de tradução, mas o CLAUDE.md do projeto proíbe imagem clínica gerada por IA em entregável final (linha vermelha 7). Sinalizar à Keila antes de enviar ao designer.

## PONTOS PARA ANÁLISE (ordenados por custo de não corrigir)

1. **Marcadores "•" residuais no ES (produção).** 10 ids do ES terminam com "•" (p41_13, p50_13, p67_04, p106_04, p112_11, p117_09, p132_06, p137_07, p147_05, p194_12), enquanto o PT do delta veio sem marcadores. Conferido nas partes 2 a 4: o PDF original tem o "•" no fim da linha nesses pontos (é o marcador do item seguinte), então a posição está correta pela regra "preservar na mesma posição". Risco: se o `traduzir_pdf` agora gera o marcador por item, esses "•" podem sair duplicados ou pendurados. Conferir na prova de diagramação.
2. **p7_02 (MENOR [1])**: único ponto com deslocamento lógico; corrigir antes da prova.
3. **p49_03 e p67_04**: itens que continuam fundidos porque o PDF não tem marcador entre eles. Se o designer criar lista visual, separar também no ES ("Edema inflamatorio: ... | Infección precoz: ..."; "...el déficit no es permanente. | Espasmo vascular transitorio inducido por el procedimiento").
4. **p49_02 e p50_13 (MENOR [2] e [3])**: ajuste de voz, baixo custo.

## PROPOSTAS DE GLOSSÁRIO

- `15-intercurrencias.md`, seção 4: trocar "enchimento capilar lentificado → llenado capilar lento" por bloco que inclua também "reperfusão capilar → llenado capilar" (decisão aplicada em p124_20).
- `15-intercurrencias.md`, seção 6: acrescentar "compressas mornas → compresas tibias", "LED-terapia → terapia LED", "curativo oclusivo → apósito oclusivo", "fundoscopia → fondoscopia".
- `90-decisiones.md`: registrar as decisões da revisão cega de 05/10/2026 que hoje só estão em `FEA-decisoes-comuns.md` (ecografía, complacencia, festón, llenado capilar, 1.000 UTR/mL), para valerem nos próximos materiais e não só neste livro.

## AJUSTES NO AUDITOR

- A "cobertura de termos obrigatórios" do `auditar.py` usa uma lista fixa do módulo de olheiras (nasoyugal, retenedor, ojera, grasa...). Num livro de intercorrências ela gera 6 avisos falsos. Proposta: carregar a lista por módulo (`--modulo 15`) ou desligar a cobertura quando o texto for um delta parcial.
- Regras novas sugeridas, como GRAVE: `ultrasonido` (deve ser ecografía neste livro), `complaciente` aplicado a tecido, `relleno capilar`, e `\b\d{4}\s?UTR` sem ponto de milhar (BLOQUEANTE de formatação de dose).
