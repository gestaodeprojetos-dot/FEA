# FEA · Revisão ES das páginas do Ebook Olheiras LATAM · 26/10/2026

Revisor: skill `fea-revision-es` (leitura de par especialista, 4 camadas). Nada foi editado no Drive; este arquivo é o produto.

**Base aplicada.** `fea-revision-es/SKILL.md` e `references/rubrica.md`; `fea-traduccion-es/references/00-nucleo.md`, `01-voz-y-estilo.md`, `11-rellenos-ah-ojeras.md` (módulo do tema) e `90-decisiones.md`; `FEA-regras-correcao-copys-latam.md`. Decisões registradas ali (US$19 de US$47, 60 %, upsell US$97 "Curso de Relleno Express", 30.000 alumnos, 9 países, 10.000 ml, +30 mil copias, marcadores `[... PENDIENTE]`, sem cronômetro, usted, depoimentos em PT com legenda ES, reescrita de tom autorizada) **não foram tratadas como achado**.

**Camada 1 (script).** Texto ES de cada doc (só o corpo, sem o bloco interno "Notas para a equipe") salvo em `/tmp/claude-0/-home-user-FEA/6500f297-8601-53d4-bc7c-33986b7f95c3/scratchpad/rev-paginas/01-ventas.txt` a `06-gracias.txt` e auditado com `auditar.py`. Todos os achados do script foram falsos positivos (ver "Ajustes no auditor"). Os denominadores de segmento abaixo são os do script.

**Camada 2 (segurança clínica).** Conferidos contra o PT: números (3 e 4 puntos de entrada, 7 días de garantía, 10.000 ml), planos e camadas ("capa ideal de aplicación", "layering (por capas)"), reologia (alto G’, menor higroscopicidad, partículas, entrecruzamento), nomes de complicação (edema persistente, efecto Tyndall, hematomas, irregularidades de relieve). Nenhuma divergência. Não há dose, via ou fármaco nestas páginas.

**Camada 3 (back-translation).** Retraduzidos sem olhar o original: os 5 módulos "✅" (páginas longa e curta), os 4 pasos, Bloques 3, 5 e 6 da Copy Página. Único desvio de sentido: Bloque 6 (generalização de um fabricante para "la industria"), registrado abaixo. Perda de termo de autor (pertuito) também registrada.

**Camada 3b (mídia/QR).** Não há QR Code nestas páginas. Imagens estão como marcador `[IMAGEN: ...]` (decisão registrada). Único ativo de vídeo: o vídeo de vendas do CPX na página de upsell, já sinalizado pelo próprio doc como "confirmar versión en español"; tratado como pendência registrada, listado em Questão ao autor.

**Linha vermelha FEA (varredura em todos os docs).** Zero em-dash no corpo ES. Zero emoji corrompido (só ✅ ✔️ ❌ ⛔ ♾️). Zero tuteo/voseo. Zero resíduo BR (R$, Pix, boleto, +55, "Brasil"). Marca de produto: só "MD Codes" (já pendente no doc). Restam dois pontos de linha vermelha: promessa de resultado estético na headline e no módulo de layering (páginas longa e curta) e status de compra simulado no upsell.

---

## 1. FEA-ES | Página de ventas - eBook de Ojeras · `1DcfgS833430UPwl7_X1E9WLBkbWc2ek37udyS0ylLSE`

```
REVISÃO · Página de ventas (longa) · 26/10/2026
Cobertura: completa. Original PT lido: «Página de vendas - Ebook de Olheiras»
           (19pNmOFaZGSo2l6BmQg0ifPAd24_1uhDiwIjinNM8Xk8, 22.09.2025).

VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 85,7 %  (102 de 119 segmentos limpos)
                               13,72 achados por mil palavras (17 em 1.239)
                               6 GRAVE · 11 MENOR
  Questões ao autor: 2  (não afetam o veredito)
```

### GRAVE

