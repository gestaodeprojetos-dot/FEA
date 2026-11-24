#!/usr/bin/env python3
"""FEA: criativo de anúncio para e-book/livro (tela dividida, livro arrastando, fotos do livro).

Uso:
    python3 fea_criativo_ebook.py projeto.json [--so N] [--preview]

projeto.json (um lote):
{
  "ffmpeg": "...", "fontes": "pasta com Montserrat-*.ttf",
  "capa": "capa plana do livro (PNG)", "fundo": "banner para fundo do CTA",
  "imagens": "pasta com as fotos extraídas (pdfimages -png -p)",
  "sfx": {"whoosh": "...", "whoosh2": "...", "page": "...", "pop": "...", "boom": "..."},
  "legendas_fig": {"044": "Necrose cutânea após preenchimento labial", ...},
  "videos": [
    {"entrada": "IMG.MOV", "transcricao": "IMG.json", "saida": "1- Titulo.mp4",
     "titulo": "Texto do gancho", "destaque": ["palavra em dourado"],
     "inicio": 0, "fim": 57.0, "trilha": "m1.wav",
     "cenas": [[0, 3, "full"], [3, 6.5, "livro", "+200 páginas"],
               [10.4, 15.2, "split", ["034-003", "093-002"]], [48.6, 57, "cta"]]}
  ]
}
Tipos de cena: full (vídeo bruto em tela cheia, zoom lento e selo do livro), split (bruto em cima,
foto clínica do livro embaixo, trocando a cada parte), livro (capa entra arrastada sobre o bruto
desfocado), cta (capa + botão "Clique em Saiba Mais"). Trecho sem cena = full.
Saída H.264 CRF 18, AAC 192k (nunca HEVC). Voz original, trilha baixa com ducking, efeitos sonoros.
"""
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
AZUL_ESC = (6, 22, 52)
AZUL = (13, 59, 122)
DOURADO = (242, 163, 58)
BRANCO = (255, 255, 255)

CORRECOES = [
    (r"\bpra\b", "para"), (r"\bPra\b", "Para"),
    (r"aço alurônico", "ácido hialurônico"), (r"ácido (lorônico|neurônico|alurônico)", "ácido hialurônico"),
    (r"\bamorose\b", "amaurose"), (r"\bintercoências\b", "intercorrências"),
    (r"Estava Mais", "Saiba Mais"), (r"Sabamais", "Saiba Mais"),
    (r"imediato é vitalício", "imediato e vitalício"),
]
DESTAQUES = ["intercorrência", "intercorrências", "isquêmicas", "necrose", "protocolos", "diagnóstico",
             "diagnósticos", "tratamento", "tratamentos", "vitalício", "vitalício.", "imediato",
             "200", "páginas", "videoaulas", "amaurose", "cegueira", "angioedema", "segurança", "inchaço",
             "livro", "zonas", "risco", "ultrassonografia", "anatomia", "cadáveres", "frescos", "pesadelo",
             "brincadeira", "graves", "5", "anos"]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_back(t):
    t = max(0.0, min(1.0, t))
    c1, c3 = 1.4, 2.4
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


class Fontes:
    def __init__(self, pasta):
        self.p = pasta
        self.cache = {}

    def __call__(self, peso, tam):
        k = (peso, tam)
        if k not in self.cache:
            self.cache[k] = ImageFont.truetype(os.path.join(self.p, f"Montserrat-{peso}.ttf"), tam)
        return self.cache[k]


def arredondar(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m)
    return im


