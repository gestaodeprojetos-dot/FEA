"""Mixa efeitos sonoros (ex.: baixados da biblioteca do HeyGen) nos momentos certos da animação.

Uso: python3 fea_som_mix.py cues.json saida.wav

cues.json:
{
  "duracao": 12.0,
  "lufs": -21,
  "cues": [
    {"arquivo": "whoosh.mp3", "momento": 1.41, "pico": 0.34, "db": -11, "pan": 0, "passa_baixa": 6500},
    {"arquivo": "chime.mp3",  "momento": 7.35, "pico": 1.77, "db": -5}
  ]
}
"momento" é quando o pico do som deve cair (ex.: o instante do encaixe); "pico" é o peak_offset do efeito.
"""
import json
import subprocess
import sys

cfg = json.load(open(sys.argv[1]))
out = sys.argv[2]
dur = float(cfg['duracao'])
inputs, chains, labels = [], [], []
for k, c in enumerate(cfg['cues']):
    inputs += ['-i', c['arquivo']]
    start_ms = max(0, int(round((c['momento'] - c.get('pico', 0)) * 1000)))
    pan = float(c.get('pan', 0))
    l, r = (1 - max(0, pan)) * 1.0, (1 + min(0, pan)) * 1.0
    f = []
    if c.get('passa_baixa'):
        f.append(f"lowpass=f={c['passa_baixa']}")
    f.append(f"volume={c.get('db', 0)}dB")
    f.append(f"aformat=channel_layouts=stereo,pan=stereo|c0={l:.2f}*c0|c1={r:.2f}*c1")
    f.append(f"adelay={start_ms}|{start_ms}")
    chains.append(f"[{k}]{','.join(f)}[s{k}]")
    labels.append(f"[s{k}]")
n = len(labels)
chains.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{dur}[z]")
chains.append(f"[z]{''.join(labels)}amix=inputs={n + 1}:normalize=0:duration=first,"
              f"afade=t=out:st={dur - 1}:d=1,loudnorm=I={cfg.get('lufs', -21)}:TP=-2:LRA=11[o]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(chains), '-map', '[o]', '-ar', '48000', out], check=True)
print('ok', out)
