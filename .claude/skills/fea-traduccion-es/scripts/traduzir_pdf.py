#!/usr/bin/env python3
"""
Substitui o texto de um PDF diagramado pela tradução, preservando imagens,
posição, fonte, corpo, cor e entrelinha do original.

Uso:
    python3 traduzir_pdf.py original.pdf mapa.json --fontes fontes/ --saida out.pdf
    python3 traduzir_pdf.py original.pdf --estrutura        # extrai o esqueleto

Como funciona:
  1. PDFs de InDesign exportam UMA LINHA POR BLOCO. O script reagrupa as linhas
     em parágrafos por geometria (mesma margem, y consecutivo, salto == entrelinha).
  2. Cada parágrafo é classificado por fonte, corpo e cor: corpo de texto,
     título de seção, cabeçalho corrido, legenda, número de página.
  3. O texto original é removido por redação, com as imagens preservadas.
  4. O espanhol é refluído no MESMO retângulo, com a MESMA fonte (completada por
     completar_fonte.py), justificação, entrelinha e recuo de primeira linha.
  5. Se o espanhol não couber — ele corre 15% a 20% mais longo — o script reduz
     a entrelinha e depois o corpo, em passos pequenos, e REGISTRA o ajuste.
     Nada é cortado: transbordo vira erro, não texto perdido.
"""
import sys, os, json, argparse, re
import pymupdf

TOL_Y      = 3.0     # tolerância para considerar linhas na mesma coluna
MAX_RED_EL = 0.06    # redução máxima da entrelinha (6%)
MAX_RED_PT = 0.04    # redução máxima do corpo (4%)

def cor_rgb(i):
    return ((i >> 16 & 255)/255, (i >> 8 & 255)/255, (i & 255)/255)

def classifica(fontes, tam, cor):
    f = ' '.join(fontes)
    if 'Guardian' in f:                       return 'corpo'
    if tam >= 20:                             return 'titulo_display'
    if 'Playfair' in f:                       return 'titulo_capitulo'
    if tam <= 7.5:                            return 'cabecalho'
    if cor == 0xffffff and tam <= 8.5:        return 'numero_pagina'
    if 'Bold' in f and tam >= 10:             return 'titulo_secao'
    if 'Medium' in f and tam <= 9.5:          return 'legenda'
    return 'outro'

def agrupa(page):
    """Reagrupa as linhas exportadas linha-a-linha em parágrafos."""
    linhas = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip() or s['text'] == ' ']
            if not spans: continue
            txt = ''.join(s['text'] for s in spans)
            if not txt.strip(): continue
            linhas.append(dict(bbox=list(l['bbox']), spans=spans, texto=txt,
                               x0=round(l['bbox'][0], 1), y0=l['bbox'][1], y1=l['bbox'][3]))
    linhas.sort(key=lambda l: (round(l['y0'], 1), l['x0']))

    # margem esquerda do corpo: o x0 mais frequente entre as linhas de texto
    from collections import Counter
    cx = Counter(l['x0'] for l in linhas)
    margem = cx.most_common(1)[0][0] if cx else 0

    paras, atual = [], None
    for l in linhas:
        fontes = {s['font'].split('+')[-1] for s in l['spans']}
        tam    = max(round(s['size'], 1) for s in l['spans'])
        cor    = l['spans'][0]['color']
        tipo   = classifica(fontes, tam, cor)
        mesmoEstilo = (atual and atual['tipo'] == tipo
                       and abs(atual['tam'] - tam) < 1.0 and atual['cor'] == cor)
        if mesmoEstilo and tipo in ('corpo', 'legenda', 'titulo_capitulo', 'titulo_display'):
            salto = l['y0'] - atual['linhas'][-1]['y0']
            # continuação = linha na margem; recuada abre novo parágrafo.
            # A última linha de um parágrafo justificado é curta: comparar a
            # margem DIREITA quebraria o parágrafo ali.
            continua = (abs(l['x0'] - margem) < 2.0) if tipo == 'corpo' else True
            if 0 < salto <= (atual['entrelinha'] or salto) * 1.6 + 2 and continua:
                atual['linhas'].append(l)
                if atual['entrelinha'] is None: atual['entrelinha'] = round(salto, 1)
                continue
        atual = dict(tipo=tipo, tam=tam, cor=cor, fontes=fontes, linhas=[l], entrelinha=None)
        paras.append(atual)

    for p in paras:
        xs0 = [l['bbox'][0] for l in p['linhas']]; xs1 = [l['bbox'][2] for l in p['linhas']]
        p['rect'] = pymupdf.Rect(min(xs0), p['linhas'][0]['bbox'][1],
                                 max(xs1), p['linhas'][-1]['bbox'][3])
        p['texto'] = re.sub(r'\s+', ' ', ' '.join(l['texto'] for l in p['linhas'])).strip()
        p['recuo'] = round(p['linhas'][0]['bbox'][0] - min(xs0[1:]) if len(xs0) > 1 else 0, 1)
        p['negrito'] = [s['text'].strip() for l in p['linhas'] for s in l['spans']
                        if 'Bold' in s['font'] and s['text'].strip()]
        if p['entrelinha'] is None:
            p['entrelinha'] = round(p['tam'] * 1.35, 1)
        # fonte real dominante: a que carrega mais caracteres no parágrafo
        from collections import Counter
        uso = Counter()
        for l in p['linhas']:
            for sp in l['spans']:
                uso[sp['font'].split('+')[-1]] += len(sp['text'])
        p['fonte'] = uso.most_common(1)[0][0] if uso else 'HelveticaNeue'
    return paras

