# -*- coding: utf-8 -*-
"""Funde os subconjuntos embutidos de cada familia num unico arquivo.

Um PDF diagramado embute UM SUBCONJUNTO POR TRECHO: a mesma familia aparece
varias vezes, cada copia com as letras de algumas paginas. Extrair uma copia da
uma fonte quase vazia. Este script funde todas as copias de cada familia,
importando de uma para a outra os glifos que faltam.

Subconjunto Type0/Identity-H nao traz cmap: o mapa caractere -> glifo vem do
ToUnicode do proprio PDF.

Uso:
    python3 fundir_subconjuntos.py material.pdf --saida fontes/
    python3 fundir_subconjuntos.py material.pdf --saida fontes/ --familias HelveticaNeue
"""
import pymupdf, io, os, sys, re, json, argparse, collections
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen


def tounicode(xref):
    k = doc.xref_get_key(xref, 'ToUnicode')
    if k[0] != 'xref': return {}
    n = int(k[1].split()[0])
    s = doc.xref_stream(n).decode('latin-1')
    m = {}
    for bloco in re.findall(r'beginbfchar(.*?)endbfchar', s, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', bloco):
            if len(b) != 4: continue          # ignora ligaduras fi/fl
            m[int(a, 16)] = int(b, 16)        # gid -> unicode
    for bloco in re.findall(r'beginbfrange(.*?)endbfrange', s, re.S):
        for ini, fim, base in re.findall(
                r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', bloco):
            if len(base) != 4: continue
            for d in range(int(fim, 16) - int(ini, 16) + 1):
                m[int(ini, 16) + d] = int(base, 16) + d
    return m

def coleta():
    subsets = collections.defaultdict(list)
    vistos = set()
    for i in range(doc.page_count):
        for f in doc.get_page_fonts(i, full=True):
            xref, base = f[0], f[3].split('+')[-1]
            if xref in vistos: continue
            vistos.add(xref)
            try: nome, ex, tp, buf = doc.extract_font(xref)
            except Exception: continue
            if buf: subsets[base].append((xref, buf))
    return subsets

def tem_contorno(t, gn):
    try: return t['glyf'][gn].numberOfContours != 0
    except Exception: return False

def unis(t, xref):
    out = {}
    cm = t.getBestCmap() if 'cmap' in t else None
    if cm:
        pares = cm.items()
    else:
        go = t.getGlyphOrder()
        pares = [(u, go[g]) for g, u in tounicode(xref).items() if g < len(go)]
    for cp, gn in pares:
        if tem_contorno(t, gn): out[cp] = gn
    return out

def funde(base, subsets, saida):
    fonts = []
    for xref, buf in subsets.get(base, []):
        try:
            t = TTFont(io.BytesIO(buf), fontNumber=0)
            if 'glyf' not in t: continue
            fonts.append((t, unis(t, xref), xref))
        except Exception: continue
    if not fonts: return dict(base=base, erro='sem TTF utilizavel')
    fonts.sort(key=lambda x: (-(('cmap' in x[0]) * 10000 + len(x[1]))))
    alvo, tem, _ = fonts[0]
    go = set(alvo.getGlyphOrder()); novos = []
    for t, mapa, _x in fonts[1:]:
        gsO = t.getGlyphSet()
        for cp, gn in mapa.items():
            if cp in tem: continue
            destino = 'uni%04X' % cp
            while destino in go: destino += 'x'
            rec = DecomposingRecordingPen(gsO); gsO[gn].draw(rec)
            tp = TTGlyphPen(None); rec.replay(tp)
            alvo['glyf'][destino] = tp.glyph()
            alvo['hmtx'][destino] = (t['hmtx'][gn][0], 0)
            for tb in alvo['cmap'].tables:
                if tb.isUnicode(): tb.cmap[cp] = destino
            tem[cp] = destino; go.add(destino); novos.append(chr(cp))
    alvo['maxp'].numGlyphs = len(alvo.getGlyphOrder())
    arq = os.path.join(saida, '%s.ttf' % base.replace('/', '_'))
    alvo.save(arq)
    return dict(base=base, subconjuntos=len(fonts), codepoints=len(tem),
                importados=''.join(sorted(novos)), arquivo=arq)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('--saida', default='fontes')
    ap.add_argument('--familias', default='')
    a = ap.parse_args()
    global doc
    doc = pymupdf.open(a.pdf)
    subsets = coleta()
    os.makedirs(a.saida, exist_ok=True)
    alvos = a.familias.split(',') if a.familias else sorted(subsets)
    print(json.dumps([funde(b, subsets, a.saida) for b in alvos],
                     ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