**[1.1] Linha vermelha 1 · promessa de resultado estético (headline)**
- Original PT: «…e alcance resultados naturais, seguros e duradouros.»
- Trecho ES exato: `Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y trabaje con seguridad, previsibilidad y resultados naturales y duraderos.`
- Problema: "resultados naturales y duraderos" é desfecho estético do paciente, não técnico. A regra FEA manda vincular "resultado" a segurança ou técnica.
- Correção: `Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y trabaje con seguridad, previsibilidad y una técnica reproducible caso a caso.`

**[1.2] Linha vermelha 1 · promessa de resultado estético (módulo layering)**
- Original PT: «Domine a técnica de Layering (camadas) para resultados naturais e duradouros.»
- Trecho ES exato: `Domine la técnica de layering (por capas) para resultados naturales y duraderos.`
- Problema: mesmo motivo de [1.1].
- Correção: `Domine la técnica de layering (por capas) para un depósito controlado del producto en cada plano.`

**[1.3] Terminologia fora do glossário · "complicações" virou "intercurrencias" (3 ocorrências)**
- `90-decisiones.md`: *intercurrencias* traduz intercorrências; *complicaciones* traduz complicações, "que o autor usa como termo distinto". O próprio doc mantém "Manejo de Complicaciones" no título do módulo, o que deixa o par inconsistente.
- a) Original «Insegurança diante de complicações como edema…» · Trecho ES: `❌ Inseguridad ante intercurrencias como edema, irregularidades o efecto Tyndall.` · Correção: `❌ Inseguridad ante complicaciones como edema, irregularidades o efecto Tyndall.`
- b) Original «Complicações e soluções – como diagnosticar e tratar com segurança.» · Trecho ES: `Intercurrencias y soluciones: cómo diagnosticarlas y tratarlas con seguridad.` · Correção: `Complicaciones y soluciones: cómo diagnosticarlas y tratarlas con seguridad.`
- c) Original «…evitando complicações.» · Trecho ES: `Aprenda a seleccionar los productos más adecuados para ojeras y a evitar intercurrencias.` · Correção: `Aprenda a seleccionar los productos más adecuados para ojeras y a evitar complicaciones.`
- Alternativa válida: se a gestão preferir "intercurrencias" em toda copy comercial, registrar a decisão em `90-decisiones.md` e o achado deixa de existir.

**[1.4] Termo de autor perdido · pertuito**
- Original PT: «Descubra os pontos corretos de acesso (pertuitos).»
- Trecho ES exato: `Descubra los puntos de acceso correctos (puntos de entrada).`
- Problema: `pertuito` é termo de autor conservado (`90-decisiones.md`, `11-rellenos-ah-ojeras.md`). A página troca pelo genérico e quebra a ponte com o ebook, onde o leitor vai encontrar "pertuito".
- Correção: `Descubra los puntos de acceso correctos (pertuitos).`

### MENOR

**[1.5] Swelling Factor sem glosa na 1ª aparição**
- Trecho ES exato: `Domine el concepto de Swelling Factor (SF) y su influencia en el resultado final.`
- Problema: o módulo 11 manda glosar a 1ª aparição como «factor de hinchazón».
- Correção: `Domine el concepto de Swelling Factor (SF), o factor de hinchazón, y su influencia en el resultado final.`

**[1.6] Title Case à moda portuguesa em títulos (9 ocorrências)**
Norma ES: maiúscula só na 1ª palavra e em nomes próprios (`01-voz-y-estilo.md` §3). O título do livro fica como está (ver Questão T1).

| Trecho ES exato | Correção |
|---|---|
| `Introducción al Razonamiento Clínico para el Relleno de Ojeras` | `Introducción al razonamiento clínico para el relleno de ojeras` |
| `Anatomía de la Región Infraorbitaria` | `Anatomía de la región infraorbitaria` |
| `Reología: La Elección del Producto de Relleno Ideal` | `Reología: la elección del producto de relleno ideal` |
| `Técnica Avanzada de Relleno Tridimensional` | `Técnica avanzada de relleno tridimensional` |
| `Intercurrencias y Manejo de Complicaciones` | `Intercurrencias y manejo de complicaciones` |
| `Sección de la Oferta` | `Sección de la oferta` |
| `+03 Bonos Exclusivos` | `+03 bonos exclusivos` |
| `Oferta Especial` | `Oferta especial` |
| `FAQ (Preguntas Frecuentes)` | `FAQ (preguntas frecuentes)` |

