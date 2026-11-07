#!/usr/bin/env python3
"""FEA: ilustrações animadas para os criativos Elite Mentoring (estilo dos slides do pitch:
fundo #011A24, brilho turquesa/água, ícones de linha, serifa com palavra em destaque).

Cada ilustração vira uma sequência PNG com transparência (painel 1000x600), que o
fea_criativo.py sobrepõe ao vídeo no instante em que o Dr. fala do assunto.

Tipos:
  crescimento  barras subindo + linha com seta (crescer a clínica, faturamento, conversão)
  pilares      pilares subindo um a um, com rótulos (avaliação, planejamento, marketing, vendas)
  passos       cartões numerados em sequência com seta (formulário > diagnóstico > plano)
  plano        itens que se somam num plano completo (toxina + preenchimento + bio...)
  relogio      anel que se completa com "2 MIN" (formulário rápido)

Uso direto (gera uma prévia): python3 fea_ilustracoes.py fontsdir saida_dir
"""
import hashlib
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

PW, PH = 1000, 600          # painel
FPS = 30
BG = (1, 26, 36)
SURF = (7, 43, 56)
LINE = (22, 66, 79)
TEAL = (98, 185, 180)
AQUA = (134, 249, 248)
INK = (234, 246, 246)
MUTED = (147, 179, 184)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def fase(t, a, b):
    return ease((t - a) / (b - a)) if b > a else float(t >= a)


class Fontes:
    def __init__(self, d):
        self.d = d
        self.cache = {}

    def get(self, nome, tam):
        k = (nome, tam)
        if k not in self.cache:
            arq = {"titulo": "Gloock-Regular.ttf",
                   "rotulo": "Rene Bieder - GalanoGrotesque Bold.otf",
                   "forte": "Rene Bieder - GalanoGrotesque ExtraBold.otf"}[nome]
            self.cache[k] = ImageFont.truetype(os.path.join(self.d, arq), tam)
        return self.cache[k]


def texto_espacado(dr, xy, txt, fonte, cor, esp=0, ancora="mm"):
    """Texto com espaçamento entre letras (o 'eyebrow' da página), centralizado em xy."""
    if not esp:
        dr.text(xy, txt, font=fonte, fill=cor, anchor=ancora)
        return
    ws = [dr.textlength(c, font=fonte) for c in txt]
    total = sum(ws) + esp * (len(txt) - 1)
    x = xy[0] - total / 2
    for c, w in zip(txt, ws):
        dr.text((x, xy[1]), c, font=fonte, fill=cor, anchor="lm")
        x += w + esp


def titulo_destaque(dr, cx, y, titulo, destaque, F, tam=50):
    """Título em Gloock branco com a palavra de destaque em água (como 'Clínica Elite' no pitch)."""
    f = F.get("titulo", tam)
    partes = [(titulo, INK)]
    if destaque and destaque in titulo:
        a, b = titulo.split(destaque, 1)
        partes = [(a, INK), (destaque, AQUA), (b, INK)]
    total = sum(dr.textlength(p, font=f) for p, _ in partes)
    x = cx - total / 2
    for p, c in partes:
        dr.text((x, y), p, font=f, fill=c, anchor="lm")
        x += dr.textlength(p, font=f)


