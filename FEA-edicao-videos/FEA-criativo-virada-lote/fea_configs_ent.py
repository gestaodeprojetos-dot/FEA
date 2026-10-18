"""FEA: roteiros das entrevistas "mito ou verdade" na prática clínica (18/10/2026, pasta "Vídeos entrevistas FEP").
Conteúdo de Instagram (2. INSTAGRAM > 0 2026 > 10- Outubro), sem CTA no fim. Kit de entrevista no padrão PITHON NEWS
da equipe: manchete de portal, faixa AO VIVO, tarja de nome, card de pergunta com microfone, card de citação.
Trilha e efeitos variam de um vídeo para o outro (Keila: "altere os sons entre os vídeos").
Os tempos das cenas saem das próprias falas (T = início da frase na transcrição), não de números soltos.
Uso: python3 fea_configs_ent.py PASTA_TRANSCRICOES PASTA_SAIDA [NOME ...]"""
import json, re, sys
from fea_configs_bf import LOGO_, SAIBA, CURSOS_, LIVE, G, GF, gerar

TR = sys.argv[1] if len(sys.argv) > 1 else '.'
_cache = {}
def _ws(nome):
    if nome not in _cache:
        d = json.load(open(f'{TR}/{nome}.json'))
        _cache[nome] = [(re.sub(r'[^\wÀ-ú]', '', w['w']).lower(), w['s'], w['e']) for s in d for w in s['words']]
    return _cache[nome]
def _acha(nome, frase, depois):
    ws = _ws(nome); alvo = [re.sub(r'[^\wÀ-ú]', '', x).lower() for x in frase.split()]
    for i in range(len(ws) - len(alvo) + 1):
        if ws[i][1] >= depois and [w[0] for w in ws[i:i + len(alvo)]] == alvo: return i, i + len(alvo) - 1
    raise ValueError(f'{nome}: frase não encontrada: {frase!r}')
def T(nome, frase, depois=0):  # início da frase
    i, _ = _acha(nome, frase, depois); return _ws(nome)[i][1]
def TE(nome, frase, depois=0):  # fim da frase
    _, j = _acha(nome, frase, depois); return _ws(nome)[j][2]
def FIM(nome):
    return _ws(nome)[-1][2]

ALUNOS = dict(a='NA PRÁTICA', b='Alunos e monitores', c='Formação Especialista em Preenchimento')
DR = dict(a='ESPECIALISTA', b='Dr. João Pithon', c='')
TRILHAS = ['groove', 'tensao', 'pulsante', 'brilho', 'epico']      # sem "urgência": é conteúdo, não oferta
SONS = ['tv', 'digital', 'radio']

def entrevista(k, nome, hl, q_fim, cat='MITO OU VERDADE', resp=None, dr=None, quem_resp=ALUNOS, perguntas=(), cit=None,
               final=None, fim=None, extra=(), primeiro=None):
    fim = fim or FIM(nome) + .6
    cenas = [dict(tipo='manchete', s=0, e=q_fim + .35, cat=cat, hl=hl, meta='Entrevista na prática clínica · Dr. João Pithon',
                  tDig=min(1.4, max(.7, q_fim - 1.2))),
             dict(tipo='aovivo', s=q_fim + .35, e=fim, tag=cat)]
    if primeiro: cenas.append(dict(tipo='tarja', s=primeiro, e=primeiro + 3.2, **DR))
    if resp is not None: cenas.append(dict(tipo='tarja', s=resp, e=resp + 3.4, **quem_resp))
    if dr is not None: cenas.append(dict(tipo='tarja', s=dr, e=dr + 3.4, **DR))
    for s, e, q in perguntas: cenas.append(dict(tipo='pergunta', s=s, e=e, q=q))
    if cit: cenas.append(dict(tipo='citacao', s=cit[0], e=cit[1], texto=cit[2], quem=cit[3] if len(cit) > 3 else 'Dr. João Pithon'))
    if final is not None: cenas.append(dict(tipo='pergunta', s=final, e=fim, h='E VOCÊ?', q=f'Mito ou verdade? {G}Comenta aqui{GF}' if cat == 'MITO OU VERDADE' else f'Qual a sua opinião? {G}Comenta aqui{GF}'))
    cenas += list(extra)
    return dict(publico='geral', cta=None, trilha=TRILHAS[k % len(TRILHAS)], vol_trilha=.13, sons=SONS[k % len(SONS)],
                inicio=0, fim=fim, zoom=[], cenas=cenas)

