#!/usr/bin/env python3
"""
Substitui o texto de um PDF diagramado pela tradução, preservando imagens,
posição, fonte, corpo, cor e entrelinha do original.

Uso:
    python3 traduzir_pdf.py original.pdf mapa.json --fontes fontes/ --saida out.pdf
    python3 traduzir_pdf.py original.pdf --estrutura        # extrai o esqueleto

Como funciona:
  1. PDFs de InDesign exportam UMA LINHA POR BLOCO. O script reagrupa as linhas
     em parágrafos por geometria (mesma margem, y consecutivo, salto == entrelinha).
  2. Cada parágrafo é classificado por fonte, corpo e cor: corpo de texto,
     título de seção, cabeçalho corrido, legenda, número de página.
  3. O texto original é removido por redação, com as imagens preservadas.
  4. O espanhol é refluído no MESMO retângulo, com a MESMA fonte (completada por
     completar_fonte.py), justificação, entrelinha e recuo de primeira linha.
  5. Se o espanhol não couber — ele corre 15% a 20% mais longo — o script reduz
     a entrelinha e depois o corpo, em passos pequenos, e REGISTRA o ajuste.
     Nada é cortado: transbordo vira erro, não texto perdido.
"""
import sys, os, json, argparse, re
import pymupdf

TOL_Y      = 3.0     # tolerância para considerar linhas na mesma coluna
MAX_RED_EL = 0.08    # redução máxima da entrelinha (8%)
MAX_RED_PT = 0.06    # redução máxima do corpo (6%)

def cor_rgb(i):
    return ((i >> 16 & 255)/255, (i >> 8 & 255)/255, (i & 255)/255)

def classifica(fontes, tam, cor):
    f = ' '.join(fontes)
    if 'Guardian' in f:                       return 'corpo'
    if tam >= 20:                             return 'titulo_display'
    if 'Playfair' in f:                       return 'titulo_capitulo'
    if tam <= 7.5:                            return 'cabecalho'
    if cor == 0xffffff and tam <= 8.5:        return 'numero_pagina'
    if 'Bold' in f and tam >= 10:             return 'titulo_secao'
    if 'Medium' in f and tam <= 9.5:          return 'legenda'
    return 'outro'

