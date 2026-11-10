#!/usr/bin/env python3
"""FEA: gera o projeto.json dos 20 criativos Elite Mentoring (pasta "10 roteiros", 07/11/2026).
Uso: python3 fea_projeto_criativos_elite.py TRABALHO > TRABALHO/projeto_criativos.json
Cada bruto é um criativo completo (gancho, método, diagnóstico, CTA), gravado de improviso a
partir do roteiro "Roteiros dos criativos" v4 (05/11/2026)."""
import json
import sys

T = sys.argv[1]

def G(texto, eyebrow="Pela primeira vez", fim=3.4):
    return {"tipo": "gancho", "ini": 0, "fim": fim, "eyebrow": eyebrow, "texto": texto}

def C(ancora, texto, eyebrow="", dur=3.6, **kw):
    return dict({"tipo": "card", "ancora": ancora, "dur": dur, "eyebrow": eyebrow, "texto": texto}, **kw)

ESQ = ["Responde o preço no direct", "Vende procedimento solto", "Ouve \u201cvou pensar\u201d"]
DIR = ["Avaliação com roteiro", "Plano de tratamento completo", "Preço depois do valor"]

def DIAG(ancora, esq=ESQ, dir=DIR, **kw):
    """Tela dividida do roteiro (SUA AVALIAÇÃO × O MÉTODO): Dr. em cima, comparação embaixo."""
    return dict({"tipo": "dividida", "ancora": ancora, "dur": 5.0, "eyebrow": "Diagnóstico gratuito · plano de ação",
                 "esq": esq, "dir": dir}, **kw)

def WHATS(ancora, **kw):
    return dict({"tipo": "whats", "ancora": ancora, "dur": 3.4,
                 "mensagens": ["Quanto é o ml?", "Qual o valor do lábio?", "Tem promoção?"]}, **kw)

# B-roll real do Drive (pastas "B roll ..."): avaliação com luva e marcação de planejamento.
# Conferido quadro a quadro: sem agulha, sem sangue, sem expressão de dor.
AVAL = [["IMG_8289", 2.0, 2.4], ["IMG_8292", 6.0, 2.4], ["IMG_8294", 5.0, 2.4]]
AVAL2 = [["IMG_8308", 2.0, 2.4], ["IMG_8293", 3.0, 2.4], ["IMG_8318", 4.0, 2.4]]
PLAN = [["IMG_8313", 2.0, 2.6], ["IMG_8313", 8.0, 2.4]]

def B(ancora, clipes, depois=3.6):
    return {"ancora": ancora, "clipes": clipes, "depois": depois}

def P(arq, *ss, dur=2.4):
    return [[arq, x, dur] for x in ss]

# Uma paciente diferente por vídeo (Keila 09/11: "coloque pacientes diferentes"), tiradas da pasta
# "00 - Brutos" (casos já publicados) e das pastas "B roll". Só avaliação, marcação, espelho ou o Dr.
# conversando: conferido quadro a quadro, sem agulha, cânula ou sangue. O vídeo 1 (aprovado em 09/11)
# fica com as tomadas dele.
BROLL = {
    1: [B("genial", AVAL), B("roteiro", PLAN, 15)],
    2: [B("roteiro", P("IMG_1744", 6, 10)), B("planos", P("IMG_1744", 20, 24), 15)],
    3: [B("realçar", P("IMG_1081", 0, 10)), B("métodos", P("IMG_1081", 26))],
    4: [B("olhar", P("IMG_0718", 0.5, 42)), B("plano", P("IMG_0718", 46), 28)],
    5: [B("mostrar", P("IMG_8295", 42, 46)), B("planejamento", P("IMG_8295", 50), 20)],
    6: [B("completo", P("IMG_2045", 8, 14), 6), B("planos", P("IMG_2045", 20), 15)],
    7: [B("avaliação", P("IMG_0725", 62, 66), 7), B("planejamento", P("IMG_0725", 70), 7)],
    8: [B("roteiro", P("IMG_2661", 2, 10), 10)],
    9: [B("avaliações", P("IMG_2509", 2), 10)],
    10: [B("baseado", P("IMG_2155", 0, 4, 18))],
    11: [B("metodologias", P("IMG_2503", 6, 10, 14))],
    12: [B("indicar", P("IMG_2072", 4, 20), 6), B("completar", P("IMG_2072", 36), 12)],
    13: [B("errando", P("IMG_1668", 0))],
    15: [B("avaliações", P("IMG_1077", 0.5, 4), 8)],
    16: [B("avaliação", P("IMG_2640", 0.5), 4)],
    17: [B("tratamentos", P("IMG_8318", 0.5, 13, 18.5), 4)],
    18: [B("metodologia", P("IMG_7285", 44, 48, 52), 9)],
    19: [B("avaliação", P("IMG_2485", 0.5), 12)],
    20: [B("roteiro", P("IMG_8311", 1)), B("planejamento", P("IMG_8311", 6), 9), B("individual", P("IMG_8311", 12))],
}