**[1.7] Título em caixa alta integral**
- Trecho ES exato: `¿LE QUEDÓ ALGUNA DUDA?`
- Problema: anti-padrão FEA (headline em caixa alta integral), herdado do PT. Se o efeito de caixa alta for desejado, que seja por CSS.
- Correção: `¿Le quedó alguna duda?`

### QUESTÃO AO AUTOR
- **[1.Q1] MD Codes.** `Comparación con otras técnicas: MD Codes y demás abordajes clásicos.` MD Codes é método associado a fabricante (linha vermelha 3). O doc já marca como pendente; confirmar se pode ser citado na página LATAM ou trocar por `Comparación con otras técnicas y abordajes clásicos.`
- **[1.Q2] Afirmação de autoridade acrescentada.** `En 2019, decidí dedicarme a los procedimientos mínimamente invasivos en la medicina estética, con un foco claro: la anatomía como base de la seguridad. Desde entonces, estudio la región facial en cadáveres frescos…` não existe no PT (que falava de "vida épica"). A reescrita é coerente com a regra de tom, mas cria um fato datado ("desde 2019, cadáveres frescos"). Confirmar com o Dr. João que a cronologia está correta.

---

## 2. FEA-ES | [NUEVA] Página de ventas - eBook de Ojeras · `1pB0_8kKRS-VI3xZ8kOCDhcEoBqdJzvTJ5MvfYLruCJc`

```
REVISÃO · [NUEVA] Página de ventas · 26/10/2026
Cobertura: completa. Original PT lido: «[NOVA] Página de vendas - Ebook de Olheiras»
           (1Wzgl5qNOVhIUMCD0V_rK9zYJCu-nn3_Z41HQqh7QueA, 14.05.2026).
           Bloco "INSIGHTS PARA COPY" do PT ausente por decisão registrada no doc (não vai ao ar).

VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 99,2 %  (118 de 119 segmentos limpos)
                               0,75 achados por mil palavras (1 em 1.341)
                               1 GRAVE · 0 MENOR
  Questões ao autor: 0
```

A reescrita de tom (blocos 1, 3, 4, 7 e 10) cumpre a regra FEA: a dor virou técnica (plano, edema, intercurrencias isquémicas), sem medo, sem paciente "infeliz", sem gênero feminino fixo, e o FAQ passou a falar com "profesionales habilitados" (corrige o "qualquer injetor" do PT, risco de linguagem para leigo). Back-translation dos blocos 3 e 7 sem perda técnica.

### GRAVE

**[2.1] Inconsistência interna · "libro digital" x "e-book"**
- O doc chama o produto de "libro digital" em 9 lugares (espelhando o "livro digital" do PT); a linha acrescentada pela decisão de autoridade usa "e-book".
- Trecho ES exato: `Este e-book ya suma +30 mil copias vendidas.`
- Correção: `Este libro digital ya suma +30 mil copias vendidas.`
- Atenção na busca e troca: a mesma frase existe, correta, nos docs 1, 3 e 4. Trocar só neste doc.

### PONTOS PARA ANÁLISE (sem achado)
- "Ahora le entrego un método claro y estructurado para que deje la improvisación…" (aqui) x "para que usted deje atrás la improvisación" (Copy Página). Ambos corretos; uniformizar é opcional.

---

## 3. FEA-ES | Página de ventas - corta - eBook de Ojeras · `1Vbpklmy46mTIQizp5eSsf1OKcVFQXA0dLnXFTY3-U-w`

