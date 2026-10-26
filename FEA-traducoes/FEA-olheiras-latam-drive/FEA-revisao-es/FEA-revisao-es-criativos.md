# FEA · Revisão ES das copies dos criativos · Ebook Olheiras LATAM

REVISÃO · Criativos, legendas e remarketing do Ebook Relleno de Ojeras (LATAM) · 26/10/2026
Revisor: skill fea-revision-es (leitura de par especialista). Nada foi editado no Drive.

**Cobertura**

| Doc ES | ID | Original PT usado | Cobertura |
|---|---|---|---|
| FEA-ES \| Creativos | 1aPENAjSDasC6RG8wcLg74dowKXJzpJwrRXSY5rWR5ME | Criativos - eBook Preenchimento de Olheiras (1Zmrby3PW4iobUoVviuunOZJjCSL3yTHG-gQ_Dux8Ws8) + copy v3 | Completa |
| FEA-ES \| Creativos 2 | 1gBY3ZkXgxrej8zyF-BwWPpVl2dxYvtgplK6p11Lewlc | Criativos - eBook Preenchimento de Olheiras 2 (1ze5LsHFmPXwcrs5E8gTYG3y2MFnCWucXs5RhBc_NxtM) + copy v3 | Completa |
| FEA-ES \| Leyendas | 1Y2j4EnGg4H9n74A947ghMHZ_FU-JiOlKkIEHCT2Vatw | Legenda I Criativos do eBook Olheiras (1PxsbyqQyibELlt9JYPT9WtnbuSUsI3t866cWhrBkRZQ) | **Parcial**: a seção Ventas tem original; a seção Remarketing é copy original LATAM, sem PT (revisada só em voz, linha vermelha e coerência com a página de vendas ES) |
| FEA-ES \| Remarketing | 1nN9XNZaK536cLA6CDjvqB0qZQMTBIiGfRHiS3q00kpg | Não existe (o Brasil não tem remarketing deste ebook) | **Parcial**: camadas 1 e 4 e checagem de claims contra `FEA-ES-pagina-ventas.html`; camadas 2 e 3 sem par PT |
| Copy dos criativos estáticos v3 (PT \| ES) | 1jiKpctRIlg3LQHS2coCPLWmEELrSoRK9Z5C-g-gGn6E | Coluna PT do próprio doc + `FEA-bilingue-PT-ES.tsv` | Completa (coluna ES) |
| Artes (scripts locais) | `fea_artes/criativos/*.py`, `FEA-copy-criativos-final.py`, `FEA-bilingue-PT-ES.tsv` | v3 | Conferência doc × arte por amostragem dirigida (preço, selo, número de autoridade, CTA, frases da linha vermelha) |

Decisões registradas tratadas como não-achado: US$19 de US$47, 60 %, upsell US$97, 30.000 alumnos, 9 países, 10.000 ml, +30 mil copias, marcadores PENDIENTE, usted, "48 horas", "SOLO HOY", "OFERTA LIMITADA", capa Allergan, "no es una técnica difícil", "Evitar tratar ojeras", "hidrofílico", "complicaciones" na legenda V3, depoimento em PT com legenda ES. Blocos "Notas para a equipe" (PT) não entram no índice.

**Camada 1 (auditor):** textos ES salvos em `/tmp/claude-0/-home-user-FEA/6500f297-8601-53d4-bc7c-33986b7f95c3/scratchpad/rev-criativos/` (`es1` a `es6`). `auditar.py` devolveu 0 achados e LIBERADO 100 % em todos, inclusive no `FEA-copy-criativos-final.py` cru, que ainda contém `R$` e `[PRECIO…]`. Os achados abaixo são todos das camadas 3 e 4 e da conferência doc × arte; ver AJUSTES NO AUDITOR.

