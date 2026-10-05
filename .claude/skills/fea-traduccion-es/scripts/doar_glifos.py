# -*- coding: utf-8 -*-
"""Doa glifos de um corte da familia para outro, com inclinacao ou
engrossamento sinteticos — o ultimo recurso antes de trocar de tipo.

Quando um corte nao tem o glifo E nao ha como compor (nao e acento nem sinal
invertido), o glifo vem de OUTRO CORTE DA MESMA FAMILIA:

  --inclinar 12   o romano virando italica. Exato quando a italica do tipo e
                  uma obliqua (Helvetica Neue Italic e). Use o italicAngle da
                  propria fonte de destino.
  --engrossar 29  romano virando Medium/Bold, por arraste horizontal. Meca a
                  diferenca de haste entre os dois cortes (bbox do 'l') em
                  unidades de 1000/em, e passe a diferenca.
  --girar         180 graus dentro da caixa, para ¿ e ¡ a partir de ? e !.

Uso:
    python3 doar_glifos.py fontes/HelveticaNeue.ttf fontes/HelveticaNeue-Italic.ttf \\
        --chars 'Hjyíó' --inclinar 12 --saida fontes/HelveticaNeue-ItalicES.ttf
    python3 doar_glifos.py fontes/HelveticaNeue-Bold.ttf fontes/HelveticaNeue-Bold.ttf \\
        --girar '¿:?,¡:!' --saida fontes/HelveticaNeue-BoldES.ttf
"""
import math, argparse, json
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform


def nome_de(t, ch):
    return (t.getBestCmap() or {}).get(ord(ch))


def registra(t, ch, glifo, larg):
    nome = 'uni%04X' % ord(ch)
    while nome in t.getGlyphOrder(): nome += 'x'
    t['glyf'][nome] = glifo
    t['hmtx'][nome] = (larg, 0)
    for tb in t['cmap'].tables:
        if tb.isUnicode(): tb.cmap[ord(ch)] = nome
    t['maxp'].numGlyphs = len(t.getGlyphOrder())


def desenha(fonte, ch, transf=None, smear=0):
    gs = fonte.getGlyphSet(); gn = nome_de(fonte, ch)
    if not gn: raise KeyError(ch)
    rec = DecomposingRecordingPen(gs); gs[gn].draw(rec)
    tp = TTGlyphPen(None)
    passos = [transf] if not smear else [transf, (transf or Transform()).translate(smear, 0)]
    for tr in passos:
        rec.replay(TransformPen(tp, tr) if tr else tp)
    return tp.glyph(), fonte['hmtx'][gn][0]


def gira(t, origem, destino):
    gs = t.getGlyphSet(); gn = nome_de(t, origem)
    bp = BoundsPen(gs); gs[gn].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    alt = getattr(t['OS/2'], 'sxHeight', 500) or 500
    tr = Transform(-1, 0, 0, -1, x0 + x1, alt * 0.52)
    rec = DecomposingRecordingPen(gs); gs[gn].draw(rec)
    tp = TTGlyphPen(None); rec.replay(TransformPen(tp, tr))
    registra(t, destino, tp.glyph(), t['hmtx'][gn][0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('doador'); ap.add_argument('destino')
    ap.add_argument('--chars', default='')
    ap.add_argument('--inclinar', type=float, default=0.0)
    ap.add_argument('--engrossar', type=int, default=0)
    ap.add_argument('--girar', default='')
    ap.add_argument('--saida', required=True)
    a = ap.parse_args()

    doador = TTFont(a.doador, fontNumber=0)
    alvo = TTFont(a.destino, fontNumber=0)
    feitos, falhas = [], []

    tr = (Transform(1, 0, math.tan(math.radians(-a.inclinar)), 1, 0, 0)
          if a.inclinar else None)
    for ch in a.chars:
        try:
            g, w = desenha(doador, ch, tr, a.engrossar)
            registra(alvo, ch, g, w + (a.engrossar * 2 // 3 if a.engrossar else 0))
            feitos.append(ch)
        except Exception as e:
            falhas.append('%s: %s' % (ch, e))

    for par in filter(None, a.girar.split(',')):
        destino, origem = par.split(':')
        try:
            gira(alvo, origem, destino); feitos.append(destino)
        except Exception as e:
            falhas.append('%s: %s' % (destino, e))

    alvo.save(a.saida)
    print(json.dumps(dict(saida=a.saida, doados=''.join(feitos), falhas=falhas),
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
