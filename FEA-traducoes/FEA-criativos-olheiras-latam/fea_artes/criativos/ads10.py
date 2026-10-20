#!/usr/bin/env python3
"""FEA · Ads 10 (Feed e Story) em espanhol LATAM. Troca só a copy.

Originais em trabalho/C-ads10-feed.png e trabalho/C-ads10-story.png (Drive Brasil).
Fonte identificada: Plus Jakarta Sans ExtraBold (título, lista e CTA).
Rodar a partir de fea_artes/:  python3 criativos/ads10.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *

PJS = fonte('PlusJakartaSans_800ExtraBold')
LARANJA = (253, 184, 84)
BRANCO = (250, 253, 255)
PRETO = (11, 11, 11)
BRILHO = lambda r, g, b: (r > 170) & (g > 140)


# Plus Jakarta Sans tem muito respiro lateral em pontuação; no original ("dominar:") ela vem
# colada à palavra. Aproximação óptica em fração do corpo da fonte.
KERN_ANTES = {':': -0.10, '.': -0.10, '!': -0.06, ',': -0.06, '”': -0.06}
KERN_DEPOIS = {'“': -0.06}


def _runs(texto):
    """Divide em trechos [(texto, ajuste_px_em)] aplicando a aproximação de pontuação."""
    out, cur, aj = [], '', 0.0
    for i, ch in enumerate(texto):
        k = KERN_ANTES.get(ch, 0) if i else 0
        if i and texto[i - 1] in KERN_DEPOIS:
            k += KERN_DEPOIS[texto[i - 1]]
        if k:
            out.append((cur, aj))
            cur, aj = ch, k
        else:
            cur += ch
    out.append((cur, aj))
    return out


def largura_kern(f, texto):
    """(esquerda_tinta, direita_tinta) do texto desenhado com a aproximação de pontuação."""
    x, l0, r0 = 0.0, None, 0
    for t, aj in _runs(texto):
        x += aj * f.size
        if t:
            l, _, r, _ = f.getbbox(t)
            l0 = x + l if l0 is None else l0
            r0 = x + r
        x += f.getlength(t)
    return l0 or 0, r0


def linha_cores(im, segs, f, cx, y_origem):
    """Escreve uma linha com trechos de cores diferentes, centrada (pela tinta) em cx."""
    d = ImageDraw.Draw(im)
    txt = ''.join(t for t, _ in segs)
    l, r = largura_kern(f, txt)
    x = cx - (r - l) / 2 - l
    pos = 0
    for t, c in segs:
        for run, aj in _runs(txt[pos:pos + len(t)]) if pos == 0 else _runs_contexto(txt, pos, len(t)):
            x += aj * f.size
            d.text((x, y_origem), run, font=f, fill=c)
            x += f.getlength(run)
        pos += len(t)


def _runs_contexto(txt, pos, n):
    """Como _runs, mas respeitando o caractere anterior ao trecho (pontuação entre cores)."""
    runs = _runs(txt[pos - 1:pos + n])
    t0, aj0 = runs[0]
    runs[0] = (t0[1:], aj0) if t0 else (t0, aj0)
    if runs[0][0] == '' and len(runs) > 1:
        # o primeiro char do trecho abriu um novo run com ajuste próprio
        return runs[1:] if runs[0][1] == 0 else runs
    return runs


def bloco_cores(im, pt, es_segs, tops, f, cx):
    """pt: linhas originais (para achar a linha de base pelo topo medido); es_segs: [[(texto, cor)]]."""
    for p, segs, ytop in zip(pt, es_segs, tops):
        linha_cores(im, segs, f, cx, ytop - f.getbbox(p)[1])


def ajustar(f, caminho, linhas, largura_max):
    while max(f.getbbox(s)[2] - f.getbbox(s)[0] for s in linhas) > largura_max and f.size > 8:
        f = ImageFont.truetype(caminho, f.size - 0.25)
    return f


def forma_caixa(im, box, cor=238):
    """Máscara da caixa clara de cantos arredondados (fechamento morfológico cobre as letras)."""
    a = np.array(im).astype(int)
    x0, y0, x1, y1 = box
    luz = ((abs(a[..., 0] - cor) < 12) & (abs(a[..., 1] - cor) < 12) & (abs(a[..., 2] - cor) < 12)).astype(np.uint8)
    m = np.zeros_like(luz)
    m[y0:y1, x0:x1] = luz[y0:y1, x0:x1]
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    return cv2.erode(m, np.ones((5, 5), np.uint8)).astype(bool)


def apagar_na_caixa(im, box, cor=238):
    """Apaga texto escuro e números laranja só dentro da forma da caixa (sem tocar nos cantos)."""
    fm = forma_caixa(im, box, cor)
    a = np.array(im)
    ai = a.astype(int)
    txt = (np.abs(ai - cor).max(2) > 10) & fm
    m = cv2.dilate(txt.astype(np.uint8) * 255, np.ones((5, 5), np.uint8))
    m[~fm] = 0
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, 6, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def apagar_cta_titulo(im, caixa):
    return apagar(im, caixa, BRILHO, 3)


TIT_PT = ['Aprenda o preenchimento', 'tridimensional de olheiras', 'ao dominar:']
TIT_ES = [[('Aprenda el relleno', LARANJA)],
          [('tridimensional', LARANJA), (' de ojeras', BRANCO)],
          [('dominando:', BRANCO)]]
LISTA_PT = ['1. Técnicas de injeção', '2. Regiões de risco', '3. Plano anatômico correto']
LISTA_ES_TXT = ['1. Técnicas de inyección', '2. Zonas de riesgo', '3. Plano anatómico correcto']
LISTA_ES = [[('1.', LARANJA), (' Técnicas de inyección', PRETO)],
            [('2.', LARANJA), (' Zonas de riesgo', PRETO)],
            [('3.', LARANJA), (' Plano anatómico correcto', PRETO)]]
CTA_PT = ['CLIQUE E GARANTA', 'O SEU DESCONTO']
CTA_ES = [[('HAGA CLIC Y ', BRANCO), ('ASEGURE', LARANJA)], [('SU DESCUENTO', LARANJA)]]


def titulo(im, caixa, tops, larg_ref):
    im = apagar_cta_titulo(im, caixa)
    f = calibrar(PJS, TIT_PT[0], larg_ref)
    bloco_cores(im, TIT_PT, TIT_ES, tops, f, 540)
    return im


def lista(im, box, tops, larg_ref, cx):
    im = apagar_na_caixa(im, box)
    f = calibrar(PJS, LISTA_PT[2], larg_ref)
    f = ajustar(f, PJS, LISTA_ES_TXT, larg_ref)  # 'correcto' é mais longo: não passa da largura original
    bloco_cores(im, LISTA_PT, LISTA_ES, tops, f, cx)
    return im, f.size


def cta(im, caixa, tops, larg_ref):
    im = apagar_cta_titulo(im, caixa)
    f = calibrar(PJS, CTA_PT[0], larg_ref)
    bloco_cores(im, CTA_PT, CTA_ES, tops, f, 540)
    return im


def feed():
    im = abrir('trabalho/C-ads10-feed.png')
    im = titulo(im, (190, 488, 890, 656), [497, 552, 607], 861 - 216 + 1)
    im, t = lista(im, (205, 688, 858, 870), [706, 758, 806], 835 - 243 + 1, 539)
    im = cta(im, (290, 893, 790, 996), [901, 951], 761 - 317 + 1)
    return im


def story():
    im = abrir('trabalho/C-ads10-story.png')
    im = titulo(im, (140, 1044, 940, 1236), [1054, 1117, 1180], 907 - 170 + 1)
    im, t = lista(im, (159, 1273, 905, 1481), [1294, 1352, 1408], 878 - 201 + 1, 539.5)
    im = cta(im, (260, 1506, 820, 1626), [1516, 1574], 794 - 286 + 1)
    return im


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print('ok', salvar(feed(), 'FEA-Ads 10 - PTO-LATAM - Feed.png'))
    print('ok', salvar(story(), 'FEA-Ads 10 - PTO-LATAM - Story.png'))
