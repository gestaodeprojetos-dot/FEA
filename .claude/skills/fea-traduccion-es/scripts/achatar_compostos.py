# -*- coding: utf-8 -*-
"""Achata glifos compostos posicionados por POINT MATCHING. Alguns tipos (Playfair Display) posicionam o acento
por POINT MATCHING, que motores de PDF costumam ignorar — o acento sai fora de
lugar. Decompor resolve na origem, sem tocar no desenho."""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen

DIR = sys.argv[1] if len(sys.argv) > 1 else 'fontes'
for arq in sorted(os.listdir(DIR)):
    if not arq.lower().endswith('.ttf'): continue
    p = os.path.join(DIR, arq)
    t = TTFont(p, fontNumber=0)
    if 'glyf' not in t: continue
    gs = t.getGlyphSet(); glyf = t['glyf']
    alvos = [g for g in t.getGlyphOrder()
             if glyf[g].isComposite() and any(
                 not (c.flags & 0x2) for c in (glyf[g].components or []))]
    if not alvos: continue
    for g in alvos:
        antes = BoundsPen(gs); gs[g].draw(antes)
        rec = DecomposingRecordingPen(gs); gs[g].draw(rec)
        tp = TTGlyphPen(None); rec.replay(tp)
        glyf[g] = tp.glyph()
    t.save(p)
    t2 = TTFont(p, fontNumber=0); gs2 = t2.getGlyphSet()
    ruim = []
    for g in alvos:
        a = BoundsPen(gs2); gs2[g].draw(a)
        if a.bounds is None: ruim.append(g)
    print('%-34s %d compostos por point-matching achatados%s'
          % (arq, len(alvos), '  VAZIOS: %s' % ruim if ruim else ''))