```
REVISÃO · Página de ventas corta · 26/10/2026
Cobertura: completa. Original PT lido: «Página de vendas - curta - Ebook de Olheiras»
           (1ItoOl_sPDStNcfQ0_sqeBACPPpyvh-6pvPrV0NrIQ6o, 22.09.2025).

VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 83,7 %  (72 de 86 segmentos limpos)
                               15,49 achados por mil palavras (14 em 904)
                               4 GRAVE · 10 MENOR
  Questões ao autor: 1  (a mesma 1.Q2)
```

A página curta reaproveita blocos da longa e herda os mesmos achados. Trechos idênticos, então a mesma busca e troca resolve os dois docs.

### GRAVE
- **[3.1]** = [1.1] headline. Trecho ES exato: `Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y trabaje con seguridad, previsibilidad y resultados naturales y duraderos.` · Correção: `Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y trabaje con seguridad, previsibilidad y una técnica reproducible caso a caso.`
- **[3.2]** = [1.2] layering. Trecho ES exato: `Domine la técnica de layering (por capas) para resultados naturales y duraderos.` · Correção: `Domine la técnica de layering (por capas) para un depósito controlado del producto en cada plano.`
- **[3.3]** = [1.3c] complicações. Trecho ES exato: `Aprenda a seleccionar los productos más adecuados para ojeras y a evitar intercurrencias.` · Correção: `Aprenda a seleccionar los productos más adecuados para ojeras y a evitar complicaciones.`
- **[3.4]** = [1.4] pertuito. Trecho ES exato: `Descubra los puntos de acceso correctos (puntos de entrada).` · Correção: `Descubra los puntos de acceso correctos (pertuitos).`

### MENOR
- **[3.5]** = [1.5] Swelling Factor. Trecho ES exato: `Domine el concepto de Swelling Factor (SF) y su influencia en el resultado final.` · Correção: `Domine el concepto de Swelling Factor (SF), o factor de hinchazón, y su influencia en el resultado final.`
- **[3.6] Title Case (8 ocorrências):** as mesmas trocas da tabela [1.6], exceto `Sección de la Oferta` (não existe neste doc): `Introducción al Razonamiento Clínico para el Relleno de Ojeras`, `Anatomía de la Región Infraorbitaria`, `Reología: La Elección del Producto de Relleno Ideal`, `Técnica Avanzada de Relleno Tridimensional`, `Intercurrencias y Manejo de Complicaciones`, `+03 Bonos Exclusivos`, `Oferta Especial`, `FAQ (Preguntas Frecuentes)`.
- **[3.7]** = [1.7]. Trecho ES exato: `¿LE QUEDÓ ALGUNA DUDA?` · Correção: `¿Le quedó alguna duda?`

### QUESTÃO AO AUTOR
- **[3.Q1]** = [1.Q2] (frase "En 2019… cadáveres frescos" acrescentada no bloco de autoridade).

---

## 4. FEA-ES | Copy Página eBook Ojeras · `1_Af60zj_W4Cld_q9JDKi9-ispKT2HUTLqxtw43wHEqg`

```
REVISÃO · Copy Página eBook Ojeras · 26/10/2026
Cobertura: completa. Original PT lido: «Copy Página Ebook Olheiras»
           (1_WSLy1upcAcgZsiuLYQAPtbWT4ISQLXjhPeV52VN7xk).

VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 97,8 %  (89 de 91 segmentos limpos)
                               2,16 achados por mil palavras (2 em 927)
                               1 GRAVE · 1 MENOR
  Questões ao autor: 2
```

Remoção de "LG na Coreia" (linha vermelha 3) e reescrita de "não é uma técnica difícil" (linha vermelha 4) conferidas e corretas. Back-translation dos Bloques 3 e 5 fiel ao PT (alto G’, menor higroscopia, 3 a 4 pontos de entrada, camada ideal).

### GRAVE