def sombra(im, raio=28, deslocy=18, opac=170):
    pad = raio * 3
    base = Image.new("RGBA", (im.size[0] + pad * 2, im.size[1] + pad * 2), (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: v * opac // 255)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 255))
    sh.putalpha(a)
    base.paste(sh, (pad, pad + deslocy), sh)
    base = base.filter(ImageFilter.GaussianBlur(raio))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def texto_contorno(d, xy, txt, fonte, cor, contorno=6, cor_c=(0, 0, 0), anchor="mm"):
    d.text(xy, txt, font=fonte, fill=cor, stroke_width=contorno, stroke_fill=cor_c, anchor=anchor)


# ---------------------------------------------------------------- recursos
class Recursos:
    def __init__(self, cfg):
        self.f = Fontes(cfg["fontes"])
        capa = Image.open(cfg["capa"]).convert("RGB")
        a = np.asarray(capa).astype(int)
        m = (a[:, :, 2] > a[:, :, 0] + 40) & (a[:, :, 0] < 60)
        ys, xs = np.where(m)
        capa = capa.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        self.capa = capa
        fundo = Image.open(cfg["fundo"]).convert("RGB")
        # fundo do CTA: lado esquerdo do banner (sem texto), esticado e desfocado
        fw, fh = fundo.size
        fundo = fundo.crop((0, 0, int(fw * 0.42), fh)).resize((W, H), Image.LANCZOS)
        fundo = fundo.filter(ImageFilter.GaussianBlur(18))
        esc = Image.new("RGB", (W, H), AZUL_ESC)
        self.fundo_cta = Image.blend(fundo, esc, 0.35)
        self.pasta_img = cfg["imagens"]
        self.leg_fig = cfg.get("legendas_fig", {})
        self.cards = {}
        self.selo = self._selo()

    def _selo(self):
        c = self.capa.copy()
        c.thumbnail((150, 210), Image.LANCZOS)
        c = arredondar(c, 8)
        s, pad = sombra(c, 10, 6, 150)
        return s, pad

    def foto(self, cid):
        """Card da foto clínica: moldura dourada, cantos suaves, etiqueta com o nome da figura."""
        if cid in self.cards:
            return self.cards[cid]
        f = os.path.join(self.pasta_img, f"x-{cid}.png")
        im = Image.open(f)
        # máscara (pdfimages grava o alfa como a imagem seguinte, em L)
        pg, n = cid.split("-")
        mf = os.path.join(self.pasta_img, f"x-{pg}-{int(n) + 1:03d}.png")
        if os.path.exists(mf):
            mk = Image.open(mf)
            if mk.mode == "L" and mk.size == im.size:
                fundo = Image.new("RGB", im.size, (255, 255, 255))
                fundo.paste(im.convert("RGB"), (0, 0), mk)
                im = fundo
        im = im.convert("RGB")
        maxw, maxh = 920, 760
        esc = min(maxw / im.width, maxh / im.height)
        im = im.resize((max(1, int(im.width * esc)), max(1, int(im.height * esc))), Image.LANCZOS)
        borda = 7
        quadro = Image.new("RGB", (im.width + borda * 2, im.height + borda * 2), DOURADO)
        quadro.paste(im, (borda, borda))
        quadro = arredondar(quadro, 14)
        card, pad = sombra(quadro, 26, 16, 190)
        leg = self.leg_fig.get(pg, "")
        self.cards[cid] = (card, pad, quadro.size, leg)
        return self.cards[cid]


# ---------------------------------------------------------------- legendas
def corrigir(t):
    for a, b in CORRECOES:
        t = re.sub(a, b, t)
    return t


def palavras(trans, ini, fim):
    out = []
    for s in trans:
        for w in s["words"]:
            if w["s"] >= ini - 0.05 and w["s"] < fim:
                out.append([w["s"] - ini, w["e"] - ini, w["w"].strip()])
    # correções que juntam duas palavras
    txt = " ".join(p[2] for p in out)
    txt2 = corrigir(txt)
    if txt2 != txt:
        toks = txt2.split(" ")
        if len(toks) == len(out):
            for p, t in zip(out, toks):
                p[2] = t
        else:  # recompõe palavra a palavra
            for p in out:
                p[2] = corrigir(p[2])
            for i in range(len(out) - 1):
                par = corrigir(out[i][2] + " " + out[i + 1][2])
                if par != out[i][2] + " " + out[i + 1][2] and len(par.split(" ")) == 2:
                    out[i][2], out[i + 1][2] = par.split(" ")
    return out


LIGACAO = {"e", "de", "do", "da", "no", "na", "o", "a", "os", "as", "com", "para", "em", "um", "uma", "que",
           "é", "eu", "você", "se", "ao", "por", "sua", "seu", "meu", "meus", "minhas", "todos", "todas", "mais"}


def blocos(ws, maxc=20, maxp=4):
    bl, cur = [], []
    for j, w in enumerate(ws):
        cur.append(w)
        txt = " ".join(x[2] for x in cur)
        fim_frase = w[2][-1:] in ",.!?"
        nxt = ws[j + 1][2] if j + 1 < len(ws) else ""
        if fim_frase or ((len(txt) >= maxc or len(cur) >= maxp) and (w[2].lower() not in LIGACAO or len(cur) >= maxp + 2)
                         and not (nxt.lower().strip(",.") == "mais" and w[2].lower() == "saiba")):
            bl.append(cur)
            cur = []
    if cur:
        bl.append(cur)
    out = []
    for i, b in enumerate(bl):
        a = b[0][0]
        e = b[-1][1] + 0.35
        if i + 1 < len(bl):
            e = min(e, bl[i + 1][0][0])
        out.append((a, e, b))
    return out


def norm(w):
    return re.sub(r"[^\wÀ-ú]", "", w.lower())


def desenhar_legenda(img, rec, bloco, t, y):
    a, e, ws = bloco
    d = ImageDraw.Draw(img)
    fonte = rec.f("ExtraBold", 66)
    toks = [w[2].rstrip(".") for w in ws]
    toks[0] = toks[0][0].lower() + toks[0][1:] if toks[0][:1].isupper() and toks[0] not in ("Saiba",) else toks[0]
    linha = " ".join(toks).rstrip(",")
    # quebra em 2 linhas se passar de 16 caracteres
    if len(linha) > 16 and len(toks) > 1:
        melhor = None
        for k in range(1, len(toks)):
            l1, l2 = " ".join(toks[:k]), " ".join(toks[k:])
            c = abs(len(l1) - len(l2))
            if melhor is None or c < melhor[0]:
                melhor = (c, k)
        linhas = [toks[:melhor[1]], toks[melhor[1]:]]
    else:
        linhas = [toks]
    # pop de entrada
    p = ease_back((t - a) / 0.18)
    esc = 0.82 + 0.18 * p
    lh = 78
    y0 = y - (len(linhas) - 1) * lh / 2
    for li, lt in enumerate(linhas):
        lt = [x.rstrip(",") if j == len(lt) - 1 and li == len(linhas) - 1 else x for j, x in enumerate(lt)]
        fonte_e = rec.f("ExtraBold", max(20, int(66 * esc)))
        larg = [d.textlength(x, font=fonte_e) for x in lt]
        esp = d.textlength(" ", font=fonte_e)
        total = sum(larg) + esp * (len(lt) - 1)
        x = W / 2 - total / 2
        for x_t, lw in zip(lt, larg):
            idx = toks.index(x_t) if x_t in toks else -1
            cor = DOURADO if (norm(x_t) in DESTAQUES or x_t.strip(",.") in ("Saiba", "Mais")) else BRANCO
            # palavra falada agora sobe um pouco de brilho
            d.text((x, y0 + li * lh), x_t, font=fonte_e, fill=cor, stroke_width=7, stroke_fill=(0, 0, 0),
                   anchor="lm")
            x += lw + esp


# ---------------------------------------------------------------- cenas
def cover_zoom(fr, z, cx=0.5, cy=0.5):
    """fr: Image W x H. Zoom z>=1 mantendo centro."""
    if z <= 1.001:
        return fr
    w, h = int(W / z), int(H / z)
    x0 = int((W - w) * cx)
    y0 = int((H - h) * cy)
    return fr.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)


def desfocado(fr, escuro=0.62):
    p = fr.resize((W // 10, H // 10), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
    return Image.blend(p, Image.new("RGB", (W, H), AZUL_ESC), escuro)


def capa_perspectiva(capa, larg, ang):
    """Capa com leve rotação 3D em Y (ang em graus, 0 = de frente)."""
    c = capa.resize((larg, int(capa.height * larg / capa.width)), Image.LANCZOS)
    w, h = c.size
    if abs(ang) < 0.5:
        return arredondar(c, 10)
    r = math.radians(ang)
    enc = math.cos(r)
    nw = max(10, int(w * enc))
    persp = math.sin(r) * 0.22 * h
    # lado mais distante encolhe
    if ang > 0:
        dst = [(0, 0), (nw, persp), (nw, h - persp), (0, h)]
    else:
        dst = [(0, -persp * 0), (nw, 0), (nw, h), (0, h)]
        dst = [(0, -persp), (nw, 0), (nw, h), (0, h + persp)]
    miny = min(p[1] for p in dst)
    dst = [(x, y - miny) for x, y in dst]
    oh = int(max(p[1] for p in dst)) + 1
    coeffs = _persp_coeffs(dst, [(0, 0), (w, 0), (w, h), (0, h)])
    out = arredondar(c, 10).transform((nw, oh), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    return out


def _persp_coeffs(pa, pb):
    m = []
    for p1, p2 in zip(pa, pb):
        m.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        m.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.array(m, dtype=float)
    B = np.array(pb, dtype=float).reshape(8)
    return np.linalg.solve(A, B).tolist()


def colar_centro(base, im, cx, cy):
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def chip(d, rec, cx, cy, txt, tam=40, cor_fundo=DOURADO, cor_txt=AZUL_ESC):
    f = rec.f("ExtraBold", tam)
    tw = d.textlength(txt, font=f)
    padx, alt = 34, tam + 34
    d.rounded_rectangle([cx - tw / 2 - padx, cy - alt / 2, cx + tw / 2 + padx, cy + alt / 2], alt // 2, fill=cor_fundo)
    d.text((cx, cy + 2), txt, font=f, fill=cor_txt, anchor="mm")


def cena_full(fr, rec, tl, dur, extra):
    z = 1.0 + 0.06 * (tl / max(dur, 0.1))
    img = cover_zoom(fr, z).convert("RGBA")
    s, pad = rec.selo
    # selo do livro no canto, entra deslizando
    p = ease(tl / 0.5)
    x = W - s.width + pad - 40 + int((1 - p) * 260)
    img.alpha_composite(s, (x, 150 - pad))
    return img, 1380


def cena_split(fr, rec, tl, dur, extra):
    fotos = extra if isinstance(extra, list) else [extra]
    img = Image.new("RGBA", (W, H), AZUL_ESC + (255,))
    # metade de cima: bruto (recorte central), entra empurrando de cima
    topo_h = 900
    z = 1.12 + 0.04 * (tl / max(dur, 0.1))
    fz = cover_zoom(fr, z, 0.5, 0.42)
    y0 = int((H - topo_h) * 0.42)
    topo = fz.crop((0, y0, W, y0 + topo_h))
    pe = ease(tl / 0.35)
    img.paste(topo, (0, int(-(1 - pe) * 200)))
    # metade de baixo: gradiente azul + card da foto
    grad = np.linspace(0, 1, H - topo_h)[:, None]
    g = (np.array(AZUL_ESC) * (1 - grad) + np.array(AZUL) * grad).astype(np.uint8)
    baixo = Image.fromarray(np.repeat(g[:, None, :], W, axis=1).reshape(H - topo_h, W, 3))
    img.paste(baixo, (0, topo_h))
    ImageDraw.Draw(img).rectangle([0, topo_h - 4, W, topo_h + 4], fill=DOURADO)
    n = len(fotos)
    parte = dur / n
    i = min(n - 1, int(tl / parte))
    tli = tl - i * parte
    card, pad, (qw, qh), leg = rec.foto(fotos[i])
    pin = ease(tli / 0.4)
    pout = ease((tli - (parte - 0.3)) / 0.3) if i < n - 1 else 0
    cx = W / 2 + (1 - pin) * W * 0.9 - pout * W * 0.9
    cy = topo_h + (H - topo_h) * 0.50
    esc = 0.96 + 0.04 * ease(tli / parte)
    c2 = card if abs(esc - 1) < 0.01 else card.resize((int(card.width * esc), int(card.height * esc)), Image.BILINEAR)
    colar_centro(img, c2, cx, cy)
    if leg:
        d = ImageDraw.Draw(img)
        f = rec.f("Bold", 30)
        ty = cy + qh * esc / 2 + 34
        if ty > H - 40:
            ty = H - 40
        tw = d.textlength(leg.upper(), font=f)
        d.rounded_rectangle([cx - tw / 2 - 20, ty - 24, cx + tw / 2 + 20, ty + 24], 24, fill=(6, 22, 52, 230),
                            outline=DOURADO, width=2)
        d.text((cx, ty + 1), leg.upper(), font=f, fill=DOURADO, anchor="mm")
    return img, topo_h


def cena_livro(fr, rec, tl, dur, extra):
    img = desfocado(fr, 0.5).convert("RGBA")
    # capa arrastada da direita com rotação, assenta no centro e flutua
    p = ease(tl / 0.7)
    ang = -38 * (1 - p)
    larg = int(560 + 40 * ease(tl / max(dur, 0.1)))
    c = capa_perspectiva(rec.capa, larg, ang)
    s, pad = sombra(c, 30, 24, 200)
    flut = math.sin(tl * 2.2) * 10 * p
    cx = W / 2 + (1 - p) * 900
    cy = H * 0.44 + flut
    colar_centro(img, s, cx, cy)
    if extra:
        d = ImageDraw.Draw(img)
        pc = ease((tl - 0.5) / 0.35)
        if pc > 0:
            chip(d, rec, W / 2, H * 0.44 + c.height / 2 + 90 + (1 - pc) * 60, extra, 44)
    return img, 1500


def cena_cta(fr, rec, tl, dur, extra):
    img = rec.fundo_cta.copy().convert("RGBA")
    p = ease(tl / 0.6)
    larg = 520
    c = capa_perspectiva(rec.capa, larg, -14 * (1 - p) + 0)
    s, pad = sombra(c, 30, 24, 210)
    flut = math.sin(tl * 2.0) * 12
    colar_centro(img, s, W / 2, H * 0.36 + (1 - p) * 300 + flut)
    d = ImageDraw.Draw(img)
    pb = ease_back((tl - 0.6) / 0.35)
    if tl > 0.6:
        pulso = 1 + 0.04 * math.sin((tl - 0.6) * 6.0)
        tam = int(58 * pulso * (0.6 + 0.4 * pb))
        f = rec.f("ExtraBold", max(10, tam))
        txt = "CLIQUE EM SAIBA MAIS"
        tw = d.textlength(txt, font=f)
        bx, by = W / 2, H * 0.68
        d.rounded_rectangle([bx - tw / 2 - 50, by - tam * 0.95, bx + tw / 2 + 50, by + tam * 0.95], int(tam * 0.95),
                            fill=DOURADO)
        d.text((bx, by + 2), txt, font=f, fill=AZUL_ESC, anchor="mm")
    pt = ease((tl - 1.0) / 0.4)
    if pt > 0:
        f2 = rec.f("Bold", 42)
        d.text((W / 2, H * 0.68 + 120 + (1 - pt) * 40), extra or "Acesso imediato e vitalício", font=f2,
               fill=(255, 255, 255, int(255 * pt)), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
    return img, 1640


CENAS = {"full": cena_full, "split": cena_split, "livro": cena_livro, "cta": cena_cta}


def desenhar_titulo(img, rec, titulo, dest, t):
    if t > 3.0:
        return
    d = ImageDraw.Draw(img)
    p = ease_back(t / 0.3)
    sai = ease((t - 2.7) / 0.3)
    tam = int(96 * (0.7 + 0.3 * p))
    f = rec.f("ExtraBold", max(10, tam))
    # quebra em linhas de até ~18 caracteres
    pal = titulo.split()
    linhas, cur = [], ""
    for w in pal:
        if len(cur) + len(w) + 1 > 18 and cur:
            linhas.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    linhas.append(cur)
    lh = int(tam * 1.02)
    y0 = H * 0.5 - (len(linhas) - 1) * lh / 2 - sai * 80
    alfa = int(255 * (1 - sai))
    destaques = {norm(x) for x in dest}
    caixa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(caixa)
    mw = max(d.textlength(l, font=f) for l in linhas)
    dc.rounded_rectangle([W / 2 - mw / 2 - 50, y0 - lh / 2 - 40, W / 2 + mw / 2 + 50, y0 + (len(linhas) - 0.5) * lh + 40],
                         36, fill=AZUL_ESC + (int(185 * (1 - sai)),), outline=DOURADO + (alfa,), width=4)
    img.alpha_composite(caixa)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(linhas):
        ws = l.split()
        larg = [d.textlength(w, font=f) for w in ws]
        esp = d.textlength(" ", font=f)
        x = W / 2 - (sum(larg) + esp * (len(ws) - 1)) / 2
        for w, lw in zip(ws, larg):
            cor = DOURADO if norm(w) in destaques else BRANCO
            d.text((x, y0 + i * lh), w, font=f, fill=cor + (alfa,), stroke_width=5, stroke_fill=(0, 0, 0, alfa),
                   anchor="lm")
            x += lw + esp


# ---------------------------------------------------------------- render
def render(cfg, v, rec, preview=False):
    ff = cfg["ffmpeg"]
    ini, fim = v["inicio"], v["fim"]
    dur = fim - ini
    trans = json.load(open(v["transcricao"]))
    ws = palavras(trans, ini, fim)
    bls = blocos(ws)
    cenas = sorted(v["cenas"], key=lambda c: c[0])

    def cena_em(t):
        for c in cenas:
            if c[0] <= t < c[1]:
                return c
        return [t, t + 1, "full"]

    saida = v["saida"]
    tmpv = saida + ".video.mp4"
    nf = int(round(dur * FPS))
    dec = subprocess.Popen([ff, "-loglevel", "error", "-ss", str(ini), "-i", v["entrada"], "-t", str(dur),
                            "-vf", f"scale={W}:{H}:flags=bicubic,fps={FPS}", "-pix_fmt", "rgb24", "-f", "rawvideo",
                            "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([ff, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast" if preview else "medium",
                            "-crf", "28" if preview else "18", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    ultimo = None
    sfx = []  # (tempo, nome, volume)
    cena_ant = None
    foto_ant = None
    for i in range(nf):
        t = i / FPS
        buf = dec.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            ultimo = Image.frombuffer("RGB", (W, H), buf, "raw", "RGB", 0, 1)
        fr = ultimo
        c = cena_em(t)
        tl, cd = t - c[0], c[1] - c[0]
        extra = c[3] if len(c) > 3 else None
        img, ylen = CENAS[c[2]](fr, rec, tl, cd, extra)
        # efeitos sonoros nas trocas
        chave = (c[0], c[2])
        if chave != cena_ant:
            if i == 0:
                sfx.append((0.0, "boom", 0.55))
            elif c[2] in ("split", "livro"):
                sfx.append((t, "whoosh", 0.45))
            elif c[2] == "cta":
                sfx.append((t, "whoosh2", 0.45))
                sfx.append((t + 0.6, "pop", 0.6))
            else:
                sfx.append((t, "whoosh2", 0.30))
            cena_ant = chave
        if c[2] == "split":
            fotos = extra if isinstance(extra, list) else [extra]
            k = min(len(fotos) - 1, int(tl / (cd / len(fotos))))
            if (c[0], k) != foto_ant:
                if k > 0:
                    sfx.append((t, "page", 0.55))
                foto_ant = (c[0], k)
        if c[2] == "livro" and abs(tl - 0.5) < 0.5 / FPS and extra:
            sfx.append((t, "pop", 0.45))
        desenhar_titulo(img, rec, v["titulo"], v.get("destaque", []), t)
        if t >= 3.0:
            for b in bls:
                if b[0] <= t < b[1]:
                    desenhar_legenda(img, rec, b, t, ylen)
                    break
        # fade final
        if t > dur - 0.4:
            k = (t - (dur - 0.4)) / 0.4
            img = Image.blend(img.convert("RGB"), Image.new("RGB", (W, H), (0, 0, 0)), k * 0.6).convert("RGBA")
        enc.stdin.write(img.convert("RGB").tobytes())
        if i % 150 == 0:
            print(f"  {os.path.basename(saida)}: {t:.0f}/{dur:.0f}s", flush=True)
    dec.stdout.close()
    dec.wait()
    enc.stdin.close()
    enc.wait()
    mixar(cfg, v, tmpv, saida, dur, sfx)
    os.remove(tmpv)


def lufs(ff, args):
    r = subprocess.run([ff, "-hide_banner"] + args + ["-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -23.0


def mixar(cfg, v, tmpv, saida, dur, sfx):
    ff = cfg["ffmpeg"]
    ini = v["inicio"]
    # voz em -16 LUFS (padrão de anúncio no celular), trilha ~20 dB abaixo da voz
    lv = lufs(ff, ["-ss", str(ini), "-t", str(dur), "-i", v["entrada"], "-vn"])
    lm = lufs(ff, ["-t", "60", "-i", v["trilha"]])
    v.setdefault("voz_vol", round(10 ** ((-16 - lv) / 20), 3))
    v.setdefault("trilha_vol", round(10 ** ((v.get("trilha_lufs", -35) - lm) / 20), 3))
    print(f"  voz {lv} LUFS x{v['voz_vol']} | trilha {lm} LUFS x{v['trilha_vol']}", flush=True)
    ins = ["-i", tmpv, "-ss", str(ini), "-t", str(dur), "-i", v["entrada"], "-stream_loop", "-1", "-i", v["trilha"]]
    filt = [f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume={v['voz_vol']},"
            f"afade=t=out:st={dur - 0.35}:d=0.35,asplit=2[voz][vsc]",
            f"[2:a]aresample=48000,atrim=0:{dur},volume={v['trilha_vol']},"
            f"afade=t=in:d=0.8,afade=t=out:st={dur - 1.2}:d=1.2[mus0]",
            "[mus0][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[mus]"]
    mix = ["[voz]", "[mus]"]
    for k, (t, nome, vol) in enumerate(sfx):
        ins += ["-i", cfg["sfx"][nome]]
        ms = int(t * 1000)
        filt.append(f"[{k + 3}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},"
                    f"adelay={ms}|{ms}[s{k}]")
        mix.append(f"[s{k}]")
    filt.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
    cmd = [ff, "-loglevel", "error", "-y"] + ins + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]",
                                                   "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                                                   "-t", str(dur), "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)


def main():
    cfg = json.load(open(sys.argv[1]))
    so = None
    if "--so" in sys.argv:
        so = [int(x) for x in sys.argv[sys.argv.index("--so") + 1].split(",")]
    preview = "--preview" in sys.argv
    rec = Recursos(cfg)
    for n, v in enumerate(cfg["videos"], 1):
        if so and n not in so:
            continue
        print(f"render {n}: {v['saida']}", flush=True)
        render(cfg, v, rec, preview)
    print("FIM")


if __name__ == "__main__":
    main()
