#!/usr/bin/env python3
"""Atalhos de Drive e Planilhas Google da FEA (usa o token de FEA-edicao-videos/fea_drive.py).

Uso:
  python3 fea_google.py arvore PASTA_ID [profundidade]        # lista pastas e arquivos com ID
  python3 fea_google.py buscar "name contains 'Links úteis'"   # busca no Drive todo (todos os drives)
  python3 fea_google.py caminho ARQUIVO_ID                     # mostra o caminho de pastas até o arquivo
  python3 fea_google.py copiar ARQUIVO_ID PASTA_DESTINO        # cópia no servidor, confere md5
  python3 fea_google.py xlsx2sheet ARQUIVO_XLSX_ID             # cria a versão Google Planilhas na mesma pasta
  python3 fea_google.py lixeira ARQUIVO_ID                     # manda para a lixeira (nunca apaga de vez)
  python3 fea_google.py planilha PLANILHA_ID [ABA]             # imprime as abas, ou as linhas da aba (com fórmulas)
  python3 fea_google.py doc DOC_ID                             # texto puro de um Google Doc
Regras: busca por nome é por prefixo de palavra ('Links úteis' acha, 'inks' não acha).
Nunca mover planilha da equipe; conferir modifiedTime antes de sobrescrever qualquer coisa.
"""
import json, sys, urllib.parse, urllib.request
sys.path.insert(0, '/home/user/FEA/FEA-edicao-videos')
from fea_drive import token

T = token()[0]
H = {'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json'}
D = 'https://www.googleapis.com/drive/v3/files'
X = '&supportsAllDrives=true&includeItemsFromAllDrives=true'


def req(url, body=None, method=None, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                                      headers=H, method=method))
    return r.read().decode() if raw else json.load(r)


def ls(fid):
    q = urllib.parse.quote(f"'{fid}' in parents and trashed=false")
    out, pt = [], ''
    while True:
        r = req(f'{D}?q={q}&fields=nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime)&pageSize=1000&orderBy=name{X}'
                + (f'&pageToken={pt}' if pt else ''))
        out += r['files']; pt = r.get('nextPageToken')
        if not pt: return out


def arvore(fid, prof=3, d=0):
    for f in ls(fid):
        pasta = f['mimeType'].endswith('folder')
        print('  ' * d + ('📁 ' if pasta else '- ') + f"{f['name']} | {f['id']}")
        if pasta and d < prof: arvore(f['id'], prof, d + 1)


def main(a):
    c = a[0]
    if c == 'arvore': arvore(a[1], int(a[2]) if len(a) > 2 else 3)
    elif c == 'buscar':
        q = urllib.parse.quote(a[1] + ' and trashed=false')
        for f in req(f'{D}?q={q}&fields=files(id,name,mimeType,modifiedTime)&corpora=allDrives&pageSize=100&orderBy=modifiedTime%20desc{X}')['files']:
            print(f['modifiedTime'][:10], '|', f['name'], '|', f['id'])
    elif c == 'caminho':
        m = req(f'{D}/{a[1]}?fields=name,parents&supportsAllDrives=true'); p = [m['name']]
        while m.get('parents'):
            m = req(f"{D}/{m['parents'][0]}?fields=name,parents&supportsAllDrives=true"); p.append(m['name'])
        print(' / '.join(reversed(p)))
    elif c == 'copiar':
        o = req(f'{D}/{a[1]}?fields=name,md5Checksum&supportsAllDrives=true')
        n = req(f'{D}/{a[1]}/copy?supportsAllDrives=true&fields=id,md5Checksum', {'name': o['name'], 'parents': [a[2]]}, 'POST')
        print(n['id'], 'md5 ok' if n.get('md5Checksum') == o.get('md5Checksum') else 'CONFERIR MD5')
    elif c == 'xlsx2sheet':
        o = req(f'{D}/{a[1]}?fields=name,parents&supportsAllDrives=true')
        nome = o['name'].rsplit('.xlsx', 1)[0]
        n = req(f'{D}/{a[1]}/copy?supportsAllDrives=true&fields=id',
                {'name': nome, 'parents': o['parents'], 'mimeType': 'application/vnd.google-apps.spreadsheet'}, 'POST')
        print('Planilha Google:', f"https://docs.google.com/spreadsheets/d/{n['id']}/edit",
              '\nDepois de trocar os links que apontavam para o xlsx, mandar o xlsx para a lixeira.')
    elif c == 'lixeira':
        print(req(f'{D}/{a[1]}?supportsAllDrives=true&fields=name,trashed', {'trashed': True}, 'PATCH'))
    elif c == 'planilha':
        S = f'https://sheets.googleapis.com/v4/spreadsheets/{a[1]}'
        if len(a) < 3:
            for s in req(S + '?fields=sheets.properties(title,sheetId)')['sheets']: print(s['properties'])
        else:
            for i, row in enumerate(req(S + '/values/' + urllib.parse.quote(a[2]) + '?valueRenderOption=FORMULA').get('values', [])):
                if any(str(x).strip() for x in row): print(i + 1, ' | '.join(map(str, row))[:400])
    elif c == 'doc':
        print(req(f'{D}/{a[1]}/export?mimeType=text/plain', raw=True))


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1:])
