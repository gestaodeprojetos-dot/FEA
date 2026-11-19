"""Atalhos do Drive para a operação de lançamentos FEA.

Usa a chave de fea_drive.py (variáveis de ambiente FEA_GDRIVE_*), nunca chave no código.
Importar com:
    import sys; sys.path.insert(0, '/home/user/FEA/.claude/skills/fea-operacao-lancamentos/scripts')
    from fea_gdrive import *
"""
import io, json, re, sys, urllib.parse, uuid
sys.path.insert(0, '/home/user/FEA/FEA-edicao-videos')
from fea_drive import token, chamar

TK = token()[0]
B = 'https://www.googleapis.com/drive/v3/files'
UP = 'https://www.googleapis.com/upload/drive/v3/files'
X = 'supportsAllDrives=true&includeItemsFromAllDrives=true'
DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def meta(i, campos='id,name,parents,mimeType,modifiedTime'):
    return json.load(chamar(TK, 'GET', f"{B}/{i}?fields={campos}&{X}"))


def caminho(i):
    p = []
    while i:
        m = meta(i); p.append(m['name']); i = (m.get('parents') or [None])[0]
    return ' / '.join(reversed(p))


def ls(i):
    q = urllib.parse.quote(f"'{i}' in parents and trashed=false"); out = []; tok = ''
    while True:
        r = json.load(chamar(TK, 'GET', f"{B}?q={q}&fields=nextPageToken,files(id,name,mimeType,modifiedTime,size)&{X}&corpora=allDrives&pageSize=200" + (f"&pageToken={tok}" if tok else '')))
        out += r['files']; tok = r.get('nextPageToken')
        if not tok: return out


def mkdir(nome, pai):
    """Cria a pasta ou devolve a que já existe com o mesmo nome."""
    for f in ls(pai):
        if f['name'] == nome and f['mimeType'].endswith('folder'): return f['id']
    return json.load(chamar(TK, 'POST', f"{B}?{X}&fields=id", {'name': nome, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [pai]}))['id']


def baixar(i):
    return chamar(TK, 'GET', f"{B}/{i}?alt=media&{X}").read()


def exportar(i, mime='text/plain'):
    return chamar(TK, 'GET', f"{B}/{i}/export?mimeType={mime}&{X}").read()


def substituir_conteudo(i, dados, mime):
    """Troca o conteúdo mantendo o mesmo ID (vale para .xlsx e para Google Doc via .docx)."""
    return json.load(chamar(TK, 'PATCH', f"{UP}/{i}?uploadType=media&{X}&fields=id,modifiedTime", cabecalhos={'Content-Type': mime}, bruto=dados))


def subir_arquivo(nome, pai, dados, mime):
    bd = uuid.uuid4().hex; m = json.dumps({'name': nome, 'parents': [pai]})
    corpo = (f'--{bd}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{m}\r\n--{bd}\r\nContent-Type: {mime}\r\n\r\n').encode() + dados + f'\r\n--{bd}--'.encode()
    return json.load(chamar(TK, 'POST', f"{UP}?uploadType=multipart&{X}&fields=id,name", cabecalhos={'Content-Type': f'multipart/related; boundary={bd}'}, bruto=corpo))


def editar_xlsx(i, funcao):
    """Baixa o .xlsx, aplica funcao(workbook), confere que ninguém mexeu no meio e sobe no mesmo ID.
    Devolve os bytes originais (guardar como backup antes de qualquer coisa)."""
    import openpyxl
    m0 = meta(i)['modifiedTime']; raw = baixar(i)
    wb = openpyxl.load_workbook(io.BytesIO(raw)); funcao(wb)
    if meta(i)['modifiedTime'] != m0: raise RuntimeError('a planilha mudou durante a edição; refazer')
    bio = io.BytesIO(); wb.save(bio); substituir_conteudo(i, bio.getvalue(), XLSX)
    return raw


def trocar_texto_doc(i, trocas):
    """Troca textos e links num Google Doc pela ida e volta em .docx.
    ATENÇÃO: cada ida e volta DUPLICA os comentários abertos do doc. Depois, fechar as cópias
    (resposta com action=resolve) e manter o original. Docs API dá 403 nesta chave."""
    import docx
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    raw = exportar(i, DOCX); d = docx.Document(io.BytesIO(raw)); n = 0
    for p in d.element.body.iter(W + 'p'):
        ts = list(p.iter(W + 't')); full = ''.join(t.text or '' for t in ts)
        novo = full
        for a, b in trocas: novo = novo.replace(a, b)
        if novo != full and ts:
            ts[0].text = novo; ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            for t in ts[1:]: t.text = ''
            n += 1
    for r in d.part.rels.values():
        if r.is_external:
            for a, b in trocas:
                if a in r.target_ref: r._target = r.target_ref.replace(a, b)
    bio = io.BytesIO(); d.save(bio); substituir_conteudo(i, bio.getvalue(), DOCX)
    return raw, n