def painel(t, dur):
    """Fundo do painel: superfície escura arredondada, borda e brilho turquesa no canto."""
    a = fase(t, 0, 0.3) * (1 - fase(t, dur - 0.3, dur))
    base = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dr = ImageDraw.Draw(base)
    dr.rounded_rectangle([4, 4, PW - 5, PH - 5], 28, fill=BG + (232,), outline=LINE + (255,), width=2)
    brilho = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    ImageDraw.Draw(brilho).ellipse([PW * 0.45, -PH * 0.6, PW * 1.3, PH * 0.55], fill=TEAL + (70,))
    brilho = brilho.filter(ImageFilter.GaussianBlur(90))
    mascara = Image.new("L", (PW, PH), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([4, 4, PW - 5, PH - 5], 28, fill=255)
    base.alpha_composite(Image.composite(brilho, Image.new("RGBA", (PW, PH), (0, 0, 0, 0)), mascara))
    return base, a


def com_brilho(camada, raio=10, forca=1.6):
    g = camada.filter(ImageFilter.GaussianBlur(raio))
    if forca != 1:
        r, gg, b, al = g.split()
        al = al.point(lambda v: min(255, int(v * forca)))
        g = Image.merge("RGBA", (r, gg, b, al))
    out = Image.new("RGBA", camada.size, (0, 0, 0, 0))
    out.alpha_composite(g)
    out.alpha_composite(camada)
    return out


# ------------------------------------------------------------------ tipos

def q_crescimento(t, dur, p, F):
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 78, p.get("titulo", "Sua clínica crescendo"), p.get("destaque", "crescendo"), F)
    texto_espacado(dr, (PW / 2, 128), p.get("eyebrow", "FATURAMENTO"), F.get("rotulo", 22), TEAL, 6)
    camada = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    n, x0, x1, base_y, topo = 6, 150, 850, 530, 190
    larg = (x1 - x0) / n
    alturas = [0.22, 0.32, 0.42, 0.55, 0.72, 0.95]
    topos = []
    for i in range(n):
        f = fase(t, 0.35 + i * 0.16, 0.85 + i * 0.16)
        h = (base_y - topo) * alturas[i] * f
        bx = x0 + i * larg + larg * 0.18
        cor = AQUA if i == n - 1 else TEAL
        alfa = 255 if i == n - 1 else 150 + i * 18
        if h > 2:
            dc.rounded_rectangle([bx, base_y - h, bx + larg * 0.64, base_y], 8, fill=cor + (alfa,))
        topos.append((bx + larg * 0.32, base_y - (base_y - topo) * alturas[i]))
    # linha de tendência desenhada por cima, com seta no fim
    fl = fase(t, 1.2, 2.3)
    if fl > 0:
        pts = [(x, y - 26) for x, y in topos]
        total = sum(math.dist(pts[i], pts[i + 1]) for i in range(n - 1))
        alvo, acc, desenho = total * fl, 0.0, [pts[0]]
        for i in range(n - 1):
            d = math.dist(pts[i], pts[i + 1])
            if acc + d >= alvo:
                r = (alvo - acc) / d
                desenho.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * r, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * r))
                break
            desenho.append(pts[i + 1])
            acc += d
        dc.line(desenho, fill=AQUA + (255,), width=7, joint="curve")
        if fl > 0.97:
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            ang = math.atan2(yb - ya, xb - xa)
            ponta = [(xb + 30 * math.cos(ang), yb + 30 * math.sin(ang)),
                     (xb + 22 * math.cos(ang + 2.4), yb + 22 * math.sin(ang + 2.4)),
                     (xb + 22 * math.cos(ang - 2.4), yb + 22 * math.sin(ang - 2.4))]
            dc.polygon(ponta, fill=AQUA + (255,))
    dc.line([(x0 - 10, base_y + 2), (x1 + 10, base_y + 2)], fill=LINE + (255,), width=3)
    img.alpha_composite(com_brilho(camada))
    return img, a


def q_pilares(t, dur, p, F):
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 78, p.get("titulo", "Os pilares da clínica"), p.get("destaque", "pilares"), F)
    rot = p.get("itens", ["AVALIAÇÃO", "PLANEJAMENTO", "MARKETING", "VENDAS"])
    n = len(rot)
    camada = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    base_y, alt = 470, 290
    larg = 880 / n
    for i, r in enumerate(rot):
        f = fase(t, 0.3 + i * 0.28, 0.9 + i * 0.28)
        cx = 60 + larg * (i + 0.5)
        w = min(120, larg * 0.5)
        h = alt * f
        if h > 34:      # abaixo disso o fuste ainda não cabe entre a base e o capitel
            topo = base_y - h
            dc.rectangle([cx - w / 2, topo + 14, cx + w / 2, base_y - 12], fill=TEAL + (120,))
            for k in range(1, 4):   # caneluras
                xk = cx - w / 2 + w * k / 4
                dc.line([(xk, topo + 20), (xk, base_y - 16)], fill=AQUA + (170,), width=3)
            dc.rounded_rectangle([cx - w / 2 - 14, topo, cx + w / 2 + 14, topo + 16], 4, fill=AQUA + (255,))
            dc.rounded_rectangle([cx - w / 2 - 14, base_y - 14, cx + w / 2 + 14, base_y + 2], 4, fill=AQUA + (255,))
        fr = fase(t, 0.6 + i * 0.28, 1.0 + i * 0.28)
        if fr > 0:
            texto_espacado(dc, (cx, base_y + 48), r, F.get("rotulo", 21 if max(map(len, rot)) > 10 else 24), INK + (int(255 * fr),), 2)
    img.alpha_composite(com_brilho(camada, 8, 1.3))
    return img, a


