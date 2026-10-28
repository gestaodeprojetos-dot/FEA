"""Acha, dentro de um intervalo de uma gravação de tela, a janela de N segundos
em que a aula está realmente acontecendo: imagem sempre em movimento (sem travar
ou carregar), sem tela preta/branca e sem corte para menus.

Uso: python3 fea_melhor_trecho.py video.mp4 inicio fim duracao
Saída: melhor_inicio score  (e as 3 melhores janelas)
"""
import subprocess
import sys
import numpy as np

CROP = tuple(int(v) for v in __import__('os').environ.get('CROP', '810,300,28,262').split(','))     # área do player (padrão: gravação da plataforma 1280x720)
W, H, FPS = 216, 80, 15

video, a, b, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
cmd = ['ffmpeg', '-v', 'error', '-ss', str(a), '-i', video, '-t', str(b - a),
       '-vf', f'crop={CROP[0]}:{CROP[1]}:{CROP[2]}:{CROP[3]},scale={W}:{H},fps={FPS},format=gray',
       '-f', 'rawvideo', '-']
raw = subprocess.run(cmd, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
n = len(fr)

# ícone de carregamento fica no centro do player: excluído da medida de movimento
mask = np.ones((H, W), bool)
cy, cx = int(H * .56), int(W * .5)
mask[cy - 14:cy + 14, cx - 14:cx + 14] = False

motion = np.zeros(n)
motion[1:] = np.abs(fr[1:] - fr[:-1])[:, mask].mean(axis=1)
std = fr.reshape(n, -1).std(axis=1)
# variação só no centro com o resto parado = carregando
center = np.zeros(n)
center[1:] = np.abs(fr[1:, cy - 14:cy + 14, cx - 14:cx + 14] - fr[:-1, cy - 14:cy + 14, cx - 14:cx + 14]).mean(axis=(1, 2))

MT = float(__import__('os').environ.get('MT', '.35'))
good = (motion > MT) & (std > 18) & ~((center > 2.5) & (motion < 1.0))
cut = motion > 25          # troca brusca de tela (menu, outra página)

k = int(dur * FPS)
res = []
for s in range(1, n - k):
    w = slice(s, s + k)
    if cut[w].sum() > 1:
        continue
    frac = good[w].mean()
    # ainda rejeita qualquer trecho com 3+ quadros seguidos parados
    run, worst = 0, 0
    for g in good[w]:
        run = 0 if g else run + 1
        worst = max(worst, run)
    if worst >= int(__import__('os').environ.get('WR', '3')):
        continue
    score = frac * 10 + min(np.median(motion[w]), 4)
    res.append((score, a + s / FPS))
res.sort(reverse=True)
if not res:
    print('nenhum')
else:
    print(' '.join(f'{t:.2f}:{sc:.2f}' for sc, t in res[:1]), '|', ' '.join(f'{t:.2f}' for sc, t in res[:8]))
