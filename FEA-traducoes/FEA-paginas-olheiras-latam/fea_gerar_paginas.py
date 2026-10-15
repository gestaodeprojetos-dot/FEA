#!/usr/bin/env python3
"""Gera, para cada página ES do Ebook Olheiras LATAM, uma pasta com .json e .html.

    python3 fea_gerar_paginas.py  ->  FEA-ES-<slug>/FEA-ES-<slug>.json e .html

O JSON é a estrutura de seções (fonte única); o HTML é renderizado dele, para o
designer finalizar. Preços, checkout e WhatsApp pendentes aparecem em destaque.
"""
import html, json, os, re
from fea_paginas_conteudo import PAGINAS

AQUI = os.path.dirname(os.path.abspath(__file__))
e = html.escape

CSS = """:root{--roxo:#5B4599;--azul:#3846BB;--lav:#D0D1E9;--alerta:#BB3838;--off:#F9F9F9;--borda:#E9E9E9;--txt:#1F1D2B;--sub:#55536A;--r:12px}
*{box-sizing:border-box}body{margin:0;background:var(--off);color:var(--txt);font:400 17px/1.65 Montserrat,sans-serif}
h1,h2,h3{font-family:Sora,sans-serif;line-height:1.2;margin:0 0 16px}h1{font-size:clamp(28px,4.4vw,46px);font-weight:800}h2{font-size:clamp(23px,3.2vw,34px);font-weight:700;color:var(--roxo)}h3{font-size:19px;font-weight:600}
.w{max-width:1040px;margin:0 auto;padding:0 20px}section{padding:64px 0;border-bottom:1px solid var(--borda)}section:nth-of-type(even){background:#fff}
.eyebrow{display:inline-block;font:700 13px Sora,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--azul);background:var(--lav);padding:6px 14px;border-radius:999px;margin-bottom:16px}
.hero{background:linear-gradient(135deg,var(--roxo),var(--azul));color:#fff}.hero h1{color:#fff}.hero .sub{opacity:.92}.hero .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}
.btn{display:inline-block;margin-top:24px;background:var(--roxo);color:#fff;font:700 16px Sora,sans-serif;text-transform:uppercase;padding:18px 32px;border-radius:var(--r);text-decoration:none;box-shadow:0 8px 24px rgba(91,69,153,.3)}
.hero .btn{background:#fff;color:var(--roxo)}.hero ul.ok li:before{color:#fff}
ul.l{padding:0;list-style:none}ul.l li{padding:8px 0 8px 32px;position:relative}ul.l li:before{content:"";position:absolute;left:0;top:14px;width:18px;height:18px;border-radius:50%;background:var(--lav)}
ul.ok li:before{content:"✓";background:none;color:var(--roxo);font-weight:800;top:7px}ul.no li:before{content:"✕";background:none;color:var(--alerta);font-weight:800;top:7px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}.card{background:#fff;border:1px solid var(--borda);border-radius:var(--r);padding:22px}.card b{display:block;font-family:Sora,sans-serif;color:var(--roxo);margin-bottom:6px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.media{border:2px dashed var(--azul);border-radius:var(--r);background:repeating-linear-gradient(45deg,#fff,#fff 10px,#F3F3FA 10px,#F3F3FA 20px);min-height:220px;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px;color:var(--azul);font:600 14px Sora,sans-serif;margin:20px 0}
.nota{border-left:4px solid #E0A100;background:#FFF8E1;padding:10px 14px;border-radius:6px;font-size:13px;color:#5C4A00;margin-top:20px}.nota:before{content:"NOTA PARA O DESIGNER · "; font-weight:700}
.pend{background:#FDECEC;color:var(--alerta);font-weight:700;padding:0 6px;border-radius:4px}
.bar{background:var(--alerta);color:#fff;text-align:center;font:700 15px Sora,sans-serif;padding:12px;position:sticky;top:0;z-index:9}
.prog{height:14px;background:var(--borda);border-radius:999px;overflow:hidden;margin-top:8px}.prog i{display:block;height:100%;background:var(--roxo)}
.offer{max-width:620px;margin:0 auto;background:#fff;border:2px solid var(--roxo);border-radius:16px;padding:36px;text-align:center}
.de{text-decoration:line-through;color:var(--sub)}.preco{font:800 44px Sora,sans-serif;color:var(--roxo);margin:6px 0}.timer{font:800 32px Sora,sans-serif;color:var(--alerta)}
.selos{margin-top:14px;font-size:13px;color:var(--sub)}
details{background:#fff;border:1px solid var(--borda);border-radius:var(--r);margin:10px 0;padding:16px 20px}summary{cursor:pointer;font:600 17px Sora,sans-serif;color:var(--roxo)}
blockquote{margin:10px 0;padding:12px 18px;border-left:4px solid var(--roxo);background:var(--lav);border-radius:0 8px 8px 0;font-style:italic}
.var{opacity:.5}.var.on{opacity:1}.foot{background:var(--txt);color:#cfcfe0;text-align:center;font-size:13px;padding:28px 0}
#pendencias{background:#FFF8E1;font-size:14px}.nota,#pendencias,.media{overflow-wrap:anywhere}.btn{max-width:100%;text-align:center}#pendencias h2{color:#5C4A00;font-size:20px}
@media(max-width:760px){.hero .grid,.cols{grid-template-columns:1fr}section{padding:44px 0}.offer{padding:24px}}"""

