"""FEA: anima so os textos de um slide 4032x1344 (pessoa e fundo parados).
Uso: python3 fea_motion_texto.py <pasta com up.png e text_alpha.png> preview|render [saida.mp4]"""
import sys, numpy as np, cv2, subprocess
S=sys.argv[1]; mode=sys.argv[2]
FPS=30; T=15.0; N=int(FPS*T)
img=cv2.imread(f'{S}/up.png').astype(np.float32)/255
H,W=img.shape[:2]
ta=cv2.imread(f'{S}/text_alpha.png',0).astype(np.float32)/255
# clean plate behind the text (only where text sits)
hole=cv2.dilate((ta>0.02).astype(np.uint8),np.ones((13,13),np.uint8))*255
sm=cv2.resize((img*255).astype(np.uint8),(W//2,H//2),interpolation=cv2.INTER_AREA)
inp=cv2.inpaint(sm,cv2.resize(hole,(W//2,H//2),interpolation=cv2.INTER_NEAREST),12,cv2.INPAINT_TELEA)
inp=cv2.resize(cv2.GaussianBlur(inp,(0,0),2),(W,H),interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
hf=cv2.GaussianBlur(hole,(0,0),3).astype(np.float32)[...,None]/255
BASE=img*(1-hf)+inp*hf
# elements = text lines (connected components grouped by vertical band)
BANDS=[('cred',190,280),('h1',280,440),('h2',440,600),('h3',600,700),('div',790,840),('b1',920,1003),('b2',1003,1070),('b3',1070,1160)]
n,lab,st,cen=cv2.connectedComponentsWithStats((ta>0.05).astype(np.uint8),8)
EL=[]
for k,(name,y0b,y1b) in enumerate(BANDS):
    ids=[i for i in range(1,n) if y0b<=cen[i][1]<y1b]
    if not ids: continue
    m=cv2.dilate(np.isin(lab,ids).astype(np.uint8),np.ones((5,5),np.uint8)).astype(bool)
    ys,xs=np.where(m); P=40
    y0,y1,x0,x1=max(ys.min()-P,0),min(ys.max()+1+P,H),max(xs.min()-P,0),min(xs.max()+1+P,W)
    EL.append(dict(name=name,k=k,y0=y0,x0=x0,a=(ta*m)[y0:y1,x0:x1].copy(),c=img[y0:y1,x0:x1].copy(),
                   cy=(ys.min()+ys.max())/2))
START={'cred':0.40,'h1':0.75,'h2':1.10,'h3':1.50,'div':1.90,'b1':2.40,'b2':2.60,'b3':2.80}
COL=np.array([1.0,0.90,0.72],np.float32)
LIM=np.clip((2150-np.arange(W,dtype=np.float32))/300,0,1)[None,:,None]
Xf=np.arange(W,dtype=np.float32)[None,:]; Yf=np.arange(H,dtype=np.float32)[:,None]
def clamp(x): return min(max(x,0.0),1.0)
def eout(x): return 1-(1-x)**3
def ein(x): return x**2
def bump(x,c,wd): return float(np.exp(-((x-c)/wd)**2))
rng=np.random.default_rng(11)
PX=rng.uniform(150,1950,60); PY=rng.uniform(150,1300,60); PR=rng.uniform(1.5,4,60); PV=rng.uniform(30,90,60)
PPH=rng.uniform(0,T,60); PA=rng.uniform(0.15,0.4,60)
def particles(buf,t):
    for i in range(60):
        u=((t+PPH[i])%T)/T; al=PA[i]*np.sin(np.pi*u)**1.5
        x=int(PX[i]); y=int(PY[i]-PV[i]*u*T*0.3); r=PR[i]; s=int(r*4)+2
        if al<0.01 or y-s<0 or y+s+1>H: continue
        yy,xx=np.mgrid[-s:s+1,-s:s+1]; g=np.exp(-(xx**2+yy**2)/(2*(r*0.9)**2)).astype(np.float32)
        buf[y-s:y+s+1,x-s:x+s+1]+=g[...,None]*al*COL
def frame(t):
    out=BASE.copy()
    pb=np.zeros_like(out); particles(pb,t); out+=pb*LIM
    glow=np.zeros((H,W),np.float32); hl=np.zeros((H,W),np.float32)
    for E in EL:
        name=E['name']; t0=START[name]; k=E['k']
        a=E['a']; c=E['c']; h,w=a.shape
        if name=='div':  # divider draws left->right, erases right->left
            pin=eout(clamp((t-t0)/0.6)); pout=ein(clamp((t-12.25)/0.5))
            cols=np.arange(w,dtype=np.float32)
            wipe=np.clip((pin*w-cols)/25,0,1)*np.clip(((1-pout)*w-cols)/25,0,1)
            aa=a*wipe[None,:]; reg=(slice(E['y0'],E['y0']+h),slice(E['x0'],E['x0']+w))
            out[reg]=out[reg]*(1-aa[...,None])+c*aa[...,None]
            continue
        pin=eout(clamp((t-t0)/0.8)); pout=ein(clamp((t-12.2-0.08*k)/0.7))
        vis=pin*(1-pout)
        if vis<0.003: continue
        oy=55*(1-pin)-40*pout; blur=10*(1-pin)+8*pout
        if blur>0.6: a=cv2.GaussianBlur(a,(0,0),blur); c=cv2.GaussianBlur(c,(0,0),blur)
        M=np.float32([[1,0,0],[0,1,oy]])
        a2=cv2.warpAffine(a,M,(w,h),flags=cv2.INTER_CUBIC)*vis
        c2=cv2.warpAffine(c,M,(w,h),flags=cv2.INTER_CUBIC)
        reg=(slice(E['y0'],E['y0']+h),slice(E['x0'],E['x0']+w))
        out[reg]=out[reg]*(1-a2[...,None])+np.clip(c2,0,1)*a2[...,None]
        lit=0.0
        if name in('h1','h2','h3'): lit=bump(t,t0+0.85,0.25)*0.9
        if name=='h2': lit+=bump(t,2.2,0.3)*0.6
        if lit>0.01: glow[reg]+=a2*lit
        if name in('h1','h2'): hl[reg]=np.maximum(hl[reg],a2)
    out+=cv2.GaussianBlur(glow,(0,0),16)[...,None]*0.7*COL+glow[...,None]*0.5
    # specular sweep across the headline during the hold
    st_=(t-7.2)/1.6
    if 0<=st_<=1:
        sp=600+1700*st_; band=np.exp(-(((Xf+0.35*(Yf-430))-sp)/80)**2)*0.6
        out+=(band*hl)[...,None]*np.array([1,0.97,0.92],np.float32)
    # light streak as the headline lands
    e=bump(t,1.6,0.5)
    if e>0.01:
        sx=500+1700*clamp((t-0.8)/1.6)
        streak=np.exp(-((Yf-505)/6)**2)*np.exp(-((Xf-sx)/800)**2)*0.9+np.exp(-((Yf-505)/55)**2)*np.exp(-((Xf-sx)/240)**2)*0.3
        out+=(streak*e)[...,None]*COL*LIM
    return np.clip(out,0,1)
if mode=='preview':
    for t in [0.2,1.0,1.6,2.3,3.5,7.8,12.6]:
        f=(frame(t)*255+0.5).astype(np.uint8)
        cv2.imwrite(f'{S}/p_{t}.jpg',cv2.resize(f,(1344,448),interpolation=cv2.INTER_AREA))
else:
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-profile:v','high','-level','5.1','-movflags','+faststart',sys.argv[3]],stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write((frame(i/FPS)*255+0.5).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print('done')