def q_passos(t, dur, p, F):
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 78, p.get("titulo", "Como funciona"), p.get("destaque", ""), F)
    itens = p.get("itens", [["Formulário", "2 minutos"], ["Diagnóstico", "com o meu time"], ["Plano", "para crescer"]])
    n = len(itens)
    camada = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    gap = 58
    w = (PW - 90 - gap * (n - 1)) / n
    y0, h = 170, 360
    for i, (tit, sub) in enumerate(itens):
        f = fase(t, 0.3 + i * 0.45, 0.8 + i * 0.45)
        if f <= 0:
            continue
        x = 45 + i * (w + gap)
        dy = (1 - f) * 40
        al = int(255 * f)
        dc.rounded_rectangle([x, y0 + dy, x + w, y0 + h + dy], 18, fill=SURF + (int(230 * f),), outline=LINE + (al,), width=2)
        dc.text((x + 34, y0 + 92 + dy), str(i + 1), font=F.get("titulo", 92), fill=AQUA + (al,), anchor="ls")
        dc.text((x + 34, y0 + 190 + dy), tit, font=F.get("titulo", 38 if len(tit) < 11 else 31), fill=INK + (al,), anchor="ls")
        for k, linha in enumerate(sub.split("\n")):
            dc.text((x + 34, y0 + 245 + dy + k * 34), linha, font=F.get("rotulo", 26), fill=MUTED + (al,), anchor="ls")
        if i < n - 1:
            fa = fase(t, 0.65 + i * 0.45, 0.95 + i * 0.45)
            if fa > 0:
                ax = x + w + 8
                ay = y0 + h / 2
                dc.line([(ax, ay), (ax + (gap - 16) * fa, ay)], fill=AQUA + (255,), width=4)
                if fa > 0.95:
                    dc.polygon([(ax + gap - 10, ay), (ax + gap - 24, ay - 9), (ax + gap - 24, ay + 9)], fill=AQUA + (255,))
    img.alpha_composite(com_brilho(camada, 6, 1.1))
    return img, a


