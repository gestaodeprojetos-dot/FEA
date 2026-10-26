# FEA · Revisão ES das copies do Ebook Olheiras LATAM

REVISÃO: copies ES do funil do ebook *Relleno tridimensional de ojeras* (7 Google Docs `FEA-ES | ...`) · 26/10/2026
Revisor: skill `fea-revision-es` (leitura de par especialista). Nenhum doc do Drive foi editado.

## Cobertura e método

| Doc ES | ID | Original PT usado | Cobertura |
|---|---|---|---|
| Comunicaciones | 1ZZA7C4v... | não existe (copy original LATAM, escrita do zero em 20/10) | **parcial**: camadas 1, 2 e 4; sem back-translation contra PT |
| Encuesta y regalo | 1nFYnMcp... | não existe (copy original LATAM) | **parcial**: camadas 1, 2 e 4 |
| Onboarding + Grupo lleno | 1wcQnNSk... | Listboss API BR (A06) 1KuVKVJy... · Descrição do grupo I Ebook Olheiras 18GzP8H_... | seções 1 a 3 completas; seções 4 e 5 sem original (parcial) |
| Listboss API | 1_2qjfrz... | Listboss API - ebook Olheiras 1KuVKVJy... | completa |
| Listboss Email | 1_lBObGj... | Listboss Email - ebook Olheiras 1mben7Qx... | completa |
| Checkout personalizado | 1PEiblJv... | Checkout Personalizado I eBook 1u_0_vDA... | completa |
| Low tickets | 1shuG_io... | Descrição do grupo I Low tickets 1P7PTHJd... | completa |

Busca no Drive por "Comunicações" e "Pesquisa/presente" do Ebook Olheiras BR não retornou doc correspondente (só o banco de dados de pesquisa de leads e docs de outros produtos), o que confirma as notas internas: Comunicaciones, Encuesta e as seções 4 e 5 do Onboarding não têm original PT. Nessas peças a revisão julga voz, consistência, linha vermelha e fatos, não fidelidade.

Decisões registradas tratadas como **não achado**: US$19 de US$47, 60 %, upsell US$97 "Curso de Relleno Express", 30.000 alumnos, 9 países, 10.000 ml, +30 mil copias, marcadores `[... PENDIENTE]` / `[... A CONFIRMAR]`, tags `[OLHEIRAS-LATAM]`, padrão de e-mail ("Hola, aquí el Dr. João Pithon." / `>> ACCIÓN <<` / "Un abrazo,"), usted, remoção de Pix/boleto e da urgência sem prazo real, remoção de `%FIRSTNAME%` em favor da abertura padrão. Bloco "Notas para a equipe" não revisado como copy.

**Alerta de método (importante para as próximas revisões):** `read_file_content` do conector Drive mostra emojis de 4 bytes como `ð` e corta os últimos caracteres de docs curtos (Listboss API, Listboss Email, Checkout, Low tickets pareciam truncados e com emoji corrompido). A exportação binária (`download_file_content`) confirma que os 4 docs estão **completos** e com emojis corretos (👇 📌 🔒 📩 🚫 ‼️). Portanto: **zero emoji corrompido e zero truncamento nos docs reais.** Toda revisão de doc ES deve conferir pela exportação antes de apontar corrupção.

Textos ES auditados (corpo, sem notas internas) em `/tmp/claude-0/-home-user-FEA/6500f297-8601-53d4-bc7c-33986b7f95c3/scratchpad/rev-copies/0[1-7]-*.txt`.

### Camada 1 (auditor) · resultado bruto e falsos positivos

| Doc | Veredito do script | Achados | Reais |
|---|---|---|---|
| Comunicaciones | LIBERADO 97,6 % | 2 GRAVE | 0 (2 FP "el mismo") |
| Encuesta | COM RESSALVAS 88,5 % | 6 GRAVE | 0 (6 FP tag OLHEIRAS) |
| Onboarding | COM RESSALVAS 92,6 % | 4 GRAVE | 0 (3 FP tag, 1 FP "los mismos") |
| Listboss API | RETIDO 62,0 % (exit 1) | 19 GRAVE | 0 (18 FP tag, 1 FP "la misma") |
| Listboss Email | RETIDO 75,6 % (exit 1) | 19 GRAVE | 0 (18 FP tag, 1 FP "la misma") |
| Checkout | LIBERADO 100 % | 0 | 0 |
| Low tickets | LIBERADO 100 % | 0 | 0 |

