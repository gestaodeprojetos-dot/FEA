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
      {"ini": 5.0, "tipo": "broll", "arquivo": "b.mp4", "src": 1.0, "cx": 0.5, "cy": 0.5, "zoom": 1},
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
            im = com_sombra(caber(Image.open(cena["imagem"]).convert("RGBA"), 700, 470))
            self.itens.append((im, W // 2, 430, 0.0))
            if cena.get("nome"):
                self.itens.append((etiqueta(cena["nome"], fonte), W // 2, 760, 0.10))
        else:
            n = len(cena["imagens"])
            larg = (W - 80) // n
            for i, f in enumerate(cena["imagens"]):
                im = com_sombra(caber(Image.open(f).convert("RGBA"), larg - 40, 400))
                cx = 40 + larg * i + larg // 2
                self.itens.append((im, cx, 470, 0.12 * i))
                if cena.get("numerar"):
                    self.itens.append((numero(i + 1, fonte), cx, 190, 0.12 * i + 0.05))

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
    def __init__(self, ff, cena, dur):
        z = cena.get("zoom", 1.0)
        cx, cy = cena.get("cx", 0.5), cena.get("cy", 0.5)
        asp = W / PAINEL_H
        vf = (f"fps={FPS},crop=w='min(iw,ih*{asp})/{z}':h='min(iw,ih*{asp})/{z}/{asp}':"
              f"x='max(0,min(iw-ow,{cx}*iw-ow/2))':y='max(0,min(ih-oh,{cy}*ih-oh/2))',"
              f"scale={W}:{PAINEL_H}:flags=lanczos,setsar=1")
        self.p = subprocess.Popen([ff, "-v", "error", "-stream_loop", "-1", "-ss", str(cena.get("src", 0)),
                                   "-i", cena["arquivo"], "-t", f"{dur + 1:.2f}", "-an", "-vf", vf,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL)   # fechado no meio de propósito
        self.ultimo = np.zeros((PAINEL_H, W, 3), np.float32)

    def quadro(self, tl):
        b = self.p.stdout.read(W * PAINEL_H * 3)
        if len(b) == W * PAINEL_H * 3:
            self.ultimo = np.frombuffer(b, np.uint8).reshape(PAINEL_H, W, 3).astype(np.float32)
        return self.ultimo

    def fechar(self):
        self.p.stdout.close()
        self.p.kill()


# ---------- composição ----------

def mascara_esfumado():
    y = np.arange(H, dtype=np.float32)
    m = np.clip((ESF_FIM - y) / (ESF_FIM - ESF_INI), 0, 1)
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
        pl[:PAINEL_H] = painel
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

    hl = render_headline(v["headline"], fonte)
    fundo = fundo_produto(v["fundo_produto"])
    mascara = mascara_esfumado()

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
            fontes[k] = (Broll(ff, c, c["t1"] - c["t0"] + TRANS) if c["tipo"] == "broll"
                         else PainelProduto(c, fundo, fonte))
        return fontes[k].quadro(t - c["t0"])

    n = int(round(dur * FPS))
    alvo = {int(round(q * FPS)) for q in quadros} if quadros else None
    for i in range(n):
        b = dr_pipe.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        t = i / FPS
        dr = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
        k = max(j for j, c in enumerate(cenas) if c["t0"] <= t + 1e-6) if t >= cenas[0]["t0"] else None
        if k is None:
            quadro = dr
        else:
            c = cenas[k]
            ant = cenas[k - 1] if k > 0 else None
            p = ease_io((t - c["t0"]) / TRANS) if ant is not None else 1.0
            novo = conteudo(c, t)
            velho = conteudo(ant, t) if (ant is not None and p < 1) else None
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
        quadro = aplicar_headline(np.clip(quadro, 0, 255).astype(np.uint8), hl, t, v["headline_fim"])
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
    pl[:PAINEL_H] = painel
    alfa = np.repeat(mascara, W, axis=1).copy()
    d = int(round(dx))
    if d:
        pl = np.roll(pl, d, axis=1)
        alfa[:, :d] = 0
    return fundo * (1 - alfa) + pl * alfa


if __name__ == "__main__":
    main()
