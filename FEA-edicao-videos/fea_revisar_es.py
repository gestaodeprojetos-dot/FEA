#!/usr/bin/env python3
"""FEA: revisão do espanhol nos Reels (skill fea-revisao-reels-es).

Uso:
    python3 fea_revisar_es.py projeto_es.json [projeto2.json ...] [--sem-audio]

Roda depois do fea_revisar.py (formato, tempo, cortes e sincronia, que valem igual para o
vídeo em espanhol). Aqui só o texto: título e legendas em espanhol, conferidos contra o
glossário FEA ES e contra o português de origem, bloco a bloco.

ERRO (Classe A, barreira clínica ou erro visível): número, negação ou marca diferente do PT,
bloco sem tradução ou com tradução velha, resíduo de português, armadilha do glossário,
¿? ou ¡! sem par, travessão, legenda que não cabe em 2 linhas, leitura rápida demais.
ATENÇÃO (conferir com os olhos): falso amigo, tratamento informal (tú), título em Title Case,
legenda longa, lista de blocos técnicos para back-translation.

--sem-audio: não recalcula as legendas PT a partir do áudio (confere só o arquivo de tradução
e o .ass); usar quando o bruto não está na máquina.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_editar_video as fe  # noqa: E402

CPS_ATENCAO = 17      # caracteres por segundo: padrão de legenda em espanhol para adulto
CPS_ERRO = 21         # acima disso não dá para ler: condensar a tradução
LINHA_ATENCAO = fe.MAX_CHARS_LINHA_ES
LINHA_ERRO = 26

# resíduo de português: letra que o espanhol não tem e palavra que não existe em espanhol
LETRAS_PT = r"[ãõçâêôàÃÕÇÂÊÔÀ]"
PALAVRAS_PT = ("você vocês não então também muito muita muitos muitas isso isto aqui já só gente vai vou "
               "com uma umas ele ela eles elas mais depois agora fazer faz tem têm bem bom boa coisa até "
               "sempre nossa nosso dele dela pele olho olhos lábio lábios agulha seringa região porém onde "
               "quando né tá olha aí ali essa esse esses essas nessa nesse pela pelas na nas num numa ao aos "
               "às ou sim obrigado sem produto planejamento preenchimento injetar injeção fio fios ponta osso "
               "mento queixo pescoço vamos lá beleza certinho daqui dali deixa").split()
# "vamos" existe em espanhol, mas "vamos lá" não: tratado abaixo
PALAVRAS_PT.remove("vamos")

# armadilhas do glossário núcleo (references/FEA-00-nucleo.md, seção 1): palavra -> correto
ARMADILHAS = [
    (r"\bzigom[aá]tic", "cigomático"), (r"\brebordo\b", "reborde"), (r"\brelevo\b", "relieve"),
    (r"\bespesura\b", "grosor"), (r"\binchazo\b", "hinchazón"), (r"\blacrimal\b", "lagrimal"),
    (r"\bretentor(es)?\b", "retenedor"), (r"\bnasojugal\b", "nasoyugal"), (r"\bcamadas?\b", "capa"),
    (r"\btecidos?\b", "tejido"), (r"\bsulcos?\b", "surco"), (r"\brugas?\b", "arruga"),
    (r"\bp[aá]lpebras?\b", "párpado"), (r"\bsobreceja", "ceja"), (r"\bbochechas?\b", "mejilla"),
    (r"\bt[eé]mporas?\b", "sien / sienes"), (r"\bjeringuilla", "jeringa"), (r"\bferidas?\b", "herida"),
    (r"\bnecrose\b", "necrosis"), (r"\bdescolamiento", "desprendimiento"), (r"\benxaqueca", "migraña"),
    (r"\bconsult[oó]rio\b", "consultorio"), (r"\bEV\b", "IV (intravenoso)"),
    (r"\bharmoniza", "armonización"), (r"\bhialur[oô]nico\b|\bhialuronico\b", "hialurónico"),
    (r"\banamnese\b", "anamnesis"), (r"\bprontuario\b", "historia clínica"),
    (r"\bvital[íi]cia\b", "vitalicia (sem acento em espanhol)"), (r"\bcanulas?\b", "cánula (com acento)"),
    (r"\bretroinyeccion\b", "retroinyección"), (r"\bmicrocanula", "microcánula"),
    (r"\bvamos lá\b|\bvamos la\b", "vamos / bien (\"vamos lá\" é português)"),
    (r"\bsupraperiosteal\b", "supraperióstico"), (r"\bplanificamiento\b", "planificación"),
    (r"\bpré-jowl\b", "pre-jowl (sem acento em espanhol)"), (r"\btecidual\b", "tisular"),
]
# falsos amigos e escolhas do catálogo: não mudam sempre, mas pedem leitura
FALSOS_AMIGOS = [
    (r"\bseñal(es)?\b", "sinal clínico em espanhol é \"signo\""),
    (r"\bencamin", "encaminhar paciente é \"derivar\""),
    (r"\bacompañamiento\b", "acompanhamento clínico é \"seguimiento\""),
    (r"\bsuceso\b", "sucesso é \"éxito\""),
    (r"\blargo\b", "largo em espanhol é comprido; largura é \"ancho\""),
    (r"\beventualmente\b", "em espanhol tende a \"ocasionalmente\""),
    (r"\bdescart", "jogar fora é \"desechar\"; \"descartar\" é excluir hipótese"),
    (r"\bcomplicaci[oó]n", "o catálogo usa \"intercurrencia\" (sigla ARTI); \"complicación\" só se o PT diz complicação"),
    (r"\bfilos?\b", "fio de sustentação é \"hilo\" (\"filo\" é gume)"),
    (r"\bhilos? de tracci[oó]n\b", "o catálogo usa \"hilo tensor\""),
    (r"\bbolus\b", "o glossário prefere \"bolo\" (bolus é alternativa aceita)"),
    (r"\bembaraz", "embarazada é grávida"),
    (r"\bbigote chino\b", "termo técnico em espanhol: \"surco nasogeniano\""),
]
INFORMAL = r"\b(tú|tienes|puedes|quieres|sabes|haces|eres|estás|vas|fíjate|mira|oye|vos|tenés|podés|querés|sabés|contigo|tu|tus)\b"
NEGACAO_PT = r"\b(não|nunca|nem|jamais|nenhum|nenhuma|sem|nada|ninguém)\b"
NEGACAO_ES = r"\b(no|nunca|ni|jamás|ningún|ninguna|ninguno|sin|tampoco|nada|nadie|evit\w*)\b"
MARCAS = sorted({m for m in fe.MARCAS_DUAS_PALAVRAS if m[0].isupper()} |
                {"Neuramis", "Revanesse", "Neauvia", "Letybo", "Vietri", "Yvoire", "Seryntox", "Kirialys",
                 "Restylane", "Volyme", "Perfectha", "Subskin", "Juvederm", "Radiesse", "Sculptra",
                 "SANEP", "SANPE", "ARTI", "3TC", "PDRR", "PithonNapoli"}, key=len, reverse=True)
TECNICO = r"\d|\b(plano|capa|cánula|aguja|bolo|arteria|vena|nervio|músculo|ligamento|periostio|dermis|" \
          r"subcutáne|supraperióst|intercurrencia|isquemia|necrosis|hialuronidasa|unidades?|mL)\b"


def numeros(t):
    return sorted(re.sub(r"\s", "", n).replace(".", "") for n in re.findall(r"\d+(?:[.,]\d+)?", t))


def sem_par(textos, abre, fecha):
    """Blocos em que o "?" fecha sem "¿" aberto (a pergunta pode começar num bloco anterior)."""
    ruins, aberto = [], False
    for i, t in enumerate(textos):
        for c in t:
            if c == abre:
                aberto = True
            elif c == fecha:
                if not aberto:
                    ruins.append(i)
                aberto = False
    if aberto:
        ruins.append(len(textos) - 1)
    return ruins


def conferir_texto(t, onde, erros, aten):
    baixo = t.lower()
    if re.search(LETRAS_PT, t):
        erros.append(f"{onde} \"{t}\": letra de português ({', '.join(sorted(set(re.findall(LETRAS_PT, t))))})")
    achadas = [w for w in re.findall(r"[\wáéíóúñü]+", baixo) if w in PALAVRAS_PT]
    if achadas:
        erros.append(f"{onde} \"{t}\": palavra em português ({', '.join(achadas)})")
    for rx, certo in ARMADILHAS:
        if re.search(rx, t, re.I):
            erros.append(f"{onde} \"{t}\": armadilha do glossário, o certo é \"{certo}\"")
    if re.search(r"[—–]", t):
        erros.append(f"{onde} \"{t}\": travessão (regra FEA: vírgula, dois-pontos ou parênteses)")
    if re.search(r"\d%", t):
        erros.append(f"{onde} \"{t}\": porcentagem com espaço em espanhol (\"70 %\")")
    if re.search(r"\d\.\d{1,2}(?!\d)", t):
        erros.append(f"{onde} \"{t}\": decimal com vírgula (\"0,2\")")
    if re.search(r"\bml\b", t):
        erros.append(f"{onde} \"{t}\": unidade \"mL\"")
    if re.search(r"\bG'", t):
        erros.append(f"{onde} \"{t}\": apóstrofo curvo \"G’\" (decisão do catálogo ES)")
    for rx, motivo in FALSOS_AMIGOS:
        if re.search(rx, t, re.I):
            aten.append(f"{onde} \"{t}\": {motivo}")
    if re.search(INFORMAL, baixo):
        aten.append(f"{onde} \"{t}\": tratamento informal; o catálogo usa \"usted\" (decisão de 20/08/2026)")


def ler_ass(caminho):
    titulo, legendas = [], []
    for linha in open(caminho, encoding="utf-8"):
        if not linha.startswith("Dialogue:"):
            continue
        p = linha.rstrip("\n").split(",", 9)
        s, e = sum(float(x) * m for x, m in zip(p[1].split(":"), (3600, 60, 1))), \
            sum(float(x) * m for x, m in zip(p[2].split(":"), (3600, 60, 1)))
        txt = re.sub(r"\{[^}]*\}", "", p[9]).replace(" ", " ")
        (titulo if p[3] == "Titulo" else legendas).append((s, e, txt))
    # a legenda sai em um evento por linha: junta as linhas do mesmo bloco
    blocos = []
    for s, e, t in legendas:
        if blocos and abs(blocos[-1][0] - s) < 1e-3 and abs(blocos[-1][1] - e) < 1e-3:
            blocos[-1][2].append(t)
        else:
            blocos.append((s, e, [t]))
    return titulo, blocos


def revisar(cfg, v, com_audio=True):
    erros, aten = [], []
    ass = v["saida"].rsplit(".", 1)[0] + ".ass"
    if not os.path.exists(ass):
        return [f"legenda final não existe: {ass} (renderizar antes)"], []
    titulo, blocos = ler_ass(ass)

    # 1. título em espanhol
    tit = v["titulo"]
    conferir_texto(tit, "[título]", erros, aten)
    for abre, fecha in (("¿", "?"), ("¡", "!")):
        if tit.count(abre) != tit.count(fecha):
            erros.append(f"[título] \"{tit}\": \"{fecha}\" sem \"{abre}\" (em espanhol abre e fecha)")
    palavras = tit.split()
    maiusculas = [w for w in palavras[1:] if w[:1].isupper() and not w.isupper()
                  and w.strip(",.:") not in fe.NOMES_PROPRIOS | fe.NOMBRES_ES | set(" ".join(MARCAS).split())
                  and w not in ("Parte", "Black", "Friday", "Vitalicia")]
    if maiusculas:
        aten.append(f"[título] \"{tit}\": espanhol usa maiúscula só na 1ª palavra e em nome próprio "
                    f"({', '.join(maiusculas)}); manter só se a Keila escreveu assim")
    if not v.get("titulo_pt"):
        aten.append("[título] sem \"titulo_pt\" no projeto: registrar a headline PT de origem para o doc de revisão")
    if v.get("cartela_final") and "perfil" in v["cartela_final"] and " no perfil" in v["cartela_final"]:
        erros.append(f"[cartela] \"{v['cartela_final']}\": em espanhol é \"Parte 2 en el perfil\"")

    # 2. legenda final (o que aparece na tela)
    textos = [" ".join(ls) for _, _, ls in blocos]
    for (s, e, ls), t in zip(blocos, textos):
        onde = f"[{s:5.1f}s]"
        conferir_texto(t, onde, erros, aten)
        if len(ls) > 2:
            erros.append(f"{onde} \"{t}\": {len(ls)} linhas (máximo 2): condensar a tradução")
        for linha in ls:
            if len(linha) > LINHA_ERRO:
                erros.append(f"{onde} linha \"{linha}\" com {len(linha)} caracteres (máximo {LINHA_ERRO}): condensar")
            elif len(linha) > LINHA_ATENCAO:
                aten.append(f"{onde} linha \"{linha}\" com {len(linha)} caracteres: conferir na tela")
        cps = len(t) / max(e - s, 0.01)
        if cps > CPS_ERRO:
            erros.append(f"{onde} \"{t}\": {cps:.0f} caracteres/s em {e - s:.1f} s, não dá para ler: condensar")
        elif cps > CPS_ATENCAO:
            aten.append(f"{onde} \"{t}\": {cps:.0f} caracteres/s: condensar se der sem perder conteúdo clínico")
        if t.rstrip().endswith("."):
            erros.append(f"{onde} \"{t}\": legenda sem ponto final (padrão FEA)")
        primeira = re.sub(r"^[¿¡]+", "", t).split(" ", 1)[0].strip(",.?!")
        if primeira[:1].isupper() and not primeira.isupper() and primeira not in fe.NOMES_PROPRIOS | fe.NOMBRES_ES \
                and not any(m.startswith(primeira) for m in MARCAS):
            aten.append(f"{onde} \"{t}\": legenda começa minúscula (padrão FEA)")
    for abre, fecha in (("¿", "?"), ("¡", "!")):
        for i in sem_par(textos, abre, fecha):
            erros.append(f"[{blocos[i][0]:5.1f}s] \"{textos[i]}\": \"{abre}...{fecha}\" sem par (a pergunta abre com \"{abre}\")")

    # 3. tradução bloco a bloco contra o português (Classe A: número, negação, marca)
    if v.get("legendas_es"):
        dados = json.load(open(v["legendas_es"], encoding="utf-8"))
        trad = dados["legendas"] if isinstance(dados, dict) else dados
        if isinstance(dados, dict) and dados.get("titulo_es") and dados["titulo_es"] != v["titulo"]:
            aten.append(f"[título] projeto \"{v['titulo']}\" diferente do arquivo de tradução \"{dados['titulo_es']}\"")
        if com_audio:
            vv, pal, dur = fe.preparar(cfg, v)
            fim = dur - (fe.CARTELA_DUR if vv.get("cartela_final") else 0)
            atuais = [t for _, _, t in fe.eventos_legenda(dict(vv, idioma="pt", legendas_es=None), pal, fim)]
            if len(atuais) != len(trad) or any(a != b["pt"] for a, b in zip(atuais, trad)):
                erros.append("tradução velha: as legendas PT mudaram depois da exportação "
                             "(rodar --exportar-legendas de novo e traduzir os blocos novos)")
        tecnicos = []
        for b in trad:
            pt, es, onde = b["pt"], (b.get("es") or "").strip(), f"[bloco {b.get('id')} {b.get('s', 0):5.1f}s]"
            if not es:
                erros.append(f"{onde} \"{pt}\": sem tradução")
                continue
            if es == "-":
                if numeros(pt) or any(m in pt for m in MARCAS) or len(pt.split()) > 3:
                    erros.append(f"{onde} \"{pt}\": bloco com conteúdo tirado da legenda (\"-\" é só para muleta como \"né?\")")
                continue
            if numeros(pt) != numeros(es):
                erros.append(f"{onde} número diferente do PT: \"{pt}\" -> \"{es}\"")
            if re.search(NEGACAO_PT, pt, re.I) and not re.search(NEGACAO_ES, es, re.I):
                erros.append(f"{onde} negação do PT sumiu: \"{pt}\" -> \"{es}\"")
            faltam = []
            for m in MARCAS:   # da mais longa para a mais curta: "Neuramis Volume" antes de "Neuramis"
                if m.lower() in pt.lower() and m.lower() not in es.lower() and not any(m in f for f in faltam):
                    faltam.append(m)
                    erros.append(f"{onde} \"{m}\" está no PT e não no ES: \"{es}\"")
            if re.search(TECNICO, es):
                tecnicos.append(str(b.get("id")))
        if tecnicos:
            aten.append(f"back-translation obrigatória (volta ao PT e compara) nos blocos técnicos: {', '.join(tecnicos)}")
    return erros, aten


def main():
    args = sys.argv[1:]
    com_audio = "--sem-audio" not in args
    args = [a for a in args if a != "--sem-audio"]
    total = 0
    for proj in args:
        cfg = json.load(open(proj, encoding="utf-8"))
        for v in cfg["videos"]:
            if (v.get("idioma") or cfg.get("idioma")) != "es":
                continue
            erros, aten = revisar(cfg, v, com_audio)
            total += len(erros)
            print(f"\n## {os.path.basename(v['saida'])}: {'REPROVADO' if erros else 'OK'}")
            for x in erros:
                print(f"  ERRO     {x}")
            for x in aten:
                print(f"  ATENÇÃO  {x}")
    print(f"\nTotal de erros (espanhol): {total}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
