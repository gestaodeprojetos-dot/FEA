#!/usr/bin/env python3
"""
Completa fontes TrueType embutidas em PDF com os glifos que faltam para o
espanhol. Companheiro de completar_fonte.py, que trata as fontes CFF/Type1.

Por que separado: em CFF os contornos são cúbicos e a saída é OTF; em TrueType
são quadráticos e a saída é TTF. Misturar os dois num só caminho de canetas
corromperia os contornos.

Descoberta que motivou este script: **o cmap mente**. Nos subconjuntos gerados
pelo InDesign, glifos como ñ, ¿ e ¡ continuam listados no cmap mas com contorno
VAZIO. Medir cobertura pelo cmap dá falso positivo — a medida válida é «o glifo
tem contorno?».

Uso:
    python3 completar_fonte_ttf.py fontes/ --precisa 'éíúóáñ¿—’'
"""
import sys, os, json, argparse
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen, DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.fontBuilder import FontBuilder

# base + componente de acento solto (Helvetica embute 'acute' e 'tilde' soltos)
ACENTOS = {
 'é':('e','acute'), 'í':('dotlessi','acute'), 'ú':('u','acute'), 'ó':('o','acute'),
 'á':('a','acute'), 'É':('E','acute'), 'Í':('I','acute'), 'Ú':('U','acute'),
 'Ó':('O','acute'), 'Á':('A','acute'), 'ñ':('n','tilde'), 'Ñ':('N','tilde'),
 'ã':('a','tilde'), 'õ':('o','tilde'), 'ü':('u','dieresis'),
}
ROTACOES  = {'¿':'question', '¡':'exclam'}          # 180°, é a construção real
ALONGAR   = {'—':('hyphen', 1000), '–':('hyphen', 500)}
ELEVAR    = {'’':('comma', 0.62)}                    # vírgula erguida à altura-x

def contornos(gs, nome):
    """Decompõe componentes: glifo composto gravado como componente quebra a
    TTGlyphPen, que exige um glyphSet para validar a referência."""
    rp = DecomposingRecordingPen(gs); gs[nome].draw(rp); return rp.value

def vazio(gs, nome):
    try: return not contornos(gs, nome)
    except Exception: return True

def desenha(pen, cmds, t=None):
    alvo = TransformPen(pen, t) if t else pen
    for cmd, args in cmds:
        getattr(alvo, cmd)(*(args or ()))

def caixa(cmds):
    pts = [p for c, a in cmds for p in (a or []) if isinstance(p, tuple)]
    if not pts: return (0, 0, 0, 0)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))

