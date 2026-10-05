# -*- coding: utf-8 -*-
"""Ficha de Entrega ES do livro de Intercorrências (padrão da ficha de olheiras,
com a identidade FEP Experience). Sai em espanhol para a equipe hispano-hablante.
Mesmas restrições do Story do pymupdf: sem fundo em bloco, negrito só no início."""
import os, pymupdf
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

HTML = """
<h1>Intercurrencias en el relleno con ácido hialurónico: edición en español</h1>
<p class="sub">Estado de la entrega · 5 de octubre de 2026 · uso interno FEA</p>

<div class="box">
<p><b>Veredicto: LIBERADO.</b> El archivo
«Intercurrencias_en_el_Relleno_con_Acido_Hialuronico_ES.pdf» (221 páginas,
español latinoamericano, trato de usted) está listo para circular.</p>
<p>Revisión ciega en 6 partes y segunda ronda sobre los 75 segmentos modificados: cero hallazgos de clase A (barrera clínica).
Índice editorial entre 97,3 % y 99,6 % en cinco partes; la parte 1 subió de
88,1 % a la franja LIBERADO al corregirse los marcadores de lista.</p>
</div>

<h2>Seguridad clínica verificada id por id contra el portugués</h2>
<ul>
<li>Todas las dosis, unidades, concentraciones, posologías y vías coinciden con el original
(hialuronidasa 1.000 UTR/mL, prednisona 40 mg, adrenalina IM 0,3 a 0,5 mg 1:1000,
amoxicilina/ácido clavulánico 875/125 mg cada 12 h, entre otras).</li>
<li>EV pasó a IV en todo el libro. Negaciones, contraindicaciones, lados y planos preservados.</li>
<li>Retrotraducción de todos los pasajes con dosis, vía y conducta: sin divergencia.</li>
</ul>

<h2>Qué se corrigió tras la revisión ciega</h2>
<table>
<tr><th>Pág.</th><th>Corrección</th></tr>
<tr><td>31, 41, 50</td><td>«1000 UTR/mL» pasa a «1.000 UTR/mL» (punto de millar del glosario).</td></tr>
<tr><td>124</td><td>«relleno capilar» pasa a «llenado capilar» (no confundir con el producto).</td></tr>
<tr><td>132, 137</td><td>«complaciente» (falso amigo) pasa a «de menor/baja complacencia».</td></tr>
<tr><td>147</td><td>Contaminación «tras la manipulación de la zona por parte del paciente».</td></tr>
<tr><td>7, 33, 41, 45, 50, 61</td><td>«ultrasonido/ultrasonografía» unificado en «ecografía».</td></tr>
<tr><td>6, 183</td><td>«swelling factor» glosado en la primera aparición; «festoon» como «festón».</td></tr>
<tr><td>20, 21, 58, 59, 67, 75, 97, 106, 112, 117, 135, 170, 188, 194</td><td>Calcos y repeticiones menores corregidos.</td></tr>
<tr><td>24, 33, 40 a 53, 59, 61, 68 a 75</td><td>Listas con marcador: cada ítem vuelve a su propio párrafo, con su marcador.</td></tr>
</table>

<h2>Códigos QR: 23 leídos por escaneo, todos con el destino correcto</h2>
<ul>
<li><b>11 QR de clase:</b> abren la clase doblada al español en YouTube (no listada).</li>
<li><b>5 QR rotos del original corregidos</b> (págs. 18, 23, 61, 64 y 68), con destino confirmado.</li>
<li><b>QR de artículo científico:</b> el artículo queda en inglés (regla del glosario).</li>
<li><b>Pendiente, compartido de los artículos:</b> solo el de las págs. 23 y 61 abre para cualquier persona. Los de las págs. 13, 18, 21, 26, 30, 33, 40, 64 y 68 exigen «Cualquier persona con el enlace: lector» en el Drive.</li>
<li><b>Pendiente, pág. 36:</b> el archivo del QR ya no existe. El recuadro describe el «Consensus Guidelines for the Management of HA Filler-Induced Vascular Occlusion», que no está en el Drive (el DeLorenzi 2014 del Drive es otro artículo).</li>
</ul>

<h2 class="brk">Reservas abiertas: decisiones del autor</h2>
<p>No impiden circular. El español reproduce fielmente el original; se corrigen en PT y ES juntos.</p>
<h3>Prioridad clínica</h3>
<ul>
<li><b>Pág. 27:</b> «reducción del tiempo de reperfusión capilar» como signo de isquemia. Lo correcto es el aumento (enlentecimiento), como dice la pág. 14.</li>
<li><b>Págs. 31, 41, 50:</b> «inyectar 1.000 UTR/mL» informa la concentración, no la dosis ni el volumen.</li>
<li><b>Piperacilina:</b> 4,5 g en un capítulo y 3,375 g en otro.</li>
<li><b>Ventana de la retina:</b> cuatro cifras distintas a lo largo del libro (30 min, 90 min, 4 h, 12 h).</li>
</ul>
<h3>Línea roja 7: imágenes generadas por IA</h3>
<p>Nueve figuras declaran imagen creada o adaptada por IA: 13, 14, 37, 39, 41, 52, 53, 61 y 62 (esta última en las págs. 192 y 194). La 53 además cita «búsqueda en internet» (derecho de uso) y la 14 y la 52 adaptan obras publicadas. Requiere decisión editorial antes de publicar en PT y ES.</p>
<h3>Títulos y conceptos</h3>
<ul>
<li>Títulos de figura repetidos o que no corresponden: 5, 27, 31, 36, 43 (repetido en 44 y 45) y 62.</li>
<li>Er:YAG descrito como «no ablativo»; efecto Tyndall explicado como «refracción» o «sombra»; triamcinolona «diluida» sin concentración final.</li>
<li>Marcas citadas en el texto (Periogard, Juvederm Volbela); «dipirona» se llama «metamizol» en parte de América Latina.</li>
</ul>

<h2>Qué se verificó en el PDF entregado</h2>
<ul>
<li>Cero glifos de fuente sustituta en las 221 páginas.</li>
<li>OCR de todas las páginas: sin portugués residual, incluidas portada, aperturas, contraportada y las figuras con texto en arte (págs. 20, 39, 54 y 122).</li>
<li>Control de superposición de líneas contra el original y revisión visual página por página.</li>
<li>Control de diagramación en el PDF entregado: cero palabras perdidas, cero líneas fuera de la mancha de texto, de recuadros o sobre imágenes, cero marcadores duplicados (revisión de diagramación del 5/10).</li>
<li>Capa de texto sin portugués residual (se retiró el encabezado oculto de las 5 aperturas de capítulo).</li>
</ul>
<p class="foot">Informes de la revisión: «FEA-traducao-intercorrencias/revisao/parte1 a parte6-relatorio.md».
Planilla de clases y QR: «FEA-Traducao-ES-Intercorrencias-Aulas-e-QR».</p>
"""

