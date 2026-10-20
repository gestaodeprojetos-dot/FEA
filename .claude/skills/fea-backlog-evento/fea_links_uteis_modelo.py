#!/usr/bin/env python3
"""Planilha "Links úteis" LATAM no padrão exato da planilha Brasil (Links úteis | Perpétuo).

Usa o próprio xlsx exportado do Brasil como molde (fonte, larguras, estilos, cabeçalho)
e troca só o conteúdo da coluna LINK: texto = nome do arquivo, hyperlink = URL.
    python3 fea_links_uteis_modelo.py br.xlsx SAIDA.xlsx
"""
import sys, copy
from openpyxl import load_workbook
from openpyxl.styles import Font

D = 'https://drive.google.com/drive/folders/'
G = 'https://docs.google.com/document/d/'
S = 'https://docs.google.com/spreadsheets/d/'
F = 'https://drive.google.com/file/d/'

# linha do molde Brasil -> (texto exibido, url ou None)
LINHAS = {
    2: ('Ebook olheiras Latam', D + '1n2cSn7QoPj8rxcp7MvZTNAuZOzVpY4kc'),
    4: ('1. COPY', D + '1YUTK9DaHqRcbeJq79ZWNHMA6StfcghCr'),
    5: ('FEA-ES | Copy Página eBook Ojeras', G + '1_Af60zj_W4Cld_q9JDKi9-ispKT2HUTLqxtw43wHEqg/edit'),
    6: ('FEA-ES | Página de Upsell - Cpx (Curso de Relleno Express)', G + '1xSxWtG7pvjFxLJsA_c1xj5ev9pm_er25Uy3Kp2R5iKE/edit'),
    7: ('FEA-ES | Checkout personalizado I e-Book', G + '1PEiblJvEh754uu8sOm71kG9EcmytGfHWRijN8iAmTIQ/edit'),
    8: ('FEA-ES | Creativos - eBook Relleno de Ojeras', G + '1aPENAjSDasC6RG8wcLg74dowKXJzpJwrRXSY5rWR5ME/edit'),
    9: ('FEA-ES | Creativos - eBook Relleno de Ojeras 2', G + '1gBY3ZkXgxrej8zyF-BwWPpVl2dxYvtgplK6p11Lewlc/edit'),
    10: ('FEA-ES | Leyendas de creativos (ventas y remarketing) - eBook Ojeras', G + '1Y2j4EnGg4H9n74A947ghMHZ_FU-JiOlKkIEHCT2Vatw/edit'),
    11: ('FEA-ES | Listboss API - eBook Ojeras', G + '1_2qjfrzOjOdkVt5iCVV50rZEGAawXcflJZ2wFfGfOhM/edit'),
    12: ('FEA-ES | Listboss Email - eBook Ojeras', G + '1_lBObGj1I0AFTjgiqnyaHXxJ0z2F5yGMwEqyMkYgtco/edit'),
    13: ('FEA-ES | Onboarding API + Grupo lleno (inclui descripción del grupo)', G + '1wcQnNSkr9F6wVRyQKG4Fu4EO2qh8Qaxy8-DmVVOJSoI/edit'),
    14: ('FEA-Avatar Grupo de Alumnos - LATAM.png (pasta 3. Capas grupo e formulários, aguardando upload)', D + '1ar8bBDc_TqFNULr1eawmTSgkfVFDQUrH'),
    16: ('2. ARTES', D + '1Q4UHzgdjlUx8_ewd1sBNWemyJ9JZT1ui'),
    17: ('1. Banner checkout', D + '1q5eyS55FaIDXOrsULKTYK2dAhL_jPlMq'),
    18: ('ESTÁTICOS', D + '1RibhoTeWsYU5wf4q__1aV_QGXGCia2n4'),
    19: ('VÍDEOS', D + '1ZKGD-pQ0iA8FHqx6Ekc8HvIWYeqkfPS3'),
    22: ('pendente: página de vendas LATAM (André Vivas)', None),
    23: ('pendente: página de upsell LATAM (André Vivas)', None),
    24: ('pendente: checkout Hotmart em USD', None),
    25: ('pendente: área de membros LATAM', None),
    29: ('pendente: páginas de teste LATAM', None), 30: (None, None), 31: (None, None), 32: (None, None),
    34: ('pendente: planilha de respostas da pesquisa LATAM', None),
    36: ('pendente: grupo de alunos LATAM', None),
}
EXTRAS = [  # mesmas duas colunas, depois do bloco do modelo
    ('Outros LATAM', None, None),
    ('Logo', 'FEA-Logo - Nome - Fonte - Ojeras LATAM.png (pasta 5. LOGO, aguardando upload)', D + '1SNsyj8xq-LdMXNkmI53NdVPOQmwwjupi'),
    ('Ebook em espanhol (PDF)', 'Relleno_Tridimensional_de_Ojeras_ES.pdf', F + '1xZR8Y-3gtfZX9pnFUskn27V0O4kUw9al/view'),
    ('Aulas traduzidas', 'Aulas traduzidas', D + '1lJlpRTaLmGc0PGEau01jTusnW8uV5t91'),
    ('Copy dos criativos estáticos', 'FEA-LATAM Copy dos Criativos Estáticos (PT | ES) v3 - Ebook Olheiras', G + '1jiKpctRIlg3LQHS2coCPLWmEELrSoRK9Z5C-g-gGn6E/edit'),
    ('Página de ventas', 'FEA-ES | Página de ventas - eBook de Ojeras', G + '1DcfgS833430UPwl7_X1E9WLBkbWc2ek37udyS0ylLSE/edit'),
    ('Página de ventas NUEVA', 'FEA-ES | [NUEVA] Página de ventas - eBook de Ojeras', G + '1pB0_8kKRS-VI3xZ8kOCDhcEoBqdJzvTJ5MvfYLruCJc/edit'),
    ('Página de ventas corta', 'FEA-ES | Página de ventas - corta - eBook de Ojeras', G + '1Vbpklmy46mTIQizp5eSsf1OKcVFQXA0dLnXFTY3-U-w/edit'),
    ('Página de gracias y encuesta', 'FEA-ES | Página de gracias y encuesta - eBook Ojeras', G + '10Z-Grn-krA7ARoh8w3Tg1gYrErBmHnCDanhnbPHPAmU/edit'),
    ('Comunicações', 'FEA-ES | Comunicaciones - eBook Ojeras', G + '1ZZA7C4vrGas5rKw5dP15pkTfdSNx1xeIRPj6uqJ5QwE/edit'),
    ('Mensagem com pesquisa e presente', 'FEA-ES | Mensaje con encuesta y regalo + API de encuesta - eBook Ojeras', G + '1nFYnMcpU_sPyz1mlCVRZL_LgRyhxGA0n1rTbu-9xFYM/edit'),
    ('Criativos de remarketing', 'FEA-ES | Creativos de remarketing - eBook Ojeras', G + '1nN9XNZaK536cLA6CDjvqB0qZQMTBIiGfRHiS3q00kpg/edit'),
    ('Descrição do grupo Low tickets', 'FEA-ES | Descripción del grupo I Low tickets', G + '1shuG_ioT7pMBeJrys-SBagkPURePnL6bSp6ndfTqhwg/edit'),
    ('Planilha de tráfego', 'FEA-Criativos para Tráfego - Ebook Olheiras LATAM', S + '13LRb10wwBDIdSsaOPxue6OYXCR0jlAVGm5U-zrwa70c/edit'),
    ('Links dos vídeos traduzidos', 'FEA-Links dos vídeos traduzidos - Ebook Olheiras LATAM', S + '1k9Cg8s6SIRdDhgVgFWhp9aPUL04zEfRvUGMPQ0nU3kc/edit'),
    ('Páginas em HTML e JSON (designer)', 'Copys páginas ES', D + '15RFlmEyX_sWqlCHJuL8ZPEo-YA0m8TgB'),
    ('Briefing reverso e planejamento', '0. PLANEJAMENTO (FEA-Briefing Reverso preenchido)', D + '1M4OEW8rnJlNtADlhKByQUM8dQJ3t3EjV'),
    ('Briefing de design', '2. ARTES (FEA-LATAM Briefing de Design)', D + '1Q4UHzgdjlUx8_ewd1sBNWemyJ9JZT1ui'),
    ('Briefing criativos e vídeo + inventário', '4. TRÁFEGO (FEA-LATAM Briefing Criativos e Edição de Vídeo e Inventário)', D + '1dsNl_SZq_LFbuqeI94ChQ7Mv1P8Jrt44'),
    ('Backlog ClickUp', 'Ebook Olheiras LATAM', 'https://app.clickup.com/9013080622/v/f/901319449714/901314001225'),
]

wb = load_workbook(sys.argv[1])
for n in wb.sheetnames:
    if n != 'EBOOK OLHEIRAS':
        del wb[n]
ws = wb['EBOOK OLHEIRAS']
ws.title = 'EBOOK OLHEIRAS LATAM'
link_font = ws['B5'].font
pend_font = Font(name='Arial', color='FFCC0000')
for r, (txt, url) in LINHAS.items():
    c = ws.cell(r, 2)
    c.hyperlink = None
    c.value = txt
    if url:
        c.hyperlink = url
        c.font = copy.copy(link_font)
    elif txt:
        c.font = pend_font
base = 39
cab_font = ws['A4'].font
for i, (nome, txt, url) in enumerate(EXTRAS):
    r = base + i
    a, b = ws.cell(r, 1), ws.cell(r, 2)
    a.value = nome
    a.font = copy.copy(cab_font if url is None else ws["A5"].font)
    a.alignment = copy.copy(ws["A5"].alignment)
    if txt:
        b.value = txt
        b.hyperlink = url
        b.font = copy.copy(link_font)
        b.alignment = copy.copy(ws["B5"].alignment)
wb.save(sys.argv[2])
print('ok', sys.argv[2])
