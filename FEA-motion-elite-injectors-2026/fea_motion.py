import sys, numpy as np, cv2, subprocess
S=sys.argv[1]; mode=sys.argv[2]  # 'preview' or 'render'
FPS=30; T=15.0; N=int(FPS*T)
img=cv2.imread(f'{S}/src/descanso.png',cv2.IMREAD_COLOR).astype(np.float32)/255
H,W=img.shape[:2]
plate=cv2.imread(f'{S}/work/plate.png').astype(np.float32)/255
pa=cv2.imread(f'{S}/work/people_alpha.png',0).astype(np.float32)/255
la=cv2.imread(f'{S}/work/logo_alpha.png',0).astype(np.float32)/255
# neon glow source: bright, bluish areas of the plate (top region)
lum=plate.mean(2)
bright=np.clip((lum-0.45)/0.35,0,1); bright[int(H*0.55):]*=0.3
glow=cv2.GaussianBlur(plate*bright[...,None],(0,0),35)*1.6
glow2=cv2.GaussianBlur(plate*bright[...,None],(0,0),8)
people=img.copy()
logo=img.copy()
# --- logo split into letters (ELITE) and subtitle letters (INJECTORS CONGRESS)
LX0,LY0,LX1,LY1=200,480,1240,860
lcrop=la[LY0:LY1,LX0:LX1]; ccrop=img[LY0:LY1,LX0:LX1]
nl,lab,st,_=cv2.connectedComponentsWithStats((lcrop>0.02).astype(np.uint8),8)
groups=[]  # (mask, kind, index, cx)
elite_cuts=[430,620,730,990]
gid={}
for i in range(1,nl):
    x,y,w,h,a=st[i]; cx=x+w/2+LX0; cy=y+h/2+LY0
    if cy<740:
        key=('E',int(np.searchsorted(elite_cuts,cx)))
    else:
        key=('S',i)
    gid.setdefault(key,[]).append(i)
LETTERS=[]
for key,ids in gid.items():
    m=np.isin(lab,ids)
    m=cv2.dilate(m.astype(np.uint8),np.ones((5,5),np.uint8)).astype(bool)
    ys,xs=np.where(m); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    a=(lcrop*m)[y0:y1,x0:x1]
    LETTERS.append(dict(kind=key[0],k=key[1],x0=x0+LX0,y0=y0+LY0,a=a,c=ccrop[y0:y1,x0:x1].copy(),cx=(x0+x1)/2+LX0))
nE=sum(1 for L in LETTERS if L['kind']=='E')
LCX,LCY=(LX0+LX1)/2,(LY0+LY1)/2
# --- individual sway centers (face positions, full res)
FACES=[(1774,330),(2066,250),(2419,250),(2701,200),(2984,250),(3296,250),(3608,290),
       (1986,580),(2318,570),(2701,640),(3054,600),(3366,600)]
rngs=np.random.default_rng(3)
SW=[dict(cx=c[0],cy=c[1],ax=rngs.uniform(7,11)*rngs.choice([-1,1]),ay=rngs.uniform(4,7),
         fx=int(rngs.integers(1,3)),fy=int(rngs.integers(1,3)),px=rngs.uniform(0,6.28),py=rngs.uniform(0,6.28)) for c in FACES]
Xf=np.arange(W,dtype=np.float32)[None,:]; Yf=np.arange(H,dtype=np.float32)[:,None]
G=[np.exp(-((Xf-f['cx'])/160)**2-((Yf-f['cy'])/240)**2).astype(np.float32) for f in SW]
Gs=sum(G)+0.06
wy=np.clip((H-Yf)/380,0,1).astype(np.float32)
WN=[(g/Gs*wy).astype(np.float32) for g in G]
del G,Gs
GX,GY=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
rng=np.random.default_rng(7)
def mkp(n,rmin,rmax,amax):
    return dict(x=rng.uniform(0,W,n),y=rng.uniform(H*0.15,H*1.05,n),r=rng.uniform(rmin,rmax,n),
                v=rng.uniform(40,140,n),ph=rng.uniform(0,T,n),a=rng.uniform(0.25,1,n)*amax,
                dx=rng.uniform(-25,25,n),k=rng.integers(1,3,n))
