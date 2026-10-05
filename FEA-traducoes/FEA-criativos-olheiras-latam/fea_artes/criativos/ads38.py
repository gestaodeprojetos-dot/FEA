#!/usr/bin/env python3
"""Ads 38 (Feed; Story se o original estiver em trabalho/) · Ebook Olheiras LATAM. Troca só a copy.

Rodar a partir de fea_artes/:  python3 criativos/ads38.py
Originais: trabalho/Jads38-feed.png (e trabalho/Jads38-story.png quando baixado).
Tablets com capa e página do ebook em PT NÃO são tocados: fase 2.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_ads36a40 import *  # noqa

AQ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCO = lambda r, g, b: (np.minimum(np.minimum(r, g), b) > 170) & ((np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 45)
OURO = lambda r, g, b: (r > 140) & ((r - b) > 50) & (g > 90)
TEXTO = lambda r, g, b: BRANCO(r, g, b) | OURO(r, g, b)
APAGAR_HL = lambda r, g, b: (r + g + b) > 300
CLARO = lambda r, g, b: (r + g + b) > 500
ESC_CTA = lambda r, g, b: (r + g + b) < 300
ESC_CTA_APAGAR = lambda r, g, b: (r + g + b) < 430
ESC_SELO = lambda r, g, b: (r + g + b) < 330

HL_PT = ['Não é mais um', 'curso de olheiras.', 'É um protocolo', 'pronto para copiar', 'na próxima paciente.']
HL_ES = ['No es otro curso', 'de ojeras.', 'Es un protocolo listo', 'para copiar con su', 'próxima paciente.']
CHK_PT = ['Qual cânula usar', 'Quando fazer bolus', 'Onde evitar volume', 'Como reduzir edema', 'Produtos e planos ideais']
CHK_ES = ['Qué cánula usar', 'Cuándo hacer un bolo', 'Dónde evitar volumen', 'Cómo reducir el edema', 'Productos y planos ideales']


def ads38(arq, P):
    im = abrir(os.path.join(AQ, 'trabalho', arq))
    # ---------- título (2 linhas brancas + 3 douradas, alinhado à esquerda) ----------
    linhas = P['hl']  # [(y_topo, y_base_caixa, x0, x1, cond)] medidas no original
    xe = min(l[2] for l in linhas)
    ref = 3
    f = calibrar_larg(SERIF_SEMI, HL_PT[ref], linhas[ref][3] - linhas[ref][2] + 1)
    campos = [campo_cor(im, (l[2], l[0], l[3] + 1, l[1] + 1), l[4]) for l in linhas]
    for l in linhas:
        im = apagar(im, (l[2] - 12, l[0] - 8, l[3] + 12, l[1] + 10), APAGAR_HL, 4)
    for l, p, e, c in zip(linhas, HL_PT, HL_ES, campos):
        y = l[0] - f.getbbox(p)[1]
        assert xe + largura(f, e) <= P['hl_xmax'], (e, xe + largura(f, e))
        im = escrever_campo(im, e, f, xe - f.getbbox(e)[0], y, c)
    # ---------- checklist ----------
    lc = medir(im, P['chk'], CLARO)
    assert len(lc) == 5, lc
    fc = f0 = calibrar_larg(SANS_MED, CHK_PT[4], lc[4][3] - lc[4][2] + 1)
    xc = min(l[2] for l in lc)
    w = max(largura(fc, e) for e in CHK_ES)
    if xc + w > P['chk_xmax']:
        fc = ImageFont.truetype(SANS_MED, fc.size * (P['chk_xmax'] - xc) / w)
    print(arq, 'checklist fonte', round(fc.size, 2))
    cor = cor_texto(im, P['chk'], CLARO)
    for l in lc:
        im = apagar(im, (l[2] - 10, l[0] - 10, l[3] + 12, l[1] + 10), CLARO, 3)
    d = ImageDraw.Draw(im)
    for l, p, e in zip(lc, CHK_PT, CHK_ES):
        base = l[0] - f0.getbbox(p)[1] + f0.getmetrics()[0]       # linha de base original
        d.text((xc - fc.getbbox(e)[0], base - fc.getmetrics()[0]), e, font=fc, fill=cor)
    # ---------- CTA ----------
    im = trocar_cta(im, P['cta'], ESC_CTA, ESC_CTA_APAGAR, P['seta'], SANS_XBOLD, 'RECEBER ACESSO IMEDIATO',
                    'OBTENER ACCESO INMEDIATO', rotulo=arq)
    # ---------- selo ----------
    im, _ = tirar_acento_selo(im, P['selo'], ESC_SELO)
    return im


FEED = dict(hl=[(467, 550, 286, 1055, BRANCO), (587, 671, 288, 1196, BRANCO), (691, 817, 286, 1079, OURO),
                (831, 939, 284, 1274, OURO), (953, 1061, 285, 1392, OURO)], hl_xmax=1395,
            chk=(400, 1100, 1300, 1900), chk_xmax=1225,
            cta=(282, 2004, 1275, 2170), seta=1157, selo=(1630, 2050, 1730, 2077))

if __name__ == '__main__':
    print('ok', salvar(ads38('Jads38-feed.png', FEED), 'FEA-Ads 38 Feed - PTO-LATAM.png'))
    if os.path.exists(os.path.join(AQ, 'trabalho', 'Jads38-story.png')):
        raise SystemExit('Story do Ads 38 baixado: medir e incluir STORY aqui (layout do Story não foi medido).')
