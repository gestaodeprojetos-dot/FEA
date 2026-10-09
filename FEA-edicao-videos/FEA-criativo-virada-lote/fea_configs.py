"""FEA: roteiro de cenas de cada vídeo da virada de lote (Elite Injectors Congress).
Gera um JSON por vídeo (cenas + legendas + zoom + duração) para a composição e o áudio.
Uso: python3 fea_configs.py PASTA_TRANSCRICOES PASTA_SAIDA"""
import json, re, sys

FRACAS = {'de', 'do', 'da', 'dos', 'das', 'o', 'a', 'os', 'as', 'em', 'e', 'que', 'para', 'no', 'na', 'nos',
          'se', 'um', 'uma', 'com', 'antes', 'mais', 'te', 'eu', 'vai', 'é', 'à', 'ao', 'sua', 'tua', 'esse'}
TROCAS = {'pra': 'para', 'mediano': 'mediando', 'sabamais': 'SAIBA MAIS'}

def palavras(trans):
    ws = [dict(t=w['w'].strip(), s=w['s'], e=w['e']) for s in trans for w in s['words']]
    out = []
    i = 0
    while i < len(ws):
        w = dict(ws[i]); base = re.sub(r'[^\wÀ-ú]', '', w['t']).lower()
        pont = re.search(r'[,.!?]$', w['t'])
        if base == 'ó':
            i += 1; continue
        if base in ('saba', 'saiba') and i + 1 < len(ws) and re.sub(r'[^\wÀ-ú]', '', ws[i + 1]['t']).lower() == 'mais':
            w['t'] = 'SAIBA MAIS'; w['e'] = ws[i + 1]['e']; pont = re.search(r'[,.!?]$', ws[i + 1]['t']); i += 1
        elif base in TROCAS:
            w['t'] = TROCAS[base]
        else:
            w['t'] = re.sub(r'[,.!?]$', '', w['t'])
        w['fim'] = bool(pont)
        out.append(w); i += 1
    return out

BLOCOS = [['elite', 'injectors', 'congress'], ['elite', 'injectors'], ['injectors', 'congress'], ['são', 'paulo'], ['sold', 'out'],
          ['te', 'vejo', 'lá'], ['até', 'lá'], ['harmonização', 'facial'], ['casos', 'clínicos'], ['ao', 'vivo'],
          ['agora', 'mesmo'], ['mais', 'caro'], ['mais', 'barato'], ['de', 'lote'], ['o', 'lote'], ['espero', 'vocês', 'lá'], ['4', 'dias'], ['três', 'dias'], ['dois', 'dias']]

def unidades(ws):
    out, i = [], 0
    low = [re.sub(r'[^\wÀ-ú ]', '', w['t']).lower() for w in ws]
    while i < len(ws):
        for bl in BLOCOS:
            n = len(bl)
            if low[i:i + n] == bl and not any(w['fim'] for w in ws[i:i + n - 1]):
                out.append(ws[i:i + n]); i += n; break
        else:
            out.append([ws[i]]); i += 1
    return out

def agrupar(ws):
    us = unidades(ws)
    tx = lambda g: ' '.join(w['t'] for u in g for w in u)
    grupos, cur = [], []
    for k, u in enumerate(us):
        prox = us[k + 1] if k + 1 < len(us) else None
        artigo = len(u) == 1 and u[0]['t'].lower() in ('o', 'a') and prox and len(prox) > 1
        if cur and (len(tx(cur + [u])) > (26 if len(u) > 1 else 22) or artigo):
            grupos.append(cur); cur = []
        cur.append(u)
        ult = u[-1]
        fraca = ult['t'].lower() in FRACAS or re.fullmatch(r'\d+', ult['t'])
        if ult['fim'] or (len(tx(cur)) >= 13 and not fraca):
            grupos.append(cur); cur = []
    if cur: grupos.append(cur)
    # grupo órfão curto (ex.: "LÁ", "MESMO") volta para o anterior
    final = []
    for g in grupos:
        if final and len(tx(g)) <= 5 and len(tx(final[-1] + g)) <= 26 and g[0][0]['s'] - final[-1][-1][-1]['e'] < .6:
            final[-1] = final[-1] + g
        else:
            final.append(g)
    leg = []
    for g in final:
        ws_ = [w for u in g for w in u]
        leg.append(dict(s=ws_[0]['s'], e=ws_[-1]['e'] + .25, w=[dict(t=x['t'].upper(), s=x['s'], e=x['e']) for x in ws_]))
    for a, b in zip(leg, leg[1:]): a['e'] = min(a['e'], b['s'])
    return leg

SUB_LOTE = 'para a virada<br>de <span class="goldtxt" style="font-weight:800">lote</span>'
def gancho_num(e, de, para, tflip, topo='FALTAM'):
    return dict(tipo='gancho', s=0, e=e, modo='numero', de=str(de), para=str(para), tFlip=tflip, topo=topo, grande='dias', sub=SUB_LOTE)
