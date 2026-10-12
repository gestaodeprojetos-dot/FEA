"""FEA: roteiros dos criativos da Black Friday Vitalícia (out/2026), no mesmo motor do criativo de virada de lote.
Tempos escritos na linha do tempo do bruto; `inicio` corta o silêncio do começo e tudo é deslocado.
Fatos da página bf.joaopithon.com.br/black-vitalicia-d/: live de abertura 20/10 às 20h, todos os cursos para
sempre por um único preço, 20 formações/cursos/imersões/livros, oferta especial para alunos.
Uso: python3 fea_configs_bf.py PASTA_TRANSCRICOES PASTA_SAIDA [NOME ...]"""
import json, sys
from fea_configs import palavras, agrupar

CURSOS = [f'card-{n}.png' for n in ('FEP', 'FEB', 'FEF', 'FEC', 'FEA2', 'FEBIO2', 'pos', 'elite', 'iar', 'ipl', 'iff52',
                                    'iff102', 'ipo', 'atsd', 'complicacoes', 'ebook1', 'ebook2', 'ctx', 'plxx', 'CPX')]
LOGO = dict(src='logo-bf.png', w=880, h=307, top=600,
            tag='Todos os meus cursos, <b style="color:var(--teal)">para sempre.</b>')
CTA = 'cta.mp4'

VIDEOS = {
 'alunos': dict(inicio=.8, fim=35.6, zoom=[(9.7, 11.7), (26.0, 27.85), (34.4, 35.6)], tremor=[(.9, 2.1)],
   sem_legenda=[(.8, 2.1)], cenas=[
    dict(tipo='alerta', s=.8, e=2.1, tA=1.0, tB=1.5),
    dict(tipo='cartao', s=2.1, e=4.2, icone='aluno', topo='EXCLUSIVO', titulo='Para os meus alunos',
         sub='uma oferta especial na Black Friday Vitalícia'),
    dict(tipo='logo', s=4.2, e=5.75),
    dict(tipo='cartao', s=5.8, e=9.65, icone='inf', topo='BLACK FRIDAY VITALÍCIA', titulo='Acesso vitalício',
         sub='todos os cursos, para sempre, por um único preço'),
    dict(tipo='cartao', s=11.7, e=15.7, icone='presente', topo='NA ABERTURA DAS INSCRIÇÕES', titulo='Bônus exclusivos',
         chips=[dict(t=11.8, html='Bônus presenciais'), dict(t=13.8, html='Pós-graduação incluída')]),
    dict(tipo='cursos', s=15.75, e=20.75, itens=[dict(t=15.8, html='Todos os cursos que já criei'),
         dict(t=17.4, html='E os que <span class="goldtxt">ainda vou lançar</span>'), dict(t=19.3, html='Atualizações vitalícias')]),
    dict(tipo='cartao', s=20.8, e=25.95, icone='valor', topo='UM ÚNICO VALOR', titulo='Nenhum real a mais',
         sub='nem para atualizações, nem para extras'),
    dict(tipo='saiba', s=27.85, e=29.25, tToque=28.3),
    dict(tipo='live', s=29.25, e=34.4, tVivo=29.95, tData=30.5, tHora=30.8, tTexto=31.5,
         texto='Abertura oficial das inscrições<br><span class="goldtxt">no Instagram do Dr. João Pithon</span>'),
 ]),
}

TEMPOS = ('s', 'e', 't', 'tA', 'tB', 'tFlip', 'tCal', 'tCarimbo', 'tToque', 'tSub', 'tVivo', 'tData', 'tHora', 'tTexto')

def deslocar(obj, d):
    if isinstance(obj, list): return [deslocar(x, d) for x in obj]
    if isinstance(obj, dict):
        return {k: (round(v - d, 3) if k in TEMPOS and isinstance(v, (int, float)) else deslocar(v, d)) for k, v in obj.items()}
    return obj

if __name__ == '__main__':
    tr, saida = sys.argv[1], sys.argv[2]
    nomes = sys.argv[3:] or list(VIDEOS)
    for nome in nomes:
        v = VIDEOS[nome]; d = v['inicio']
        leg = agrupar(palavras(json.load(open(f'{tr}/{nome}.json'))))
        leg = [g for g in leg if g['e'] > d]
        cfg = dict(nome=nome, tema='bf', logo=LOGO, cursos=CURSOS, cta=CTA, inicio=d,
                   dur=round(v['fim'] - d, 2), fim_fala=round(v['fim'] - d - .2, 2),
                   zoom=[(round(a - d, 2), round(b - d, 2)) for a, b in v['zoom']],
                   tremor=[(round(max(0, a - d), 2), round(b - d, 2)) for a, b in v.get('tremor', [])],
                   sem_legenda=[(round(a - d, 2), round(b - d, 2)) for a, b in v.get('sem_legenda', [])],
                   cenas=deslocar(v['cenas'], d), legendas=deslocar(leg, d))
        json.dump(cfg, open(f'{saida}/{nome}.json', 'w'), ensure_ascii=False, indent=1)
        print(nome, cfg['dur'], '|', ' / '.join(' '.join(w['t'] for w in g['w']) for g in cfg['legendas']))
