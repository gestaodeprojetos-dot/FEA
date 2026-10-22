#!/usr/bin/env python3
"""Audita os criativos copiados do MTB 08/26 para achar data do evento gravada (11/08, agosto, terça).

Imagem: entra numa prancha (mosaico com o nome) para revisão visual.
Vídeo: baixa, transcreve o áudio (Whisper small) e monta uma prancha com 1 quadro a cada 2 s.
Uso: python3 fea_auditar_criativos.py mapa.json PASTA_SAIDA
"""
import json, os, re, subprocess, sys, unicodedata
from PIL import Image, ImageDraw, ImageOps
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, baixar_arquivo

mapa, saida = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(saida, exist_ok=True)
IMG = ("image/png", "image/jpeg")
VID = ("video/mp4", "video/quicktime")
itens = [v for v in mapa.values() if v["mime"] in IMG + VID and ("TRÁFEGO" in unicodedata.normalize("NFC", v["caminho"])
         or "WHATSAPP" in v["caminho"] or "INGRESSO" in v["caminho"])]
tk, _ = token()


def prancha(arquivos, rotulos, destino, cols=4, lado=360):
    linhas = (len(arquivos) + cols - 1) // cols
    folha = Image.new("RGB", (cols * lado, linhas * (lado + 28)), "white")
    d = ImageDraw.Draw(folha)
    for i, (a, r) in enumerate(zip(arquivos, rotulos)):
        im = ImageOps.contain(Image.open(a).convert("RGB"), (lado, lado))
        x, y = (i % cols) * lado, (i // cols) * (lado + 28)
        folha.paste(im, (x, y + 28)); d.text((x + 4, y + 6), r[:52], fill="black")
    folha.save(destino, quality=80)


# imagens: pranchas de 12
imgs = [v for v in itens if v["mime"] in IMG]
locais = []
for v in imgs:
    p = os.path.join(saida, "img_" + v["id"] + ".img")
    if not os.path.exists(p): baixar_arquivo(tk, v["id"], p)
    locais.append((p, v["caminho"].split("/")[-1]))
for n in range(0, len(locais), 12):
    lote = locais[n:n + 12]
    prancha([a for a, _ in lote], [r for _, r in lote], os.path.join(saida, f"prancha_img_{n // 12:02d}.jpg"))
print("pranchas de imagem:", (len(locais) + 11) // 12, flush=True)

# vídeos
from faster_whisper import WhisperModel
modelo = WhisperModel("small", device="cpu", compute_type="int8",
                      download_root="/tmp/claude-0/-home-user-FEA/ce2ef478-67a4-5284-b1d6-9d4c8f98649b/scratchpad/models")
resumo = {}
for v in [v for v in itens if v["mime"] in VID]:
    nome = v["caminho"].split("/")[-1]
    vid = os.path.join(saida, v["id"] + ".video")
    if os.path.exists(os.path.join(saida, v["id"] + ".json")): continue
    baixar_arquivo(tk, v["id"], vid)
    wav = vid + ".wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-ac", "1", "-ar", "16000", wav], check=True)
    segs, _ = modelo.transcribe(wav, language="pt", vad_filter=True)
    texto = " ".join(s.text.strip() for s in segs)
    qdir = vid + "_q"; os.makedirs(qdir, exist_ok=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vid, "-vf", "fps=1/2,scale=360:-2", f"{qdir}/%03d.jpg"], check=True)
    quadros = sorted(os.listdir(qdir))
    prancha([os.path.join(qdir, q) for q in quadros], [f"{nome} {i*2}s" for i in range(len(quadros))],
            os.path.join(saida, f"prancha_vid_{v['id']}.jpg"), cols=6, lado=240)
    data = bool(re.search(r"agosto|onze de|\b11\b|terça", texto, re.I))
    resumo[v["id"]] = {"nome": nome, "caminho": v["caminho"], "texto": texto, "fala_data": data}
    json.dump(resumo[v["id"]], open(os.path.join(saida, v["id"] + ".json"), "w"), ensure_ascii=False)
    for f in (vid, wav): os.remove(f)
    subprocess.run(["rm", "-rf", qdir])
    print("VIDEO", "DATA!" if data else "ok   ", nome, flush=True)
print("FIM")
