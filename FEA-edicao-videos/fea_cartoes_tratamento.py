#!/usr/bin/env python3
"""FEA: cartões de tratamento (número roxo + texto) e resumo dos 3. Uso: python3 fea_cartoes_tratamento.py FONTE PASTA ITENS_JSON RESUMO_JSON"""
import sys, json
from PIL import Image, ImageDraw, ImageFont
F, P, itens = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
ft=ImageFont.truetype(F,64); fn=ImageFont.truetype(F,70); d0=ImageDraw.Draw(Image.new("RGB",(1,1)))
for n,linhas in itens:
    larg=max(d0.textbbox((0,0),l,font=ft)[2] for l in linhas)
    W=larg+270; H=90*len(linhas)+90
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,W-1,H-1],28,fill=(255,255,255,255))
    d.ellipse([50,H//2-55,160,H//2+55],fill=(91,69,153,255))
    b=d.textbbox((0,0),n,font=fn); d.text((105-(b[0]+b[2])/2,H//2-(b[1]+b[3])/2),n,font=fn,fill=(255,255,255,255))
    y=45
    for l in linhas: d.text((200,y),l,font=ft,fill=(30,27,75,255)); y+=90
    im.save(f"{P}/t{n}.png")
# resumo: 3 cartões de uma linha
ft=ImageFont.truetype(F,56); fn=ImageFont.truetype(F,56)
res=[(n," ".join(l).replace("(","").replace(")","")) for n,l in itens]
res=[(n,t) for n,t in json.loads(sys.argv[4])]
larg=max(d0.textbbox((0,0),t,font=ft)[2] for _,t in res); W=larg+200; h=140
im=Image.new("RGBA",(W,3*h+44),(0,0,0,0)); d=ImageDraw.Draw(im)
for i,(n,t) in enumerate(res):
    y=i*(h+22); d.rounded_rectangle([0,y,W-1,y+h-1],26,fill=(255,255,255,255))
    d.ellipse([34,y+h//2-44,122,y+h//2+44],fill=(91,69,153,255))
    b=d.textbbox((0,0),n,font=fn); d.text((78-(b[0]+b[2])/2,y+h//2-(b[1]+b[3])/2),n,font=fn,fill=(255,255,255,255))
    b=d.textbbox((0,0),t,font=ft); d.text((150,y+h//2-(b[1]+b[3])/2),t,font=ft,fill=(30,27,75,255))
im.save(f"{P}/t_todos.png")
