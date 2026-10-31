# FEA · Fundos procedurais do template de palco Elite Injectors Congress (4032 x 1344)
import numpy as np, sys
from PIL import Image, ImageFilter
W,H=4032,1344
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
def rgb(h): return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
PRETO=rgb('050C0F'); AZUL=rgb('7FB3C6'); GELO=rgb('D3EAF2'); FUNDO2=rgb('0B1A21'); RED=rgb('7F1D1D')
yy,xx=np.mgrid[0:H,0:W].astype(float)
def g(cx,cy,rx,ry): return np.exp(-(((xx-cx)/rx)**2+((yy-cy)/ry)**2))
def mix(img,col,a): return img*(1-a[...,None])+col*a[...,None]
def base(spots,floor=True):
    img=np.zeros((H,W,3))+PRETO
    img=mix(img,FUNDO2,0.55*g(W/2,H*0.55,W*0.7,H*0.9))
    for cx,rx,ry,a in spots:
        img=mix(img,AZUL,a*g(cx,-150,rx,ry))
        img=mix(img,GELO,a*0.35*g(cx,-200,rx*0.35,ry*0.5))
    if floor:
        img=mix(img,AZUL,0.45*g(W/2,H+10,W*0.38,70))
        img=mix(img,GELO,0.25*g(W/2,H+5,W*0.2,25))
    v=np.clip(((xx-W/2)/(W*0.62))**2+((yy-H/2)/(H*1.1))**2,0,1)
    img=img*(1-0.45*v[...,None])
    return img
def monograma(img,cx,top,altura,alpha_fill,alpha_line):
    m=Image.open('T-mask.png').split()[-1]
    w=int(m.width*altura/m.height); m=m.resize((w,altura),Image.LANCZOS)
    M=np.zeros((H,W)); x0=int(cx-w/2)
    ys,ye=max(0,top),min(H,top+altura); xs,xe=max(0,x0),min(W,x0+w)
    arr=np.asarray(m,float)/255
    M[ys:ye,xs:xe]=arr[ys-top:ye-top,xs-x0:xe-x0]
    Mi=Image.fromarray((M*255).astype(np.uint8))
    er=np.asarray(Mi.filter(ImageFilter.MinFilter(13)),float)/255
    edge=np.clip(M-er,0,1)
    glow=np.asarray(Image.fromarray((edge*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18)),float)/255
    fade=np.clip(1-(yy-max(top,0))/(H*1.05),0.08,1)
    img=mix(img,GELO,M*alpha_fill*fade)
    img=mix(img,AZUL,np.clip(glow*1.6,0,1)*alpha_line*0.6*fade)
    img=mix(img,GELO,edge*alpha_line*fade)
    return img
def save(img,nome):
    rng=np.random.default_rng(3); img=img+rng.normal(0,1.2,img.shape)
    Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save(f'{OUT}/{nome}'.replace('.png','.jpg'),quality=93,subsampling=0)
    print(nome)
a=base([(W/2,1500,1000,.42)]); a=monograma(a,W/2,-260,1900,.05,.42); save(a,'FEA-elite-fundo-abertura.png')
h=base([(3150,1300,950,.40)]); h=monograma(h,3150,-120,1750,.05,.38); save(h,'FEA-elite-fundo-destaque.png')
save(base([(W/2,1900,800,.22)]),'FEA-elite-fundo-conteudo.png')
c=base([(W/2,1500,950,.34)]); save(c,'FEA-elite-fundo-centro.png')
r=base([(3300,1500,800,.18)]); r=mix(r,RED,0.5*g(0,H,1700,900)); save(r,'FEA-elite-fundo-alerta.png')