**Camada 2 (segurança clínica):** sem divergência. Conferidos contra o PT: plano, profundidade, "zonas de riesgo", "cuándo NO rellenar", "dónde NO tocar" (negações preservadas), "Bolo, microbolo y retroinyección", "Producto muy hidrofílico", "Plano superficial", "Edema y efecto Tyndall". No remarketing (sem PT), os dados técnicos "3 a 4 puntos de entrada", "alto G’ y baja higroscopicidad" e "cadáveres frescos" batem com a página de vendas ES. Tratamento usted em 100 % dos segmentos; nenhum tú/vos. Nenhuma marca de produto, nenhum em-dash no ES.

---

## 1. FEA-ES | Creativos (1aPENAjSDasC6RG8wcLg74dowKXJzpJwrRXSY5rWR5ME)

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 96,7 %  (118 de 122 segmentos limpos)
                               3,39 achados por mil palavras (1.179 palavras)
                               2 GRAVE · 2 MENOR
  Questões ao autor: 0
```

── GRAVE ─────────────────────────────────────

[1.1] ADS 13 · emoji corrompido (regra de correção LATAM: nunca deixar "ð")
    Original PT:  «Caixinha: Faça uma pergunta ðð½» (já corrompido no original)
    Tradução ES:  «Cajita: Haga una pregunta ð»
    Problema:     resíduo de mojibake de emoji. A arte ES (`ads02.py`) não tem emoji, então o doc diverge da arte.
    Correção:     «Cajita: Haga una pregunta»

[1.2] ADS 09 · sentido alterado (camada 3)
    Original PT:  «Hoje, saber fazer o preenchimento dessa região é algo que diferencia a maior parte dos injetores de todo o mundo»
    Tradução ES:  «Hoy, saber rellenar esta región es lo que distingue a los inyectores en todo el mundo.»
    Back-translation: "saber preencher esta região é o que distingue os injetores no mundo todo" (todos os injetores; sumiu o contraste com "a maior parte").
    Problema:     a ideia de diferenciação frente à maioria se perdeu; a frase fica genérica e sem tensão. Mesmo texto na arte v3 Ads 04 (`ads04.py` l.19) e na v3.
    Correção:     «Hoy, saber rellenar esta región es lo que distingue a un inyector de la mayoría, en todo el mundo.»

── MENOR ─────────────────────────────────────

[1.3] Cabeçalho · lusismo de preço
    Tradução ES:  «Precio de la oferta: de US$47 por US$19 (60 % de descuento).»
    Problema:     "de X por Y" é estrutura portuguesa; no corpo os anúncios usam "De US$47 a solo US$19".
    Correção:     «Precio de la oferta: US$19 (antes US$47, 60 % de descuento).»

[1.4] ADS 15 · marcador truncado (fim do doc)
    Tradução ES:  «[IMAGEN: arte Ads 01 «60 % de descuento», usar la versión ES de la carpeta 2. ARTE»
    Problema:     colchete não fecha e falta o "S" de ARTES. Conferir no Drive se o truncamento é do doc ou da leitura do conector.
    Correção:     «[IMAGEN: arte Ads 01 «60 % de descuento», usar la versión ES de la carpeta 2. ARTES]»

---

## 2. FEA-ES | Creativos 2 (1gBY3ZkXgxrej8zyF-BwWPpVl2dxYvtgplK6p11Lewlc)

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 98,8 %  (167 de 169 segmentos limpos)
                               1,62 achados por mil palavras (1.236 palavras)
                               0 GRAVE · 2 MENOR
  Questões ao autor: 2 (Q1, Q4)
```

── MENOR ─────────────────────────────────────

[2.1] Cabeçalho · lusismo de preço (mesmo caso de 1.3)
    Tradução ES:  «Precio de la oferta: de US$47 por US$19 (60 % de descuento).»
    Correção:     «Precio de la oferta: US$19 (antes US$47, 60 % de descuento).»

