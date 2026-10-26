"""Monta o spec de edição (cards, telas cheias, botão) a partir das palavras em espanhol do vídeo dublado.
Uso: fea_bft_plan.py palavras.json video.mp4 saida.mp4 spec.json [ajustes.json]"""
import json, re, sys, unicodedata, subprocess

def nz(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.sub(r"[^a-z0-9% ]", "", "".join(c for c in t if not unicodedata.combining(c)))

words, video, out, specp = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3], sys.argv[4]
adj = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
T = [nz(w[2]) for w in words]
txt = " ".join(T)


def find(pat, after=0.0):
    """tempos (início, fim) das ocorrências de uma sequência de palavras."""
    toks = pat.split(); res = []
    for i in range(len(T) - len(toks) + 1):
        if all(re.fullmatch(p, T[i + j]) for j, p in enumerate(toks)) and words[i][0] >= after:
            res.append((words[i][0], words[i + len(toks) - 1][1], i))
    return res


inserts, cards, cta = [], [], []
busy = []
def free(a, b): return all(b <= x0 - 0.4 or a >= x1 + 0.4 for x0, x1 in busy)
def add_insert(a, b, **kw):
    a, b = max(1.6, a), min(dur - 0.3, b)
    if not free(a, b):  # encurta para caber antes do próximo elemento ocupado
        nxt = min((x0 for x0, x1 in busy if x0 > a), default=b)
        b = min(b, nxt - 0.45)
    if b - a < 1.6 or not free(a, b): return False
    inserts.append(dict(t0=round(a, 2), t1=round(b, 2), **kw)); busy.append((a, b)); return True

# botão nas menções de "Más información"
for a, b, i in find(r"mas informacion"):
    s0 = next((words[j][0] for j in range(i, max(-1, i - 5), -1) if re.match(r"(haz|clic|toca|aqui)", T[j])), a)
    cta.append({"t0": round(s0 - 0.1, 2), "t1": round(min(dur, b + 1.6), 2)}); busy.append((s0 - 0.1, b + 1.6))

first_end = next((w[1] for w in words if w[2][-1:] in ".!?" and w[1] > 2.5), 3.5)
hook_end = min(first_end + 0.3, 3.8)
busy.append((0.0, hook_end))  # o card de abertura fica pelo menos até o fim da 1a frase
# 1) checklist quando cita toxina/relleno/bioestimuladores juntos (1a vez)
for a, b, i in find(r"(toxina|relleno|bioestimuladores?)"):
    near = [w for w in words[i + 1:i + 14] if re.match(r"(toxina|relleno|bioestimulador)", nz(w[2]))]
    if near:
        a = max(a, hook_end + 0.6)
        end = max(near[-1][1] + 0.5, a + 2.4)
        if add_insert(a - 0.1, min(end, a + 3.6), kind="checklist", title="Combo Total",
                      items=["Toxina botulínica", "Relleno facial", "Bioestimuladores de colágeno"]): break
# 2) número de clases
for a, b, i in sorted(find(r"\d+ clases"), key=lambda x: -int(T[x[2]])):
    if add_insert(a - 0.2, a + 2.4, kind="number", value="+" + T[i], label="clases disponibles"): break
# 3) data do en vivo
for a, b, i in find(r"10 de noviembre"):
    if add_insert(a - 0.3, a + 2.6, kind="date"): break
# 4) arte Combo Total (1a menção depois de 4 s)
for a, b, i in find(r"combo total", after=4.0):
    if add_insert(a - 0.2, a + 2.4, kind="combo"): break

if not any(i["kind"] == "combo" for i in inserts):  # sem espaço na menção do Combo: usa outra menção da Black Friday
    for a, b, i in find(r"black friday", after=8.0):
        if add_insert(a - 0.2, a + 2.4, kind="combo"): break

# cards no topo
def add_card(a, b, label, title):
    a = max(0.15, a); b = min(dur - 0.2, b)
    if b - a < 1.5: return
    if any(not (b <= c["t0"] - 0.3 or a >= c["t1"] + 0.3) for c in cards): return
    cards.append({"t0": round(a, 2), "t1": round(b, 2), "label": label, "title": title})

add_card(0.15, hook_end, "Black Friday Total", adj.get("hook", "Todos mis cursos en un solo combo"))
for a, b, i in find(r"(12|doce) meses") + find(r"un ano"):
    add_card(a - 0.3, a + 3.0, "Acceso por 12 meses", "Toxina, relleno y bioestimuladores"); break
for a, b, i in find(r"espanol"):
    if a > 3: add_card(a - 0.4, a + 2.8, "100% en español", "Clases, resúmenes y materiales"); break
for a, b, i in find(r"bonos"):
    add_card(a - 0.4, a + 3.0, "Solo para quien esté en vivo", "Bonos exclusivos en la apertura"); break
for a, b, i in find(r"menor precio"):
    add_card(a - 0.4, a + 2.8, "Black Friday Total", "Al menor precio posible"); break

spec = {"video": video, "out": out, "words": words, "cards": cards, "inserts": sorted(inserts, key=lambda x: x["t0"]), "cta": cta,
        "endcard": adj.get("endcard")}
for k in ("cards", "inserts", "cta"):
    if k in adj: spec[k] = adj[k]
json.dump(spec, open(specp, "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: spec[k] for k in ("cards", "inserts", "cta")}, ensure_ascii=False))
