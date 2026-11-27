"""Renderiza os slides animados da Elite Mentoring e corta um MP4 por clique.

Uso: python3 fea_render_slides.py SAIDA 02 03 10 ...
Para cada slide: renderiza o vídeo inteiro a 60 fps, corta um clipe por passo
(STEPS do HTML), um clipe de loop quando houver (LOOP) e salva o último quadro em PNG.
"""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
FPS = 60
os.makedirs(OUT, exist_ok=True)

META_JS = """
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(process.argv[1]);
  console.log(JSON.stringify(await p.evaluate(() => ({ steps: window.STEPS, loop: window.LOOP }))));
  await b.close();
})();
"""


def enc(src, out, a, b):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ss', f'{a:.4f}', '-to', f'{b:.4f}', '-an',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', out], check=True)


for s in sys.argv[2:]:
    url = f'file://{DIR}/FEA-elite-slides.html?s={s}'
    meta = json.loads(subprocess.run(['node', '-e', META_JS, url], capture_output=True, text=True, check=True).stdout)
    full = f'{DIR}/full-{s}.mp4'
    env = dict(os.environ, HTML=f'FEA-elite-slides.html?s={s}')
    subprocess.run(['node', f'{DIR}/render_par.js', str(FPS), full, '4'], env=env, check=True, capture_output=True)
    steps = meta['steps']
    prev = 0.0
    for i, t in enumerate(steps, 1):
        name = f'FEA-elite-slide-{s}.mp4' if len(steps) == 1 else f'FEA-elite-slide-{s}-clique-{i}.mp4'
        enc(full, f'{OUT}/{name}', prev, t)
        prev = t
    if meta['loop']:
        a, b = meta['loop']
        enc(full, f'{OUT}/FEA-elite-slide-{s}-loop.mp4', a, b)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.05', '-i', full, '-frames:v', '1', '-update', '1',
                    f'{OUT}/FEA-elite-slide-{s}-final.png'], check=True)
    print(s, 'ok', len(steps), 'clique(s)', 'loop' if meta['loop'] else '', flush=True)