[2.2] ADS 18 · redundância criada pela universalização
    Original PT:  «Nenhum outro lugar no Brasil ensina esse método.» (+ selo "O PRIMEIRO")
    Tradução ES:  «Un método exclusivo del Dr. João Pithon.»
    Problema:     a mesma arte já traz o selo «MÉTODO EXCLUSIVO DEL DR. JOÃO PITHON · +30 MIL COPIAS VENDIDAS»; a frase repete o selo palavra por palavra e perde o argumento de exclusividade. As regras de correção LATAM já indicam a forma universal "ningún otro programa enseña…".
    Correção:     «Ningún otro programa enseña este método.»

---

## 3. FEA-ES | Leyendas (1Y2j4EnGg4H9n74A947ghMHZ_FU-JiOlKkIEHCT2Vatw)

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 94,7 %  (36 de 38 segmentos limpos)
                               5,06 achados por mil palavras (395 palavras)
                               1 GRAVE · 1 MENOR
  Questões ao autor: 2 (Q2, Q3)
  Cobertura parcial: Remarketing sem original PT.
```

── GRAVE ─────────────────────────────────────

[3.1] Remarketing V1 · inconsistência interna do título do ebook
    Tradução ES:  «Usted ya visitó la página del ebook Relleno Tridimensional de Ojeras.»
    Problema:     em todos os criativos o título é «Relleno tridimensional de ojeras» (maiúscula só na primeira palavra, norma ES e padrão do material). Title Case aqui é decalque do PT. Mesmo achado em 4.1 e 4.2.
    Correção:     «Usted ya visitó la página del ebook Relleno tridimensional de ojeras.»

── MENOR ─────────────────────────────────────

[3.2] Ventas V2 · preposição calcada
    Original PT:  «O guia definitivo em Preenchimento de Olheiras»
    Tradução ES:  «La guía definitiva en relleno de ojeras»
    Problema:     "definitiva en" é calco de "definitivo em"; em espanhol a guia é "sobre" ou "de" um tema.
    Correção:     «La guía definitiva sobre relleno de ojeras»

---

## 4. FEA-ES | Remarketing (1nN9XNZaK536cLA6CDjvqB0qZQMTBIiGfRHiS3q00kpg)

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 85,4 %  (41 de 48 segmentos limpos)
                               11,24 achados por mil palavras (623 palavras)
                               2 GRAVE · 5 MENOR
  Questões ao autor: 2 (Q2, Q5)
  Cobertura parcial: copy original LATAM, sem PT.
```

── GRAVE ─────────────────────────────────────

[4.1] RMKT 01 · Leyenda · inconsistência interna do título
    Tradução ES:  «En el ebook Relleno Tridimensional de Ojeras, el Dr. João Pithon reúne el razonamiento que usa para prevenir esas intercurrencias:»
    Correção:     «En el ebook Relleno tridimensional de ojeras, el Dr. João Pithon reúne el razonamiento que usa para prevenir esas intercurrencias:»

[4.2] RMKT 03 · Leyenda · inconsistência interna do título
    Tradução ES:  «El ebook Relleno Tridimensional de Ojeras está organizado para consulta rápida:»
    Correção:     «El ebook Relleno tridimensional de ojeras está organizado para consulta rápida:»

── MENOR ─────────────────────────────────────

[4.3] RMKT 01, 02 e 03 · gênero de "arte" (3 ocorrências)
    Tradução ES:  «Texto de la arte:»
    Problema:     no singular, "arte" é masculino (el arte); "la arte" soa erro de nativo de português.
    Correção:     «Texto del arte:» (nas três ocorrências)

[4.4] RMKT 01 · Leyenda · sinal "+" em prosa
    Tradução ES:  «Un material de consulta que ya suma +30 mil copias vendidas, hoy por **US$19**.»
    Problema:     "+30 mil" é formato de selo; em frase corrida o espanhol escreve por extenso, e "suma +30" fica truncado.
    Correção:     «Un material de consulta que ya suma más de 30 mil copias vendidas, hoy por **US$19**.»

