"""Checagem obrigatória NADA PERDIDO (criada depois da legenda da Fig. 18, que
perdeu uma linha sem nenhum aviso): toda palavra do mapa id->ES precisa estar na
camada de texto da página do PDF entregue.
Uso: python3 fea_conferir_perda.py mapa-es.json traduzido.pdf   (exit 1 se faltar)"""
import sys, re, json, collections, pymupdf
mapa = json.load(open(sys.argv[1])); doc = pymupdf.open(sys.argv[2])
def toks(t):
    t = re.sub(r'</?(b|i|br)\s*/?>', ' ', t).replace('\u00ad', '').replace('\u00a0', ' ')
    t = re.sub(r'(\w)-\s*\n\s*([a-záéíóúñü])', r'\1\2', t)   # só junta com continuação minúscula
    return [w for w in re.findall(r'[\wáéíóúñüÁÉÍÓÚÑÜ%]+', t.lower()) if len(w) > 1]
falta = []
porPag = collections.defaultdict(list)
for k, v in mapa.items():
    m = re.match(r'p(\d+)_', k)
    if m and v: porPag[int(m.group(1))].append((k, v))
for n, itens in sorted(porPag.items()):
    if n > doc.page_count: continue
    texto = doc[n - 1].get_text()
    # palavra partida no fim da página continua na seguinte
    if n < doc.page_count: texto += '\n' + doc[n].get_text()[:400]
    if n > 1: texto = doc[n - 2].get_text()[-400:] + '\n' + texto
    pag = collections.Counter(toks(texto))
    # também sem juntar hífen ('Filler-\nrelated' é palavra composta, não quebra)
    for w, c in collections.Counter(re.findall(r'[\wáéíóúñüÁÉÍÓÚÑÜ%]+', texto.lower().replace('\u00ad', ''))).items():
        pag[w] = max(pag[w], c)
    juntas = ' '.join(pag)
    for k, v in itens:
        need = collections.Counter(toks(v))
        # fragmento de palavra partida entre ids ('ries-' + 'gos') aparece
        # dentro da palavra inteira na página
        tv = toks(v); limpo = re.sub(r'<[^>]+>', '', v).strip()
        frag = set()
        if tv and limpo.endswith('-'): frag.add(tv[-1])
        if tv and limpo[:1].islower(): frag.add(tv[0])
        miss = [w for w, c in need.items() if pag[w] < c and not (w in frag and w in juntas)]
        if miss: falta.append((n, k, miss[:12]))
for f in falta: print(*f)
print(len(falta), 'ids com palavra faltando')
sys.exit(1 if falta else 0)
