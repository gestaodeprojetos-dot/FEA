"""Funções auxiliares dos criativos Ads 36 a Ads 40 (Ebook Olheiras LATAM).

Só complementa fea_arte_lib: texto com degradê (dourado / branco-cinza) copiado do
próprio original, texto com espaçamento entre letras (CTAs em caixa alta) e
calibração por altura de maiúscula. Nada de IA generativa: o degradê é amostrado
dos pixels do texto original e reaplicado na mesma posição relativa.
Este arquivo não gera nada sozinho (rodar_todos.py o executa sem efeito).
"""
import os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fea_arte_lib import *  # noqa

SERIF_SEMI = fonte('NotoSerif_600SemiBold')
SERIF_BOLD = fonte('NotoSerif_700Bold')
SANS_REG = fonte('NotoSans_400Regular')
SANS_MED = fonte('NotoSans_500Medium')
SANS_SEMI = fonte('NotoSans_600SemiBold')
SANS_BOLD = fonte('NotoSans_700Bold')
SANS_XBOLD = fonte('NotoSans_800ExtraBold')


def F(caminho, tam):
    return ImageFont.truetype(caminho, float(tam))


def campo_cor(im, caixa, cond, sigma=None):
    """Mapa de cor (h, w, 3) do texto original dentro da caixa: cor média local dos
    pixels de núcleo das letras, espalhada por convolução normalizada."""
    x0, y0, x1, y1 = caixa
    a = np.array(im)[y0:y1, x0:x1].astype(np.float32)
    m = mascara(im, caixa, cond).astype(np.uint8)
    m = cv2.erode(m, np.ones((3, 3), np.uint8)).astype(np.float32)
    s = sigma or max(4.0, (y1 - y0) / 6)
    num = cv2.GaussianBlur(a * m[..., None], (0, 0), s)
    den = cv2.GaussianBlur(m, (0, 0), s)[..., None]
    out = num / np.maximum(den, 1e-4)
    falta = den[..., 0] < 1e-3
    if falta.any():
        med = a[m > 0].mean(0) if m.sum() else np.array([255, 255, 255], np.float32)
        out[falta] = med
    return np.clip(out, 0, 255)


def mascara_texto(tam_img, partes, f, y):
    """partes: [(x, texto)] na mesma linha. Devolve máscara L do tamanho da imagem."""
    L = Image.new('L', tam_img, 0)
    d = ImageDraw.Draw(L)
    for x, t in partes:
        d.text((x, y), t, font=f, fill=255)
    return L


def pintar_mascara(im, L, campo=None, cor=None, caixa_campo=None):
    """Compõe a máscara L sobre im. campo: mapa de cor esticado para caixa_campo
    (x0, y0, x1, y1) onde ficam as letras novas; ou cor sólida."""
    a = np.array(im).astype(np.float32)
    al = np.array(L).astype(np.float32)[..., None] / 255
    if campo is not None:
        x0, y0, x1, y1 = caixa_campo
        c = cv2.resize(campo, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
        cor_img = a.copy()
        cor_img[y0:y1, x0:x1] = c
    else:
        cor_img = np.zeros_like(a) + np.array(cor, np.float32)
    a = a * (1 - al) + cor_img * al
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8))


def bbox_mask(L):
    b = L.getbbox()
    return b


def escrever_campo(im, texto, f, x, y, campo):
    """Escreve 'texto' com origem (x, y) colorindo com o campo esticado na caixa real das letras."""
    L = mascara_texto(im.size, [(x, texto)], f, y)
    b = L.getbbox()
    return pintar_mascara(im, L, campo=campo, caixa_campo=b)


def largura(f, t):
    l, _, r, _ = f.getbbox(t)
    return r - l


def calibrar_altura(caminho, ref, altura):
    """Tamanho em que o glifo 'ref' (ex.: 'H') tem a altura medida."""
    _, a, _, b = ImageFont.truetype(caminho, 400).getbbox(ref)
    return ImageFont.truetype(caminho, round(400 * altura / (b - a) * 4) / 4)


