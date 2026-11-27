#!/usr/bin/env python3
"""Renomeia criativos em vídeo prontos para VID_[MMAA]_[TAG]_[NNN]_[FORMATO].mp4 (Keila, 26/11/2026).

Uso:
  python3 fea_renomear_criativos.py PASTA_CRIATIVOS_PRONTOS MMAA TAG           # só mostra o plano
  python3 fea_renomear_criativos.py PASTA_CRIATIVOS_PRONTOS MMAA TAG --aplicar # renomeia
Ex.: python3 fea_renomear_criativos.py 1V6c3-ZNi-rrMFOIr2gIG81LNfTDRkYey 1226 MBIO --aplicar
Número = o do "Ads N" original (3 dígitos). Repetido em outra fase: a fase posterior (ordem das
subpastas: 1. CAPTAÇÃO, 2. ANTECIPAÇÃO, 3. LEMBRETE...) recebe o próximo número livre.
Formato pelas dimensões: 1080x1920=9x16, 1080x1350=4x5, 1080x1080=1x1, 1920x1080=16x9.
Brutos nunca. O link do Drive não muda.
"""
import json, re, sys, urllib.parse, urllib.request
sys.path.insert(0, '/home/user/FEA/FEA-edicao-videos')
from fea_drive import token
H = {'Authorization': 'Bearer ' + token()[0], 'Content-Type': 'application/json'}
D = 'https://www.googleapis.com/drive/v3/files'


def ls(fid):
    q = urllib.parse.quote(f"'{fid}' in parents and trashed=false")
    return json.load(urllib.request.urlopen(urllib.request.Request(
        f'{D}?q={q}&fields=files(id,name,mimeType,videoMediaMetadata(width,height))&pageSize=1000&orderBy=name'
        '&supportsAllDrives=true&includeItemsFromAllDrives=true', headers=H)))['files']


FMT = {(1080, 1920): '9x16', (1080, 1350): '4x5', (1080, 1080): '1x1', (1920, 1080): '16x9'}
raiz, mmaa, tag = sys.argv[1:4]; aplicar = '--aplicar' in sys.argv
vids = []
def walk(fid, fase=''):
    for f in ls(fid):
        if f['mimeType'].endswith('folder'): walk(f['id'], f['name'])
        elif f['mimeType'].startswith('video'): vids.append((fase, f))
walk(raiz)
usados, plano = set(), []
for fase, f in sorted(vids, key=lambda x: x[0]):
    if f['name'].startswith('VID_'): usados.add(int(f['name'].split('_')[3])); continue
    m = re.search(r'(?i)ads\s*(\d+)', f['name'])
    plano.append([fase, f, int(m.group(1)) if m else None])
for p in plano:
    n = p[2]
    if n is None or n in usados:
        n = max(usados | {x[2] or 0 for x in plano}) + 1
    usados.add(n); p[2] = n
for fase, f, n in plano:
    vm = f.get('videoMediaMetadata', {}); w, h = vm.get('width'), vm.get('height')
    novo = f'VID_{mmaa}_{tag}_{n:03d}_{FMT.get((w, h), f"{w}x{h}")}.mp4'
    print(fase[:16], '|', f['name'], '->', novo)
    if aplicar:
        urllib.request.urlopen(urllib.request.Request(f"{D}/{f['id']}?supportsAllDrives=true",
                               data=json.dumps({'name': novo}).encode(), headers=H, method='PATCH'))
print('APLICADO' if aplicar else 'Só o plano. Rode de novo com --aplicar.')
