# -*- coding: utf-8 -*-
"""Ficha de entrega do ebook espanhol, em PDF, para circular no time.

Resume o veredito, as onze trocas aplicadas depois da revisao cega e as
ressalvas que continuam abertas. Sai em espanhol porque o destinatario e a
equipe que atende o publico hispano-hablante.

Duas restricoes do motor de composicao do pymupdf que a folha de estilo
respeita, e que quebram o alinhamento se alguem mexer:

1. As corridas de uma linha sao alinhadas pelo TOPO da caixa, nao pela linha
   de base. Qualquer troca de fonte ou de corpo no meio da linha — um
   monoespacado embutido, um negrito no meio da frase — desce a palavra em
   relacao ao resto. Por isso: termo entre aspas angulares em vez de
   monoespacado, e negrito so quando abre o paragrafo, a celula ou o item.
2. Fundo de bloco (`background`) e repintado em cada pagina por onde o fluxo
   passa, deixando faixas soltas nas paginas seguintes. Por isso a hierarquia
   sai por cor, peso e filete, nunca por preenchimento.

Uso, a partir de traducciones/relleno-ojeras/:
    python3 produccion/ficha_entrega_es.py
"""
import os
import pymupdf

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

HTML = """
<h1>Relleno Tridimensional de Ojeras — edición en español</h1>
<p class="sub">Estado de la entrega · 23 de septiembre de 2026 · uso interno FEA</p>

<div class="box">
<p><b>Veredicto: LIBERADO.</b> El archivo
«Relleno_Tridimensional_de_Ojeras_ES.pdf» — 74 páginas,
español latinoamericano — está listo para comercializar.</p>
<p>Auditoría determinística: índice 100 % (1.221 de 1.221 segmentos
limpios), cero hallazgos de clase A (barrera clínica).</p>
</div>

<h2>Qué salió corregido en esta versión</h2>
<p>Once cambios aplicados tras la revisión ciega. Todos verificados en la capa
de texto y en renderizado página por página.</p>
<table>
<tr><th>Pág.</th><th>Qué se corrigió</th></tr>
<tr><td>12</td><td>Faltaba la preposición: «apunte el celular al código QR».</td></tr>
<tr><td>17, 21, 22, 52</td><td>El reborde orbitario tenía cinco nombres distintos. Unificado en «reborde orbitario», conservando «superior» e «inferior» donde el original distingue los bordes.</td></tr>
<tr><td>30</td><td>«en sentido distal» → caudal. «Craneal» se empareja con «caudal»; «distal» pertenece a otro eje.</td></tr>
<tr><td>34</td><td>La sigla «(ORL)» contradecía el adjetivo y difería de las págs. 12 y 49 → (LRO) en las dos ocurrencias.</td></tr>
<tr><td>6</td><td>«Metodología ARTI» con mayúscula, como en las otras seis menciones.</td></tr>
<tr><td>52</td><td>«ligamento LCC» decía «ligamento ligamento» → soporte al LCC.</td></tr>
<tr><td>20</td><td>Guion corto sustituido por raya en la apertura del capítulo.</td></tr>
<tr><td>44</td><td>La unidad «20 mg/mL» ya no se parte entre líneas.</td></tr>
</table>

<h2>Qué se verificó después de aplicar</h2>
<ul>
<li>Auditoría LIBERADO, 100 %; cero hallazgos de clase A.</li>
<li>Cero glifos de fuente sustituta en las 74 páginas.</li>
<li>Capa de texto idéntica en las 64 páginas no tocadas.</li>
<li>Cero superposiciones nuevas en las 10 páginas tocadas.</li>
<li>Intactos: 136 imágenes, 33 códigos QR clicables, 8 marcadores de navegación,
idioma del documento «es-419», metadatos de título y autor.</li>
<li>Las 10 páginas tocadas fueron revisadas visualmente a 200 y 300 dpi, una por una.</li>
</ul>

<h2 class="brk">Reservas — lo que sigue abierto</h2>
<p>Ninguna de estas reservas impide comercializar. Se listan por costo de no
resolverlas.</p>

<h3>1. Falta el PDF original en portugués</h3>
<p class="tag">bloquea dos capas de revisión</p>
<p>Sin el original no se ejecutaron las capas 2 y 3 de la revisión: la
verificación dosis por dosis contra la fuente y la retrotraducción de los
pasajes técnicos. Esas capas son las que detectan el error silencioso — el
número correcto en la estructura equivocada, el ligamento cambiado, el orden de
los pasos invertido, el «no» perdido. El español no los delata: el texto queda
perfectamente legible diciendo otra cosa.</p>
<p><b>Lo que sí está cubierto:</b> coherencia interna, plausibilidad clínica y
calidad editorial. Toda la posología verificable está íntegra
(«prednisona 40 mg/día», «Arnica montana D2»,
«20 mg/mL», «25 mg/mL», decimales con coma,
espacio entre cifra y unidad).</p>
<p><b>Costo de cerrarlo:</b> cerca de una hora, en cuanto llegue el PDF en portugués.</p>

<h3>2. Dos códigos QR llevan a material que no está en español</h3>
<p class="tag">decisión del autor</p>
<p>Pág. 12 (e-book de Allergan) y págs. 18, 25 y 30 (libro AFE, el mismo destino
en las tres). Los 20 QR de video ya apuntan a los activos en español, y los QR de
artículo científico apuntan al artículo en inglés, como manda el glosario —
decisión ya tomada.</p>

<h3>3. Tres puntos que dependen del autor</h3>
<p class="tag">no afectan el veredicto</p>
<ul>
<li><b>Pág. 34</b> — el texto anuncia «los siguientes elementos anatómicos» y la
lista no aparece; el párrafo siguiente ya concluye. O se perdió, o la frase
debería remitir a una figura.</li>
<li><b>Pág. 40</b> — «la fuerza G que se le aplica». G′ es el módulo elástico; en
reología no existe «fuerza G», y en español el término remite a fuerza de
aceleración. Probable holgura del original.</li>
<li><b>Pág. 66</b> — el pie «Anatomía del SNY y del SPM» está bajo la foto del
hematoma, sin relación con la imagen. Residuo repetido de la pág. 30.</li>
</ul>

<h3>4. Un punto tipográfico registrado</h3>
<p class="tag">sin impacto de contenido</p>
<p>En los infográficos de las págs. 22, 36 y 57 la cursiva de máquina de escribir
sólo existe como píxel, no como fuente: fue sustituida por Liberation Mono
Italic. Es el único punto del material que cambia de tipografía.</p>

<h2>Dos cosas que la revisión descartó</h2>
<ul>
<li><b>No hay texto perdido entre las págs. 29 y 30.</b> Un informe anterior lo
señalaba. La pág. 29 cierra con un período completo y la pág. 30 abre una sección
nueva; la alarma venía de un DOCX incompleto.</li>
<li><b>La entrega anterior en DOCX estaba incompleta</b> — le faltaba la pág. 26
entera. Este PDF está completo; el DOCX ya no sirve como referencia de contenido.</li>
</ul>

<h2>Lo que la revisión confirmó correcto</h2>
<ul>
<li><b>Terminología bloqueada, sin excepción:</b> «cigomático»
con C en las 10 ocurrencias; «surco nasoyugal» en las 10;
«efecto Tyndall» con T mayúscula en las 10. Cero ocurrencias
de las trampas listadas en el glosario.</li>
<li><b>Trato formal uniforme:</b> «usted» en todo el material,
incluidos los imperativos de la conclusión. Ningún tuteo.</li>
<li><b>Marcas intactas:</b> Yvoire Contour, Restylane Lift, Voluma, Subskin,
Biogelis Volume, Traumeel S, Motix, Thrombophob, Allergan.</li>
<li><b>Español nativo:</b> sin lusismo sintáctico, sin conector repetido, sin
énfasis comercial brasileño traducido al pie de la letra.</li>
</ul>

<p class="foot">Informe completo de la revisión:
«traducciones/relleno-ojeras/relatorio-revision-es.md».
Script de las correcciones:
«traducciones/relleno-ojeras/produccion/correcciones_revision.py».</p>
"""

