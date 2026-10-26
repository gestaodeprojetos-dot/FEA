"""Remapeia mapa-es.json para a estrutura v3: listas numeradas das págs. 31 e 41
viram um id por item (antes a continuação recuada colava no item seguinte)."""
import json, re
a = json.load(open('produccion/estrutura.json')); b = json.load(open('produccion/estrutura-v3.json'))
m = json.load(open('produccion/mapa-es.json'))
norm = lambda t: re.sub(r'[\s•]+', ' ', t).strip()
N = lambda n: '<b>%d.</b>    ' % n
B = lambda t: '<b>%s</b>' % t
NOVO = {
 'p31_08': N(1) + B('Interrumpir la aplicación de inmediato.'),
 'p31_09': N(2) + B('Masaje vigoroso') + ' del área comprometida.',
 'p31_10': N(3) + B('Compresas tibias') + ' para vasodilatación.',
 'p31_11': N(4) + B('Hialuronidasa:') + ' inyectar ' + B('1.000 UTR/mL en la región afectada') + ', repetir cada 15 a 30 min según sea necesario.',
 'p41_03': 'El manejo de la oclusión vascular es una emergencia médica estética. El tratamiento debe iniciarse en minutos.',
 'p41_04': N(1) + B('PDRR – Protocolo de Diagnóstico y Reperfusión Rápida'),
 'p41_05': N(2) + B('Sospecha diagnóstica:') + ' cambio de coloración, dolor, reperfusión capilar lenta.',
 'p41_06': N(3) + B('Registro:') + ' fotos y videos para seguimiento y discusión multidisciplinaria.',
 'p41_07': N(4) + B('Medidas iniciales:') + ' masaje vigoroso para fragmentar el relleno, calor local y terapia LED para vasodilatación.',
 'p41_08': N(5) + B('Hialuronidasa:') + ' aplicación en altas dosis (1.000 UTR/mL) en la región comprometida, con repetición cada 15 a 30 minutos si es necesario.',
 'p41_09': N(6) + B('Terapia farmacológica adyuvante:'),
}
out = {}
for p in b:
    old = {norm(x['pt']): x['id'] for x in a[p]}
    for x in b[p]:
        k = x['id']
        if k in NOVO: out[k] = NOVO[k]
        elif norm(x['pt']) in old and old[norm(x['pt'])] in m: out[k] = m[old[norm(x['pt'])]]
        elif norm(x['pt']) not in old: print('SEM TRADUCAO', k, x['pt'][:60])
for k, v in m.items():
    pg = k[1:].split('_')[0]
    if k not in out and pg not in ('31', '41'): out[k] = v
json.dump(out, open('produccion/mapa-es.json', 'w'), ensure_ascii=False, indent=1)
print(len(m), len(out))
