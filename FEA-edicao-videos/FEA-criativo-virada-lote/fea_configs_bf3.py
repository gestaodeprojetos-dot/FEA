"""FEA: roteiros do 3º lote da Black Friday Vitalícia (17/10/2026, pasta "Criativos black ", 9 brutos IMG_7731 a 7739).
Lembrete (antes de 20/10): IMG_7731 e IMG_7738. Vendas (inscrições abertas): 7732, 7733, 7734, 7736, 7737, 7739.
IMG_7735 (6 s) termina no meio da frase ("participar da...") e fica de fora.
Trilha alternada entre os vídeos (Keila: "ir mudando a musiquinha de fundo para não ficar tudo igual").
Fatos da página: live de abertura 20/10 às 20h; inclusos Pós-Graduação Injetáveis e Elite Injectors Congress
(01 e 02/11, São Paulo). "Certificação do MEC", "curso presencial demonstrativo", "1.200 aulas" e "500 aulas" não estão
na página: ficam só na fala e na legenda, nunca em cartão.
Uso: python3 fea_configs_bf3.py PASTA_TRANSCRICOES PASTA_SAIDA [NOME ...]"""
import sys
from fea_configs_bf import K, LOGO_, SAIBA, CURSOS_, LIVE, CONTA, G, GF, VITAL, gerar

POS = ('presente', 'BÔNUS ESPECIAL', 'Pós-Graduação em Injetáveis', 'incluída na Black Friday Vitalícia')
NUNCA = ('valor', VITAL, 'Nunca mais compre um curso', 'de harmonização facial')
def TODOS(s, e, t1, t2, t3=None):
    it = [(t1, 'Todos os cursos que já fiz'), (t2, f'Todos que {G}ainda vou fazer{GF}')]
    if t3: it.append((t3, 'Atualizações vitalícias'))
    return CURSOS_(s, e, it)
def PG(s, e, topo='BÔNUS ESPECIAL', texto=f'Incluída na {G}Black Friday Vitalícia{GF}', tTexto=None):
    # cena da Pós com a identidade visual da pós (pasta enviada pela Keila em 17/10/2026): selo, grafismo, cobre
    return dict(tipo='pos', s=s, e=e, topo=topo, texto=texto, tTexto=tTexto or s + .9)
def ELITE(s, e, t1, t2):
    # palestrantes do Elite Injectors Congress (fotos e nomes da página el.joaopithon.com.br)
    return dict(tipo='palestrantes', s=s, e=e, itens=[dict(t=t1, html=f'{G}Elite Injectors Congress{GF}'), dict(t=t2, html='01 e 02/11 · São Paulo')])
def B(trilha, publico='geral', **k):
    return dict(publico=publico, cta='cta.mp4', trilha=trilha, vol_trilha=.22, **k)