**[4.1] Desvio de sentido · Bloque 6 generaliza um fabricante para "la industria"**
- Original PT: «…inclusive da indústria de preenchedores, como a LG na Coreia, que iniciou revisões reológicas…»
- Trecho ES exato: `Este enfoque viene despertando el interés incluso de la industria de productos de relleno, que ya inició revisiones reológicas para aumentar la precisión de las indicaciones clínicas de sus materiales.`
- Problema: no PT, quem iniciou revisões foi **um** fabricante. Ao tirar a marca, o ES passou a afirmar que "la industria" (o setor inteiro) iniciou revisões, uma afirmação maior que a do autor e sem fonte.
- Correção: `Este enfoque viene despertando el interés incluso de fabricantes de productos de relleno: uno de ellos ya inició revisiones reológicas para aumentar la precisión de las indicaciones clínicas de sus materiales.`

### MENOR

**[4.2] Apóstrofo reto em G’**
- Original PT: «Alto G’» (apóstrofo curvo).
- Trecho ES exato: `Alto G'`
- Problema: `01-voz-y-estilo.md` §3: apóstrofo sempre curvo, `G’`.
- Correção: `Alto G’`

### QUESTÃO AO AUTOR
- **[4.Q1]** Bloque 6: o doc já pede ao Dr. João confirmação de que a afirmação sobre a revisão reológica pode ser publicada sem citar fonte. Mantida.
- **[4.Q2]** = [1.Q2] (frase "En 2019… cadáveres frescos" no Bloque 11, inexistente no PT).

---

## 5. FEA-ES | Página de Upsell - Cpx · `1xSxWtG7pvjFxLJsA_c1xj5ev9pm_er25Uy3Kp2R5iKE`

```
REVISÃO · Página de Upsell CPX · 26/10/2026
Cobertura: completa. Original PT lido: «Página de UPSell - Cpx»
           (1YAfAftTA1GuzUHDHbmXFu_466iFwVUiJf5xtM4M0LuA, 22.09.2025).

VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 87,5 %  (21 de 24 segmentos limpos)
                               14,02 achados por mil palavras (3 em 214)
                               2 GRAVE · 1 MENOR
  Questões ao autor: 1
```

### GRAVE

**[5.1] Linha vermelha · urgência e status de compra simulados (2 segmentos)**
- Original PT: «Tarja vermelha: Atenção não feche ou atualize essa página.» · «Barra: Processando a sua compra 90%»
- Trechos ES exatos: `Franja roja: Atención, no cierre ni actualice esta página.` e `Barra: Procesando su compra 90 %`
- Problema: a regra registrada para as **páginas** manda remover urgência fabricada. A barra de 90 % simula um processamento que não existe e a franja vermelha cria pressão artificial. O próprio doc reconhece isso e deixou a alternativa como "pendiente de decisión"; enquanto as duas versões convivem, o designer pode montar a falsa.
- Correção: apagar as duas linhas e promover a alternativa já escrita, sem o rótulo de pendência:
  - `Franja roja: Atención, no cierre ni actualice esta página.` → `Su compra del e-book fue confirmada. Antes de cerrar esta página, vea esta oportunidad complementaria.`
  - `Barra: Procesando su compra 90 %` → (apagar)
  - Em seguida apagar a linha `Alternativa recomendada (pendiente de decisión): «Su compra del ebook fue confirmada. Antes de cerrar esta página, vea esta oportunidad complementaria.»`
- (Grafia "e-book" na correção alinhada com as páginas de vendas; ver P1.)

### MENOR
- **[5.2]** = [1.7]. Trecho ES exato: `¿LE QUEDÓ ALGUNA DUDA?` · Correção: `¿Le quedó alguna duda?`

### QUESTÃO AO AUTOR
- **[5.Q1] Vídeo de vendas do CPX e oferta no LATAM.** `Insertar el VIDEO de venta del CPX (el video que ya se usa en la página de ventas; confirmar versión en español).` Se o vídeo for o brasileiro, a página espanhola vai embutir vídeo em português (pela rubrica, ativo PT numa entrega ES). Já é pendência registrada do doc (junto com "confirmar se o upsell CPX será oferecido no funil LATAM"), por isso não entra como classe A; precisa estar resolvido antes de publicar.

