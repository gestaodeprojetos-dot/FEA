#!/usr/bin/env python3
"""FEA: monta anúncio a partir de bruto selfie (legenda palavra a palavra estilo Ads 021,
faixas vermelhas em X na abertura e botão Saiba Mais). Uso: FEA_TRAB=pasta python3 fea_ads_brutos.py ID [--so-ass]

FEA_TRAB (pasta de trabalho) precisa ter: env.sh e fonts/ (fea_preparar_ambiente.sh),
brutos/IMG_<ID>.MOV, tr/IMG_<ID>.json (fea_transcrever.py), cfg.json (ver
FEA-projeto-ads-bfv-virada-lote.json: faixa_ate = segundo do bruto em que a frase de abertura
termina, cortar = trechos do bruto a remover, nome = arquivo de saída) e gfx/ gerado por
fea_ads_graficos.js (tape_<ID>.png, periodos.json, botao.png). Saída em FEA_TRAB/out/.
Padrão aprovado pela Keila em 10/11/2026 (Ads 021 BFV): faixas em X até o fim da frase de urgência."""
import json, re, subprocess, sys, os
S = os.environ.get("FEA_TRAB") or os.path.dirname(os.path.abspath(__file__))
F = open(f"{S}/env.sh").read().split("=",1)[1].strip()
CFG = json.load(open(f"{S}/cfg.json"))
PER = json.load(open(f"{S}/gfx/periodos.json"))

TROCA = {"pra":"para","pro":"para o","vitalice":"Vitalícia","vitalícia":"Vitalícia","hormonização":"harmonização",
         "imunização":"harmonização","sabar":"Saiba","injectives":"Injectors","r$2.500":"R$ 2.500"}
def palavras(vid):
    d = json.load(open(f"{S}/tr/IMG_{vid}.json"))
    ws = sorted([w for s in d for w in s["words"]], key=lambda w: w["s"])
    out = []
    for w in ws:
        t = w["w"].strip(); fim_frase = bool(re.search(r"[.?!,]$", t))
        nu = re.sub(r"[.,?!]", "", t)
        if nu.lower() in ("ó",): continue
        if nu.lower() == "cebamais":
            m = (w["s"]+w["e"])/2
            out += [dict(s=w["s"], e=m, t="Saiba", p=False), dict(s=m, e=w["e"], t="Mais", p=fim_frase)]; continue
        nu = TROCA.get(nu.lower(), nu)
        out.append(dict(s=w["s"], e=w["e"], t=nu, p=fim_frase))
    return out

def mapa(segs):
    def f(t):
        acc = 0
        for a, b in segs:
            if a <= t <= b: return acc + t - a
            acc += b - a
        return None
    return f

def ts(t):
    h = int(t//3600); m = int(t%3600//60); s = t%60
    return f"{h}:{m:02d}:{s:05.2f}"

def gera_ass(vid, segs, ws):
    f = mapa(segs); W = []
    for w in ws:
        a, b = f(w["s"]), f(w["e"])
        if a is None or b is None: continue
        W.append(dict(w, s=a, e=b))
    # blocos: até 3 palavras e 18 caracteres, quebra em pontuação ou pausa
    blocos, cur = [], []
    for i, w in enumerate(W):
        txt = " ".join(x["t"] for x in cur + [w])
        if cur and (len(cur) >= 3 or len(txt) > 18 or w["s"] - cur[-1]["e"] > 0.35):
            blocos.append(cur); cur = []
        cur.append(w)
        if w["p"]: blocos.append(cur); cur = []
    if cur: blocos.append(cur)
    GOLD = r"{\c&H4FCDF2&}"; WHITE = r"{\c&HFFFFFF&}"
    ev = []
    for k, bl in enumerate(blocos):
        fim_bloco = min(blocos[k+1][0]["s"], bl[-1]["e"] + 0.6) if k+1 < len(blocos) else bl[-1]["e"] + 0.6
        for j, w in enumerate(bl):
            a = w["s"] if j else min(w["s"], bl[0]["s"])
            b = bl[j+1]["s"] if j+1 < len(bl) else fim_bloco
            if b - a < 0.04: continue
            txt = " ".join((GOLD + x["t"].upper() + WHITE) if x is w else x["t"].upper() for x in bl)
            pop = r"{\fscx108\fscy108\t(0,90,\fscx100\fscy100)}" if j == 0 else ""
            ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},Leg,,0,0,0,,{pop}{txt}")
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,Montserrat ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,4.5,3,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [e.replace(",Leg,,0,0,0,,", r",Leg,,0,0,0,,{\pos(540,1330)}", 1) for e in ev]
    return head + "\n".join(ev) + "\n", W

