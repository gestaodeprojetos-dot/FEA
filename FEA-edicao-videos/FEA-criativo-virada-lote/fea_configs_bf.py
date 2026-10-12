"""FEA: roteiros dos criativos da Black Friday Vitalícia (out/2026), no mesmo motor do criativo de virada de lote.
Tempos escritos na linha do tempo do bruto; `inicio` corta o silêncio do começo e tudo é deslocado.
Fatos da página bf.joaopithon.com.br/black-vitalicia-d/: live de abertura 20/10 às 20h, todos os cursos para
sempre por um único preço, 20 formações/cursos/imersões/livros, oferta especial para alunos.
Uso: python3 fea_configs_bf.py PASTA_TRANSCRICOES PASTA_SAIDA [NOME ...]"""
import json, re, sys
from fea_configs import palavras, agrupar

CURSOS = [f'card-{n}.png' for n in ('FEP', 'FEB', 'FEF', 'FEC', 'FEA2', 'FEBIO2', 'pos', 'elite', 'iar', 'ipl', 'iff52',
                                    'iff102', 'ipo', 'atsd', 'complicacoes', 'ebook1', 'ebook2', 'ctx', 'plxx', 'CPX')]
LOGO = dict(src='logo-bf.png', w=880, h=307, top=600,
            tag='Todos os meus cursos, <b style="color:var(--teal)">para sempre.</b>')
CTA = 'cta.mp4'

def K(s, e, icone, topo, titulo, sub='', chips=()):
    return dict(tipo='cartao', s=s, e=e, icone=icone, topo=topo, titulo=titulo, sub=sub,
                chips=[dict(t=t, html=h) for t, h in chips])
def LOGO_(s, e): return dict(tipo='logo', s=s, e=e)
def SAIBA(s, e, t): return dict(tipo='saiba', s=s, e=e, tToque=t)
def CURSOS_(s, e, itens): return dict(tipo='cursos', s=s, e=e, itens=[dict(t=t, html=h) for t, h in itens])
def LIVE(s, e, dia, texto, tData=None, tVivo=None, tTexto=None, selo='AO VIVO'):
    # 20/10 (abertura geral) tem 20h na página; 19/10 (alunos) não tem horário publicado: esconde
    return dict(tipo='live', s=s, e=e, dia=dia, hora='20h' if dia == 20 else None, selo=selo, texto=texto,
                tData=tData or s + .1, tHora=(tData or s + .1) + .3, tVivo=tVivo or s + .5, tTexto=tTexto or s + .8)
def CONTA(s, e, itens, tTotal=None, total=True, totalTexto='', carimbo='', tCarimbo=None, topo='CONTA RÁPIDA'):
    return dict(tipo='conta', s=s, e=e, topo=topo, itens=[dict(t=t, nome=n, valor=v, tv=tv) for t, n, v, tv in itens],
                tTotal=tTotal, total=total, totalTexto=totalTexto, carimbo=carimbo, tCarimbo=tCarimbo, rotulo='TOTAL')
def FEP(s, e, tLogo, texto, topo='CONVITE EXCLUSIVO'):
    # logo da FEP (pasta enviada pela Keila em 12/10/2026) quando ele fala "meu aluno da FEP"
    return dict(tipo='marca', s=s, e=e, tLogo=tLogo, logo='fep-logo.png', sub='fep-texto.png', topo=topo, texto=texto)
def DATAS(s, e, t20, t19): return dict(tipo='datas', s=s, e=e, t20=t20, t19=t19)
G = '<span class="goldtxt">'; GF = '</span>'
VITAL = 'BLACK FRIDAY VITALÍCIA'

