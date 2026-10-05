#!/usr/bin/env python3
"""Ads 40 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Rodar a partir de fea_artes/:  python3 criativos/ads40.py
Originais: trabalho/Jads40-feed.png, trabalho/Jads40-story.png (Drive BR).
Preço: lido de precos.json (PRECOS['preco']); se for número (ex.: 'US$19,00') o
inteiro sai grande e os centavos sobrescritos, como no original; se for o
placeholder 'US$ [PRECIO]', o texto é ajustado à largura do cartão.
O Story é o mesmo layout do Feed deslocado 722 px para baixo.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads36a40 import *  # noqa

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLARO = lambda r, g, b: (r + g + b) > 450
CLARO_APAGAR = lambda r, g, b: (r + g + b) > 200
OURO = lambda r, g, b: (r > 150) & (r - b > 40)
OURO_APAGAR = lambda r, g, b: (r > 70) & (r - b > 20)
CORPO = lambda r, g, b: (r + g + b) > 400
ESC_CTA = lambda r, g, b: (r + g + b) < 300
ESC_CTA_APAGAR = lambda r, g, b: (r + g + b) < 430
ESC_SELO = lambda r, g, b: (r + g + b) < 330

HL_PT = ['Acesso vitalício', 'por apenas']
HL_ES = ['Acceso de por vida', 'por solo']
BD_PT = ['Copie o protocolo tridimensional', 'de olheiras utilizado por mais de', '30 mil profissionais.']
BD_ES = ['Copie el protocolo tridimensional', 'de ojeras con más de 30 mil', 'copias vendidas.']

# medidas do Feed (Story = +722 em y)
HL = [(695, 812, 511, 1643), (892, 1012, 672, 1485)]
PRECO_R = (647, 1109, 811, 1228)     # 'R$'
PRECO_INT = (861, 1095, 1300, 1408)  # '97'
PRECO_DEC = (1327, 1114, 1515, 1238)  # ',00'
CARTAO_X = (339, 1821)               # cartão escuro
BD = (380, 1490, 1780, 1800)
CTA = (510, 1852, 1652, 2018)
SETA = 1509
SELO = (365, 428, 482, 455)


def preco(im, dy):
    S = lambda c: (c[0], c[1] + dy, c[2], c[3] + dy)
    r, it, dc = S(PRECO_R), S(PRECO_INT), S(PRECO_DEC)
    c_r, c_i, c_d = (campo_cor(im, (c[0], c[1], c[2] + 1, c[3] + 1), OURO) for c in (r, it, dc))
    f_r = calibrar_altura(SERIF_SEMI, 'R', 102)
    f_i = calibrar_altura(SERIF_BOLD, '9', it[3] - it[1])
    f_d = calibrar_altura(SERIF_SEMI, '0', 104)
    topo_r, topo_d = r[1] + 6, dc[1]                       # topo da maiúscula 'R' e dos zeros
    base_i = it[3] - (f_i.getbbox('9', anchor='ls')[3])    # linha de base dos dígitos grandes
    cx = (r[0] + dc[2]) / 2
    for c in (r, it, dc):
        im = apagar(im, (c[0] - 12, c[1] - 12, c[2] + 12, c[3] + 12), OURO_APAGAR, 5)
    txt = PRECOS['preco'].strip()
    m = re.match(r'^(\D*?)\s*(\d+)(?:([.,])(\d+))?$', txt)
    if m:
        moeda, inteiro, sep, dec = m.group(1).strip(), m.group(2), m.group(3) or '', m.group(4) or ''
        sup = (sep + dec) if dec else ''
    else:  # placeholder, ex. 'US$ [PRECIO]'
        mm = re.match(r'^(\S*\$)\s*(.*)$', txt)
        moeda, inteiro, sup = (mm.group(1), mm.group(2), '') if mm else ('', txt, '')
    gap1 = (it[0] - r[2])                                   # espaço moeda -> inteiro
    gap2 = (dc[0] - it[2])
    larg_max = CARTAO_X[1] - CARTAO_X[0] - 2 * 110
    fi = f_i
    while True:
        wm = largura(f_r, moeda) if moeda else 0
        wi = largura(fi, inteiro)
        wd = largura(f_d, sup) if sup else 0
        total = wm + (gap1 if moeda else 0) + wi + (gap2 if sup else 0) + wd
        if total <= larg_max or fi.size < 40:
            break
        fi = F(SERIF_BOLD, fi.size - 1)
    x = cx - total / 2
    if moeda:
        L = mascara_texto(im.size, [(x - f_r.getbbox(moeda)[0], topo_r - f_r.getbbox('R')[1])], f_r, 0) if False else None
        L = Image.new('L', im.size, 0)
        ImageDraw.Draw(L).text((x - f_r.getbbox(moeda)[0], topo_r - f_r.getbbox('R')[1]), moeda, font=f_r, fill=255)
        im = pintar_mascara(im, L, campo=c_r, caixa_campo=L.getbbox())
        x += wm + gap1
    L = Image.new('L', im.size, 0)
    if fi.size == f_i.size:
        ImageDraw.Draw(L).text((x - fi.getbbox(inteiro)[0], base_i), inteiro, font=fi, fill=255, anchor='ls')
    else:  # texto reduzido (placeholder): centrado na altura dos dígitos originais
        bb = fi.getbbox(inteiro, anchor='ls')
        yb = (it[1] + it[3]) / 2 - (bb[1] + bb[3]) / 2
        ImageDraw.Draw(L).text((x - fi.getbbox(inteiro)[0], yb), inteiro, font=fi, fill=255, anchor='ls')
    im = pintar_mascara(im, L, campo=c_i, caixa_campo=L.getbbox())
    x += wi + gap2
    if sup:
        L = Image.new('L', im.size, 0)
        ImageDraw.Draw(L).text((x - f_d.getbbox(sup)[0], topo_d - f_d.getbbox('0')[1]), sup, font=f_d, fill=255)
        im = pintar_mascara(im, L, campo=c_d, caixa_campo=L.getbbox())
    print('preço:', repr(txt), '-> moeda', repr(moeda), 'valor', repr(inteiro), 'centavos', repr(sup), 'fonte', fi.size)
    return im


def ads40(arq, dy):
    im = abrir(os.path.join(AQ, 'trabalho', arq))
    W = im.width
    S = lambda c: (c[0], c[1] + dy, c[2], c[3] + dy)
    # ---------- título branco ----------
    hl = [(a + dy, b + dy, c, d) for a, b, c, d in HL]
    cor = cor_texto(im, (hl[0][2], hl[0][0], hl[0][3], hl[0][1]), CLARO)
    f = calibrar_larg(SERIF_SEMI, HL_PT[0], hl[0][3] - hl[0][2] + 1)
    for l in hl:
        im = apagar(im, (l[2] - 12, l[0] - 10, l[3] + 12, l[1] + 10), CLARO_APAGAR, 4)
    cx = (CARTAO_X[0] + CARTAO_X[1]) / 2
    d = ImageDraw.Draw(im)
    for l, p, e in zip(hl, HL_PT, HL_ES):
        base = l[0] - f.getbbox(p)[1] + f.getmetrics()[0]
        assert largura(f, e) < CARTAO_X[1] - CARTAO_X[0] - 160, e
        d.text((cx - largura(f, e) / 2 - f.getbbox(e)[0], base - f.getmetrics()[0]), e, font=f, fill=cor)
    # ---------- preço ----------
    im = preco(im, dy)
    # ---------- corpo ----------
    bd = medir(im, S(BD), CORPO)
    assert len(bd) == 3, bd
    fb = calibrar_larg(SANS_REG, BD_PT[0], bd[0][3] - bd[0][2] + 1)
    corb = cor_texto(im, S(BD), CORPO)
    cxb = (bd[0][2] + bd[0][3]) / 2
    for l in bd:
        im = apagar(im, (l[2] - 10, l[0] - 10, l[3] + 10, l[1] + 10), CLARO_APAGAR, 3)
    d = ImageDraw.Draw(im)
    for l, p, e in zip(bd, BD_PT, BD_ES):
        d.text((cxb - largura(fb, e) / 2 - fb.getbbox(e)[0], l[0] - fb.getbbox(p)[1]), e, font=fb, fill=corb)
    # ---------- CTA ----------
    im = trocar_cta(im, S(CTA), ESC_CTA, ESC_CTA_APAGAR, SETA, SANS_XBOLD, 'GARANTIR MEU ACESSO AGORA',
                    'QUIERO MI ACCESO AHORA', rotulo=arq)
    # ---------- selo ----------
    im, _ = tirar_acento_selo(im, S(SELO), ESC_SELO)
    return im


if __name__ == '__main__':
    for arq, dy, nome in [('Jads40-feed.png', 0, 'FEA-Ads 40 Feed - PTO-LATAM.png'),
                          ('Jads40-story.png', 722, 'FEA-Ads 40 Story - PTO-LATAM.png')]:
        print('ok', salvar(ads40(arq, dy), nome))