Os 69 achados do script são todos falsos positivos (regras e ajuste propostos no fim). Os vereditos abaixo usam o índice recalculado pelo revisor.

### Linha vermelha FEA (varredura nos 7 docs)

Em-dash (U+2014): 0 · "pra": 0 · tú/vos/vosotros: 0 (usted consistente em todo o corpo) · emojis corrompidos: 0 (ver alerta de método) · marca de AH ou toxina: 0 · promessa estética garantida: 0 · tom motivacional: 0 · urgência fabricada: 0 nas copies (o pop-up "SU DESCUENTO DE 60 % ESTÁ RESERVADO" é neutro, sem prazo). Pontos de atenção de compliance que não são erro de tradução estão em QUESTÃO AO AUTOR.

---

## 1. FEA-ES | Comunicaciones · eBook Ojeras (1ZZA7C4vrGas5rKw5dP15pkTfdSNx1xeIRPj6uqJ5QwE)

Cobertura: parcial (sem original PT; copy original LATAM).

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 90,4 %  (75 de 83 segmentos limpos)
                               7,14 achados por mil palavras (1.121 palavras)
                               5 GRAVE · 3 MENOR
  Questões ao autor: 4
```

**Classe A:** nenhum achado. Números conferidos: 10.000 ml, 30.000 alumnos, 9 países, +30 mil copias, US$97 (decisões); "3 a 4 puntos de entrada" bate com a página de ventas ES ("entre 3 y 4 puntos de entrada"); "3 casos clínicos" bate com o ebook ES ("+ 3 casos clínicos").

**Pontos para análise (ordem: custo de não corrigir)**

[C1] GRAVE · inconsistência interna: título do ebook em Title Case (2 segmentos)
- Trecho ES (WhatsApp C1, título em negrito): «Bienvenido(a) al grupo de alumnos del ebook Relleno Tridimensional de Ojeras»
- Trecho ES (e-mail C1): «Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI»
- Problema: o título canônico do ebook ES (miolo traduzido, Listboss API e Listboss Email) é em minúscula a partir da 2ª palavra, que é a norma RAE para título de obra. O aluno recebe o mesmo título grafado de dois jeitos no mesmo dia (e-mail Listboss + e-mail Comunicación 1).
- Correção: «Bienvenido(a) al grupo de alumnos del ebook Relleno tridimensional de ojeras» · «Relleno tridimensional de ojeras: una guía completa con la metodología ARTI»

[C2] GRAVE · inconsistência interna: "e-mail" no corpo, "correo" no restante do funil (2 segmentos)
- Trecho ES (e-mail C1): «basta con responder este e-mail o escribir a»
- Trecho ES (e-mail C3): «Si tiene dudas antes de decidir, responda este e-mail.»
- Problema: os 4 e-mails do Listboss usam "correo" ("Basta con responder este correo", "puede responder este correo"). Mesmo leitor, mesma caixa de entrada, dois termos.
- Correção: «basta con responder este correo o escribir a» · «Si tiene dudas antes de decidir, responda este correo.»

[C3] GRAVE · terminologia fora da decisão registrada (1 segmento)
- Trecho ES (e-mail C1): «Intercurrencias y manejo de complicaciones»
- Problema: `90-decisiones.md` fixa "intercurrencias" e registra "complicaciones" como termo distinto do autor. A linha mistura os dois para o mesmo capítulo e soa redundante.
- Correção: «Intercurrencias y su manejo»

[C4] MENOR · voz: elipse que soa traduzida (1 segmento)
- Trecho ES (WhatsApp C2): «¿Su planificación de ojeras empieza en la jeringa o en la anamnesis?»
- Problema: "planificación de ojeras" planeja a olheira, não o procedimento.
- Correção: «¿Su planificación del relleno de ojeras empieza en la jeringa o en la anamnesis?»

[C5] MENOR · voz: "Desde que" com valor causal ambíguo (1 segmento)
- Trecho ES (e-mail C3): «Desde que usted recibió el ebook, quiero compartir algo que escucho con frecuencia de nuestros alumnos:»
- Problema: em ES "desde que" lê-se como marco temporal ("desde o momento em que"), o que não casa com "quiero compartir".
- Correção: «Ahora que usted ya tiene el ebook, quiero compartir algo que escucho con frecuencia de nuestros alumnos:»

[C6] MENOR · padrão de assinatura (1 segmento)
- Trecho ES (e-mail C3): «Nos vemos adentro.»
- Problema: a regra das copies LATAM fixa "Un abrazo," antes de "Dr. João Pithon"; os outros 2 e-mails da sequência usam. Além disso, "nos vemos adentro" pressupõe compra de quem ainda está decidindo o upsell.
- Correção: «Un abrazo,»

Não contado (rótulo interno): «PREENCABEZADO» aqui vs «ENCABEZADO» no Listboss Email para o mesmo campo. Uniformizar o rótulo (sugestão: "PREENCABEZADO", que é o termo do campo de pré-visualização) para não confundir quem configura.

---

## 2. FEA-ES | Mensaje con encuesta y regalo + API de encuesta (1nFYnMcpU_sPyz1mlCVRZL_LgRyhxGA0n1rTbu-9xFYM)

Cobertura: parcial (sem original PT; copy original LATAM).

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 92,3 %  (48 de 52 segmentos limpos)
                               5,35 achados por mil palavras (747 palavras)
                               4 GRAVE · 0 MENOR
  Questões ao autor: 1
```

