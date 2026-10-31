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
logo_glow=cv2.GaussianBlur(la,(0,0),18)
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
    M=aff(1.03+0.012*np.sin(w),11*np.sin(w),4*np.cos(w),W/2,H/2)
    bg=cv2.warpAffine(bgsrc,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    # light sweep across background, once per loop (off-screen at loop seam)
    pos=-0.35*W+1.7*W*(t/T)
    d=(X+0.45*Y-pos)
    band=np.exp(-(d/260)**2)*0.16+np.exp(-(d/60)**2)*0.05
    bg=1-(1-bg)*(1-band[...,None]*COL)
    particles(bg,PB,t)
    # people: counter-parallax, anchored bottom-center
    Mp=aff(1.008-0.006*np.sin(w),-5*np.sin(w),0,2700,H)
    pw=cv2.warpAffine(people,Mp,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    aw=cv2.warpAffine(pa,Mp,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)[...,None]
    out=bg*(1-aw)+pw*aw
    particles(out,PF,t)
    # logo: steady, soft glow + specular shimmer pass
    lg=(0.10+0.06*np.sin(2*w))*logo_glow[...,None]*COL
    out=out+lg
    out=out*(1-la[...,None])+logo*la[...,None]
    sh_t=(t-2.0)/2.2
    if 0<=sh_t<=1:
        sp=230+(1200-230+500)*sh_t-250
        sd=(X+0.35*(Y-660)-sp)
        shine=np.exp(-(sd/70)**2)*0.75
        out=out+(shine*la)[...,None]*np.array([1,0.97,0.9],np.float32)
    return np.clip(out,0,1)
if mode=='preview':
    for t in [0,3.0,7.5,11]:
        f=(frame(t)*255).astype(np.uint8)
        cv2.imwrite(f'{S}/work/f_{t}.jpg',cv2.resize(f,(2016,672),interpolation=cv2.INTER_AREA))
        cv2.imwrite(f'{S}/work/crop_{t}.jpg',f[150:900,1500:3300])
else:
    out=sys.argv[3]
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-profile:v','high','-level','5.1','-movflags','+faststart',out],stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write((frame(i/FPS)*255+0.5).astype(np.uint8).tobytes())
        if i%50==0: print(i,flush=True)
    p.stdin.close(); p.wait(); print('done')
