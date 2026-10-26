"""Corte dinâmico: remove os silêncios do vídeo dublado (respiros entre frases), mantendo o fps original.
Uso: fea_dinamico.py entrada.mp4 palavras.json saida.mp4 palavras_saida.json
Mede o silêncio no áudio (janelas de 10 ms), corta pausas > 0,12 s deixando 0,05 s de folga de cada lado,
e remapeia os tempos das palavras para o vídeo cortado."""
import json, subprocess, sys, wave, os
import numpy as np

src, wj, dst, wout = sys.argv[1:5]
PAD, MINGAP = 0.05, 0.12
tmp = dst + ".wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", tmp], check=True, stdin=subprocess.DEVNULL)
a = np.frombuffer(wave.open(tmp).readframes(10 ** 9), dtype=np.int16).astype(float); os.remove(tmp)
rms = np.array([np.sqrt((a[k:k + 160] ** 2).mean()) for k in range(0, len(a) - 160, 160)])
db = 20 * np.log10(rms + 1e-9)
voiced = db > max(np.percentile(db, 90) - 24, 25)  # limiar relativo ao volume da fala
# preenche microburacos (< 80 ms) dentro das palavras
v = voiced.copy()
k = 0
while k < len(v):
    if not v[k]:
        j = k
        while j < len(v) and not v[j]: j += 1
        if j - k < 8 and k > 0 and j < len(v): v[k:j] = True
        k = j
    else: k += 1
dur = len(v) / 100
keep, k = [], 0
segs = []
while k < len(v):
    if v[k]:
        j = k
        while j < len(v) and v[j]: j += 1
        segs.append([k / 100, j / 100]); k = j
    else: k += 1
for s0, s1 in segs:
    s0, s1 = max(0, s0 - PAD), min(dur, s1 + PAD)
    if keep and s0 - keep[-1][1] < MINGAP: keep[-1][1] = s1
    else: keep.append([s0, s1])
keep = [[round(x, 3), round(y, 3)] for x, y in keep if y - x > 0.12]
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "json", src],
                               capture_output=True, text=True).stdout)
fps = pr["streams"][0]["r_frame_rate"]
args, fc, cat = ["ffmpeg", "-v", "error", "-y"], [], ""
for n, (x, y) in enumerate(keep):
    args += ["-ss", f"{x:.3f}", "-t", f"{y - x:.3f}", "-i", src]
    fc.append(f"[{n}:v]fps={fps},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[v{n}]")
    fc.append(f"[{n}:a]aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={max(0, y - x - 0.01):.3f}:d=0.01[a{n}]")
    cat += f"[v{n}][a{n}]"
fc.append(f"{cat}concat=n={len(keep)}:v=1:a=1[v][a]")
subprocess.run(args + ["-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst], check=True, stdin=subprocess.DEVNULL)


def remap(t):
    off = 0.0
    for x, y in keep:
        if t < x: return off
        if t <= y: return off + t - x
        off += y - x
    return off


words = json.load(open(wj))
json.dump([[round(remap(a0), 3), round(max(remap(a0) + 0.05, remap(a1)), 3), w] for a0, a1, w in words], open(wout, "w"), ensure_ascii=False)
tot = sum(y - x for x, y in keep)
print(f"{os.path.basename(src)}: {dur:.1f}s -> {tot:.1f}s ({len(keep)} trechos)")
