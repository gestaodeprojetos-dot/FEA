#!/usr/bin/env python3
"""FEA: edição dinâmica de Reels no estilo "Volpe" (pedido da Keila, 22/10/2026).

Diferente do fea_editar_video.py (título fixo + legenda em bloco), aqui o vídeo é montado
quadro a quadro em Python (PIL) para ter os três ganchos e os cortes de impacto:

  - gancho visual: tela dividida (imagem de impacto em cima, Dr. embaixo) com flash e zoom
    a cada troca de imagem; imagens com tratamento "sinistro" (menos cor, mais contraste,
    vinheta) para olheira, flacidez etc.
  - gancho escrito: 2 a 3 linhas em caixas no meio da tela, uma delas em destaque roxo FEA.
  - gancho falado: a primeira frase do Dr., sem legenda enquanto o gancho escrito está na tela.
  - legenda de 1 a 3 palavras por vez (ExtraBold branca com sombra), no meio da tela.
  - corte de respiros (pausas longas encurtadas) e zoom alternado no Dr. a cada trecho.
  - produto recortado sem fundo (rembg) aparecendo com "pop" ao lado da cabeça.
  - cartela de autoridade com fundo desfocado e ícone de comentário no fim.

Uso:
    python3 fea_editar_dinamico.py projeto.json [--previa]

projeto.json (tempos em segundos do BRUTO; o script converte para a linha do tempo editada):
{
  "ffmpeg": "/caminho/ffmpeg", "fonts": "fonts/",
  "entrada": "brutos/IMG_7935.MOV", "transcricao": "tr/IMG_7935.json", "saida": "out/x.mp4",
  "rosto": [0.48, 0.40],                 # centro do rosto do Dr. (fração do quadro)
  "manter": [[0, 3.85], [5.8, 59.75]],
  "zoom": [1.0, 1.12],                   # zoom alternado por trecho de "manter"
  "pausa_max": 0.35,                     # pausas maiores que isso são encurtadas
  "gancho": {"linhas": ["...", "...", "..."], "destaque": 1, "ate": 11.8},
  "broll": [{"ini": 0, "fim": 1.3, "img": "img/a.jpg"},
            {"ini": 1.3, "fim": 2.5, "video": "modelo.mp4", "t0": 8.0, "crop": [0, 150, 576, 512]}],
  "produtos": [{"ini": 19.6, "fim": 20.6, "png": "prod/yvoire.png"}],
  "vitrine": {"ini": 29.5, "fim": 31.5, "pngs": ["..."]},
  "cartela": {"ini": 14.2, "fim": 18.9, "linha1": "Dr. João Pithon", "linha2": "reologia das olheiras"},
  "comentario": {"ini": 62.0, "fim": 99},
  "frases": [["solo infector", "swelling factor"]],   # troca de palavras na legenda (pode juntar 2)
  "correcoes": [["\\\\bLift\\\\b", "Lyft"]]
}
"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fea_editar_video import NOMES_PROPRIOS, corrigir, encaixar_cortes, perfil_voz  # noqa: E402

W, H, FPS = 1080, 1920, 30
ROXO = (91, 69, 153)
LAVANDA = (208, 209, 233)
METADE = H // 2


# ---------------------------------------------------------------- linha do tempo

def apertar_pausas(manter, db, limiar, passo, pausa_max):
    """Divide cada trecho nos silêncios maiores que pausa_max, deixando 0,12 s de respiro de cada lado."""
    saida = []
    for k, (a, b) in enumerate(manter):
        i0, i1 = int(a / passo), int(b / passo)
        cortes, ini_sil = [], None
        for i in range(i0, i1):
            if db[i] < limiar:
                ini_sil = i if ini_sil is None else ini_sil
            else:
                if ini_sil is not None and (i - ini_sil) * passo > pausa_max:
                    cortes.append((ini_sil * passo + 0.12, i * passo - 0.12))
                ini_sil = None
        t = a
        for s, e in cortes:
            if s - t > 0.2:
                saida.append([t, s, k])
            t = e
        saida.append([t, b, k])
    return saida


class Mapa:
    def __init__(self, trechos):
        self.trechos, off = [], 0.0
        for a, b, k in trechos:
            self.trechos.append((a, b, off, k))
            off += b - a
        self.dur = off

    def __call__(self, t):
        for a, b, off, _ in self.trechos:
            if t < a:
                return off
            if t < b:
                return off + t - a
        return self.dur


# ---------------------------------------------------------------- legenda

def palavras_editadas(trans, mapa, frases, correcoes):
    ws = [dict(p, w=p["w"].strip()) for s in trans for p in s["words"] if p["w"].strip()]
    # frases: junta palavras vizinhas ("solo infector," -> "swelling factor,")
    for de, para in frases:
        n = len(de.split())
        k = 0
        while k + n <= len(ws):
            trecho = " ".join(w["w"] for w in ws[k:k + n])
            limpo = re.sub(r"[.,?!]", "", trecho).lower()
            if limpo == de.lower():
                pont = re.findall(r"[.,?!]+$", trecho)
                ws[k:k + n] = [{"s": ws[k]["s"], "e": ws[k + n - 1]["e"], "w": para + (pont[0] if pont else "")}]
            k += 1
    saida = []
    for p in ws:
        meio = (p["s"] + p["e"]) / 2
        dentro = any(a <= meio < b for a, b, _, _ in mapa.trechos)
        if dentro:
            saida.append({"w": corrigir(p["w"], correcoes), "s": mapa(p["s"]), "e": mapa(p["e"])})
    return saida


NOMES = NOMES_PROPRIOS | {"Voluma", "Lyft", "Juvéderm", "Gel", "Yvoire", "Perfectha", "Dr", "Dr."}


def blocos(palavras, max_pal=3, max_chars=18):
    out, cur = [], []
    for k, p in enumerate(palavras):
        cur.append(p)
        texto = " ".join(x["w"] for x in cur)
        prox = palavras[k + 1] if k + 1 < len(palavras) else None
        fim_frase = re.search(r"[.?!,]$", p["w"])
        pausa = prox is not None and (prox["s"] - p["e"] > 0.3 or prox["w"][:1].isupper() and re.sub(r"[.,?!]", "", prox["w"]) not in NOMES)
        cheio = len(cur) >= max_pal or (prox is not None and len(texto) + 1 + len(prox["w"]) > max_chars)
        if prox is None or fim_frase or pausa or cheio:
            out.append(cur)
            cur = []
    res = []
    for k, b in enumerate(out):
        ini = b[0]["s"]
        fim = out[k + 1][0]["s"] if k + 1 < len(out) else b[-1]["e"] + 0.4
        fim = min(fim, b[-1]["e"] + 0.6)
        texto = " ".join(x["w"] for x in b)
        texto = re.sub(r"[.;]$", "", re.sub(r" -(\w)", r"-\1", texto))   # "pré -maxila" -> "pré-maxila"; sem ponto final
        res.append((ini, fim, texto))
    return res


# ---------------------------------------------------------------- desenho

class Fontes:
    def __init__(self, pasta):
        self.p = pasta
        self.cache = {}

    def __call__(self, peso, tam):
        k = (peso, tam)
        if k not in self.cache:
            self.cache[k] = ImageFont.truetype(os.path.join(self.p, f"Montserrat-{peso}.ttf"), tam)
        return self.cache[k]


def texto_sombra(texto, fonte, cor=(255, 255, 255), sombra=8, largura_max=None):
    """Texto branco com sombra suave (como no Volpe). Devolve RGBA recortado."""
    linhas = [texto]
    if largura_max and fonte.getlength(texto) > largura_max:
        pal = texto.split()
        meio = min(range(1, len(pal)), key=lambda i: abs(fonte.getlength(" ".join(pal[:i])) - fonte.getlength(" ".join(pal[i:]))))
        linhas = [" ".join(pal[:meio]), " ".join(pal[meio:])]
    asc, desc = fonte.getmetrics()
    lh = int((asc + desc) * 1.0)
    lw = int(max(fonte.getlength(l) for l in linhas))
    pad = sombra * 3
    im = Image.new("RGBA", (lw + 2 * pad, lh * len(linhas) + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(im), ImageDraw.Draw(sh)
    for i, l in enumerate(linhas):
        x = pad + (lw - fonte.getlength(l)) / 2
        y = pad + i * lh
        ds.text((x + 2, y + 4), l, font=fonte, fill=(0, 0, 0, 230), stroke_width=3, stroke_fill=(0, 0, 0, 230))
        d.text((x, y), l, font=fonte, fill=cor + (255,), stroke_width=2, stroke_fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(sombra))
    sh.alpha_composite(im)
    return sh


def gancho_img(linhas, destaque, fonte):
    """Caixas encostadas, como o gancho do Volpe: branca com texto preto; a de destaque em roxo FEA."""
    asc, desc = fonte.getmetrics()
    padx, pady = 18, 8
    alt = asc + desc + 2 * pady
    larg = [int(fonte.getlength(l)) + 2 * padx for l in linhas]
    Wt = max(larg)
    im = Image.new("RGBA", (Wt, alt * len(linhas)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(linhas):
        x0 = (Wt - larg[i]) // 2
        fundo, cor = ((ROXO, (255, 255, 255)) if i == destaque else ((255, 255, 255), (20, 20, 20)))
        d.rectangle([x0, i * alt, x0 + larg[i], (i + 1) * alt], fill=fundo + (255,))
        d.text((x0 + padx, i * alt + pady), l, font=fonte, fill=cor)
    return im


def icone_comentario(tam=260):
    s = 4
    im = Image.new("RGBA", (tam * s, tam * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = 16 * s
    m = 20 * s
    d.rounded_rectangle([m, m, tam * s - m, int(tam * s * 0.72)], radius=60 * s, outline=(255, 255, 255, 255), width=lw)
    # rabinho do balão
    bx = int(tam * s * 0.30)
    by = int(tam * s * 0.72) - lw // 2
    d.polygon([(bx, by), (bx + 70 * s, by), (bx - 10 * s, by + 70 * s)], fill=(255, 255, 255, 255))
    for k in range(3):
        cx = int(tam * s * (0.33 + 0.17 * k))
        cy = int(tam * s * 0.43)
        r = 14 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
    im = im.resize((tam, tam), Image.LANCZOS)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 160), (0, 0), im)
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    sh.alpha_composite(im)
    return sh


def vinheta(w, h, forca=0.55):
    y, x = np.ogrid[-1:1:h * 1j, -1:1:w * 1j]
    r = np.sqrt(x ** 2 * 0.9 + y ** 2)
    m = np.clip(1 - forca * np.clip(r - 0.35, 0, None) ** 1.6, 0, 1)
    return m[..., None]


VIN = None


def sinistro(im, cor=0.65, contraste=1.25, brilho=0.92):
    """Tratamento de impacto: menos cor, mais contraste, leve tom frio e vinheta."""
    global VIN
    im = ImageEnhance.Color(im).enhance(cor)
    im = ImageEnhance.Contrast(im).enhance(contraste)
    im = ImageEnhance.Brightness(im).enhance(brilho)
    a = np.asarray(im).astype(np.float32)
    a[..., 2] *= 1.04
    a[..., 0] *= 0.97
    if VIN is None or VIN.shape[:2] != a.shape[:2]:
        VIN = vinheta(a.shape[1], a.shape[0])
    a *= VIN
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def cobrir(im, w, h, foco=(0.5, 0.5)):
    esc = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * esc), math.ceil(im.height * esc)), Image.LANCZOS)
    x = int((im.width - w) * foco[0])
    y = int((im.height - h) * foco[1])
    return im.crop((x, y, x + w, y + h))


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def pop(t, dur=0.28):
    """Escala do "pop": cresce até 1,08 e assenta em 1,0."""
    if t >= dur:
        return 1.0
    x = t / dur
    return 0.55 + 0.53 * ease(x) - 0.08 * max(0, x - 0.7) / 0.3


# ---------------------------------------------------------------- render

def preparar_broll(cfg, ff, mapa, pasta_tmp):
    itens = []
    for k, b in enumerate(cfg.get("broll", [])):
        ini, fim = mapa(b["ini"]), mapa(b["fim"])
        if fim - ini < 0.1:
            continue
        item = {"ini": ini, "fim": fim}
        if "img" in b:
            im = Image.open(b["img"]).convert("RGB")
            big = cobrir(im, int(W * 1.12), int(METADE * 1.12), tuple(b.get("foco", (0.5, 0.45))))
            item["img"] = sinistro(big, **b.get("tratamento", {}))
        else:
            n = int(math.ceil((fim - ini) * FPS)) + 2
            x, y, w, h = b["crop"]
            out = os.path.join(pasta_tmp, f"broll{k}_%04d.jpg")
            subprocess.run([ff, "-v", "error", "-y", "-ss", str(b["t0"]), "-i", b["video"], "-frames:v", str(n),
                            "-vf", f"fps={FPS},crop={w}:{h}:{x}:{y},scale={W}:{METADE}:flags=lanczos",
                            "-q:v", "2", out], check=True)
            item["frames"] = [out % (i + 1) for i in range(n) if os.path.exists(out % (i + 1))]
            item["trat"] = b.get("tratamento", {"cor": 0.8, "contraste": 1.18, "brilho": 0.95})
        itens.append(item)
    return itens


def quadro_broll(item, t):
    lt = t - item["ini"]
    if "img" in item:
        prog = lt / max(0.1, item["fim"] - item["ini"])
        z = 1.0 + 0.10 * prog + 0.06 * (1 - ease(lt / 0.25))   # Ken Burns + soco no início
        big = item["img"]
        w, h = int(W * 1.12 / z), int(METADE * 1.12 / z)
        x, y = (big.width - w) // 2, (big.height - h) // 2
        return big.crop((x, y, x + w, y + h)).resize((W, METADE), Image.BILINEAR)
    i = min(int(lt * FPS), len(item["frames"]) - 1)
    im = sinistro(Image.open(item["frames"][i]).convert("RGB"), **item["trat"])
    z = 1.0 + 0.06 * (1 - ease(lt / 0.25))
    if z > 1.001:
        w, h = int(W / z), int(METADE / z)
        im = im.crop(((W - w) // 2, (METADE - h) // 2, (W - w) // 2 + w, (METADE - h) // 2 + h)).resize((W, METADE), Image.BILINEAR)
    return im


def renderizar(cfg, previa=False):
    ff = cfg["ffmpeg"]
    fontes = Fontes(cfg["fonts"])
    pasta_tmp = cfg.get("tmp", "tmp_dinamico")
    os.makedirs(pasta_tmp, exist_ok=True)

    db, limiar, passo = perfil_voz(ff, cfg["entrada"])
    manter = encaixar_cortes(cfg["manter"], db, passo)
    trechos = apertar_pausas(manter, db, limiar, passo, cfg.get("pausa_max", 0.35))
    mapa = Mapa(trechos)
    print(f"duração editada: {mapa.dur:.1f} s em {len(trechos)} trechos", flush=True)

    # 1) base: Dr. cortado, com zoom alternado por trecho de "manter"
    zooms = cfg.get("zoom", [1.0, 1.12])
    fx, fy = cfg.get("rosto", (0.5, 0.4))
    partes, rot = [], []
    for i, (a, b, k) in enumerate(trechos):
        z = zooms[k % len(zooms)]
        cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
        cx = min(max(int(fx * W - cw / 2), 0), W - cw)
        cy = min(max(int(fy * H - ch * fy), 0), H - ch)
        partes.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,scale={W}:{H},crop={cw}:{ch}:{cx}:{cy},"
                      f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1[v{i}];"
                      f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
                      f"afade=t=out:st={max(0, b - a - 0.012):.3f}:d=0.012[a{i}];")
        rot.append(f"[v{i}][a{i}]")
    fc = "".join(partes) + "".join(rot) + f"concat=n={len(trechos)}:v=1:a=1[v][a]"
    base = os.path.join(pasta_tmp, "base.mp4")
    subprocess.run([ff, "-v", "error", "-y", "-i", cfg["entrada"], "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-c:a", "pcm_s16le",
                    base.replace(".mp4", ".mov")], check=True)
    base = base.replace(".mp4", ".mov")

    # 2) camadas
    trans = json.load(open(cfg["transcricao"], encoding="utf-8"))
    pal = palavras_editadas(trans, mapa, cfg.get("frases", []), cfg.get("correcoes", []))
    leg = blocos(pal)
    g = cfg.get("gancho")
    g_fim = mapa(g["ate"]) if g else 0
    g_img = gancho_img(g["linhas"], g.get("destaque", 1), fontes("Bold", 58)) if g else None
    broll = preparar_broll(cfg, ff, mapa, pasta_tmp)
    prods = []
    for p in cfg.get("produtos", []):
        im = Image.open(p["png"]).convert("RGBA")
        im.thumbnail((p.get("larg", 420), p.get("alt", 560)), Image.LANCZOS)
        prods.append({"ini": mapa(p["ini"]), "fim": mapa(p["fim"]), "img": im, "pos": p.get("pos", (0.78, 0.30))})
    vit = cfg.get("vitrine")
    if vit:
        ims = []
        for f in vit["pngs"]:
            im = Image.open(f).convert("RGBA")
            im.thumbnail((230, 330), Image.LANCZOS)
            ims.append(im)
        vit = {"ini": mapa(vit["ini"]), "fim": mapa(vit["fim"]), "ims": ims}
    cart = cfg.get("cartela")
    if cart:
        c1 = texto_sombra(cart["linha1"], fontes("ExtraBold", 66), sombra=10)
        c2 = texto_sombra(cart["linha2"], fontes("ExtraBoldItalic", 84), cor=LAVANDA, sombra=10, largura_max=W - 120)
        cart = {"ini": mapa(cart["ini"]), "fim": mapa(cart["fim"]), "c1": c1, "c2": c2}
    com = cfg.get("comentario")
    if com:
        com = {"ini": mapa(com["ini"]), "fim": min(mapa(com["fim"]), mapa.dur), "img": icone_comentario()}
    cache_leg = {}
    fonte_leg = fontes("ExtraBold", 64)

    # 3) quadro a quadro
    n_total = int(mapa.dur * FPS)
    if previa:
        n_total = min(n_total, int(cfg.get("previa_s", 12) * FPS))
    dec = subprocess.Popen([ff, "-v", "error", "-i", base, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    saida = cfg["saida"]
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
    enc = subprocess.Popen([ff, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", base, "-map", "0:v", "-map", "1:a",
                            "-c:v", "libx264", "-preset", "medium" if not previa else "veryfast",
                            "-crf", "18" if not previa else "23", "-pix_fmt", "yuv420p", "-profile:v", "high",
                            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                            saida], stdin=subprocess.PIPE)
    trocas_broll = sorted(round(b["ini"], 3) for b in broll)
    for n in range(n_total):
        raw = dec.stdout.read(W * H * 3)
        if len(raw) < W * H * 3:
            break
        t = n / FPS
        fr = Image.frombuffer("RGB", (W, H), raw, "raw", "RGB", 0, 1)
        b_ativo = next((b for b in broll if b["ini"] <= t < b["fim"]), None)
        c_ativa = cart and cart["ini"] <= t < cart["fim"]
        if c_ativa:
            peq = fr.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
            fr = ImageEnhance.Brightness(peq.resize((W, H), Image.BILINEAR)).enhance(0.45)
        if b_ativo:
            # embaixo: o Dr. (rosto no centro da metade de baixo)
            zb = 1.22   # Dr. um pouco mais perto na metade de baixo, como no Volpe
            bw, bh = int(W / zb), int(METADE / zb)
            x0 = min(max(int(fx * W - bw / 2), 0), W - bw)
            y0 = min(max(int(fy * H) - int(bh * 0.40), 0), H - bh)
            img = Image.new("RGB", (W, H))
            img.paste(quadro_broll(b_ativo, t), (0, 0))
            img.paste(fr.crop((x0, y0, x0 + bw, y0 + bh)).resize((W, METADE), Image.BILINEAR), (0, METADE))
            fr = img
        fr = fr.convert("RGBA")
        # produtos ao lado da cabeça
        for p in prods:
            if p["ini"] <= t < p["fim"]:
                s = pop(t - p["ini"])
                im = p["img"]
                if s != 1.0:
                    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
                sh = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
                sh.paste((0, 0, 0, 120), (30, 40), im)
                sh = sh.filter(ImageFilter.GaussianBlur(14))
                cx, cy = int(p["pos"][0] * W), int(p["pos"][1] * H)
                fr.alpha_composite(sh, (cx - sh.width // 2, cy - sh.height // 2))
                fr.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
        if vit and vit["ini"] <= t < vit["fim"]:
            larg = sum(i.width for i in vit["ims"]) + 24 * (len(vit["ims"]) - 1)
            x = (W - larg) // 2
            for k, im in enumerate(vit["ims"]):
                s = pop(t - vit["ini"] - 0.08 * k)
                if t - vit["ini"] - 0.08 * k < 0:
                    x += im.width + 24
                    continue
                im2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
                fr.alpha_composite(im2, (x + (im.width - im2.width) // 2, int(H * 0.17) - im2.height // 2))
                x += im.width + 24
        # gancho escrito
        if g_img is not None and t < g_fim:
            fr.alpha_composite(g_img, ((W - g_img.width) // 2, METADE - g_img.height // 2))
        # cartela
        if c_ativa:
            lt = t - cart["ini"]
            a = ease(lt / 0.3)
            y = int(H * 0.40 + 30 * (1 - a))
            for im in (cart["c1"], cart["c2"]):
                im2 = im if a >= 1 else Image.fromarray((np.asarray(im) * np.array([1, 1, 1, a])).astype(np.uint8))
                fr.alpha_composite(im2, ((W - im.width) // 2, y))
                y += im.height - 40
        # legenda (some durante o gancho e a cartela)
        elif t >= g_fim:
            bl = next((x for x in leg if x[0] <= t < x[1]), None)
            if bl:
                if bl[2] not in cache_leg:
                    cache_leg[bl[2]] = texto_sombra(bl[2], fonte_leg, largura_max=W - 160)
                im = cache_leg[bl[2]]
                yc = METADE - 70 if b_ativo else int(H * 0.60)
                fr.alpha_composite(im, ((W - im.width) // 2, yc - im.height // 2))
        # ícone de comentário
        if com and com["ini"] <= t < com["fim"]:
            s = pop(t - com["ini"], 0.35)
            im = com["img"].resize((int(260 * s), int(260 * s)), Image.BILINEAR)
            fr.alpha_composite(im, ((W - im.width) // 2, int(H * 0.70) - im.height // 2))
        fr = fr.convert("RGB")
        # flash nas trocas de imagem
        ult = max((x for x in trocas_broll if x <= t), default=None)
        if ult is not None and t - ult < 0.17:
            a = 0.55 * (1 - (t - ult) / 0.17)
            fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), a)
        enc.stdin.write(fr.tobytes())
        if n % 150 == 0:
            print(f"  {t:5.1f}/{mapa.dur:.1f} s", flush=True)
    enc.stdin.close()
    enc.wait()
    dec.kill()
    print("ok:", saida, flush=True)
    json.dump({"trechos": trechos, "legendas": leg}, open(saida + ".log.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    renderizar(cfg, previa="--previa" in sys.argv)