VIDEOS = {
 # ---------------- ALUNOS (19/10) ----------------
 'alunos': dict(inicio=.12, fim=35.6, publico='alunos', trilha='urgencia', vol_trilha=.28,
   trocas=[(['20', 'do', '10'], ['19/10'])],      # o Dr. fala "19 do 10" (Keila, 12/10/2026); o Whisper ouviu 20
   zoom=[(9.7, 11.7), (26.0, 27.85), (34.4, 35.6)], tremor=[(.3, 2.05)], sem_legenda=[(.12, 2.05)], cenas=[
    # "Atenção" começa em 0,35 s e "alunos" em 1,25 s (medido no áudio; o Whisper marcava 1,0 e 1,5)
    dict(tipo='alerta', s=.12, e=2.05, tA=.35, tB=1.25),
    K(2.1, 4.2, 'aluno', 'EXCLUSIVO', 'Para os meus alunos', 'uma oferta especial na Black Friday Vitalícia'),
    LOGO_(4.2, 5.75),
    K(5.8, 9.65, 'inf', VITAL, 'Acesso vitalício', 'todos os cursos, para sempre, por um único preço'),
    K(11.7, 15.7, 'presente', 'NA ABERTURA DAS INSCRIÇÕES', 'Bônus exclusivos', chips=[(11.8, 'Bônus presenciais'), (13.8, 'Pós-graduação incluída')]),
    CURSOS_(15.75, 20.75, [(15.8, 'Todos os cursos que já criei'), (17.4, f'E os que {G}ainda vou lançar{GF}'), (19.3, 'Atualizações vitalícias')]),
    K(20.8, 25.95, 'valor', 'UM ÚNICO VALOR', 'Nenhum real a mais', 'nem para atualizações, nem para extras'),
    SAIBA(27.85, 29.25, 28.3),
    LIVE(29.25, 34.4, 19, f'Abertura oficial das inscrições<br>{G}no Instagram do Dr. João Pithon{GF}', tData=30.5, tVivo=29.95, tTexto=31.5),
 ]),
 # Ads 113 versão final (Keila, 12/10/2026): bruto "alunos" inteiro, sem cortes; a data é 20/10 mesmo e o CTA é o de 20 de outubro.
 'alunos20': dict(inicio=.12, fim=35.9, publico='alunos', cta='cta.mp4', trilha='urgencia', vol_trilha=.28,
   zoom=[(9.7, 11.7), (26.0, 27.85), (34.4, 35.9)], tremor=[(.3, 2.05)], sem_legenda=[(.12, 2.05)], cenas=[
    dict(tipo='alerta', s=.12, e=2.05, tA=.35, tB=1.25),
    K(2.1, 4.2, 'aluno', 'EXCLUSIVO', 'Para os meus alunos', 'uma oferta especial na Black Friday Vitalícia'),
    LOGO_(4.2, 5.75),
    K(5.8, 9.65, 'inf', VITAL, 'Acesso vitalício', 'todos os cursos, para sempre, por um único preço'),
    K(11.7, 15.7, 'presente', 'NA ABERTURA DAS INSCRIÇÕES', 'Bônus exclusivos', chips=[(11.8, 'Bônus presenciais'), (13.8, 'Pós-graduação incluída')]),
    CURSOS_(15.75, 20.75, [(15.8, 'Todos os cursos que já criei'), (17.4, f'E os que {G}ainda vou lançar{GF}'), (19.3, 'Atualizações vitalícias')]),
    K(20.8, 25.95, 'valor', 'UM ÚNICO VALOR', 'Nenhum real a mais', 'nem para atualizações, nem para extras'),
    SAIBA(27.85, 29.25, 28.3),
    LIVE(29.25, 34.4, 20, f'Abertura oficial das inscrições<br>{G}no Instagram do Dr. João Pithon{GF}', tData=29.4, tVivo=29.95, tTexto=31.5),
 ]),
 # Ads 113 refeito (Keila, 12/10/2026): o final do alunos dizia "ao vivo dia 20/10" e "abertura oficial no Instagram".
 # Bruto montado: alunos até "clique em Saiba Mais" (29,0 s) + final do IMG_0869 "então esteja comigo ao vivo 19 do 10,
 # te espero lá" (19,6 a 22,9 s). A cena da live cobre a emenda.
 'alunos19': dict(inicio=.12, fim=32.3, publico='alunos', trilha='urgencia', vol_trilha=.28,
   zoom=[(9.7, 11.7), (26.0, 27.85)], tremor=[(.3, 2.05)], sem_legenda=[(.12, 2.05)], cenas=[
    dict(tipo='alerta', s=.12, e=2.05, tA=.35, tB=1.25),
    K(2.1, 4.2, 'aluno', 'EXCLUSIVO', 'Para os meus alunos', 'uma oferta especial na Black Friday Vitalícia'),
    LOGO_(4.2, 5.75),
    K(5.8, 9.65, 'inf', VITAL, 'Acesso vitalício', 'todos os cursos, para sempre, por um único preço'),
    K(11.7, 15.7, 'presente', 'NA ABERTURA DAS INSCRIÇÕES', 'Bônus exclusivos', chips=[(11.8, 'Bônus presenciais'), (13.8, 'Pós-graduação incluída')]),
    CURSOS_(15.75, 20.75, [(15.8, 'Todos os cursos que já criei'), (17.4, f'E os que {G}ainda vou lançar{GF}'), (19.3, 'Atualizações vitalícias')]),
    K(20.8, 25.95, 'valor', 'UM ÚNICO VALOR', 'Nenhum real a mais', 'nem para atualizações, nem para extras'),
    SAIBA(27.85, 29.0, 28.3),
    LIVE(28.95, 32.3, 19, f'Live de abertura para alunos<br>{G}te espero lá{GF}', tData=29.1, tVivo=30.2, tTexto=31.3),
 ]),
 'IMG_0867': dict(fim=44.38, publico='alunos',   # termina em "Black Friday Vitalícia": a frase seguinte fica sem concluir (Keila, 12/10/2026)
   zoom=[(14.1, 18.0), (30.7, 37.2)], cenas=[
    FEP(0, 4.9, 1.2, f'Um convite {G}especial e exclusivo{GF}'),
    LOGO_(5.0, 6.6),
    K(6.6, 14.0, 'presente', 'PARA ALUNOS', 'Um dia especial de abertura', chips=[(11.3, 'Valores especiais'), (12.7, 'Condições especiais')]),
    K(18.0, 23.2, 'aluno', 'ALUNOS PRIMEIRO', 'Um dia antes', 'da abertura para quem ainda não é aluno'),
    LIVE(23.2, 30.6, 19, f'Live de abertura exclusiva<br>{G}somente para alunos{GF}', tData=24.8, tVivo=26.6, tTexto=28.9),
    SAIBA(37.2, 38.5, 37.7),
    LIVE(38.5, 42.6, 19, f'Ao vivo com o Dr. João<br>{G}abertura para alunos{GF}', tData=40.5, tVivo=39.8, tTexto=41.0),
    LOGO_(42.6, 44.38),
 ]),
 'IMG_0868': dict(fim=31.8, publico='alunos', zoom=[(21.3, 27.0)], cenas=[
    FEP(0, 4.6, 1.2, f'Um convite {G}muito especial{GF}'),
    LOGO_(4.7, 6.8),
    LIVE(6.8, 12.6, 19, f'Um dia antes da abertura geral<br>{G}somente para alunos da FEP{GF}', tData=8.0, tVivo=10.4, tTexto=10.6, selo='SÓ PARA ALUNOS'),
    K(12.7, 21.2, 'presente', 'SÓ PARA ALUNOS DA FEP', 'Um dia de antecipação', chips=[(15.0, 'Valores especiais'), (16.8, 'Condições especiais')]),
    K(27.1, 31.8, 'aluno', 'DIA 19/10', 'Abertura em formato exclusivo', 'te espero lá'),
 ]),
 'IMG_0869': dict(fim=23.1, publico='alunos', zoom=[(19.6, 23.1)], cenas=[
    FEP(0, 3.75, 1.2, f'Uma {G}condição especial{GF}', topo='PARA OS MEUS ALUNOS'),
    LOGO_(3.8, 6.9),
    DATAS(7.0, 14.6, 9.6, 12.0),
    K(14.6, 19.5, 'presente', 'DIA DE INSCRIÇÕES ESPECIAL', 'Só para alunos', chips=[(15.3, 'Valores especiais'), (16.8, 'Tudo de mais especial')]),
    LIVE(19.6, 23.1, 19, f'{G}Te espero lá{GF}', tData=21.1, tVivo=20.8, tTexto=22.0),
 ]),
 'IMG_0871': dict(fim=31.5, publico='alunos', zoom=[(14.6, 16.6)], cenas=[
    FEP(0.1, 5.6, 1.2, f'Condições e {G}valores especiais{GF}', topo='PARA OS MEUS ALUNOS'),
    LOGO_(5.7, 7.4),
    DATAS(7.5, 14.6, 9.6, 12.1),
    K(16.6, 22.8, 'valor', 'PARA VOCÊ PARTICIPAR', 'Pagando menos', chips=[(16.8, 'Bônus especiais'), (18.7, 'Valores especiais'), (20.2, 'Tudo de mais especial')]),
    SAIBA(22.9, 25.9, 25.2),
    LIVE(25.9, 31.3, 19, f'Live de abertura<br>{G}para alunos da FEP{GF}', tData=28.6, tVivo=27.3, tTexto=28.9),
 ]),
 'IMG_0872': dict(fim=27.2, publico='alunos', zoom=[(21.3, 27.2)], cenas=[
    K(0, 4.0, 'aluno', 'PARA QUEM JÁ É MEU ALUNO', 'A sua chance'),
    LOGO_(4.1, 6.6),
    LIVE(6.7, 11.4, 19, f'Um dia antes<br>{G}da abertura geral{GF}', tData=8.5, tVivo=9.8, tTexto=9.9, selo='SÓ PARA ALUNOS'),
    K(11.5, 16.0, 'valor', 'NO DIA DOS ALUNOS', 'Pagando menos', chips=[(13.7, 'Bônus especiais'), (14.9, 'Condições especiais')]),
    SAIBA(16.1, 17.8, 17.0),
    LIVE(17.8, 21.2, 19, f'Live de abertura<br>{G}para alunos{GF}', tData=18.0, tVivo=19.5, tTexto=20.0),
 ]),
 'IMG_0873': dict(fim=29.2, publico='alunos', zoom=[(8.9, 13.9)], cenas=[
    LOGO_(0, 1.8),
    K(1.8, 5.5, 'aluno', VITAL, 'Para alunos'),
    K(5.6, 8.8, 'valor', 'PARA QUEM JÁ FEZ UM CURSO MEU', 'Pague menos', 'na Black Friday'),
    K(14.0, 19.9, 'inf', 'ALUNO VITALÍCIO', 'Condições especiais', chips=[(18.0, 'Valores especiais'), (19.0, 'Dia especial')]),
    LIVE(20.0, 23.0, 19, f'Abertura das inscrições<br>{G}para quem já é aluno{GF}', tData=20.1, tVivo=21.0, tTexto=21.1, selo='SÓ PARA ALUNOS'),
    SAIBA(23.0, 24.8, 24.2),
    LIVE(24.8, 28.2, 19, f'Live de abertura especial<br>{G}para você que é aluno{GF}', tData=25.0, tVivo=25.1, tTexto=26.0),
 ]),
 # ---------------- ABERTURA GERAL (20/10, 20h) ----------------
 'IMG_0876': dict(fim=27.0, publico='geral', zoom=[(18.4, 20.4)], cenas=[
    LOGO_(0, 2.0),
    LIVE(2.0, 5.2, 20, 'Abertura oficial das inscrições', tData=2.2, tVivo=3.1, tTexto=3.4),
    K(5.3, 9.6, 'inf', VITAL, 'Seu último curso de harmonização da vida'),
    SAIBA(10.0, 11.4, 10.7),
    K(11.4, 18.3, 'presente', 'NA LIVE DE ABERTURA', 'Bônus especiais', chips=[(15.0, 'Pós-graduação'), (16.4, 'Cursos presenciais'), (17.5, 'E muito mais')]),
    SAIBA(20.4, 21.9, 20.7),
    LIVE(21.9, 26.6, 20, f'Eu explico {G}cada detalhe{GF} ao vivo', tData=22.0, tVivo=22.2, tTexto=23.5),
 ]),
 '71F04D8F-1E4E-43B3-8CBD-632A44D35F2F': dict(fim=41.9, publico='geral', zoom=[], cenas=[
    K(0.3, 7.1, 'valor', 'CONTA RÁPIDA', 'Some quanto você já gastou', 'não os certificados'),
    CONTA(7.2, 22.4, [(8.1, 'Curso de botox', 5, 9.3), (10.8, 'Curso de preenchimento', 10, 12.4),
                      (13.4, 'Especialização', 20, 14.6), (16.6, 'Congressos', 10, 19.1)], tTotal=20.3),
    K(22.4, 27.4, 'valor', 'PARE DE GASTAR', 'com cursos isolados'),
    LOGO_(27.6, 30.5),
    K(30.6, 36.4, 'inf', 'ACESSO VITALÍCIO', 'Nunca mais pague para continuar aprendendo'),
    K(38.2, 41.9, 'valor', 'PARA O RESTO DA VIDA', 'Nenhum real a mais'),
 ]),
 '7BE3AE3C-A4DD-44D5-8340-BEACA482AA04': dict(fim=56.3, publico='geral', zoom=[], cenas=[
    K(0.3, 6.0, 'valor', 'CONTA RÁPIDA', 'Some quanto você já jogou fora', 'em cursos, não os certificados'),
    CONTA(7.4, 24.9, [(9.7, 'Curso de botox', 5, 11.1), (12.8, 'Preenchimento', 10, 13.9),
                      (15.5, 'Especialização', 20, 16.8), (18.4, 'Congressos', 10, 19.3)], tTotal=20.4),
    LOGO_(25.0, 27.8),
    K(27.9, 34.5, 'inf', VITAL, 'Seu último curso da vida', 'com atualizações vitalícias'),
    CURSOS_(34.6, 44.1, [(35.6, 'Todas as especializações'), (37.6, 'Todas as atualizações'), (40.0, f'Todas as {G}novidades{GF}')]),
    LIVE(44.2, 50.3, 20, f'Pague uma vez<br>{G}e nunca mais pague por atualizações{GF}', tData=46.5, tVivo=45.0, tTexto=47.5),
    SAIBA(50.4, 53.0, 52.4),
    LIVE(53.0, 55.9, 20, f'Live de abertura<br>{G}te vejo lá{GF}', tData=53.1, tVivo=54.2, tTexto=54.5),
 ]),
 'IMG_0883': dict(fim=54.9, publico='geral', zoom=[(29.9, 35.0)], cenas=[
    K(0.2, 3.5, 'valor', 'CONTA RÁPIDA', 'Quanto você já gastou em cursos?'),
    CONTA(3.5, 18.6, [(4.0, 'Botox', None, None), (4.6, 'Preenchimento', None, None), (5.3, 'Especializações', None, None),
                      (7.6, 'Atualização (+1 ano)', 5, 9.3), (10.5, 'Outra atualização', 5, 12.9)],
          tTotal=13.6, total=False, totalTexto='e não para...'),
    K(18.6, 29.9, 'valor', 'COM ESSE DINHEIRO', 'Você poderia ter...', chips=[(21.0, 'Reformado a clínica'), (23.3, 'Comprado materiais'),
                                                                             (26.9, 'Feito mais procedimentos'), (28.9, 'Comprado um carro')]),
    K(35.0, 39.1, 'inf', 'CURSO VITALÍCIO', 'Nunca mais gaste um centavo', 'com atualizações vitalícias'),
    LIVE(39.2, 49.4, 20, f'Live de abertura das inscrições<br>{G}para você se destacar{GF}', tData=40.1, tVivo=42.0, tTexto=43.0),
    SAIBA(50.6, 52.7, 51.3),
    LIVE(52.7, 54.9, 20, 'A gente se vê na live de abertura', tData=52.8, tVivo=53.0, tTexto=53.3),
 ]),
 '5D268809-CD98-4B01-BC7D-8DBCB924C66A': dict(fim=70.8, publico='geral', zoom=[(14.8, 18.0)], cenas=[
    K(0.1, 5.7, 'valor', 'FAÇA AS CONTAS', 'Quanto você já gastou em cursos?'),
    K(5.8, 9.3, 'inf', 'ACESSO VITALÍCIO', 'Um curso vitalício', 'com atualizações vitalícias'),
    K(9.4, 14.75, 'valor', 'QUANTO VOCÊ JÁ GASTOU EM', 'Cursos e congressos', chips=[(10.7, 'Botox'), (11.3, 'Preenchimento'), (12.2, 'Fios'),
                                                                                    (12.6, 'Bioestimuladores'), (13.4, 'Congressos')]),
    K(21.2, 24.2, 'aulas', 'NA PLATAFORMA', '1.200 aulas'),
    K(24.3, 40.4, 'valor', 'TUDO INCLUSO', 'Quanto custaria cada curso?', chips=[(25.2, 'Preenchimento'), (27.7, 'Botox'), (30.0, 'Fios'),
                                                                              (32.4, 'Gestão de clínicas'), (36.0, 'Corporal'), (38.1, 'Rinomodelação')]),
    K(40.5, 46.7, 'aulas', 'E MAIS', 'Imersões avançadas', chips=[(40.7, 'Olheiras'), (41.2, 'Complicações'), (42.1, 'Full Face'), (44.5, 'Técnicas tridimensionais')]),
    K(46.8, 50.0, 'presente', 'E AINDA', 'Aulas ao vivo e bônus'),
    K(50.0, 54.2, 'valor', 'UMA INSCRIÇÃO', 'Nenhum real a mais'),
    CURSOS_(54.3, 59.7, [(54.3, 'Todos os módulos'), (56.2, f'Com {G}acesso imediato{GF}')]),
    SAIBA(65.4, 67.4, 66.3),
    LOGO_(67.4, 69.2),
 ], trocas=[(['cima', 'a', 'mais'], ['SAIBA', 'MAIS'])]),
 '940537B5-B585-4FC8-B3CA-ADA617B53A80': dict(fim=92.2, publico='geral', zoom=[], cenas=[
    LOGO_(0, 1.75),
    K(1.8, 4.6, 'inf', VITAL, 'Seu último curso de harmonização da vida'),
    K(4.9, 11.7, 'aulas', 'ALÉM DAS AULAS TEÓRICAS', 'Materiais de apoio', chips=[(9.1, 'Para baixar'), (10.1, 'Artigos científicos')]),
    K(12.9, 17.0, 'aulas', 'NA PLATAFORMA', '1.200 aulas', 'de todos os temas'),
    K(19.8, 25.9, 'aulas', 'EM TODOS OS MÓDULOS', 'Intercorrências', chips=[(24.0, 'Material de apoio')]),
    K(26.0, 34.6, 'aulas', 'PARA DOWNLOAD', 'Material de apoio', chips=[(26.6, 'Lista de medicamentos'), (29.1, 'Artigos científicos'), (33.2, 'Resumos')]),
    K(46.0, 50.4, 'aulas', 'O MAIOR APOIO', 'Técnico e científico'),
    K(50.5, 59.3, 'aulas', 'TODOS OS TEMAS', 'Do básico ao avançado', chips=[(51.9, 'Toxina botulínica'), (57.9, 'Reologia dos preenchedores')]),
    K(74.6, 79.1, 'inf', 'NA PALMA DA SUA MÃO', 'Atualizações vitalícias', 'para o resto da sua vida'),
    LOGO_(79.1, 81.5),
    SAIBA(81.5, 84.0, 83.0),
    CURSOS_(84.6, 90.6, [(84.6, 'Acesso a tudo isso'), (87.4, 'Todos os temas de harmonização'), (89.1, f'{G}Para o resto da vida{GF}')]),
 ]),
 'E277AFF3-ED15-472E-86AE-F83C6B1BEB00': dict(fim=71.6, publico='geral', zoom=[(9.5, 11.7)], cenas=[
    K(0.1, 4.4, 'aulas', 'FALA, INJETOR DE ELITE', 'Já viu a plataforma do Combo Vitalício?'),
    LOGO_(4.4, 5.9),
    CURSOS_(5.9, 9.5, [(5.9, 'Todos os cursos que já fiz'), (7.5, f'E todos que {G}vou fazer{GF}')]),
    K(12.9, 18.0, 'aulas', 'MAIS DE', '1.200 aulas', 'de todos os temas de harmonização facial'),
    K(20.9, 23.8, 'inf', 'NA PLATAFORMA', '1.200 aulas', 'com atualizações vitalícias'),
    K(23.8, 30.2, 'aulas', 'TODOS OS TEMAS', 'Aula de tudo', chips=[(25.9, 'Bioestimuladores'), (27.6, 'Toxina'), (28.7, 'Anatomia em cadáver fresco')]),
    K(30.2, 36.5, 'presente', 'E MAIS', 'Bônus e livros', chips=[(30.2, 'Aulas bônus'), (31.5, 'Aulas ao vivo'), (34.2, 'Livro de olheiras'), (35.3, 'Livro de intercorrências')]),
    K(36.5, 47.0, 'aulas', 'CURSOS', 'Todos inclusos', chips=[(36.5, 'Full Face'), (39.5, 'Complicações'), (41.4, 'Corporal'), (42.5, 'Gestão de clínicas'),
                                                               (45.2, 'Fios'), (45.6, 'Preenchimento'), (46.4, 'Botox')]),
    K(53.1, 57.7, 'inf', 'MUITO MATERIAL', 'Atualizações para o resto da vida'),
    K(59.9, 66.4, 'valor', 'QUEM APROVEITAR', 'O menor valor da história', 'sem pagar um real a mais por atualizações'),
    SAIBA(66.4, 67.9, 67.4),
    K(67.9, 71.0, 'inf', VITAL, 'Seu último curso de harmonização da vida'),
 ]),
 'F77693E7-3FD8-4499-9C64-AB2E9B74BF20': dict(fim=75.8, publico='geral', zoom=[],
   cortes=[(57.35, 60.40), (68.40, 70.60)],      # "se inscrevendo dia 20 do 11" (data errada, ele corrige) e "pronto, entrega"
   remover=[('se', 57.0), ('pronto', 68.2)],      # palavras da legenda que o Whisper deixou na beira do corte (o áudio já está limpo)
   cenas=[
    K(0.1, 3.3, 'aulas', 'EM MENOS DE 1 MINUTO', 'Por que se inscrever?'),
    LOGO_(3.3, 4.7),
    K(4.7, 9.3, 'inf', VITAL, 'O seu último curso de harmonização'),
    K(10.4, 14.2, 'aulas', 'COMBO VITALÍCIO', '1.200 aulas'),
    K(14.2, 23.9, 'aulas', 'TODOS OS TEMAS', 'Do iniciante ao avançado', chips=[(16.8, 'Preenchimento'), (17.9, 'Botox'), (18.9, 'Fios'), (20.0, 'Gestão de clínicas')]),
    K(23.9, 34.9, 'aulas', 'E MAIS', 'Imersões avançadas', chips=[(25.0, 'Corporal'), (26.2, 'Rinomodelação'), (27.2, 'Olheiras'), (28.2, 'Complicações'),
                                                                 (29.4, 'Lábios'), (31.4, 'Full Face')]),
    K(34.9, 44.5, 'presente', 'BÔNUS', 'Livro, anatomia e aulas ao vivo', chips=[(34.9, 'Livro de olheiras'), (36.7, 'Anatomia em cadáver fresco'),
                                                                                   (39.9, 'Aulas ao vivo'), (43.5, 'Bioestimuladores')]),
    CURSOS_(44.5, 50.7, [(44.5, 'Todos os temas de harmonização'), (49.4, f'{G}Na palma da sua mão{GF}')]),
    K(50.7, 57.3, 'inf', 'ATUALIZAÇÕES VITALÍCIAS', 'Tudo que eu lançar até o fim da vida'),
    LIVE(60.42, 65.1, 20, f'Abertura das inscrições<br>{G}Black Friday Vitalícia{GF}', tData=60.6, tVivo=61.6, tTexto=62.5),
    SAIBA(65.2, 66.8, 66.0),
    K(70.62, 73.2, 'inf', 'ACESSO A TUDO ISSO', 'Para o resto da sua vida'),
    SAIBA(73.2, 74.4, 73.6),
 ]),
 'IMG_0884': dict(inicio=2.4, fim=80.6, publico='geral', zoom=[],
   cortes=[(37.12, 43.45)],      # notificação "Armazenamento do iPad Cheio" (38,1 a 42,3 s); corte nos silêncios. Voz começa em 2,6 s
   cenas=[
    K(2.45, 7.0, 'inf', 'COMBO VITALÍCIO', 'Seu último curso de harmonização da vida'),
    LOGO_(7.0, 9.6),
    K(10.2, 13.3, 'aulas', 'ATUALMENTE', '1.252 conteúdos'),
    K(13.4, 25.0, 'aulas', 'VOCÊ VAI TER', 'Cursos completos', chips=[(15.0, 'Preenchimento'), (16.4, 'Botox'), (18.0, 'Fios'), (19.5, 'Gestão de clínicas'),
                                                                     (20.6, 'Atenda Todo Santo Dia'), (22.3, 'Preenchimento Express')]),
    K(25.0, 39.5, 'aulas', 'CURSOS AVANÇADOS', 'Imersões e especializações', chips=[(25.8, 'Corporal'), (27.8, 'Rinomodelação'), (29.7, 'Olheiras'),
                                                                                    (31.8, 'Complicações'), (34.3, 'Preenchimento labial'), (36.5, 'Full Face')]),
    K(43.4, 53.0, 'presente', 'E MAIS', 'Livros, aulas e cursos', chips=[(43.4, 'Livro de olheiras'), (46.6, 'Aulas ao vivo'), (48.9, 'Anatomia'),
                                                                          (50.4, 'Bioestimuladores'), (52.4, 'Toxina Express')]),
    CURSOS_(54.9, 63.3, [(54.9, 'Centenas de módulos'), (56.4, 'Aulas ao vivo'), (59.1, f'Mais de {G}200 casos clínicos{GF}')]),
    K(63.4, 67.4, 'inf', 'NA PALMA DA SUA MÃO', 'Com atualizações vitalícias'),
    LOGO_(67.5, 70.0),
    SAIBA(72.6, 74.2, 73.4),
    K(74.2, 78.2, 'inf', 'ATUALIZAÇÕES', 'Para o resto da sua vida'),
 ]),
 'IMG_0886': dict(inicio=3.45, fim=62.1,   # voz termina em 61,8 s: sem tablet parado antes do CTA
   publico='geral', zoom=[], cenas=[
    K(3.45, 6.9, 'aulas', VITAL, 'Veja a plataforma'),
    K(7.0, 9.6, 'aulas', 'NA PLATAFORMA', '1.200 aulas', 'de todos os temas'),
    K(9.7, 17.0, 'aulas', 'TODOS OS TEMAS', 'Cursos completos', chips=[(9.7, 'Preenchimento'), (11.2, 'Botox'), (12.5, 'Fios'), (13.6, 'Gestão de clínicas'), (15.9, 'Corporal')]),
    K(17.0, 23.4, 'aulas', 'E MAIS', 'Imersões avançadas', chips=[(17.2, 'Rinomodelação'), (18.4, 'Olheiras'), (19.2, 'Complicações'), (20.8, 'Full Face')]),
    K(23.5, 28.0, 'presente', 'BÔNUS', 'Livros e aulas ao vivo', chips=[(23.5, 'Livros'), (24.3, 'Aulas ao vivo'), (25.9, 'Cursos bônus'), (27.0, 'Bioestimuladores')]),
    CURSOS_(28.1, 33.7, [(28.1, 'Todos esses módulos'), (32.2, f'Em {G}uma única compra{GF}')]),
    K(33.7, 44.7, 'inf', 'NUNCA MAIS PAGUE POR ATUALIZAÇÕES', 'Sempre mais conteúdo', chips=[(38.2, 'Mais aulas'), (39.1, 'Mais conteúdos'), (40.4, 'Mais atualizações')]),
    K(44.7, 49.2, 'valor', 'UMA INSCRIÇÃO', 'Atualizações para o resto da vida'),
    K(53.8, 58.2, 'inf', 'QUEM SE INSCREVER AGORA', 'Acesso a tudo isso'),
    SAIBA(58.2, 59.4, 58.7),
    LOGO_(59.6, 61.4),
 ]),
}