JS = """document.querySelectorAll('[data-timer]').forEach(el=>{let s=+el.dataset.timer*60;const t=()=>{const m=String(Math.floor(s/60)).padStart(2,'0'),x=String(s%60).padStart(2,'0');el.textContent='00:'+m+':'+x;if(s>0)s--};t();setInterval(t,1000)});"""


def txt(s):
    """Escapa e destaca marcadores [PENDENTE] e preços sem valor."""
    s = e(s)
    return re.sub(r'(US\$ \[[^\]]+\]|\[[A-ZÁÉÍÓÚÑ][^\]]*\])', r'<span class="pend">\1</span>', s)


def cta(c):
    if not c:
        return ''
    href = c['acao'] if c['acao'].startswith('#') else '#'
    extra = '' if c['acao'].startswith('#') else f' data-pendente="{e(c["acao"])}"'
    return f'<a class="btn" href="{href}"{extra}>{txt(c["texto"])}</a>'


def lista(itens, cls='ok'):
    return f'<ul class="l {cls}">' + ''.join(f'<li>{txt(i)}</li>' for i in itens) + '</ul>' if itens else ''


def midias(s):
    return ''.join(f'<div class="media">[{e(m["tipo"].upper())}] {e(m["descricao"])}</div>' for m in s.get('midia', []))


