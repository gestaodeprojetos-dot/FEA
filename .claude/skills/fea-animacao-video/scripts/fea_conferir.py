"""Conferências antes de entregar um vídeo.

  python3 fea_conferir.py folha video.mp4 folha.jpg [t1,t2,...]      folha de contato com quadros-chave
  python3 fea_conferir.py emenda video.mp4 inicio.png fim.png         1º quadro = slide anterior? último = slide final?
  python3 fea_conferir.py som audio_ou_video                          volume a cada 0,1 s e lista de picos
"""
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def frame(video, t=None, last=False):
    f = tempfile.mktemp(suffix='.png')
    args = ['-sseof', '-0.05'] if last else (['-ss', str(t)] if t is not None else [])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-i', video, '-frames:v', '1', '-update', '1', f], check=True)
    return Image.open(f).convert('RGB')


def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))


cmd = sys.argv[1]
if cmd == 'folha':
    video, out = sys.argv[2], sys.argv[3]
    ts = [float(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else list(np.linspace(0.2, duration(video) - .1, 8))
    cols = 4; rows = (len(ts) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 480, rows * 270))
    for k, t in enumerate(ts):
        im = frame(video, t); im.thumbnail((480, 270)); sheet.paste(im, ((k % cols) * 480, (k // cols) * 270))
    sheet.save(out); print('ok', out)
elif cmd == 'emenda':
    video, ini, fim = sys.argv[2:5]
    for nome, im, ref in (('início', frame(video), ini), ('fim', frame(video, last=True), fim)):
        a = np.asarray(im, float); b = np.asarray(Image.open(ref).convert('RGB').resize(im.size), float)
        e = np.abs(a - b).mean()
        print(f'{nome}: diferença média {e:.1f}', 'OK' if e < 4 else 'DIVERGE (vai dar pulo no clique)')
elif cmd == 'som':
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[2], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; w = 1600
    v = [20 * np.log10(np.sqrt((x[i:i + w] ** 2).mean()) + 1e-9) for i in range(0, len(x) - w, w)]
    print('pico geral:', round(20 * np.log10(np.abs(x).max() + 1e-9), 1), 'dB')
    print('picos (s):', [round(i * .1, 1) for i in range(1, len(v) - 1) if v[i] > -32 and v[i] >= v[i - 1] and v[i] >= v[i + 1]])
