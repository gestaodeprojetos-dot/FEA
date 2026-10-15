# -*- coding: utf-8 -*-
"""O cmap mente: subconjuntos listam codepoints cujo glifo esta vazio, e o
motor de texto desenha nada em vez de recorrer a alternativa. Remover essas
entradas devolve o comportamento correto (ex.: fi/fl viram f+i, f+l)."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

BRANCOS = {0x20, 0xA0, 0x2007, 0x2009, 0x200A, 0x200B, 0x2060, 0xFEFF}
for arq in sorted(os.listdir(sys.argv[1])):
    if not arq.lower().endswith(('.ttf', '.otf')): continue
    p = os.path.join(sys.argv[1], arq)
    t = TTFont(p, fontNumber=0)
    if 'cmap' not in t: continue
    gs = t.getGlyphSet()
    vazios = set()
    for cp, gn in (t.getBestCmap() or {}).items():
        if cp in BRANCOS: continue
        bp = BoundsPen(gs)
        try: gs[gn].draw(bp)
        except Exception: pass
        if bp.bounds is None: vazios.add(cp)
    if not vazios: continue
    for tb in t['cmap'].tables:
        for cp in list(tb.cmap):
            if cp in vazios: del tb.cmap[cp]
    t.save(p)
    amostra = ''.join(chr(c) for c in sorted(vazios)[:12])
    print('%-34s -%d entradas fantasma  %r' % (arq, len(vazios), amostra))
