"""Corta uma animação em um vídeo por clique (PowerPoint), mais o loop e um PNG final de reserva.

Uso: python3 fea_cortar_cliques.py pagina.html pasta_saida [fps=30] [VW VH]
A página precisa de window.STEPS (fim de cada clique) e, se tiver loop, window.LOOP = [inicio, fim].
Roda o fea_render.js (mesma pasta deste script) a partir da pasta da página.
"""
import json
import os
import subprocess
import sys

html, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
fps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
vw, vh = (sys.argv[4], sys.argv[5]) if len(sys.argv) > 5 else ('1920', '1080')
here = os.path.dirname(os.path.abspath(__file__))
base = os.path.splitext(os.path.basename(html))[0]
os.makedirs(out, exist_ok=True)

meta_js = """
let pw; try { pw = require('playwright'); } catch (e) { pw = require('/opt/node22/lib/node_modules/playwright'); }
(async () => { const b = await pw.chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.goto(process.argv[1]);
console.log(JSON.stringify(await p.evaluate(() => ({ steps: window.STEPS || [window.DURATION], loop: window.LOOP || null }))));
await b.close(); })();
"""
meta = json.loads(subprocess.run(['node', '-e', meta_js, 'file://' + html], capture_output=True, text=True, check=True).stdout)
full = os.path.join(out, f'{base}-completo.mp4')
env = dict(os.environ, HTML=os.path.basename(html), VW=vw, VH=vh, FPS=str(fps))
subprocess.run(['node', os.path.join(here, 'fea_render.js'), 'video', full, '4'], cwd=os.path.dirname(html), env=env, check=True)


def cut(a, b, name):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', full, '-ss', f'{a:.4f}', '-to', f'{b:.4f}', '-an', '-c:v', 'libx264',
                    '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', os.path.join(out, name)], check=True)


steps, prev = meta['steps'], 0.0
for i, t in enumerate(steps, 1):
    cut(prev, t, f'{base}.mp4' if len(steps) == 1 else f'{base}-clique-{i}.mp4'); prev = t
if meta['loop']:
    cut(meta['loop'][0], meta['loop'][1], f'{base}-loop.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.05', '-i', full, '-frames:v', '1', '-update', '1',
                os.path.join(out, f'{base}-final.png')], check=True)
print('ok', len(steps), 'clique(s)', 'com loop' if meta['loop'] else '')