DATA = dict(t=0, html='01 e 02 de <span class="goldtxt">novembro</span>', icone='cal')
LOCAL = dict(t=0, html='WTC Sheraton · <span style="color:var(--teal)">São Paulo</span>', icone='pin')
def chip(base, t): d = dict(base); d['t'] = t; return d

VIDEOS = {
 'IMG_7584': dict(contador='04 : 01', fim_fala=23.45, zoom=[(4.36, 7.22), (15.0, 16.6), (19.7, 22.68)], cenas=[
    gancho_num(2.62, 5, 4, .62), dict(tipo='logo', s=2.45, e=4.38),
    dict(tipo='celular', s=7.22, e=10.82, chips=[chip(DATA, 8.0), chip(LOCAL, 9.72)]),
    dict(tipo='lote', s=10.8, e=15.05, modo='barato', tSub=13.82), dict(tipo='saiba', s=15.0, e=16.62, tToque=15.84),
    dict(tipo='virada', s=16.58, e=19.66, de=10, ate=14, tCal=17.28, tFlip=17.95, tCarimbo=18.5),
    dict(tipo='lote', s=19.7, e=22.72, modo='poucas'), dict(tipo='final', s=22.68)]),
 'IMG_7586': dict(contador='04 : 01', fim_fala=23.4, zoom=[(4.7, 8.45), (15.2, 17.25)], cenas=[
    gancho_num(3.1, 5, 4, .45, 'EM'), dict(tipo='logo', s=3.05, e=4.68),
    dict(tipo='lote', s=8.45, e=12.3, modo='barato', sub='o menor valor', tSub=9.3),
    dict(tipo='virada', s=12.3, e=15.15, de=10, ate=14, tCal=13.1, tFlip=14.3, tCarimbo=14.85),
    dict(tipo='lote', s=15.2, e=17.25, modo='poucas'), dict(tipo='saiba', s=17.25, e=19.35, tToque=18.6),
    dict(tipo='celular', s=19.35, e=22.0, chips=[chip(DATA, 19.9), chip(LOCAL, 20.9)]), dict(tipo='final', s=21.95)]),
 'IMG_7587': dict(contador='03 : 01', fim_fala=27.6, zoom=[(3.45, 5.85), (13.2, 16.65), (22.0, 24.25)], cenas=[
    gancho_num(2.05, 4, 3, .45, 'EM'), dict(tipo='logo', s=2.0, e=3.45),
    dict(tipo='palestrantes', s=5.85, e=10.35, itens=[dict(t=6.2, html='Todas as atualizações'), dict(t=7.6, html='Técnicas ao vivo'),
        dict(t=9.0, html='Os principais <span class="goldtxt">palestrantes</span>')]),
    dict(tipo='saiba', s=16.65, e=17.9, tToque=17.4),
    dict(tipo='virada', s=17.9, e=21.95, de=11, ate=14, tCal=18.4, tFlip=19.45, tCarimbo=20.7),
    dict(tipo='lote', s=22.0, e=24.25, modo='poucas'), dict(tipo='saiba', s=24.25, e=25.35, tToque=24.7),
    dict(tipo='final', s=25.35)]),
 'IMG_7588': dict(contador='02 : 01', fim_fala=33.0, zoom=[(3.55, 6.05), (17.55, 21.65), (30.0, 32.25)], cenas=[
    gancho_num(3.55, 3, 2, .85, 'FALTAM'), dict(tipo='logo', s=6.05, e=7.25),
    dict(tipo='palestrantes', s=9.85, e=17.55, itens=[dict(t=10.8, html='Casos clínicos ao vivo'), dict(t=13.5, html='Rodas de conversa'),
        dict(t=15.0, html='Os principais <span class="goldtxt">palestrantes</span>')]),
    dict(tipo='celular', s=21.65, e=26.15, rolar=240, chips=[chip(DATA, 22.4), chip(LOCAL, 24.2)]),
    dict(tipo='virada', s=26.15, e=28.65, de=12, ate=14, tCal=26.5, tFlip=27.2, tCarimbo=27.9),
    dict(tipo='saiba', s=28.65, e=31.15, tToque=29.2), dict(tipo='lote', s=30.0, e=32.25, modo='poucas'),
    dict(tipo='final', s=32.25)]),
 'IMG_7589': dict(contador='02 : 01', fim_fala=20.0, zoom=[(3.25, 5.25), (9.75, 12.55)], cenas=[
    gancho_num(1.9, 3, 2, .1), dict(tipo='logo', s=1.85, e=3.25),
    dict(tipo='palestrantes', s=5.25, e=9.75, itens=[dict(t=6.0, html='Tendências científicas'), dict(t=7.8, html='Procedimentos de <span class="goldtxt">harmonização</span>')]),
    dict(tipo='saiba', s=14.75, e=15.6, tToque=15.2),
    dict(tipo='virada', s=15.55, e=18.75, de=12, ate=14, tCal=15.95, tFlip=16.95, tCarimbo=17.6),
    dict(tipo='final', s=18.7)]),
 'IMG_7590': dict(contador='02 : 01', fim_fala=29.5, zoom=[(3.25, 5.95), (12.75, 16.45)], cenas=[
    gancho_num(1.9, 3, 2, .1), dict(tipo='logo', s=1.85, e=3.25),
    dict(tipo='saiba', s=5.95, e=8.95, tToque=8.3),
    dict(tipo='virada', s=8.95, e=12.75, de=12, ate=14, tCal=10.5, tFlip=11.2, tCarimbo=12.0),
    dict(tipo='lote', s=16.45, e=21.45, modo='poucas'),
    dict(tipo='palestrantes', s=21.45, e=27.65, itens=[dict(t=22.8, html='Os principais <span class="goldtxt">palestrantes</span>'),
        dict(t=25.0, html='Casos clínicos presenciais'), dict(t=26.3, html='Ao vivo')]),
    dict(tipo='final', s=27.6)]),
 'IMG_7591': dict(contador='01 : 01', fim_fala=26.2, rotulo='O 1º LOTE VIRA AMANHÃ', zoom=[(3.55, 6.35), (19.75, 24.35)], cenas=[
    dict(tipo='gancho', s=0, e=2.3, modo='calendario', de=13, para=14, tFlip=.3, topo='A VIRADA DE LOTE É', grande='amanhã',
         sub='quarta, <span class="goldtxt" style="font-weight:800">14/10</span>'),
    dict(tipo='logo', s=2.25, e=3.55),
    dict(tipo='celular', s=6.35, e=9.65, contador='01 : 01', chips=[dict(t=8.3, html='O menor <span class="goldtxt">valor possível</span>', icone='tag'), chip(DATA, 9.0)]),
    dict(tipo='saiba', s=9.65, e=12.05, tToque=11.3), dict(tipo='lote', s=12.05, e=16.25, modo='barato', sub='valores especiais', tSub=13.9),
    dict(tipo='virada', s=16.25, e=19.75, de=13, ate=14, tCal=16.9, tFlip=17.6, tCarimbo=18.6, carimbo='ÚLTIMA CHANCE'),
    dict(tipo='final', s=24.35)]),
 'IMG_7593': dict(contador='00 : 09', fim_fala=32.0, rotulo='O 1º LOTE VIRA HOJE', zoom=[(13.85, 16.25), (17.85, 20.0)], cenas=[
    dict(tipo='gancho', s=0, e=2.7, modo='calendario', de=14, para=14, tFlip=99, alerta=True, topo='A VIRADA DE LOTE É', grande='hoje',
         sub='quarta, <span class="goldtxt" style="font-weight:800">14/10</span>'),
    dict(tipo='logo', s=2.65, e=4.35),
    dict(tipo='virada', s=4.35, e=7.45, de=14, ate=14, tCal=4.5, tFlip=4.9, tCarimbo=5.45),
    dict(tipo='saiba', s=7.45, e=9.35, tToque=8.8), dict(tipo='lote', s=9.35, e=13.85, modo='barato', sub='o valor mais barato', tSub=12.1),
    dict(tipo='saiba', s=16.25, e=17.85, tToque=16.6),
    dict(tipo='celular', s=20.0, e=22.55, chips=[chip(DATA, 20.3), chip(LOCAL, 21.6)]),
    dict(tipo='palestrantes', s=22.55, e=29.95, itens=[dict(t=22.65, html='Casos clínicos ao vivo'), dict(t=24.1, html='Presencial'),
        dict(t=27.1, html='Os principais <span class="goldtxt">nomes</span>')]),
    dict(tipo='final', s=29.95)]),
}

if __name__ == '__main__':
    tr, saida = sys.argv[1], sys.argv[2]
    for nome, v in VIDEOS.items():
        trans = json.load(open(f'{tr}/{nome}.json'))
        leg = agrupar(palavras(trans))
        for c in v['cenas']:
            if c['tipo'] == 'celular': c.setdefault('contador', v['contador'])
            if c['tipo'] == 'final' and v.get('rotulo'): c['rotulo'] = v['rotulo']
        cfg = dict(nome=nome, dur=round(v['fim_fala'] + 2.3, 2), fim_fala=v['fim_fala'], zoom=v['zoom'], cenas=v['cenas'], legendas=leg)
        json.dump(cfg, open(f'{saida}/{nome}.json', 'w'), ensure_ascii=False, indent=1)
        print(nome, cfg['dur'], '|', ' / '.join(' '.join(w['t'] for w in g['w']) for g in leg))
