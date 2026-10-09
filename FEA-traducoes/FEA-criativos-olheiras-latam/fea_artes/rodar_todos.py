#!/usr/bin/env python3
"""Roda todos os scripts de criativo (fea_artes/criativos/*.py). Usar depois de mudar precos.json."""
import glob, os, subprocess, sys
aqui = os.path.dirname(os.path.abspath(__file__))
falhas = []
for s in sorted(glob.glob(os.path.join(aqui, 'criativos', '*.py'))):
    r = subprocess.run([sys.executable, s], cwd=aqui, capture_output=True, text=True)
    print(('ok   ' if r.returncode == 0 else 'ERRO ') + os.path.basename(s))
    if r.returncode:
        falhas.append(s); print(r.stderr[-800:])
subprocess.run([sys.executable, os.path.join(aqui, "fea_mockup_capa_es.py")], cwd=aqui)
subprocess.run([sys.executable, os.path.join(aqui, "fea_mockup_livro_branco.py")], cwd=aqui)
subprocess.run([sys.executable, os.path.join(aqui, "fea_mockup_lombada_es.py")], cwd=aqui)
sys.exit(1 if falhas else 0)