**Classe A:** nenhum achado. Usted consistente; nenhuma promessa; formulário restrito a profissionais habilitados (pergunta 1), alinhado à linha vermelha 5.

**Pontos para análise**

[E1] GRAVE · inconsistência operacional: separador do nome de evento diferente do Listboss (3 segmentos)
- Trecho ES: «EVENTO: [OLHEIRAS-LATAM] Listboss – Encuesta»
- Trecho ES: «EVENTO: [OLHEIRAS-LATAM] Listboss – Recordatorio encuesta»
- Trecho ES: «EVENTO: [OLHEIRAS-LATAM] Listboss – Regalo»
- Problema: Listboss API e Listboss Email nomeiam todos os eventos, listas e tags com « · » (ponto médio): «[OLHEIRAS-LATAM] Listboss · Compra aprobada». Aqui o separador é «–» (meia-risca). Nome de evento e de tag precisa ser idêntico byte a byte na ferramenta; quem configurar copiando dos dois docs cria eventos duplicados.
- Correção: «EVENTO: [OLHEIRAS-LATAM] Listboss · Encuesta» · «EVENTO: [OLHEIRAS-LATAM] Listboss · Recordatorio encuesta» · «EVENTO: [OLHEIRAS-LATAM] Listboss · Regalo»

[E2] GRAVE · inconsistência interna: título do ebook em Title Case (1 segmento)
- Trecho ES (mensagem 2): «Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI»
- Correção: «Relleno tridimensional de ojeras: una guía completa con la metodología ARTI»

---

## 3. FEA-ES | Onboarding API + Grupo lleno (1wcQnNSkr9F6wVRyQKG4Fu4EO2qh8Qaxy8-DmVVOJSoI)

Cobertura: seções 1 a 3 contra PT (A06 e Descrição do grupo I Ebook Olheiras); seções 4 e 5 sem original.

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 81,5 %  (44 de 54 segmentos limpos)
                               17,67 achados por mil palavras (566 palavras)
                               9 GRAVE · 1 MENOR
  Questões ao autor: 0