def completa(caminho, precisa, saida):
    ft = TTFont(caminho)
    if 'glyf' not in ft: return dict(erro='não é TrueType')
    ordem = list(ft.getGlyphOrder())
    gs = ft.getGlyphSet()
    hmtx = ft['hmtx'].metrics
    upem = ft['head'].unitsPerEm

    # nome de glifo por caractere, e o que está de fato utilizável
    porChar = {}
    if 'cmap' in ft:
        for t in ft['cmap'].tables:
            for cp, gn in t.cmap.items(): porChar.setdefault(chr(cp), gn)
    else:
        # subconjunto sem cmap: deduz pelos nomes de glifo
        from fontTools.agl import toUnicode
        for gn in ordem:
            try: u = toUnicode(gn)
            except Exception: u = ''
            if len(u) == 1: porChar.setdefault(u, gn)
    util = {c for c, gn in porChar.items() if gn in gs and not vazio(gs, gn)}

    novos, criados, naoFeitos = {}, [], []
    def pega(nome):
        """contornos de um glifo pelo NOME, se tiver desenho"""
        return None if (nome not in gs or vazio(gs, nome)) else contornos(gs, nome)

    for ch in precisa:
        if ch in util: continue
        feito = None
        # 1) base + acento solto
        if ch in ACENTOS:
            bn, an = ACENTOS[ch]
            base = pega(bn) or (pega(porChar.get(bn.replace('dotless',''), '')) if 'dotless' in bn else None)
            ac = pega(an)
            if base and ac:
                bx0, by0, bx1, by1 = caixa(base); ax0, ay0, ax1, ay1 = caixa(ac)
                larg = hmtx.get(bn, (int(upem*0.5), 0))[0]
                pen = TTGlyphPen(None); desenha(pen, base)
                dx = (bx0+bx1)/2 - (ax0+ax1)/2
                dy = by1 - ay0 + upem*0.02
                if bn.isupper(): dy = by1 - ay0 + upem*0.01
                desenha(pen, ac, Transform().translate(dx, dy))
                feito = (pen.glyph(), larg)
        # 2) rotação de 180°: ¿ e ¡ são o ? e o ! girados
        if feito is None and ch in ROTACOES:
            src = pega(ROTACOES[ch])
            if src:
                x0, y0, x1, y1 = caixa(src)
                larg = hmtx.get(ROTACOES[ch], (int(upem*0.35), 0))[0]
                pen = TTGlyphPen(None)
                t = Transform().translate(x0+x1, y0+y1).scale(-1, -1)
                desenha(pen, src, t)
                feito = (pen.glyph(), larg)
        # 3) alongamento até a largura desejada
        if feito is None and ch in ALONGAR:
            gn, alvo = ALONGAR[ch]; src = pega(gn)
            if src:
                x0, y0, x1, y1 = caixa(src)
                fx = (alvo*upem/1000*0.92)/max(x1-x0, 1)
                pen = TTGlyphPen(None)
                desenha(pen, src, Transform().translate(upem*0.02, 0).scale(fx, 1))
                feito = (pen.glyph(), int(alvo*upem/1000))
        # 4) elevação: vírgula vira apóstrofo curvo
        if feito is None and ch in ELEVAR:
            gn, frac = ELEVAR[ch]; src = pega(gn)
            xref = pega('x') or pega('o')
            if src and xref:
                _, _, _, xh = caixa(xref); x0, y0, x1, y1 = caixa(src)
                pen = TTGlyphPen(None)
                desenha(pen, src, Transform().translate(0, xh - y0 + (xh*frac - xh)))
                feito = (pen.glyph(), hmtx.get(gn, (int(upem*0.28), 0))[0])
        if feito:
            gnNovo = 'uni%04X' % ord(ch)
            novos[gnNovo] = feito; criados.append(ch)
            porChar[ch] = gnNovo
        else:
            naoFeitos.append(ch)

    if not novos:
        return dict(criados=[], nao_sintetizaveis=naoFeitos, arquivo=None)

    # reconstrói: glifos originais com desenho + os novos
    glifos, larguras = {}, {}
    for gn in ordem:
        if gn in novos: continue
        try:
            cm = contornos(gs, gn)
        except Exception:
            cm = []
        pen = TTGlyphPen(None); desenha(pen, cm)
        glifos[gn] = pen.glyph(); larguras[gn] = (hmtx.get(gn, (0, 0))[0], hmtx.get(gn, (0, 0))[1])
    for gn, (gl, lg) in novos.items():
        glifos[gn] = gl; larguras[gn] = (lg, 0)

    cmapNovo = {ord(c): gn for c, gn in porChar.items() if gn in glifos}
    nomeFonte = os.path.splitext(os.path.basename(caminho))[0] + 'ES'
    fb = FontBuilder(upem, isTTF=True)
    fb.setupGlyphOrder(['.notdef'] + [g for g in glifos if g != '.notdef'])
    fb.setupCharacterMap(cmapNovo)
    fb.setupGlyf(glifos)
    fb.setupHorizontalMetrics(larguras)
    asc = ft['hhea'].ascent; desc = ft['hhea'].descent
    fb.setupHorizontalHeader(ascent=asc, descent=desc)
    fb.setupNameTable({'familyName': nomeFonte, 'styleName': 'Regular',
                       'psName': nomeFonte, 'fullName': nomeFonte})
    fb.setupOS2(sTypoAscender=asc, sTypoDescender=desc,
                usWinAscent=abs(asc), usWinDescent=abs(desc))
    fb.setupPost()
    fb.save(saida)
    return dict(criados=criados, nao_sintetizaveis=naoFeitos, arquivo=saida,
                glifos=len(glifos))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--precisa', default='éíúóáñÑÉÍÚÓÁ¿—’')
    ap.add_argument('--filtro', default='')
    a = ap.parse_args()
    res = {}
    for f in sorted(os.listdir(a.dir)):
        if not f.lower().endswith('.ttf'): continue
        if a.filtro and a.filtro not in f: continue
        if f.endswith('ES.ttf'): continue
        alvo = os.path.join(a.dir, os.path.splitext(f)[0] + 'ES.ttf')
        try:
            res[f] = completa(os.path.join(a.dir, f), a.precisa, alvo)
        except Exception as e:
            res[f] = dict(erro='%s: %s' % (type(e).__name__, e))
    print(json.dumps(res, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
