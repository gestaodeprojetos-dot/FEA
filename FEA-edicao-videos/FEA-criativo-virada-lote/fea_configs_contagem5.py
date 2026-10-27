"""FEA: criativos animados da contagem regressiva do Elite Injectors Congress (27/10/2026, pasta "5 dias congresso"),
no modelo da virada de lote. Congresso em 01 e 02/11 (domingo e segunda), WTC Sheraton, São Paulo; inscrições
encerradas (o Dr. fala no IMG_8244). Keila: "com uma musiquinha legal impactante e baixa" -> trilha 'epico' a 18%.
IMG_8241 e IMG_8242: 5 dias · IMG_8243: 4 dias · IMG_8244: 3 dias · IMG_8245: 2 dias.
Uso: python3 fea_configs_contagem5.py PASTA_TRANSCRICOES PASTA_SAIDA"""
import json, sys
from fea_configs_bf import K, LOGO_, SAIBA, G, GF, gerar, mapa

SUB = f'para o {G}Elite Injectors Congress{GF}'
def NUM(e, de, para, tflip, topo):
    return dict(tipo='gancho', s=0, e=e, modo='numero', de=str(de), para=str(para), tFlip=tflip, topo=topo, grande='dias', sub=SUB)
def PAL(s, e, itens): return dict(tipo='palestrantes', s=s, e=e, itens=[dict(t=t, html=h) for t, h in itens])
def ESG(s, e, t, b, carimbo): return dict(tipo='esgotado', s=s, e=e, tCarimbo=t, a='ELITE INJECTORS CONGRESS', b=b,
                                          c='01 E 02 DE NOVEMBRO · SÃO PAULO', carimbo=carimbo)
def FIM(s): return dict(tipo='final', s=s, rotulo='O CONGRESSO COMEÇA EM', grande='01/11', botao='TE VEJO LÁ')
DATA = '01 e 02 de novembro · São Paulo'
# imagens de apoio: vídeo "Visita técnica Elite Injectors (sem CTA)" (pasta 9- Visita técnica, Keila 27/10/2026).
# Tempos do bruto do Dr. (s, e) e do vídeo da visita (de). crop_h 1440 corta a legenda gravada na visita.
VISITA = '/tmp/claude-0/-home-user-FEA/1a096594-a9fd-570f-8a02-14d5ab643a70/scratchpad/visita/visita.mp4'
SALAO, LED, PALCO, MESAS, LED_GENTE, ESTRUTURA, SALA_VIP, STANDS = 6.0, 48.0, 56.0, 60.0, 70.0, 102.5, 12.0, 8.0
def INS(s, e, de): return dict(s=s, e=e, de=de)
TROCAS = [(['tô'], ['estou']), (['tá'], ['está']), (['pra'], ['para']), (['pro'], ['para', 'o']), (['para', 'gente'], ['para', 'a', 'gente'])]
def V(**k): return dict(publico='geral', cta=None, trilha='epico', vol_trilha=.18, trocas=TROCAS, **k)

