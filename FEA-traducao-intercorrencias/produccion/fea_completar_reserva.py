"""Glifos que o português nunca usou e o espanhol precisa (Y, %, [ ], ’, letras
acentuadas em cortes raros). O motor de PDF cai em Noto Serif sem avisar. Aqui cada
glifo ausente (ou com contorno vazio) é copiado de uma fonte livre da mesma classe,
escalado pela altura de maiúscula do alvo. Funciona com TrueType e CFF."""
import glob, sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
X = 'produccion/fontes-extra/'
PARES = [
 ('fontes/HeadingProDouble-Bold.otf', X+'Montserrat-Bold.ttf'),
 ('fontes/GuardianTextEgyp-Regular.otf', X+'RobotoSlab-Regular.ttf'),
 ('fontes/GuardianTextEgyp-Bold.otf', X+'RobotoSlab-Bold.ttf'),
 ('fontes/HelveticaNeue-Italic.ttf', X+'LiberationSans-Italic.ttf'),
 ('fontes/HelveticaNeue-ItalicES.ttf', X+'LiberationSans-Italic.ttf'),
 ('fontes/HelveticaNeue-MediumES.ttf', X+'LiberationSans-Regular.ttf'),
 ('fontes/HelveticaNeue-Medium.ttf', X+'LiberationSans-Regular.ttf'),
 ('fontes/HelveticaNeue-BoldES.ttf', X+'LiberationSans-Bold.ttf'),
 ('fontes/HelveticaNeueES.ttf', X+'LiberationSans-Regular.ttf'),
 ('fontes/HelveticaNeue-CondensedBold.ttf', X+'LiberationSans-Bold.ttf'),
 ('fontes/ArialUnicodeMS.ttf', X+'LiberationSans-Regular.ttf'),
 ('fontes/AdventPro-BoldES.ttf', X+'AdventPro-Bold-OFL.ttf'),
 ('fontes/AdventPro-Bold.ttf', X+'AdventPro-Bold-OFL.ttf'),
 ('fontes/AdventPro-Medium.ttf', X+'AdventPro-Medium-OFL.ttf'),
 ('fontes/AdventPro-SemiBold.ttf', X+'AdventPro-SemiBold-OFL.ttf'),
]
CHARS = ''.join(chr(c) for c in range(0x21, 0x7f)) + 'áéíóúÁÉÍÓÚñÑüÜ¿¡“”‘’«»%≥≤°±·×–'
def tem(t, gs, cm, c):
    g = cm.get(ord(c))
    if not g or g not in gs: return False
    p = BoundsPen(gs); gs[g].draw(p); return p.bounds is not None
def capH(t, gs, cm):
    for c in 'HIE':
        if tem(t, gs, cm, c):
            p = BoundsPen(gs); gs[cm[ord(c)]].draw(p); return p.bounds[3]
    return t['head'].unitsPerEm * 0.7
def completa(alvo, doador):
    t = TTFont(alvo); d = TTFont(doador)
    cmt = t.getBestCmap() or {}; gst = t.getGlyphSet(); cmd = d.getBestCmap(); gsd = d.getGlyphSet()
    k = capH(t, gst, cmt) / capH(d, gsd, cmd)
    cff = 'CFF ' in t
    feitos = []
    for c in CHARS:
        if tem(t, gst, cmt, c) or not cmd.get(ord(c)): continue
        gd = cmd[ord(c)]; adv = round(d['hmtx'][gd][0] * k)
        nome = cmt.get(ord(c)) or ('uni%04X' % ord(c))
        if cff:
            top = t['CFF '].cff.topDictIndex[0]
            pen = T2CharStringPen(adv, None)
            rec = DecomposingRecordingPen(gsd); gsd[gd].draw(rec); rec.replay(TransformPen(pen, (k, 0, 0, k, 0, 0)))
            cs = pen.getCharString(private=top.Private, globalSubrs=t['CFF '].cff.GlobalSubrs)
            if nome in top.CharStrings.charStrings:
                idx = top.CharStrings.charStrings[nome]
                if top.CharStrings.charStringsAreIndexed:
                    top.CharStrings.charStringsIndex.items[idx] = cs
                else:
                    top.CharStrings.charStrings[nome] = cs
            else:
                if top.CharStrings.charStringsAreIndexed:
                    top.CharStrings.charStringsIndex.append(cs)
                    top.CharStrings.charStrings[nome] = len(top.CharStrings.charStringsIndex) - 1
                else:
                    top.CharStrings.charStrings[nome] = cs
                # charset e glyphOrder costumam ser a MESMA lista: acrescentar
                # nos dois duplicava o nome e deslocava o cmap em um glifo
                if nome not in top.charset: top.charset.append(nome)
                if nome not in t.getGlyphOrder():
                    t.setGlyphOrder(t.getGlyphOrder() + [nome])
        else:
            pen = TTGlyphPen(None)
            rec = DecomposingRecordingPen(gsd); gsd[gd].draw(rec); rec.replay(TransformPen(pen, (k, 0, 0, k, 0, 0)))
            t['glyf'][nome] = pen.glyph()
            if nome not in t.getGlyphOrder():
                t.setGlyphOrder(t.getGlyphOrder() + [nome])
        t['hmtx'][nome] = (adv, 0)
        for tb in t['cmap'].tables:
            if tb.isUnicode(): tb.cmap[ord(c)] = nome
        feitos.append(c)
    if 'maxp' in t: t['maxp'].numGlyphs = len(t.getGlyphOrder())
    t.save(alvo)
    return ''.join(feitos)
if __name__ == '__main__':
    import os
    for a, d in PARES:
        if os.path.exists(a): print(a.split('/')[-1], '<-', d.split('/')[-1], ':', completa(a, d))