def main():
    vid = sys.argv[1]; c = CFG[vid]
    ws = palavras(vid)
    ini = max(0, ws[0]["s"] - 0.25); fim = ws[-1]["e"] + 0.5
    segs, a = [], ini
    for x, y in c.get("cortar", []):
        segs.append((a, x)); a = y
    segs.append((a, fim))
    ass, W = gera_ass(vid, segs, ws)
    os.makedirs(f"{S}/out", exist_ok=True)
    open(f"{S}/out/{vid}.ass", "w").write(ass)
    if "--so-ass" in sys.argv: print(ass); return
    f = mapa(segs)
    bend = f(c["faixa_ate"]) + 0.15
    # botões: cada "Saiba Mais" fora da janela das faixas
    bot = []
    for i in range(len(W)-1):
        if W[i]["t"].lower() == "saiba" and W[i+1]["t"].lower().startswith("mais") and W[i]["s"] > bend + 0.3:
            if not bot or W[i]["s"] - bot[-1] > 2.5: bot.append(W[i]["s"])
    P = PER[vid]; A = 0.30; CY = 1580
    flt = []
    # corte
    parts = "".join(f"[0:v]trim={x}:{y},setpts=PTS-STARTPTS[v{k}];[0:a]atrim={x}:{y},asetpts=PTS-STARTPTS[a{k}];" for k, (x, y) in enumerate(segs))
    parts += "".join(f"[v{k}][a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[vc][ac];"
    flt.append(parts)
    flt.append(f"[1:v]format=rgba,split=2[s1][s2];"
               f"[s1]crop=1800:150:'mod(t*170,{P})':0,rotate=-{A}:ow=rotw(-{A}):oh=roth(-{A}):c=none,fade=out:st={bend-0.2:.2f}:d=0.2:alpha=1[t1];"
               f"[s2]crop=1800:150:'{P}-mod(t*170,{P})':0,rotate={A}:ow=rotw({A}):oh=roth({A}):c=none,fade=out:st={bend-0.2:.2f}:d=0.2:alpha=1[t2];"
               f"[vc]scale=1080:1920,setsar=1,ass={S}/out/{vid}.ass:fontsdir={S}/fonts[vs];"
               f"[vs][t1]overlay=540-w/2:{CY}-h/2:eof_action=pass[x1];[x1][t2]overlay=540-w/2:{CY}-h/2:eof_action=pass[x2]")
    last = "x2"
    for k, t0 in enumerate(bot):
        flt.append(f";[2:v]scale=420:-1,format=rgba,fade=in:st=0:d=0.15:alpha=1,fade=out:st=1.85:d=0.15:alpha=1,setpts=PTS+{t0:.2f}/TB[b{k}];[{last}][b{k}]overlay=(W-w)/2:1420:eof_action=pass[y{k}]")
        last = f"y{k}"
    cmd = [F, "-v", "error", "-y", "-i", f"{S}/brutos/IMG_{vid}.MOV",
           "-loop", "1", "-framerate", "30", "-t", f"{bend:.2f}", "-i", f"{S}/gfx/tape_{vid}.png",
           "-loop", "1", "-framerate", "30", "-t", "2", "-i", f"{S}/gfx/botao.png",
           "-filter_complex", "".join(flt), "-map", f"[{last}]", "-map", "[ac]", "-r", "30",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{S}/out/{c['nome']}.mp4"]
    subprocess.run(cmd, check=True)
    print(vid, "ok", f"faixas ate {bend:.2f}s", "botoes", [round(b,2) for b in bot], "dur", round(sum(y-x for x,y in segs),2))
main()