def agrupa(page):
    """Reagrupa as linhas exportadas linha-a-linha em parágrafos."""
    linhas = []
    for b in page.get_text('dict')['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip() or s['text'] == ' ']
            if not spans: continue
            txt = ''.join(s['text'] for s in spans)
            if not txt.strip(): continue
            linhas.append(dict(bbox=list(l['bbox']), spans=spans, texto=txt,
                               x0=round(l['bbox'][0], 1), y0=l['bbox'][1], y1=l['bbox'][3]))
    linhas.sort(key=lambda l: (round(l['y0'], 1), l['x0']))

    paras, atual = [], None
    for l in linhas:
        fontes = {s['font'].split('+')[-1] for s in l['spans']}
        tam    = max(round(s['size'], 1) for s in l['spans'])
        cor    = l['spans'][0]['color']
        tipo   = classifica(fontes, tam, cor)
        mesmoEstilo = (atual and atual['tipo'] == tipo
                       and abs(atual['tam'] - tam) < 1.0 and atual['cor'] == cor)
        if mesmoEstilo and tipo in ('corpo', 'legenda', 'titulo_capitulo',
                                    'titulo_display', 'titulo_secao', 'cabecalho'):
            salto = l['y0'] - atual['linhas'][-1]['y0']
            # continuação = linha na margem; recuada abre novo parágrafo.
            # A última linha de um parágrafo justificado é curta: comparar a
            # margem DIREITA quebraria o parágrafo ali.
            # Continuação: a linha começa na margem do parágrafo ou à ESQUERDA
            # da primeira linha (que é a recuada). Linha mais à direita que a
            # anterior abre parágrafo novo. Usar a margem do próprio parágrafo,
            # e não uma margem global da página, é o que faz isto funcionar em
            # páginas com caixas laterais e legendas.
            prev = atual['linhas'][-1]
            # legendas e rótulos lado a lado, em colunas diferentes, não podem
            # ser fundidos: exige sobreposição horizontal real entre as linhas
            ov = min(l['bbox'][2], prev['bbox'][2]) - max(l['bbox'][0], prev['bbox'][0])
            larg = min(l['bbox'][2]-l['bbox'][0], prev['bbox'][2]-prev['bbox'][0]) or 1
            mesmaColuna = ov / larg > 0.4
            continua = (l['x0'] <= prev['x0'] + 1.5) if tipo == 'corpo' else mesmaColuna
            # com uma única linha ainda não se conhece a entrelinha: usar o
            # corpo como referência, senão QUALQUER salto seria aceito e dois
            # rótulos distantes na mesma coluna acabariam no mesmo parágrafo
            limSalto = (atual['entrelinha'] * 1.6 + 2 if atual['entrelinha']
                        else atual['tam'] * 2.0)
            if 0 < salto <= limSalto and continua:
                atual['linhas'].append(l)
                if atual['entrelinha'] is None: atual['entrelinha'] = round(salto, 1)
                continue
        atual = dict(tipo=tipo, tam=tam, cor=cor, fontes=fontes, linhas=[l], entrelinha=None)
        paras.append(atual)

    for p in paras:
        xs0 = [l['bbox'][0] for l in p['linhas']]; xs1 = [l['bbox'][2] for l in p['linhas']]
        p['rect'] = pymupdf.Rect(min(xs0), p['linhas'][0]['bbox'][1],
                                 max(xs1), p['linhas'][-1]['bbox'][3])
        bruto = ' '.join(l['texto'] for l in p['linhas'])
        bruto = re.sub(r'(\w)-\s+(\w)', r'\1\2', bruto)      # desfaz hifenização de fim de linha
        p['texto'] = re.sub(r'\s+', ' ', bruto).strip()
        p['recuo'] = round(p['linhas'][0]['bbox'][0] - min(xs0[1:]) if len(xs0) > 1 else 0, 1)
        p['negrito'] = [s['text'].strip() for l in p['linhas'] for s in l['spans']
                        if 'Bold' in s['font'] and s['text'].strip()]
        # linha de base da primeira linha: é ela que a tradução tem de repetir
        p['base_y'] = p['linhas'][0]['spans'][0]['origin'][1]
        p['base_y_fim'] = p['linhas'][-1]['spans'][0]['origin'][1]
        if p['entrelinha'] is None:
            p['entrelinha'] = round(p['tam'] * 1.35, 1)
        # fonte real dominante: a que carrega mais caracteres no parágrafo
        from collections import Counter
        uso = Counter()
        for l in p['linhas']:
            for sp in l['spans']:
                uso[sp['font'].split('+')[-1]] += len(sp['text'])
        p['fonte'] = uso.most_common(1)[0][0] if uso else 'HelveticaNeue'
    return paras

def prepara_fontes(dirFontes):
    arch = pymupdf.Archive()
    reg = {}
    for f in sorted(os.listdir(dirFontes)):
        if not f.lower().endswith(('.otf', '.ttf')): continue
        nome = os.path.splitext(f)[0]
        arch.add(os.path.join(dirFontes, f), f)
        reg[nome] = f
    return arch, reg

def css_de(p, reg, familia=None):
    tam = p['tam']; el = p['entrelinha']
    align = 'justify' if p['tipo'] == 'corpo' else 'left'
    r, g, b = cor_rgb(p['cor'])
    base = p.get('fonte', 'HelveticaNeue')
    # prefere a variante completada com os glifos do espanhol
    if base + 'ES' in reg: base = base + 'ES'
    normal = base if base in reg else None
    if normal is None:                                  # tenta a variante sem peso
        cand = [n for n in reg if n.startswith(base.split('-')[0])]
        normal = sorted(cand, key=len)[0] if cand else list(reg)[0]
    raiz = normal.replace('ES', '').split('-')[0]
    cands = [n for n in reg if n.startswith(raiz) and 'Bold' in n]
    irmaoBold = next((n for n in cands if n.endswith('ES')), cands[0] if cands else normal)
    familia = 'F' + re.sub(r'[^A-Za-z]', '', raiz)
    faces = ['@font-face {font-family: %s; src: url(%s); font-weight: normal;}'
             % (familia, reg[normal]),
             '@font-face {font-family: %s; src: url(%s); font-weight: bold;}'
             % (familia, reg[irmaoBold])]
    return '\n'.join(faces) + """
p {font-family: %s; font-size: %.2fpx; line-height: %.4f; text-align: %s;
   margin: 0; text-indent: %.1fpx; color: rgb(%d,%d,%d);}
b {font-weight: bold;}
""" % (familia, tam, el/tam, align, max(p['recuo'], 0), r*255, g*255, b*255)

def html_de(es, negritos):
    """Reaplica o negrito do original. Se o mapa já traz <b>, respeita o mapa."""
    if '<b>' in es: return '<p>%s</p>' % es
    txt = es
    for frase in sorted({n for n in negritos if len(n) > 3}, key=len, reverse=True):
        if frase in txt and '<b>' not in frase:
            txt = txt.replace(frase, '<b>%s</b>' % frase, 1)
    return '<p>%s</p>' % txt

FLUXO = ('corpo', 'titulo_secao', 'titulo_capitulo', 'titulo_display')
MARGEM_INF = 12.0      # respiro mínimo até o pé da página

def mede(page, rect, html, css, arch, baixo=1):
    """Compõe num rascunho e devolve (1ª linha de base, última, transbordou, escala)."""
    tmp = pymupdf.open()
    pg = tmp.new_page(width=page.rect.width, height=page.rect.height)
    sobra, esc = pg.insert_htmlbox(rect, html, css=css, archive=arch, scale_low=baixo)
    bases = [s['origin'][1] for b in pg.get_text('dict')['blocks'] if not b['type']
             for l in b['lines'] for s in l['spans'] if s['text'].strip()]
    tmp.close()
    if not bases: return None, None, True, esc
    return min(bases), max(bases), sobra < 0, esc

def colunas(paras, mapa):
    """Agrupa em colunas de texto os parágrafos que correm juntos."""
    fluxo = [p for p in paras if p['tipo'] in FLUXO and p['id'] in mapa and mapa[p['id']]]
    fluxo.sort(key=lambda p: p['rect'].y0)
    cols = []
    for p in fluxo:
        posto = False
        for c in cols:
            u = c[-1]
            ov = min(p['rect'].x1, u['rect'].x1) - max(p['rect'].x0, u['rect'].x0)
            larg = min(p['rect'].width, u['rect'].width) or 1
            salto = p['base_y'] - u['base_y_fim']
            razao = max(p['tam'], u['tam']) / max(min(p['tam'], u['tam']), 0.1)
            if (ov / larg > 0.4 and 0 < salto < (u['entrelinha'] or 12) * 1.9
                    and razao <= 1.6):
                c.append(p); posto = True; break
        if posto: continue
        cols.append([p])
    return cols

def cresce_dir(p):
    """Quem pode ganhar largura: títulos, rótulos e parágrafos de uma só linha
    (nesses a caixa original abraça o texto português, e o espanhol é maior).
    Parágrafo justificado de várias linhas mantém a largura da coluna."""
    return p['tipo'] != 'corpo' or len(p['linhas']) == 1

def obstaculos(page, paras):
    """Tudo que a tradução não pode invadir: parágrafos, imagens e os fios
    desenhados (as linhas douradas de topo e pé de página, por exemplo)."""
    obs = [dict(id=p['id'], rect=p['rect']) for p in paras]
    d = page.get_text('dict')
    for b in d['blocks']:
        if b['type'] == 1:
            obs.append(dict(id=None, rect=pymupdf.Rect(b['bbox'])))
    for dr in page.get_drawings():
        r = dr['rect']
        if r.width > 3 and r.height < 6 or r.height > 3 and r.width < 6:
            obs.append(dict(id=None, rect=r))
    return obs

def limite_abaixo(page, base, paras, ignora=()):
    """Até onde este bloco pode crescer sem invadir o que vem abaixo dele."""
    lim = page.rect.y1 - MARGEM_INF
    ids = {x['id'] for x in ignora}
    for o in paras:
        if o['id'] == base['id'] or o['id'] in ids: continue
        ov = min(base['rect'].x1, o['rect'].x1) - max(base['rect'].x0, o['rect'].x0)
        larg = min(base['rect'].width, o['rect'].width) or 1
        if ov / larg > 0.25 and o['rect'].y0 > base['rect'].y1 - 1:
            lim = min(lim, o['rect'].y0 - 2)
    return max(lim, base['rect'].y1 + 2)

def limite_direita(page, base, obs, ignora=()):
    """Títulos e rótulos não são justificados: em espanhol eles crescem para a
    direita até o próximo obstáculo, em vez de encolher de corpo."""
    lim = page.rect.x1 - MARGEM_INF
    ids = {x['id'] for x in ignora}
    for o in obs:
        if o['id'] == base['id'] or o['id'] in ids: continue
        ov = min(base['rect'].y1, o['rect'].y1) - max(base['rect'].y0, o['rect'].y0)
        alt = min(base['rect'].height, o['rect'].height) or 1
        if ov / alt > 0.3 and o['rect'].x0 > base['rect'].x1 - 1:
            lim = min(lim, o['rect'].x0 - 3)
    return max(lim, base['rect'].x1 + 2)

def limite_da_coluna(page, col, obs):
    """Até onde a coluna pode crescer sem invadir nada."""
    lim = page.rect.y1 - MARGEM_INF
    base = col[-1]
    ids = {p['id'] for p in col}
    for o in obs:
        if o['id'] in ids: continue
        ov = min(base['rect'].x1, o['rect'].x1) - max(base['rect'].x0, o['rect'].x0)
        larg = min(base['rect'].width, o['rect'].width) or 1
        if ov / larg > 0.25 and o['rect'].y0 > base['rect'].y1 - 1:
            lim = min(lim, o['rect'].y0 - 3)
    return max(lim, base['rect'].y1 + 2)

def compoe_coluna(page, col, mapa, arch, reg, lim, limDir, redEl, redPt, tol=False):
    """Alinha a coluna inteira mantendo a 1ª linha de base e os respiros do
    original. Devolve [(parágrafo, rect, html, css, escala)] ou None. Com
    tol=True nunca desiste nem perde texto: o parágrafo que não couber é
    reduzido pelo htmlbox e a redução volta registrada em `escala`."""
    saida = []
    alvo = col[0]['base_y']
    for i, p in enumerate(col):
        if p.get('ancora_fixa'): alvo = p['base_y']
        q = dict(p)
        q['entrelinha'] = p['entrelinha'] * (1 - redEl)
        q['tam'] = p['tam'] * (1 - redPt)
        css = css_de(q, reg)
        html = html_de(mapa[p['id']], p['negrito'])
        x1 = limDir[p['id']] if cresce_dir(p) else p['rect'].x1 + 2
        rect = pymupdf.Rect(p['rect'].x0 - 1, p['rect'].y0 - 2, x1, lim)

        b0, b1, estourou, esc = mede(page, rect, html, css, arch)
        if b0 is None or estourou:
            if not tol: return None
            b0, b1, estourou, esc = mede(page, rect, html, css, arch, baixo=0)
            if b0 is None:
                saida.append((p, rect, html, css, 0.0)); continue

        dy = alvo - b0
        fundo = max(lim, p['rect'].y1 + max(dy, 0) + 3)
        rect = pymupdf.Rect(rect.x0, rect.y0 + dy, rect.x1, fundo)
        baixo = 1 if esc >= 0.999 else 0
        b0, b1, estourou, esc = mede(page, rect, html, css, arch, baixo=baixo)
        if b0 is None or estourou or b1 > fundo:
            if not tol: return None
            b0, b1, estourou, esc = mede(page, rect, html, css, arch, baixo=0)
            if b0 is None:
                saida.append((p, rect, html, css, 0.0)); continue

        saida.append((p, rect, html, css, esc))
        if i + 1 < len(col):
            vao = col[i+1]['base_y'] - p['base_y_fim']       # respiro original
            alvo = b1 + vao * (1 - redEl)
    return saida

def preserva(page, paras, mapa, red, reg, dirFontes, log):
    """A redação apaga TODO texto que toca o retângulo — inclusive o que não é
    nosso. Nas aberturas de capítulo o numeral gigante ('03.') cruza a caixa do
    título. Guardamos esses trechos antes e os redesenhamos idênticos depois."""
    guarda = []
    for p in paras:
        if p['id'] in mapa: continue
        for l in p['linhas']:
            r = pymupdf.Rect(l['bbox'])
            if not any((r & q).is_valid and (r & q).get_area() > 0 for q in red): continue
            for s in l['spans']:
                if not s['text'].strip(): continue
                nome = s['font'].split('+')[-1]
                arq = None
                for cand in (nome, nome + 'ES'):
                    if cand in reg: arq = os.path.join(dirFontes, reg[cand]); break
                guarda.append(dict(texto=s['text'], origem=s['origin'], tam=s['size'],
                                   cor=cor_rgb(s['color']), arq=arq, fonte=nome,
                                   id=p['id']))
    return guarda

def redesenha(page, guarda, log):
    for g in guarda:
        try:
            if g['arq']:
                page.insert_text(g['origem'], g['texto'], fontsize=g['tam'],
                                 fontfile=g['arq'], fontname='P' + re.sub(r'\W', '', g['fonte'])[:12],
                                 color=g['cor'])
            else:
                page.insert_text(g['origem'], g['texto'], fontsize=g['tam'],
                                 fontname='helv', color=g['cor'])
                log.append(dict(pagina=page.number+1, id=g['id'],
                                erro='trecho preservado redesenhado em fonte substituta (%s ausente)'
                                     % g['fonte']))
        except Exception as e:
            log.append(dict(pagina=page.number+1, id=g['id'],
                            erro='falha ao redesenhar trecho preservado: %s' % e))


def parte_em_dois(es, k):
    """Divide o espanhol depois da k-ésima palavra, respeitando o <b>: se o
    corte cair dentro do negrito, fecha na primeira parte e reabre na segunda."""
    fichas = re.findall(r'<[^>]+>|[^\s<]+|\s+', es)
    a, b, n, negrito = [], [], 0, False
    for f in fichas:
        if f.startswith('<'):
            if f.lower().startswith('<b'): negrito = True
            elif f.lower().startswith('</b'): negrito = False
            (a if n < k else b).append(f); continue
        if not f.strip():
            (a if n < k else b).append(f); continue
        if n == k and negrito:
            a.append('</b>'); b.append('<b>')
        (a if n < k else b).append(f)
        n += 1
    sa = ''.join(a).strip(); sb = ''.join(b).strip()
    if sa.count('<b>') > sa.count('</b>'): sa += '</b>'
    if sb.count('</b>') > sb.count('<b>'): sb = '<b>' + sb
    return sa, sb

def cabe_no_grupo(page, q, es, arch, reg):
    css = css_de(q, reg)
    rect = pymupdf.Rect(q['rect'].x0 - 1, q['rect'].y0 - 2,
                        q['rect'].x1 + 2, q['rect'].y1 + 2)
    b0, b1, estourou, _e = mede(page, rect, '<p>%s</p>' % es, css, arch)
    return b0 is not None and not estourou

def conta_palavras(es):
    return len(re.findall(r'\S+', re.sub(r'<[^>]+>', ' ', es)))

def enche(page, q, es, arch, reg, redEl=0.0, redPt=0.0):
    """Quantas palavras do espanhol cabem nesta caixa de altura fixa."""
    q = dict(q)
    q['entrelinha'] = q['entrelinha'] * (1 - redEl)
    q['tam'] = q['tam'] * (1 - redPt)
    total = conta_palavras(es)
    if total < 2: return es, ''
    lo, hi, melhor = 1, total, 1
    while lo <= hi:
        meio = (lo + hi) // 2
        sa, _ = parte_em_dois(es, meio)
        if cabe_no_grupo(page, q, sa, arch, reg):
            melhor = meio; lo = meio + 1
        else:
            hi = meio - 1
    return parte_em_dois(es, melhor)

def grupos_de_contorno(p):
    """Um parágrafo justificado que contorna uma imagem, um QR ou uma capitular
    tem uma ou mais linhas com medida diferente do corpo do parágrafo. Devolve
    a lista de fatias de linhas (uma por medida), ou None se for um parágrafo
    retangular comum. A última linha, sempre curta, nunca conta."""
    if p['tipo'] != 'corpo' or len(p['linhas']) < 3: return None
    L = [(l['bbox'][0], l['bbox'][2]) for l in p['linhas']]
    mn0 = min(x for x, _ in L); mx1 = max(y for _, y in L)

    def concorda(fatia):
        """linhas justificadas na MESMA medida estreita (não apenas curtas)"""
        if len(fatia) < 2: return False
        xs1 = [y for _, y in fatia]; xs0 = [x for x, _ in fatia[1:]] or [fatia[0][0]]
        estreita = (max(xs1) <= mx1 - 20) or (min(xs0) >= mn0 + 20)
        return estreita and (max(xs1) - min(xs1) <= 4)

    a = 0
    while a < len(L) - 1 and (L[a][0] >= mn0 + 20 or L[a][1] <= mx1 - 20): a += 1
    if not concorda(L[:a]): a = 0
    c = 0
    while c < len(L) - 1 - a and L[len(L)-1-c][1] <= mx1 - 20: c += 1
    # a última linha é curta por natureza: só conta como contorno com companhia
    if not concorda(L[len(L)-c:-1] or L[len(L)-c:]): c = 0
    if not a and not c: return None
    cortes = []
    if a: cortes.append((0, a))
    if a or c: cortes.append((a, len(L) - c))
    if c: cortes.append((len(L) - c, len(L)))
    return [f for f in cortes if f[1] > f[0]]

def desdobra_contornos(page, paras, mapa, arch, reg):
    """Desdobra em caixas reais os parágrafos que contornam uma imagem ou uma
    capitular, para o refluxo do espanhol não invadir a arte."""
    saida, mp, contornos = [], dict(mapa), {}
    for p in paras:
        gs = grupos_de_contorno(p) if p['id'] in mp and mp.get(p['id']) else None
        if not gs or len(gs) < 2:
            saida.append(p); continue
        pecas = []
        for k, (i, j) in enumerate(gs):
            ls = p['linhas'][i:j]
            q = dict(p); q['linhas'] = ls; q['id'] = p['id'] + 'abcd'[k]
            q['rect'] = pymupdf.Rect(min(l['bbox'][0] for l in ls), ls[0]['bbox'][1],
                                     max(l['bbox'][2] for l in ls), ls[-1]['bbox'][3])
            q['base_y'] = ls[0]['spans'][0]['origin'][1]
            q['base_y_fim'] = ls[-1]['spans'][0]['origin'][1]
            q['recuo'] = p['recuo'] if k == 0 else 0
            # cada pedaço tem posição ditada pela arte: não pode ser empurrado
            q['ancora_fixa'] = True
            pecas.append(q)
        inteiro = mp.pop(p['id'])
        contornos[pecas[0]['id']] = dict(pecas=[q['id'] for q in pecas], texto=inteiro)
        for k, v in reparte(page, pecas, inteiro, arch, reg).items(): mp[k] = v
        saida += pecas
    return saida, mp, contornos

def reparte(page, pecas, inteiro, arch, reg, redEl=0.0, redPt=0.0):
    """Distribui o espanhol entre as caixas do contorno, no corpo pedido."""
    saida, resto = {}, inteiro
    for q in pecas[:-1]:
        parte, resto = enche(page, q, resto, arch, reg, redEl, redPt)
        saida[q['id']] = parte
    saida[pecas[-1]['id']] = resto
    return saida

def preserva(page, paras, mapa, red, reg, dirFontes, log):
    """A redação apaga TODO texto que toca o retângulo — inclusive o que não é
    nosso. Nas aberturas de capítulo o numeral gigante ('03.') cruza a caixa do
    título. Guardamos esses trechos antes e os redesenhamos idênticos depois."""
    guarda = []
    for p in paras:
        if p['id'] in mapa: continue
        for l in p['linhas']:
            r = pymupdf.Rect(l['bbox'])
            if not any((r & q).is_valid and (r & q).get_area() > 0 for q in red): continue
            for s in l['spans']:
                if not s['text'].strip(): continue
                nome = s['font'].split('+')[-1]
                arq = None
                for cand in (nome, nome + 'ES'):
                    if cand in reg: arq = os.path.join(dirFontes, reg[cand]); break
                guarda.append(dict(texto=s['text'], origem=s['origin'], tam=s['size'],
                                   cor=cor_rgb(s['color']), arq=arq, fonte=nome,
                                   id=p['id']))
    return guarda

def redesenha(page, guarda, log):
    for g in guarda:
        try:
            if g['arq']:
                page.insert_text(g['origem'], g['texto'], fontsize=g['tam'],
                                 fontfile=g['arq'], fontname='P' + re.sub(r'\W', '', g['fonte'])[:12],
                                 color=g['cor'])
            else:
                page.insert_text(g['origem'], g['texto'], fontsize=g['tam'],
                                 fontname='helv', color=g['cor'])
                log.append(dict(pagina=page.number+1, id=g['id'],
                                erro='trecho preservado redesenhado em fonte substituta (%s ausente)'
                                     % g['fonte']))
        except Exception as e:
            log.append(dict(pagina=page.number+1, id=g['id'],
                            erro='falha ao redesenhar trecho preservado: %s' % e))


def parte_em_dois(es, k):
    """Divide o espanhol depois da k-ésima palavra, respeitando o <b>: se o
    corte cair dentro do negrito, fecha na primeira parte e reabre na segunda."""
    fichas = re.findall(r'<[^>]+>|[^\s<]+|\s+', es)
    a, b, n, negrito = [], [], 0, False
    for f in fichas:
        if f.startswith('<'):
            if f.lower().startswith('<b'): negrito = True
            elif f.lower().startswith('</b'): negrito = False
            (a if n < k else b).append(f); continue
        if not f.strip():
            (a if n < k else b).append(f); continue
        if n == k and negrito:
            a.append('</b>'); b.append('<b>')
        (a if n < k else b).append(f)
        n += 1
    sa = ''.join(a).strip(); sb = ''.join(b).strip()
    if sa.count('<b>') > sa.count('</b>'): sa += '</b>'
    if sb.count('</b>') > sb.count('<b>'): sb = '<b>' + sb
    return sa, sb

def divide_em_L(page, pa, pb, es, arch, reg):
    """Parágrafo que contorna uma capitular: a cabeça corre numa caixa estreita
    de altura fixa e o resto na largura cheia. Acha por busca binária quantas
    palavras cabem na cabeça."""
    total = len(re.findall(r'(?<![<>/\w])[^\s<]+', re.sub(r'<[^>]+>', ' ', es).strip()))
    if total < 2: return es, ''
    css = css_de(pa, reg)
    rect = pymupdf.Rect(pa['rect'].x0 - 1, pa['rect'].y0 - 2,
                        pa['rect'].x1 + 2, pa['rect'].y1 + 2)
    lo, hi, melhor = 1, total, 1
    while lo <= hi:
        meio = (lo + hi) // 2
        sa, _ = parte_em_dois(es, meio)
        b0, b1, estourou, _e = mede(page, rect, '<p>%s</p>' % sa, css, arch)
        if b0 is not None and not estourou:
            melhor = meio; lo = meio + 1
        else:
            hi = meio - 1
    return parte_em_dois(es, melhor)

def desdobra_capitulares(page, paras, mapa, arch, reg):
    """Detecta o parágrafo com cabeça recuada (capitular ao lado) e o desdobra
    em dois parágrafos reais, para o refluxo não invadir a letra capitular."""
    saida, mp = [], dict(mapa)
    for p in paras:
        xs = [round(l['bbox'][0], 1) for l in p['linhas']]
        base = min(xs); rec = 0
        for x in xs:
            if x > base + 8: rec += 1
            else: break
        if (p['tipo'] != 'corpo' or rec < 2 or rec >= len(xs)
                or p['id'] not in mp or not mp[p['id']]):
            saida.append(p); continue
        def monta(ls, suf):
            q = dict(p); q['linhas'] = ls; q['id'] = p['id'] + suf
            q['rect'] = pymupdf.Rect(min(l['bbox'][0] for l in ls), ls[0]['bbox'][1],
                                     max(l['bbox'][2] for l in ls), ls[-1]['bbox'][3])
            q['base_y'] = ls[0]['spans'][0]['origin'][1]
            q['base_y_fim'] = ls[-1]['spans'][0]['origin'][1]
            q['recuo'] = 0
            return q
        pa = monta(p['linhas'][:rec], 'a'); pb = monta(p['linhas'][rec:], 'b')
        esA, esB = divide_em_L(page, pa, pb, mp[p['id']], arch, reg)
        mp.pop(p['id'], None)
        mp[pa['id']] = esA; mp[pb['id']] = esB
        saida += [pa, pb]
    return saida, mp

def assenta_display(page, p, es, reg, dirFontes):
    """Título de display com entrelinha FECHADA (menor que a altura do desenho)
    não cabe no htmlbox: a caixa corta o acento da primeira linha. Aqui cada
    linha é assentada na sua própria linha de base, exatamente como no original.
    Só se aplica quando o espanhol tem o mesmo número de blocos da quebra
    original — é o caso das aberturas silabadas (SU MÁ RIO → ÍN DI CE)."""
    toks = es.split()
    if len(toks) != len(p['linhas']): return False
    base = p.get('fonte', 'HelveticaNeue')
    arq = None
    for cand in (base + 'ES', base):
        if cand in reg: arq = os.path.join(dirFontes, reg[cand]); break
    if not arq: return False
    for l, t in zip(p['linhas'], toks):
        page.insert_text((l['bbox'][0], l['spans'][0]['origin'][1]), t,
                         fontsize=p['tam'], fontfile=arq,
                         fontname='D' + re.sub(r'\W', '', base)[:12],
                         color=cor_rgb(p['cor']))
    return True

def aplica(page, paras, mapa, arch, reg, log, dirFontes='fontes'):
    paras, mapa, contornos = desdobra_contornos(page, paras, mapa, arch, reg)
    # 1) remove o texto original, preservando imagens
    red = []
    for p in paras:
        if p['tipo'] == 'numero_pagina': continue
        if p['id'] not in mapa: continue
        for l in p['linhas']:
            r = pymupdf.Rect(l['bbox'])
            red.append(r)
            page.add_redact_annot(r)
    guarda = preserva(page, paras, mapa, red, reg, dirFontes, log)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    redesenha(page, guarda, log)

    # títulos de display com entrelinha fechada: assentados linha por linha
    for p in paras:
        if (p['tipo'] == 'titulo_display' and p['id'] in mapa and mapa[p['id']]
                and p['entrelinha'] < p['tam'] * 1.05 and len(p['linhas']) > 1):
            if assenta_display(page, p, mapa[p['id']], reg, dirFontes):
                mapa = dict(mapa); mapa.pop(p['id'])
                log.append(dict(pagina=page.number+1, id=p['id'],
                                ajuste='display assentado linha por linha (entrelinha fechada)'))

    obs = obstaculos(page, paras)
    cols = colunas(paras, mapa)
    emFluxo = {p['id'] for c in cols for p in c}

    # 2) colunas de texto: o espanhol corre mais longo, então a coluna cresce
    #    para baixo até onde houver espaço livre, mantendo a 1ª linha de base.
    for col in cols:
        lim = limite_da_coluna(page, col, obs)
        limDir = {p['id']: limite_direita(page, p, obs, ignora=col) for p in col}
        pecasCont = [contornos[p['id']] for p in col if p['id'] in contornos]
        porId = {p['id']: p for p in col}
        def mapaDe(redEl, redPt):
            if not pecasCont or (not redEl and not redPt): return mapa
            m = dict(mapa)
            for c in pecasCont:
                if not all(i in porId for i in c['pecas']): continue
                m.update(reparte(page, [porId[i] for i in c['pecas']], c['texto'],
                                 arch, reg, redEl, redPt))
            return m
        pronto = None
        for redEl in (0, 0.02, 0.04, 0.06, MAX_RED_EL):
            for redPt in (0, 0.02, 0.04, MAX_RED_PT):
                mp2 = mapaDe(redEl, redPt)
                pronto = compoe_coluna(page, col, mp2, arch, reg, lim, limDir, redEl, redPt)
                if pronto:
                    if redEl or redPt:
                        log.append(dict(pagina=page.number+1, id=col[0]['id'],
                                        ajuste='coluna: entrelinha -%d%% corpo -%d%%'
                                               % (redEl*100, redPt*100)))
                    break
            if pronto: break
        if not pronto:
            # nem com a escada: mantém tudo alinhado e reduz SÓ o parágrafo que
            # não cabe, registrando quanto
            pronto = compoe_coluna(page, col, mapaDe(MAX_RED_EL, MAX_RED_PT), arch, reg,
                                   lim, limDir, MAX_RED_EL, MAX_RED_PT, tol=True)
            if not pronto:
                pronto = [(p, pymupdf.Rect(p['rect'].x0 - 1, p['rect'].y0 - 2,
                                           p['rect'].x1 + 2, p['rect'].y1 + 2),
                           html_de(mapa[p['id']], p['negrito']), css_de(p, reg), 0.0)
                          for p in col]
                log.append(dict(pagina=page.number+1, id=col[0]['id'],
                                erro='coluna recomposta na caixa original (último recurso)'))

        for p, rect, html, css, esc in pronto:
            # scale_low=0 SEMPRE na hora de assentar: a escada já escolheu o
            # corpo; deixar o htmlbox reduzir é o que garante que nunca se perde
            # texto. Qualquer redução real fica registrada abaixo.
            sobra, real = page.insert_htmlbox(rect, html, css=css, archive=arch,
                                              scale_low=0)
            if real < 0.999:
                log.append(dict(pagina=page.number+1, id=p['id'],
                                erro='reduzido pelo htmlbox para %.0f%% do corpo' % (real*100)))
            elif sobra < 0:
                log.append(dict(pagina=page.number+1, id=p['id'],
                                erro='TRANSBORDO — texto pode ter sido cortado'))

    # 3) elementos soltos (legendas, cabeçalhos, rótulos): caixa própria
    for p in paras:
        if p['id'] in emFluxo or p['id'] not in mapa or not mapa[p['id']]: continue
        html = html_de(mapa[p['id']], p['negrito'])
        ok = False
        for redEl in (0, 0.02, 0.04, 0.06, MAX_RED_EL):
            for redPt in (0, 0.02, 0.04, MAX_RED_PT):
                q = dict(p); q['entrelinha'] = p['entrelinha']*(1-redEl); q['tam'] = p['tam']*(1-redPt)
                css = css_de(q, reg)
                limP = limite_abaixo(page, p, paras)
                limD = (limite_direita(page, p, obs) if cresce_dir(p)
                        else p['rect'].x1 + 2)
                rect = pymupdf.Rect(p['rect'].x0 - 1, p['rect'].y0 - 2, limD, limP)
                b0, _b1, estourou, _esc = mede(page, rect, html, css, arch)
                if b0 is not None:
                    dy = p['base_y'] - b0
                    rect = pymupdf.Rect(rect.x0, rect.y0 + dy, rect.x1, limP)
                if p['tipo'] == 'titulo_display':
                    rect = pymupdf.Rect(rect.x0, rect.y0, rect.x1,
                                        max(rect.y1, p['rect'].y1 + 4))
                sobra, real = page.insert_htmlbox(rect, html, css=css, archive=arch,
                                                  scale_low=1)
                if sobra >= 0:
                    if redEl or redPt:
                        log.append(dict(pagina=page.number+1, id=p['id'],
                                        ajuste='entrelinha -%d%% corpo -%d%%' % (redEl*100, redPt*100)))
                    ok = True; break
                page.add_redact_annot(rect); page.apply_redactions(
                    images=pymupdf.PDF_REDACT_IMAGE_NONE,
                    graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
            if ok: break
        if not ok:
            css = css_de(p, reg)
            rect = pymupdf.Rect(p['rect'].x0 - 1, p['rect'].y0 - 2,
                                p['rect'].x1 + 2, p['rect'].y1 + 2)
            _, esc = page.insert_htmlbox(rect, html, css=css, archive=arch, scale_low=0)
            log.append(dict(pagina=page.number+1, id=p['id'],
                            erro='reduzido pelo htmlbox para %.0f%% do corpo' % (esc*100)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf'); ap.add_argument('mapa', nargs='?')
    ap.add_argument('--fontes', default='fontes')
    ap.add_argument('--saida', default='traduzido.pdf')
    ap.add_argument('--paginas', default='')
    ap.add_argument('--estrutura', action='store_true')
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    alvo = ([int(x) for x in a.paginas.split(',')] if a.paginas
            else list(range(1, doc.page_count+1)))

    if a.estrutura:
        out = {}
        for n in alvo:
            paras = agrupa(doc[n-1])
            for i, p in enumerate(paras): p['id'] = 'p%d_%02d' % (n, i)
            out[str(n)] = [dict(id=p['id'], tipo=p['tipo'], tam=p['tam'],
                                cor=hex(p['cor']), entrelinha=p['entrelinha'],
                                recuo=p['recuo'], base_y=round(p['base_y'],1),
                                base_y_fim=round(p['base_y_fim'],1),
                                rect=[round(v,1) for v in p['rect']],
                                negrito=p['negrito'], pt=p['texto']) for p in paras]
        print(json.dumps(out, ensure_ascii=False, indent=1)); return

    mapa = json.load(open(a.mapa, encoding='utf-8'))
    arch, reg = prepara_fontes(a.fontes)
    log = []
    for n in alvo:
        page = doc[n-1]
        paras = agrupa(page)
        for i, p in enumerate(paras): p['id'] = 'p%d_%02d' % (n, i)
        aplica(page, paras, mapa, arch, reg, log, a.fontes)
    doc.save(a.saida, garbage=3, deflate=True)
    print(json.dumps(dict(saida=a.saida, paginas=alvo, ajustes=log),
                     ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
