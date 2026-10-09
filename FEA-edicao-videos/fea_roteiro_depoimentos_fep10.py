#!/usr/bin/env python3
"""FEA: roteiro dos 6 depoimentos FEP Experience 10 (out/2026) -> FEA-projeto-depoimentos-fep10.json.

Tempos em segundos do bruto, tirados da transcrição com tempo por palavra.
Uso: python3 fea_roteiro_depoimentos_fep10.py PASTA_TRABALHO
"""
import json
import os
import sys

T = sys.argv[1]

# cada vídeo: trechos mantidos, legendas [ini, fim, pt, es], destaques [ini, fim, PT, ES]
V = [
    dict(id="d1", n=26, crop=dict(cx=1920, h=1700),
         trechos=[[0.0, 37.2]],
         legendas=[
             [0.00, 2.18, "Olá, eu sou a Dra. Estefany Mota,", "Hola, soy la doctora Estefany Mota,"],
             [2.36, 4.38, "sou especialista em medicina estética", "soy especialista en medicina estética,"],
             [4.90, 6.06, "e venho do Paraguai.", "vengo desde Paraguay."],
             [6.30, 9.26, "Conheci o Dr. João em um congresso", "Conocí al doctor João en un congreso"],
             [9.26, 11.12, "de medicina estética, há muitos anos.", "de medicina estética hace muchos años."],
             [11.80, 15.30, "Assisti a uma aula presencial de rinomodelação",
              "Asistí a un aula presencial de rinomodelación"],
             [15.30, 17.50, "no congresso e me apaixonei pelas técnicas dele.",
              "en el congreso y me enamoré de sus técnicas."],
             [17.74, 20.60, "Desde então, comprei os cursos online,", "Desde entonces compré los cursos online,"],
             [20.60, 23.40, "que me ajudaram muito durante toda a minha carreira,",
              "que me ayudaron muchísimo durante toda mi carrera,"],
             [23.40, 25.96, "porque ele realmente mostra", "porque él realmente muestra"],
             [25.96, 28.38, "e nos ajuda com todas as dúvidas que temos.",
              "y nos ayuda con todas las dudas que tenemos."],
             [28.38, 31.90, "E agora, para fechar com chave de ouro,", "Y ahora, para cerrar con broche de oro,"],
             [31.90, 35.12, "vim ao curso presencial em São Paulo", "vine al curso presencial en São Paulo"],
             [35.12, 36.94, "e estou amando a experiência.", "y me está encantando la experiencia."],
         ],
         destaques=[
             [12.90, 17.50, "Rinomodelação", "Rinomodelación"],
             [31.90, 35.12, "Curso presencial", "Curso presencial"],
         ]),
    dict(id="d2", destaques_dub=[["un antes y un después", "Antes y después"], ["la calidad de los videos", "Calidad de los videos"], ["volver a ver las clases", "Volver a ver las clases"], ["muy seguros", "Muy seguros"]], n=27, crop=dict(cx=1950, h=1440),
         trechos=[[0.0, 8.45], [9.62, 12.40], [14.26, 18.98], [36.86, 55.70],
                  [60.26, 62.95], [66.64, 71.55], [72.00, 73.90], [74.82, 82.05]],
         legendas=[
             [0.00, 2.86, "Conheci o Dr. João através das redes sociais,",
              "Conocí al doctor João a través de las redes sociales,"],
             [3.56, 5.42, "faço a FEP Online,", "hago la FEP Online,"],
             [6.00, 8.32, "que foi um divisor de águas para mim.", "que fue un antes y un después para mí."],
             [9.70, 12.28, "Iniciei os meus preenchimentos de olheira", "Empecé mis rellenos de ojeras"],
             [14.32, 16.56, "assistindo às lives do Dr. João,", "viendo los directos del doctor João,"],
             [17.14, 18.88, "seguindo ele no Instagram.", "siguiéndolo en Instagram."],
             [36.92, 41.00, "A FEP Online, a qualidade dos vídeos,", "La FEP Online, la calidad de los videos,"],
             [41.58, 44.28, "os detalhes, super capacita vocês", "los detalles, los capacita muchísimo"],
             [44.28, 47.82, "a fazerem o melhor trabalho possível,", "para hacer el mejor trabajo posible,"],
             [47.98, 51.34, "de forma online, em casa, no conforto,", "de forma online, en casa, con comodidad,"],
             [51.68, 52.90, "a qualquer momento,", "en cualquier momento,"],
             [53.04, 55.60, "com essa possibilidade de revisitar as aulas,",
              "con la posibilidad de volver a ver las clases,"],
             [60.32, 62.82, "e isso com certeza é um diferencial.", "y eso, sin duda, es un diferencial."],
             [66.72, 70.02, "O trabalho do Dr. João dispensa comentários,",
              "El trabajo del doctor João no necesita comentarios,"],
             [70.36, 71.46, "ele é sensacional:", "es sensacional:"],
             [72.06, 73.82, "a didática, a forma de falar,", "la didáctica, la forma de hablar,"],
             [74.88, 76.60, "a forma de apresentar o trabalho.", "la forma de presentar el trabajo."],
             [76.98, 79.64, "Ele também deixa a gente muito confortável",
              "Él también nos hace sentir muy cómodos"],
             [79.64, 82.00, "e muito seguro para realizar os procedimentos.",
              "y muy seguros para realizar los procedimientos."],
         ],
         destaques=[
             [6.42, 8.32, "Divisor de águas", "Antes y después"],
             [39.60, 41.00, "Qualidade dos vídeos", "Calidad de los videos"],
             [53.26, 55.60, "Revisitar as aulas", "Volver a ver las clases"],
             [79.64, 82.00, "Muito seguro", "Muy seguros"],
         ]),
    dict(id="d3", destaques_dub=[["técnico científica", "Técnico-científica"], ["un curso completo", "Curso completo"], ["disección", "Disección"], ["no tuve dudas", "Sin dudas"], ["muy segura", "Muy segura"]], n=28, crop=dict(cx=2050, h=1600),
         trechos=[[0.0, 2.85], [14.10, 17.98], [18.16, 27.08], [27.08, 35.80], [71.02, 75.86],
                  [112.10, 118.12], [125.40, 130.34], [131.62, 136.70], [144.32, 147.70]],
         legendas=[
             [0.00, 2.70, "Meu nome é Jânia, eu sou aluna da FEP Online.",
              "Mi nombre es Jânia, soy alumna de la FEP Online."],
             [14.16, 17.88, "O que me trouxe à FEP Online?", "¿Qué me trajo a la FEP Online?"],
             [18.24, 20.86, "Todo o embasamento técnico-científico,", "Toda la base técnico-científica,"],
             [20.86, 24.42, "para que me trouxesse, me deixasse mais segura", "para que me diera, me dejara más segura"],
             [24.42, 27.08, "e preparada para atuar aqui presencialmente.", "y preparada para actuar aquí de forma presencial."],
             [27.08, 31.64, "É um curso completo, onde aprendi muitas técnicas,",
              "Es un curso completo, donde aprendí muchas técnicas,"],
             [31.90, 35.68, "a teoria, material, reologia. É um curso completo.",
              "la teoría, material, reología. Es un curso completo."],
             [71.10, 73.28, "Tem toda a parte de anatomia,", "Tiene toda la parte de anatomía,"],
             [73.72, 75.76, "da dissecção dos cadáveres.", "de la disección de cadáveres."],
             [112.18, 114.76, "Quando eu cheguei aqui ontem, que eu encontrei o paciente,",
              "Cuando llegué aquí ayer y encontré al paciente,"],
             [115.00, 118.12, "a única coisa que eu queria de fato era atender,",
              "lo único que quería de verdad era atender,"],
             [125.44, 127.72, "mas eu não tive dúvidas", "pero no tuve dudas"],
             [127.72, 130.24, "de como eu faria o procedimento,", "de cómo haría el procedimiento,"],
             [131.70, 134.52, "pelo conhecimento agregado,", "por el conocimiento sumado,"],
             [134.62, 136.58, "conhecimento adquirido através da FEP.",
              "conocimiento adquirido a través de la FEP."],
             [144.40, 145.76, "Para mim, é um curso completo.", "Para mí, es un curso completo."],
             [145.90, 147.56, "Me deixou muito tranquila e muito segura.", "Me dejó muy tranquila y muy segura."],
         ],
         destaques=[
             [19.00, 22.38, "Técnico-científico", "Técnico-científica"],
             [27.08, 28.60, "Curso completo", "Curso completo"],
             [73.72, 75.76, "Dissecção", "Disección"],
             [126.02, 127.72, "Sem dúvidas", "Sin dudas"],
             [145.90, 147.56, "Muito segura", "Muy segura"],
         ]),
    dict(id="d4", destaques_dub=[["resolver muchas dudas", "Resolver dudas"], ["siempre está ahí", "Siempre ahí"], ["vale mucho la pena", "Vale la pena"]], n=29, crop=dict(cx=2010, h=1440),
         trechos=[[0.0, 9.10], [10.14, 37.40]],
         legendas=[
             [0.00, 1.86, "Oi, eu sou a Dra. Mariana,", "Hola, soy la doctora Mariana,"],
             [2.12, 5.52, "eu sou aluna da FEP Online, do Dr. João Pithon.", "alumna de la FEP Online, del doctor João Pithon."],
             [5.72, 9.04, "Já acompanho o doutor há muito tempo no Instagram.",
              "Sigo al doctor desde hace mucho tiempo en Instagram."],
             [10.20, 14.22, "E a FEP Online me ajuda a tirar muitas dúvidas",
              "Y la FEP Online me ayuda a resolver muchas dudas"],
             [14.22, 17.44, "que eu tenho no decorrer do dia a dia do consultório.", "que tengo en el día a día del consultorio."],
             [17.48, 19.66, "Afinal, são um monte de procedimentos", "Al final, son muchos procedimientos"],
             [19.66, 21.66, "e a gente não consegue lembrar de tudo.", "y no logramos recordar todo."],
             [21.66, 25.70, "E a FEP Online está sempre lá para socorrer a gente.",
              "Y la FEP Online siempre está ahí para ayudarnos."],
             [25.88, 26.94, "Eu gosto bastante.", "Me gusta mucho."],
             [27.40, 30.88, "Eu indico para todas as amigas, para todos os profissionais,",
              "La recomiendo a todas mis amigas, a todos los profesionales,"],
             [31.06, 33.88, "para quem está ingressando na harmonização facial.",
              "a quienes están empezando en la armonización facial."],
             [34.20, 36.02, "Eu acho um diferencial.", "Me parece un diferencial."],
             [36.20, 37.26, "Vale muito a pena.", "Vale mucho la pena."],
         ],
         destaques=[
             [12.66, 14.22, "Tirar dúvidas", "Resolver dudas"],
             [22.86, 25.70, "Sempre lá", "Siempre ahí"],
             [36.20, 37.26, "Vale muito a pena", "Vale la pena"],
         ]),
    dict(id="d5", destaques_dub=[["despejar sus dudas", "Despejar sus dudas"], ["refinen su técnica", "Refinar su técnica"]], n=30, crop=dict(cx=1985, h=1540),
         trechos=[[0.0, 33.40]],
         legendas=[
             [0.00, 1.86, "Olá, eu sou a Dra. Gabriela,", "Hola, soy la doctora Gabriela,"],
             [2.38, 4.10, "já atuo na área, já tem um tempinho.", "ya trabajo en el área hace un tiempo."],
             [4.36, 5.68, "E eu queria dizer a vocês", "Y quería decirles a ustedes"],
             [5.68, 8.10, "que ainda não fazem parte da FEP Online", "que todavía no son parte de la FEP Online"],
             [8.46, 9.82, "que é muito importante,", "que es muy importante,"],
             [10.02, 13.42, "porque você consegue tirar suas dúvidas,", "porque puedes resolver tus dudas,"],
             [13.54, 17.04, "revisar algum material que você ainda não tem tanta habilidade",
              "repasar algún material en el que todavía no tienes tanta habilidad"],
             [17.24, 19.94, "ou estudar para melhorar a sua técnica.", "o estudiar para mejorar tu técnica."],
             [20.24, 21.24, "Eu super recomendo.", "Lo recomiendo muchísimo."],
             [21.60, 23.86, "Para quem ainda não conhece o Dr. João Pithon,",
              "Si todavía no conoces al doctor João Pithon,"],
             [24.32, 28.48, "siga ele, faça parte desse grupo da FEP Online,",
              "síguelo, forma parte de este grupo de la FEP Online,"],
             [28.48, 30.78, "que você vai atualizar os seus conhecimentos",
              "porque vas a actualizar tus conocimientos"],
             [30.78, 33.18, "e vai melhorar muito e refinar a sua técnica.", "y vas a mejorar mucho y refinar tu técnica."],
         ],
         destaques=[
             [10.90, 13.42, "Tirar suas dúvidas", "Resolver tus dudas"],
             [31.98, 33.18, "Refinar a sua técnica", "Refinar tu técnica"],
         ]),
    dict(id="d6", destaques_dub=[["mi técnica", "Mi técnica"], ["elegir el horario", "Elegir el horario"], ["vale mucho la pena", "Vale la pena"]], n=31, crop=dict(cx=2050, h=1420),
         trechos=[[0.0, 7.45], [8.72, 19.30], [19.40, 25.10], [34.40, 46.60]],
         legendas=[
             [0.00, 1.52, "Olá, meu nome é Mariana,", "Hola, mi nombre es Mariana,"],
             [1.70, 3.94, "trabalho na área da estética já faz um tempo.", "trabajo en el área de la estética hace un tiempo."],
             [4.12, 7.32, "Conheço o Dr. João pelas redes sociais, pelo Instagram,",
              "Conozco al doctor João por las redes sociales, por Instagram,"],
             [8.80, 10.54, "também sou aluna da FEP Online.", "y también soy alumna de la FEP Online."],
             [11.14, 15.60, "Os vídeos do Dr. João, dos procedimentos estéticos,",
              "Los videos del doctor João, de los procedimientos estéticos,"],
             [15.82, 17.70, "me ajudaram muito na minha técnica,", "me ayudaron mucho en mi técnica,"],
             [17.88, 19.22, "no dia a dia do consultório.", "en el día a día del consultorio."],
             [19.46, 22.30, "E também me facilitou muito ter essa facilidade",
              "Y también me ayudó mucho tener esa facilidad"],
             [22.30, 25.04, "de escolher o horário para assistir às aulas.", "de elegir el horario para ver las clases."],
             [34.46, 36.56, "Para quem quer,", "Para quien quiere,"],
             [36.82, 39.84, "deseja melhorar sua técnica, refinar,", "desea mejorar su técnica, refinar,"],
             [40.40, 42.32, "ter um conhecimento mais aprofundado,", "tener un conocimiento más profundo,"],
             [42.58, 44.88, "eu indico muito o curso.", "le recomiendo mucho el curso."],
             [45.20, 46.42, "Vale muito a pena.", "Vale mucho la pena."],
         ],
         destaques=[
             [15.82, 17.70, "Minha técnica", "Mi técnica"],
             [22.30, 25.04, "Escolher o horário", "Elegir el horario"],
             [45.20, 46.42, "Vale muito a pena", "Vale la pena"],
         ]),
]