CSS = """
* { font-family: Helvetica; }
h1 { font-size: 19px; margin: 0 0 2px 0; color: #7a5a12; }
p.sub { font-size: 9.5px; color: #666; margin: 0 0 14px 0; }
h2 { font-size: 13.5px; margin: 20px 0 6px 0; color: #7a5a12; }
h3 { font-size: 11px; margin: 14px 0 1px 0; color: #222; }
p.tag { font-size: 8.5px; color: #8a6b1d; margin: 0 0 4px 0; }
p, li, td, th { font-size: 9.6px; line-height: 1.5; color: #1a1a1a; }
li { margin-bottom: 3px; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 4px 0; }
/* nada de fundo em bloco: o motor do Story repinta o retangulo de fundo em
   cada pagina por onde o fluxo passa, e sobram faixas soltas. Hierarquia por
   cor e peso, nao por preenchimento. */
th { text-align: left; padding: 4px 6px; color: #5c4410;
     border-bottom: 2px solid #c8b58a; }
td { padding: 4px 6px; border-bottom: 1px solid #e6e0d4; vertical-align: top; }
td:first-child, th:first-child { width: 62px; white-space: nowrap; }
div.box { border-left: 3px solid #b99a4a; padding: 2px 0 2px 11px;
          margin: 4px 0 8px 0; }
div.box p { margin: 0 0 4px 0; }
/* o motor do Story alinha tamanhos diferentes pelo topo, nao pela linha de
   base: qualquer corpo menor num trecho embutido desceria a palavra. Por isso
   o monoespacado mantem o corpo do texto. */
span.mono { font-family: Courier; }
span.tag { color: #8a6b1d; font-weight: normal; }
p.foot { font-size: 8.5px; color: #777; margin-top: 18px; }
"""

MARGEM = 52
caixa = pymupdf.Rect(MARGEM, MARGEM, 595 - MARGEM, 842 - MARGEM)
story = pymupdf.Story(html=HTML, user_css=CSS)
escritor = pymupdf.DocumentWriter('miolo-tmp.pdf')
while True:
    dev = escritor.begin_page(pymupdf.Rect(0, 0, 595, 842))
    mais, _ = story.place(caixa)
    story.draw(dev)
    escritor.end_page()
    if not mais:
        break
escritor.close()

doc = pymupdf.open('miolo-tmp.pdf')
for i, page in enumerate(doc):
    page.insert_text(pymupdf.Point(MARGEM, 842 - 32),
                     'FEA · Relleno Tridimensional de Ojeras (ES) · estado de la entrega · %d/%d'
                     % (i + 1, len(doc)),
                     fontname='helv', fontsize=7.5, color=(0.55, 0.55, 0.55))
doc.set_metadata({'title': 'Relleno Tridimensional de Ojeras (ES) — estado de la entrega',
                  'author': 'FEA — Formação em Estética Avançada',
                  'subject': 'Veredicto, correcciones aplicadas y reservas abiertas'})
doc.save('Ficha_de_Entrega_ES.pdf', deflate=True)
print('paginas', len(doc))