---

## 6. FEA-ES | Página de gracias y encuesta - eBook Ojeras · `10Z-Grn-krA7ARoh8w3Tg1gYrErBmHnCDanhnbPHPAmU`

```
REVISÃO · Página de gracias y encuesta · 26/10/2026
Cobertura: PARCIAL. Não existe original PT: é copy escrita do zero em ES (declarado no
           próprio doc). Busca no Drive por "Obrigado" + "Olheiras" só achou páginas de
           outros produtos (Vitalício 2025, PLX). Rodadas: camada 1, camada 4 e linha
           vermelha. Camadas 2 e 3 sem objeto de comparação.

VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 97,6 %  (40 de 41 segmentos limpos)
                               1,55 achados por mil palavras (1 em 645)
                               0 GRAVE · 1 MENOR
  Questões ao autor: 1
```

Registro usted consistente, sem urgência, sem promessa, público habilitado na pergunta 1, área de membros com `/es/` (regra cumprida).

### MENOR

**[6.1] Saudação com duplo gênero**
- Trecho ES exato: `Bienvenido(a) al ebook Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI.`
- Problema: a [NUEVA] neutralizou o gênero via usted; aqui a manchete usa "(a)", que soa formulário. Nas opções da enquete (`Médico(a)` etc.) o duplo gênero é aceitável e fica.
- Correção: `Le damos la bienvenida al ebook Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI.`

### QUESTÃO AO AUTOR
- **[6.Q1] Faixas sobrepostas na pergunta 3.** `( ) De 1 a 3 años · ( ) De 3 a 5 años` (quem tem exatamente 3 anos cabe nas duas). Sugestão: `( ) De 1 a 3 años · ( ) Más de 3 y hasta 5 años · ( ) Más de 5 años`. Afeta a segmentação, não a tradução.

---

## Pontos transversais (não entram em índice de nenhum doc)

**P1 · "e-book" x "ebook" entre materiais.** Páginas de vendas (docs 1, 3, 4): "e-book". Upsell e Gracias: "ebook". O glossário (`00-nucleo.md` §7) diz "ebook". Dentro de cada doc o uso é coerente, por isso não contei como achado; mas o aluno vê as duas grafias no mesmo funil (vendas → upsell → gracias). Recomendo decidir uma e registrar em `90-decisiones.md`. Minha recomendação: **e-book** (grafia dominante nas páginas que vão ao ar, 30 ocorrências, e a mais usada no mercado hispano), trocando as 6 de Gracias/Upsell; ou manter "ebook" do glossário e trocar as ~30 das páginas. A primeira opção custa menos.

**T1 · Título do livro em Title Case.** `Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI` está em Title Case (norma ES pediria "Relleno tridimensional de ojeras: una guía completa con la metodología ARTI"). Como é nome de produto e precisa bater com a capa do PDF ES (`Relleno_Tridimensional_de_Ojeras_ES.pdf`), não marquei como achado. Questão ao autor: confirmar a grafia da capa e usar a mesma em todos os docs.

## Pontos para análise, ordenados por custo de não corrigir

1. **[5.1] Barra "Procesando su compra 90 %" no upsell.** Linha vermelha (urgência simulada) numa página que vai ao ar no momento de maior confiança do comprador.
2. **[1.1]/[3.1] e [1.2]/[3.2] "resultados naturales y duraderos".** Linha vermelha 1, está na headline das duas páginas de vendas (primeira frase lida).
3. **[4.1] "la industria… ya inició revisiones".** Afirmação factual ampliada sem fonte, numa página pública.
4. **[1.3]/[3.3] complicaciones x intercurrencias (4 segmentos).** Ou corrige, ou registra decisão; sem isso a dúvida volta em todo material.
5. **[1.4]/[3.4] pertuito.** Barato e mantém a ponte com o ebook.
6. **[2.1] "e-book" na [NUEVA]** e **P1** (grafia entre materiais).
7. **[1.6]/[3.6] Title Case (17 segmentos), [1.7]/[3.7]/[5.2] caixa alta, [1.5]/[3.5] glosa SF, [4.2] G’, [6.1] Bienvenido(a).** Editorial; é o que mais pesa no índice das páginas longa e curta, mas não tem risco.

