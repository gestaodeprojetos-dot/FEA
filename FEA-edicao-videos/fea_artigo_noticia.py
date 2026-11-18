#!/usr/bin/env python3
"""FEA: Reels "artigo comentado" no formato notícia (protótipo de 18/11/2026).

Formato pedido pela Keila e pelo Dr. João (18/11/2026), reproduzindo a entrada dos vídeos
"Skincare" e "Melhores produtos" (pastas 10- Outubro e 11- Novembro):
  - Gancho de 2 a 4 s: foto clínica forte do próprio artigo em tela cheia, zoom lento, título
    em faixas brancas (texto preto) no meio do quadro, selo roxo "ARTIGO CIENTÍFICO", crédito
    da fonte e aviso "Imagens de publicação científica", trilha mais alta.
  - Depois o Dr. falando: tela dividida (em cima o artigo, embaixo o Dr.) quando ele cita o
    artigo, tela cheia quando é raciocínio dele. Página online rolando, páginas do PDF com
    realce lavanda e borda roxa no trecho citado, figuras do artigo, ilustração de vídeo FEA.
  - Legenda padrão da skill fea-edicao-reels (Montserrat Bold 56, ~80% da altura), que na tela
    dividida cai no Dr., nunca no artigo.
  - Trilha de fundo: arquivo da FEA (se houver) ou base instrumental original gerada aqui
    (síntese própria, sem direitos de terceiros). Ducking: -24 a -28 dB abaixo da voz, mais
    alta só no gancho.

Uso:
    python3 fea_artigo_noticia.py projeto.json [--previa] [--so-legenda] [--quadros t1,t2,...]

--so-legenda: só o .ass (conferir o texto).  --quadros: PNGs de conferência nesses tempos (s
da edição), sem render.  --previa: 540x960 rápido.  Sem opção: entrega (H.264 CRF 18,
AAC 192k 48 kHz, 1080x1920, 30 fps).

Projeto (todos os tempos de cena em segundos DO BRUTO; o script converte para a edição):
{
  "ffmpeg": "...", "fontsdir": "fonts",
  "videos": [{                       # bloco compatível com fea_revisar.py / fea_doc_legendas.py
    "entrada": "bruto/IMG_9455.MOV", "transcricao": "tr/IMG_9455.json",
    "saida": "out/1- Título.mp4", "titulo": "Título", "titulo_origem": "inventado",
    "manter": [[0.0, 11.45], ...], "sem_cta": true, "fade_final": 0.4,
    "correcoes": [], "remover_legenda": []
  }],
  "noticia": {
    "titulo_linhas": ["Linha 1", "linha 2"],
    "selo": "ARTIGO CIENTÍFICO",
    "credito": "Fonte: Autor et al., Revista 2024",
    "aviso": "Imagens de publicação científica",
    "pre": 0.5,                      # s de gancho antes da 1ª fala (só trilha)
    "pos": 0.5,                      # s de último quadro parado depois da última palavra (fade)
    "titulo_ate": 3.15,              # s do bruto em que o título sai
    "dr_recorte_y": 180,             # y do recorte 1080x960 do Dr. na tela dividida
    "legenda_dividida_y": 1100,      # base da legenda na tela dividida (logo abaixo da costura)
    "trilha": {"arquivo": null, "gancho_db": -12, "fundo_db": -26, "semente": 7},
    "fontes": {                       # imagens usadas nas cenas
      "fig1": {"img": "pdf/fig-001.jpg", "recorte": [0, 0, 0.29, 1]},          # frações
      "p3":   {"pdf": "bruto/artigo.pdf", "pagina": 3, "dpi": 300},
      "web":  {"img": "web/unesp_top.png"},
      "recon": {"video": "ilus/x.mp4", "de": 27.6, "ate": 33.6, "velocidade": 0.75, "recorte_y": 100}
    },
    "cenas": [
      {"de": -0.5, "ate": 1.9, "modo": "cheia", "fonte": "fig1", "zoom": [1.0, 1.10], "foco": [0.5, 0.5],
       "aviso": true},
      {"de": 3.15, "ate": 5.5, "modo": "dividida", "fonte": "fig1b", "rotulo": "Fig. 1: ..."},
      {"de": 5.5, "ate": 11.4, "modo": "dividida", "fonte": "web", "rolar": [0.0, 0.45],
       "janela": [0.02, 0.98]},
      {"de": 82.6, "ate": 93.1, "modo": "dividida", "fonte": "p3", "janela": [0.05, 0.50],
       "realces": [[82.6, "Nodule 49 (89.1%)"], [85.6, "PLLA–Elleva® 27 (49.1%)|PLLA–Sculptra® 11 (20.0%)"]]}
    ]
  }
}
Fora das cenas, o Dr. fica em tela cheia. "realces": [inicio_no_bruto, "frase|outra frase"]: cada
frase é procurada nas palavras do PDF (pdftotext -bbox) e ganha o realce; a janela acompanha.
"janela" (PDF e web): faixa horizontal [x0, x1] da página mostrada (fração da largura).
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
import fea_editar_video as fe  # noqa: E402

W, H = 1080, 1920
FPS = 30
META = H // 2                      # costura da tela dividida
ROXO = (91, 69, 153)
AZUL = (56, 70, 187)
LAVANDA = (208, 209, 233)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
FUNDO = (18, 16, 28)
TRANSICAO = 0.25                   # crossfade entre cenas (s)
SR = 48000
CACHE = "cache"                    # pasta de trabalho (definida no main: noticia.trabalho/cache)


# ---------------------------------------------------------------- tempo bruto -> edição

def mapa_tempo(manter, pre):
    def f(t):
        if t < 0:
            return max(0.0, pre + t)
        acc = pre
        for a, b in manter:
            if t < a:
                return acc
            if t <= b:
                return acc + t - a
            acc += b - a
        return acc
    return f


# ---------------------------------------------------------------- fontes e texto

class Fontes:
    def __init__(self, pasta):
        self.pasta = pasta
        self.cache = {}

    def __call__(self, peso, tam):
        k = (peso, tam)
        if k not in self.cache:
            self.cache[k] = ImageFont.truetype(os.path.join(self.pasta, f"Montserrat-{peso}.ttf"), tam)
        return self.cache[k]


def caixa_texto(draw, xy, texto, fonte, fg, bg, pad=(22, 10), raio=0, ancora="mm"):
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), texto, font=fonte)
    w, h = r - l, b - t
    asc, desc = fonte.getmetrics()
    hh = asc + desc * 0.15
    if ancora == "mm":
        x0, y0 = x - w / 2 - pad[0], y - hh / 2 - pad[1]
    else:                        # "lm"
        x0, y0 = x, y - hh / 2 - pad[1]
    x1, y1 = x0 + w + 2 * pad[0], y0 + hh + 2 * pad[1]
    if bg is not None:
        draw.rounded_rectangle([x0, y0, x1, y1], raio, fill=bg)
    draw.text((x0 + pad[0] - l, y0 + pad[1] + (hh - asc) / 2 + 2), texto, font=fonte, fill=fg)
    return x0, y0, x1, y1


def camada_titulo(fontes, linhas, cy):
    """Faixas brancas com texto preto, uma por linha (entrada estilo notícia das referências)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = fontes("ExtraBold", 66)
    alt = 96
    y = cy - alt * (len(linhas) - 1) / 2
    for ln in linhas:
        caixa_texto(d, (W / 2, y), ln, f, PRETO, BRANCO, pad=(24, 12), raio=4)
        y += alt
    return im