CSS = """
* { font-family: Helvetica; }
h1 { font-size: 18px; margin: 0 0 2px 0; color: #5B4599; }
p.sub { font-size: 9.5px; color: #666; margin: 0 0 14px 0; }
h2 { font-size: 13px; margin: 18px 0 6px 0; color: #5B4599; }
h3 { font-size: 10.5px; margin: 12px 0 2px 0; color: #3846BB; }
p, li, td, th { font-size: 9.4px; line-height: 1.5; color: #1a1a1a; }
li { margin-bottom: 3px; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 4px 0; }
th { text-align: left; padding: 4px 6px; color: #5B4599; border-bottom: 2px solid #5B4599; }
td { padding: 4px 6px; border-bottom: 1px solid #E9E9E9; vertical-align: top; }
td:first-child, th:first-child { width: 90px; }
div.box { border-left: 3px solid #5B4599; padding: 2px 0 2px 11px; margin: 4px 0 8px 0; }
div.box p { margin: 0 0 4px 0; }
p.foot { font-size: 8.3px; color: #777; margin-top: 16px; }
"""
MARGEM = 52
caixa = pymupdf.Rect(MARGEM, MARGEM, 595 - MARGEM, 842 - MARGEM)
story = pymupdf.Story(html=HTML, user_css=CSS)
esc = pymupdf.DocumentWriter('produccion/miolo-tmp.pdf')
while True:
    dev = esc.begin_page(pymupdf.Rect(0, 0, 595, 842))
    mais, _ = story.place(caixa); story.draw(dev); esc.end_page()
    if not mais: break
esc.close()
doc = pymupdf.open('produccion/miolo-tmp.pdf')
for i, page in enumerate(doc):
    page.insert_text(pymupdf.Point(MARGEM, 842 - 32),
                     'FEA · Intercurrencias en el relleno con ácido hialurónico (ES) · estado de la entrega · %d/%d' % (i + 1, len(doc)),
                     fontname='helv', fontsize=7.5, color=(0.55, 0.55, 0.55))
doc.set_metadata({'title': 'Intercurrencias (ES): estado de la entrega', 'author': 'FEA, Formación Especialista en Anatomía'})
doc.save('produccion/FEA-Ficha_de_Entrega_Intercurrencias_ES.pdf', deflate=True)
os.remove('produccion/miolo-tmp.pdf')
print('paginas', len(doc))
