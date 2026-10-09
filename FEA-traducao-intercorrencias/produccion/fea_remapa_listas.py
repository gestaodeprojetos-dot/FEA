"""Remapeia mapa-es.json para a estrutura v2 (itens de lista separados)."""
import json,re
a=json.load(open('produccion/estrutura.json'));b=json.load(open('produccion/estrutura-v2.json'))
m=json.load(open('produccion/mapa-es.json'))
norm=lambda t: re.sub(r'[\s•]+',' ',t).strip()
B=lambda t:'<b>%s</b>'%t
NOVO={
'p24_04':B('Arteria facial:')+' irriga la región perioral; su obstrucción puede comprometer los labios y la región paranasal.',
'p24_05':B('Arterias labiales (superior e inferior):')+' irrigan los labios; pueden causar palidez, dolor, riesgo de ulceración y evolución hacia necrosis.',
'p24_06':B('Arteria columelar:')+' puede causar necrosis de la columela y de la punta nasal.',
'p24_07':B('Arteria angular:')+' discurre cerca del canto medial del ojo y se comunica con la oftálmica, por lo que puede causar amaurosis. Además, por sus variaciones anatómicas, se considera una vía crítica para la necrosis nasal.',
'p24_08':B('Arterias nasales (alar inferior, subalar, nasal lateral y nasal dorsal):')+' riesgo elevado de necrosis nasal y, dada la proximidad con la circulación oftálmica, de complicaciones oculares.',
'p24_09':B('Arterias supratroclear y supraorbitaria:')+' irrigan la frente y la glabela; su obstrucción puede provocar necrosis cutánea y amaurosis.',
'p24_10':B('Arteria temporal superficial:')+' irriga la región temporal, el cuero cabelludo y el arco superciliar; su oclusión provoca dolor intenso, necrosis de la región temporal y posible alopecia.',
'p33_12':B('Ultrasonido con Doppler:')+' para localizar obstrucciones y guiar la aplicación de hialuronidasa.',
'p33_13':B('Oxigenoterapia hiperbárica:')+' 5 a 10 sesiones en días seguidos; mejora la oxigenación tisular y la cicatrización.',
'p40_07':B('Intervención tardía (> 24 h):')+' riesgo elevado de necrosis y secuelas permanentes.',
'p40_08':B('Casos de embolización retiniana:')+' pronóstico reservado, con baja tasa de recuperación visual; el tiempo previsto para un mejor pronóstico es de 30 minutos, aunque, según algunos oftalmólogos, el cuadro puede revertirse hasta 4 horas después del procedimiento como período máximo.',
'p42_03':B('Necrosis cutánea:')+' cuando el flujo no se restablece a tiempo.',
'p42_04':B('Cicatrices inestéticas y retracciones.'),
'p42_05':B('Compromiso ocular:')+' puede conducir a amaurosis irreversible.',
'p43_03':B('Técnica adecuada:')+' aspirar siempre antes de inyectar, aplicar lentamente y en pequeñas cantidades.',
'p43_04':B('Uso de cánulas')+' en áreas de alto riesgo.',
'p43_05':B('Conocimiento anatómico profundo')+' de las variaciones vasculares del rostro.',
'p43_10':B('Entorno preparado:')+' tener hialuronidasa disponible en cantidad suficiente.',
'p46_06':B('Sufrimiento celular reversible:')+' edema intracelular, alteración de la permeabilidad, inicio de estrés oxidativo.',
'p46_07':B('Sufrimiento celular avanzado (principio de necrosis):')+' tejido en hipoxia prolongada, con áreas de daño celular subletal.',
'p46_08':B('Necrosis irreversible:')+' lisis celular, inflamación intensa, formación de costra necrótica.',
'p49_02':B('Hematoma:')+' coloración violácea, sin palidez y, en general, con mejoría con la compresión local.',
'p49_03':B('Edema inflamatorio:')+' piel caliente y enrojecida, sin livedo reticular. '+B('Infección precoz:')+' rara en las primeras horas, asociada a calor local y secreción.',
'p49_04':B('Reacción alérgica:')+' prurito y edema difuso, sin patrón segmentario.',
'p50_04':B('Hialuronidasa:')+' 1.000 UTR/mL infiltrada en la región comprometida, repetida cada 15 a 30 minutos según necesidad.',
'p50_08':'Sildenafil 50 mg VO como vasodilatador.',
'p50_09':B('Corticoides sistémicos:')+' prednisona 40 mg por la mañana; en casos graves, Diprospan IM.',
'p51_10':B('Enzimático:')+' uso de colagenasa o papaína en gel, para la eliminación gradual del tejido desvitalizado.',
'p51_11':B('Autolítico:')+' apósitos oclusivos (hidrogel, hidrocoloide), que favorecen la acción enzimática natural.',
'p51_12':B('Quirúrgico:')+' indicado en necrosis extensas, gruesas o infectadas, realizado con anestesia local.',
'p53_05':B('Principio de necrosis:')+' membranas celulares comprometidas, pero con parte aún viable.',
'p53_06':B('Necrosis irreversible:')+' lisis celular, liberación de enzimas lisosomales, inflamación intensa y formación de costra.',
'p59_06':B('Compresión extrínseca')+' de la microcirculación retiniana por partículas del relleno.',
'p61_10':B('Dolor ocular o cefalea frontal.'),
'p61_11':B('Oftalmoplejía:')+' dificultad para mover el ojo.',
'p61_12':B('Ptosis palpebral.'),
'p61_13':B('Blanqueamiento retiniano')+' y '+B('mancha rojo cereza en la fóvea')+' (examen oftalmológico con fondoscopia).',
'p68_09':'Suspender de inmediato la aplicación.',
'p68_10':B('Iniciar hialuronidasa en dosis alta (1.000 UTR/mL):')+' realizar flush en el trayecto de las arterias supraorbitarias, supratrocleares, nasal dorsal, angular/facial o temporal superficial, según el área infiltrada.',
'p69_02':B('Técnica:')+' intento de punción intravascular con aspiración para reflujo positivo, seguido de flush vigoroso de hialuronidasa para disolver el ácido hialurónico.',
'p69_03':B('Objetivo:')+' destruir el material obstructivo y restaurar la perfusión.',
'p69_04':B('Masaje ocular digital intermitente:')+' 5 a 10 segundos de compresión seguidos de relajación, para intentar desalojar el émbolo.',
'p70_02':B('Vasodilatación sistémica:')+' puede considerarse sildenafil 50 mg VO.',
'p70_03':B('Corticoterapia sistémica:')+' prednisona 40 mg/día VO, respetando el ciclo circadiano, o Diprospan IM, para reducir la inflamación secundaria.',
'p70_04':B('Oxigenoterapia hiperbárica precoz:')+' si está disponible, una sesión inmediata puede mejorar la oxigenación retiniana hasta 12 h después del evento.',
'p71_04':B('Hialuronidasa retrobulbar o peribulbar:')+' descrita en protocolos recientes, pero de eficacia aún controvertida y dependiente de la experiencia del operador.',
'p75_06':B('Tiempo crítico:')+' la retina tolera hasta 90 minutos sin oxigenación. Tras este período, la probabilidad de reversión es mínima.',
'p75_07':B('Casos tratados precozmente (menos de 1 h):')+' pueden recuperar parcialmente la visión.',
}
out={}
for p in b:
    old={norm(x['pt']):x['id'] for x in a[p]}
    for x in b[p]:
        k=x['id']
        if k in NOVO: out[k]=NOVO[k]
        elif norm(x['pt']) in old:
            oid=old[norm(x['pt'])]
            if oid in m: out[k]=m[oid]
        else:
            if any(i.startswith('p%s_'%p) for i in NOVO) or True:
                print('SEM TRADUCAO',k,x['pt'][:80])
# ids extras do mapa (fora da estrutura) preservados se a página não mudou
for k,v in m.items():
    pg=k[1:].split('_')[0]
    if k not in out and [norm(x['pt']) for x in a.get(pg,[])]==[norm(x['pt']) for x in b.get(pg,[])]:
        out[k]=v
json.dump(out,open('produccion/mapa-es-v2.json','w'),ensure_ascii=False,indent=1)
print(len(m),len(out))
