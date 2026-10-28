"""FEA: troca o dia na linha "20 DE OUTUBRO" do CTA da Black Friday Vitalícia (ex.: 20 -> 19 para alunos).
Quadro a quadro: acha a primeira palavra da linha (o número, inclusive durante a animação de digitação),
apaga com inpaint e desenha o novo número com Inter Bold na mesma altura, alinhado pela direita.
Uso: python3 fea_cta_data.py CTA.mp4 SAIDA.mp4 NOVO_DIA FONTE_INTER.ttf"""
import subprocess, sys, tempfile, glob, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ent, sai, novo, fonte = sys.argv[1:5]
X0, X1 = 60, 1020
# a linha da data sobe devagar durante o CTA (y de 1636 a 1709): procurar a cada quadro
# o grupo de linhas brancas com 30 a 46 px de altura entre y 1600 e 1720
tmp = tempfile.mkdtemp()
subprocess.run(['ffmpeg', '-v', 'error', '-i', ent, f'{tmp}/f_%05d.png'], check=True)
fps = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
                               '-of', 'csv=p=0', ent]).decode().strip()

def fonte_alt(h):
    f = ImageFont.truetype(fonte, 10); f.set_variation_by_name('Bold')
    for sz in range(20, 140):
        f = ImageFont.truetype(fonte, sz); f.set_variation_by_name('Bold')
        bb = f.getbbox('0')
        if bb[3] - bb[1] >= h: return f
    return f

trocados = 0
for p in sorted(glob.glob(f'{tmp}/f_*.png')):
    im = cv2.imread(p); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    linhas_b = np.where((g[1600:1730, X0:X1] > 190).sum(1) > 2)[0]
    grp = []; ini = ant = None
    for r in linhas_b:
        if ant is None or r > ant + 3:
            if ini is not None: grp.append((ini, ant))
            ini = r
        ant = r
    if ini is not None: grp.append((ini, ant))
    grp = [(a + 1600, b + 1600) for a, b in grp if 30 <= b - a <= 46]
    if not grp: continue
    Y0, Y1 = grp[0][0] - 3, grp[0][1] + 4
    band = g[Y0:Y1, X0:X1] > 190
    cols = np.where(band.sum(0) > 1)[0]
    if len(cols) == 0: continue
    # agrupa colunas em glifos e palavras (espaço = buraco >= 12 px)
    grupos = []; ini = cols[0]; ant = cols[0]
    for c in cols[1:]:
        if c - ant > 1: grupos.append((ini, ant)); ini = c
        ant = c
    grupos.append((ini, ant))
    palavra = [grupos[0]]
    for a, b in grupos[1:]:
        if a - palavra[-1][1] >= 12: break
        palavra.append((a, b))
    xa, xb = palavra[0][0] + X0, palavra[-1][1] + X0
    linhas = np.where(band[:, palavra[0][0]:palavra[-1][1] + 1].sum(1) > 0)[0]
    ya, yb = linhas.min() + Y0, linhas.max() + Y0
    if not (2 <= xb - xa <= 90 and yb - ya >= 20): continue      # não é o número (ainda vazio ou outra coisa)
    n_glifos = len(palavra)
    texto = novo[:n_glifos] if n_glifos < len(novo) else novo
    # brilho do texto original (acompanha o fade da animação)
    brilho = int(np.percentile(g[ya:yb + 1, xa:xb + 1], 97))
    mask = np.zeros(g.shape, np.uint8)
    mask[ya - 4:yb + 5, xa - 4:xb + 5] = 255
    lim = (g > 90).astype(np.uint8) * 255
    mask = cv2.bitwise_and(mask, cv2.dilate(lim, np.ones((5, 5), np.uint8)))
    im = cv2.inpaint(im, cv2.dilate(mask, np.ones((3, 3), np.uint8)), 6, cv2.INPAINT_TELEA)
    pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    f = fonte_alt(yb - ya + 1); d = ImageDraw.Draw(pil)
    bb = d.textbbox((0, 0), texto, font=f)
    x = xb - (bb[2] - bb[0]) - bb[0] + 1; y = ya - bb[1]
    d.text((x, y), texto, font=f, fill=(brilho, brilho, brilho))
    pil.save(p); trocados += 1
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', fps, '-i', f'{tmp}/f_%05d.png', '-i', ent, '-map', '0:v', '-map', '1:a',
                '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-shortest', sai], check=True)
print('quadros trocados:', trocados)