```

**Classe A:** nenhum achado. Seções 1 a 3 fiéis ao PT: os 2 passos, o aviso de privado, a denúncia no Instagram e o link da área de membros (com `/es/`) estão todos presentes. Atenção: o índice está a 1,5 ponto do piso de retenção (80 %); os itens O1 e O2 são busca e troca e levam o doc acima de 95 %.

**Pontos para análise**

[O1] GRAVE · inconsistência interna: título do ebook em Title Case (5 segmentos, o mais caro do lote)
- Trecho ES (seção 1): «Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI»
- Trecho ES (seção 2, nome do grupo): «Ebook Relleno Tridimensional de Ojeras | Dr. João Pithon»
- Trecho ES (seção 3): «¡Bienvenido(a) a la Comunidad de Alumnos del ebook Relleno Tridimensional de Ojeras!»
- Trecho ES (seção 4): «Bienvenido(a) al grupo de alumnos del ebook Relleno Tridimensional de Ojeras»
- Trecho ES (seção 5, versão grupo): «abrimos un nuevo grupo exclusivo del ebook Relleno Tridimensional de Ojeras.»
- Correção: trocar, nos 5 trechos, «Relleno Tridimensional de Ojeras» por «Relleno tridimensional de ojeras» e «Una Guía Completa con la Metodología ARTI» por «una guía completa con la metodología ARTI». Nome do grupo: «Ebook Relleno tridimensional de ojeras | Dr. João Pithon».

[O2] GRAVE · inconsistência operacional: evento e lista com outro número e outro separador (2 segmentos)
- Trecho ES: «EVENTO: A06 · [OLHEIRAS-LATAM] Listboss – Compra aprobada»
- Trecho ES: «LISTA: [OLHEIRAS-LATAM] Listboss – Compra aprobada»
- Problema: o Listboss API ES renumerou os eventos (Pix e boleto removidos) e a compra aprovada é **A02**, com separador « · ». Aqui continua A06 (numeração BR) e com «–». Dois docs configurando o mesmo gatilho com nomes diferentes.
- Correção: «EVENTO: A02 · [OLHEIRAS-LATAM] Listboss · Compra aprobada» · «LISTA: [OLHEIRAS-LATAM] Listboss · Compra aprobada»

[O3] GRAVE · inconsistência interna: duas redações para a mesma mensagem automática (2 segmentos)
- Trecho ES (seção 1): «Para comenzar, solo faltan 2 pasos:»
- Trecho ES (seção 1): «donde recibirá actualizaciones, contenidos e información importante.»
- Problema: a seção 1 é a mesma mensagem do evento A02 do Listboss API, mas com texto diferente («Faltan solo 2 pasos para que comience:» / «donde recibirá avisos, contenidos e información importante.», e ✅ no fim da confirmação). A equipe IAutomate não tem como saber qual vale.
- Correção: alinhar ao Listboss API (doc-fonte do evento): «Faltan solo 2 pasos para que comience:» · «donde recibirá avisos, contenidos e información importante.» (ou declarar nas notas qual dos dois docs é o canônico).

[O4] MENOR · inconsistência de emoji entre descrições de grupo (1 segmento)
- Trecho ES (seção 3): «⛔ Está prohibido contactar a los miembros del grupo por mensaje privado.»
- Problema: as notas dizem que o emoji do original estava corrompido; a exportação do PT mostra que era 🚫 (o `ð«` é artefato do leitor do conector). A descrição Low tickets ES usa 🚫 na mesma frase.
- Correção: «🚫 Está prohibido contactar a los miembros del grupo por mensaje privado.»

---

## 4. FEA-ES | Listboss API · eBook Ojeras (1_2qjfrzOjOdkVt5iCVV50rZEGAawXcflJZ2wFfGfOhM)

Cobertura: completa (PT: Listboss API - ebook Olheiras).

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 100,0 %  (50 de 50 segmentos limpos)
                               0,00 achados por mil palavras (432 palavras)
                               0 GRAVE · 0 MENOR
  Questões ao autor: 1
```

**Classe A:** nenhum achado. Os 4 eventos mantidos (carrinho, compra aprovada, cartão recusado, reembolso) correspondem a A05 a A08 do PT, sem omissão; a remoção de A01 a A04 (Pix/boleto) e da alternativa "Pix ou boleto" no cartão recusado é decisão registrada. Doc completo e com 👇 corretos na exportação.

