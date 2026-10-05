#!/usr/bin/env python3
"""
Completa uma fonte embutida em PDF com os glifos que faltam para o espanhol,
sintetizando-os a partir dos glifos que a própria fonte já tem.

Por que existe: PDFs exportados de InDesign embutem apenas o SUBCONJUNTO de
glifos usado no idioma original. Um subconjunto português não tem ñ, ¿, ¡, «, »
nem travessão — então é impossível escrever espanhol com a fonte original, e
substituir a fonte muda a tipografia de todo o material.

Este script resolve mantendo a fonte: monta os glifos faltantes compondo os
existentes (ñ = n + til extraído de ã; travessão = meia-risca alongada;
« » = sinal de maior espelhado; • copiado do peso irmão).

Uso:
    python3 completar_fonte.py material.pdf --saida fontes/
    python3 completar_fonte.py material.pdf --relatorio     # só diagnostica
"""
import sys, io, os, json, argparse
from fontTools.cffLib import CFFFontSet
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.misc.transform import Transform

# caractere -> nome de glifo PostScript
CH2NOME = {'ñ':'ntilde','Ñ':'Ntilde','¿':'questiondown','¡':'exclamdown',
 '“':'quotedblleft','”':'quotedblright','–':'endash','-':'hyphen',
 'ü':'udieresis','Ü':'Udieresis','«':'guillemotleft','»':'guillemotright',
 '—':'emdash','•':'bullet','Ó':'Oacute','Í':'Iacute','Ú':'Uacute',
 'Á':'Aacute','É':'Eacute','?':'question','!':'exclam','’':'quoteright',
 'D':'D','J':'J','W':'W','X':'X','6':'six','9':'nine',',':'comma',';':'semicolon'}
DIGITOS = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five',
           '6':'six','7':'seven','8':'eight','9':'nine'}