def calibrar_larg(caminho, texto, larg):
    """Como calibrar() da lib, mas por proporção (rápido)."""
    l, _, r, _ = ImageFont.truetype(caminho, 400).getbbox(texto)
    return ImageFont.truetype(caminho, round(400 * larg / (r - l) * 4) / 4)


def largura_track(f, t, track):
    return sum(f.getlength(c) for c in t) + track * (len(t) - 1) - f.getbbox(t[0])[0] - (f.getlength(t[-1]) - f.getbbox(t[-1])[2])


def escrever_track(im, t, f, x_esq, y_topo_maiusc, cor, track):
    """Caixa alta com espaçamento: x_esq = borda esquerda da 1ª letra; y_topo = topo das maiúsculas."""
    d = ImageDraw.Draw(im)
    _, tp, _, _ = f.getbbox('H')
    x = x_esq - f.getbbox(t[0])[0]
    y = y_topo_maiusc - tp
    for c in t:
        d.text((x, y), c, font=f, fill=cor)
        x += f.getlength(c) + track
    return im


def track_medido(f, t, largura_medida):
    nat = largura_track(f, t, 0)
    return (largura_medida - nat) / (len(t) - 1)


def tirar_acento(im, caixa, cond, dil=2, raio=4):
    """Remove só o acento (pixels de texto dentro da caixa pequena acima da letra)."""
    return apagar(im, caixa, cond, dil, raio)


def componentes(im, caixa, cond):
    m = mascara(im, caixa, cond).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    return [(int(st[i][0] + caixa[0]), int(st[i][1] + caixa[1]), int(st[i][0] + st[i][2] + caixa[0]),
             int(st[i][1] + st[i][3] + caixa[1]), int(st[i][4])) for i in range(1, n)]


def tirar_acento_selo(im, caixa, cond, fator=0.3, dil=2):
    """Apaga o acento agudo de 'CÓPIAS' no selo: o menor componente escuro e mais alto
    da caixa. Inpainting só nos pixels desse componente (dilatados), sem tocar as letras vizinhas."""
    x0, y0, x1, y1 = caixa
    m = mascara(im, caixa, cond).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    ids = [i for i in range(1, n) if st[i][4] >= 4]
    med = np.median([st[i][4] for i in ids])
    ac = [i for i in ids if st[i][4] < fator * med]
    if not ac:
        raise SystemExit(f'acento do selo não achado em {caixa}')
    i = min(ac, key=lambda k: st[k][1])
    alvo = (lab == i).astype(np.uint8)
    alvo = cv2.dilate(alvo, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8))
    outros = cv2.dilate(((lab > 0) & (lab != i)).astype(np.uint8), np.ones((3, 3), np.uint8))
    alvo[outros > 0] = 0
    a = np.array(im)
    M = np.zeros(a.shape[:2], np.uint8)
    M[y0:y1, x0:x1] = alvo * 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), M, 3, cv2.INPAINT_TELEA)
    c = st[i]
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)), [(int(c[0] + x0), int(c[1] + y0), int(c[2]), int(c[3]))]