VIDEOS = {
 'IMG_8241': V(inicio=.15, fim=11.9, inserts=[INS(7.65, 9.0, SALAO), INS(9.0, 10.4, MESAS)], zoom=[(5.6, 7.65), (9.0, 11.9)], cenas=[        # "Em cinco dias começa..."
    NUM(1.9, 6, 5, .5, 'EM'), LOGO_(1.85, 3.3),
    K(3.3, 5.6, 'aulas', 'O NOSSO CONGRESSO', 'Técnicas injetáveis', DATA),
    K(7.65, 9.0, 'cal', 'O LOCAL', 'WTC Sheraton', 'está incrível'),
    SAIBA(10.0, 11.3, 10.4), FIM(11.3)]),
 'IMG_8242': V(inicio=.3, fim=42.7, inserts=[INS(30.4, 33.4, ESTRUTURA), INS(37.0, 40.0, LED_GENTE)], zoom=[(2.9, 5.25), (5.25, 7.6), (21.6, 26.2), (30.4, 34.5), (37.0, 40.0)], cenas=[   # "5 dias para o..."
    NUM(1.45, 6, 5, .3, 'FALTAM'), LOGO_(1.45, 2.85),
    K(2.9, 5.25, 'aulas', 'O NOSSO CONGRESSO', 'Técnicas injetáveis', 'casos clínicos ao vivo'),
    PAL(7.65, 11.95, [(8.5, f'Os principais {G}palestrantes{GF}'), (10.4, 'Técnicas injetáveis')]),
    K(12.2, 16.1, 'valor', 'NO PALCO', 'O que vamos falar', '', [(12.3, 'Toxina botulínica'), (13.4, 'Preenchimento facial'),
                                                                  (14.4, 'Bioestimuladores'), (15.5, 'Fios')]),
    K(16.15, 21.6, 'aulas', 'ALÉM DA TÉCNICA', 'Marketing e vendas', 'para você crescer profissionalmente'),
    K(26.2, 30.4, 'sino', 'NO EVENTO', 'Live injection', '', [(28.0, 'Perguntas e respostas'), (29.8, 'Contato presencial')]),
    K(34.55, 37.0, 'cal', 'FALTAM', '5 dias', DATA),
    K(40.05, 41.15, 'cal', 'O LOCAL', 'São Paulo', 'WTC Sheraton'),
    SAIBA(39.9, 41.15, 40.3), FIM(41.15)]),
 'IMG_8243': V(inicio=0, fim=50.45, inserts=[INS(40.3, 43.4, PALCO), INS(43.4, 46.4, MESAS)], remover=[('meu', 16.0)], zoom=[(3.2, 5.95), (12.6, 15.9), (19.1, 23.6), (28.6, 31.0), (40.3, 46.4)], cenas=[  # "4 dias para começar"
    NUM(2.0, 5, 4, .35, 'FALTAM'), LOGO_(1.95, 3.2),
    K(5.95, 8.5, 'sino', 'EM 4 DIAS', 'Todas as novidades', 'do mundo dos injetáveis'),
    K(8.55, 12.6, 'aulas', 'BASEADO EM CIÊNCIA', 'O que é relevante', 'para usar no seu consultório'),
    K(15.95, 19.05, 'valor', 'O QUE SAIU DE NOVO', 'Produtos e técnicas', '', [(17.0, 'Produtos novos'), (18.1, 'Técnicas novas')]),
    PAL(23.6, 28.55, [(24.4, f'Os principais {G}palestrantes{GF}'), (25.9, 'O que eles usam no dia a dia')]),
    K(31.0, 34.4, 'aulas', 'NÃO É SÓ', 'Demonstração e marketing', ''),
    K(34.45, 40.3, 'valor', 'NO ELITE', 'Saber o que usar', 'e os pulos do gato'),
    K(46.45, 49.2, 'cal', 'FALTAM', '4 dias', DATA),
    SAIBA(47.9, 49.25, 48.3), FIM(49.25)]),
 'IMG_8244': V(inicio=.25, fim=42.85, inserts=[INS(6.7, 12.6, LED), INS(13.7, 15.6, SALA_VIP), INS(17.0, 19.6, STANDS), INS(37.5, 41.0, LED_GENTE)], zoom=[(2.9, 5.0), (12.65, 13.7), (19.6, 24.0), (27.35, 31.3), (31.3, 35.1)], cenas=[  # "Apenas três dias"
    NUM(1.75, 4, 3, .95, 'APENAS'), LOGO_(1.75, 2.9),
    K(5.05, 12.65, 'cal', 'O LOCAL', 'WTC Sheraton', 'São Paulo', [(7.4, 'Aquário no meio'), (8.9, '2 telões de LED'), (11.6, 'Ambiente gigante')]),
    K(13.7, 19.6, 'presente', 'ESTRUTURA', 'Super evento', '', [(13.9, 'Sala VIP'), (17.2, 'Patrocinadores'), (18.9, 'Produtos')]),
    ESG(24.05, 27.35, 25.4, 'Inscrições', 'ENCERRADAS'),
    LOGO_(35.1, 36.4),
    K(36.45, 41.3, 'cal', 'SÃO PAULO', 'WTC Sheraton', '01 e 02 de novembro'),
    SAIBA(40.0, 41.35, 40.4), FIM(41.35)]),
 'IMG_8245': V(inicio=0, fim=36.65, inserts=[INS(8.75, 12.4, PALCO), INS(12.4, 15.1, SALAO)], cortes=[(30.3, 31.35)], zoom=[(2.75, 5.0), (8.75, 12.4), (12.4, 15.15), (19.5, 22.45)], cenas=[  # "Em dois dias começa"
    NUM(1.55, 3, 2, .35, 'EM'), LOGO_(1.55, 2.75),
    K(5.0, 8.75, 'presente', 'VAI SER', 'Imperdível', '', [(7.9, 'Inesquecível')]),
    K(15.15, 19.5, 'aulas', 'NO ELITE', 'Você vai aprender', 'e levar muita coisa para casa'),
    K(22.5, 28.9, 'aulas', 'DE VERDADE', 'Atualização real', '', [(24.3, 'Atualizar'), (25.6, 'Aprender de fato'), (27.2, 'Solidificar o conhecimento')]),
    K(31.4, 33.5, 'cal', 'EM APENAS', '2 dias', DATA),
    LOGO_(33.9, 35.0),
    SAIBA(35.6, 36.65, 35.9),
    FIM(36.4)]),
}

if __name__ == '__main__':
    tr, saida = sys.argv[1], sys.argv[2]
    gerar(VIDEOS, tr, saida)
    for nome in VIDEOS:     # cartela final fica 2 s depois da última palavra (como na virada de lote)
        p = f'{saida}/{nome}.json'; c = json.load(open(p))
        v = VIDEOS[nome]; f = mapa(v.get('inicio', 0), v.get('cortes', []))
        c['inserts'] = [dict(s=f(x['s']), e=f(x['e']), de=x['de'], src=VISITA, crop_h=1440) for x in v.get('inserts', [])]
        c['dur'] = round(c['dur'] + 2.0, 2); c.pop('tema', None); c.pop('logo', None); c.pop('cursos', None)
        for g in c['legendas']:
            for a, b in zip(g['w'], g['w'][1:]):
                if a['t'] == 'QUISER' and b['t'] == 'SAIBA MAIS': b['t'] = 'SABER MAIS'
        json.dump(c, open(p, 'w'), ensure_ascii=False, indent=1)