# grafia das marcas e termos que o Whisper erra (as marcas ficam na fala do Dr.: precisam de aprovação, ver resumo)
TROCAS = [(['cima', 'a', 'mais'], ['Saiba', 'Mais']), (['rhinomodelação'], ['rinomodelação']), (['pros'], ['para', 'os']), (['revaneskis'], ['Revanesse']), (['neuromis'], ['Neuramis']), (['neuromys'], ['Neuramis']), (['neuronis'], ['Neuramis']),
          (['jeep'], ['Deep']), (['resilane'], ['Restylane']), (['letibol'], ['Letybo']), (['dispult'], ['Dysport']),
          (['zelmen'], ['Xeomin']), (['profilo'], ['Profhilo']), (['biogealiz'], ['Biogelis']), (['cândula'], ['cânula']),
          (['arteiras'], ['artérias']), (['assegurança'], ['a', 'segurança']), (['perdo'], ['perda']), (['superbitária'], ['supraorbitária']),
          (['bigotinês'], ['bigode', 'chinês']), (['suco', 'naslobial'], ['sulco', 'nasolabial']), (['rosteiro'], ['rosto', 'inteiro']),
          (['reino', 'de', 'modulação'], ['rinomodelação']), (['o', 'reino', 'de', 'modulação'], ['a', 'rinomodelação']),
          (['biostimuladores'], ['bioestimuladores']), (['m', 'face'], ['hemiface']), (['e', 'voar', 'contou'], ['Ivoire', 'Contour']),
          (['ivoar'], ['Ivoire']), (['e', 'voar'], ['Ivoire']), (['renova'], ['Rennova']), (['consentimento'], ['consenso'])]