def secao(s):
    t = s['tipo']
    head = (f'<span class="eyebrow">{txt(s["eyebrow"])}</span>' if s.get('eyebrow') else '')
    tag = 'h1' if t in ('hero', 'headline_variants') else 'h2'
    head += f'<{tag}>{txt(s["titulo"])}</{tag}>' if s.get('titulo') else ''
    corpo = ''.join(f'<p>{txt(p)}</p>' for p in s.get('texto', []))
    nota = f'<div class="nota">{txt(s["nota_designer"])}</div>' if s.get('nota_designer') else ''
    sid = f'id="{s["id"]}"'
    if t == 'timer_bar':
        return f'<div class="bar" {sid}>{txt(s["texto"][0])} <span data-timer="{s["timer_min"]}">00:15:00</span></div>'
    if t == 'alert_bar':
        return f'<div class="bar" {sid}>{txt(s["texto"][0])}</div>'
    if t == 'progress_bar':
        return f'<section {sid}><div class="w"><b>{txt(s["texto"][0])}</b> {s["valor"]}%<div class="prog"><i style="width:{s["valor"]}%"></i></div></div></section>'
    if t == 'footer':
        return f'<footer class="foot">{txt(s["texto"][0])}</footer>'
    if t in ('hero', 'headline_variants'):
        if t == 'headline_variants':
            head = ''.join(f'<h1 class="var{" on" if i == 0 else ""}" data-variacao="{e(v["titulo"])}">{txt(v["texto"])}</h1>' for i, v in enumerate(s['itens']))
        sub = f'<p class="sub"><b>{txt(s["subtitulo"])}</b></p>' if s.get('subtitulo') else ''
        extra = f'<p class="sub">{txt(s["texto_extra"])}</p>' if s.get('texto_extra') else ''
        left = head + corpo + lista(s.get('lista')) + sub + extra + cta(s.get('cta'))
        right = midias(s) or '<div class="media">[MOCKUP] Capa ES do ebook</div>'
        return f'<section class="hero" {sid}><div class="w grid"><div>{left}</div><div>{right}</div></div><div class="w">{nota}</div></section>'
    body = corpo
    if t == 'pain':
        a, b = lista(s.get('contras'), 'no'), lista(s.get('pros'), 'ok')
        sub = f'<h3>{txt(s["subtitulo"])}</h3>' if s.get('subtitulo') else ''
        body += f'<div class="cols"><div>{b}</div><div>{a}</div></div>' if s.get('ordem') == 'pros_primeiro' else a + sub + b
    elif t in ('steps', 'features', 'bonuses', 'options'):
        body += '<div class="cards">' + ''.join(f'<div class="card"><b>{txt(i["titulo"])}</b>{txt(i["texto"])}</div>' for i in s['itens']) + '</div>'
    elif t == 'modules':
        body += ''.join(f'<details><summary>{txt(i["titulo"])}</summary>{lista(i["lista"])}</details>' for i in s['itens'])
    elif t == 'faq':
        body += ''.join(f'<details><summary>{txt(i["titulo"])}</summary><p>{txt(i["texto"])}</p></details>' for i in s['itens'])
    elif t == 'offer':
        ofr = head + lista(s.get('lista'))
        ofr += f'<p>{txt(s["texto_ancora"])}' + (f' <span class="de">{txt(s["preco_de"])}</span>' if s.get('preco_de') and 'debería' in s.get('texto_ancora', '') else '') + '</p>' if s.get('texto_ancora') else ''
        if s.get('preco_de') and 'debería' not in s.get('texto_ancora', ''):
            ofr += f'<p>De <span class="de">{txt(s["preco_de"])}</span></p>'
        ofr += f'<p>{txt(s.get("prefixo_preco", ""))}</p><div class="preco">{txt(s["preco"])}</div>'
        if s.get('timer_min'):
            ofr += f'<p><b>ESTA OFERTA TERMINA EN:</b></p><div class="timer" data-timer="{s["timer_min"]}">00:15:00</div>'
        ofr += cta(s.get('cta')) + (f'<div class="selos">{" | ".join(map(txt, s["selos"]))}</div>' if s.get('selos') else '')
        return f'<section {sid}><div class="w"><div class="offer">{ofr}</div>{midias(s)}{nota}</div></section>'
    else:
        body += ''.join(f'<blockquote>“{txt(c)}”</blockquote>' for c in s.get('citacoes', []))
        body += lista(s.get('lista'))
        if s.get('subtitulo'):
            body += f'<h3>{txt(s["subtitulo"])}</h3>'
    if s.get('texto_extra'):
        body += f'<p>{txt(s["texto_extra"])}</p>'
    if t == 'authority':
        return f'<section {sid}><div class="w cols"><div>{head}{body}{cta(s.get("cta"))}</div><div>{midias(s)}</div></div><div class="w">{nota}</div></section>'
    return f'<section {sid}><div class="w">{head}{body}{midias(s)}{cta(s.get("cta"))}{nota}</div></section>'


def pagina(p):
    pend = '<section id="pendencias"><div class="w"><h2>Pendências antes de publicar (remover esta seção)</h2>' + lista(p['pendencias'], 'no') + \
           f'<p>Copy fonte: <a href="{e(p["fonte_copy"])}">{e(p["fonte_copy"])}</a> · Identidade: {txt(p["identidade_visual"])}</p></div></section>'
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(p["pagina"])}</title><link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>' + ''.join(secao(s) for s in p['secoes']) + pend + f'<script>{JS}</script></body></html>')


if __name__ == '__main__':
    for p in PAGINAS:
        d = os.path.join(AQUI, f'FEA-ES-{p["slug"]}')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, f'FEA-ES-{p["slug"]}.json'), 'w', encoding='utf-8') as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        with open(os.path.join(d, f'FEA-ES-{p["slug"]}.html'), 'w', encoding='utf-8') as f:
            f.write(pagina(p))
        print(p['slug'], len(p['secoes']), 'seções')
