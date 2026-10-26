"""Remapeia mapa-es.json quando um id antigo vira N ids novos (itens de lista,
subtítulos em negrito, subitens com hífen). Parte o espanhol pelo mesmo marcador:
' - ' para subitens, o último <b> para subtítulo. Para no primeiro caso ambíguo.
Uso: python3 fea_remapa_generico.py estrutura_antiga.json estrutura_nova.json"""
import json, re, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
m = json.load(open('produccion/mapa-es.json'))
norm = lambda t: re.sub(r'[\s•]+', ' ', t).strip()
out, mudou = {}, set()
for p in b:
    old = {norm(x['pt']): x['id'] for x in a[p]}
    nv = b[p]; i = 0
    while i < len(nv):
        x = nv[i]
        if norm(x['pt']) in old:
            if old[norm(x['pt'])] in m: out[x['id']] = m[old[norm(x['pt'])]]
            i += 1; continue
        for k in range(2, 8):
            junto = norm(' '.join(y['pt'] for y in nv[i:i + k]))
            if junto in old: break
        else:
            raise SystemExit('sem correspondência: %s %s' % (x['id'], x['pt'][:60]))
        pecas = nv[i:i + k]; es = re.sub(r'\s*•\s*$', '', m[old[junto]]).strip()
        if all(y['pt'].lstrip().startswith('-') for y in pecas[1:]):
            partes = re.split(r'\s(?=- )', es)
        elif k == 2 and '<b>' in es[1:]:
            j = es.rfind('<b>'); partes = [es[:j].strip(), es[j:].strip()]
        elif k == 2 and norm(pecas[1]['pt']).endswith(':') and '. ' in es:
            j = es.rfind('. ') + 1; partes = [es[:j].strip(), es[j:].strip()]
        else:
            raise SystemExit('não sei partir: %s' % old[junto])
        assert len(partes) == k, (old[junto], partes)
        for y, t in zip(pecas, partes): out[y['id']] = t.strip(); mudou.add(p)
        i += k
for k, v in m.items():
    if k not in out and k[1:].split('_')[0] not in mudou: out[k] = v
json.dump(out, open('produccion/mapa-es.json', 'w'), ensure_ascii=False, indent=1)
print('páginas remapeadas:', sorted(mudou, key=int), len(m), '->', len(out))