def q_plano(t, dur, p, F):
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 78, p.get("titulo", "Plano de tratamento completo"), p.get("destaque", "completo"), F)
    itens = p.get("itens", ["TOXINA", "PREENCHIMENTO", "BIOESTIMULADOR", "FIOS"])
    camada = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    # chips em no máximo 2 linhas: a fonte diminui até caber (com 5 itens, a 3ª linha
    # encavalava no rodapé: "TECNOLOGIAS" riscado pela linha, Keila 07/11)
    for tam in (34, 30, 27, 24):
        fr = F.get("forte", tam)
        pad, gap = int(tam * 1.9), int(tam * 1.5)
        linhas, atual, larg_lin = [], [], 0
        for it in itens:
            wc = dc.textlength(it, font=fr) + pad
            if atual and larg_lin + wc > 900:
                linhas.append(atual)
                atual, larg_lin = [], 0
            atual.append((it, wc))
            larg_lin += wc + gap
        linhas.append(atual)
        if len(linhas) <= 2:
            break
    alt = int(tam * 2.25)
    passo_lin = alt + 44
    k = 0
    y = 230 if len(linhas) == 1 else 175
    for li, ln in enumerate(linhas):
        total = sum(wc for _, wc in ln) + gap * (len(ln) - 1)
        x = (PW - total) / 2
        for j, (it, wc) in enumerate(ln):
            f = fase(t, 0.3 + k * 0.3, 0.7 + k * 0.3)
            if f > 0:
                al = int(255 * f)
                dy = (1 - f) * 30
                dc.rounded_rectangle([x, y + dy, x + wc, y + alt + dy], alt // 2, fill=SURF + (int(240 * f),), outline=AQUA + (al,), width=3)
                dc.text((x + wc / 2, y + alt / 2 + 2 + dy), it, font=fr, fill=INK + (al,), anchor="mm")
                if j < len(ln) - 1:
                    dc.text((x + wc + gap / 2, y + alt / 2), "+", font=F.get("forte", int(tam * 1.4)), fill=AQUA + (al,), anchor="mm")
            x += wc + gap
            k += 1
        y += passo_lin
    fz = fase(t, 0.4 + k * 0.3, 0.8 + k * 0.3)
    if fz > 0:
        yb = y + 20
        dc.line([(PW / 2 - 300 * fz, yb), (PW / 2 + 300 * fz, yb)], fill=AQUA + (255,), width=4)
        texto_espacado(dc, (PW / 2, yb + 46), p.get("rodape", "UM PLANO, NÃO UM PROCEDIMENTO"), F.get("rotulo", 26),
                       AQUA + (int(255 * fz),), 5)
    img.alpha_composite(com_brilho(camada, 7, 1.2))
    return img, a


def q_relogio(t, dur, p, F):
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 78, p.get("titulo", "Formulário rápido"), p.get("destaque", "rápido"), F)
    camada = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    dc = ImageDraw.Draw(camada)
    cx, cy, r = PW / 2, 340, 170
    dc.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE + (255,), width=16)
    f = fase(t, 0.3, 1.9)
    if f > 0:
        dc.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * f, fill=AQUA + (255,), width=16)
    fn = fase(t, 0.5, 1.0)
    dc.text((cx, cy - 18), p.get("numero", "2"), font=F.get("titulo", 150), fill=INK + (int(255 * fn),), anchor="mm")
    texto_espacado(dc, (cx, cy + 82), p.get("unidade", "MINUTOS"), F.get("rotulo", 28), TEAL + (int(255 * fn),), 6)
    img.alpha_composite(com_brilho(camada, 8, 1.2))
    return img, a


