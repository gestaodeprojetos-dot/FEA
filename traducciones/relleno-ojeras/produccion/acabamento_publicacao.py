# -*- coding: utf-8 -*-
"""Acabamento de publicacao do ebook espanhol.

Quatro correcoes sobre o PDF traduzido, todas verificaveis:

1. GLIFOS DE RECURSO — a Helvetica Neue Bold fundida nao tinha 'h', 'j' e 'y'
   (o portugues nunca os usou em negrito neste livro), e o motor caiu para
   Noto Serif: tres letras serifadas no meio de palavras em negrito, nas
   paginas 11 e 12. Os glifos vem da Medium com arraste horizontal de
   28/1000 em — a diferenca de haste medida entre os dois cortes (114 -> 142).
   A letra errada NAO sai por redacao: a redacao apaga o operador de texto
   inteiro, e levaria a linha toda junto (testado — 'Piel ' desaparecia).
   Como o fundo e branco puro nos tres pontos (amostrado acima e abaixo de
   cada glifo), a letra errada e coberta e a certa desenhada por cima.
   A letra certa e mais estreita que a fatia que a serifada ocupava, entao
   vai centrada: a sobra se divide nos dois lados e nada se desloca.
   Resta na camada de texto o glifo antigo, oculto sob a mascara; o texto
   extraido sai correto, que e o que importa para busca, copia e leitor de
   tela. Some de vez na proxima passagem completa do traduzir_pdf.py.

2. METADADOS — o arquivo saiu do InDesign sem titulo, autor nem assunto.

3. IDIOMA — /Lang era 'en-US', herdado do portugues: um leitor de tela
   pronunciaria o espanhol com fonetica inglesa. Passa a 'es-419'.

4. MARCADORES E LINKS — 74 paginas sem indice navegavel, e nenhum QR
   clicavel embora o texto diga «haga clic aqui». Entram 8 marcadores e um
   link sobre cada QR, com o destino que o proprio codigo carrega.

Uso:
    python3 acabamento_publicacao.py entrada.pdf fonte_bold.ttf log-qr.json saida.pdf
"""
import sys, json
import pymupdf

ENTRADA, FONTE_BOLD, LOG_QR, SAIDA = sys.argv[1:5]

TITULO = 'Relleno Tridimensional de Ojeras — Una Guía Completa con la Metodología ARTI'
AUTOR  = 'Dr. João Pithon'
MARCADORES = [
    [1, 'Índice', 3], [1, 'Introducción', 5],
    [1, 'Metodología ARTI en el Relleno de Ojeras', 7],
    [1, '01. A — Anatomía y fisiología del envejecimiento', 10],
    [1, '02. R — Reología: la elección del producto ideal', 37],
    [1, '03. T — Técnicas', 47],
    [1, '04. I — Intercurrencias', 59],
    [1, '05. Conclusión', 71],
]

doc  = pymupdf.open(ENTRADA)
face = pymupdf.Font(fontfile=FONTE_BOLD)
rel  = {'glifos': [], 'marcadores': 0, 'links': 0}

# ---- 1. glifos de recurso ------------------------------------------------
alvos = {}
for pno in range(doc.page_count):
    for b in doc[pno].get_text('dict')['blocks']:
        if b['type']:
            continue
        for l in b['lines']:
            sp = l['spans']
            for i, s in enumerate(sp):
                if 'Noto' not in s['font'] or not s['text'].strip():
                    continue
                x1 = sp[i + 1]['origin'][0] if i + 1 < len(sp) else s['bbox'][2]
                alvos.setdefault(pno, []).append({
                    'ch': s['text'], 'tam': s['size'], 'cor': s['color'],
                    'x0': s['origin'][0], 'x1': x1, 'y': s['origin'][1],
                    'bbox': list(s['bbox']),
                })

