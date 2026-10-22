"""Criativo novo a partir de uma arte aprovada da campanha: mantém foto, logo, botão e selo
"AO VIVO", apaga o bloco de texto (título, apoio, data) e escreve a copy nova no mesmo lugar,
com a mesma fonte, cores e margem. Nenhuma imagem gerada por IA: a foto é a da arte original.

Uso como módulo: criar(modelo_png, titulo, apoio, data1, data2, saida)
Título aceita [trecho] para destacar em verde."""
import re, sys
import cv2, numpy as np
from PIL import Image, ImageDraw
from rapidocr_onnxruntime import RapidOCR
sys.path.insert(0, "/home/user/FEA/FEA-MTB-11-26")
from fea_trocar_data_arte import fonte

_ocr = RapidOCR()


def _caixas(img):
    r, _ = _ocr(img)
    return [(t, int(min(p[0] for p in b)), int(min(p[1] for p in b)), int(max(p[0] for p in b)), int(max(p[1] for p in b))) for b, t, s in r]


def _bloco(cx):
    """Linhas do bloco editável: abaixo do logo, acima do botão "Toque em Saiba Mais"."""
    logo = max(c[4] for c in cx if re.search(r"Botul", c[0], re.I))
    botao = min(c[2] for c in cx if re.search(r"Toq|Togue", c[0]))
    linhas = [c for c in cx if c[2] > logo + 20 and c[4] < botao - 10]
    i_data = next(i for i, c in enumerate(linhas) if re.match(r"Segunda", c[0]))
    return linhas[:i_data], linhas[i_data:]


def _quebrar(texto, f, largura, d):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if d.textlength(t.replace("[", "").replace("]", ""), font=f) <= largura or not atual: atual = t
        else: linhas.append(atual); atual = p
    return linhas + [atual]


def _escrever(d, x, y, linha, f, branco, verde, verde_aberto):
    """Escreve uma linha com trechos [verdes]; o destaque pode atravessar a quebra de linha."""
    for parte in re.split(r"(\[|\])", linha):
        if parte == "[": verde_aberto = True; continue
        if parte == "]": verde_aberto = False; continue
        d.text((x, y), parte, font=f, fill=verde if verde_aberto else branco)
        x += d.textlength(parte, font=f)
    return verde_aberto


def criar(modelo, titulo, apoio, data1, data2, saida):
    img = np.asarray(Image.open(modelo).convert("RGB")).copy()
    cx = _caixas(modelo)
    texto, data = _bloco(cx)
    todas = texto + data
    x0 = min(c[1] for c in todas)
    largura = (max(c[3] for c in texto) - x0) * 0.9   # folga para não encostar na foto
    # cores medidas na arte: branco no título, verde na data
    def cor(c, verdeia):
        reg = img[c[2]:c[4], c[1]:c[3]].reshape(-1, 3).astype(int)
        sel = reg[(reg[:, 1] - reg[:, 0] > 60)] if verdeia else reg[reg.min(1) > 170]
        return tuple(int(v) for v in np.median(sel, 0)) if len(sel) else ((0, 214, 100) if verdeia else (242, 242, 242))
    verde, branco = cor(data[0], True), cor(texto[0], False)
    # apaga só a tinta do texto antigo (foto e fundo ficam)
    m = np.zeros(img.shape[:2], np.uint8)
    for c in todas:
        reg = img[c[2] - 6:c[4] + 6, c[1] - 6:c[3] + 6].astype(int)
        tinta = (reg.max(2) > 70) | (reg[:, :, 1] - reg[:, :, 0] > 40)
        m[c[2] - 6:c[4] + 6, c[1] - 6:c[3] + 6] = tinta * 255
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    img = cv2.inpaint(img, m, 9, cv2.INPAINT_TELEA)
    out = Image.fromarray(img); d = ImageDraw.Draw(out)
    # data no mesmo lugar e corpo da original
    alt_data = data[0][4] - data[0][2]
    f_d1, f_d2 = fonte("sora", 700, alt_data * 0.95), fonte("sora", 400, alt_data * 0.95)
    d.text((x0, data[0][2] - alt_data * 0.12), data1, font=f_d1, fill=verde)
    if len(data) > 1: d.text((x0, data[1][2] - alt_data * 0.12), data2, font=f_d2, fill=branco)
    # título e apoio ocupam o espaço entre o topo do título antigo e a data
    topo, fundo = texto[0][2], data[0][2] - alt_data * 1.3
    corpo_t = (texto[0][4] - texto[0][2]) * 1.15
    while True:
        f_t, f_a = fonte("sora", 700, corpo_t), fonte("sora", 400, corpo_t * 0.58)
        lt, la = _quebrar(titulo, f_t, largura, d), _quebrar(apoio, f_a, largura, d)
        h = len(lt) * corpo_t * 1.12 + corpo_t * 0.7 + len(la) * corpo_t * 0.58 * 1.3
        if h <= fundo - topo or corpo_t < 20: break
        corpo_t *= 0.95
    y = topo + (fundo - topo - h) / 2 if len(lt) < 3 else topo
    aberto = False
    for l in lt:
        aberto = _escrever(d, x0, y, l, f_t, branco, verde, aberto); y += corpo_t * 1.12
    y += corpo_t * 0.7
    for l in la:
        d.text((x0, y), l, font=f_a, fill=branco); y += corpo_t * 0.58 * 1.3
    out.save(saida)
    return saida