[4.5] RMKT 03 · Leyenda · sinal "+" em prosa
    Tradução ES:  «Ya son +30 mil copias vendidas, con 7 días de garantía.»
    Correção:     «Ya son más de 30 mil copias vendidas, con 7 días de garantía.»

Claims conferidos contra a página de vendas ES (sem achado): 3 a 4 puntos de entrada, alto G’ y menor higroscopicidad, estudo em cadáveres frescos, PDF com acesso imediato e de por vida, 7 días de garantía, 9 países.

---

## 5. Copy dos criativos estáticos v3 · coluna ES (1jiKpctRIlg3LQHS2coCPLWmEELrSoRK9Z5C-g-gGn6E)

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 99,1 %  (215 de 217 segmentos ES limpos)
                               0,98 achados por mil palavras (2.049 palavras)
                               1 GRAVE · 1 MENOR
  Questões ao autor: 0
```

── GRAVE ─────────────────────────────────────

[5.1] Ads 04 · sentido alterado (mesmo caso de 1.2)
    Tradução ES:  «Hoy, saber rellenar esta región es lo que distingue a los inyectores en todo el mundo.»
    Correção:     «Hoy, saber rellenar esta región es lo que distingue a un inyector de la mayoría, en todo el mundo.»
    Arte afetada: `fea_artes/criativos/ads04.py` l.19 (Feed e Story).

── MENOR ─────────────────────────────────────

[5.2] [FEED] ADS 18 · redundância com o selo (mesmo caso de 2.2)
    Tradução ES:  «Un método exclusivo del Dr. João Pithon.»
    Correção:     «Ningún otro programa enseña este método.»
    Arte afetada: `fea_jpg_ads18.py`.

---

## 6. Docs × artes × fontes locais (inconsistências)

Fora do índice (não são segmentos de doc), mas cada uma pode reintroduzir erro na próxima rodada de arte.

[6.1] GRAVE · fonte oficial das artes desatualizada
    `FEA-copy-criativos-final.py` (que `FEA-instrucoes-agentes.md` declara "copy oficial") ainda traz o estado de 05/10: valores em reais e marcador, por exemplo «De R$ 200,00 a solo R$ 97,00 [PRECIO EN MONEDA LOCAL: CONFIRMAR, el original dice R$ 200,00 tachado y R$ 97,00]», e no Ads 01 «76 % DE DESCUENTO PARA INYECTORES [DESCUENTO EN MONEDA LOCAL: CONFIRMAR, el original dice 76 %]». As artes saem certas porque leem `precos.json` (US$19 / US$47 / 60 %), mas qualquer agente que copiar texto do `.py` leva R$ para a arte.
    Correção: atualizar a coluna ES do `.py` para o texto da v3 (preço em US$, 60 %, sem marcadores).

[6.2] GRAVE · TSV com promessa de resultado (linha vermelha)
    `FEA-bilingue-PT-ES.tsv` ainda tem, no Ads 08 e no Ads 14, «…con la metodología ARTI y logre resultados naturales, seguros y duraderos.» (a v3 e as artes já trocaram por «trabaje con seguridad, previsibilidad y criterio anatómico»). O TSV também não tem as linhas do Ads 06 e do Ads 09.
    Correção: regerar o TSV a partir do `.py` atualizado.

[6.3] GRAVE · Banner de checkout ES ainda promete resultado (linha vermelha)
    A v3 afirma "Mesma troca aplicada nos docs FEA-ES de criativos, checkout e legenda", mas a arte `apoio_banner_checkout.py` (l.27 e 28) escreve «metodología ARTI y logre resultados naturales, seguros y duraderos.».
    Correção: «metodología ARTI y trabaje con seguridad, previsibilidad y criterio anatómico.» e recompor a arte. (Peça de checkout, fora dos 5 docs, registrada porque contradiz a v3.)

[6.4] ADS 13 do doc 1 com "ð" e arte sem emoji: ver 1.1.

[6.5] Pendência possivelmente vencida na v3: "Artes Ads 06 e 09: recompor em ES com US$19". As artes existem localmente (`FEA-artes-ES/FEA-Ads 06 - PTO-LATAM - Feed.png` e `…Ads 09…`, 09/10, depois do `precos.json` com US$19). Confirmar se subiram para LATAM ESTÁTICOS e, se sim, baixar a pendência.

[6.6] Coerentes (sem achado): preço e percentual nas artes (`precos.json`), selo «MÉTODO EXCLUSIVO DEL» + «DR. JOÃO PITHON» + «COPIAS» sem acento, «Después de formar a más de 30.000 alumnos…» (`ads37.py`), «con más de 30 mil copias vendidas» (`ads40.py`), CTAs «Más información», legenda «Testimonio original en portugués» nos prints.

---

## PONTOS PARA ANÁLISE (ordenados por custo de não corrigir)

1. **6.1 e 6.2: fontes locais desatualizadas.** É o item mais caro: o `.py` é a referência dos agentes de arte, e uma regeneração a partir dele (ou do TSV) recoloca R$, "76 %" e a promessa de resultado em várias artes de uma vez.
2. **6.3: banner de checkout com promessa de resultado.** Linha vermelha FEA, peça visível no momento da compra, e a v3 diz que já estava corrigido.
3. **1.2 / 5.1: "distingue a los inyectores".** Aparece no doc 1, na v3 e na arte Ads 04 (Feed e Story): três lugares para trocar, mais a arte para recompor.
4. **3.1, 4.1 e 4.2: título do ebook em Title Case** em três legendas de remarketing. É a inconsistência que o leitor vê, porque o título aparece em quase todas as peças.
5. **1.1: emoji corrompido** no doc 1 (correção de 1 minuto).
6. **2.2 / 5.2: ADS 18 repete o selo.** Exige recompor uma arte jpg.
7. **Menores de texto:** 1.3, 2.1, 3.2, 4.3 a 4.5, 1.4.

## QUESTÃO AO AUTOR

[Q1] Creativos 2, ADS 12 e ADS 03 · critério de CTA. O doc PT do ADS 12 termina com «Toque em Saiba Mais e garanta o seu.», e o ES não tem CTA (segue a arte v3, que também não tem). No ADS 03 acontece o inverso: a arte não tem CTA e o ES manteve «Toque en Más información y asegure el suyo.». Decidir se o doc ES espelha o doc PT ou a arte. Se a arte do ADS 12 tiver CTA, a ausência no ES é omissão de trecho.

[Q2] Leyendas (Remarketing V2) e Remarketing (RMKT 02) · alcance do número de autoridade. «Más de 30.000 alumnos en 9 países ya aprendieron con este método.» atribui ao método de olheiras o total de alunos da FEA. A página de vendas ES diz «Ya he formado a más de 30.000 alumnos con estas técnicas», então há base, mas o próprio Ads 40 foi corrigido por confundir cópias com profissionais. Confirmar com o Dr. João se a frase se sustenta ou se fica «Más de 30.000 alumnos en 9 países ya se formaron con el Dr. João Pithon.».

[Q3] Leyendas, Remarketing V1 · «Usted ya visitó la página del ebook…». Dizer ao usuário que se sabe que ele visitou a página pode pesar na revisão de anúncio do Meta e soa invasivo. Alternativa neutra: «Si usted ya conoce el ebook Relleno tridimensional de ojeras y todavía tiene dudas, vale la pena saber de dónde viene este método.».

[Q4] Creativos 2, ADS 11 e 16 · «videoclases». As notas do próprio doc mandam retirar o item da arte até existir versão ES das videoaulas, mas o corpo do doc e as artes (`fea_jpg_ads11.py`, `fea_jpg_ads16.py`) mantêm «videoclases explicativas». Decidir: retirar ou manter (a página de vendas ES também promete videoclases).

[Q5] Notas internas citam pessoas fora do mapa de equipe do CLAUDE.md (Leo Quirino na arte do remarketing, Matheus van der Ham na legenda). Confirmar antes de atribuir tarefa.

Observação fora de escopo: o pop-up Hotmart ES (`apoio_popup_hotmart.py`) tem «ESTA OFERTA ESPECIAL ES POR TIEMPO LIMITADO» e «¡Finalice su inscripción y asegure su descuento mientras aún hay tiempo!». A regra LATAM manda remover "por tiempo limitado" fabricado nas páginas; confirmar se vale para o checkout.

## PROPOSTAS DE GLOSSÁRIO (para `90-decisiones.md`)

| Item | Proposta |
|---|---|
| Título do ebook em ES | Forma única «Relleno tridimensional de ojeras: una guía completa con la metodología ARTI»; nunca Title Case |
| "+30 mil copias vendidas" | Formato de selo e headline; em prosa, «más de 30 mil copias vendidas» |
| Linha de preço em texto corrido | «US$19 (antes US$47)»; em arte, «De US$47 a solo US$19». Evitar «de US$47 por US$19» |
| "arte" (peça gráfica) | Masculino: «el arte», «texto del arte» |
| Aspas em legenda de depoimento | Hoje: arte e doc 2 usam «…», legendas usam “…” (decisão do catálogo, motivada pela fonte dos PDFs). Fixar uma só para anúncios |
| Universalização de "Nenhum outro lugar no Brasil" | «Ningún otro programa enseña este método.» (já sugerido nas regras LATAM), sem repetir o selo |

## AJUSTES NO AUDITOR (`fea-traduccion-es/scripts/auditar.py`)

O auditor deu 100 % em todos os textos, inclusive no `.py` com R$ e marcadores. Nenhum falso positivo; o problema são lacunas de regra:

| Regra proposta | Severidade | Regex |
|---|---|---|
| Mojibake de emoji ou acento | GRAVE | `ð\|Ã[\x80-\xbf]\|â€` |
| Moeda brasileira em entrega LATAM | GRAVE | `R\$\s?\d` |
| Marcador de preço pendente em texto final | GRAVE | `\[(PRECIO\|DESCUENTO)[^\]]*\]` |
| "la arte" | MENOR | `\bla arte\b` |
| Preço "de X por Y" | MENOR | `\bde\s+US\$\s?\d+\s+por\b` |
| Título do ebook em Title Case | GRAVE | `Relleno Tridimensional de Ojeras` |

Registrar também que o auditor conta como segmento toda linha com mais de 2 caracteres, inclusive rótulos de direção de arte ("Foto del Dr. João", "Mockup del ebook"); isso infla o denominador em cerca de 15 % nos docs de criativos.

---

## TABELA RESUMO

| Doc | Classe A | Índice B (limpos/total) | GRAVE | MENOR | Questões | Veredito |
|---|---|---|---|---|---|---|
| FEA-ES \| Creativos | 0 | 96,7 % (118/122) | 2 | 2 | 0 | LIBERADO |
| FEA-ES \| Creativos 2 | 0 | 98,8 % (167/169) | 0 | 2 | 2 | LIBERADO |
| FEA-ES \| Leyendas | 0 | 94,7 % (36/38) | 1 | 1 | 2 | LIBERADO COM RESSALVAS (cobertura parcial) |
| FEA-ES \| Remarketing | 0 | 85,4 % (41/48) | 2 | 5 | 2 | LIBERADO COM RESSALVAS (cobertura parcial) |
| Copy v3 (coluna ES) | 0 | 99,1 % (215/217) | 1 | 1 | 0 | LIBERADO |
| Docs × artes × fontes locais | 0 | n/a | 3 | 0 | 0 | Corrigir antes de regerar artes |
| **Total** | **0** | | **9** | **11** | **5 únicas** | |