for pno, itens in alvos.items():
    page = doc[pno]
    for it in itens:
        cobre = pymupdf.Rect(it['x0'], it['bbox'][1] - 0.4,
                             it['x1'], it['bbox'][3] + 0.4)
        page.draw_rect(cobre, color=None, fill=(1, 1, 1), width=0)
        av = face.text_length(it['ch'], fontsize=it['tam'])
        dx = ((it['x1'] - it['x0']) - av) / 2.0
        page.insert_text((it['x0'] + dx, it['y']), it['ch'],
                         fontname='hnb', fontfile=FONTE_BOLD, fontsize=it['tam'],
                         color=pymupdf.sRGB_to_pdf(it['cor']))
        rel['glifos'].append({'pagina': pno + 1, 'letra': it['ch'],
                              'fatia_pt': round(it['x1'] - it['x0'], 3),
                              'avanco_pt': round(av, 3),
                              'folga_lado_pt': round(dx, 3)})

# ---- 2 e 3. metadados e idioma ------------------------------------------
doc.set_metadata({
    'title': TITULO, 'author': AUTOR,
    'subject': 'Relleno de ojeras con ácido hialurónico: anatomía periorbitaria, '
               'reología, técnicas de inyección e intercurrencias. Metodología ARTI.',
    'keywords': 'relleno de ojeras, ojeras, ácido hialurónico, metodología ARTI, '
                'anatomía periorbitaria, ligamento retinacular orbitario, reología, '
                'G prima, cánula, hialuronidasa, intercurrencias, estética avanzada, FEA',
    'creator': 'FEA — Formación en Estética Avanzada',
    'producer': 'FEA — edición en español (LatAm)',
})
doc.xref_set_key(doc.pdf_catalog(), 'Lang', '(es-419)')

# ---- 4. marcadores e links ----------------------------------------------
doc.set_toc(MARCADORES)
rel['marcadores'] = len(MARCADORES)

log = json.load(open(LOG_QR))
for d in log['detalhe']:
    uri = d.get('para') or d.get('de')
    if not uri:
        continue
    page = doc[d['pagina'] - 1]
    r = pymupdf.Rect(d['rect'])
    if any(pymupdf.Rect(l['from']).intersects(r) for l in page.get_links()):
        continue
    page.insert_link({'kind': pymupdf.LINK_URI, 'from': r, 'uri': uri})
    rel['links'] += 1

try:                      # os QR nao trocados: le o destino do proprio codigo
    import cv2, numpy as np
    det = cv2.QRCodeDetector()
    for i in range(doc.page_count):
        page = doc[i]; pix = page.get_pixmap(dpi=200)
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR if pix.n == 4 else cv2.COLOR_RGB2BGR)
        ok, txts, pts, _ = det.detectAndDecodeMulti(img)
        if not ok:
            continue
        for t, p in zip(txts, pts):
            if not t or not t.lower().startswith('http'):
                continue
            xs = [float(q[0]) * 72 / 200 for q in p]
            ys = [float(q[1]) * 72 / 200 for q in p]
            r = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
            if any(pymupdf.Rect(l['from']).intersects(r) for l in page.get_links()):
                continue
            page.insert_link({'kind': pymupdf.LINK_URI, 'from': r, 'uri': t})
            rel['links'] += 1
except ImportError:
    rel['aviso'] = 'opencv ausente: so os QR do log ganharam link'

doc.save(SAIDA, garbage=4, deflate=True, clean=True)
doc.close()

v = pymupdf.open(SAIDA)
rel['verificacao'] = {
    'paginas': v.page_count,
    'linhas_corrigidas': [t for t in ('Piel y tejido subcutáneo:', 'Almohadillas grasas:')
                          if any(t in v[i].get_text() for i in range(v.page_count))],
    'links': sum(len(v[i].get_links()) for i in range(v.page_count)),
    'marcadores': len(v.get_toc()),
    'Lang': v.xref_get_key(v.pdf_catalog(), 'Lang')[1],
}
print(json.dumps(rel, ensure_ascii=False, indent=1))