def cartao_abertura(gancho, destaque, selo, logo, fontsdir, saida):
    """Tela cheia da marca (fundo da página com brilhos turquesa, logo, selo e gancho grande)
    para cobrir o começo em que o Dr. ainda está se ajeitando na cadeira."""
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), BG + (255,))
    for (x0, y0, x1, y1, cor, a) in [(400, -500, 1500, 700, TEAL, 95), (-500, 1300, 600, 2300, AQUA, 45)]:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([x0, y0, x1, y1], fill=cor + (a,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    lg = Image.open(logo).convert("RGBA")
    lg.thumbnail((640, 400))
    img.alpha_composite(lg, ((W - lg.width) // 2, 560))
    F = Fontes(fontsdir)
    dr = ImageDraw.Draw(img)
    texto_espacado(dr, (W / 2, 860), selo, F.get("rotulo", 30), TEAL, 8)
    palavras, linhas, at = gancho.split(), [], ""
    for w in palavras:
        if len(at + " " + w) > 18 and at:
            linhas.append(at)
            at = w
        else:
            at = (at + " " + w).strip()
    linhas.append(at)
    for i, l in enumerate(linhas):
        titulo_destaque(dr, W / 2, 1000 + i * 108, l, destaque if destaque in l else "", F, tam=92)
    dr.line([(W / 2 - 60, 1000 + len(linhas) * 108 + 10), (W / 2 + 60, 1000 + len(linhas) * 108 + 10)], fill=AQUA, width=4)
    img.save(saida)
    return saida


def q_fotos(t, dur, p, F):
    """Fotos impressas (borda branca, levemente giradas) entrando uma a uma: 'antes' do Dr."""
    img, a = painel(t, dur)
    dr = ImageDraw.Draw(img)
    titulo_destaque(dr, PW / 2, 70, p.get("titulo", "Onde eu comecei"), p.get("destaque", "comecei"), F)
    fotos = p.get("fotos", [])
    n = len(fotos)
    angs = [-7, 3, -3, 6][:n]
    w = 250
    for i, (arq, ang) in enumerate(zip(fotos, angs)):
        f = fase(t, 0.25 + i * 0.4, 0.75 + i * 0.4)
        if f <= 0:
            continue
        chave = (arq, w)
        if chave not in _FOTOS:
            im = ImageOps.exif_transpose(Image.open(arq)).convert("RGB")
            alvo = (w, int(w * 1.25))
            im = ImageOps.fit(im, alvo, Image.LANCZOS)
            im = ImageEnhance.Color(im).enhance(0.75)      # tom levemente esmaecido de foto antiga
            moldura = Image.new("RGBA", (alvo[0] + 24, alvo[1] + 64), (245, 245, 240, 255))
            moldura.paste(im, (12, 12))
            _FOTOS[chave] = moldura
        fr = _FOTOS[chave].rotate(ang, expand=True, resample=Image.BICUBIC)
        esc = 0.85 + 0.15 * f
        fr = fr.resize((int(fr.width * esc), int(fr.height * esc)), Image.LANCZOS)
        if f < 1:
            r, g, b, al = fr.split()
            fr = Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * f))))
        cx = PW / 2 + (i - (n - 1) / 2) * 290
        cy = 345 + (1 - f) * 40
        sombra = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        sombra.putalpha(fr.split()[3].point(lambda v: int(v * 0.45)))
        sombra = sombra.filter(ImageFilter.GaussianBlur(12))
        img.alpha_composite(sombra, (int(cx - fr.width / 2 + 8), int(cy - fr.height / 2 + 12)))
        img.alpha_composite(fr, (int(cx - fr.width / 2), int(cy - fr.height / 2)))
    return img, a


_FOTOS = {}


TIPOS = {"fotos": q_fotos,
         "crescimento": q_crescimento, "pilares": q_pilares, "passos": q_passos, "plano": q_plano,
         "relogio": q_relogio}


def gerar(tipo, params, dur, fontsdir, pasta_cache):
    """Gera (ou reaproveita) a sequência PNG e devolve o padrão de nome para o FFmpeg."""
    chave = hashlib.sha1(json.dumps([tipo, params, dur, 3], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
    pasta = os.path.join(pasta_cache, f"{tipo}-{chave}")
    n = int(round(dur * FPS))
    if not (os.path.isdir(pasta) and len(os.listdir(pasta)) >= n):
        os.makedirs(pasta, exist_ok=True)
        F = Fontes(fontsdir)
        for i in range(n):
            t = i / FPS
            img, a = TIPOS[tipo](t, dur, params, F)
            # entrada: sobe 30 px e aparece; saída: some
            if a < 1:
                r, g, b, al = img.split()
                img = Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))
            sub = int((1 - fase(t, 0, 0.35)) * 30)
            if sub:
                novo = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
                novo.alpha_composite(img, (0, sub))
                img = novo
            img.save(os.path.join(pasta, f"{i:04d}.png"), compress_level=1)
    return os.path.join(pasta, "%04d.png"), n


if __name__ == "__main__":
    fd, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    F = Fontes(fd)
    exemplos = [("crescimento", {}), ("pilares", {}), ("passos", {}), ("plano", {}), ("relogio", {})]
    tiras = []
    for tipo, p in exemplos:
        img, _ = TIPOS[tipo](2.6, 3.4, p, F)
        fundo = Image.new("RGBA", (PW, PH), (60, 60, 60, 255))
        fundo.alpha_composite(img)
        tiras.append(fundo.resize((PW // 2, PH // 2)))
    folha = Image.new("RGB", (PW // 2 * 3, PH // 2 * 2), (60, 60, 60))
    for i, im in enumerate(tiras):
        folha.paste(im.convert("RGB"), ((i % 3) * PW // 2, (i // 3) * PH // 2))
    folha.save(os.path.join(out, "previa_ilustracoes.png"))
    print("ok")
