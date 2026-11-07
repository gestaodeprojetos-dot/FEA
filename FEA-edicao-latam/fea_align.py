"""Alinha o roteiro em espanhol (texto exato) aos tempos das palavras do whisper. Uso: fea_align.py palavras.json roteiro.txt saida.json"""
import json, re, sys, difflib, unicodedata


def norm(w):
    w = unicodedata.normalize("NFKD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if not unicodedata.combining(c)))


def align(words, script):
    sw = script.split()
    a = [norm(w[2]) for w in words]; b = [norm(x) for x in sw]
    out = [None] * len(sw)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): out[j1 + k] = [words[i1 + k][0], words[i1 + k][1], sw[j1 + k]]
        elif tag == "replace":
            t0, t1 = words[i1][0], words[i2 - 1][1]; n = j2 - j1
            for q in range(n): out[j1 + q] = [round(t0 + (t1 - t0) * q / n, 2), round(t0 + (t1 - t0) * (q + 1) / n, 2), sw[j1 + q]]
    # inserções (palavra do roteiro sem par): entre vizinhos
    for k, o in enumerate(out):
        if o is None:
            prev = next((out[j][1] for j in range(k - 1, -1, -1) if out[j]), 0.0)
            nxt = next((out[j][0] for j in range(k + 1, len(out)) if out[j]), prev + 0.3)
            out[k] = [prev, max(prev + 0.05, min(nxt, prev + 0.35)), sw[k]]
    return out


if __name__ == "__main__":
    w = json.load(open(sys.argv[1])); s = open(sys.argv[2]).read()
    json.dump(align(w, s), open(sys.argv[3], "w"), ensure_ascii=False)
