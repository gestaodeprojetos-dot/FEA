#!/usr/bin/env python3
"""
Auditor determinístico de tradução PT-BR -> ES (LatAm) para material FEA.

Uso:
    python3 auditar.py texto_es.txt [--json]

Não substitui a leitura crítica. Cobre a classe de erro que é mecânica:
resíduo de português, lusismo sintático, falso amigo clínico, ortotipografia,
posologia e tratamento. O que sobra depois disto é julgamento — e é aí que
entra a skill fea-revision-es.

Severidades:
    BLOQUEANTE  erro clínico ou de sentido; não pode publicar
    GRAVE       denuncia tradução; leitor especialista percebe
    MENOR       ortotipografia e preferência de registro
"""
import re, sys, json, unicodedata

# ---------------------------------------------------------------- regras
# (severidade, rótulo, regex, sugestão[, flags]) — flags omitido = re.I
REGRAS = [
 # ---- resíduo de português -------------------------------------------
 ('BLOQUEANTE','resíduo PT: anatomia', r'\bzigom[áa]tic',           'cigomático (com C)'),
 ('BLOQUEANTE','resíduo PT: anatomia', r'\bnasojugal\b',            'nasoyugal'),
 ('BLOQUEANTE','resíduo PT: anatomia', r'\brebordo\b',              'reborde'),
 ('BLOQUEANTE','resíduo PT: anatomia', r'\bp[áa]lpebra\b',          'párpado'),
 ('BLOQUEANTE','resíduo PT: anatomia', r'\blacrimal\b',             'lagrimal'),
 ('BLOQUEANTE','resíduo PT: anatomia', r'\bretentor',               'retenedor'),
 ('GRAVE','resíduo PT', r'\brelevo\b',                              'relieve'),
 ('GRAVE','resíduo PT', r'\bespessura\b|\bespesura\b',              'grosor'),
 ('GRAVE','resíduo PT', r'\bincha[çc]o\b',                          'hinchazón'),
 ('GRAVE','resíduo PT', r'\bcamada\b',                              'capa'),
 ('GRAVE','resíduo PT', r'\btecido\b',                              'tejido'),
 ('GRAVE','resíduo PT', r'\bsulco\b',                               'surco'),
 ('GRAVE','resíduo PT', r'\bruga\b',                                'arruga'),
 ('GRAVE','resíduo PT', r'\bagulha\b',                              'aguja'),
 ('GRAVE','resíduo PT', r'\bnecrose\b',                             'necrosis'),
 ('GRAVE','resíduo PT', r'\btrombose\b',                            'trombosis'),
 ('GRAVE','resíduo PT', r'\bamaurose\b',                            'amaurosis'),
 ('GRAVE','resíduo PT', r'\bferida\b',                              'herida'),
 ('GRAVE','resíduo PT', r'\bpreenchi',                              'relleno'),
 ('GRAVE','resíduo PT', r'\bolheira',                               'ojera'),
 ('GRAVE','resíduo PT', r'\bgordura\b',                             'grasa'),
 ('GRAVE','resíduo PT', r'\bbochecha\b',                            'mejilla'),
 ('GRAVE','resíduo PT', r'\bdesbridamento\b',                       'desbridamiento'),
 ('GRAVE','resíduo PT', r'\bozonioterapia\b',                       'ozonoterapia'),
 ('GRAVE','resíduo PT', r'\btriancinolona\b',                       'triamcinolona'),
 ('GRAVE','resíduo PT', r'\bclavulanato\b',                         'ácido clavulánico'),
 ('GRAVE','resíduo PT', r'\bbenzodiazep[íi]nico',                   'benzodiacepina'),
 ('GRAVE','resíduo PT', r'\bcarbapen[êe]mico',                      'carbapenémico'),
 ('GRAVE','resíduo PT', r'\bdispneia\b',                            'disnea'),
 ('GRAVE','resíduo PT', r'\bdescolamento\b',                        'desprendimiento'),
 ('GRAVE','resíduo PT', r'\benxaqueca\b',                           'migraña'),
 ('GRAVE','resíduo PT', r'\bhilos? de tracci[óo]n\b',               'hilos tensores'),

 # ---- clínico: falso amigo que muda o sentido ------------------------
 ('BLOQUEANTE','falso amigo clínico', r'\bse[ñn]ales?\s+(cl[íi]nic|t[íi]pic|cl[áa]sic)', 'signo(s) clínico(s) — «señal» é sinal de trânsito'),
 ('BLOQUEANTE','falso amigo clínico', r'\bdescartar\s+(la\s+aguja|el\s+material|la\s+c[áa]nula|la\s+jeringa)', 'desechar — «descartar» em ES = excluir diagnóstico'),
 ('GRAVE','falso amigo clínico', r'\bencaminar\s+al?\s+paciente',   'derivar al paciente'),
 ('GRAVE','falso amigo clínico', r'\bacompa[ñn]amiento\b',          'seguimiento'),
 ('GRAVE','falso amigo clínico', r'\bprontuario\b',                 'historia clínica'),
 ('GRAVE','falso amigo clínico', r'\bbula\b',                       'prospecto / ficha técnica'),

 # ---- posologia e via (risco clínico) --------------------------------
 ('BLOQUEANTE','via de administração', r'\b\d+\s*mg\s+EV\b|\bEV\b(?!\s*[a-záéíóú])', 'IV (intravenosa) — «EV» não se usa em espanhol'),
 ('BLOQUEANTE','posologia', r'\b\d{1,2}/\d{1,2}\s*h\b',            'cada N h — a notação 12/12h não existe em espanhol'),
 ('GRAVE','unidade grudada', r'\b\d+(mg|ml|mL|g|mm|cm|UI|UTR)\b',  'espaço entre cifra e unidade'),
 ('GRAVE','unidade pluralizada', r'\b\d+\s*(mgs|mls|gs)\b',        'unidade não pluraliza: 20 mg'),
 ('GRAVE','decimal com ponto', r'\b\d+\.\d\b',                      'decimal com coma: 0,5'),

 # ---- lusismo sintático ----------------------------------------------
 ('GRAVE','lusismo: el mismo pronome', r'\b(el|la|los|las)\s+mism[oa]s?\b(?!\s+(que|tiempo|d[íi]a|modo|nivel|producto|paciente|t[ée]cnica|regi[óo]n|forma|zona|plano|capa|efecto|caso|tipo|sentido|principio|resultado|autor|mecanismo|criterio|grupo|volumen|punto|plano))', 'pronome enclítico: «se lo masajea», «sus cuidados»'),
 ('GRAVE','lusismo: a nivel de', r'\ba\s+nivel\s+de\s+(la\s+piel|el\s+tejido|la\s+dermis|la\s+capa|la\s+regi[óo]n)', '«en la piel» — «a nivel de» só para nível real'),
 ('GRAVE','lusismo: en base a', r'\ben\s+base\s+a\b',               'con base en / sobre la base de'),
 ('MENOR','lusismo: es por eso que', r'\bes\s+por\s+eso\s+que\b',   'por eso / es por lo que'),
 ('MENOR','lusismo: de acuerdo a', r'\bde\s+acuerdo\s+a\b',         'de acuerdo con'),
 ('MENOR','lusismo: en relación a', r'\ben\s+relaci[óo]n\s+a\b',    'en relación con / con respecto a'),
 ('GRAVE','lusismo: donde sem lugar', r'\b(casos?|situaci[óo]n(es)?|pacientes?)\s+donde\b', 'en el que / en la que / en los que'),
 ('BLOQUEANTE','lusismo: ênclise', r'\b[a-záéíóúñ]{3,}(?:a|e|i)se\b(?<!\bclase)(?<!\bbase)(?<!\bfase)(?<!\bfrase)(?<!\bdose)', 'próclise: «se aplica», não «aplicase»'),
 ('BLOQUEANTE','lusismo: futuro do subjuntivo', r'\b\w+(?:are|iere|ere)\b(?=\s+(el|la|los|las|un|una|edema|sangrado))', 'presente: «si persiste», não «si persistiere»'),
 ('GRAVE','haber impessoal plural', r'\bhubieron\b',                'hubo — haber impessoal é sempre singular'),
 ('GRAVE','«a» de OD pessoa', r'\b(evaluar|orientar|derivar|tratar|examinar|instruir|remitir)\s+el\s+paciente\b', 'al paciente'),
 ('MENOR','gerúndio de posterioridade', r',\s+(obteniendo|logrando|generando|resultando|provocando|causando|permitiendo)\b', 'con lo que se obtiene / y así se logra'),

 # ---- tratamento -----------------------------------------------------
 ('BLOQUEANTE','tuteo/voseo', r'\b(t[úu]\s|vos\s|vosotros|ten[ée]s\b|pod[ée]s\b|deb[ée]s\b|tienes\b|puedes\b|debes\b|vas\s+a\s+aprender|aprender[áa]s)\b', 'tratamento formal: usted'),
 ('MENOR','tratamento abreviado', r'\bUd\.\b',                      'usted por extenso na prosa'),

 # ---- ortotipografia -------------------------------------------------
 ('GRAVE','falta ¿ de abertura', None,                              'interrogação abre com ¿'),
 ('GRAVE','falta ¡ de abertura', None,                              'exclamação abre com ¡'),
 ('MENOR','percentual sem espaço', r'\d%',                          'espaço antes do %: «70 %»'),
 ('MENOR','aspas retas', r'"[^"\n]{2,}"',                           'aspas angulares «…»'),
 ('MENOR','hífen como raya', r'(?<=[a-záéíóúñ,])\s-\s(?=[a-záéíóúñ])',   'raya — sem espaço interno (rótulos curtos de capítulo, tipo «A - Anatomía», estão isentos)', 0),
]