TEMPOS = ('s', 'e', 't', 'tA', 'tB', 'tFlip', 'tCal', 'tCarimbo', 'tToque', 'tSub', 'tVivo', 'tData', 'tHora', 'tTexto', 'tv', 'tTotal', 't20', 't19')

def mapa(inicio, cortes):
    """tempo do bruto -> tempo do vídeo editado (corta o começo e os trechos de `cortes`)."""
    def f(t):
        if t is None: return None
        x = max(t, inicio) - inicio
        for a, b in cortes:
            if t >= b: x -= b - a
            elif t > a: x -= t - a
        return round(x, 3)
    return f

def deslocar(obj, f):
    if isinstance(obj, list): return [deslocar(x, f) for x in obj]
    if isinstance(obj, dict):
        return {k: (f(v) if k in TEMPOS and isinstance(v, (int, float)) else deslocar(v, f)) for k, v in obj.items()}
    return obj

def trocar_seq(ws, trocas):
    """troca sequências de palavras (ex.: ['20','do','10'] -> ['19/10']) mantendo o tempo do trecho."""
    base = lambda w: re.sub(r'[^\wÀ-ú/]', '', w['t']).lower()
    for velho, novo in trocas:
        i = 0
        while i <= len(ws) - len(velho):
            if [base(w) for w in ws[i:i + len(velho)]] == velho:
                a, b, fim = ws[i]['s'], ws[i + len(velho) - 1]['e'], ws[i + len(velho) - 1]['fim']
                passo = (b - a) / len(novo)
                ws[i:i + len(velho)] = [dict(t=n, s=a + k * passo, e=a + (k + 1) * passo, fim=fim and k == len(novo) - 1) for k, n in enumerate(novo)]
            i += 1
    return ws