def FORM(ancora, **kw):
    return C(ancora, "Formulário rápido · *2 minutos*", "Preencha a aplicação", **kw)

def CTA(ancora, **kw):
    return dict({"tipo": "cta", "ancora": ancora, "fim": "final"}, **kw)

V = [
 ("1- Quase 100% na cadeira", [["IMG_9008", 0.45, 30.92, "exato"], ["IMG_9008", 32.98, 55.97, "exato"], ["IMG_9008", 58.92, 63.7]],
  [G("*Quase 100%* das pacientes fecham o tratamento"),
   C("carisma", "Não é carisma, preço *nem genialidade*", "O que não é", chips=["Carisma", "Preço"], riscar=True, dur=3.4),
   C("roteiro", "Um *método* replicável, com roteiro", "O que é", dur=3.6),
   CTA("clicar"), FORM("dois"), DIAG("avaliação gratuita")],
  [["IMG_9008", 24.11, 24.65]]),
 ("2- Não é sorte nem carisma, é método", [["IMG_9009", 0.0, 55.92, "exato"], ["IMG_9009", 68.75, 78.2, "exato"]],
  [G("Por que quase toda paciente *fecha no mesmo dia*?", "Pela primeira vez"),
   C("sorte", "Não é sorte nem carisma. *É método.*", "O segredo", chips=["Sorte", "Carisma"], riscar=True, dur=3.2),
   C("roteiro", "Roteiro, perguntas e *planos de tratamento*", "O método", dur=4.0),
   CTA("clicar"), FORM("dois"), DIAG("pré-diagnóstico")], []),
 ("3- Ela veio fazer só o lábio", [["IMG_9059", 0.0, 38.47, "exato"], ["IMG_9059", 41.2, 58.33, "exato"], ["IMG_9059", 67.56, 71.88, "exato"]],
  [G("Ela veio fazer *só o lábio*", "Avaliação completa"),
   C("saiu", "Saiu com o *tratamento completo*", "O resultado", chips=["Full face", "Bioestimulador", "Toxina"], dur=4.0),
   C("conjunto", "Ela não quer um lábio. *Quer um conjunto.*", "O que ela quer", dur=3.4),
   C("chaves", "As chaves da minha *conversão*", "Pela primeira vez", dur=3.6),
   DIAG("avaliação gratuita"), CTA("clicar"), FORM("demora")], []),
 ("4- Dificuldade em vender mais seringas", [["IMG_9069", 0.0, 38.84, "exato"], ["IMG_9069", 44.78, 61.73, "exato"], ["IMG_9069", 69.1, 73.44, "exato"], ["IMG_9069", 79.8, 85.4, "exato"]],
  [G("Dificuldade em vender *mais seringas*?", "O erro está na avaliação"),
   C("gerenciamento", "Um plano, *não um procedimento*", "O rosto inteiro", chips=["Toxina", "Preenchimento", "Bioestimulador", "Fios"], dur=4.2),
   C("metodologia", "Minha metodologia *completa*", "Pela primeira vez", dur=3.4),
   WHATS("seringas", depois=8), DIAG("avaliação de diagnóstico", esq=["Vende seringa", "Compete por preço", "Plano de um procedimento"], dir=["Olha o rosto inteiro", "Plano de tratamento completo", "Ticket maior"]), CTA("clicar"), FORM("demora")], []),
 ("5- Você perde a paciente na hora do preço", [["IMG_9070", 0.0, 61.5], ["IMG_9070", 68.0, 68.8]],
  [G("Você perde a paciente *na hora do preço*", "O momento do preço"),
   C("agregar", "Valor *antes* do preço", "A ordem", chips=["O que", "Como", "Por que", "Resultado"], dur=4.2),
   C("pilares", "Os 4 pilares da *conversão*", "Onde você erra", chips=["Planejamento", "Avaliação", "Marketing", "Vendas"], dur=4.0),
   C("método", "O método que cresce *há 5 anos*", "Pela primeira vez", dur=3.4),
   DIAG("avaliação gratuita"), CTA("clicar"), FORM("formulário pra")], []),
 ("6- Você não precisa de mais pacientes", [["IMG_9066", 0.0, 53.4]],
  [G("Você não precisa de *mais pacientes*", "Ticket maior"),
   C("clínicas", "Menos pacientes, *ticket maior*", "Planos mais completos", chips=["Toxina", "Preenchimento", "Bioestimulador"], dur=4.2),
   C("primeira", "Meu método, *pela primeira vez*", "No seu dia a dia", dur=3.4),
   DIAG("diagnóstico gratuito"), CTA("clicar"), FORM("dois")], []),
 ("7- A agenda lotada tem método", [["IMG_9077", 0.2, 52.6]],
  [G("A agenda lotada *tem método*", "Pela primeira vez"),
   C("existe", "O método que *nunca mostrei*", "Avaliação · planejamento · vendas", chips=["Avaliação", "Marketing", "Vendas"], dur=4.2),
   DIAG("avaliação de diagnóstico"), CTA("clicar"), FORM("dois"),
   C("vagas", "Vagas *semanais* limitadas", "Seleção individual", dur=3.4)], []),
 ("8- Quando a paciente diz vou pensar", [["IMG_9073", 3.1, 68.4]],
  [G("“Vou pensar”", "A paciente adorou tudo e saiu dizendo"),
   C("quase", "Taxa de conversão de *quase 100%*", "No meu consultório", dur=3.4),
   C("barato", "Não é preço. *É método.*", "O motivo", chips=["Roteiro", "Planejamento", "Método"], dur=4.0),
   DIAG("avaliação de diagnóstico"), CTA("clicar"), FORM("demora")], []),
 ("9- Sala alugada e agenda vazia", [["IMG_9076", 0.0, 58.4]],
  [G("Sozinha numa sala alugada, *como ele faz isso?*", "Você"),
   C("comecei", "Eu também comecei *assim*", "Sem pacientes, conversão baixa", dur=3.8),
   C("metodologia", "O que mudou: *um método*", "Avaliação · planejamento · vendas", chips=["Avaliação", "Execução", "Vendas"], dur=4.0),
   DIAG("avaliação de diagnóstico"), CTA("clicar")], []),
 ("10- Técnica boa não basta para converter", [["IMG_9060", 0.0, 62.5]],
  [G("Técnica boa *não basta* para converter", "O que mudou minha agenda"),
   C("instagram", "Instagram + *conversão*", "O que faltava", chips=["Redes sociais", "Avaliação", "Planejamento"], dur=4.2),
   C("método", "Um método, *pela primeira vez*", "", dur=3.2),
   CTA("clicando"), DIAG("avaliação de diagnóstico")], []),
 ("11- O mesmo paciente não faz o consultório crescer", [["IMG_9078", 0.0, 65.3]],
  [G("O mesmo paciente *não faz você crescer*", "Captação + conversão"),
   C("captação", "Captação, conversão e *previsibilidade*", "Faturamento constante", dur=4.0),
   C("primeira", "Todo o meu método, *pela primeira vez*", "Vendas e marketing", dur=3.6),
   CTA("clicando"), DIAG("avaliação gratuita")], []),
 ("12- Full face acima de 5 mL, o erro está no método", [["IMG_9079", 0.0, 64.9]],
  [G("Full face acima de 5 mL *não fecha*?", "Uma conversa no consultório"),
   C("método", "O erro está *no método*", "Indicação e plano completo", chips=["Toxina", "Bioestimulador", "Tecnologias"], dur=4.2),
   C("metodologia", "Metodologia *completa*", "Pela primeira vez", chips=["Avaliação", "Planejamento", "Vendas"], dur=4.0),
   DIAG("avaliação de diagnóstico"), CTA("clicar"), FORM("dois")], []),
 ("13- Sei injetar, mas não sei vender", [["IMG_9081", 0.0, 47.0]],
  [G("“Sei injetar, mas *não sei vender*”", "A queixa que mais escuto"),
   C("método", "Meu método *completo* de crescimento", "Pela primeira vez", chips=["Vendas", "Marketing"], dur=4.0),
   DIAG("avaliação de diagnóstico"), CTA("clicar"),
   C("vagas", "Avaliações *um a um*", "Vagas limitadas por semana", dur=3.4)], []),
 ("14- Procuro 3 profissionais de harmonização", [["IMG_9082", 0.0, 9.0], ["IMG_9082", 11.95, 23.05], ["IMG_9082", 26.0, 41.8]],
  [G("Procuro *3 profissionais*", "Harmonização facial"),
   CTA("clicar"), C("três pessoas", "*3 vagas* gratuitas", "Avaliação de diagnóstico", dur=3.4, depois=12),
   DIAG("participará")], []),
 ("15- Clínica de alto padrão", [["IMG_9143", 0.5, 64.7]],
  [G("Você sonha com uma clínica *de alto padrão*?", "A minha trajetória"),
   C("marketing", "Marketing, vendas e *conversão*", "O que mudou", chips=["Avaliação", "Marketing", "Vendas"], dur=4.0),
   CTA("clicar"), FORM("dois"), DIAG("apto")], []),
 ("16- Aumente sua conversão em harmonização", [["IMG_9145", 0.5, 41.0], ["IMG_9145", 43.6, 44.6]],
  [G("Quer aumentar sua *conversão*?", "Fica neste vídeo"),
   C("metodologia", "Avaliação, marketing e *vendas*", "Pela primeira vez", dur=3.6),
   CTA("clicar"), FORM("dois"), DIAG("avaliação com")], []),
 ("17- O método por trás da clínica de alto padrão", [["IMG_9147", 0.2, 31.4], ["IMG_9147", 35.1, 57.0]],
  [G("Clínica de alto padrão e *tratamentos completos*", "Eu sempre sonhei com"),
   C("desenvolvi", "Isso acontece porque *existe um método*", "Pela primeira vez", chips=["Marketing", "Vendas"], dur=4.0),
   DIAG("diagnóstico"), CTA("clicar")], []),
 ("18- Planejamento full face que converte", [["IMG_9148", 0.0, 54.3]],
  [G("Planejamento full face *que converte*", "Existe um método"),
   C("passos", "Passos simples e *replicáveis*", "Planos mais amplos e rentáveis", dur=4.0),
   CTA("clicar"), DIAG("avaliação de diagnóstico")], []),
 ("19- A jornada do paciente começa no WhatsApp", [["IMG_9149", 0.1, 53.3]],
  [G("A jornada do paciente *começa no WhatsApp*", "Do direct à conversão"),
   WHATS("dificuldade", depois=5), C("captação", "Onde a venda *escapa*", "Os passos da jornada", chips=["Captação", "Avaliação", "Planejamento"], seta=True, dur=4.4),
   C("método", "Existe *um método*", "", dur=3.2),
   CTA("clicar"), DIAG("selecionadas")], []),
 ("20- Quase 100% de conversão, nem sempre foi assim", [["IMG_9150", 0.0, 10.95], ["IMG_9150", 14.35, 68.5]],
  [G("Conversão de *quase 100%*", "Nem sempre foi assim"),
   C("roteiro", "O que não pode faltar *na avaliação*", "A metodologia", chips=["Roteiro", "Planejamento", "Opções"], dur=4.4),
   C("individual", "Cada paciente *é individual*", "", dur=3.2),
   CTA("clicar"), FORM("formuláriozinho"), DIAG("diagnóstico gratuito")], []),
]