def prepara_fontes(dirFontes):
    arch = pymupdf.Archive()
    reg = {}
    for f in sorted(os.listdir(dirFontes)):
        if not f.lower().endswith(('.otf', '.ttf')): continue
        nome = os.path.splitext(f)[0]
        arch.add(os.path.join(dirFontes, f), f)
        reg[nome] = f
    return arch, reg

def css_de(p, reg, familia=None):
    tam = p['tam']; el = p['entrelinha']
    align = 'justify' if p['tipo'] == 'corpo' else 'left'
    r, g, b = cor_rgb(p['cor'])
    base = p.get('fonte', 'HelveticaNeue')
    # prefere a variante completada com os glifos do espanhol
    if base + 'ES' in reg: base = base + 'ES'
    normal = base if base in reg else None
    if normal is None:                                  # tenta a variante sem peso
        cand = [n for n in reg if n.startswith(base.split('-')[0])]
        normal = sorted(cand, key=len)[0] if cand else list(reg)[0]
    raiz = normal.replace('ES', '').split('-')[0]
    cands = [n for n in reg if n.startswith(raiz) and 'Bold' in n]
    irmaoBold = next((n for n in cands if n.endswith('ES')), cands[0] if cands else normal)
    familia = 'F' + re.sub(r'[^A-Za-z]', '', raiz)
    faces = ['@font-face {font-family: %s; src: url(%s); font-weight: normal;}'
             % (familia, reg[normal]),
             '@font-face {font-family: %s; src: url(%s); font-weight: bold;}'
             % (familia, reg[irmaoBold])]
    return '\n'.join(faces) + """
p {font-family: %s; font-size: %.2fpx; line-height: %.4f; text-align: %s;
   margin: 0; text-indent: %.1fpx; color: rgb(%d,%d,%d);}
b {font-weight: bold;}
""" % (familia, tam, el/tam, align, max(p['recuo'], 0), r*255, g*255, b*255)

def html_de(es, negritos):
    """Reaplica o negrito do original. Se o mapa já traz <b>, respeita o mapa."""
    if '<b>' in es: return '<p>%s</p>' % es
    txt = es
    for frase in sorted({n for n in negritos if len(n) > 3}, key=len, reverse=True):
        if frase in txt and '<b>' not in frase:
            txt = txt.replace(frase, '<b>%s</b>' % frase, 1)
    return '<p>%s</p>' % txt

def aplica(page, paras, mapa, arch, reg, log):
    # 1) remove o texto original, preservando imagens
    for p in paras:
        if p['tipo'] == 'numero_pagina': continue
        if p['id'] not in mapa: continue
        for l in p['linhas']:
            page.add_redact_annot(pymupdf.Rect(l['bbox']))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

    # 2) refluí o espanhol no mesmo retângulo
    for p in paras:
        if p['id'] not in mapa: continue
        es = mapa[p['id']]
        if not es: continue
        html = html_de(es, p['negrito'])
        # folga de 2pt à direita e generosa embaixo: o espanhol corre mais longo
        rect = pymupdf.Rect(p['rect'].x0 - 1, p['rect'].y0 - 2,
                            p['rect'].x1 + 2, p['rect'].y1 + 2)
        ok = False
        for redEl in (0, 0.02, 0.04, MAX_RED_EL):
            for redPt in (0, 0.02, MAX_RED_PT):
                q = dict(p); q['entrelinha'] = p['entrelinha']*(1-redEl); q['tam'] = p['tam']*(1-redPt)
                css = css_de(q, reg)
                sobra, _ = page.insert_htmlbox(rect, html, css=css, archive=arch, scale_low=0)
                if sobra >= 0:
                    if redEl or redPt:
                        log.append(dict(pagina=page.number+1, id=p['id'],
                                        ajuste='entrelinha -%d%% corpo -%d%%'%(redEl*100, redPt*100)))
                    ok = True; break
                # não caber: limpa e tenta com menos entrelinha/corpo
                page.add_redact_annot(rect); page.apply_redactions(
                    images=pymupdf.PDF_REDACT_IMAGE_NONE,
                    graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
            if ok: break
        if not ok:
            log.append(dict(pagina=page.number+1, id=p['id'], erro='TRANSBORDO — não caiu no quadro'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('mapa', nargs='?')
    ap.add_argument('--fontes', default='fontes')
    ap.add_argument('--saida', default='traduzido.pdf')
    ap.add_argument('--paginas', default='')
    ap.add_argument('--estrutura', action='store_true')
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    alvo = ([int(x) for x in a.paginas.split(',')] if a.paginas
            else list(range(1, doc.page_count+1)))

    if a.estrutura:
        out = {}
        for n in alvo:
            paras = agrupa(doc[n-1])
            for i, p in enumerate(paras): p['id'] = 'p%d_%02d' % (n, i)
            out[str(n)] = [dict(id=p['id'], tipo=p['tipo'], tam=p['tam'],
                                cor=hex(p['cor']), entrelinha=p['entrelinha'],
                                recuo=p['recuo'], rect=[round(v,1) for v in p['rect']],
                                negrito=p['negrito'], pt=p['texto']) for p in paras]
        print(json.dumps(out, ensure_ascii=False, indent=1)); return

    mapa = json.load(open(a.mapa, encoding='utf-8'))
    arch, reg = prepara_fontes(a.fontes)
    log = []
    for n in alvo:
        page = doc[n-1]
        paras = agrupa(page)
        for i, p in enumerate(paras): p['id'] = 'p%d_%02d' % (n, i)
        aplica(page, paras, mapa, arch, reg, log)
    doc.save(a.saida, garbage=3, deflate=True)
    print(json.dumps(dict(saida=a.saida, paginas=alvo, ajustes=log),
                     ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