CH2NOME.update(DIGITOS)
CH2NOME.update({c: c for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'})
NOME2CH = {v: k for k, v in CH2NOME.items()}

# receitas de síntese: glifo -> (tipo, parâmetros)
#   'acento'  : base + acento isolado de um glifo doador
#   'escala'  : doador transformado
#   'espelho' : doador espelhado horizontalmente
#   'duplo'   : doador repetido lado a lado
RECEITAS = {
 'ntilde':      ('acento', 'n', 'atilde', 'a'),
 'Ntilde':      ('acento', 'N', 'atilde', 'a'),
 'Oacute':      ('acento', 'O', 'oacute', 'o'),
 'Iacute':      ('acento', 'I', 'iacute', 'n'),   # 'n' dá a altura-x sem o pingo do i
 'Uacute':      ('acento', 'U', 'uacute', 'u'),
 'Aacute':      ('acento', 'A', 'aacute', 'a'),
 'Eacute':      ('acento', 'E', 'eacute', 'e'),
 'udieresis':   ('acento', 'u', None, None),      # trema montado de dois pontos
 'emdash':      ('largura_alvo', ['endash', 'hyphen'], 1000),  # 1 em, medido do doador
 'guillemotright':('duplo', 'greater', 0.58),
 'guillemotleft': ('espelho','guillemotright', None),
}

def carrega_subsets(pdf):
    """Extrai as fontes CFF embutidas, uma entrada por nome de base."""
    import pymupdf
    doc = pymupdf.open(pdf)
    out = {}
    for pg in range(doc.page_count):
        for f in doc[pg].get_fonts():
            xref, ext, typ, base, name, enc = f[:6]
            limpo = base.split('+')[-1]
            if limpo in out: continue
            try: nome, ext2, tp, buf = doc.extract_font(xref)
            except Exception: continue
            if not buf or ext2 != 'cff': continue
            out[limpo] = dict(base=base, buf=buf, xref=xref)
    return out

def abre_cff(buf):
    cff = CFFFontSet(); cff.decompile(io.BytesIO(buf), None)
    return cff, cff[cff.fontNames[0]]

def contornos(td, nome):
    """Grava os contornos de um glifo como lista de comandos de caneta."""
    cs = td.CharStrings[nome]
    rp = RecordingPen(); cs.draw(rp)
    return rp.value

def separa_acento(td, comAcento, semAcento):
    """Isola o contorno do acento: os contornos de 'ã' que não estão em 'a'.
    Critério: contorno cujo y mínimo fica acima do topo do glifo base."""
    base = contornos(td, semAcento)
    ys = [p[1] for cmd, args in base for p in (args or []) if isinstance(p, tuple)]
    topoBase = max(ys) if ys else 0
    todos = contornos(td, comAcento)
    # divide em contornos (cada moveTo abre um novo)
    grupos, atual = [], []
    for cmd, args in todos:
        if cmd == 'moveTo' and atual: grupos.append(atual); atual = []
        atual.append((cmd, args))
    if atual: grupos.append(atual)
    acento = []
    for g in grupos:
        ys = [p[1] for cmd, args in g for p in (args or []) if isinstance(p, tuple)]
        if ys and min(ys) >= topoBase * 0.92:
            acento.extend(g)
    return acento, topoBase

def desenha(pen, cmds, transform=None):
    alvo = TransformPen(pen, transform) if transform else pen
    for cmd, args in cmds:
        getattr(alvo, cmd)(*(args or ()))

def sintetiza(td, nome, glifosDisp, doadorBullet=None, externos=None, engrossar=0):
    """Monta o charstring de um glifo faltante. Devolve (charstring, largura)."""
    # doador de outro peso da mesma família, engrossado para casar com o negrito
    if externos and nome in externos and nome not in glifosDisp:
        cmds, larg = externos[nome]
        pen = T2CharStringPen(larg, None)
        if engrossar:
            e = engrossar
            for dx, dy in ((0,0), (e,0), (0,e), (e,e)):
                desenha(pen, cmds, Transform().translate(dx, dy))
        else:
            desenha(pen, cmds)
        return pen.getCharString(), larg

    if nome not in RECEITAS and nome != 'bullet': return None

    if nome == 'bullet':
        if not doadorBullet: return None
        cmds, larg = doadorBullet
        pen = T2CharStringPen(larg, None); desenha(pen, cmds)
        return pen.getCharString(), larg

    tipo = RECEITAS[nome][0]

    if tipo == 'acento':
        _, base, doador, doadorBase = RECEITAS[nome]
        if base not in glifosDisp: return None
        cmdsBase = contornos(td, base)
        ysB = [p[1] for c,a in cmdsBase for p in (a or []) if isinstance(p,tuple)]
        xsB = [p[0] for c,a in cmdsBase for p in (a or []) if isinstance(p,tuple)]
        largBase = td.CharStrings[base].width if hasattr(td.CharStrings[base],'width') else 500
        pen = T2CharStringPen(largBase, None)
        desenha(pen, cmdsBase)
        if nome == 'udieresis':
            # trema: dois pontos a partir de 'period', escalados
            if 'period' not in glifosDisp: return None
            pt = contornos(td, 'period')
            ysP=[p[1] for c,a in pt for p in (a or []) if isinstance(p,tuple)]
            xsP=[p[0] for c,a in pt for p in (a or []) if isinstance(p,tuple)]
            larguraPt = (max(xsP)-min(xsP)) if xsP else 100
            alturaBase = max(ysB) if ysB else 700
            cx = (min(xsB)+max(xsB))/2 if xsB else 250
            for dx in (-larguraPt*0.85, larguraPt*0.85):
                t = Transform().translate(cx+dx-(min(xsP)+max(xsP))/2,
                                          alturaBase*1.06-(min(ysP) if ysP else 0)).scale(0.95,0.95)
                desenha(pen, pt, t)
            return pen.getCharString(), largBase
        if doador not in glifosDisp or doadorBase not in glifosDisp: return None
        acento, topoDoador = separa_acento(td, doador, doadorBase)
        if not acento: return None
        ysA = [p[1] for c,a in acento for p in (a or []) if isinstance(p,tuple)]
        xsA = [p[0] for c,a in acento for p in (a or []) if isinstance(p,tuple)]
        # centraliza o acento sobre a base e assenta na altura da base
        cxA = (min(xsA)+max(xsA))/2; cxB = (min(xsB)+max(xsB))/2 if xsB else cxA
        alvoY = max(ysB) if ysB else topoDoador
        dy = alvoY - min(ysA) + (max(ysA)-min(ysA))*0.10
        maiuscula = base.isupper()
        esc = 1.0 if not maiuscula else 0.92
        t = Transform().translate(cxB-cxA*esc, dy if not maiuscula else dy*0.99).scale(esc, esc)
        desenha(pen, acento, t)
        return pen.getCharString(), largBase

    if tipo == 'largura_alvo':
        # alonga o doador até a largura desejada, preservando a espessura do traço
        _, doadores, alvo = RECEITAS[nome]
        for doador in doadores:
            if doador not in glifosDisp: continue
            cmds = contornos(td, doador)
            xs = [p[0] for c,a in cmds for p in (a or []) if isinstance(p, tuple)]
            larguraTinta = (max(xs) - min(xs)) if xs else 400
            fx = (alvo * 0.92) / larguraTinta        # 8% de folga lateral
            pen = T2CharStringPen(alvo, None)
            desenha(pen, cmds, Transform().translate(alvo*0.04, 0).scale(fx, 1.0))
            return pen.getCharString(), alvo
        return None

    if tipo == 'escala':
        _, doadores, fatores, fy = RECEITAS[nome]
        if isinstance(doadores, str): doadores, fatores = [doadores], [fatores]
        for doador, fx in zip(doadores, fatores):
            if doador not in glifosDisp: continue
            cmds = contornos(td, doador)
            larg = td.CharStrings[doador].width if hasattr(td.CharStrings[doador],'width') else 500
            pen = T2CharStringPen(int(larg*fx), None)
            desenha(pen, cmds, Transform().scale(fx, fy))
            return pen.getCharString(), int(larg*fx)
        return None

    if tipo == 'duplo':
        _, doador, esc = RECEITAS[nome]
        if doador not in glifosDisp: return None
        cmds = contornos(td, doador)
        xs=[p[0] for c,a in cmds for p in (a or []) if isinstance(p,tuple)]
        ys=[p[1] for c,a in cmds for p in (a or []) if isinstance(p,tuple)]
        larg1 = (max(xs)-min(xs)) if xs else 400
        # centro vertical do sinal, escalado, deve cair no meio da altura-x
        refs = [g for g in ('x','n','o','e') if g in glifosDisp]
        alturaX = 500
        if refs:
            cr = contornos(td, refs[0])
            yr = [p[1] for c,a in cr for p in (a or []) if isinstance(p,tuple)]
            if yr: alturaX = max(yr)
        cy = ((max(ys)+min(ys))/2) if ys else 250
        dy = alturaX/2 - cy*esc
        total = int(larg1*esc*2*1.20)
        pen = T2CharStringPen(total, None)
        for i in (0,1):
            t = Transform().translate(i*larg1*esc*1.08 + larg1*esc*0.06, dy).scale(esc, esc)
            desenha(pen, cmds, t)
        return pen.getCharString(), total

    if tipo == 'espelho':
        _, doador, _ = RECEITAS[nome]
        return None  # tratado em segunda passada
    return None

def reconstroi(td, faltantes, doadorBullet=None, psName='FonteCompleta', externos=None, engrossar=0):
    """Reconstrói a fonte com FontBuilder, incluindo os glifos sintetizados.
    O CFF do fontTools não aceita glifo novo no índice existente, então a rota
    correta é montar uma fonte nova a partir dos contornos — o que também rende
    um cmap real, necessário para qualquer renderizador usar a fonte."""
    from fontTools.fontBuilder import FontBuilder
    from fontTools.agl import toUnicode
    from fontTools.cffLib import PrivateDict

    # todo charstring precisa de um PrivateDict já ao ser criado: desenhar um
    # charstring sem private falha na leitura da largura (nominalWidthX)
    priv = PrivateDict(); priv.nominalWidthX = 0; priv.defaultWidthX = 0

    disp = set(td.charset)
    larguraDe = lambda g: (td.CharStrings[g].width
                           if hasattr(td.CharStrings[g], 'width') and td.CharStrings[g].width
                           else 500)

    # 1) glifos originais, redesenhados para normalizar
    charstrings, larguras = {}, {}
    for g in td.charset:
        try:
            cmds = contornos(td, g); larg = larguraDe(g)
            pen = T2CharStringPen(larg, None); desenha(pen, cmds)
            cs = pen.getCharString(); cs.private = priv
            charstrings[g] = cs; larguras[g] = larg
        except Exception:
            continue

    # 2) glifos sintetizados
    criados = []
    for nome in faltantes:
        if nome in charstrings: continue
        try:
            r = sintetiza(td, nome, disp, doadorBullet, externos, engrossar)
        except Exception:
            r = None
        if r:
            cs, larg = r
            cs.private = priv
            charstrings[nome] = cs; larguras[nome] = larg
            disp.add(nome); criados.append(nome)
    # espelhados, que dependem do par
    for nome in faltantes:
        if nome in charstrings: continue
        if RECEITAS.get(nome, (None,))[0] != 'espelho': continue
        _, doador, _ = RECEITAS[nome]
        if doador not in charstrings: continue
        cmds = contornos(td, doador) if doador in td.charset else None
        if cmds is None:
            rp = RecordingPen(); charstrings[doador].draw(rp); cmds = rp.value
        xs = [p[0] for c,a in cmds for p in (a or []) if isinstance(p, tuple)]
        larg = larguras.get(doador, 500)
        pen = T2CharStringPen(larg, None)
        desenha(pen, cmds, Transform().translate((max(xs)+min(xs)) if xs else 0, 0).scale(-1,1))
        cs = pen.getCharString(); cs.private = priv
        charstrings[nome] = cs; larguras[nome] = larg
        criados.append(nome)

    if '.notdef' not in charstrings:
        pen = T2CharStringPen(500, None); pen.moveTo((0,0)); pen.closePath()
        cs = pen.getCharString(); cs.private = priv
        charstrings['.notdef'] = cs; larguras['.notdef'] = 500

    ordem = ['.notdef'] + [g for g in charstrings if g != '.notdef']

    # 3) cmap: nome de glifo -> unicode
    cmap = {}
    for g in ordem:
        if g == '.notdef': continue
        u = NOME2CH.get(g)
        if u is None:
            try:
                uni = toUnicode(g)
                u = uni if len(uni) == 1 else None
            except Exception:
                u = None
        if u: cmap[ord(u)] = g

    fb = FontBuilder(1000, isTTF=False)
    fb.setupGlyphOrder(ordem)
    fb.setupCharacterMap(cmap)
    fb.setupCFF(psName, {'FullName': psName, 'FamilyName': psName, 'Weight': 'Regular'},
                charstrings, {})
    fb.setupHorizontalMetrics({g: (larguras.get(g,500), 0) for g in ordem})
    fb.setupHorizontalHeader(ascent=780, descent=-220)
    fb.setupNameTable({'familyName': psName, 'styleName': 'Regular',
                       'psName': psName, 'fullName': psName})
    fb.setupOS2(sTypoAscender=780, sTypoDescender=-220, usWinAscent=980, usWinDescent=250)
    fb.setupPost()
    contornosOut = {g: (RecordingPen(), larguras.get(g,500)) for g in ()}
    return fb.font, criados, cmap

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--saida', default='fontes_completas')
    ap.add_argument('--precisa', default='ñÑ¿¡üÜ«»—•ÓÍÚÁÉ?!DJWX69,;',
                    help='caracteres que o espanhol precisa')
    ap.add_argument('--relatorio', action='store_true')
    a = ap.parse_args()

    subs = carrega_subsets(a.pdf)
    precisa = {CH2NOME[c] for c in a.precisa if c in CH2NOME}
    os.makedirs(a.saida, exist_ok=True)
    resumo = {}

    # doador de bullet: qualquer subset da família que já o tenha
    doadorBullet = None
    for nome, info in subs.items():
        cff, td = abre_cff(info['buf'])
        if 'bullet' in td.charset:
            larg = td.CharStrings['bullet'].width if hasattr(td.CharStrings['bullet'],'width') else 400
            doadorBullet = (contornos(td,'bullet'), larg); break

    # ordem: pesos Regular antes dos Bold, para que o Regular sirva de doador
    def prioridade(kv):
        n = kv[0].lower()
        return (0 if ('regular' in n and 'it' not in n) else 1 if 'bold' in n else 2, n)

    doadoresFamilia = {}   # familia -> {glifo: (cmds, largura)}
    for nome, info in sorted(subs.items(), key=prioridade):
        cff, td = abre_cff(info['buf'])
        antes = set(td.charset)
        falta = sorted(precisa - antes)
        familia = nome.split('-')[0]
        ext = None; eng = 0
        if 'Bold' in nome and familia in doadoresFamilia:
            ext = doadoresFamilia[familia]
            eng = 16          # engrossamento em unidades de 1000/em
        elif familia not in doadoresFamilia:
            # guarda os contornos deste peso para servir de doador aos irmãos
            doadoresFamilia[familia] = {
                g: (contornos(td, g),
                    td.CharStrings[g].width if hasattr(td.CharStrings[g],'width') and td.CharStrings[g].width else 500)
                for g in td.charset if g != '.notdef'}
        if a.relatorio:
            resumo[nome] = dict(glifos=len(antes), falta=[NOME2CH.get(g,g) for g in falta])
            continue
        dest = os.path.join(a.saida, nome + '.otf')
        try:
            ft, criados, cmap = reconstroi(td, falta, doadorBullet, psName=nome.replace('-','')+'ES',
                                           externos=ext, engrossar=eng)
            ft.save(dest)
            naoFeitos = [g for g in falta if g not in criados]
            resumo[nome] = dict(glifos_antes=len(antes), glifos_depois=len(cmap),
                                criados=[NOME2CH.get(g,g) for g in criados],
                                nao_sintetizaveis=[NOME2CH.get(g,g) for g in naoFeitos],
                                arquivo=dest)
        except Exception as e:
            resumo[nome] = dict(glifos_antes=len(antes), erro='%s: %s'%(type(e).__name__, e))

    print(json.dumps(resumo, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