def datas_legenda(ws):
    """'19 do 10' / '20 do 10' viram '19/10' / '20/10' (pedido da Keila, 12/10/2026)."""
    return trocar_seq(trocar_seq(ws, [(['19', 'do', '10'], ['19/10'])]), [(['20', 'do', '10'], ['20/10'])])

if __name__ == '__main__':
    tr, saida = sys.argv[1], sys.argv[2]
    nomes = sys.argv[3:] or list(VIDEOS)
    for nome in nomes:
        v = VIDEOS[nome]; ini = v.get('inicio', 0); cortes = v.get('cortes', []); f = mapa(ini, cortes)
        ws = palavras(json.load(open(f'{tr}/{nome}.json')))
        ws = trocar_seq(ws, v.get('trocas', []) + [(['black', 'friday', 'vitalício'], ['BLACK', 'FRIDAY', 'VITALÍCIA']),
                                                   (['como', 'vitalício'], ['COMBO', 'VITALÍCIO'])])
        ws = datas_legenda(ws)
        base = lambda w: re.sub(r'[^\wÀ-ú/]', '', w['t']).lower()
        ws = [w for w in ws if not any(base(w) == p and abs(w['s'] - t) < .3 for p, t in v.get('remover', []))]
        ws = [w for w in ws if ini - .4 <= w['s'] < v['fim'] and not any(a <= (w['s'] + w['e']) / 2 < b for a, b in cortes)]   # pelo meio da palavra
        for a, b in cortes:     # a legenda quebra no corte, para não juntar frases de lados diferentes
            antes = [w for w in ws if (w['s'] + w['e']) / 2 < a]
            if antes: antes[-1]['fim'] = True
        leg = agrupar(ws)
        # legenda que começa dentro da abertura sem legenda (ex.: 'ATENÇÃO ALUNOS') não reaparece no fim dela
        leg = [g for g in leg if not any(a - .1 <= g['s'] < b for a, b in v.get('sem_legenda', []))]
        dur = f(v['fim'])
        manter = []; t0 = ini
        for a, b in cortes: manter.append((t0, a)); t0 = b
        manter.append((t0, v['fim']))
        cfg = dict(nome=nome, tema='bf', logo=LOGO, cursos=CURSOS, publico=v['publico'],
                   cta=v.get('cta') or ('cta19.mp4' if v['publico'] == 'alunos' else 'cta.mp4'),
                   trilha=v.get('trilha'), vol_trilha=v.get('vol_trilha', .2), inicio=ini, manter=manter,
                   dur=round(dur, 2), fim_fala=round(dur - .2, 2),
                   zoom=[(f(a), f(b)) for a, b in v['zoom']], tremor=[(f(a), f(b)) for a, b in v.get('tremor', [])],
                   sem_legenda=[(f(a), f(b)) for a, b in v.get('sem_legenda', [])],
                   cenas=deslocar(v['cenas'], f), legendas=deslocar(leg, f))
        json.dump(cfg, open(f'{saida}/{nome}.json', 'w'), ensure_ascii=False, indent=1)
        print(nome, cfg['publico'], cfg['dur'], '|', ' / '.join(' '.join(w['t'] for w in g['w']) for g in cfg['legendas']))