## Propostas de glossário (para `90-decisiones.md`, não aplicadas)

| Item | Proposta |
|---|---|
| e-book / ebook na copy comercial | Registrar uma grafia única para todo o funil LATAM (ver P1). |
| complicações x intercorrências na copy comercial | Ou reafirmar a distinção do ebook (complicaciones ≠ intercurrencias), ou registrar exceção: "na copy comercial, intercurrencias cobre ambos". |
| Títulos de seção em páginas | Registrar: sentence case em H2/H3 de página; exceção só para nome de produto e de técnica com marca ("Técnica Tridimensional"). |
| Status de compra simulado (barra %, "no cierre esta página") | Acrescentar à regra "sem cronômetro nas páginas": também sem barra de progresso simulada nem franja de alerta. |

## Ajustes no auditor (`auditar.py`)

Todos os achados do script nesta rodada foram falsos positivos:

| Achado do script | Onde | Por que é falso positivo | Regra proposta |
|---|---|---|---|
| BLOQUEANTE "lusismo: ênclise" em `Revise` | [NUEVA], `Revise su correo electrónico` | É imperativo formal de *revisar* (usted), não ênclise. Verbos em -sar fazem imperativo em -se. | Excluir da regra de ênclise palavras em início de frase seguidas de possessivo/artigo, ou lista branca de imperativos em -se (`revise, ingrese, piense, use, pase, cause, precise`). |
| GRAVE "resíduo PT" `Olheira`/`Preenchi` | linhas de crédito de todos os docs (`de «Página de vendas - Ebook de Olheiras»`, nome do arquivo `Preenchimento Tridimensional de Olheiras_02_ebook2.pdf`) | É citação do título do original e nome de arquivo, que devem ficar em PT. | Ignorar texto entre `«…»` precedido de "de" na linha "Traducción al español…" e tokens com `_` ou extensão de arquivo (`\.pdf\b`). |
| GRAVE "falta ¿ de abertura" | [NUEVA], URL do Figma `...FEP---PUBLIC?node-id=0-1` | O `?` é da query string da URL. | Remover `https?://\S+` antes de checar `¿`. |
| MENOR "hífen como raya" | linha de crédito da corta (`Página de vendas - curta - Ebook de Olheiras`) | Hífen dentro do título PT citado. | Mesma exclusão de `«…»` acima. |

## Tabela resumo

| # | Doc | Original PT | Classe A | Índice B | Achados B (GRAVE/MENOR) | Densidade /mil | Questões | Veredito |
|---|---|---|---|---|---|---|---|---|
| 1 | Página de ventas | lido | 0 | 85,7 % (102/119) | 17 (6/11) | 13,72 | 2 | LIBERADO COM RESSALVAS |
| 2 | [NUEVA] Página de ventas | lido | 0 | 99,2 % (118/119) | 1 (1/0) | 0,75 | 0 | LIBERADO |
| 3 | Página corta | lido | 0 | 83,7 % (72/86) | 14 (4/10) | 15,49 | 1 | LIBERADO COM RESSALVAS |
| 4 | Copy Página eBook Ojeras | lido | 0 | 97,8 % (89/91) | 2 (1/1) | 2,16 | 2 | LIBERADO |
| 5 | Página de Upsell | lido | 0 | 87,5 % (21/24) | 3 (2/1) | 14,02 | 1 | LIBERADO COM RESSALVAS |
| 6 | Página de gracias | **não existe** (copy original ES), cobertura parcial | 0 | 97,6 % (40/41) | 1 (0/1) | 1,55 | 1 | LIBERADO |
| | **Total** | | **0** | | **38 (14/24)** | | **7** + 2 transversais | 3 LIBERADO · 3 COM RESSALVAS · 0 RETIDO |
