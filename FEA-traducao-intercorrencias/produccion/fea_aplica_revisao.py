"""Aplica as correções da revisão cega (fea-revision-es) ao mapa v2."""
import json,sys
f='produccion/mapa-es-v2.json'; m=json.load(open(f))
R=[
('p31_08','1000 UTR/mL','1.000 UTR/mL'),
('p20_04','con destaque para la participación de','con especial participación de'),
('p6_03','alto “swelling factor”','alto <i>swelling factor</i> (capacidad de hinchamiento del gel)'),
('p21_06','fueron los angiosomas afectados con mayor frecuencia','fueron los angiosomas comprometidos con mayor frecuencia'),
('p124_20','relleno capilar','llenado capilar'),
('p132_06','menos complaciente','de menor complacencia'),
('p137_07','poco complaciente','de baja complacencia'),
('p147_05','por manipulación del paciente','tras la manipulación de la zona por parte del paciente'),
('p194_12','un pequeño acúmulo','una pequeña acumulación'),
('p188_11','amarronada','parduzca'),
('p106_04','de los casos: necesidad de observación hospitalaria','de los casos, lo que hace necesaria la observación hospitalaria'),
('p97_09','EN LABIO SUPERIOR POSHIALURONIDASA','EN EL LABIO SUPERIOR TRAS HIALURONIDASA'),
('p58_02','en el plano intraocular','a nivel intraocular'),
('p59_04','CONTRIBUYENTES:','QUE CONTRIBUYEN:'),
('p67_04','suele tener antecedentes previos','suele referir antecedentes'),
('p112_11','No sujetar los movimientos','No restringir los movimientos del paciente'),
('p117_09','en atenciones futuras','en sesiones futuras'),
('p135_04','lo que hace el diagnóstico más difícil y a menudo se confunde con','lo que dificulta el diagnóstico, y el cuadro a menudo se confunde con'),
('p75_04','inyección de productos de relleno','inyección de rellenos'),
('p75_04','del producto de relleno,','del relleno,'),
]
er=0
for k,a,b in R:
    if a not in m.get(k,''): print('NAO ACHEI',k,a); er+=1; continue
    m[k]=m[k].replace(a,b)
for k,v in m.items():
    if 'complaciente' in v: print('complaciente resta',k)
json.dump(m,open(f,'w'),ensure_ascii=False,indent=1); sys.exit(er)
# Rodada 2 (revisão do delta, 05/10/2026): aplicados direto em mapa-es.json
# p7_02 «ya que guía» -> «y permite guiar» · p49_02 «con mejoría con» -> «mejora con» · p50_13 «mapear el área y la extensión»
# Retorno do autor (07/10/2026), aplicado direto em mapa-es.json:
# p27_03 «tiempo de reperfusión» -> «velocidad de perfusión» · p31_11 exemplo de diluição 3.000 UTR em 3 mL
# piperacilina/tazobactam padronizada 4,5 g IV cada 6 h (p34_04, antes 3,375 g; p149_12; p154_05)
