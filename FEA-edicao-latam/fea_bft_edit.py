"""FEA Black Friday Total LATAM: edição no estilo dos criativos do Elite Injectors Congress.

Camadas (todas geradas aqui, quadro a quadro, e sobrepostas ao vídeo dublado):
  legenda   caixa alta, 2 a 4 palavras, branca com contorno escuro e 1 palavra em dourado
  cards     card escuro no topo com a logo, rótulo dourado e título branco (entra deslizando)
  inserts   telas cheias de 1,5 a 3 s (logo, arte Combo Total, número grande, checklist, data do en vivo)
  cta       botão dourado "MÁS INFORMACIÓN" com seta pulsando
  cartela   a cartela final padrão (logo + "Toca en Más información" digitado) é concatenada no fim

Uso: python3 fea_bft_edit.py spec.json
spec = {"video","out","words":[[t0,t1,palavra],...],"chunks"(opcional),"cards":[...],"inserts":[...],"cta":[...],"endcard"}
"""
import json, math, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
W, H = 1080, 1920
GOLD, GOLD_HI, DARK, WHITE = (222, 176, 98), (246, 214, 150), (12, 10, 8), (255, 255, 255)
F = {w: os.path.join(ASSETS, f"Montserrat-{w}.ttf") for w in (700, 800, 900)}
_fc = {}


def font(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(F[w], s)
    return _fc[k]


def ease(x):
    x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3


def env(t, t0, t1, fi=0.3, fo=0.25):
    """0..1 de entrada/saída de um elemento."""
    if t < t0 or t > t1: return 0.0
    return min(ease((t - t0) / fi), ease((t1 - t) / fo) if fo else 1.0)


def logo(w):
    lg = Image.open(os.path.join(ASSETS, "FEA-black-friday-total-logo.png")).convert("RGBA")
    return lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)


LOGO_S, LOGO_M, LOGO_L = logo(150), logo(520), logo(820)


def fade(im, a):
    if a >= 0.999: return im
    im = im.copy(); al = im.split()[3].point(lambda v: int(v * a)); im.putalpha(al); return im


# ---------------------------------------------------------------- legenda
STOP = set("de la el los las en y a al tu mi su con para que un una por del se lo no es o te me mis tus todo todos toda todas este esta esto aquí allá haz".split())
KEY = re.compile(r"^(BLACK|FRIDAY|TOTAL|COMBO|ESPAÑOL|\d+%?|MESES|AÑO|CLASES|TOXINA|RELLENO|BIOESTIMULADORES|BONOS|VIVO|APERTURA|NOVIEMBRE|PRECIO|INFORMACIÓN|FORMACIONES|EXCLUSIVOS)$")


CAP_SIZE = 62  # tamanho único em todas as legendas (Keila, 26/10: nada de letra maior que a outra)


def caption_img(text):
    words = text.upper().split()
    keys = [i for i, w in enumerate(words) if KEY.match(w.strip(",.:;!?¡¿"))]
    if not keys:
        cand = [i for i, w in enumerate(words) if w.lower().strip(",.:;!?¡¿") not in STOP]
        keys = [max(cand, key=lambda i: len(words[i]))] if cand else []
    hl = set(keys[:2])
    size = CAP_SIZE
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    f = font(900, size)
    lines, cur = [], []
    for i, w in enumerate(words):
        t = " ".join(words[j] for j in cur + [i])
        if cur and d.textlength(t, font=f) > 960: lines.append(cur); cur = [i]
        else: cur.append(i)
    if cur: lines.append(cur)
    lh = int(size * 1.08)
    im = Image.new("RGBA", (W, lh * len(lines) + 60), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh); dr = ImageDraw.Draw(im)
    for li, ln in enumerate(lines):
        y = 30 + li * lh
        tw = d.textlength(" ".join(words[j] for j in ln), font=f); x = (W - tw) / 2
        for j in ln:
            w = words[j]
            ds.text((x + 4, y + 6), w, font=f, fill=(0, 0, 0, 170))
            dr.text((x, y), w, font=f, fill=(GOLD_HI if j in hl else WHITE) + (255,), stroke_width=7, stroke_fill=(10, 8, 6, 235))
            x += d.textlength(w + " ", font=f)
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    sh.alpha_composite(im)
    return sh