VIDEOS = {
 # ---------------- lembrete ----------------
 # 92 s explicando a Black. Corte da hesitação "E essa vai ser a maior... E essa..." (73,3 a 80,4 s): fica
 # "...que você vai ter na história. Essa vai ser oficialmente a maior Black Friday da harmonização facial."
 'IMG_7731': B('epico', inicio=.4, fim=91.3, cortes=[(73.28, 80.36)],
   trocas=[(['porção'], ['promoção'])],
   zoom=[(14.2, 16.9), (27.1, 30.3), (37.2, 41.7), (52.4, 56.6), (66.4, 73.25), (85.3, 86.7)], cenas=[
    LOGO_(2.3, 3.65),
    K(3.7, 7.95, 'aluno', 'COM TRANSPARÊNCIA', 'Como vai funcionar', 'a Black Friday Vitalícia'),
    K(8.3, 13.8, 'presente', 'TODOS OS DETALHES', 'Bônus e condições', chips=[(8.8, 'Bônus'), (10.1, 'Detalhes'), (13.0, 'Curso vitalício')]),
    K(17.0, 20.2, 'presente', 'PARA QUEM ESTIVER AO VIVO', 'Bônus especiais'),
    ELITE(20.3, 27.0, 21.2, 25.7),
    PG(30.4, 36.9),
    TODOS(46.3, 52.3, 46.3, 48.6, 50.8),
    LIVE(56.7, 61.4, 20, 'Primeira aula ao vivo', tData=57.5, tVivo=60.6, tTexto=60.9),
    K(61.5, 66.3, 'presente', 'AO VIVO', 'Bônus especiais', 'para quem estiver na live'),
    LOGO_(80.4, 84.9),
    LIVE(86.75, 91.3, 20, 'Abertura das inscrições', tData=87.2, tVivo=88.2, tTexto=89.8)]),
 # ele fala "dia 20 de outubro" 2 vezes: sai o 1º e a pausa (Keila, 17/10), fica "começa aqui. Dia 20 de outubro abriremos"
 'IMG_7738': B('pulsante', inicio=.3, fim=21.9, cortes=[(5.3, 9.3)], zoom=[(11.35, 13.4)], cenas=[
    LOGO_(.9, 2.5),
    K(2.6, 5.25, 'inf', VITAL, 'A maior Black Friday', 'da harmonização facial'),
    LIVE(9.3, 11.3, 20, 'Abertura das inscrições', tData=9.45, tVivo=10.0, tTexto=10.4),
    TODOS(13.45, 18.9, 14.6, 16.0, 17.6),
    SAIBA(19.6, 21.9, 20.0)]),
 # ---------------- vendas ----------------
 'IMG_7732': B('brilho', inicio=.2, fim=31.8, zoom=[(7.7, 10.5), (15.5, 19.2)], cenas=[
    K(.2, 2.9, 'inf', 'INSCRIÇÕES ABERTAS', 'Black Friday Vitalícia', 'todos os cursos, para sempre, por um único preço'),
    TODOS(2.95, 7.6, 3.0, 4.5, 6.2),
    PG(10.6, 15.4, topo='BÔNUS SUPER ESPECIAL'),
    K(19.3, 24.6, 'aluno', 'VOCÊ VAI TER', 'Todos os cursos e a Pós-Graduação'),
    LOGO_(24.7, 29.3),
    SAIBA(29.4, 31.8, 30.1)]),
 'IMG_7733': B('urgencia', inicio=.2, fim=33.5, zoom=[(10.7, 14.7), (17.2, 19.0), (27.2, 30.9)], cenas=[
    K(.2, 3.9, 'inf', VITAL, 'A maior Black Friday', 'da harmonização facial'),
    LOGO_(4.3, 5.9),
    TODOS(6.1, 10.6, 6.2, 7.4, 8.9),
    K(19.1, 23.0, 'inf', 'PARA O RESTO DA VIDA', 'Atualizações vitalícias', 'todos os cursos que já fiz e que vou fazer'),
    PG(23.05, 27.1),
    SAIBA(31.0, 33.5, 31.6)]),
 'IMG_7734': B('groove', inicio=.3, fim=35.45, zoom=[(24.0, 28.7), (29.2, 31.0)], cenas=[
    K(.3, 2.6, *NUNCA),
    LOGO_(2.8, 4.4),
    TODOS(4.45, 10.4, 5.0, 7.2, 8.9),
    K(10.5, 20.6, 'aulas', 'TODOS OS CURSOS', 'Da toxina à reologia',
      chips=[(11.3, 'Toxina botulínica'), (13.0, 'Preenchimento'), (14.3, 'Bioestimuladores'), (15.8, 'Fios'),
             (16.4, 'Corporal'), (17.7, 'Anatomia'), (18.5, 'Intercorrências'), (19.6, 'Reologia')]),
    PG(20.7, 24.0, topo='E AINDA'),
    LOGO_(31.1, 33.0),
    SAIBA(33.3, 35.45, 33.8)]),
 'IMG_7736': B('tensao', inicio=.2, fim=32.45, remover=[('meu', 2.3)], zoom=[(10.55, 12.1), (24.3, 30.2)], cenas=[
    K(.2, 2.5, *NUNCA),
    LOGO_(2.6, 5.5),
    TODOS(5.7, 10.5, 5.8, 7.2, 9.0),
    SAIBA(12.1, 13.3, 12.6),
    K(13.3, 19.4, 'aulas', 'TODOS OS CURSOS', 'Da toxina às intercorrências',
      chips=[(14.2, 'Toxina'), (14.8, 'Preenchedores'), (15.5, 'Bioestimuladores'), (16.5, 'Fios'), (17.0, 'Corporal'),
             (17.6, 'Anatomia'), (18.2, 'Intercorrências')]),
    PG(19.5, 24.2, topo='E AINDA', texto=f'Já incluída na {G}Black Friday Vitalícia{GF}', tTexto=24.6),
    SAIBA(30.3, 32.45, 30.9)]),
 'IMG_7737': B('epico', inicio=.2, fim=38.75, zoom=[(20.4, 26.6), (32.7, 34.7), (37.4, 38.75)], cenas=[
    CONTA(.2, 4.4, [(.9, 'Atualizações', None, None), (3.2, 'Cursos', None, None), (3.7, 'Congressos', None, None)],
          total=False, topo='QUANTO VOCÊ JÁ GASTOU'),
    K(4.5, 8.2, 'valor', 'NUNCA MAIS', 'Pague por nenhum curso', 'nem por nenhuma atualização'),
    LOGO_(8.3, 10.3),
    CURSOS_(10.4, 16.2, [(10.4, 'Todos os cursos que já fiz'), (12.0, f'Todos que {G}ainda vou fazer{GF}'),
                         (12.9, 'Todas as atualizações'), (14.4, f'Até o {G}fim da vida{GF}')]),
    K(16.3, 20.3, 'valor', 'UM ÚNICO VALOR', 'Nenhum centavo a mais', 'atualizações vitalícias'),
    K(26.7, 32.6, 'inf', 'PARA O RESTO DA VIDA', 'Tudo o que vem pela frente', 'tudo o que eu ainda vou produzir'),
    SAIBA(34.8, 37.4, 35.4)]),
 # corte do tropeço "Eu já falei do congresso? Não. Putz..." (14,15 a 20,6 s): ele retoma em "E além do mais, o meu congresso"
 'IMG_7739': B('brilho', inicio=.15, fim=35.85, cortes=[(14.15, 20.6)],
   trocas=[(['cima', 'a', 'mais'], ['Saiba', 'Mais']), (['friday', 'e', 'vitalícia'], ['Friday', 'Vitalícia'])],
   zoom=[(10.0, 14.1)], cenas=[
    LOGO_(.9, 2.75),
    TODOS(3.0, 6.1, 4.1, 5.0),
    PG(6.2, 9.95, topo='VOCÊS VÃO TER'),
    ELITE(20.65, 25.0, 23.8, 24.4),
    K(25.1, 29.1, 'valor', 'UM ÚNICO VALOR', 'Paga uma vez', 'e nunca mais um real a mais'),
    LOGO_(30.5, 33.2),
    SAIBA(33.6, 35.85, 34.2)]),
}

if __name__ == '__main__':
    gerar(VIDEOS, sys.argv[1], sys.argv[2], sys.argv[3:])
