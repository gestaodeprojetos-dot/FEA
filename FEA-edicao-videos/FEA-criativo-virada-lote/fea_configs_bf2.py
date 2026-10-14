"""FEA: roteiros do 2º lote da Black Friday Vitalícia (13/10/2026, "criativos black aeroporto", Dr. João no aeroporto).
Mesmo motor e mesmas cenas do fea_configs_bf.py. Público geral: live de abertura 20/10 às 20h, CTA de 20 de outubro.
Contagem: 5 dias = 15/10 (quinta), 4 = 16/10, 3 = 17/10, 2 = 18/10, amanhã = 19/10, hoje = 20/10 (terça).
Uso: python3 fea_configs_bf2.py PASTA_TRANSCRICOES PASTA_SAIDA [NOME ...]"""
import sys
from fea_configs_bf import K, LOGO_, SAIBA, CURSOS_, LIVE, CONTA, G, GF, VITAL, gerar

SUB = 'Abertura das inscrições · 20/10 às 20h'
ULTIMO = ('aulas', VITAL, 'Seu último curso de harmonização facial', 'da vida')
SINO = ('sino', 'LIVE DE ABERTURA')

def NUM(e, de, para, tflip, topo):
    return dict(tipo='gancho', s=0, e=e, modo='numero', de=str(de), para=str(para), tFlip=tflip, topo=topo, grande='dias', sub=SUB)
def CAL(e, de, para, tflip, grande, alerta=False, sub=SUB):
    return dict(tipo='gancho', s=0, e=e, modo='calendario', de=de, para=para, tFlip=tflip, alerta=alerta,
                topo='AS INSCRIÇÕES ABREM', grande=grande, sub=sub)
def B(**k):
    return dict(publico='geral', cta='cta.mp4', trilha='urgencia', vol_trilha=.24, **k)

