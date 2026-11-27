"""Monta uma apresentação do Google Slides com os vídeos animados da Elite Mentoring,
na ordem da copy, um vídeo por slide (como no PowerPoint), com notas do apresentador."""
import json
import os
import re
import urllib.parse
import urllib.request

FOLDER = '1bg9G_pUdrK3nUacbOgV-yWPFpDbXERDW'


def token():
    data = urllib.parse.urlencode({'client_id': os.environ['FEA_GDRIVE_CLIENT_ID'], 'client_secret': os.environ['FEA_GDRIVE_CLIENT_SECRET'],
                                   'refresh_token': os.environ['FEA_GDRIVE_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}).encode()
    return json.load(urllib.request.urlopen('https://oauth2.googleapis.com/token', data))['access_token']


TOK = token()


def api(method, url, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f'Bearer {TOK}', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))


TITLES = {
    '02': 'Raio-X da Clínica Elite', '03': 'Os 4 pilares', '09': 'Some as 4 notas', '10': 'Qual é o momento da sua clínica?',
    '12': 'Como virar uma Clínica Elite', '13': 'Três níveis', '14': '1h por semana', '15': 'Portal: vamos voltar no tempo',
    '19': 'Rostos = vidas = clínica que cresce', '27': 'Portal: vamos voltar ao presente', '28': 'Os 6 sins',
    '46': 'Quanto vale? (recibo)', '49': 'Tem mais', '54': 'Desafio Clínica Elite', '58': 'Segunda cadeira',
    '59': 'Por apenas R$ 35.000', '60': 'Revelação: R$ 25.000', '62': 'Garantia de 7 dias', '67': 'Bem-vinda, Clínica Elite'}
CLICK_NOTE = {
    '10': ['Título e as 4 faixas apagadas', 'Acende 0 a 15: Clínica no improviso', 'Acende 16 a 25: Fatura, mas não sobra', 'Acende 26 a 33: Pronta para escalar', 'Acende 34 a 40: Clínica Elite'],
    '12': ['Título e passo 1: Diagnóstico', 'Passo 2: Plano', 'Passo 3: Acompanhamento'],
    '14': ['1h e a frase', 'Só 1 hora? Sim. Feita do jeito certo.'],
    '28': ['Título e os 6 cartões apagados'] + [f'Pergunta {i} acende (SIM)' for i in range(1, 7)],
    '46': ['Título e o recibo vazio', 'Mentoria de 6 meses: R$ 35.000', 'Cursos online por 12 meses: R$ 20.000', '8 calls individuais: R$ 8.000', 'Grupo e encontro presencial: R$ 5.000', 'Diagnóstico nos 4 pilares: R$ 2.000', 'Total: R$ 70.000'],
}
PENDING = [('23', 'Linha do tempo do Dr. João', 'Falta: marcos, idades e a queda.'),
           ('24 e 25', 'Datas com raio (verde e vermelho)', 'Falta: mês e ano das duas datas.'),
           ('37', 'Mentores (guarda-chuva)', 'Falta: fotos do Dr. João, Luca e dos 4 mentores.'),
           ('47', 'Cursos em cards', 'Falta: lista de cursos e capas (reaproveita o carrossel da Black Friday).')]

files = api('GET', 'https://www.googleapis.com/drive/v3/files?' + urllib.parse.urlencode({
    'q': f"'{FOLDER}' in parents and mimeType='video/mp4' and trashed=false", 'fields': 'files(id,name)', 'pageSize': 200,
    'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}))['files']
items = []
for f in files:
    m = re.match(r'FEA-elite-slide-(\d+)(?:-clique-(\d+)|-(loop))?\.mp4', f['name'])
    s, c, lp = m.groups()
    items.append((int(s), 99 if lp else int(c or 1), s, c, lp, f['id']))
items.sort()
nclk = {}
for it in items:
    if it[3]: nclk[it[2]] = max(nclk.get(it[2], 0), int(it[3]))

pres = api('POST', 'https://www.googleapis.com/drive/v3/files?supportsAllDrives=true&fields=id', {
    'name': 'FEA-elite-mentoring-slides-animados (visualização)', 'mimeType': 'application/vnd.google-apps.presentation', 'parents': [FOLDER]})
PID = pres['id']
p = api('GET', f'https://slides.googleapis.com/v1/presentations/{PID}')
W, H = p['pageSize']['width']['magnitude'], p['pageSize']['height']['magnitude']
first = p['slides'][0]['objectId']

reqs = [{'deleteObject': {'objectId': first}}]
n = 0


def emu(x): return {'magnitude': x, 'unit': 'EMU'}


def bg(sid):
    reqs.append({'updatePageProperties': {'objectId': sid, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': {'red': 1 / 255, 'green': 26 / 255, 'blue': 36 / 255}}}}}, 'fields': 'pageBackgroundFill'}})


def text(sid, tid, txt, x, y, w, h, size, color, bold=False, font='Montserrat'):
    reqs.append({'createShape': {'objectId': tid, 'shapeType': 'TEXT_BOX', 'elementProperties': {'pageObjectId': sid, 'size': {'width': emu(w), 'height': emu(h)},
                 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'EMU'}}}})
    reqs.append({'insertText': {'objectId': tid, 'text': txt}})
    reqs.append({'updateTextStyle': {'objectId': tid, 'style': {'fontSize': {'magnitude': size, 'unit': 'PT'}, 'bold': bold, 'fontFamily': font,
                 'foregroundColor': {'opaqueColor': {'rgbColor': color}}}, 'fields': 'fontSize,bold,fontFamily,foregroundColor'}})


INK, CY, MUT = {'red': .95, 'green': .98, 'blue': .98}, {'red': .53, 'green': .98, 'blue': .97}, {'red': .56, 'green': .70, 'blue': .71}

# capa
n += 1; sid = f's{n}'
reqs.append({'createSlide': {'objectId': sid, 'insertionIndex': 0, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}}); bg(sid)
text(sid, 'c1', 'ELITE MENTORING · ELITE INJECTORS CONGRESS', W * .08, H * .28, W * .84, H * .08, 12, CY, True)
text(sid, 'c2', 'Slides animados do pitch', W * .08, H * .36, W * .84, H * .16, 40, INK, False, 'Playfair Display')
text(sid, 'c3', 'Um vídeo por clique, na ordem da copy. Em modo apresentação, cada vídeo toca sozinho ao entrar no slide.\nA numeração “Slide 10 · clique 2/5” é a dos 78 slides da copy. Detalhes de cada clique nas notas do apresentador.',
     W * .08, H * .56, W * .84, H * .2, 13, MUT)

pend_done = set()
for _, _, s, c, lp, fid in items:
    for code, ttl, why in PENDING:
        first_num = int(code.split()[0])
        if code not in pend_done and first_num < int(s):
            pend_done.add(code)
            n += 1; sid = f's{n}'
            reqs.append({'createSlide': {'objectId': sid, 'insertionIndex': n - 1, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}}); bg(sid)
            text(sid, f'p{n}a', f'SLIDE {code} · A FAZER', W * .08, H * .38, W * .84, H * .08, 12, CY, True)
            text(sid, f'p{n}b', ttl, W * .08, H * .45, W * .84, H * .12, 30, INK, False, 'Playfair Display')
            text(sid, f'p{n}c', why, W * .08, H * .58, W * .84, H * .1, 14, MUT)
    n += 1; sid = f's{n}'
    reqs.append({'createSlide': {'objectId': sid, 'insertionIndex': n - 1, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}}); bg(sid)
    reqs.append({'createVideo': {'objectId': f'v{n}', 'source': 'DRIVE', 'id': fid, 'elementProperties': {'pageObjectId': sid,
                 'size': {'width': emu(W), 'height': emu(H)}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 0, 'translateY': 0, 'unit': 'EMU'}}}})
    reqs.append({'updateVideoProperties': {'objectId': f'v{n}', 'videoProperties': {'autoPlay': True, 'mute': True}, 'fields': 'autoPlay,mute'}})
    if lp:
        label = f'Slide {s} · {TITLES[s]} · loop (no PowerPoint: “Repetir até ser interrompido”)'
    elif c:
        k = nclk[s]; label = f'Slide {s} · {TITLES[s]} · clique {c}/{k}: {CLICK_NOTE.get(s, [""] * k)[int(c) - 1]}'
    else:
        label = f'Slide {s} · {TITLES[s]}' + (' · entrada' if s in ('15', '27', '67') else '')
    reqs.append(('NOTES', sid, label))

# primeira passada: tudo menos as notas
batch = [r for r in reqs if not isinstance(r, tuple)]
for i in range(0, len(batch), 400):
    api('POST', f'https://slides.googleapis.com/v1/presentations/{PID}:batchUpdate', {'requests': batch[i:i + 400]})
# notas do apresentador
p = api('GET', f'https://slides.googleapis.com/v1/presentations/{PID}')
notes_id = {sl['objectId']: sl['slideProperties']['notesPage']['notesProperties']['speakerNotesObjectId'] for sl in p['slides']}
nreq = [{'insertText': {'objectId': notes_id[sid], 'text': label}} for _, sid, label in [r for r in reqs if isinstance(r, tuple)]]
api('POST', f'https://slides.googleapis.com/v1/presentations/{PID}:batchUpdate', {'requests': nreq})
print(PID, len(p['slides']), 'slides')