def pilula(fontes, texto, cor=ROXO, tam=40, peso="Bold"):
    f = fontes(peso, tam)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    l, t, r, b = tmp.textbbox((0, 0), texto, font=f)
    asc, desc = f.getmetrics()
    w, h = r - l + 56, int(asc + desc * 0.15) + 26
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=cor + (255,))
    d.text((28 - l, 13 + 2), texto, font=f, fill=BRANCO)
    return im


def etiqueta(fontes, texto, tam=26):
    """Crédito / aviso: texto branco em faixa escura translúcida."""
    f = fontes("SemiBold", tam)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    l, t, r, b = tmp.textbbox((0, 0), texto, font=f)
    asc, desc = f.getmetrics()
    w, h = r - l + 28, int(asc + desc * 0.2) + 14
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=(10, 8, 20, 170))
    d.text((14 - l, 7 + 1), texto, font=f, fill=BRANCO)
    return im


# ---------------------------------------------------------------- fontes visuais

def palavras_pdf(pdf, pagina, dpi, cache={}):
    """Palavras da página com caixa em pixels (pdftotext -bbox)."""
    k = (pdf, pagina, dpi)
    if k in cache:
        return cache[k]
    html = subprocess.run(["pdftotext", "-bbox", "-f", str(pagina), "-l", str(pagina), pdf, "-"],
                          capture_output=True, text=True, check=True).stdout
    esc = dpi / 72.0
    out = []
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', html):
        x0, y0, x1, y1 = (float(m.group(i)) * esc for i in range(1, 5))
        out.append((x0, y0, x1, y1, m.group(5).replace("&amp;", "&")))
    cache[k] = out
    return out


def _norm(s):
    s = s.replace("­", "").replace("‐", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"[^\w%().,-]", "", s.lower())


def achar_frase(palavras, frase):
    """Caixas das linhas da frase (sequência de palavras); a frase pode quebrar linha."""
    alvo = [_norm(x) for x in frase.split() if _norm(x)]
    toks = [_norm(p[4]) for p in palavras]
    for i in range(len(toks)):
        j, k, usados = i, 0, []
        while k < len(alvo) and j < len(toks):
            if not toks[j]:
                j += 1
                continue
            if toks[j] == alvo[k] or (len(alvo[k]) > 3 and toks[j].startswith(alvo[k])) or \
                    (k == len(alvo) - 1 and alvo[k].startswith(toks[j]) and len(toks[j]) > 2):
                usados.append(j)
                j += 1
                k += 1
            elif usados and toks[j] + (toks[j + 1] if j + 1 < len(toks) else "") == alvo[k]:
                usados += [j, j + 1]
                j += 2
                k += 1
            else:
                break
        if k == len(alvo):
            # agrupa por linha
            linhas = []
            for u in usados:
                x0, y0, x1, y1, _ = palavras[u]
                if linhas and abs(linhas[-1][1] - y0) < (y1 - y0) * 0.6 and x0 > linhas[-1][2] - 5:
                    l = linhas[-1]
                    linhas[-1] = [min(l[0], x0), min(l[1], y0), max(l[2], x1), max(l[3], y1)]
                else:
                    linhas.append([x0, y0, x1, y1])
            return linhas
    raise SystemExit(f"ERRO: frase não encontrada no PDF: {frase!r}")


