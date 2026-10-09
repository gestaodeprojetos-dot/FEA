#!/usr/bin/env python3
"""Gera o HTML do doc de copy dos criativos estáticos (vira Google Doc no upload).

    python3 fea_gerar_doc_copy.py  ->  FEA-copy-criativos-v2.html

Dados em FEA-copy-criativos-final.py (lista C). O doc mora em 1. COPY / 2. Criativos;
as artes ES vão para a pasta ESTÁTICOS do tráfego.
"""
import html, os

AQUI = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(AQUI, 'FEA-copy-criativos-final.py'), encoding='utf-8').read(), ns)
C = ns['C']

BRASIL = 'https://drive.google.com/drive/folders/1UoFid4S3Fdb2VsZq49k_TZGHpf9clCNF'
ESTATICOS = 'https://drive.google.com/drive/folders/1RibhoTeWsYU5wf4q__1aV_QGXGCia2n4'
PDF_ES = 'https://drive.google.com/file/d/1xZR8Y-3gtfZX9pnFUskn27V0O4kUw9al/view'
e = html.escape

h = ['<html><body><h1>Copy dos criativos estáticos · Ebook Olheiras LATAM (PT | ES) · v2</h1>',
     f'<p><b>Uso:</b> trocar <u>só</u> o texto de cada arte do Brasil pelo espanhol abaixo, mantendo layout, fotos, cores e fontes. '
     f'Origem: <a href="{BRASIL}">1. Vendas (Brasil)</a>. Salvar as artes ES na pasta <a href="{ESTATICOS}">ESTÁTICOS (tráfego)</a> trocando '
     '<b>PTO</b> por <b>PTO-LATAM</b> no nome. Story usa a mesma copy do Feed. Este doc fica em 1. COPY / 2. Criativos (regra: todo doc de copy mora na pasta de copy).</p>',
     '<p><b>v2:</b> (1) preço no padrão das traduções LATAM de Olheiras: mantém o valor do Brasil e marca [PRECIO EN MONEDA LOCAL: CONFIRMAR, el original dice …], '
     'que sai da arte quando o preço local for definido; (2) prova social universalizada: sem referência ao Brasil, um único conjunto de números '
     '(+30 mil copias vendidas do ebook; más de 30.000 alumnos, como na página de vendas ES) e selo "Método exclusivo del Dr. João Pithon"; '
     '(3) urgência ("48 horas", "SOLO HOY", "OFERTA LIMITADA"), "no es una técnica difícil" e a capa Allergan mantidos como no original, por decisão da gestão em 05/10/2026; '
     '(4) Ads 06 e Ads 09 transcritos olhando a imagem e já recompostos em espanhol (arquivos FEA-ES-Ads 06/09); '
     '(5) depoimentos em print: sem depoimento hispanohablante, o print fica original em português com legenda ES "Testimonio original en portugués".</p>',
     '<p><b>Qualidade:</b> skill fea-traduccion-es · auditor LIBERADO 100 %, 0 bloqueantes · revisão cega fea-revision-es com os achados de texto corrigidos.</p>']

for nome, arquivos, pares, nota in C:
    h.append(f'<h2>{e(nome)}</h2><p><i>{e(arquivos)}</i></p>')
    if pares:
        h.append('<table border="1" cellpadding="5"><tr><td><b>PT (Brasil)</b></td><td><b>ES (LATAM)</b></td></tr>')
        h += [f'<tr><td>{e(pt)}</td><td>{e(es)}</td></tr>' for pt, es in pares]
        h.append('</table>')
    if nota:
        h.append(f'<p>⚠️ {e(nota)}</p>')

h.append('<h2>Mockups do ebook: troca pela edição ES</h2>'
         f'<p>Toda arte que mostra capa ou página do ebook em português (algumas com página ilegível gerada por IA) recebe a capa ou a página real da '
         f'<a href="{PDF_ES}">edição ES em PDF</a>, na mesma posição e perspectiva. Nunca gerar capa ou página por IA. Artes afetadas: Ads 13, 14 e 15 (png); '
         '[FEED] ADS 02; [STORIES] ADS 01, 09, 15_V2 e 17; Ads 34 (título do capítulo 04 da edição ES); Ads 36 (página ES correspondente, QR para destino ES).</p>')
h.append('<h2>Pendências para a gestão</h2><ol>'
         '<li><b>Mídia:</b> QR Code do Ads 31 e mockup com QR do Ads 36 apontam para destino em português; "videoclases" (ADS 11 e 16) só com versão ES das videoaulas.</li>'
         '<li><b>Preço local:</b> substituir os marcadores [PRECIO EN MONEDA LOCAL] quando a oferta em dólar estiver definida (o "76 %" do Ads 01 é recalculado junto); '
         'nas artes já recompostas (Ads 06 e 09) o preço segue R$ como no Brasil.</li>'
         '<li><b>Número de alunos:</b> confirmar com o Dr. João que "más de 30.000 alumnos" (página de vendas ES) é o dado vigente.</li>'
         '<li><b>TCLE:</b> conferir autorização das fotos de paciente nos prints de depoimento (ADS 05 e 08).</li></ol></body></html>')

open(os.path.join(AQUI, 'FEA-copy-criativos-v2.html'), 'w', encoding='utf-8').write(''.join(h))
print('ok', sum(len(x) for x in h), 'caracteres')
