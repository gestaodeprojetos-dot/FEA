#!/usr/bin/env python3
"""Ads 39 (Feed e Story) · Ebook Olheiras LATAM. Troca só a copy.

Rodar a partir de fea_artes/:  python3 criativos/ads39.py
Originais: trabalho/Jads39-feed.png, trabalho/Jads39-story.png (Drive BR).
Faixa de mockups do ebook (capa e páginas em PT, QR Codes) NÃO é tocada: fase 2.
O 'olheiras' gigante e quase transparente do fundo vira 'ojeras' (ver marca_dagua()).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads36a40 import *  # noqa

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYFAIR = fonte('PlayfairDisplay_600SemiBold')
ESC = lambda r, g, b: (r + g + b) < 250
OURO = lambda r, g, b: (r > 150) & ((r - b) > 60)
TIT = lambda r, g, b: ((r + g + b) < 300) | (((r - b) > 60) & (r > 120))
TIT_APAGAR = lambda r, g, b: ((r + g + b) < 600) | ((r - b) > 25)
ESC_APAGAR = lambda r, g, b: (r + g + b) < 600
OURO_CTA = lambda r, g, b: (r > 150) & (r - b > 70)
OURO_CTA_APAGAR = lambda r, g, b: (r > 90) & (r - b > 35)

SUB_PT, SUB_ES = 'O ebook mostra exatamente:', 'El ebook muestra exactamente:'
IT_PT = ['Onde entrar', 'Profundidade correta', 'Produto ideal para cada plano']
IT_ES = ['Dónde entrar', 'La profundidad correcta', 'El producto ideal para cada plano']


def ads39(arq, P):
    im = abrir(os.path.join(AQ, 'trabalho', arq))
    W = im.width
    # ---------- título ----------
    l1, l2 = P['hl']
    cor_esc = cor_texto(im, (l1[2], l1[0], l1[3], l1[1]), ESC)
    g0, g1 = P['ouro_x']
    campo = campo_cor(im, (g0, l2[0], g1 + 1, l2[1] + 1), OURO)
    f = calibrar_larg(SERIF_SEMI, 'A maioria das complicações', l1[3] - l1[2] + 1)
    fp = calibrar_larg(PLAYFAIR, 'começa aqui', g1 - g0 + 1)
    base1 = l1[0] - f.getbbox('A maioria das complicações')[1] + f.getmetrics()[0]
    base2 = l2[0] - f.getbbox('em olheiras')[1] + f.getmetrics()[0]
    for l in (l1, l2):
        im = apagar_liso(im, (l[2] - 14, l[0] - 30, l[3] + 14, l[1] + 34), TIT_APAGAR, 4)
    # escala única para as duas linhas caberem na largura útil
    t1 = 'La mayoría de las complicaciones'
    a, b, c = 'en ojeras ', 'empieza aquí', '.'
    w2 = lambda f_, fp_: f_.getlength(a) + fp_.getlength(b) + f_.getlength(c)
    esc = min(1, P['larg_max'] / largura(f, t1), P['larg_max'] / w2(f, fp))
    assert esc >= 0.85, esc
    fn, fpn = F(SERIF_SEMI, f.size * esc), F(PLAYFAIR, fp.size * esc)
    print(arq, 'título escala %.3f' % esc)
    cx = W / 2
    d = ImageDraw.Draw(im)
    d.text((cx - largura(fn, t1) / 2 - fn.getbbox(t1)[0], base1 - fn.getmetrics()[0]), t1, font=fn, fill=cor_esc)
    x = cx - w2(fn, fpn) / 2
    yb = base2
    d.text((x, yb), a, font=fn, fill=cor_esc, anchor='ls')
    x += fn.getlength(a)
    L = Image.new('L', im.size, 0)
    ImageDraw.Draw(L).text((x, yb), b, font=fpn, fill=255, anchor='ls')
    im = pintar_mascara(im, L, campo=campo, caixa_campo=L.getbbox())
    x += fpn.getlength(b)
    ImageDraw.Draw(im).text((x, yb), c, font=fn, fill=cor_esc, anchor='ls')
    # ---------- subtítulo ----------
    sub = medir(im, P['sub'], ESC)[0]
    fs = calibrar_larg(SANS_BOLD, SUB_PT, sub[3] - sub[2] + 1)
    cor = cor_texto(im, P['sub'], ESC)
    im = apagar_liso(im, (sub[2] - 10, sub[0] - 12, sub[3] + 10, sub[1] + 14), ESC_APAGAR, 3)
    ys = sub[0] - fs.getbbox(SUB_PT)[1]
    ImageDraw.Draw(im).text((W / 2 - largura(fs, SUB_ES) / 2 - fs.getbbox(SUB_ES)[0], ys), SUB_ES, font=fs, fill=cor)
    # ---------- itens (texto à direita de cada ícone, mesmo x inicial) ----------
    segs = P['itens']  # [(y0, y1, x0, x1)] por item, medidos no original
    fi = calibrar_larg(SANS_REG, IT_PT[2], segs[2][3] - segs[2][2] + 1)
    cori = cor_texto(im, (segs[2][2], segs[2][0], segs[2][3], segs[2][1]), ESC)
    for (y0, y1, x0, x1) in segs:
        im = apagar_liso(im, (x0 - 10, y0 - 12, x1 + 12, y1 + 14), ESC_APAGAR, 3)
    d = ImageDraw.Draw(im)
    for (y0, y1, x0, x1), p, e, lim in zip(segs, IT_PT, IT_ES, P['itens_xmax']):
        assert x0 + largura(fi, e) <= lim, (e, x0 + largura(fi, e), lim)
        d.text((x0 - fi.getbbox(e)[0], y0 - fi.getbbox(p)[1]), e, font=fi, fill=cori)
    # ---------- CTA ----------
    im = trocar_cta(im, P['cta'], OURO_CTA, OURO_CTA_APAGAR, P['seta'], SANS_XBOLD, 'VER PROTOCOLO COMPLETO',
                    'VER EL PROTOCOLO COMPLETO', rotulo=arq)
    # ---------- marca d'água 'olheiras' -> 'ojeras' ----------
    if P['marca']['tam']:
        im = marca_dagua(im, P['marca'], P.get('marca_excluir'))
    return im


def marca_dagua(im, M, excluir=None):
    """'olheiras' gigante, desfocado e quase transparente (mais claro que o fundo cinza).
    1) fundo estimado por abertura morfológica (remove estruturas claras finas) + desfoque;
    2) marca = imagem - fundo, só onde o modelo do 'olheiras' original (fonte, tamanho,
       base e desfoque ajustados ao original) tem letra; intensidade medida linha a linha;
    3) a marca é subtraída e 'ojeras' entra com a mesma fonte, tamanho, linha de base,
       desfoque e intensidade, centrado. Botão escuro do CTA fica fora (está na frente).
    Só operações clássicas sobre os pixels do próprio original."""
    x0, y0, x1, y1 = M['caixa']
    a = np.array(im).astype(np.float32)
    reg = a[y0:y1, x0:x1].copy()
    lum = reg.mean(2)
    h, w = lum.shape
    ign = cv2.dilate((lum < 120).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
    lum_f = lum.copy()
    lum_f[ign] = 255
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (201, 201))
    fundo = cv2.GaussianBlur(cv2.dilate(cv2.erode(lum_f, ker), ker), (0, 0), 25)
    marca = np.clip(lum - fundo, 0, None)
    marca[ign] = 0
    f = F(fonte(M['fonte']), M['tam'])

    def render(t, x):
        L = Image.new('L', (w, h), 0)
        ImageDraw.Draw(L).text((x, M['base'] - y0), t, font=f, fill=255, anchor='ls')
        return cv2.GaussianBlur(np.array(L).astype(np.float32) / 255, (0, 0), M['desfoque'])

    velho = render('olheiras', M['x'])
    num, den = (marca * velho).sum(1), (velho * velho).sum(1)
    A = np.where(den > 1, num / np.maximum(den, 1e-6), np.nan)
    ok = ~np.isnan(A)
    A = np.interp(np.arange(h), np.where(ok)[0], A[ok])
    A = cv2.GaussianBlur(A.reshape(-1, 1).astype(np.float32), (0, 0), 12).ravel()
    zona = np.clip(cv2.GaussianBlur(velho, (0, 0), M['desfoque']) / 0.05, 0, 1)
    zona[ign] = 0
    reg -= (marca * zona)[..., None]
    t = 'ojeras'
    novo = render(t, w / 2 - largura(f, t) / 2 - f.getbbox(t)[0]) * A[:, None]
    novo[ign] = 0
    reg += novo[..., None]
    a[y0:y1, x0:x1] = reg
    print('marca d\'água: intensidade média %.1f' % float(np.median(A[ok])) if ok.any() else '')
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8))


FEED = dict(hl=[(222, 341, 265, 1889), (352, 444, 344, 1813)], ouro_x=(1063, 1787), larg_max=1840,
            sub=(300, 1610, 1900, 1710),
            itens=[(1783, 1827, 561, 898), (1783, 1827, 1135, 1723), (1930, 1987, 733, 1565)],
            itens_xmax=[975, 2000, 2000],
            cta=(464, 2066, 1694, 2260), seta=1514,
            marca=dict(caixa=(0, 2262, 2160, 2700), kernel=None, suave=None, tam=None, base=None, desfoque=None, intens=None))
STORY = dict(hl=[(698, 817, 265, 1889), (828, 920, 344, 1813)], ouro_x=(1063, 1787), larg_max=1840,
             sub=(300, 2140, 1900, 2240),
             itens=[(2334, 2386, 468, 867), (2334, 2386, 1146, 1842), (2507, 2575, 671, 1654)],
             itens_xmax=[960, 2050, 2050],
             cta=(355, 2670, 1806, 2899), seta=1594,
             marca=dict(caixa=(0, 2640, 2160, 3330), kernel=None, suave=None, tam=None, base=None, desfoque=None, intens=None),
             marca_excluir=(330, 2650, 1830, 2930))

if __name__ == '__main__':
    for arq, P, nome in [('Jads39-feed.png', FEED, 'FEA-Ads 39 Feed - PTO-LATAM.png'),
                         ('Jads39-story.png', STORY, 'FEA-Ads 39 Story - PTO-LATAM.png')]:
        print('ok', salvar(ads39(arq, P), nome))