class Fonte:
    """Imagem grande (figura, página do PDF, captura web) ou vídeo, carregada sob demanda."""

    def __init__(self, base, cfg, ff):
        self.cfg, self.ff, self.base = cfg, ff, base
        self._img = None
        self.video = cfg.get("video")

    def caminho(self, p):
        return p if os.path.isabs(p) else os.path.join(self.base, p)

    def imagem(self):
        if self._img is None:
            c = self.cfg
            if "pdf" in c:
                saida = os.path.join(CACHE, f"pg{c['pagina']}_{c.get('dpi', 300)}.png")
                if not os.path.exists(saida):
                    os.makedirs(os.path.dirname(saida), exist_ok=True)
                    raiz = saida[:-4]
                    subprocess.run(["pdftoppm", "-r", str(c.get("dpi", 300)), "-f", str(c["pagina"]),
                                    "-l", str(c["pagina"]), "-png", "-singlefile", self.caminho(c["pdf"]), raiz],
                                   check=True)
                im = Image.open(saida).convert("RGB")
            else:
                im = Image.open(self.caminho(c["img"])).convert("RGB")
            if c.get("recorte"):
                x0, y0, x1, y1 = c["recorte"]
                im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
            self._img = im
        return self._img

    def palavras(self):
        c = self.cfg
        return palavras_pdf(self.caminho(c["pdf"]), c["pagina"], c.get("dpi", 300))