def _videos():
    V = {}
    n = 'IMG_7828'; V[n] = entrevista(0, n, 'Olheiras com agulha: técnica ultrapassada?', TE(n, 'ou não?'),
        resp=T(n, 'Técnica ultrapassada. Por'), dr=T(n, 'Pronto, ele tem'), cit=(T(n, 'aumenta muito'), TE(n, 'hematomas') + .6, 'A agulha aumenta muito a incidência de hematomas'),
        final=T(n, 'E você?'))
    n = 'IMG_7830'; V[n] = entrevista(1, n, 'Olheiras com agulha: técnica ultrapassada?', TE(n, 'mito ou verdade?'),
        resp=T(n, 'Verdade.'), cit=(T(n, 'a melhor técnica'), TE(n, 'mais natural.'), 'A melhor técnica é com cânula: mais segura e mais natural', 'Resposta na prática clínica'),
        final=FIM(n) - .3)
    n = 'IMG_7831'; f = TE(n, 'sem dúvida.') + .6
    V[n] = entrevista(2, n, 'Rinomodelação só com agulha: técnica ultrapassada?', TE(n, 'mito ou verdade?'), fim=f,
        resp=T(n, 'Verdade. Verdade.'), cit=(T(n, 'na agulha'), TE(n, 'tridimensional,'), 'Na agulha você não consegue entregar o preenchimento tridimensional', 'Resposta na prática clínica'),
        final=T(n, 'Ultrapassado. Ultrapassado.'))
    n = 'IMG_7833'; V[n] = entrevista(3, n, 'Rinomodelação só com agulha: técnica ultrapassada?', TE(n, 'verdade?'),
        resp=T(n, 'Verdade.'), dr=T(n, 'assegurança'),
        perguntas=[(T(n, 'é proibido'), TE(n, 'com agulha?', T(n, 'é proibido')) + .8, 'É proibido fazer rinomodelação com agulha?')],
        cit=(T(n, 'assegurança') + 1.2, T(n, 'assegurança') + 4.6, f'{G}Segurança{GF} em primeiro lugar, sempre'),
        final=T(n, 'E você, ultrapassado'))
    n = 'IMG_7834'; V[n] = entrevista(4, n, 'Anestesia do forame supraorbitário na toxina: perda de tempo?', TE(n, 'verdade?', 10),
        resp=T(n, 'Eu acho que é perda'),
        perguntas=[(T(n, 'E se o paciente'), TE(n, 'fazer?', T(n, 'E se o paciente')) + .6, 'E se o paciente for muito sensível e pedir a anestesia?')],
        dr=T(n, 'realmente, na nossa'), cit=(T(n, 'Não é um erro'), TE(n, 'resultado,', T(n, 'Não é um erro')), 'Não é um erro fazer: não atrapalha o resultado, só gasta mais tempo'),
        final=T(n, 'Qual a tua opinião?'))
    n = 'IMG_7835'; t20 = T(n, 'dia 20 de outubro')
    V[n] = entrevista(0, n, 'Todas as toxinas duram o mesmo tempo?', TE(n, 'clínica?'), cat='PRÁTICA CLÍNICA',
        resp=T(n, 'Eu acho que algumas'),
        perguntas=[(T(n, 'Todas as toxinas têm'), TE(n, 'opinião?', T(n, 'Todas as toxinas têm')) + .6, 'Todas as toxinas têm a mesma durabilidade?')],
        dr=T(n, 'Não temos um'), cit=(T(n, 'nos estudos'), TE(n, 'resultados', T(n, 'nos estudos')) + .8, 'Nos estudos, elas entregam os mesmos resultados'),
        extra=[LIVE(t20 - .1, T(n, 'vai ter curso') - .05, 20, 'Abertura das inscrições', tData=t20 + .2, tVivo=t20 + 1.2, tTexto=t20 + 1.6),
               CURSOS_(T(n, 'vai ter curso'), T(n, 'se você quiser se') - .05, [(T(n, 'vai ter curso'), 'Todos os cursos'), (T(n, 'com acesso ao'), f'Acesso {G}vitalício{GF}')]),
               dict(tipo='pergunta', s=T(n, 'comenta a'), e=FIM(n) + .6, h='COMENTA', q=f'{G}VITALÍCIO{GF}')])
    n = 'IMG_7839'; tc = T(n, 'Quero fazer um último')
    V[n] = entrevista(1, n, 'Preenchimento de glabela com agulha: técnica ultrapassada?', TE(n, 'verdade?'),
        resp=T(n, 'Eu não sei,'),
        perguntas=[(T(n, 'Então é proibido'), TE(n, 'não?', T(n, 'Então é proibido')) + .5, 'É proibido fazer preenchimento de glabela?'),
                   (T(n, 'Quero saber de vocês'), tc - .1, f'Glabela: pode ou não pode preencher? {G}Agulha ou cânula?{GF}')],
        dr=T(n, 'Minha opinião,'), cit=(T(n, 'Cândula 22,'), TE(n, 'profundo.', T(n, 'Cândula 22,')), 'Cânula 22, plano superficial, fugindo das artérias do plano profundo'),
        extra=[LOGO_(tc, T(n, 'todos os cursos') - .05),
               CURSOS_(T(n, 'todos os cursos'), T(n, 'você vai fazer o seguinte') - .05, [(T(n, 'todos os cursos'), 'Todos os cursos que já fiz'), (T(n, 'todos que eu for'), f'Todos que {G}ainda vou fazer{GF}')]),
               dict(tipo='pergunta', s=T(n, 'comenta vitalícia'), e=FIM(n) + .6, h='COMENTA', q=f'{G}VITALÍCIA{GF}')])
    n = 'IMG_7841'; tb = T(n, 'E se você quiser participar')
    V[n] = entrevista(2, n, 'Bioremodelador para qualidade de pele: você usa?', TE(n, 'não?'), cat='PRÁTICA CLÍNICA',
        resp=T(n, 'Eu uso.'),
        perguntas=[(T(n, 'Agora, quando'), TE(n, 'indica?') + .6, 'Quando você indica?'),
                   (T(n, 'E você? Você usa'), tb - .1, f'Você usa na sua prática clínica? {G}Bom custo-benefício?{GF}')],
        dr=T(n, 'Eu acho que essa'), cit=(T(n, 'ele é um refinamento'), TE(n, 'refinamento.', T(n, 'ele é um refinamento')) + .4, f'Um {G}refinamento{GF} do refinamento'),
        extra=[LOGO_(tb, T(n, 'ter acesso a todos') - .05),
               CURSOS_(T(n, 'ter acesso a todos'), T(n, 'E além do mais') - .05, [(T(n, 'ter acesso a todos'), 'Todos os cursos que já fiz'), (T(n, 'todos que eu vou'), f'Todos que {G}ainda vou fazer{GF}')]),
               dict(tipo='pos', s=T(n, 'E além do mais'), e=T(n, 'Além disso,') - .05, topo='E AINDA', texto=f'Incluída na {G}Black Friday Vitalícia{GF}', tTexto=T(n, 'E além do mais') + 1.0),
               SAIBA(T(n, 'Clica aqui em Saiba'), FIM(n) + .6, T(n, 'Saiba Mais'))])
    n = 'IMG_7845'; V[n] = entrevista(3, n, 'Os 3 melhores preenchedores para os lábios', TE(n, 'lábios?'), cat='TOP 3 NA PRÁTICA',
        primeiro=T(n, 'Pra mim,'), resp=T(n, 'Eu gosto do Deep.'),
        cit=(T(n, 'A minha opinião é'), TE(n, 'paciente.', T(n, 'A minha opinião é')) + .4, f'Não tem o melhor. Tem a {G}melhor indicação{GF} para cada perfil de paciente'),
        final=T(n, 'E na sua opinião'))
    n = 'IMG_7846'; V[n] = entrevista(4, n, 'Os 3 melhores produtos para rinomodelação', TE(n, 'rinomodelação?'), cat='TOP 3 NA PRÁTICA',
        primeiro=T(n, 'Três melhores produtos,'), resp=T(n, 'E voar,'),
        cit=(T(n, 'precisa ser um produto'), TE(n, 'projeção', T(n, 'precisa ser um produto')) + 1.0, f'Precisa de {G}capacidade de projeção{GF} para deixar o nariz firme e estruturado'),
        final=T(n, 'Qual as suas'))
    n = 'IMG_7848'; V[n] = entrevista(0, n, 'Os 3 melhores produtos para o bigode chinês', TE(n, 'chinês?'), cat='TOP 3 NA PRÁTICA',
        primeiro=T(n, 'Três melhores produtos.'), resp=T(n, 'Eu gosto muito do'),
        cit=(T(n, 'maleabilidade,'), TE(n, 'migrar.'), f'Projeção e {G}maleabilidade{GF}: o produto não pode nodular nem migrar'),
        final=T(n, 'eu quero saber as suas'))
    n = 'IMG_7851'; V[n] = entrevista(1, n, 'Preenchimento labial com seringa BD: perda de tempo?', TE(n, 'verdade?'),
        resp=T(n, 'Mito, total!'), dr=T(n, 'Eu não uso.'),
        cit=(T(n, 'a individualização'), TE(n, 'importante.') + .4, f'A {G}individualização{GF} é o mais importante'),
        final=T(n, 'E a sua opinião,'))
    n = 'IMG_7854'; V[n] = entrevista(2, n, 'Efeito vacina da toxina: mito ou verdade?', TE(n, 'verdade?'),
        resp=T(n, 'Verdade.'),
        perguntas=[(T(n, 'Quantos pacientes'), TE(n, 'pegou?') + .5, 'Quantos pacientes você já viu com efeito vacina?')],
        dr=T(n, 'Todos os pacientes que'), cit=(T(n, 'o efeito vacina ainda'), TE(n, 'oficial.') + .5, 'Ainda não existe uma comprovação oficial do efeito vacina'),
        final=T(n, 'Efeito vacina, mito', 60))
    for v in V.values(): v['trocas'] = TROCAS
    return V

if __name__ == '__main__':
    VIDEOS = _videos()
    gerar(VIDEOS, sys.argv[1], sys.argv[2], sys.argv[3:])
