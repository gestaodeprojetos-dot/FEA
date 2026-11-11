"""Gera a logo ELITE EXPERIENCE a partir do vetor original do Elite Mentoring (EM_Asset 19.svg).
O símbolo e a palavra ELITE são copiados do original sem alteração; a palavra EXPERIENCE é montada
com o mesmo traço das letras de MENTORING (E, N, R, I reaproveitadas; X, P e C construídas no mesmo traço)."""
import re, pathlib
AQUI = pathlib.Path(__file__).resolve().parent
orig = (AQUI / 'origem' / 'FEA-elite-mentoring-original.svg').read_text()

# --- partes do original que ficam iguais (símbolo + ELITE) ---
body = re.search(r'<g id="Layer_1">(.*)</g>', orig, re.S).group(1)
elems = re.findall(r'<(?:path|polygon|rect)[^>]*/>', body)
manter = [e for e in elems if 'cls-5' not in e]          # tudo menos as letras de MENTORING
defs = re.search(r'<defs>.*?</style>(.*?)</defs>', orig, re.S).group(1)  # gradientes do símbolo

Y0, Y1 = 93.7, 119.22
def poly(pts, dx):  # pts relativos -> string
    return ' '.join(f'{x+dx:.2f} {y:.2f}' for x, y in pts)

def shift_poly(points_str, ox):
    v = list(map(float, points_str.split()))
    return [(v[i]-ox, v[i+1]) for i in range(0, len(v), 2)]

E_pts = shift_poly("205.01 106.93 218.78 106.93 218.78 104.55 205.01 104.55 205.01 96.12 219.55 96.12 219.55 93.7 202.36 93.7 202.36 119.22 219.62 119.22 219.62 116.8 205.01 116.8 205.01 106.93", 202.36)
N_pts = shift_poly("255.26 114.65 237.03 93.7 235.09 93.7 235.09 119.22 237.74 119.22 237.74 98.44 255.94 119.22 257.92 119.22 257.92 93.7 255.26 93.7 255.26 114.65", 235.09)
W_X, w = 20.0, 3.2
X_a = [(0, Y0), (w, Y0), (W_X, Y1), (W_X-w, Y1)]
X_b = [(W_X-w, Y0), (W_X, Y0), (w, Y1), (0, Y1)]

def R_path(dx):
    o = 345.62 - dx
    return (f'M{362.61-o:.2f},100.28c0-3.96-3.12-6.58-7.79-6.58h-9.2v25.52h2.65v-12.29h5.44l11.82,12.29h3.32l-11.99-12.46'
            f'c3.53-.67,5.74-3.09,5.74-6.48ZM{348.27-o:.2f},104.55v-8.46h6.55c3.09,0,5.14,1.68,5.14,4.23s-2.05,4.23-5.14,4.23h-6.55Z')
def P_path(dx):
    o = 345.62 - dx
    return (f'M{362.61-o:.2f},100.28c0-3.96-3.12-6.58-7.79-6.58h-9.2v25.52h2.65v-12.29h6.55c4.67,0,7.79-2.69,7.79-6.65Z'
            f'M{348.27-o:.2f},104.55v-8.46h6.55c3.09,0,5.14,1.68,5.14,4.23s-2.05,4.23-5.14,4.23h-6.55Z')
def C_path(dx):
    # derivado do G original: mesmo centro, mesmos raios interno/externo e mesmo corte do terminal superior,
    # espelhado embaixo
    cx, cy, ri, ro = 452.46, 106.48, 10.64, 13.24
    o = (cx - ro) - dx
    ix, iyt, iyb = 460.48 - o, 99.48, 113.48
    ox_, oyt, oyb = 462.81 - o, 98.22, 114.74
    return (f'M{ix:.2f},{iyt}A{ri},{ri} 0 1 0 {ix:.2f},{iyb}L{ox_:.2f},{oyb}A{ro},{ro} 0 1 1 {ox_:.2f},{oyt}Z')

larg = {'E': 17.26, 'X': W_X, 'P': 16.99, 'R': 21.3, 'I': 2.65, 'N': 22.83, 'C': 23.59}
palavra = 'EXPERIENCE'
gaps = [13, 13, 15.5, 15.5, 15.5, 16, 15.5, 12.5, 13.5]
x_ini, x_fim = 160.2, 465.25            # mesma largura ocupada por MENTORING no original
soma_l = sum(larg[c] for c in palavra)
k = (x_fim - x_ini - soma_l) / sum(gaps)
def letras(cls):
    out, x = [], x_ini
    for i, c in enumerate(palavra):
        if c == 'E': out.append(f'<polygon class="{cls}" points="{poly(E_pts, x)}"/>')
        elif c == 'N': out.append(f'<polygon class="{cls}" points="{poly(N_pts, x)}"/>')
        elif c == 'X': out += [f'<polygon class="{cls}" points="{poly(X_a, x)}"/>', f'<polygon class="{cls}" points="{poly(X_b, x)}"/>']
        elif c == 'R': out.append(f'<path class="{cls}" d="{R_path(x)}"/>')
        elif c == 'P': out.append(f'<path class="{cls}" d="{P_path(x)}"/>')
        elif c == 'I': out.append(f'<rect class="{cls}" x="{x:.2f}" y="{Y0}" width="2.65" height="25.52"/>')
        elif c == 'C': out.append(f'<path class="{cls}" fill-rule="evenodd" d="{C_path(x)}"/>')
        x += larg[c] + (gaps[i] * k if i < len(gaps) else 0)
    return out

def svg(nome, cor_elite, cor_exp, grad, fundo=None):
    d = defs
    d = re.sub(r'stop-color="#85f9f7"', f'stop-color="{grad[0]}"', d)
    d = re.sub(r'stop-color="#2db9b3"', f'stop-color="{grad[1]}"', d)
    style = (f'.cls-1{{fill:{cor_elite};}}.cls-2{{fill:url(#linear-gradient-3);}}.cls-3{{fill:url(#linear-gradient-2);}}'
             f'.cls-4{{fill:url(#linear-gradient);}}.cls-5{{fill:{cor_exp};}}')
    bg = f'<rect x="-30" y="-30" width="529.14" height="179.88" fill="{fundo}"/>' if fundo else ''
    vb = '-30 -30 529.14 179.88' if fundo else '0 0 469.14 119.88'
    s = (f'<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
         f'viewBox="{vb}"><title>Elite Experience</title><defs><style>{style}</style>{d}</defs>{bg}<g id="logo">'
         + ''.join(manter) + ''.join(letras('cls-5')) + '</g></svg>')
    (AQUI / f'{nome}.svg').write_text(s)
    return nome

# A: mesma paleta do Elite Mentoring
svg('FEA-elite-experience-A-paleta-mentoring', '#4d5e65', '#6dcdc9', ('#85f9f7', '#2db9b3'))
# B: EXPERIENCE e símbolo em dourado (evento presencial), ELITE mantém o cinza-azulado
svg('FEA-elite-experience-B-dourado', '#4d5e65', '#b8913f', ('#ecd08a', '#a87b2c'))
# C: dourado sobre fundo escuro (backdrop, telão, credencial)
svg('FEA-elite-experience-C-dourado-fundo-escuro', '#f2efe8', '#d4b06a', ('#f3dc9e', '#b48836'), fundo='#16202a')
print('ok', round(k, 4))
