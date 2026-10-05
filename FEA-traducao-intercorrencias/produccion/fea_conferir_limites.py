"""Checagem obrigatória de LIMITES da diagramação (criada depois do erro da pág. 23):
nenhuma linha do espanhol pode sair da área que o original ocupa.
  1. margem: linha além da margem direita/esquerda do texto original da página
  2. quadro: linha que começa dentro de um quadro (fundo preenchido) e vaza a
     borda, ou linha de fora que cruza a borda do quadro
  3. imagem: linha sobre imagem/QR que no original não tinha texto por cima
  4. pé: linha abaixo da última linha de texto do original (fora o fólio)
  5. marcador: dois '•' no mesmo item (o de cima aparece como '⁝')
  6. encolhido: corpo de texto menor que 92 % do corpo original (limite da skill)
Uso: python3 fea_conferir_limites.py original.pdf traduzido.pdf  (exit 1 se achar)"""
import sys, pymupdf

def linhas(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t and t not in ('•',): out.append((pymupdf.Rect(l['bbox']), t))
    return out

def quadros(page):
    return [dr['rect'] for dr in page.get_drawings()
            if dr.get('fill') is not None and dr['rect'].width > 80 and dr['rect'].height > 30
            and dr['rect'].width < page.rect.width - 20 and dr['rect'].height < page.rect.height - 20]

def imagens(page):
    return [pymupdf.Rect(b['bbox']) for b in page.get_text('dict')['blocks'] if b['type'] == 1
            and pymupdf.Rect(b['bbox']).width < page.rect.width - 20]

def area(r): return max(r.width, 0) * max(r.height, 0)

o, t = pymupdf.open(sys.argv[1]), pymupdf.open(sys.argv[2])
achados = []
for n in range(t.page_count):
    po, pt = o[n], t[n]
    LO = [r for r, _ in linhas(po) if 45 < r.y0 < 605]
    LT = [(r, s) for r, s in linhas(pt) if 45 < r.y0 < 605]
    if not LO or not LT: continue
    x0, x1 = min(r.x0 for r in LO), max(r.x1 for r in LO)
    y1 = max(r.y1 for r in LO)
    Q = quadros(pt); I = imagens(po)
    for r, s in LT:
        tag = None
        if r.x1 > max(x1, 400.6) + 1.5 or r.x0 < x0 - 3: tag = 'margem'
        for q in Q:
            dentro = q.contains(pymupdf.Point(r.x0 + 1, (r.y0 + r.y1) / 2))
            if dentro and (r.x1 > q.x1 - 1 or r.y1 > q.y1 + 1): tag = 'quadro'
            if not dentro and r.intersects(q) and area(r & q) > 0.15 * area(r): tag = 'quadro'
        for im in I:
            if area(r & im) > 0.15 * area(r) and not any(area(x & im) > 0.15 * area(x) for x in LO):
                tag = 'imagem'
        if r.y1 > max(y1, 592) + 2: tag = tag or 'pé'
        if tag: achados.append((n + 1, tag, [round(v) for v in r], s[:50]))
    bs = [c['bbox'] for b in pt.get_text('rawdict')['blocks'] for l in b.get('lines', [])
          for sp in l['spans'] for c in sp['chars'] if c['c'] == '•']
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            if abs(bs[i][0] - bs[j][0]) < 3 and abs(bs[i][1] - bs[j][1]) < 9:
                achados.append((n + 1, 'marcador', [round(v) for v in bs[i]], '• duplicado'))
    import collections
    def tamanhos(pg):
        c = collections.Counter()
        for b in pg.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                if 45 < l['bbox'][1] < 605:
                    for sp in l['spans']:
                        if sp['text'].strip(): c[round(sp['size'], 1)] += len(sp['text'])
        return c
    orig = sorted({t for t in tamanhos(po)})
    if orig:
        for b in pt.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                if not (45 < l['bbox'][1] < 605): continue
                for sp in l['spans']:
                    if not sp['text'].strip(): continue
                    acima = [o for o in orig if o >= sp['size'] - 0.05]
                    if acima and sp['size'] / acima[0] < 0.915 and sp['size'] / acima[0] > 0.5:
                        achados.append((n + 1, 'encolhido', [round(v) for v in sp['bbox']],
                                        '%.2f de %.1f: %s' % (sp['size'], acima[0], sp['text'][:30])))
                        break
pags = sorted({a[0] for a in achados})
for a in achados: print(*a)
print(len(achados), 'linhas fora do limite em', len(pags), 'páginas:', pags)
sys.exit(1 if achados else 0)