TERMOS_ESPERADOS = ['cigomátic','nasoyugal','retenedor','relleno','ojera',
 'grasa','capa','tejido','signo','manejo','seguimiento','posprocedimiento']

def audita(texto):
    achados=[]
    linhas=texto.split('\n')
    for regra in REGRAS:
        sev,rot,rx,sug = regra[:4]
        flags = regra[4] if len(regra)>4 else re.I
        if rx is None: continue
        for n,l in enumerate(linhas,1):
            for m in re.finditer(rx,l,flags):
                ini=max(0,m.start()-45); fim=min(len(l),m.end()+45)
                achados.append(dict(sev=sev,regra=rot,linha=n,
                    trecho=('…' if ini else '')+l[ini:fim].strip()+('…' if fim<len(l) else ''),
                    encontrado=m.group(0).strip(),sugestao=sug))
    # pontuação de abertura: ? ou ! sem par de abertura na mesma frase
    for n,l in enumerate(linhas,1):
        for sinal,abre,rot in (('?','¿','falta ¿ de abertura'),('!','¡','falta ¡ de abertura')):
            if sinal in l and l.count(abre)<l.count(sinal):
                achados.append(dict(sev='GRAVE',regra=rot,linha=n,
                    trecho=l.strip()[:120],encontrado=sinal,
                    sugestao='abrir com '+abre))
    return achados