CORRECOES = [
    [r"(?i)\b(saiba|seba|sabe a|saba) ?mais\b", "Saiba mais"], [r"(?i)\bsabamais\b", "Saiba mais"],
    [r"\bcom face\b", "full face"], [r"\ba 5 anos\b", "há 5 anos"],
    [r"\bcompleto formulário\b", "completa o formulário"], [r"\bCompleto o formulário\b", "completa o formulário"],
    [r"^que fez aumentar", "o que fez aumentar"], [r"\bpro melhor\b", "para o melhor"],
    [r"completa que o formulário espera", "completa o formulário e espera"],
    [r"\belas tem\b", "elas têm"], [r"\bnão tem mais pacientes", "não têm mais pacientes"],
]

# revisão da Keila (09/11): zoom no Dr. sem as pernas, cortes sem salto e sem encurtar pausas
AJUSTES = {
    1: {"zoom": [1.45, 0.5, 0.40], "zoom_alterna": 1.12, "apertar": False},
    2: {"zoom": [1.45, 0.5, 0.40], "zoom_alterna": 1.12, "apertar": False},
    # "para o seu... para a tua": sai o tropeço inteiro (38,47 a 41,2 s) e a legenda recebe o
    # "para a tua" que a transcrição tinha esticado sobre o tropeço
    3: {"zoom_alterna": 1.0, "remover_legenda": [["IMG_9059", 38.4, 41.68]],
        "inserir_legenda": [["IMG_9059", 41.25, 41.42, "para"], ["IMG_9059", 41.42, 41.52, "a"],
                            ["IMG_9059", 41.52, 41.68, "tua"]]},
}

videos = []
for saida, trechos, cartelas, remover in V:
    num = int(saida.split("-")[0])
    videos.append(dict({"saida": f"{T}/out/{saida}.mp4", "trechos": trechos, "cartelas": cartelas,
                        "remover_legenda": remover, "correcoes": CORRECOES, "broll": BROLL.get(num, [])},
                       **AJUSTES.get(num, {})))
print(json.dumps({"ffmpeg": None, "fontsdir": f"{T}/fonts", "assets": f"{T}/assets", "brutos": f"{T}/brutos", "broll": f"{T}/broll",
                  "transcricoes": f"{T}/tr", "videos": videos}, ensure_ascii=False, indent=1))
