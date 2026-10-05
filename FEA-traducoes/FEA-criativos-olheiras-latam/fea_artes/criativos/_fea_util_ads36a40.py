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


def tirar_acento_selo(im, caixa, cond, fator=0.3, folga=3):
    """Apaga o acento agudo de 'CÓPIAS' no selo: o menor componente escuro e mais alto
    da caixa. A área do acento (até a linha logo acima do topo do O) é refeita por
    interpolação horizontal entre as colunas de fundo dos dois lados (fundo do selo é
    degradê suave), sem tocar o O."""
    x0, y0, x1, y1 = caixa
    m = mascara(im, caixa, cond).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    ids = [i for i in range(1, n) if st[i][4] >= 4]
    med = np.median([st[i][4] for i in ids])
    ac = [i for i in ids if st[i][4] < fator * med]
    if not ac:
        raise SystemExit(f'acento do selo não achado em {caixa}')
    i = min(ac, key=lambda k: st[k][1])
    ax, ay, aw, ah = (int(v) for v in st[i][:4])
    ax += x0; ay += y0
    a = np.array(im).astype(np.float32)
    lum = a.sum(2)
    xa, xb = ax - folga, ax + aw + folga
    # topo do O: primeira linha abaixo do acento com pixel de texto, depois de pelo menos 1 linha
    r = ay + ah
    while r < ay + ah + 12 and not (lum[r, xa + 1:xb] < 330).any():
        r += 1
    for x in range(xa + 1, xb):
        t = (x - xa) / (xb - xa)
        for y in range(ay - folga, r):
            a[y, x] = a[y, xa] * (1 - t) + a[y, xb] * t
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)), [(ax, ay, aw, ah, r)]


def apagar_area(im, caixa, raio=5):
    """Inpainting da caixa inteira (para acento desfocado que se funde à letra de baixo)."""
    a = np.array(im)
    M = np.zeros(a.shape[:2], np.uint8)
    M[caixa[1]:caixa[3], caixa[0]:caixa[2]] = 255
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), M, raio, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))


def tirar_acento_desfocado(im, xa, xb, y_ini, y_topo_O, y_base_O, desvio=True):
    """Acento agudo desfocado colado no topo do O (selo grande desfocado do canto).
    O 'O' é simétrico na vertical: a metade de cima (onde o acento se funde) é
    reconstruída espelhando a metade de baixo da própria letra; acima do O, o fundo
    é interpolado na horizontal entre as colunas xa e xb (fora do acento). Só usa
    pixels do próprio original, nada é gerado."""
    a = np.array(im).astype(np.float32)
    yc2 = y_topo_O + y_base_O          # 2 x centro vertical do O
    ym = (y_topo_O + y_base_O) // 2
    for x in range(xa + 1, xb):
        t = (x - xa) / (xb - xa)
        for y in range(y_ini, y_topo_O - 1):
            a[y, x] = a[y, xa] * (1 - t) + a[y, xb] * t
        for y in range(y_topo_O - 1, ym):
            ys = yc2 - y   # espelho; transfere só o desvio em relação ao fundo da linha (fundo tem degradê)
            fundo_src = a[ys, xa] * (1 - t) + a[ys, xb] * t
            fundo_dst = a[y, xa] * (1 - t) + a[y, xb] * t
            a[y, x] = fundo_dst + (a[ys, x] - fundo_src) if desvio else a[ys, x]
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8))


def apagar_liso(im, caixa, cond, dil=4, sigma=12):
    """Para fundo liso/degradê suave: troca os pixels de texto (dilatados) pela média
    ponderada dos pixels de fundo vizinhos (convolução normalizada). Evita o 'fantasma'
    que o Telea às vezes deixa em degradê claro."""
    a = np.array(im).astype(np.float32)
    x0, y0, x1, y1 = caixa
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = mascara(im, caixa, cond).astype(np.uint8)
    m = cv2.dilate(m, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8)).astype(np.float32)
    p = int(4 * sigma)
    X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - p), min(a.shape[1], x1 + p), min(a.shape[0], y1 + p)
    sub, ms = a[Y0:Y1, X0:X1], m[Y0:Y1, X0:X1]
    outros = cv2.dilate(mascara(im, (X0, Y0, X1, Y1), cond).astype(np.uint8),
                        np.ones((2 * dil + 1, 2 * dil + 1), np.uint8)).astype(np.float32)
    fundo = (1 - ms) * (1 - outros)   # texto vizinho fora da caixa não entra na média
    for _ in range(3):  # repete para preencher miolos grandes
        num = cv2.GaussianBlur(sub * fundo[..., None], (0, 0), sigma)
        den = cv2.GaussianBlur(fundo, (0, 0), sigma)[..., None]
        est = num / np.maximum(den, 1e-4)
        ok = den[..., 0] > 1e-3
        sub = np.where((ms[..., None] > 0) & ok[..., None], est, sub)
        if ok[ms > 0].all():
            break
        sigma *= 2
    a[Y0:Y1, X0:X1] = sub
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8))