**Pontos para análise:** nenhum achado de classe B. Os 19 apontamentos do auditor são falsos positivos (18 pela tag `[OLHEIRAS-LATAM]`, 1 por «con la misma tarjeta», uso adjetival correto). Este doc é a referência de nomes de evento (« · ») que Encuesta e Onboarding devem seguir.

---

## 5. FEA-ES | Listboss Email · eBook Ojeras (1_lBObGj1I0AFTjgiqnyaHXxJ0z2F5yGMwEqyMkYgtco)

Cobertura: completa (PT: Listboss Email - ebook Olheiras).

```
VEREDITO: LIBERADO
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 98,7 %  (77 de 78 segmentos limpos)
                               1,53 achados por mil palavras (652 palavras)
                               0 GRAVE · 1 MENOR
  Questões ao autor: 0 (a duplicidade do marcador de WhatsApp no e-mail 4 já está nas notas)
```

**Classe A:** nenhum achado. E-mails 5 a 8 do PT cobertos; remoção da frase "por tiempo limitado" e dos e-mails de Pix/boleto é decisão registrada. Doc completo e com 📌 corretos na exportação.

**Pontos para análise**

[L1] MENOR · ortotipografia herdada do PT (1 segmento)
- Trecho ES: «ENVÍO: 05 minutos después de ingresar en la lista»
- Problema: zero à esquerda em cardinal não é usual em ES (no Listboss API está «5 minutos»).
- Correção: «ENVÍO: 5 minutos después de ingresar en la lista»

Os 19 apontamentos do auditor são falsos positivos (18 pela tag, 1 por «con la misma tarjeta»).

---

## 6. FEA-ES | Checkout personalizado I e-Book (1PEiblJvEh754uu8sOm71kG9EcmytGfHWRijN8iAmTIQ)

Cobertura: completa (PT: Checkout Personalizado I eBook).

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 86,7 %  (13 de 15 segmentos limpos)
                               20,83 achados por mil palavras (144 palavras)
                               2 GRAVE · 1 MENOR
  Questões ao autor: 1
```

**Classe A:** nenhum achado. Headline reescrita sem promessa estética e pop-up sem "por tiempo limitado" são decisões registradas e estão corretas frente à linha vermelha.

**Pontos para análise**

[K1] GRAVE · lusismo na ancoragem de preço (2 segmentos, área de maior conversão)
- Trecho ES (checkout): «De US$47 por US$19 (60 % de descuento)»
- Trecho ES (pop-up): «de US$47 por US$19.»
- Problema: "de X por Y" é a construção brasileira de preço riscado. Em ES latino-americano o leitor lê "por" como multiplicação ou troca; o uso nativo é "antes/ahora" ou "de X a Y".
- Correção: «Antes US$47, ahora US$19 (60 % de descuento)» · «por US$19 (antes US$47).»

[K2] MENOR · termo comercial calcado (mesmo segmento do pop-up, não recontado no índice)
- Trecho ES: «Finalice su inscripción y asegure su ebook»
- Problema: "inscripción" (calco de "inscrição") é para curso ou evento; para ebook o natural é "compra".
- Correção: «Finalice su compra y asegure su ebook»

Frase final do pop-up corrigida inteira, juntando K1 e K2: «Finalice su compra y asegure su ebook por US$19 (antes US$47).»

---

## 7. FEA-ES | Descripción del grupo I Low tickets (1shuG_ioT7pMBeJrys-SBagkPURePnL6bSp6ndfTqhwg)

Cobertura: completa (PT: Descrição do grupo I Low tickets).

```
VEREDITO: LIBERADO COM RESSALVAS
  Classe A (barreira clínica): 0
  Classe B (índice editorial): 93,3 %  (14 de 15 segmentos limpos)
                               5,99 achados por mil palavras (167 palavras)
                               1 GRAVE · 0 MENOR
  Questões ao autor: 0
