#!/usr/bin/env python3
"""FEA: edição de Reels no modelo "notícia" (tela dividida, headline que desliza, B-roll e produtos).

Uso:
    python3 fea_editar_noticia.py projeto.json [--previa] [--quadros t1,t2,...]

--previa      720p rápido, só para conferir (a entrega é sempre em 1080p, H.264 CRF 18)
--quadros     só gera PNGs dos instantes pedidos (segundos do vídeo final), sem render

Pedido da Keila (26/10/2026), vídeo "Melhores produtos" (IMG_7934):
  - headline no modelo do "1- Olheiras" (pasta 20- Entrevistas mito ou verdade): barra dourada
    à esquerda e o texto em caixas brancas que sai de trás da barra, deslizando para o lado,
    como faixa de telejornal;
  - tela dividida com esfumaçado no meio (B-roll ou produto em cima, Dr. João embaixo);
  - quando o Dr. fala um produto, a foto do produto aparece sem fundo e sem borda;
  - música calma de fundo, baixa;
  - B-roll do banco "FEA-B-roll pele flácida e envelhecida (face)".
A legenda é a mesma do padrão FEA (fea_editar_video.py: correções, voz, blocos), só entra
depois que a headline sai.

projeto.json:
{
  "ffmpeg": "...", "fontsdir": "fonts",
  "fonte_headline": "fonts/Sora-700.ttf",
  "video": {
    "entrada": "bruto.MOV", "transcricao": "tr/x.json", "saida": "out/1- Titulo.mp4",
    "headline": ["Linha 1", "Linha 2"], "headline_fim": 4.6,          # s do vídeo final
    "manter": [[5.0, 18.4], ...], "correcoes": [[regex, troca], ...],
    "fundo_produto": {"imagem": "quadro.png", "crop": [x, y, w, h]},  # fundo desfocado do painel
    "cenas": [                                                         # tempos em s do BRUTO
      {"ini": 5.0, "tipo": "broll", "arquivo": "b.mp4", "src": 1.0, "cx": 0.5, "cy": 0.5, "zoom": 1,
       "rotulo": "1. Limpeza"},                                        # rotulo é opcional
      {"ini": 11.2, "tipo": "produto", "imagem": "p.png", "nome": "Neuramis Deep"},
      {"ini": 17.0, "tipo": "produtos", "imagens": ["a.png", "b.png", "c.png"], "numerar": true},
      {"ini": 33.6, "tipo": "cheio"}
    ],
    "musica": {"arquivo": "m.mp3", "ini": 0, "abaixo_da_voz_db": 20}
  }
}
"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as base  # noqa: E402

W, H, FPS = 1080, 1920, 30
PAINEL_H = 1000          # altura do painel de cima (B-roll ou produto)
ESF_INI, ESF_FIM = 820, 1000   # faixa do esfumaçado entre o painel e o Dr.
DESCE = 480              # quanto o Dr. desce na tela dividida (cabeça logo abaixo do esfumaçado)
TRANS = 0.38             # duração da transição deslizante (s)
POP = 0.30               # entrada do produto (s)

# headline: medida em pixels no "1- Olheiras" (barra 18 px, caixas a 14 px da barra, ~72 px por linha)
HL_BARRA_X, HL_BARRA_L = 143, 18
HL_CAIXA_X = 175
HL_LINHA_H, HL_LINHA_GAP = 80, 6
HL_FONTE = 60
HL_Y = 730               # topo da primeira linha
HL_DOURADO = (219, 208, 147)
ROXO = (91, 69, 153)     # #5B4599, identidade FEA
LAVANDA = (208, 209, 233)


ESTILOS = {
    # referência do Dr. (27/10/2026, reels "03 cremes fantásticos" e "3 cremes de farmácia"): B-roll em
    # close extremo ocupando ~2/3 da tela, Dr. menor embaixo, zoom contínuo e headline grande
    "exagerado": {"PAINEL_H": 1240, "ESF_INI": 1070, "ESF_FIM": 1240, "DESCE": 720, "PUSH": 0.16,
                  "HL_FONTE": 80, "HL_LINHA_H": 106, "HL_LINHA_GAP": 8, "HL_Y": 860,
                  "PROD_MAX": (860, 700), "PROD_Y": 540, "PROD_NOME_Y": 970,
                  "PRODS_ALT": 640, "PRODS_Y": 600, "PRODS_NUM_Y": 210},
    # Keila, 27/10/2026, refeito depois de "nada a ver com as referências": tela dividida na metade,
    # B-roll do gancho cresce até quase a tela cheia, headline centralizada na emenda (caixas brancas,
    # letra preta grossa), depois o Dr. em tela cheia. O B-roll é renderizado com 1700 px e recortado
    # no centro conforme a altura da cena ("altura" ou "cresce": [h0, h1] no projeto).
    "referencia": {"PAINEL_H": 1700, "ALTURA": 960, "CROP_CENTRO": True, "PUSH": 0.06, "HL_CENTRO": True,
                   "PROD_MAX": (860, 560), "PROD_Y": 850, "PROD_NOME_Y": 1170,
                   "PRODS_ALT": 520, "PRODS_Y": 860, "PRODS_NUM_Y": 560, "ROTULO_Y": 1180, "DESCE_OFF": 300},
}
ALTURA = None            # altura visível do painel (None = PAINEL_H inteiro)
CROP_CENTRO = False      # recorta o painel no centro (True) ou no topo
DESCE_OFF = 520          # o Dr. desce (altura do painel - 520 px): cabeça logo abaixo do esfumaçado
HL_CENTRO = False        # headline centralizada na emenda (estilo referencia) em vez da barra dourada
ROTULO_Y = None
PROD_MAX, PROD_Y, PROD_NOME_Y = (700, 470), 430, 760          # produto único no painel
PRODS_ALT, PRODS_Y, PRODS_NUM_Y = 400, 470, 190                # vários lado a lado
PUSH = 0.0               # zoom contínuo do B-roll (fração a mais no fim da cena); 0 = parado


def aplicar_estilo(nome):
    if nome:
        globals().update(ESTILOS[nome])


def ease(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


def ease_io(p):
    p = min(1.0, max(0.0, p))
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


# ---------- tempo: bruto -> vídeo final ----------

def mapa_tempo(manter):
    def f(t):
        off = 0.0
        for a, b in manter:
            if t < a:
                return off          # caiu num trecho cortado: vai para o começo do próximo
            if t <= b:
                return off + t - a
            off += b - a
        return off
    return f


# ---------- headline ----------

def render_headline(linhas, fonte):
    ft = ImageFont.truetype(fonte, HL_FONTE)
    camadas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(camadas)
    y = HL_Y
    for ln in linhas:
        l, t, r, b = d.textbbox((0, 0), ln, font=ft)
        larg = r - l + 2 * 16
        d.rectangle([HL_CAIXA_X, y, HL_CAIXA_X + larg, y + HL_LINHA_H], fill=(255, 255, 255, 255))
        ty = y + (HL_LINHA_H - (b - t)) / 2 - t
        d.text((HL_CAIXA_X + 16 - l, ty), ln, font=ft, fill=(0, 0, 0, 255))
        y += HL_LINHA_H + HL_LINHA_GAP
    barra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(barra).rectangle([HL_BARRA_X, HL_Y, HL_BARRA_X + HL_BARRA_L - 1, y - HL_LINHA_GAP],
                                    fill=HL_DOURADO + (255,))
    larg_total = max(np.nonzero(np.asarray(camadas)[:, :, 3].max(0))[0]) - HL_CAIXA_X + 1
    return np.asarray(camadas).astype(np.float32), np.asarray(barra).astype(np.float32), larg_total


def render_headline_centro(linhas, fonte, tam=66):
    """Caixas brancas centralizadas, letra preta grossa (reels de referência do Dr., 27/10/2026)."""
    ft = ImageFont.truetype(fonte, tam)
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    caixas = []
    for ln in linhas:
        l, t, r, b = d0.textbbox((0, 0), ln, font=ft)
        caixas.append((ln, r - l + 40, l, t, b))
    alt = int(tam * 1.32)
    im = Image.new("RGBA", (W, len(linhas) * (alt + 6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, larg, l, t, b) in enumerate(caixas):
        x0, y0 = (W - larg) // 2, i * (alt + 6)
        d.rectangle([x0, y0, x0 + larg, y0 + alt], fill=(255, 255, 255, 255))
        d.text((x0 + 20 - l, y0 + (alt - (b - t)) / 2 - t), ln, font=ft, fill=(0, 0, 0, 255))
    return im


def aplicar_headline_centro(quadro, im, t, fim, emenda):
    p_in = ease((t - 0.10) / 0.30)
    p_out = 1 - ease((t - fim) / 0.25)
    a = min(p_in, p_out)
    if a <= 0:
        return quadro
    esc = 0.88 + 0.12 * p_in
    img = im.resize((int(im.width * esc), int(im.height * esc)))
    if a < 1:
        img.putalpha(img.split()[3].point(lambda v: int(v * a)))
    tela = Image.fromarray(quadro).convert("RGBA")
    y = int(min(H - img.height - 40, emenda - img.height * 0.55))
    tela.alpha_composite(img, ((W - img.width) // 2, max(0, y)))
    return np.asarray(tela.convert("RGB"))


def aplicar_headline(quadro, hl, t, fim):
    caixas, barra, larg = hl
    # entrada: barra aparece (0,05-0,25 s) e o texto sai de trás dela (0,20-0,75 s);
    # saída: o texto volta para trás da barra e a barra some
    if t > fim + TRANS + 0.2:
        return quadro
    a_barra = ease((t - 0.05) / 0.2) * (1 - ease((t - fim - TRANS) / 0.2))
    p = ease((t - 0.20) / 0.55) if t < fim else 1 - ease_io((t - fim) / TRANS)
    dx = int(round(-(larg + 20) * (1 - p)))
    if a_barra <= 0:
        return quadro
    out = quadro.astype(np.float32)
    if p > 0:
        cam = np.zeros_like(caixas)
        if dx < 0:
            cam[:, :W + dx] = caixas[:, -dx:]
        else:
            cam[:] = caixas
        cam[:, :HL_CAIXA_X, 3] = 0          # o texto nunca aparece à esquerda da barra
        al = cam[:, :, 3:4] / 255
        out = out * (1 - al) + cam[:, :, :3] * al
    al = barra[:, :, 3:4] / 255 * a_barra
    out = out * (1 - al) + barra[:, :, :3] * al
    return out.astype(np.uint8)


# ---------- painel de produto ----------

def fundo_produto(cfg_fundo):
    im = Image.open(cfg_fundo["imagem"]).convert("RGB")
    if cfg_fundo.get("crop"):
        x, y, w, h = cfg_fundo["crop"]
        im = im.crop((x, y, x + w, y + h))
    im = im.resize((W, PAINEL_H)).filter(ImageFilter.GaussianBlur(28))
    lav = Image.new("RGB", im.size, LAVANDA)
    return np.asarray(Image.blend(im, lav, 0.35)).astype(np.float32)


def com_sombra(im):
    """Produto recortado com sombra suave embaixo (sem caixa branca nem borda)."""
    pad = 60
    tela = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = im.split()[3]
    sombra = Image.new("RGBA", tela.size, (20, 10, 40, 0))
    s_alpha = Image.new("L", tela.size, 0)
    s_alpha.paste(a.point(lambda v: v * 0.45), (pad + 8, pad + 22))
    sombra.putalpha(s_alpha.filter(ImageFilter.GaussianBlur(18)))
    tela = Image.alpha_composite(tela, sombra)
    tela.alpha_composite(im, (pad, pad))
    return tela


def etiqueta(nome, fonte, tam=40):
    ft = ImageFont.truetype(fonte, tam)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    l, t, r, b = d.textbbox((0, 0), nome, font=ft)
    w, h = r - l + 2 * 30, tam + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=ROXO + (255,))
    d.text((30 - l, (h - (b - t)) / 2 - t), nome, font=ft, fill=(255, 255, 255, 255))
    return im


def caber(im, mw, mh):
    f = min(mw / im.width, mh / im.height)
    return im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)


class PainelProduto:
    def __init__(self, cena, fundo, fonte):
        self.fundo = fundo
        self.itens = []          # (imagem RGBA, centro x, centro y, atraso)
        if cena["tipo"] == "produto":
            im = com_sombra(caber(Image.open(cena["imagem"]).convert("RGBA"), *PROD_MAX))
            self.itens.append((im, W // 2, PROD_Y, 0.0))
            if cena.get("nome"):
                self.itens.append((etiqueta(cena["nome"], fonte), W // 2, PROD_NOME_Y, 0.10))
        else:
            n = len(cena["imagens"])
            larg = (W - 80) // n
            for i, f in enumerate(cena["imagens"]):
                im = com_sombra(caber(Image.open(f).convert("RGBA"), larg - 40, PRODS_ALT))
                cx = 40 + larg * i + larg // 2
                self.itens.append((im, cx, PRODS_Y, 0.12 * i))
                if cena.get("numerar"):
                    self.itens.append((numero(i + 1, fonte), cx, PRODS_NUM_Y, 0.12 * i + 0.05))

    def quadro(self, tl):
        tela = Image.fromarray(self.fundo.astype(np.uint8)).convert("RGBA")
        for im, cx, cy, atraso in self.itens:
            p = ease((tl - atraso) / POP)
            if p <= 0:
                continue
            esc = 0.86 + 0.14 * p
            imr = im if esc >= 0.999 else im.resize((max(1, int(im.width * esc)), max(1, int(im.height * esc))))
            if p < 1:
                a = imr.split()[3].point(lambda v: int(v * p))
                imr = imr.copy()
                imr.putalpha(a)
            tela.alpha_composite(imr, (int(cx - imr.width / 2), int(cy - imr.height / 2)))
        return np.asarray(tela.convert("RGB")).astype(np.float32)


def numero(n, fonte):
    ft = ImageFont.truetype(fonte, 44)
    im = Image.new("RGBA", (84, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, 83, 83], fill=ROXO + (255,))
    l, t, r, b = d.textbbox((0, 0), str(n), font=ft)
    d.text((42 - (r - l) / 2 - l, 42 - (b - t) / 2 - t), str(n), font=ft, fill=(255, 255, 255, 255))
    return im


# ---------- B-roll ----------

class Broll:
    def __init__(self, ff, cena, dur, fonte=None, alt=None):
        self.ph = alt or PAINEL_H     # renderiza na altura máxima da cena: em 960 px a imagem não fica cortada
        # "rotulo": etiqueta roxa no pé do painel (ex.: "1. Limpeza"), entra com o mesmo pop do produto
        self.rotulo = etiqueta(cena["rotulo"], fonte, 46) if cena.get("rotulo") else None
        self.push, self.dur = cena.get("push", PUSH), max(dur - TRANS, 0.5)
        z = cena.get("zoom", 1.0)
        cx, cy = cena.get("cx", 0.5), cena.get("cy", 0.5)
        asp = W / self.ph
        vf = (f"fps={FPS},crop=w='min(iw,ih*{asp})/{z}':h='min(iw,ih*{asp})/{z}/{asp}':"
              f"x='max(0,min(iw-ow,{cx}*iw-ow/2))':y='max(0,min(ih-oh,{cy}*ih-oh/2))',"
              f"scale={W}:{self.ph}:flags=lanczos,setsar=1")
        self.p = subprocess.Popen([ff, "-v", "error", "-stream_loop", "-1", "-ss", str(cena.get("src", 0)),
                                   "-i", cena["arquivo"], "-t", f"{dur + 1:.2f}", "-an", "-vf", vf,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL)   # fechado no meio de propósito
        self.ultimo = np.zeros((self.ph, W, 3), np.float32)

    def quadro(self, tl):
        b = self.p.stdout.read(W * self.ph * 3)
        if len(b) == W * self.ph * 3:
            self.ultimo = np.frombuffer(b, np.uint8).reshape(self.ph, W, 3).astype(np.float32)
        base_q = self.ultimo
        if self.push:
            z = 1 + self.push * ease_io(tl / self.dur)
            cw, ch = W / z, self.ph / z
            x0, y0 = (W - cw) / 2, (self.ph - ch) / 2
            im = Image.fromarray(self.ultimo.astype(np.uint8)).resize(
                (W, self.ph), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
            base_q = np.asarray(im).astype(np.float32)
        if self.rotulo is None:
            return base_q
        p = ease((tl - 0.15) / POP)
        if p <= 0:
            return base_q
        esc = 0.86 + 0.14 * p
        im = self.rotulo.resize((int(self.rotulo.width * esc), int(self.rotulo.height * esc)))
        if p < 1:
            im.putalpha(im.split()[3].point(lambda v: int(v * p)))
        tela = Image.fromarray(base_q.astype(np.uint8)).convert("RGBA")
        ry = (ROTULO_Y - (PAINEL_H - self.ph) // 2) if ROTULO_Y is not None else self.ph - 260
        tela.alpha_composite(im, (int(W / 2 - im.width / 2), int(ry - im.height / 2)))
        return np.asarray(tela.convert("RGB")).astype(np.float32)

    def fechar(self):
        self.p.stdout.close()
        self.p.kill()


# ---------- composição ----------

def mascara_esfumado(h=None):
    banda = ESF_FIM - ESF_INI
    fim = ESF_FIM if h is None else h
    y = np.arange(H, dtype=np.float32)
    m = np.clip((fim - y) / banda, 0, 1)
    m = m * m * (3 - 2 * m)                     # suave nas duas pontas
    return m[:, None, None]


def compor(dr, painel, desce, dx_painel, mascara):
    """dr: quadro inteiro do Dr.; painel: imagem do painel de cima (ou None); desce: quanto o Dr.
    desceu (0 = tela cheia); dx_painel: deslocamento horizontal do painel (transição)."""
    if painel is None and desce == 0:
        return dr
    out = np.empty((H, W, 3), np.float32)
    d = int(round(desce))
    if d > 0:
        out[d:] = dr[:H - d]
        out[:d] = dr[d - 1::-1] if d <= H - d else dr[0:1]   # topo espelhado (fica por baixo do painel)
    else:
        out[:] = dr
    if painel is not None:
        pl = np.zeros((H, W, 3), np.float32)
        alfa = mascara.copy()
        pl[:painel.shape[0]] = painel
        if dx_painel:
            dx = int(round(dx_painel))
            pl = np.roll(pl, dx, axis=1)
            alfa = np.repeat(alfa, W, axis=1)
            if dx > 0:
                alfa[:, :dx] = 0
            else:
                alfa[:, W + dx:] = 0
        out = out * (1 - alfa) + pl * alfa
    return out


def main():
    args = sys.argv[1:]
    previa = "--previa" in args
    quadros = None
    if "--quadros" in args:
        quadros = [float(x) for x in args[args.index("--quadros") + 1].split(",")]
    cfg = json.load(open([a for a in args if a.endswith(".json")][0], encoding="utf-8"))
    ff, v = cfg["ffmpeg"], cfg["video"]
    fonte = cfg["fonte_headline"]
    aplicar_estilo(v.get("estilo"))

    # cortes no respiro e legenda: mesma lógica do padrão FEA
    db = base.perfil_voz(ff, v["entrada"])
    trans = json.load(open(v["transcricao"], encoding="utf-8"))
    manter = base.encaixar_cortes(v["manter"], db[0], db[2], [w for s in trans for w in s["words"]])
    # no modelo notícia a legenda roda junto com a headline (referência "1- Olheiras"): posições
    # diferentes na tela, e a fala do começo não fica sem legenda
    base.TITULO_DUR = 0.0
    vleg = dict(v, titulo="-", titulo_origem="imagem")
    dur = base.renderizar(cfg, vleg, "legenda")
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    linhas = [ln for ln in open(ass, encoding="utf-8") if ",Titulo," not in ln]
    open(ass, "w", encoding="utf-8").writelines(linhas)
    print(f"cortes: {manter}  duração: {dur:.2f}s", flush=True)

    tmap = mapa_tempo(manter)
    cenas = sorted(v["cenas"], key=lambda c: c["ini"])
    for c in cenas:
        c["t0"] = tmap(c["ini"])
    for c, prox in zip(cenas, cenas[1:] + [None]):
        c["t1"] = prox["t0"] if prox else dur

    if HL_CENTRO:
        hl = render_headline_centro(v["headline"], os.path.join(cfg["fontsdir"], "Montserrat-ExtraBold.ttf"))
    else:
        hl = render_headline(v["headline"], fonte)
    fundo = fundo_produto(v["fundo_produto"]) if v.get("fundo_produto") else None
    mascara0 = mascara_esfumado()

    # Dr. já cortado, direto do FFmpeg em quadros brutos
    partes, rot, arot = [], [], []
    for i, (a, b) in enumerate(manter):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1,fps={FPS}[v{i}]")
        partes.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={max(0, b - a - 0.02)}:d=0.02[a{i}]")
        rot.append(f"[v{i}]")
        arot.append(f"[a{i}]")
    fc_v = ";".join(x for x in partes if x.startswith("[0:v]")) + ";" + "".join(rot) + \
        f"concat=n={len(rot)}:v=1:a=0[vc]"
    fc_a = ";".join(x for x in partes if x.startswith("[0:a]")) + ";" + "".join(arot) + \
        f"concat=n={len(arot)}:v=0:a=1[ac]"
    tmpdir = os.path.dirname(os.path.abspath(v["saida"]))
    voz = os.path.join(tmpdir, "_voz.wav")
    subprocess.run([ff, "-y", "-v", "error", "-i", v["entrada"], "-filter_complex", fc_a, "-map", "[ac]",
                    "-ar", "48000", "-ac", "2", voz], check=True)
    dr_pipe = subprocess.Popen([ff, "-v", "error", "-i", v["entrada"], "-filter_complex", fc_v, "-map", "[vc]",
                                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

    # música baixa, sempre ~20 dB abaixo da voz, com entrada e saída suaves
    mus = v.get("musica")
    audio = voz
    if mus:
        def media_db(arq, extra=()):
            r = subprocess.run([ff, "-v", "info", *extra, "-i", arq, "-t", f"{dur:.2f}", "-af", "volumedetect",
                                "-f", "null", "-"], capture_output=True, text=True).stderr
            return float(re.search(r"mean_volume: (-?[\d.]+) dB", r).group(1))
        arq_mus, ini_mus = mus["arquivo"], mus.get("ini", 0)
        if mus.get("nivelar"):
            # faixa com parte calma e refrão forte ("Cat Walk" varia 9 dB): nivela antes de medir,
            # para a música não crescer no meio do vídeo
            arq_mus = os.path.join(tmpdir, "_musica_nivelada.wav")
            subprocess.run([ff, "-y", "-v", "error", "-ss", str(ini_mus), "-i", mus["arquivo"], "-t", f"{dur + 1:.2f}",
                            "-af", "acompressor=threshold=-30dB:ratio=8:attack=20:release=400:makeup=6,"
                            "dynaudnorm=f=150:g=15:m=10", "-ar", "48000", arq_mus], check=True)
            ini_mus = 0
        ganho = media_db(voz) - mus.get("abaixo_da_voz_db", 20) - media_db(arq_mus, ("-ss", str(ini_mus)))
        audio = os.path.join(tmpdir, "_audio.wav")
        subprocess.run([ff, "-y", "-v", "error", "-i", voz, "-ss", str(ini_mus), "-i", arq_mus,
                        "-filter_complex",
                        f"[1:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,volume={ganho:.2f}dB,aresample=48000,"
                        f"aformat=channel_layouts=stereo,afade=t=in:d=1.2,afade=t=out:st={dur - 2:.3f}:d=2[m];"
                        f"[0:a][m]amix=inputs=2:normalize=0:duration=first[a]",
                        "-map", "[a]", "-ar", "48000", audio], check=True)
        print(f"música: {ganho:+.1f} dB", flush=True)

    saida = v["saida"]
    if previa:
        pasta, nome = saida.rsplit("/", 1)
        saida = f"{pasta}/PREVIA {nome}"
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    vf = f"ass='{esc}':fontsdir='{cfg['fontsdir']}'" + (",scale=720:1280" if previa else "")
    enc = None
    if quadros is None:
        enc = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                "-r", str(FPS), "-i", "-", "-i", audio, "-vf", vf, "-map", "0:v", "-map", "1:a",
                                "-c:v", "libx264", "-preset", "fast" if previa else "medium",
                                "-crf", "23" if previa else "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                                "-movflags", "+faststart", saida], stdin=subprocess.PIPE)

    fontes = {}            # cena -> objeto (B-roll aberto ou painel de produto)

    def conteudo(c, t):
        if c["tipo"] == "cheio":
            return None
        k = id(c)
        if k not in fontes:
            alt_max = max(c["cresce"]) if c.get("cresce") else (c.get("altura") or ALTURA or PAINEL_H)
            fontes[k] = (Broll(ff, c, c["t1"] - c["t0"] + TRANS, fonte, alt_max) if c["tipo"] == "broll"
                         else PainelProduto(c, fundo, fonte))
        q = fontes[k].quadro(t - c["t0"])
        h = altura(c, t)
        y0 = (q.shape[0] - h) // 2 if CROP_CENTRO else 0
        return q[y0:y0 + h]

    def altura(c, t):
        if c.get("cresce"):
            h0, h1 = c["cresce"]
            return int(h0 + (h1 - h0) * ease_io((t - c["t0"]) / max(0.5, c["t1"] - c["t0"])))
        return int(c.get("altura", ALTURA or PAINEL_H))

    n = int(round(dur * FPS))
    alvo = {int(round(q * FPS)) for q in quadros} if quadros else None
    for i in range(n):
        b = dr_pipe.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        t = i / FPS
        dr = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
        k = max(j for j, c in enumerate(cenas) if c["t0"] <= t + 1e-6) if t >= cenas[0]["t0"] else None
        emenda = H * 0.5
        if k is None:
            quadro = dr
        else:
            c = cenas[k]
            ant = cenas[k - 1] if k > 0 else None
            p = ease_io((t - c["t0"]) / TRANS) if ant is not None else 1.0
            novo = conteudo(c, t)
            velho = conteudo(ant, t) if (ant is not None and p < 1) else None
            hv = novo.shape[0] if novo is not None else (velho.shape[0] if velho is not None else 0)
            if velho is not None and novo is not None and velho.shape[0] != hv:
                velho = velho[:hv] if velho.shape[0] > hv else np.vstack(
                    [velho, np.repeat(velho[-1:], hv - velho.shape[0], axis=0)])
            DESCE = max(0, hv - DESCE_OFF)
            mascara = mascara_esfumado(hv) if hv else mascara0
            emenda = hv
            if p >= 1 or ant is None:
                quadro = compor(dr, novo, DESCE if novo is not None else 0, 0, mascara)
            elif novo is not None and velho is not None:
                # troca de painel: o novo entra pela direita empurrando o antigo (efeito notícia)
                meio = compor(dr, velho, DESCE, -W * p, mascara)
                quadro = compor_por_cima(meio, novo, W * (1 - p), mascara)
            elif novo is not None:
                # tela cheia -> dividida: o Dr. desce e o painel entra deslizando
                quadro = compor(dr, novo, DESCE * p, W * (1 - p), mascara)
            else:
                # dividida -> cheia: o painel sai pela esquerda e o Dr. sobe
                quadro = compor(dr, velho, DESCE * (1 - p), -W * p, mascara)
            for kk in list(fontes):
                if all(id(cc) != kk for cc in (c, ant)) and isinstance(fontes[kk], Broll):
                    fontes[kk].fechar()
                    del fontes[kk]
        quadro = np.clip(quadro, 0, 255).astype(np.uint8)
        if HL_CENTRO:
            quadro = aplicar_headline_centro(quadro, hl, t, v["headline_fim"], emenda or H * 0.5)
        else:
            quadro = aplicar_headline(quadro, hl, t, v["headline_fim"])
        if alvo is not None:
            if i in alvo:
                Image.fromarray(quadro).save(os.path.join(tmpdir, f"_quadro_{t:05.2f}.png"))
            if i > max(alvo):
                break
            continue
        enc.stdin.write(np.ascontiguousarray(quadro, np.uint8).tobytes())
        if i % 150 == 0:
            print(f"  {t:5.1f}/{dur:.1f}s", flush=True)
    dr_pipe.stdout.close()
    dr_pipe.kill()
    if enc:
        enc.stdin.close()
        enc.wait()
        print(f"{saida}: {dur:.1f}s", flush=True)


def compor_por_cima(fundo, painel, dx, mascara):
    pl = np.zeros((H, W, 3), np.float32)
    pl[:painel.shape[0]] = painel
    alfa = np.repeat(mascara, W, axis=1).copy()
    d = int(round(dx))
    if d:
        pl = np.roll(pl, d, axis=1)
        alfa[:, :d] = 0
    return fundo * (1 - alfa) + pl * alfa


if __name__ == "__main__":
    main()