FIXES = [(r"(?i)cien por ciento", "100%"), (r"(\d+) %", r"\1%"), (r"(?i)\bpit[oó]n\b", "Pithon"), (r"(?i)más\s+información", "Más información")]


def chunks_from_words(words, end):
    WEAK = STOP | {"un", "y", "en", "de", "nuestra", "nuestro", "más", "esta", "este", "las", "los", "black", "combo", "por", "con"}
    res, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        lw = w[2].lower().strip(",.:;!?¡¿")
        punct = w[2][-1:] in ".,:;!?"
        gap = nxt is not None and nxt[0] - w[1] > 0.45
        nl = nxt[2].lower().strip(",.:;!?") if nxt else ""
        glue = nxt is not None and ((lw == "más" and nl.startswith("informaci")) or (lw == "friday" and nl in ("total", "combo")) or (lw == "total" and nl == "combo") or (lw == "combo" and nl == "total") or (lw.isdigit() and nl in ("ml", "clases", "meses", "%", "de", "por")))
        weak = lw in WEAK
        if not glue and (punct or gap or len(cur) >= 6 or (len(cur) >= 3 and not weak and (cur[-1][1] - cur[0][0]) > 0.7)):
            res.append(cur); cur = []
    if cur: res.append(cur)
    out = []
    for k, c in enumerate(res):
        t0 = c[0][0]; t1 = res[k + 1][0][0] if k + 1 < len(res) else min(end, c[-1][1] + 0.6)
        t1 = min(t1, c[-1][1] + 0.7)
        txt = " ".join(w[2] for w in c).strip(" ,;:").rstrip(".")
        for a_, b_ in FIXES: txt = re.sub(a_, b_, txt)
        out.append([round(t0, 3), round(t1, 3), txt])
    return out


# ---------------------------------------------------------------- card do topo
def card_img(label, title):
    f1, f2 = font(800, 32), font(900, 60)
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    lines, cur = [], ""
    for w in title.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f2) <= 680: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    hgt = 70 + 40 + len(lines) * 68
    cw = 960
    im = Image.new("RGBA", (cw + 40, hgt + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 26, cw + 20, hgt + 26], 30, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); im.alpha_composite(sh)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([20, 20, cw + 20, hgt + 20], 30, fill=(16, 13, 10, 238), outline=GOLD + (190,), width=3)
    lg = LOGO_S.resize((170, int(LOGO_S.height * 170 / LOGO_S.width)), Image.LANCZOS)
    im.alpha_composite(lg, (52, 20 + (hgt - lg.height) // 2))
    tx = 52 + 170 + 36
    dr.line([(tx - 18, 50), (tx - 18, hgt - 10)], fill=GOLD + (120,), width=2)
    y = 20 + (hgt - (44 + len(lines) * 68)) // 2
    dr.text((tx, y), label.upper(), font=f1, fill=GOLD + (255,))
    y += 44
    for ln in lines:
        dr.text((tx, y), ln, font=f2, fill=WHITE + (255,)); y += 68
    return im


# ---------------------------------------------------------------- telas cheias
_bg = None


def bg_dark(t):
    global _bg
    if _bg is None:
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.55)) ** 2).clip(0, 1)
        c0, c1 = np.array([58, 44, 20]), np.array([6, 5, 4])
        rgb = (c0 * (1 - r[..., None]) + c1 * r[..., None]).astype("uint8")
        _bg = Image.fromarray(np.dstack([rgb, np.full((H, W), 255, "uint8")]), "RGBA")
    return _bg.copy()