VIDEOS = {
 # ---------------- contagem regressiva até a abertura (20/10) ----------------
 'IMG_0892': B(inicio=.5, fim=16.0, zoom=[(11.0, 13.9)], cenas=[       # "Faltam 5 dias"
    NUM(2.45, 6, 5, .78, 'FALTAM'), LOGO_(3.5, 5.0),
    K(5.05, 9.35, *ULTIMO), SAIBA(9.55, 11.0, 10.15),
    LIVE(13.95, 16.0, 20, f'Abertura das inscrições<br>{G}te vejo lá{GF}', tData=14.0, tVivo=14.3, tTexto=14.6)]),
 'IMG_0894': B(inicio=.6, tol_inicio=.6, fim=18.5, zoom=[(13.95, 15.5), (17.75, 18.5)], cenas=[    # "4 dias"
    NUM(2.4, 5, 4, .85, 'FALTAM'), LOGO_(2.45, 3.65),
    LIVE(3.7, 7.55, 20, f'Live de abertura<br>{G}das inscrições{GF}', tData=3.85, tVivo=6.75, tTexto=7.0),
    SAIBA(7.6, 9.45, 8.85),
    K(9.5, 13.9, *SINO, 'Ative as notificações', chips=[(10.0, 'Notificações'), (10.9, 'Agenda'), (12.4, 'Live de abertura')]),
    K(15.55, 17.75, *ULTIMO)]),
 'IMG_0895': B(inicio=.1, fim=15.8, zoom=[(7.0, 8.1)], cenas=[       # "Em três dias"
    NUM(2.5, 4, 3, .45, 'EM'), LOGO_(2.55, 3.65),
    K(3.7, 6.95, 'presente', 'NA LIVE DE ABERTURA', 'Todos os bônus', 'para quem estiver ao vivo'),
    SAIBA(8.1, 9.75, 9.0),
    K(9.8, 13.95, *SINO, 'Ative as notificações', chips=[(10.5, 'Notificações'), (12.1, 'Agenda'), (12.9, 'Live de abertura')]),
    LIVE(14.0, 15.8, 20, f'Te espero lá<br>{G}em três dias{GF}', tData=14.05, tVivo=14.3, tTexto=14.7)]),
 'IMG_0896': B(inicio=.35, fim=21.2, zoom=[(6.4, 8.0)], cenas=[       # "Em apenas dois dias"
    NUM(2.75, 3, 2, 1.0, 'EM'), LOGO_(2.8, 3.95),
    K(3.97, 6.4, *ULTIMO), SAIBA(8.0, 9.45, 8.55),
    K(9.5, 14.15, *SINO, 'Ative os lembretes', chips=[(9.6, 'Lembretes'), (10.7, 'Notificações'), (11.9, 'Agenda'), (12.9, 'Live de abertura')]),
    K(14.2, 18.6, 'presente', 'PARA QUEM ESTIVER AO VIVO', 'Bônus especiais', chips=[(14.8, 'Bônus presenciais'), (16.7, 'Bônus especiais')]),
    LIVE(18.65, 21.2, 20, f'Live de abertura<br>{G}te vejo lá{GF}', tData=18.75, tVivo=19.5, tTexto=20.4)]),
 'IMG_0897': B(inicio=.3, fim=18.1, zoom=[(7.0, 8.0)], cenas=[        # "Amanhã"
    CAL(2.2, 19, 20, .75, 'amanhã'), LOGO_(2.2, 3.3),
    K(3.35, 7.0, *ULTIMO), SAIBA(8.0, 9.6, 8.7),
    K(9.65, 13.35, *SINO, 'Ative as notificações', chips=[(9.7, 'Notificações'), (11.25, 'Lembretes'), (12.1, 'Agenda')]),
    K(13.4, 16.7, 'presente', 'PARA QUEM ESTIVER AO VIVO', 'Todos os bônus', chips=[(14.4, 'Todos os bônus'), (15.4, 'Bônus presenciais')]),
    LIVE(16.75, 18.1, 20, 'Te vejo lá', tData=16.8, tVivo=17.0, tTexto=17.3)]),
 'IMG_0898': B(inicio=.4, fim=26.3, zoom=[(22.5, 26.3)], cenas=[       # "Hoje"
    CAL(2.15, 20, 20, 99, 'hoje', alerta=True, sub='Live de abertura às 20h'), LOGO_(2.2, 3.5),
    K(3.52, 5.95, 'aviao', 'EMBARQUE', 'Pega esse voo comigo', 'para o resto da vida'),
    CURSOS_(6.0, 12.5, [(6.0, 'Todas as atualizações'), (8.38, 'Todas as novidades'), (9.54, 'Todos os cursos'),
                        (10.7, f'Tudo que eu {G}ainda vou fazer{GF}')]),
    K(12.55, 16.8, 'valor', 'UM ÚNICO VALOR', 'Nenhum real a mais', 'se inscreve uma vez, atualizações vitalícias'),
    SAIBA(17.4, 19.0, 18.1),
    LIVE(19.05, 22.45, 20, f'Live de abertura<br>{G}das inscrições{GF}', tData=19.15, tVivo=21.4, tTexto=21.75)]),
 # ---------------- inscrições abertas (a partir de 20/10) ----------------
 'IMG_0891': B(inicio=.35, fim=18.95, zoom=[(2.3, 4.8), (7.2, 9.5)], cenas=[       # "Tô atrasado para pegar meu voo"
    K(.35, 2.3, 'aviao', 'PORTÃO DE EMBARQUE', 'Não se atrase', 'para a Black Friday Vitalícia'),
    LOGO_(4.8, 6.0), K(9.5, 13.8, *ULTIMO), SAIBA(14.6, 16.85, 15.15),
    K(16.9, 18.95, 'aviao', 'EMBARQUE', 'Pega esse voo comigo', 'Black Friday Vitalícia')]),
 'IMG_0899': B(inicio=.4, fim=23.4, zoom=[(10.6, 11.8), (19.2, 23.4)], cenas=[      # "Bora comigo"
    K(.4, 3.4, *ULTIMO), LOGO_(3.45, 4.65),
    K(4.7, 8.95, 'inf', 'INSCRIÇÕES ABERTAS', 'Black Friday Vitalícia', 'seu último curso da vida'),
    SAIBA(9.25, 10.6, 10.1),
    CURSOS_(11.8, 16.95, [(12.65, 'Todos os cursos que já fiz'), (13.91, f'Todos que {G}ainda vou fazer{GF}'), (15.35, 'Atualizações vitalícias')]),
    SAIBA(17.25, 19.2, 18.5)]),
 'IMG_0900': B(inicio=.2, fim=22.2, zoom=[(3.95, 7.6), (9.6, 12.5), (16.3, 18.4)], cenas=[     # "Últimos dias"
    K(.2, 3.9, 'inf', 'INSCRIÇÕES ABERTAS', 'Black Friday Vitalícia', 'todos os cursos, para sempre, por um único preço'),
    SAIBA(12.55, 14.0, 13.0), K(14.02, 16.3, *ULTIMO), SAIBA(18.4, 19.8, 18.9), LOGO_(20.6, 22.2)]),
 'IMG_0901': B(inicio=.1, fim=25.6, zoom=[(3.35, 5.85), (24.35, 25.6)], cenas=[      # "Vou virar o lote"
    LOGO_(1.15, 2.95), SAIBA(5.9, 7.7, 6.6), K(8.7, 11.6, *ULTIMO),
    K(11.65, 14.55, 'inf', 'PARA O RESTO DA VIDA', 'Atualizações vitalícias', 'tudo que eu ainda vou fazer'),
    CURSOS_(14.6, 23.4, [(15.44, 'Todos os cursos'), (16.04, 'Toxina botulínica'), (17.04, 'Preenchimento'), (17.62, 'Bioestimuladores'),
                         (18.54, f'Harmonização {G}facial e corporal{GF}'), (22.16, f'Na {G}palma da sua mão{GF}')]),
    SAIBA(23.45, 24.35, 23.9)]),
 'IMG_0902': B(inicio=.15, fim=23.45, zoom=[(22.2, 23.45)], cenas=[      # "Nunca mais compre um curso"
    K(.15, 3.45, 'valor', VITAL, 'Nunca mais compre um curso', 'de harmonização facial'),
    LOGO_(3.5, 5.15),
    CURSOS_(5.2, 10.85, [(6.36, 'Preenchimento facial'), (7.46, 'Bioestimuladores'), (8.32, 'Fios'), (9.04, 'Toxina botulínica'),
                         (10.0, f'{G}E muito mais{GF}')]),
    K(10.9, 13.6, 'inf', 'PARA O RESTO DA VIDA', 'Atualizações vitalícias'),
    K(13.65, 20.6, 'valor', 'UM ÚNICO VALOR', 'Paga uma vez', 'e nunca mais um real a mais',
      chips=[(13.7, 'Novos cursos'), (15.28, 'Atualizações'), (16.16, 'Congressos')]),
    SAIBA(20.65, 22.2, 21.2)]),
 'IMG_0903': B(inicio=.15, fins=[31.16, 28.24], fim=37.0, zoom=[(14.95, 15.85), (18.75, 20.5), (32.6, 35.4)], cenas=[    # "Quanto você já gastou"
    K(.15, 2.95, 'valor', 'PERGUNTA RÁPIDA', 'Quanto você já gastou em cursos?', 'toda a sua vida'),
    dict(CONTA(3.0, 11.0, [(3.04, 'Toxina e preenchimento', None, None), (4.5, 'Fios e bioestimuladores', None, None),
                           (5.48, 'Especializações', None, None), (6.28, 'Congressos', None, None)],
               tTotal=9.3, total=False, totalTexto='R$ 0', topo='QUANTO VOCÊ JÁ GASTOU'), rotulo='A MAIS, PARA SEMPRE'),
    K(11.0, 13.05, 'inf', 'PARA O RESTO DA VIDA', 'Atualizações vitalícias'),
    LOGO_(13.1, 14.95),
    CURSOS_(15.85, 18.75, [(15.88, 'Todos os cursos que já fiz'), (17.2, f'Todos que {G}ainda vou fazer{GF}')]),
    K(20.55, 27.0, 'aulas', 'ATÉ O FIM DA VIDA', 'Tudo que eu lançar de novo',
      chips=[(20.6, 'Técnicas'), (21.72, 'Abordagens'), (22.7, 'Atualizações'), (23.72, 'Novidades')]),
    K(27.05, 31.25, 'valor', 'UM ÚNICO VALOR', 'Nenhum real a mais', 'se inscrevendo uma vez na Black Friday Vitalícia'),
    SAIBA(31.3, 32.6, 32.0), LOGO_(35.42, 37.0)]),
 'IMG_0904': B(inicio=.1, fim=21.05, zoom=[(2.3, 4.1), (12.9, 16.6), (19.9, 21.05)], cenas=[      # "Último dia"
    K(.1, 2.25, 'cal', VITAL, 'Último dia', 'para se inscrever'),
    K(4.1, 8.3, 'valor', 'UM ÚNICO VALOR', 'Paga uma vez', 'e nunca mais paga por atualizações'),
    CURSOS_(8.4, 12.9, [(8.46, 'Todos os cursos que já fiz'), (10.0, f'Todos que {G}ainda vou fazer{GF}'), (11.02, 'Atualizações vitalícias')]),
    SAIBA(16.65, 18.2, 17.0), LOGO_(18.2, 19.9)]),
 # ---------------- refações de 13/10/2026 (pasta 1. VENDAS, Dr. no rio) ----------------
 # Base = vídeo já editado por outra pessoa (o bruto não está no Drive): áudio com o vento removido (DeepFilterNet),
 # legenda antiga gravada apagada (inpaint) e coberta pela legenda nova mais baixa (cap_top); a manchete antiga dos
 # primeiros 2,8 s fica embaixo da abertura em tela cheia; o CTA antigo sai e entra o CTA da Black.
 'V08': B(inicio=0, fim=18.62, cortes=[(8.32, 9.55)], cap_top=1420, zoom=[(9.6, 11.4)],      # "8- Inscrições abertas"
   trocas=[(['black', 'friday', 'e', 'vitalícia'], ['Black', 'Friday', 'Vitalícia'])], cenas=[
    LOGO_(0, 2.9), K(3.45, 6.1, *ULTIMO), SAIBA(6.55, 8.3, 6.7),
    K(11.45, 13.15, 'inf', 'INSCRIÇÕES ABERTAS', 'Black Friday Vitalícia', 'todos os cursos, para sempre, por um único preço'),
    K(13.3, 15.95, 'inf', 'PARA O RESTO DA SUA VIDA', 'Estaremos juntos'),
    LOGO_(16.1, 18.62)]),
 'V13': B(inicio=0, fim=15.85, cap_top=1420, zoom=[(3.05, 4.9), (7.6, 8.85), (10.6, 12.2)], cenas=[    # "13- Último dia de inscrições"
    LOGO_(0, 2.9), K(4.95, 7.4, *ULTIMO), SAIBA(8.85, 10.5, 9.3),
    K(12.25, 14.2, 'cal', VITAL, 'Último dia', 'para se inscrever'), SAIBA(14.25, 15.85, 14.95)]),
 # ---------------- influencer (14/10/2026, "FEA-influencer-black-roteiro1-v2") ----------------
 # Ela diz "Eu sou uma inteligência artificial" 2 vezes: fica só a 2ª (Keila). O vídeo já tem o rótulo
 # "Dr. João Pithon" gravado em y 1344 a 1421 (12,6 a 15,4 s): só nesse trecho a legenda desce para
 # bem abaixo dele (cap_faixas), no resto fica na altura normal (Keila, 14/10: a legenda ficava em cima do nome).
 'INF1': B(inicio=2.8, fim=23.5, cap_faixas=[(12.5, 16.2, 1540)], trocas=[(['dr', 'joão'], ['Dr.', 'João'])], zoom=[(2.8, 4.85), (5.15, 8.0)], cenas=[
    K(8.0, 9.55, 'aluno', 'VOCÊ PRECISA', 'Estudar anatomia'),
    LIVE(9.65, 12.4, 20, 'Abertura das inscrições', tData=10.45, tVivo=11.6, tTexto=11.9),
    K(13.2, 16.15, 'inf', 'PELA PRIMEIRA VEZ', 'Black Friday Vitalícia', 'todos os cursos, para sempre, por um único preço'),
    CURSOS_(16.2, 21.45, [(16.27, 'Acesso vitalício'), (17.97, 'Todos os cursos do Dr. João'), (19.31, f'Inclusive os que {G}ainda vai lançar{GF}')]),
    SAIBA(21.65, 23.5, 22.6)]),
 # 14/10/2026, "FEA-influencer-black-edema-v2" (720p, a montagem escala). Personagem de IA com edema labial: selo
 # discreto de cena simulada com IA no começo (a 1ª influencer se apresenta como IA; esta não). Nome gravado
 # "Dr. João Pithon" em y≈1420 de 14,0 a 16,1 s: legenda desce nesse trecho.
 'INF2': B(inicio=.2, fim=21.9, cap_faixas=[(13.9, 16.25, 1560)], trocas=[(['dr', 'joão'], ['Dr.', 'João'])],
   selo=(.2, 8.0, 'Cena simulada com inteligência artificial'),
   zoom=[(2.2, 4.7), (8.0, 11.5)], tremor=[(4.08, 4.64)], cenas=[
    K(5.0, 7.75, 'aulas', 'SEGURANÇA', 'Anatomia antes da técnica'),
    LIVE(11.75, 13.9, 20, 'Abertura das inscrições', tData=12.3, tVivo=13.3, tTexto=13.5),
    K(13.95, 16.15, 'inf', VITAL, 'Acesso vitalício', 'todos os cursos, para sempre, por um único preço'),
    CURSOS_(16.2, 20.45, [(16.2, 'Acesso para sempre'), (17.48, 'Todos os cursos do Dr. João'), (18.76, f'Inclusive os que {G}ainda vai lançar{GF}')]),
    SAIBA(20.5, 21.9, 21.27)]),
}


if __name__ == '__main__':
    gerar(VIDEOS, sys.argv[1], sys.argv[2], sys.argv[3:])