BRUTO = {"d1": "Depoimento 1 espanhol, fep 10.mp4", "d2": "depoimento 2 fep 10.mp4",
         "d3": "depoimento 3 fep 10.mp4", "d4": "DEPOIMENTO 4 fep 10.mp4",
         "d5": "Depoimento 5 fep 10.mp4", "d6": "Depoimento 6 FEP 10.mp4"}


def esticar(legs):
    """Legenda fica na tela até a próxima começar quando o intervalo é curto (sem piscar)."""
    out = []
    for i, l in enumerate(legs):
        l = list(l)
        prox = legs[i + 1][0] if i + 1 < len(legs) else None
        if prox is not None and prox - l[1] < 0.7:
            l[1] = prox                        # emenda: nunca duas legendas na tela ao mesmo tempo
        else:
            l[1] += 0.25
        out.append(l)
    return out


def encaixar(vid, trechos):
    """Move cada corte para o respiro mais próximo no áudio (o tempo da palavra erra até 0,3 s)."""
    import wave
    import numpy as np
    w = wave.open(f"{T}/wav/{vid}.wav")
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    dur = len(a) / 16000

    def db(t):
        i = int(t * 16000)
        s = a[max(i - 400, 0):i + 400]
        return 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9) if len(s) else -99

    def melhor(t, lo, hi):
        cand = [round(x, 2) for x in np.arange(max(t + lo, 0), min(t + hi, dur), 0.01)]
        quietos = [x for x in cand if db(x) < -36]
        if quietos:
            return min(quietos, key=lambda x: abs(x - t))
        return min(cand, key=db)

    out = []
    for x, y in trechos:
        x2 = x if x == 0 else melhor(x, -0.35, 0.12)
        y2 = y if y >= dur - 0.3 else melhor(y, -0.12, 0.35)
        out.append([x2, y2])
    return out


proj = {"fontes": f"{T}/fonts", "saida": f"{T}/saida",
        "cta": {"pt": f"{T}/cta/FEA-cta-FEP.mp4", "es": f"{T}/cta/FEA-cta-FEP-ES.mp4"}, "videos": []}
for v in V:
    proj["videos"].append({
        "id": v["id"], "entrada": f"{T}/brutos/{BRUTO[v['id']]}",
        "nome": {"pt": f"Ads {v['n']} FEP.mp4", "es": f"Ads {v['n']} FEP ES.mp4"},
        "crop": v["crop"], "trechos": encaixar(v["id"], v["trechos"]),
        "legendas": esticar(v["legendas"]), "destaques": v["destaques"],
        "destaques_dub": v.get("destaques_dub", [])})
dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FEA-projeto-depoimentos-fep10.json")
json.dump(proj, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(dest)
