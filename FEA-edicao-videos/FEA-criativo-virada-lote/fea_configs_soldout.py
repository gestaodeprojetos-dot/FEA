"""FEA: criativo animado "Sold out" do Elite Injectors Congress (26/10/2026), no modelo da virada de lote
(Keila: "eu quero esse modelo", pasta FEA-Elite-virada-de-lote). Bruto IMG_8181 (pasta "Sold out elite congress").
Versão curta: abertura (ingressos esgotados), palestrantes e temas, e o convite para a próxima edição.
Tempos na linha do tempo do bruto. Fatos da página el.joaopithon.com.br/elite-injectors-congress/:
01 e 02/11, WTC Sheraton, São Paulo, 11 palestrantes nos cards (o Dr. fala "12 grandes palestrantes").
Uso: python3 fea_configs_soldout.py PASTA_TRANSCRICOES PASTA_SAIDA"""
import json, sys
from fea_configs_bf import K, LOGO_, SAIBA, G, GF, gerar, mapa
from fea_configs_contagem5 import VISITA, PALCO, MESAS, LED_GENTE, INS

def ESG(s, e, tCarimbo): return dict(tipo='esgotado', s=s, e=e, tCarimbo=tCarimbo, a='ELITE INJECTORS CONGRESS',
                                     b='Ingressos', c='01 E 02 DE NOVEMBRO · SÃO PAULO', carimbo='ESGOTADO')
def PAL(s, e, itens): return dict(tipo='palestrantes', s=s, e=e, itens=[dict(t=t, html=h) for t, h in itens])

VIDEOS = {
 'IMG_8181': dict(publico='geral', cta=None, trilha='epico', vol_trilha=.2, inicio=0, fim=109.0,
   cortes=[(8.68, 24.98), (39.7, 88.7)],
   trocas=[(['para', 'gente'], ['para', 'a', 'gente']), (['para', 'edição'], ['para', 'a', 'edição'])],
   zoom=[(3.6, 4.7), (29.15, 31.8), (88.7, 90.95), (100.6, 102.6)],
   inserts=[INS(29.15, 31.8, PALCO), INS(88.7, 90.95, MESAS), INS(100.6, 102.6, LED_GENTE)],
   cenas=[
    K(0, 2.45, 'sino', 'COMUNICADO', 'Elite Injectors Congress', '01 e 02 de novembro'),
    LOGO_(2.45, 3.6),
    ESG(4.7, 8.68, 7.45),
    PAL(25.0, 29.15, [(26.6, f'Grandes {G}palestrantes{GF}'), (27.8, 'Trazendo as suas técnicas')]),
    K(31.8, 35.6, 'valor', 'NO PALCO', 'Técnicas injetáveis', '', [(31.9, 'Preenchimento'), (32.5, 'Toxina'), (33.4, 'Fios'),
                                                                    (33.9, 'Bioestimuladores'), (34.8, 'Tecnologias')]),
    K(35.65, 39.7, 'cal', 'PRESENCIAL', '2 dias de atualizações', '', [(38.0, 'Casos clínicos ao vivo')]),
    K(91.0, 96.65, 'aluno', 'PRÓXIMA EDIÇÃO', 'Muitos já garantiram a vaga', 'do ano que vem'),
    SAIBA(96.65, 99.1, 97.4),
    LOGO_(99.1, 100.6),
    K(102.6, 106.5, 'valor', 'ELITE INJECTORS CONGRESS', f'Tendências científicas', f'com {G}evidências reais{GF}'),
    dict(tipo='final', s=107.6, rotulo='INGRESSOS 2026', grande='Esgotados', botao='PRÓXIMA EDIÇÃO'),
   ]),
}

if __name__ == '__main__':
    tr, saida = sys.argv[1], sys.argv[2]
    gerar(VIDEOS, tr, saida)
    for nome in VIDEOS:     # cartela final fica 2 s depois da última palavra (como na virada de lote)
        p = f'{saida}/{nome}.json'; c = json.load(open(p))
        v = VIDEOS[nome]; f = mapa(v.get('inicio', 0), v.get('cortes', []))
        c['inserts'] = [dict(s=f(x['s']), e=f(x['e']), de=x['de'], src=VISITA, crop_h=1440) for x in v.get('inserts', [])]
        c['dur'] = round(c['dur'] + 2.0, 2); c.pop('tema', None); c.pop('logo', None); c.pop('cursos', None)
        # "se você quiser saber mais" é o verbo, não o botão: o palavras() trocava por "SAIBA MAIS"
        for g in c['legendas']:
            for a, b in zip(g['w'], g['w'][1:]):
                if a['t'] == 'QUISER' and b['t'] == 'SAIBA MAIS': b['t'] = 'SABER MAIS'
        json.dump(c, open(p, 'w'), ensure_ascii=False, indent=1)
        print(nome, 'dur', c['dur'])