class LeitorVideo:
    def __init__(self, ff, arq, w, h, vf="", ss=0.0):
        self.w, self.h = w, h
        cmd = [ff, "-nostdin", "-v", "error", "-ss", f"{ss:.3f}", "-i", arq, "-an",
               "-vf", (vf + "," if vf else "") + f"fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.ultimo = None

    def ler(self):
        n = self.w * self.h * 3
        buf = self.p.stdout.read(n)
        if len(buf) == n:
            self.ultimo = Image.frombuffer("RGB", (self.w, self.h), buf, "raw", "RGB", 0, 1)
        return self.ultimo

    def fechar(self):
        try:
            self.p.stdout.close()
            self.p.kill()
        except Exception:
            pass


def suave(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def cobrir(im, w, h, zoom=1.0, foco=(0.5, 0.5)):
    """Recorte 'cover' com zoom em torno do foco (frações)."""
    esc = max(w / im.width, h / im.height) * max(1.0, zoom)
    cw, ch = w / esc, h / esc
    cx = min(max(foco[0] * im.width, cw / 2), im.width - cw / 2)
    cy = min(max(foco[1] * im.height, ch / 2), im.height - ch / 2)
    caixa = (max(0.0, cx - cw / 2), max(0.0, cy - ch / 2),
             min(float(im.width), cx + cw / 2), min(float(im.height), cy + ch / 2))
    return im.resize((w, h), Image.LANCZOS, box=caixa)


# ---------------------------------------------------------------- render de um painel

def painel_documento(fonte, cena, t_ed, w, h, mapa, desenhar_realce=True):
    """Página (PDF/web) recortada na faixa 'janela', rolando ou acompanhando o realce."""
    im = fonte.imagem()
    x0f, x1f = cena.get("janela", [0.0, 1.0])
    cw = (x1f - x0f) * im.width
    esc = w / cw
    ch = h / esc
    ini, fim = mapa(cena["de"]), mapa(cena["ate"])
    prog = (t_ed - ini) / max(0.01, fim - ini)
    realces = []
    cy = None
    if cena.get("realces") or cena.get("marcas"):
        # realce ativo = o último cujo início já passou; a janela desliza até ele em 0,5 s
        if cena.get("realces"):
            pal = fonte.palavras()
            ativos = [(mapa(r0), [c for fr in frase.split("|") for c in achar_frase(pal, fr)])
                      for r0, frase in cena["realces"]]
        else:             # "marcas": [[inicio_no_bruto, [x0, y0, x1, y1] em frações], ...]
            ativos = [(mapa(r0), [[x0 * im.width, y0 * im.height, x1 * im.width, y1 * im.height]
                                  for x0, y0, x1, y1 in (cx if isinstance(cx[0], list) else [cx])])
                      for r0, cx in cena["marcas"]]
        idx = max([i for i, (r0, _) in enumerate(ativos) if r0 <= t_ed + 1e-6] or [0])
        centro = lambda cx: (min(c[1] for c in cx) + max(c[3] for c in cx)) / 2
        if not cena.get("rolar"):
            alvo = centro(ativos[idx][1])
            if idx > 0:
                ant = centro(ativos[idx - 1][1])
                a = suave((t_ed - ativos[idx][0]) / 0.5)
                alvo = ant + (alvo - ant) * a
            cy = alvo - ch * (cena.get("realce_y", 0.5) - 0.5)
        r0 = ativos[idx][0]
        if t_ed >= r0:
            realces = [(c, suave((t_ed - r0) / 0.35)) for c in ativos[idx][1]]
    if cy is None:
        a, b = cena.get("rolar", [0.0, 0.0])
        topo = (a + (b - a) * suave(prog)) * im.height
        cy = topo + ch / 2
    cy = min(max(cy, ch / 2), im.height - ch / 2)
    zoom = 1.0 + cena.get("zoom_lento", 0.03) * min(1.0, max(0.0, prog))
    cw2, ch2 = cw / zoom, ch / zoom
    cx = (x0f + x1f) / 2 * im.width
    caixa = (cx - cw2 / 2, cy - ch2 / 2, cx + cw2 / 2, cy + ch2 / 2)
    out = im.resize((w, h), Image.LANCZOS, box=caixa).convert("RGBA")
    if realces and desenhar_realce:
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        e = w / cw2
        for (bx0, by0, bx1, by1), a in realces:
            X0 = (bx0 - caixa[0]) * e - 10
            Y0 = (by0 - caixa[1]) * e - 7
            X1 = (bx1 - caixa[0]) * e + 10
            Y1 = (by1 - caixa[1]) * e + 7
            X1a = X0 + (X1 - X0) * a
            d.rounded_rectangle([X0, Y0, X1a, Y1], 10, fill=LAVANDA + (120,), outline=ROXO + (255,), width=5)
        # o lavanda translúcido escurece pouco o texto preto: multiplica em vez de cobrir
        base = np.asarray(out).astype(np.float32)
        o = np.asarray(ov).astype(np.float32)
        al = o[..., 3:4] / 255.0
        mult = base[..., :3] * (1 - al) + base[..., :3] * (o[..., :3] / 255.0) * al
        borda = (o[..., 3] == 255)[..., None]
        rgb = np.where(borda, o[..., :3], mult)
        out = Image.fromarray(np.dstack([rgb, base[..., 3:]]).astype(np.uint8), "RGBA")
    return out


class Compositor:
    def __init__(self, proj, base):
        self.p = proj
        self.n = proj["noticia"]
        self.v = proj["videos"][0]
        self.base = base
        self.ff = proj["ffmpeg"]
        self.fontes = Fontes(proj["fontsdir"] if os.path.isabs(proj["fontsdir"]) else os.path.join(base, proj["fontsdir"]))
        self.src = {k: Fonte(base, c, self.ff) for k, c in self.n["fontes"].items()}
        self.pre = self.n.get("pre", 0.5)
        self.mapa = mapa_tempo(self.v["manter"], self.pre)
        self.cenas = sorted(self.n["cenas"], key=lambda c: c["de"])
        self.tit = camada_titulo(self.fontes, self.n["titulo_linhas"], META)
        self.selo = pilula(self.fontes, self.n.get("selo", "ARTIGO CIENTÍFICO"), cor=ROXO, tam=34, peso="ExtraBold")
        self.cred = etiqueta(self.fontes, self.n["credito"])
        self.aviso = etiqueta(self.fontes, self.n.get("aviso", "Imagens de publicação científica"), tam=24)
        self.rotulos = {}
        self.leitores = {}
        self.titulo_fim = self.mapa(self.n["titulo_ate"])

    def cena_em(self, t):
        for c in self.cenas:
            if self.mapa(c["de"]) <= t < self.mapa(c["ate"]):
                return c
        return None

    def painel(self, c, t, w, h):
        f = self.src[c["fonte"]]
        if f.video:
            k = id(c)
            if k not in self.leitores:
                cv = f.cfg
                vel = cv.get("velocidade", 1.0)
                vf = f"setpts=PTS/{vel}" if vel != 1.0 else ""
                ry = cv.get("recorte_y", 0)
                vf = (vf + "," if vf else "") + f"scale=1080:1920,crop=1080:{int(1080 * h / w)}:0:{ry}"
                self.leitores[k] = LeitorVideo(self.ff, f.caminho(cv["video"]), w, h, vf=vf, ss=cv.get("de", 0.0))
            return self.leitores[k].ler().convert("RGBA")
        if "pdf" in f.cfg or c.get("janela") or c.get("rolar") or c.get("marcas"):
            return painel_documento(f, c, t, w, h, self.mapa)
        ini, fim = self.mapa(c["de"]), self.mapa(c["ate"])
        prog = (t - ini) / max(0.01, fim - ini)
        z0, z1 = c.get("zoom", [1.0, 1.06])
        foco0 = c.get("foco", [0.5, 0.5])
        foco1 = c.get("foco_fim", foco0)
        a = suave(prog)
        foco = (foco0[0] + (foco1[0] - foco0[0]) * a, foco0[1] + (foco1[1] - foco0[1]) * a)
        if c.get("encaixar"):
            # foto inteira, sem ampliar além do original (nítida), com fundo desfocado da própria foto
            k = ("fundo", id(c))
            if k not in self.rotulos:
                fundo = cobrir(f.imagem(), w, h).filter(ImageFilter.GaussianBlur(28))
                self.rotulos[k] = Image.blend(fundo, Image.new("RGB", (w, h), FUNDO), 0.45).convert("RGBA")
            im = self.rotulos[k].copy()
            fi = f.imagem()
            esc = min(w / fi.width, h / fi.height) * (z0 + (z1 - z0) * prog)
            fw, fh = int(fi.width * esc), int(fi.height * esc)
            fg = fi.resize((fw, fh), Image.LANCZOS)
            x, y = (w - fw) // 2, (h - fh) // 2
            if fh > h or fw > w:          # zoom passou do painel: recorta no foco
                fx, fy = int(foco[0] * fw - w / 2), int(foco[1] * fh - h / 2)
                fx, fy = min(max(0, fx), max(0, fw - w)), min(max(0, fy), max(0, fh - h))
                fg = fg.crop((fx, fy, fx + min(w, fw), fy + min(h, fh)))
                x, y = (w - fg.width) // 2, (h - fg.height) // 2
            im.paste(fg, (x, y))
            return im
        return cobrir(f.imagem(), w, h, z0 + (z1 - z0) * prog, foco).convert("RGBA")

    def rotulo(self, texto):
        if texto not in self.rotulos:
            self.rotulos[texto] = pilula(self.fontes, texto, tam=36)
        return self.rotulos[texto]

    def quadro_cena(self, c, t, dr):
        """dr = quadro do Dr. (1080x1920 RGB) no tempo t."""
        if c is None:
            return dr.convert("RGBA")
        modo = c.get("modo", "dividida")
        if modo == "cheia":
            im = self.painel(c, t, W, H)
            if c.get("aviso"):
                im.alpha_composite(self.aviso, (W - self.aviso.width - 28, 150))
            im.alpha_composite(self.cred, (28, H - 330))
            return im
        im = Image.new("RGBA", (W, H), FUNDO + (255,))
        topo = self.painel(c, t, W, META)
        im.alpha_composite(topo, (0, 0))
        ry = self.n.get("dr_recorte_y", 380)
        im.paste(dr.crop((0, ry, W, ry + META)), (0, META))
        d = ImageDraw.Draw(im)
        d.rectangle([0, META - 3, W, META + 3], fill=ROXO + (255,))
        # aviso no alto à esquerda; crédito embaixo à esquerda, acima do rótulo da costura
        # (o centro do painel é do trecho em destaque, que a janela acompanha)
        if c.get("aviso"):
            im.alpha_composite(self.aviso, (24, 130))
        if c.get("credito", True):
            im.alpha_composite(self.cred, (24, META - self.cred.height - 50))
        if c.get("rotulo"):
            r = self.rotulo(c["rotulo"])
            im.alpha_composite(r, ((W - r.width) // 2, META - r.height // 2))
        return im

    def quadro(self, t, dr):
        c = self.cena_em(t)
        im = self.quadro_cena(c, t, dr)
        # crossfade curto na troca de cena (entrada de cada cena e volta para o Dr.)
        borda = None
        for k in self.cenas:
            for tb in (self.mapa(k["de"]), self.mapa(k["ate"])):
                if 0 < t - tb < TRANSICAO and tb > 0.05:
                    borda = tb
        if borda is not None:
            antes = self.cena_em(borda - 1.0 / FPS)
            if antes is not c and not (antes and c and antes.get("fonte") == c.get("fonte") and
                                       antes.get("modo") == c.get("modo") and not self.src[c["fonte"]].video):
                im0 = self.quadro_cena(antes, borda - 1.0 / FPS, dr)
                a = suave((t - borda) / TRANSICAO)
                im = Image.blend(im0, im, a)
        # entrada estilo notícia: título, selo e crédito até titulo_ate
        if t < self.titulo_fim:
            a_in = suave(t / 0.25) if self.pre > 0 else 1.0
            a_out = suave((self.titulo_fim - t) / 0.25)
            a = min(a_in, a_out)
            ov = self.tit.copy()
            sy = META - 96 * (len(self.n["titulo_linhas"]) - 1) / 2 - 62 - self.selo.height
            ov.alpha_composite(self.selo, ((W - self.selo.width) // 2, int(sy)))
            if a < 1:
                ov.putalpha(ov.getchannel("A").point(lambda x: int(x * a)))
            im.alpha_composite(ov)
        return im.convert("RGB")

    def fechar(self):
        for l in self.leitores.values():
            l.fechar()


# ---------------------------------------------------------------- trilha

def gerar_trilha(dur, pre, semente=7):
    """Base instrumental original (síntese própria, sem amostras de terceiros): pad em Lá menor
    (Am-F-C-G, 92 BPM), arpejo suave, baixo e pulso leve; no gancho, subida curta e impacto."""
    from scipy.signal import fftconvolve, lfilter
    rng = np.random.default_rng(semente)
    n = int(dur * SR)
    t = np.arange(n) / SR
    bpm = 92.0
    beat = 60 / bpm
    compasso = 4 * beat
    acordes = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]   # Am F C G (MIDI)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    pad = np.zeros(n)
    arp = np.zeros(n)
    baixo = np.zeros(n)
    pulso = np.zeros(n)
    nb = int(math.ceil(dur / compasso)) + 1
    for k in range(nb):
        t0 = pre + k * compasso
        ac = acordes[k % 4]
        i0, i1 = int(max(0, t0) * SR), int(min(dur, t0 + compasso + 0.6) * SR)
        if i1 <= i0:
            continue
        tt = t[i0:i1] - t0
        env = np.minimum(1, tt / 0.8) * np.minimum(1, np.maximum(0, (compasso + 0.6 - tt) / 0.6))
        for m in ac:
            for det in (-0.08, 0.0, 0.08):
                f = hz(m + det / 1.0)
                pad[i0:i1] += env * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt + 0.3)) / 9
        fb = hz(ac[0] - 12)
        baixo[i0:i1] += env * np.sin(2 * np.pi * fb * tt) * 0.5
        # arpejo em colcheias, notas do acorde uma oitava acima
        for j in range(8):
            ts_ = t0 + j * beat / 2
            if ts_ < 0 or ts_ >= dur:
                continue
            m = ac[[0, 1, 2, 1, 0, 2, 1, 2][j]] + 12
            a0 = int(ts_ * SR)
            a1 = min(n, a0 + int(1.2 * SR))
            tq = t[a0:a1] - ts_
            arp[a0:a1] += np.sin(2 * np.pi * hz(m) * tq) * np.exp(-tq * 5.5) * (0.9 if j % 2 == 0 else 0.6)
        for j in range(4):
            ts_ = t0 + j * beat
            if ts_ < 0 or ts_ >= dur:
                continue
            a0 = int(ts_ * SR)
            a1 = min(n, a0 + int(0.35 * SR))
            tq = t[a0:a1] - ts_
            pulso[a0:a1] += np.sin(2 * np.pi * (48 + 40 * np.exp(-tq * 30)) * tq) * np.exp(-tq * 9)
    # pad mais escuro (passa-baixa de 1 polo)
    pad = lfilter([0.08], [1, -0.92], pad)
    mix = 0.55 * pad + 0.16 * arp + 0.30 * baixo + 0.22 * pulso
    # gancho: subida de ruído filtrado até o impacto em "pre" e grave longo
    if pre > 0.05:
        i1 = int(pre * SR)
        sub = rng.standard_normal(i1) * np.linspace(0, 1, i1) ** 2
        sub = lfilter([0.15], [1, -0.85], sub)
        mix[:i1] += 0.35 * sub
    i0 = int(pre * SR)
    tq = t[i0:min(n, i0 + int(2.5 * SR))] - pre
    mix[i0:i0 + len(tq)] += 0.9 * np.sin(2 * np.pi * (40 + 30 * np.exp(-tq * 6)) * tq) * np.exp(-tq * 2.2)
    ruido = rng.standard_normal(len(tq)) * np.exp(-tq * 7)
    mix[i0:i0 + len(tq)] += 0.12 * lfilter([0.3], [1, -0.6], ruido)
    # reverb curto (resposta exponencial própria) e estéreo leve
    ir_n = int(1.6 * SR)
    ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 3.2)
    ir = lfilter([0.2], [1, -0.8], ir)
    ir /= np.abs(ir).sum() / 6
    wet_l = fftconvolve(mix, ir)[:n]
    wet_r = fftconvolve(mix, np.roll(ir, 331))[:n]
    l = mix + 0.35 * wet_l
    r = mix + 0.35 * wet_r
    st = np.stack([l, r], 1)
    st /= np.max(np.abs(st)) + 1e-9
    return st * 0.9


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def ler_audio(ff, arq, ini=None, fim=None):
    cmd = [ff, "-nostdin", "-v", "error"]
    if ini is not None:
        cmd += ["-ss", f"{ini:.3f}", "-to", f"{fim:.3f}"]
    cmd += ["-i", arq, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def montar_audio(proj, base, saida_wav, duracao, relatorio):
    """Voz (trechos do bruto) + trilha com ducking. Devolve os níveis medidos."""
    ff = proj["ffmpeg"]
    n_ = proj["noticia"]
    v = proj["videos"][0]
    pre = n_.get("pre", 0.5)
    ent = v["entrada"] if os.path.isabs(v["entrada"]) else os.path.join(base, v["entrada"])
    bruto = ler_audio(ff, ent)
    partes = [np.zeros((int(round(pre * SR)), 2))]
    for a, b in v["manter"]:
        seg = bruto[int(round(a * SR)):int(round(b * SR))].copy()
        r = min(len(seg) // 2, int(0.02 * SR))
        if r:
            rampa = np.linspace(0, 1, r)[:, None]
            seg[:r] *= rampa
            seg[-r:] *= rampa[::-1]
        partes.append(seg)
    voz = np.concatenate(partes)
    n = int(round(duracao * SR))
    voz = np.pad(voz, ((0, max(0, n - len(voz))), (0, 0)))[:n]
    # nível da voz: média RMS das janelas de 50 ms com fala (acima do piso + 12 dB)
    jan = int(0.05 * SR)
    m = voz[: len(voz) // jan * jan].mean(1).reshape(-1, jan)
    dbs = 20 * np.log10(np.sqrt((m ** 2).mean(1)) + 1e-12)
    vivas = dbs[dbs > -90]
    piso = np.percentile(vivas, 5)
    fala = m[dbs > piso + 12]
    voz_db = rms_db(fala)
    tr = n_.get("trilha", {})
    if tr.get("arquivo"):
        arq = tr["arquivo"] if os.path.isabs(tr["arquivo"]) else os.path.join(base, tr["arquivo"])
        mus = ler_audio(ff, arq)
        if len(mus) < n:
            mus = np.tile(mus, (n // len(mus) + 1, 1))
        mus = mus[:n]
        origem = os.path.basename(arq)
    else:
        mus = gerar_trilha(duracao, pre, tr.get("semente", 7))[:n]
        origem = "base instrumental original gerada por fea_artigo_noticia.gerar_trilha (sem direitos de terceiros)"
    corpo = mus[int((pre + 4) * SR):] if len(mus) > (pre + 8) * SR else mus
    mus_db = rms_db(corpo)
    g_fundo = tr.get("fundo_db", -26)
    g_gancho = tr.get("gancho_db", -12)
    titulo_fim = mapa_tempo(v["manter"], pre)(n_["titulo_ate"])
    tt = np.arange(n) / SR
    alvo = np.full(n, voz_db + g_fundo)
    # gancho: mais alto, desce até o fundo em 0,8 s depois do título
    desce = np.clip((tt - titulo_fim) / 0.8, 0, 1)
    alvo = (voz_db + g_gancho) * (1 - desce) + (voz_db + g_fundo) * desce
    ganho = 10 ** ((alvo - mus_db) / 20)
    # final: fade da trilha junto com o fade do vídeo
    ff_ = float(v.get("fade_final", 0.4))
    ganho *= np.clip((duracao - tt) / max(0.05, ff_ + 0.6), 0, 1)
    ganho *= np.clip(tt / 0.05, 0, 1)
    mix = voz + mus * ganho[:, None]
    fv = np.clip((duracao - tt) / max(0.05, ff_), 0, 1)
    mix *= fv[:, None]
    pico = np.max(np.abs(mix))
    if pico > 0.97:
        mix *= 0.97 / pico
    import wave
    pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
    with wave.open(saida_wav, "wb") as wv:
        wv.setnchannels(2)
        wv.setsampwidth(2)
        wv.setframerate(SR)
        wv.writeframes(pcm.tobytes())
    info = {"voz_db": round(voz_db, 1), "trilha_fundo_abaixo_da_voz_db": g_fundo,
            "trilha_gancho_abaixo_da_voz_db": g_gancho, "origem_trilha": origem}
    relatorio.update(info)
    return info


# ---------------------------------------------------------------- legenda (padrão da skill)

def gerar_legenda(proj, base, caminho_ass):
    """Mesma legenda do fea_editar_video (Montserrat Bold 56, ~80% da altura), deslocada pelo
    gancho, sem o título ASS (o título é a faixa branca desenhada aqui) e só depois do título."""
    v = dict(proj["videos"][0])
    n_ = proj["noticia"]
    ff = proj["ffmpeg"]
    pre = n_.get("pre", 0.5)
    ent = v["entrada"] if os.path.isabs(v["entrada"]) else os.path.join(base, v["entrada"])
    trp = v["transcricao"] if os.path.isabs(v["transcricao"]) else os.path.join(base, v["transcricao"])
    db_voz = fe.perfil_voz(ff, ent)
    trans = json.load(open(trp, encoding="utf-8"))
    palavras = []
    for seg in trans:
        ws = [dict(w) for w in seg["words"]]
        for i, w in enumerate(ws):
            if i and palavras and not w["w"].startswith(" "):
                palavras[-1]["w"] += w["w"]
                palavras[-1]["e"] = min(w["e"], palavras[-1]["s"] + 1.2)
                continue
            palavras.append(dict(w, e=min(w["e"], w["s"] + 1.2), e0=w["e"], ini=(i == 0)))
    palavras.sort(key=lambda p: p["s"])
    palavras = fe.numerar_enumeracao(palavras)
    palavras = fe.juntar_quantidades(palavras, *db_voz)
    for a, b in v.get("remover_legenda", []):
        palavras = [p for p in palavras if not (a <= (p["s"] + p["e"]) / 2 < b)]
    palavras = [p for p in palavras if re.sub(r"[^\w]", "", p["w"]).lower() != "ó"]
    palavras = fe.ancorar_na_voz(palavras, *db_voz)
    palavras, dur = fe.remapear_palavras(palavras, v["manter"])
    for p in palavras:
        p["s"] += pre
        p["e"] += pre
    dur += pre + n_.get("pos", 0.0)
    passo = db_voz[2]
    db_ed = np.concatenate([np.zeros(int(pre / passo))] +
                           [db_voz[0][int(a / passo):int(b / passo)] for a, b in v["manter"]])
    titulo_fim = mapa_tempo(v["manter"], pre)(n_["titulo_ate"])
    antigo = fe.TITULO_DUR
    fe.TITULO_DUR = titulo_fim
    try:
        fe.gerar_ass(v, palavras, dur, caminho_ass, voz=(db_ed, db_voz[1], passo))
    finally:
        fe.TITULO_DUR = antigo
    linhas = [l for l in open(caminho_ass, encoding="utf-8") if not l.startswith("Dialogue: 1,") or ",Titulo," not in l]
    open(caminho_ass, "w", encoding="utf-8").write("".join(linhas))
    return dur


def _seg(ts_):
    h, m, x = ts_.split(":")
    return int(h) * 3600 + int(m) * 60 + float(x)


def reposicionar_legenda(caminho_ass, comp):
    """Na tela dividida a legenda sobe para logo abaixo da costura (como nas referências
    Skincare): no lugar padrão (~80%) ela cairia na boca do Dr., que ocupa a metade de baixo.
    Legenda que atravessa a troca de cena é dividida em dois eventos."""
    sobe = fe.LEGENDA_Y + 20 - comp.n.get("legenda_dividida_y", 1100)
    limites = sorted({round(comp.mapa(c[k]), 3) for c in comp.cenas for k in ("de", "ate")})
    saida = []
    for linha in open(caminho_ass, encoding="utf-8"):
        if not linha.startswith("Dialogue: 0,") or ",Legenda," not in linha:
            saida.append(linha)
            continue
        p = linha.split(",", 9)
        s, e = _seg(p[1]), _seg(p[2])
        cortes = [s] + [t for t in limites if s < t < e] + [e]
        pedacos = []
        for a, b in zip(cortes, cortes[1:]):
            if b - a < 0.02:
                continue
            c = comp.cena_em((a + b) / 2)
            txt = p[9]
            if c is not None and c.get("modo", "dividida") == "dividida":
                txt = re.sub(r"\\pos\((\d+),(\d+)\)", lambda m: f"\\pos({m.group(1)},{int(m.group(2)) - sobe})", txt)
            if pedacos and pedacos[-1][2] == txt:      # mesma posição: um evento só
                pedacos[-1][1] = b
            else:
                pedacos.append([a, b, txt])
        # pedaço curto (< 0,35 s) numa posição pisca na tela: fica na posição do vizinho
        while len(pedacos) > 1:
            k = min(range(len(pedacos)), key=lambda i: pedacos[i][1] - pedacos[i][0])
            if pedacos[k][1] - pedacos[k][0] >= 0.35:
                break
            if k + 1 < len(pedacos):
                pedacos[k + 1][0] = pedacos[k][0]
            else:
                pedacos[k - 1][1] = pedacos[k][1]
            del pedacos[k]
        for a, b, txt in pedacos:
            saida.append(",".join(p[:1] + [fe.ts(a), fe.ts(b)] + p[3:9] + [txt]))
    open(caminho_ass, "w", encoding="utf-8").write("".join(saida))


# ---------------------------------------------------------------- render

def base_dr(proj, base, arq):
    """Trechos do bruto, já girados para 1080x1920, com o gancho (1º quadro parado) na frente."""
    v = proj["videos"][0]
    ff = proj["ffmpeg"]
    pre = proj["noticia"].get("pre", 0.5)
    ent = v["entrada"] if os.path.isabs(v["entrada"]) else os.path.join(base, v["entrada"])
    partes, rot = [], []
    for i, (a, b) in enumerate(v["manter"]):
        partes.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H},setsar=1,fps={FPS}[v{i}]")
        rot.append(f"[v{i}]")
    filtro = ";".join(partes) + ";" + "".join(rot) + f"concat=n={len(rot)}:v=1:a=0[c];" \
        f"[c]tpad=start_duration={pre}:start_mode=clone:stop_duration={proj['noticia'].get('pos', 0.0) + 0.2}:stop_mode=clone[o]"
    subprocess.run([ff, "-y", "-v", "error", "-i", ent, "-filter_complex", filtro, "-map", "[o]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", arq], check=True)


def main():
    args = sys.argv[1:]
    proj_arq = args[0]
    base = os.path.dirname(os.path.abspath(proj_arq))
    proj = json.load(open(proj_arq, encoding="utf-8"))
    v = proj["videos"][0]
    v["manter"] = [[float(t[0]), float(t[1])] for t in v["manter"]]   # "exato" é sempre exato aqui
    saida = v["saida"] if os.path.isabs(v["saida"]) else os.path.join(base, v["saida"])
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    global CACHE
    CACHE = os.path.join(proj["noticia"].get("trabalho") or base, "cache")
    os.makedirs(CACHE, exist_ok=True)
    ass = saida.rsplit(".", 1)[0] + ".ass"
    dur = gerar_legenda(proj, base, ass)
    comp = Compositor(proj, base)
    reposicionar_legenda(ass, comp)
    print(f"legenda: {ass} ({dur:.2f} s)")
    if "--so-legenda" in args:
        return
    dr_arq = os.path.join(CACHE, "base_dr.mp4")
    if not os.path.exists(dr_arq) or os.path.getmtime(dr_arq) < os.path.getmtime(proj_arq):
        base_dr(proj, base, dr_arq)
    if "--quadros" in args:
        # "b12.5" = 12,5 s do bruto (convertido para a edição)
        tempos = [comp.mapa(float(x[1:])) if x.startswith("b") else float(x)
                  for x in args[args.index("--quadros") + 1].split(",")]
        for tq in tempos:
            dr = LeitorVideo(proj["ffmpeg"], dr_arq, W, H, ss=tq)
            im = comp.quadro(tq, dr.ler())
            dr.fechar()
            # legenda queimada também, para conferir sobreposição
            tmp = os.path.join(CACHE, f"q_{tq:07.2f}.png")
            im.save(tmp)
            esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
            subprocess.run([proj["ffmpeg"], "-y", "-v", "error", "-i", tmp, "-vf",
                            f"setpts=PTS+{tq}/TB,ass='{esc}':fontsdir='{comp.fontes.pasta}'",
                            "-frames:v", "1", tmp.replace("q_", "Q_")], check=True)
            print(tmp.replace("q_", "Q_"))
        comp.fechar()
        return
    rel = {}
    wav = os.path.join(CACHE, "audio_final.wav")
    montar_audio(proj, base, wav, dur, rel)
    previa = "--previa" in args
    ff = proj["ffmpeg"]
    esc = ass.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    nf = int(round(dur * FPS))
    fade = float(v.get("fade_final", 0.4))
    vf = f"ass='{esc}':fontsdir='{comp.fontes.pasta}',fade=t=out:st={max(0, dur - fade):.3f}:d={fade}"
    if previa:
        vf += ",scale=540:960"
        saida = saida.rsplit("/", 1)[0] + "/PREVIA " + saida.rsplit("/", 1)[1]
        codec = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "128k"]
    else:
        codec = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high",
                 "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    enc = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", wav, "-vf", vf, "-map", "0:v", "-map", "1:a",
                            *codec, "-pix_fmt", "yuv420p", "-r", str(FPS), "-shortest",
                            "-movflags", "+faststart", saida], stdin=subprocess.PIPE)
    dr = LeitorVideo(ff, dr_arq, W, H)
    for i in range(nf):
        t = i / FPS
        q = dr.ler()
        enc.stdin.write(comp.quadro(t, q).tobytes())
        if i % 300 == 0:
            print(f"  {t:6.1f}/{dur:.1f} s", flush=True)
    enc.stdin.close()
    enc.wait()
    dr.fechar()
    comp.fechar()
    rel.update(saida=saida, duracao=round(dur, 2))
    json.dump(rel, open(saida.rsplit(".", 1)[0] + ".noticia.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(rel, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
