#!/usr/bin/env python3
"""Gera o site estático da Vercel (public/index.html) a partir da página FEA-curadoria-instagram.html.

A página-fonte é escrita sem <html>/<head>/<body> (formato do link privado do Claude);
este script envolve o conteúdo num documento completo para a Vercel servir.
Uso: python3 fea_montar_site.py
"""
import os
aqui = os.path.dirname(os.path.abspath(__file__))
fonte = open(os.path.join(aqui, "FEA-curadoria-instagram.html"), encoding="utf-8").read()
corte = fonte.index('<header class="hero')
cabeca, corpo = fonte[:corte], fonte[corte:]
html = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + cabeca + '</head>\n<body>\n' + corpo + '\n</body>\n</html>\n')
os.makedirs(os.path.join(aqui, "public"), exist_ok=True)
open(os.path.join(aqui, "public", "index.html"), "w", encoding="utf-8").write(html)
print("ok: public/index.html")