def cobertura(texto):
    t=texto.lower()
    return {k:len(re.findall(k,t)) for k in TERMOS_ESPERADOS}

def main():
    if len(sys.argv)<2: print(__doc__); sys.exit(2)
    texto=open(sys.argv[1],encoding='utf-8').read()
    ach=audita(texto); cob=cobertura(texto)
    if '--json' in sys.argv:
        print(json.dumps(dict(achados=ach,cobertura=cob),ensure_ascii=False,indent=1)); return
    ordem={'BLOQUEANTE':0,'GRAVE':1,'MENOR':2}
    ach.sort(key=lambda a:(ordem[a['sev']],a['linha']))
    n_b=sum(1 for a in ach if a['sev']=='BLOQUEANTE')
    n_g=sum(1 for a in ach if a['sev']=='GRAVE')
    n_m=sum(1 for a in ach if a['sev']=='MENOR')
    print('AUDITORIA — %s'%sys.argv[1])
    print('%d BLOQUEANTE · %d GRAVE · %d MENOR\n'%(n_b,n_g,n_m))
    for a in ach:
        print('[%s] %s  (linha %d)'%(a['sev'],a['regra'],a['linha']))
        print('   encontrado: %s'%a['encontrado'])
        print('   sugestão:   %s'%a['sugestao'])
        print('   contexto:   %s\n'%a['trecho'])
    print('COBERTURA DE TERMOS OBRIGATÓRIOS')
    for k,v in cob.items():
        print('   %-18s %s'%(k, v if v else '0  ← ausente, verificar se deveria aparecer'))
    sys.exit(1 if n_b else 0)

if __name__=='__main__': main()
