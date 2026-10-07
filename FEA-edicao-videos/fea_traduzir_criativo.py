#!/usr/bin/env python3
"""FEA: tradução de criativo com texto queimado (legenda e letreiros em português -> espanhol).

Pedido da Keila (07/10/2026): pasta de anúncios FEP com legenda em português gravada na imagem.
Tirar a legenda PT e deixar só a legenda em espanhol, no mesmo lugar, tamanho e tempo.

Fluxo (ver FEA-traducao-criativos.md):
  1. fea_ocr_criativo.py ocr    -> lê os textos queimados (OCR a 3 quadros/s)
  2. fea_ocr_criativo.py blocos -> agrupa em blocos com tempo e posição (legenda de 2 linhas = 1 bloco)
  3. tradução: es/N.json com {id: "texto em espanhol" | null}; null = texto da cena, fica como está
  4. este script:
       - passada 1: escolhe o quadro de referência de cada bloco (texto completo) e mede, quadro a quadro,
         quando o bloco está na tela
       - passada 2: apaga o texto PT (inpainting só na letra e no contorno) e desenha o ES por cima

Uso:
    python3 fea_traduzir_criativo.py FFMPEG video_1080.mp4 cfg.json original.mp4 saida.mp4 [inicio dur]

Estilos (detectados no quadro de referência, ou forçados com "tipo" no cfg):
    contorno  texto branco com contorno escuro (legenda comum)
    branco    texto branco sem contorno sobre fundo colorido (letreiro grande, cartela final)
    caixa     texto escuro em caixa branca (título estilo story); a caixa nova cobre a antiga
Saída: 1080x1920, 30 fps, H.264 CRF 18 (nunca HEVC, não abre no computador da Keila), áudio AAC 192k.
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.environ.get("FEA_FONTES", os.path.join(AQUI, "fonts"))


def el(n):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))


K3, K7, K9, K13 = el(3), el(7), el(9), el(13)


def fonte(nome, tam):
    arq = nome if nome.endswith(".ttf") else f"Montserrat-{nome}.ttf"
    return ImageFont.truetype(os.path.join(FONTES, arq), int(round(tam)))


def mascaras(roi, limiar=205):
    """claro: pixel claro; lc: claro encostado em escuro (letra branca com contorno);
    le: escuro encostado em claro (letra preta em caixa branca); br: branco neutro (letra branca)."""
    g = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    v = roi.max(axis=2)
    sat = v.astype(np.int16) - roi.min(axis=2)
    claro = ((v >= 190) & (g >= 150)).astype(np.uint8)
    escuro = (g <= 70).astype(np.uint8)
    lc = claro & cv2.dilate(escuro, K7)
    le = escuro & cv2.dilate(claro, K7)
    br = ((g >= limiar) & (sat <= 45)).astype(np.uint8)
    return claro, lc, le, br


def tinta(tipo, lc, le, br, zona):
    if tipo == "caixa":
        return le
    if tipo == "caixa_escura":
        return br & zona
    if tipo == "branco":
        return br & zona
    return lc


def recorte(bbox, pad):
    x0, y0, x1, y1 = bbox
    return max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)


def ler_quadros(ff, video, ini=None, dur=None):
    cmd = [ff, "-nostdin", "-v", "error"]
    if ini is not None:
        cmd += ["-ss", str(ini), "-t", str(dur)]
    cmd += ["-i", video, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3 * 2)
    i = int(round((ini or 0) * FPS))
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield i, np.frombuffer(b, np.uint8).reshape(H, W, 3)
        i += 1
    p.wait()


def largura(txt, f):
    return f.getlength(txt) if txt else 0


def quebrar(texto, f, maxw):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for w in par.split():
            cand = (atual + " " + w).strip()
            if atual and largura(cand, f) > maxw:
                linhas.append(atual)
                atual = w
            else:
                atual = cand
        if atual:
            linhas.append(atual)
    # equilibra 2 linhas (evita linha final com 1 palavra)
    if len(linhas) == 2 and "\n" not in texto:
        ws = texto.split()
        k = min(range(1, len(ws)), key=lambda k: max(largura(" ".join(ws[:k]), f), largura(" ".join(ws[k:]), f)))
        a, b = " ".join(ws[:k]), " ".join(ws[k:])
        if max(largura(a, f), largura(b, f)) <= maxw * 1.05:
            linhas = [a, b]
    return linhas


def zona_linhas(bl, roi_xy, shape, pad=4):
    z = np.zeros(shape, np.uint8)
    x0r, y0r = roi_xy
    for ln in bl["linhas"]:
        lx0, ly0, lx1, ly1 = ln["bbox"]
        z[max(0, ly0 - y0r - pad):max(0, ly1 - y0r + pad), max(0, lx0 - x0r - pad):max(0, lx1 - x0r + pad)] = 1
    return z


def classificar(bl, ref_roi, roi_xy, claro, lc, le, br):
    x0r, y0r = roi_xy
    bx0, by0, bx1, by1 = bl["bbox"]
    zona = zona_linhas(bl, roi_xy, claro.shape)
    sub = claro[by0 - y0r:by1 - y0r, bx0 - x0r:bx1 - x0r]
    area = max(1, (bx1 - bx0) * (by1 - by0))
    lh = (by1 - by0) / max(1, len(bl["linhas"]))
    # caixa: muito branco, texto escuro dentro, e o branco termina perto do texto (não é blusa/parede)
    if sub.size and sub.mean() > 0.45 and le[by0 - y0r:by1 - y0r, bx0 - x0r:bx1 - x0r].sum() > 0.04 * area:
        n, lab, st, _ = cv2.connectedComponentsWithStats(claro, 8)
        sl = lab[by0 - y0r:by1 - y0r, bx0 - x0r:bx1 - x0r]
        cont = np.bincount(sl.ravel(), minlength=n)
        cont[0] = 0
        if cont.max() > 0:
            ax, ay, aw, ah, area_c = st[int(cont.argmax()), :5]
            encosta = ax <= 1 or ay <= 1 or ax + aw >= claro.shape[1] - 1 or ay + ah >= claro.shape[0] - 1
            if not encosta and area_c >= 0.5 * area and aw <= (bx1 - bx0) + 6 * lh and ah <= (by1 - by0) + 4 * lh:
                bl["_caixa_antiga"] = [int(ax + x0r), int(ay + y0r), int(ax + aw + x0r), int(ay + ah + y0r)]
                return "caixa"
        # caixa sem borda visível (caixa branca grudada em fundo branco): decide pela polaridade da letra.
        # Letra branca com contorno tem "ilhas" brancas (miolo da letra) cercadas de preto; letra preta em
        # fundo branco só tem os miolos pequenos (o, a, e).
        esc = (cv2.cvtColor(ref_roi, cv2.COLOR_BGR2GRAY) <= 70).astype(np.uint8) & zona
        n, lab, st, _ = cv2.connectedComponentsWithStats(claro, 8)
        h_, w_ = claro.shape
        borda_ok = (st[:, 0] > 0) & (st[:, 1] > 0) & (st[:, 0] + st[:, 2] < w_) & (st[:, 1] + st[:, 3] < h_)
        ilha = borda_ok & (st[:, 4] < 0.02 * h_ * w_)
        ilha[0] = False
        ilhas = (ilha[lab] & zona.astype(bool)).sum()
        if esc.sum() > 50 and ilhas < 0.35 * esc.sum():
            return "caixa"
    wz = (br & zona).astype(bool)
    if wz.sum() < 30:
        return "contorno"
    g = cv2.cvtColor(ref_roi, cv2.COLOR_BGR2GRAY)
    anel = cv2.dilate(wz.astype(np.uint8), K7).astype(bool) & ~cv2.dilate(wz.astype(np.uint8), K3).astype(bool)
    # fundo branco em volta (blusa, parede): só o critério de contorno funciona
    fora = cv2.dilate(zona, el(25)).astype(bool) & ~cv2.dilate(zona, K9).astype(bool)
    if fora.sum() and br[fora].mean() > 0.35:
        return "contorno"
    if np.median(g[anel]) < 75:
        return "contorno"
    return "branco"


def preparar(bl, ref_roi, roi_xy):
    """Mede tipo, fonte, cor e posição do bloco no quadro de referência; desenha o ES (RGBA)."""
    x0r, y0r = roi_xy
    claro, lc, le, br = mascaras(ref_roi, bl.get("limiar", 205))
    tipo = bl.get("tipo") or classificar(bl, ref_roi, roi_xy, claro, lc, le, br)
    bl["tipo"] = tipo
    zona = zona_linhas(bl, roi_xy, claro.shape)
    bl["_zona"] = cv2.dilate(zona, el(21))
    t = tinta(tipo, lc, le, br, bl["_zona"]) & cv2.dilate(zona, K9)
    bl["_ref"] = t.copy()
    g = cv2.cvtColor(ref_roi, cv2.COLOR_BGR2GRAY)
    nucleo = cv2.erode(t, K3).astype(bool)
    if tipo not in ("caixa", "caixa_escura") and nucleo.sum() > 30:
        bl["_cor"] = tuple(int(c) for c in np.median(ref_roi[nucleo], axis=0)[::-1])
    else:
        bl["_cor"] = (255, 255, 255)
    fundo = cv2.dilate(t, el(31)).astype(bool) & ~cv2.dilate(t, el(15)).astype(bool)
    bl["_chapado"] = bool(tipo not in ("caixa", "caixa_escura") and fundo.sum() > 50 and g[fundo].std() < 6)
    if bl["_chapado"]:
        bl["_cor_fundo"] = np.median(ref_roi[fundo], axis=0).astype(np.uint8)

    maius = sum(c.isupper() for c in bl["pt"]) > 0.7 * max(1, sum(c.isalpha() for c in bl["pt"]))
    if tipo == "branco" and maius and not bl["_chapado"]:
        nome = bl.get("fonte", "Anton-Regular.ttf")       # letreiro grande condensado
    else:
        nome = bl.get("fonte", "Bold")
    f100 = fonte(nome, 100)
    tams, centros, x0s, x1s, alts = [], [], [], [], []
    for ln in bl["linhas"]:
        lx0, ly0, lx1, ly1 = ln["bbox"]
        m = t[max(0, ly0 - y0r):max(0, ly1 - y0r), max(0, lx0 - x0r):max(0, lx1 - x0r)]
        cols = np.where(m.any(axis=0))[0]
        rows = np.where(m.any(axis=1))[0]
        if len(cols) < 2:
            continue
        iw = cols[-1] - cols[0] + 1
        w100 = largura(ln["txt"], f100)
        if w100 > 0:
            tams.append(100 * iw / w100)
        centros.append(max(ly0, y0r) + (rows[0] + rows[-1]) / 2)
        alts.append(rows[-1] - rows[0] + 1)
        x0s.append(max(lx0, x0r) + cols[0])
        x1s.append(max(lx0, x0r) + cols[-1])
    bx0, by0, bx1, by1 = bl["bbox"]
    tam = float(np.median(tams)) if tams else (by1 - by0) / max(1, len(bl["linhas"])) * 0.8
    if maius and alts and nome.startswith("Anton"):
        tam = float(np.median(alts)) / 0.72          # altura de maiúscula da Anton ~0,72 do corpo
    tam = max(18, min(160, tam * bl.get("escala", 1.0)))
    passo = float(np.median(np.diff(centros))) if len(centros) > 1 else tam * 1.22
    passo = max(tam * 1.0, min(tam * 1.5, passo))
    cx = (min(x0s) + max(x1s)) / 2 if x0s else (bx0 + bx1) / 2
    cy = float(np.mean(centros)) if centros else (by0 + by1) / 2
    esquerda = len(x0s) > 1 and (max(x0s) - min(x0s)) < 8 and (max(x1s) - min(x1s)) > 20
    larg_pt = (max(x1s) - min(x0s)) if x1s else (bx1 - bx0)
    f = fonte(nome, tam)
    n_pt = len(bl["linhas"])
    maxw = min(W * 0.9, max(larg_pt * (1.45 if n_pt == 1 else 1.12), W * 0.42)) * bl.get("largura", 1.0)
    linhas = quebrar(bl["es"], f, maxw)
    if not linhas:                                  # es = "": só apaga o PT, sem texto novo
        bl["_img"], bl["_pos"], bl["_tam"], bl["_fonte"] = None, (0, 0), round(tam, 1), nome
        return
    larg = max(largura(l, f) for l in linhas)
    asc, desc = f.getmetrics()
    alt = passo * (len(linhas) - 1) + asc + desc
    if tipo in ("caixa", "caixa_escura"):
        escura = tipo == "caixa_escura"
        if escura:
            bl["_cor_caixa"] = tuple(int(c) for c in np.median(ref_roi[(g <= 45)], axis=0)[::-1]) if (g <= 45).any() else (0, 0, 0)
        lh = (by1 - by0) / max(1, len(bl["linhas"]))
        # caixa forçada (fundo branco grudado na caixa): folga típica da caixa de story
        old = bl.get("_caixa_antiga") or [bx0 - 0.45 * lh, by0 - 0.35 * lh, bx1 + 0.45 * lh, by1 + 0.35 * lh]
        pad = tam * 0.38
        bw = max(larg + 2 * pad, old[2] - old[0] + 6)
        bh = max(alt + 2 * pad * 0.8, old[3] - old[1] + 6)
        ccx = (old[0] + old[2]) / 2 if not esquerda else old[0] - 3 + bw / 2
        ccy = (old[1] + old[3]) / 2
        if (esquerda or escura) and x0s:
            pad = tam * 0.28
            # estilo story: uma caixa por linha, alinhada à esquerda, cada uma cobrindo a linha PT antiga
            larg_old = [b_ - a_ for a_, b_ in zip(x0s, x1s)]
            ws = [max(largura(l, f), larg_old[k] if k < len(larg_old) else 0) + 2 * pad for k, l in enumerate(linhas)]
            alt_l = asc + desc + 1.2 * pad
            bw, bh = max(ws), passo * (len(linhas) - 1) + alt_l
            img = Image.new("RGBA", (int(bw) + 4, int(bh) + 4), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            cor_caixa = bl.get("_cor_caixa", (0, 0, 0)) if escura else (255, 255, 255)
            cor_txt = tuple(bl.get("cor_texto", (255, 255, 255) if escura else (0, 0, 0)))
            for k, l in enumerate(linhas):
                y = k * passo
                d.rounded_rectangle([0, y, ws[k], y + alt_l + (passo - alt_l if k < len(linhas) - 1 and passo > alt_l else 0)],
                                    radius=tam * 0.25, fill=cor_caixa + (255,))
            for k, l in enumerate(linhas):
                d.text((pad, k * passo + 0.6 * pad), l, font=f, fill=cor_txt + (255,))
            bl["_img"] = np.array(img)
            bl["_pos"] = (int(round(min(x0s) - pad)), int(round(centros[0] - (asc + desc) / 2 - 0.6 * pad)))
            bl["_tam"] = round(tam, 1)
            bl["_fonte"] = nome
            return
        img = Image.new("RGBA", (int(bw) + 4, int(bh) + 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cor_caixa = bl.get("_cor_caixa", (0, 0, 0)) if escura else (255, 255, 255)
        cor_txt = tuple(bl.get("cor_texto", (255, 255, 255) if escura else (0, 0, 0)))
        d.rounded_rectangle([0, 0, bw, bh], radius=tam * 0.32, fill=cor_caixa + (255,))
        y = (bh - alt) / 2
        for l in linhas:
            x = pad if esquerda else (bw - largura(l, f)) / 2
            d.text((x, y), l, font=f, fill=cor_txt + (255,))
            y += passo
        bl["_img"] = np.array(img)
        bl["_pos"] = (int(round(ccx - bw / 2)), int(round(ccy - bh / 2)))
    else:
        borda = max(2, int(round(tam * bl.get("contorno", 0.10)))) if tipo == "contorno" and not bl["_chapado"] else 0
        m = max(2 * borda, int(tam * 0.15)) + 2
        img = Image.new("RGBA", (int(larg + 2 * m), int(alt + 2 * m)), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        y = m
        pos = []
        for l in linhas:
            x = m if esquerda else (img.width - largura(l, f)) / 2
            pos.append((x, y, l))
            y += passo
        if tipo == "branco" and not bl["_chapado"]:
            # sombra suave, como o letreiro original
            sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ds = ImageDraw.Draw(sombra)
            for x, y, l in pos:
                ds.text((x + tam * 0.03, y + tam * 0.04), l, font=f, fill=(0, 0, 0, 150))
            img = Image.alpha_composite(img, sombra.filter(ImageFilter.GaussianBlur(tam * 0.06)))
            d = ImageDraw.Draw(img)
        for x, y, l in pos:
            if borda:
                d.text((x, y), l, font=f, fill=bl["_cor"] + (255,), stroke_width=borda, stroke_fill=(0, 0, 0, 255))
            else:
                d.text((x, y), l, font=f, fill=bl["_cor"] + (255,))
        bl["_img"] = np.array(img)
        px = (min(x0s) - m) if esquerda else (cx - img.width / 2)
        bl["_pos"] = (int(round(px)), int(round(cy - img.height / 2)))
    bl["_tam"] = round(tam, 1)
    bl["_fonte"] = nome


def colar(quadro, rgba, pos):
    x, y = pos
    h, w = rgba.shape[:2]
    xa, ya = max(0, x), max(0, y)
    xb, yb = min(W, x + w), min(H, y + h)
    if xb <= xa or yb <= ya:
        return
    sub = rgba[ya - y:yb - y, xa - x:xb - x].astype(np.float32)
    a = sub[..., 3:4] / 255.0
    dst = quadro[ya:yb, xa:xb].astype(np.float32)
    quadro[ya:yb, xa:xb] = (dst * (1 - a) + sub[..., 2::-1] * a).astype(np.uint8)


def sobrepoe(a, b):
    ax0, ay0, ax1, ay1 = a["bbox"]
    bx0, by0, bx1, by1 = b["bbox"]
    return min(ax1, bx1) > max(ax0, bx0) and min(ay1, by1) + 15 > max(ay0, by0)


def main():
    ff, video, cfg_path, original, saida = sys.argv[1:6]
    ini = float(sys.argv[6]) if len(sys.argv) > 7 else None
    dur = float(sys.argv[7]) if len(sys.argv) > 7 else None
    cfg = json.load(open(cfg_path))
    blocos = [b for b in cfg["blocos"] if b.get("acao") != "manter" and b.get("es") is not None]
    for b in blocos:
        b["_roi"] = recorte(b["bbox"], 70)
        b["_f0"] = max(0, int((b["t0"] - 0.45) * FPS))
        b["_f1"] = int((b["t1"] + 0.15) * FPS)
        b["_tintas"] = {}

    # passada 1: referência (quadro com o texto completo) e máscaras de cada quadro na janela do bloco
    a0 = max(0, ini - 2) if ini is not None else None
    for i, q in ler_quadros(ff, video, a0, (dur + 4) if dur else None):
        for b in blocos:
            if b["_f0"] <= i <= b["_f1"]:
                x0, y0, x1, y1 = b["_roi"]
                roi = q[y0:y1, x0:x1]
                _, lc, le, br = mascaras(roi, b.get("limiar", 205))
                b["_tintas"][i] = (np.packbits(lc), np.packbits(le), np.packbits(br))
                if b["t0"] * FPS <= i <= (b["t1"] - 0.2) * FPS and i % 3 == 0:
                    z = zona_linhas(b, (x0, y0), lc.shape)
                    b.setdefault("_cands", []).append((int(((lc | le | br) & z).sum()), i, roi.copy()))
    for b in blocos:
        cands = b.pop("_cands", [])
        if not cands:
            continue
        mx = max(c[0] for c in cands)
        meio = (b["t0"] + b["t1"]) / 2 * FPS
        _, fi, roi = min((c for c in cands if c[0] >= 0.9 * mx), key=lambda c: abs(c[1] - meio))
        b["_fref"] = fi
        x0, y0, _, _ = b["_roi"]
        preparar(b, roi, (x0, y0))
        ref = b["_ref"].astype(bool)
        refd = cv2.dilate(b["_ref"], K7).astype(bool)
        nref = max(1, ref.sum())
        shape = ref.shape

        def un(pk):
            return np.unpackbits(pk)[:shape[0] * shape[1]].reshape(shape)
        pres = {}
        for i, (plc, ple, pbr) in b["_tintas"].items():
            m = tinta(b["tipo"], un(plc), un(ple), un(pbr), b["_zona"]).astype(bool)
            pres[i] = (m & refd).sum() / nref
        b["_presenca"] = pres
        on = [i for i in sorted(pres) if pres[i] > 0.5]
        if on:
            trechos, comeco = [], on[0]
            for a, c in zip(on, on[1:] + [None]):
                if c is None or c != a + 1:
                    trechos.append((comeco, a))
                    comeco = c
            # junta trechos separados por falha curta (mão passando na frente)
            unidos = [list(trechos[0])]
            for a, c in trechos[1:]:
                if a - unidos[-1][1] <= 8:
                    unidos[-1][1] = c
                else:
                    unidos.append([a, c])
            # o bloco vem de um único texto contínuo do OCR: vale do primeiro ao último quadro em que aparece
            # (texto branco sobre fundo que clareia some da detecção por alguns quadros e volta)
            b["_d0"], b["_d1"] = unidos[0][0], unidos[-1][1]
        else:
            b["_d0"], b["_d1"] = int(b["t0"] * FPS), int(b["t1"] * FPS)
        # nunca menos que o intervalo em que o OCR viu o texto (letreiro longo que atravessa corte de cena)
        b["_d0"] = min(b["_d0"], int(round(b["t0"] * FPS)))
        b["_d1"] = max(b["_d1"], int(round((b["t1"] - 1 / 3) * FPS)))
        b["_mref"] = cv2.dilate(b["_ref"], el(31) if b.get("_chapado") else el(21))
        b["_mref7"] = cv2.dilate(b["_ref"], K13)
    for b in blocos:
        b.pop("_tintas", None)
    prontos = sorted([b for b in blocos if "_ref" in b], key=lambda b: b["_d0"])
    # no mesmo lugar, o bloco anterior sai quando o próximo entra (nunca 2 legendas sobrepostas)
    for k, a in enumerate(prontos):
        for b in prontos[k + 1:]:
            if b["_img"] is not None and b["_d0"] > a["_d0"] and sobrepoe(a, b) and b["_d0"] <= a["_d1"]:
                a["_d1"] = b["_d0"] - 1

    # passada 2: apaga PT e desenha ES
    cmd = [ff, "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-"]
    if ini is not None:
        cmd += ["-ss", str(ini), "-t", str(dur)]
    cmd += ["-i", original, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", "-shortest", saida]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, q in ler_quadros(ff, video, ini, dur):
        q = q.copy()
        ativos = [b for b in prontos if b["_f0"] <= i <= b["_f1"]]
        for b in ativos:
            if b["tipo"] in ("caixa", "caixa_escura"):
                continue
            perto = b["_d0"] - 10 <= i <= b["_d1"] + 10      # cobre entrada e saída com fade
            if b["_presenca"].get(i, 0) < 0.05 and not perto:
                continue
            x0, y0, x1, y1 = b["_roi"]
            roi = q[y0:y1, x0:x1]
            if b.get("_chapado"):
                roi[b["_mref"].astype(bool)] = b["_cor_fundo"]
                continue
            _, lc, le, br = mascaras(roi, b.get("limiar", 205))
            m = cv2.dilate(tinta(b["tipo"], lc, le, br, b["_zona"]), K13)
            if perto:
                m = m | b["_mref7"]
            m = m & b["_mref"]
            if m.any():
                q[y0:y1, x0:x1] = cv2.inpaint(roi, m * 255, 7, cv2.INPAINT_TELEA)
        for b in ativos:
            if b["_d0"] <= i <= b["_d1"] and b["_img"] is not None:
                colar(q, b["_img"], b["_pos"])
        enc.stdin.write(q.tobytes())
    enc.stdin.close()
    enc.wait()
    rel = [{"id": b["id"], "tipo": b.get("tipo"), "fonte": b.get("_fonte"), "tam": b.get("_tam"),
            "de": round(b.get("_d0", 0) / FPS, 2), "ate": round(b.get("_d1", 0) / FPS, 2),
            "pt": b["pt"], "es": b["es"]} for b in blocos]
    json.dump(rel, open(saida + ".relatorio.json", "w"), ensure_ascii=False, indent=1)
    print("ok", saida)


if __name__ == "__main__":
    main()