PB=mkp(170,1.5,5,0.55); PF=mkp(26,7,16,0.22)
sprites={}
def sprite(r):
    key=round(r*2)/2
    if key not in sprites:
        s=int(key*4)+3; yy,xx=np.mgrid[-s:s+1,-s:s+1]
        g=np.exp(-(xx**2+yy**2)/(2*(key*0.9)**2)).astype(np.float32)
        sprites[key]=g
    return sprites[key]
COL=np.array([1.0,0.88,0.62],np.float32)  # BGR light cyan-blue
def particles(buf,P,t):
    for i in range(len(P['x'])):
        u=((t+P['ph'][i])%T)/T  # lifecycle 0..1 within loop
        al=P['a'][i]*np.sin(np.pi*u)**1.5*(0.75+0.25*np.sin(2*np.pi*P['k'][i]*t/T+i))
        if al<0.01: continue
        x=P['x'][i]+P['dx'][i]*np.sin(2*np.pi*u); y=P['y'][i]-P['v'][i]*u*T*0.35
        g=sprite(P['r'][i]); s=g.shape[0]//2
        xi,yi=int(x),int(y)
        x0,x1=max(xi-s,0),min(xi+s+1,W); y0,y1=max(yi-s,0),min(yi+s+1,H)
        if x0>=x1 or y0>=y1: continue
        buf[y0:y1,x0:x1]+=g[y0-(yi-s):y1-(yi-s),x0-(xi-s):x1-(xi-s),None]*al*COL
def aff(scale,tx,ty,cx,cy):
    return np.float32([[scale,0,(1-scale)*cx+tx],[0,scale,(1-scale)*cy+ty]])
