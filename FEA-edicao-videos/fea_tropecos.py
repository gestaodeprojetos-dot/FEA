"""Linha do tempo literal de um bruto, com suspeitas de erro de fala marcadas."""
import json, sys, re, subprocess
import numpy as np
sp, b = sys.argv[1], sys.argv[2]
ff = open(sp + "/env.sh").read().split("=", 1)[1].strip()
pcm = subprocess.run([ff, "-v", "error", "-i", f"{sp}/brutos/{b}.MOV", "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(float); h = 800
n = len(a) // h; db = 20 * np.log10(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1)) + 1)
sil = np.percentile(db, 5) + 6
ws = sorted([w for s in json.load(open(f"{sp}/trv/{b}.json")) for w in s["words"]], key=lambda w: w["s"])
norm = lambda w: re.sub(r"[^\w]", "", w.lower())
out = []
for i, w in enumerate(ws):
    marca = ""
    t = w["w"].strip()
    if i and norm(t) == norm(ws[i - 1]["w"]) and norm(t) not in ("é",):
        marca += " <REPETE>"
    if i > 1 and norm(t) == norm(ws[i - 2]["w"]) and i + 1 < len(ws) and norm(ws[i + 1]["w"]) == norm(ws[i - 1]["w"]):
        marca += " <REPETE2>"
    if t.endswith("...") or t.endswith("-"):
        marca += " <CORTADA>"
    if w.get("p", 1) < 0.4:
        marca += f" <p{w['p']:.2f}>"
    if i:
        g0, g1 = ws[i - 1]["e"], w["s"]
        if g1 - g0 > 0.35:
            seg = db[int(g0 / 0.05):int(g1 / 0.05)]
            voz = (seg > sil + 4).sum() * 0.05
            out.append(f"\n   [pausa {g1 - g0:.1f}s{' COM VOZ %.1fs' % voz if voz >= 0.25 else ''}] ")
    out.append(f"{t}@{w['s']:.2f}{marca}")
print(" ".join(out))