_art = {}


def art(name):
    if name not in _art: _art[name] = Image.open(os.path.join(ASSETS, name)).convert("RGBA")
    return _art[name]


def insert_frame(ins, t):
    k, t0, t1 = ins["kind"], ins["t0"], ins["t1"]
    p = (t - t0) / max(0.01, t1 - t0)
    im = bg_dark(t)
    d = ImageDraw.Draw(im)
    if k == "combo":  # arte oficial Combo Total com o Dr. (zoom lento)
        a = art("combo_com.jpg"); s = 1.0 + 0.05 * p
        side = int(1120 * s); a2 = a.resize((side, side), Image.LANCZOS)
        m = Image.new("L", a2.size, 255); md = ImageDraw.Draw(m)
        for k2 in range(90):  # funde as bordas da arte no fundo escuro
            md.rectangle([k2, k2, side - 1 - k2, side - 1 - k2], outline=int(255 * k2 / 90))
        a2.putalpha(m)
        im.alpha_composite(a2, ((W - side) // 2, 150 - int(28 * (s - 1) * 10)))
        lg = LOGO_S.resize((380, int(LOGO_S.height * 380 / LOGO_S.width)))
        im.alpha_composite(fade(lg, ease((t - t0 - 0.2) / 0.4)), ((W - lg.width) // 2, 1300))
    elif k == "logo":
        e = ease((t - t0) / 0.6); L = LOGO_L.resize((int(LOGO_L.width * (1.08 - 0.08 * e)), int(LOGO_L.height * (1.08 - 0.08 * e))), Image.LANCZOS)
        im.alpha_composite(fade(L, e), ((W - L.width) // 2, 700 - L.height // 2))
        if ins.get("tagline"):
            f = font(700, 44); _center_lines(d, ins["tagline"], f, 900, 980, fill=(240, 232, 220, int(255 * ease((t - t0 - 0.3) / 0.4))))
    elif k == "number":
        e = ease((t - t0) / 0.8)
        val = ins["value"]; m = re.match(r"(\D*)(\d+)(.*)", val)
        shown = f"{m.group(1)}{int(int(m.group(2)) * e)}{m.group(3)}" if m else val
        f = font(900, ins.get("size", 230)); tw = d.textlength(shown, font=f)
        _gold_text(im, ((W - tw) / 2, 560), shown, f)
        _center_lines(d, ins["label"].upper(), font(900, 58), 900, 900, fill=WHITE + (int(255 * ease((t - t0 - 0.2) / 0.4)),))
        im.alpha_composite(LOGO_S.resize((240, int(LOGO_S.height * 240 / LOGO_S.width))), ((W - 240) // 2, 230))
    elif k == "checklist":
        many = len(ins["items"]) > 4  # 6 formações: bloco mais compacto, termina acima da faixa da legenda
        ly, ty, y0 = (190, 420, 520) if many else (260, 520, 680)
        im.alpha_composite(LOGO_S.resize((300, int(LOGO_S.height * 300 / LOGO_S.width))), ((W - 300) // 2, ly))
        if ins.get("title"): _center_lines(d, ins["title"].upper(), font(900, 46 if many else 52), 960, ty, fill=WHITE + (255,))
        fs, step, x0, maxw = (44, 104, 90, 760) if many else (56, 130, 150, 640)
        while fs > 30 and max(d.textlength(it, font=font(800, fs)) for it in ins["items"]) > maxw: fs -= 2
        f = font(800, fs); y = y0
        for n, item in enumerate(ins["items"]):
            e = ease((t - t0 - 0.12 - n * (0.16 if many else 0.22)) / 0.3)
            if e <= 0: y += step; continue
            x = x0 + int(60 * (1 - e)); a = int(255 * e); h = step - 34
            d.rounded_rectangle([x - 10, y - 14, W - x0 + 10, y + h], 22, fill=(20, 16, 12, int(220 * e)), outline=GOLD + (int(170 * e),), width=2)
            cy = y + (h - 14) // 2
            d.ellipse([x + 12, cy - 20, x + 52, cy + 20], fill=GOLD + (a,))
            d.line([(x + 22, cy), (x + 30, cy + 9), (x + 44, cy - 9)], fill=DARK + (a,), width=5)
            d.text((x + 74, cy - fs * 0.62), item, font=f, fill=WHITE + (a,)); y += step
    elif k == "date":  # en vivo de apertura
        e = ease((t - t0) / 0.5)
        cx, cy = W // 2, 720
        d.rounded_rectangle([cx - 190, cy - 230 + int(40 * (1 - e)), cx + 190, cy + 190 + int(40 * (1 - e))], 36, fill=(250, 246, 238, int(255 * e)))
        d.rounded_rectangle([cx - 190, cy - 230 + int(40 * (1 - e)), cx + 190, cy - 120 + int(40 * (1 - e))], 36, fill=GOLD + (int(255 * e),))
        d.rectangle([cx - 190, cy - 160 + int(40 * (1 - e)), cx + 190, cy - 120 + int(40 * (1 - e))], fill=GOLD + (int(255 * e),))
        _center_text(d, "NOVIEMBRE", font(900, 44), cy - 205 + int(40 * (1 - e)), fill=DARK + (int(255 * e),))
        _center_text(d, "10", font(900, 210), cy - 120 + int(40 * (1 - e)), fill=DARK + (int(255 * e),))
        _center_text(d, "MARTES", font(800, 36), cy + 125 + int(40 * (1 - e)), fill=(110, 90, 60, int(255 * e)))
        a2 = int(255 * ease((t - t0 - 0.35) / 0.4))
        _center_text(d, "EN VIVO DE APERTURA", font(900, 60), 1000, fill=GOLD_HI + (a2,))
        _center_text(d, "El menor precio del Combo Total", font(700, 40), 1085, fill=(240, 232, 220, a2))
        im.alpha_composite(LOGO_S.resize((240, int(LOGO_S.height * 240 / LOGO_S.width))), ((W - 240) // 2, 230))
    # entrada/saída rápida
    a = min(ease((t - t0) / 0.18), ease((t1 - t) / 0.18))
    return fade(im, a)


def _center_text(d, s, f, y, fill):
    tw = d.textlength(s, font=f); d.text(((W - tw) / 2, y), s, font=f, fill=fill)


def _center_lines(d, s, f, maxw, y, fill):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    for ln in lines:
        _center_text(d, ln, f, y, fill); y += int(f.size * 1.15)


def _gold_text(im, xy, s, f):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).text(xy, s, font=f, fill=255)
    yy = np.linspace(0, 1, im.size[1])[:, None]
    g0, g1 = np.array(GOLD_HI), np.array((176, 128, 52))
    grad = (g0 * (1 - yy[..., None]) + g1 * yy[..., None]).astype("uint8")
    grad = np.broadcast_to(grad, (im.size[1], im.size[0], 3))
    gl = Image.fromarray(np.dstack([grad, np.array(m)]), "RGBA")
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v // 2))
    im.alpha_composite(sh); im.alpha_composite(gl)


# ---------------------------------------------------------------- botão
def cta_img(t, t0):
    f = font(900, 44); txt = "MÁS INFORMACIÓN"
    d = ImageDraw.Draw(Image.new("RGB", (8, 8))); tw = d.textlength(txt, font=f)
    bw, bh = int(tw + 110), 100
    im = Image.new("RGBA", (bw + 40, bh + 140), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 130, bw + 20, 130 + bh], 50, fill=(0, 0, 0, 160))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    dr.rounded_rectangle([20, 120, bw + 20, 120 + bh], 50, fill=GOLD + (255,), outline=GOLD_HI + (255,), width=3)
    dr.text((20 + (bw - tw) / 2, 120 + (bh - 52) / 2), txt, font=f, fill=DARK + (255,))
    bounce = int(14 * abs(math.sin((t - t0) * 5.5)))
    cx = 20 + bw // 2
    dr.polygon([(cx - 26, 40 + bounce), (cx + 26, 40 + bounce), (cx, 92 + bounce)], fill=GOLD_HI + (255,))
    dr.rectangle([cx - 9, 6 + bounce, cx + 9, 44 + bounce], fill=GOLD_HI + (255,))
    s = 0.8 + 0.2 * ease((t - t0) / 0.2)
    if s < 0.999: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im


# ---------------------------------------------------------------- render
def main(spec):
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate:format=duration",
                                    "-of", "json", spec["video"]], capture_output=True, text=True).stdout)
    num, den = map(int, pr["streams"][0]["r_frame_rate"].split("/")); fps = num / den
    dur = float(pr["format"]["duration"]); nfr = int(dur * fps)
    chunks = spec.get("chunks") or chunks_from_words(spec["words"], dur)
    capimgs = [caption_img(c[2]) for c in chunks]
    cards = [(c, card_img(c["label"], c["title"])) for c in spec.get("cards", [])]
    capy = spec.get("caption_y", 1300)
    args = ["ffmpeg", "-v", "error", "-y", "-i", spec["video"], "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-framerate", f"{num}/{den}", "-i", "-"]
    fc = ["[0:v][1:v]overlay=0:0:eof_action=pass:format=auto,format=yuv420p,setsar=1[vm]"]
    if spec.get("endcard"):
        args += ["-i", spec["endcard"]]
        fc += [f"[2:v]fps={num}/{den},format=yuv420p,setsar=1[ve]", "[0:a]aresample=48000,aformat=channel_layouts=stereo[am]",
               "[2:a]aresample=48000,aformat=channel_layouts=stereo[ae]", "[vm][am][ve][ae]concat=n=2:v=1:a=1[v][a]"]
        vmap, amap = "[v]", "[a]"
    else:
        vmap, amap = "[vm]", "0:a"
    args += ["-filter_complex", ";".join(fc), "-map", vmap, "-map", amap, "-c:v", "libx264", "-preset", "fast", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", spec["out"]]
    proc = subprocess.Popen(args, stdin=subprocess.PIPE)
    empty = Image.new("RGBA", (W, H), (0, 0, 0, 0)).tobytes()
    for k in range(nfr):
        t = k / fps
        layers = []
        ins = next((i for i in spec.get("inserts", []) if i["t0"] <= t < i["t1"]), None)
        if ins: layers.append((insert_frame(ins, t), (0, 0)))
        for c, img in cards:
            a = env(t, c["t0"], c["t1"], 0.35, 0.3)
            if a > 0 and not ins:
                dy = int(-50 * (1 - ease((t - c["t0"]) / 0.35)))
                layers.append((fade(img, a), (40 - 20, c.get("y", 70) + dy)))
        for c in spec.get("cta", []):
            if c["t0"] <= t < c["t1"]:
                b = cta_img(t, c["t0"]); layers.append((fade(b, env(t, c["t0"], c["t1"], 0.15, 0.2)), ((W - b.width) // 2, c.get("y", 1470))))
        cy = ins.get("cap_y", 1690 if ins["kind"] == "combo" else capy) if ins else capy
        for (a0, a1, _), img in zip(chunks, capimgs):
            if a0 <= t < a1:
                layers.append((img, ((W - img.width) // 2, cy - img.height // 2)))
                break
        if not layers:
            proc.stdin.write(empty); continue
        can = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for im, (x, y) in layers: can.alpha_composite(im, (int(x), int(y)))
        proc.stdin.write(can.tobytes())
    proc.stdin.close()
    if proc.wait(): raise SystemExit("ffmpeg falhou")
    return chunks


if __name__ == "__main__":
    sp = json.load(open(sys.argv[1])); main(sp)