def trocar_cta(im, botao, cond_letra, cond_apagar, seta_x0, caminho_fonte, pt, es, folga_seta=None,
               folga_esq_min=70, area_min=150, rotulo=''):
    """CTA em caixa alta com espaçamento, dentro de um botão (fundo liso ou degradê).
    Mede as letras originais (componentes à esquerda da seta), calibra fonte pela altura
    da maiúscula e o tracking pela largura, apaga por inpainting e escreve o ES centrado
    no mesmo centro; se passar da seta, encosta à esquerda e, se faltar folga, reduz
    a fonte (máx. 15 %)."""
    bx0, by0, bx1, by1 = botao
    cs = [c for c in componentes(im, (bx0 + 10, by0 + 10, seta_x0 - 2, by1 - 10), cond_letra) if c[4] > area_min]
    mt, mh = np.median([c[1] for c in cs]), np.median([c[3] - c[1] for c in cs])
    cs = [c for c in cs if abs(c[1] - mt) <= 0.3 * mh and abs((c[3] - c[1]) - mh) <= 0.35 * mh]  # só letras da linha
    xs0, xs1 = min(c[0] for c in cs), max(c[2] for c in cs)
    topo = int(np.median([c[1] for c in cs]))
    alt = int(np.median([c[3] - c[1] for c in cs]))
    f = calibrar_altura(caminho_fonte, 'H', alt)
    tr = track_medido(f, pt, xs1 - xs0)
    cor = cor_texto(im, (xs0, topo, xs1, topo + alt), cond_letra)
    im = apagar(im, (xs0 - 14, topo - 14, xs1 + 14, topo + alt + 24), cond_apagar, 4)
    if folga_seta is None:
        folga_seta = seta_x0 - xs1
    limite = seta_x0 - folga_seta
    cx = (xs0 + xs1) / 2
    tam0 = f.size
    while True:
        wl = largura_track(f, es, tr)
        xi = cx - wl / 2
        if xi + wl > limite:
            xi = limite - wl
        if xi >= bx0 + folga_esq_min:
            break
        if f.size < tam0 * 0.85:
            raise SystemExit(f'CTA {es} não cabe nem com -15 %')
        f = ImageFont.truetype(caminho_fonte, f.size - 0.25)
        tr *= 0.995
    a_nova = f.getbbox('H')[3] - f.getbbox('H')[1]
    escrever_track(im, es, f, xi, topo + (alt - a_nova) / 2, cor, tr)
    print(rotulo, 'CTA', es, 'fonte', f.size, '(orig', tam0, ') x', round(xi), round(xi + wl), 'limite', limite)
    return im


def titulo_linhas(im, linhas_med, pts, ess, caminho_fonte, ref_idx, cor, cx, limites, escala_min=0.85, apagar_cond=None,
                  caixa_apagar=None, rotulo=''):
    """Título de várias linhas centrado: calibra pela linha PT ref_idx, mantém a linha de
    base de cada linha original e, se alguma linha ES passar do limite (x_min, x_max) da
    sua posição, reduz tudo por igual (mín. escala_min)."""
    l = linhas_med[ref_idx]
    f = calibrar_larg(caminho_fonte, pts[ref_idx], l[3] - l[2] + 1)
    esc = 1.0
    for e, (xmn, xmx) in zip(ess, limites):
        w = largura(f, e)
        esc = min(esc, 2 * min(cx - xmn, xmx - cx) / w)
    if esc < escala_min:
        raise SystemExit(f'{rotulo}: título não cabe (escala {esc:.2f})')
    if caixa_apagar:
        im = apagar(im, caixa_apagar, apagar_cond, 4)
    d = ImageDraw.Draw(im)
    fn = ImageFont.truetype(caminho_fonte, f.size * min(1, esc))
    for (top, bot, _, _), p, e in zip(linhas_med, pts, ess):
        base = top - f.getbbox(p)[1] + f.getmetrics()[0]   # linha de base do original
        y = base - fn.getmetrics()[0]
        d.text((cx - largura(fn, e) / 2 - fn.getbbox(e)[0], y), e, font=fn, fill=cor)
    print(rotulo, 'título fonte', round(f.size, 2), '->', round(fn.size, 2))
    return im, fn


def apagar_area(im, caixa, raio=5):
    """Inpainting da caixa inteira (para acento desfocado que se funde à letra de baixo)."""
    a = np.array(im)
    M = np.zeros(a.shape[:2], np.uint8)
    M[caixa[1]:caixa[3], caixa[0]:caixa[2]] = 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), M, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