```

**Classe A:** nenhum achado. Texto completo até «en la armonización facial.» na exportação; emojis 🔒 📩 🚫 ‼️ corretos.

**Pontos para análise**

[T1] GRAVE · resíduo PT (1 segmento)
- Trecho ES: «verifique si es ADM del grupo y, si no lo es,»
- Problema: "ADM" é abreviação brasileira de grupo de WhatsApp; em ES não é usual, e a descrição do grupo do ebook ES já usa "administrador".
- Correção: «verifique si es administrador del grupo y, si no lo es,»

---

## QUESTÃO AO AUTOR (não afeta veredito)

[Q1] Comunicaciones C3 · citação de aluno sem fonte. «Muchos alumnos del ebook me escriben con la misma pregunta: “Doctor, entendí el razonamiento. ¿Dónde puedo ver la ejecución?”» e «“Entendí la anatomía y la reología. Me falta ver la técnica ejecutada para aplicarla con confianza”». O ebook LATAM está estreando, então ainda não há alunos hispanohablantes escrevendo. Fala entre aspas atribuída a aluno precisa de fonte real (regra "nunca inventar fato"). Opções: trocar por pergunta retórica («Después de entender el razonamiento, la pregunta natural es: ¿dónde puedo ver la ejecución?») ou usar depoimento real do BR rotulado "Testimonio original en portugués".

[Q2] Comunicaciones C3 · claim absoluto. «validé más de 10.000 ml aplicados sin intercurrencias isquémicas» vem da página de ventas ES, então não é invenção da copy. Mesmo assim é afirmação clínica absoluta numa comunicação de venda; confirmar com a equipe médica (Francine Almeida) se o enunciado está documentado e aprovado para uso em ES.

[Q3] Comunicaciones C3 · «con 7 días de garantía» e o bono «Relleno Full Face guiado por ultrasonido en vivo». O bono confere com a página de upsell ES; a garantia de 7 dias não aparece em nenhuma página ES do repositório. Confirmar a política de garantia do upsell LATAM antes de publicar.

[Q4] Comunicaciones C2 · «es la clase más vista por nuestros alumnos». O dado é da base BR (Anamnese). Se a aula ES ainda é marcador pendente, a frase atribui à versão ES um dado de audiência da versão PT. Sugestão neutra: «la clase más vista de toda nuestra base de alumnos».

[Q5] Encuesta · pergunta 3 com faixas sobrepostas: «De 1 a 3 años · De 3 a 5 años» (3 anos cai em duas opções; idem 1 ano com «Menos de 1 año»). Sugestão: «Menos de 1 año · De 1 a 2 años · De 3 a 5 años · Más de 5 años». Decisão de quem vai ler a pesquisa.

[Q6] Listboss API A04 · o PT rotula o contato do reembolso como "Contato do comercial" (retenção), e o ES rotula «Contacto de soporte». Definir qual time atende reembolso LATAM; se for o comercial, separar os marcadores (a nota do Listboss Email já prevê isso).

[Q7] Checkout · caixa alta integral no pop-up («SU DESCUENTO DE 60 % ESTÁ RESERVADO») e «La GUÍA DEFINITIVA» espelham o PT, mas caixa alta integral em headline está na lista de anti-padrões FEA. Decidir se o LATAM mantém (fidelidade ao layout BR) ou passa para «Su descuento de 60 % está reservado».

## PROPOSTAS DE GLOSSÁRIO (90-decisiones.md)

| Item | Proposta |
|---|---|
| Título do ebook ES | Canônico: «Relleno tridimensional de ojeras: una guía completa con la metodología ARTI» (norma RAE para título de obra). Proibido Title Case em copy e nome de grupo. |
| Canal | «correo» no corpo das mensagens; "e-mail" só em rótulo interno. |
| Nome de evento/lista/tag Listboss | Separador « · » e numeração ES (A01 a A04). Nunca «–» nem numeração BR (A05 a A08). |
| Preço riscado | «Antes US$47, ahora US$19» ou «por US$19 (antes US$47)». Nunca «de US$47 por US$19». |
| ADM (WhatsApp) | «administrador». |
| inscrição (compra de ebook) | «compra» (reservar «inscripción» para curso, imersão e evento). |
| Rótulo de pré-visualização de e-mail | «PREENCABEZADO» em todos os docs. |
| Emoji de proibição em descrição de grupo | 🚫 (igual ao BR). |

## AJUSTES NO AUDITOR (auditar.py)

1. **Tag de automação.** A regra `\bolheira` dispara em `[OLHEIRAS-LATAM]` (66 dos 69 falsos positivos desta rodada). Proposta: antes de aplicar as regras, remover da linha todo `\[[A-Z0-9-]+\]` e todo marcador `\[[^\]]*(PENDIENTE|A CONFIRMAR)[^\]]*\]`.
2. **"el mismo" adjetival.** «la misma pregunta», «la misma tarjeta», «el mismo razonamiento», «son los mismos» são usos corretos. Proposta: só marcar quando o termo funciona como pronome, isto é, seguido de pontuação ou fim de linha, ou precedido de preposição + artigo sem substantivo depois: `\b(del|al|de la|de los|con el|con la|en el|en la)\s+mism[oa]s?\b(?!\s+[a-záéíóúñ])` e `\bmism[oa]s?\s*[.,;:]`.
3. **Exit code.** O docstring diz "exit 1 = há BLOQUEANTE", mas o script sai com 1 quando o índice fica abaixo de 80 % sem nenhum BLOQUEANTE (Listboss API e Email). Ou o docstring passa a dizer "exit 1 = RETIDO", ou o código separa os casos (1 = BLOQUEANTE, 3 = retido por índice).
4. **Regra nova (GRAVE, lusismo comercial):** `\bde\s+US?\$\s?\d+[.,]?\d*\s+por\s+US?\$` → sugestão «antes US$X, ahora US$Y».
5. **Regra nova (GRAVE, resíduo PT):** `\bADM\b` → «administrador».
6. **Método de leitura (não é o script):** para doc do Drive, auditar sempre o texto da exportação (`download_file_content`), nunca o de `read_file_content`, que corrompe emoji de 4 bytes e trunca o final.

---

## Tabela resumo

| Doc | Cobertura | Classe A | Índice classe B | Achados B (GRAVE · MENOR) | Questões | Veredito |
|---|---|---|---|---|---|---|
| Comunicaciones | parcial (sem PT) | 0 | 90,4 % (75/83) | 8 (5 · 3) | 4 | LIBERADO COM RESSALVAS |
| Encuesta y regalo | parcial (sem PT) | 0 | 92,3 % (48/52) | 4 (4 · 0) | 1 | LIBERADO COM RESSALVAS |
| Onboarding + Grupo lleno | parcial (seções 4 e 5 sem PT) | 0 | 81,5 % (44/54) | 10 (9 · 1) | 0 | LIBERADO COM RESSALVAS |
| Listboss API | completa | 0 | 100,0 % (50/50) | 0 | 1 | LIBERADO |
| Listboss Email | completa | 0 | 98,7 % (77/78) | 1 (0 · 1) | 0 | LIBERADO |
| Checkout personalizado | completa | 0 | 86,7 % (13/15) | 3 (2 · 1) | 1 | LIBERADO COM RESSALVAS |
| Low tickets | completa | 0 | 93,3 % (14/15) | 1 (1 · 0) | 0 | LIBERADO COM RESSALVAS |
| **Total** | 4 completas · 3 parciais | **0** | **92,5 % (321/347)** | **27 (21 · 6)** | **7** | 2 LIBERADO · 5 COM RESSALVAS · 0 RETIDO |

Nota: Low tickets (93,3 %) e Encuesta (92,3 %) ficam na faixa com ressalvas por um único tipo de achado de busca e troca; corrigidos, chegam a 100 %.

Prioridade de correção (custo de não corrigir): 1) título do ebook em Title Case (8 segmentos em 3 docs); 2) nomes de evento e lista com «–» e A06 (5 segmentos, risco operacional de evento duplicado); 3) «de US$47 por US$19» no checkout (área de conversão); 4) duas redações para a mensagem de compra aprovada; 5) «e-mail» vs «correo»; 6) demais itens MENOR. Antes de publicar Comunicación 3, resolver Q1 a Q3.
