"""Remapeia mapa-es.json para a estrutura v5: rótulos em negrito ('Dolor moderado
persistente:') saem do item anterior e viram id próprio (págs. 88, 125, 126, 178).
O espanhol é partido no último <b>...:</b> do id antigo."""
import json, re
a = json.load(open('produccion/estrutura.json')); b = json.load(open('produccion/estrutura-v5.json'))
m = json.load(open('produccion/mapa-es.json'))
norm = lambda t: re.sub(r'[\s•]+', ' ', t).strip()
out = {}
for p in b:
    old = {norm(x['pt']): x['id'] for x in a[p]}
    novos = [x for x in b[p]]
    i = 0
    while i < len(novos):
        x = novos[i]; k = x['id']
        if norm(x['pt']) in old:
            oid = old[norm(x['pt'])]
            if oid in m: out[k] = m[oid]
            i += 1; continue
        # par (frase + rótulo) que no estrutura antiga era um id só
        y = novos[i + 1] if i + 1 < len(novos) else None
        junto = norm(x['pt'] + ' ' + (y['pt'] if y else ''))
        oid = old.get(junto)
        assert oid and y, ('sem correspondência', k, x['pt'][:60])
        es = re.sub(r'\s*•\s*$', '', m[oid]).strip()
        j = es.rfind('<b>')
        assert j > 0, (oid, es)
        out[k] = es[:j].strip(); out[y['id']] = es[j:].strip()
        i += 2
for k, v in m.items():
    pg = k[1:].split('_')[0]
    if k not in out and pg not in ('88', '125', '126', '178'): out[k] = v
json.dump(out, open('produccion/mapa-es.json', 'w'), ensure_ascii=False, indent=1)
print(len(m), len(out))
for k in ['p88_12','p88_13','p88_15','p88_16','p125_19','p125_20','p126_04','p126_05','p178_10','p178_11']: print(k, '|', out.get(k))