X=np.arange(W,dtype=np.float32)[None,:]; Y=np.arange(H,dtype=np.float32)[:,None]
def frame(t):
    w=2*np.pi*t/T
    # background: slow breathing zoom + lateral drift, neon pulse
    k=0.55+0.45*np.sin(2*w-0.6)
    bgsrc=plate+glow*(0.04+0.12*k)+glow2*(0.02+0.05*k)
    M=aff(1.045+0.018*np.sin(w),-20*np.sin(w),6*np.cos(w),W/2,H/2)
    bg=cv2.warpAffine(bgsrc,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    # light sweep across background, once per loop (off-screen at loop seam)
    pos=-0.35*W+1.7*W*(t/T)
    d=(X+0.45*Y-pos)
    band=np.exp(-(d/260)**2)*0.16+np.exp(-(d/60)**2)*0.05
    bg=1-(1-bg)*(1-band[...,None]*COL)
    particles(bg,PB,t)
    # people: counter-parallax, anchored bottom-center
    sc=1.0+0.022*(0.5-0.5*np.cos(w)); tx=14*np.sin(w); ax_,ay_=2700,H
    qx=(GX-tx-ax_)/sc+ax_; qy=(GY-ay_)/sc+ay_
    dx=np.zeros((H,W),np.float32); dy=np.zeros((H,W),np.float32)
    for f,wn in zip(SW,WN):
        dx+=wn*np.float32(f["ax"]*np.sin(f["fx"]*w+f["px"])); dy+=wn*np.float32(f["ay"]*np.sin(f["fy"]*w+f["py"]))
    mx=(qx-dx).astype(np.float32); my=(qy-dy).astype(np.float32)
    pw=cv2.remap(people,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    aw=cv2.remap(pa,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)[...,None]
    out=bg*(1-aw)+pw*aw
    particles(out,PF,t)
    # logo: breathing scale + float, ELITE letters wave and light up one by one, subtitle tracking wave
    ls=1.0+0.03*np.sin(w-0.8); lfy=8*np.sin(w+0.5)
    pad=40
    canvas_c=np.zeros((LY1-LY0+2*pad,LX1-LX0+2*pad,3),np.float32); canvas_a=np.zeros(canvas_c.shape[:2],np.float32)
    canvas_g=np.zeros(canvas_c.shape[:2],np.float32)
    for L in LETTERS:
        if L['kind']=='E':
            i=L['k']
            ox=0; oy=-11*np.sin(2*w-i*0.9)
            lt=(t-0.8-0.35*i)
            lit=np.exp(-(lt/0.28)**2)+np.exp(-((t-8.3-0.35*i)/0.28)**2)
        else:
            ox=(L['cx']-LCX)*0.025*np.sin(w-0.8); oy=-4*np.sin(2*w-(L['cx']-LX0)*0.008-1.2)
            lit=0.0
        h,wl=L['a'].shape
        X0=L['x0']-LX0+pad+ox; Y0=L['y0']-LY0+pad+oy
        Mt=np.float32([[1,0,X0],[0,1,Y0]])
        sz=(canvas_c.shape[1],canvas_c.shape[0])
        a2=cv2.warpAffine(L['a'],Mt,sz,flags=cv2.INTER_LINEAR)
        c2=cv2.warpAffine(L['c'],Mt,sz,flags=cv2.INTER_LINEAR)
        canvas_c=canvas_c*(1-a2[...,None])+c2*a2[...,None]
        canvas_a=np.maximum(canvas_a,a2)
        if lit>0.01: canvas_g+=a2*lit
    # place canvas with global logo transform
    Ml=aff(ls,-LX0+pad*0,lfy,LCX-LX0+pad,LCY-LY0+pad)
    Ml=np.float32([[ls,0,(1-ls)*LCX+LX0*(ls-ls)+ (LX0-pad)*ls - (LX0-pad)*0 ],[0,ls,0]])
    # explicit: canvas coord u -> frame coord: LCX + ls*(u + LX0 - pad - LCX)
    Ml=np.float32([[ls,0,LCX+ls*(LX0-pad-LCX)],[0,ls,LCY+ls*(LY0-pad-LCY)+lfy]])
    fa=cv2.warpAffine(canvas_a,Ml,(W,H),flags=cv2.INTER_LINEAR)
    fc=cv2.warpAffine(canvas_c,Ml,(W,H),flags=cv2.INTER_LINEAR)
    fg=cv2.warpAffine(canvas_g,Ml,(W,H),flags=cv2.INTER_LINEAR)
    small=cv2.resize(fa[LY0-120:LY1+120,LX0-160:LX1+160],None,fx=0.25,fy=0.25)
    halo=cv2.resize(cv2.GaussianBlur(small,(0,0),5),(LX1-LX0+320,LY1-LY0+240))
    k2=0.16+0.10*np.sin(2*w)
    out[LY0-120:LY1+120,LX0-160:LX1+160]+=halo[...,None]*k2*COL
    gl=cv2.GaussianBlur(fg[LY0-120:LY1+120,LX0-160:LX1+160],(0,0),14)
    out[LY0-120:LY1+120,LX0-160:LX1+160]+=gl[...,None]*0.55*COL
    out=out*(1-fa[...,None])+fc*fa[...,None]
    out=out+(fg*0.55)[...,None]*np.array([1,0.97,0.92],np.float32)
    return np.clip(out,0,1)
if mode=='preview':
    for t in [0,1.6,3.75,7.5,11.25]:
        f=(frame(t)*255).astype(np.uint8)
        cv2.imwrite(f'{S}/work/f_{t}.jpg',cv2.resize(f,(2016,672),interpolation=cv2.INTER_AREA))
        cv2.imwrite(f'{S}/work/crop_{t}.jpg',f[100:1000,1500:3800]); cv2.imwrite(f'{S}/work/logo_{t}.jpg',f[400:950,100:1350])
else:
    out=sys.argv[3]
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-profile:v','high','-level','5.1','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write((frame(i/FPS)*255+0.5).astype(np.uint8).tobytes())
        if i%50==0: print(i,flush=True)
    p.stdin.close(); p.wait(); print('done')
