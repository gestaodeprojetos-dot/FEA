# REFERÊNCIA (URA da reabertura da Black, 24/11/2026): montagem de áudio da URA a partir de falas gravadas do Dr. João.
# Ajustar SRC (arquivos wav 44.1k mono), REFSPEECH (trechos de referência de timbre) e P (peças: fonte, início, fim, pausa, limites).
# Técnica: corte por energia (refine), equalização FIR para o timbre da referência, nivelamento pelo RMS da fala ativa,
# pausa com ruído de sala, compressor leve e loudnorm linear no final. Limite: 30 s. Ouvir e transcrever o resultado antes de entregar.
import numpy as np,wave,subprocess
from scipy.signal import welch,firwin2,fftconvolve
sr=44100
def rd(f):
  w=wave.open(f);return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)/32768
def wr(f,x):
  w=wave.open(f,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes());w.close()
SRC={'019':rd('src_019h.wav'),'aov':rd('src_aovivo.wav'),'eh':rd('src_ehoje.wav'),'l1':rd('src_lote1.wav')}
FR=int(0.01*sr)
def env(x): n=len(x)//FR; return 20*np.log10(np.sqrt((x[:n*FR].reshape(n,FR)**2).mean(1))+1e-9)
E={k:env(v) for k,v in SRC.items()}
FLOOR={k:np.percentile(e,8) for k,e in E.items()}
PEAK={k:np.percentile(e,95) for k,e in E.items()}
def refine(k,a,b,stop_a=None,stop_b=None):
  e=E[k]; fl=FLOOR[k]; lim=fl+0.35*(PEAK[k]-fl)  # quiet threshold
  i=int(a*100); j=int(b*100)
  # start: move back while energy above lim (still inside word), max 0.15s, not before stop_a
  lo=int((stop_a if stop_a else a-0.25)*100)
  while i>lo and e[i-1]>lim: i-=1
  # end: move forward while energy above lim, max 0.25s, not beyond stop_b
  hi=int((stop_b if stop_b else b+0.3)*100)
  while j<hi and e[j]>lim: j+=1
  # add small tail of decay (up to 40ms) staying below lim
  j=min(j+4,hi); i=max(i-2,lo)
  return i/100,j/100
REFSPEECH=[(36.79,41.76),(70.92,73.64),(79.22,84.84)]
f,pref=welch(np.concatenate([SRC['019'][int(a*sr):int(b*sr)] for a,b in REFSPEECH]),sr,nperseg=8192)
def sm(p):
  o=np.zeros_like(p)
  for i,fr in enumerate(f):
    if fr<20: o[i]=p[i];continue
    m=(f>=fr/2**(1/6))&(f<=fr*2**(1/6)); o[i]=p[m].mean()
  return o
FIR={}
for k,x in SRC.items():
  if k=='019': g=np.zeros_like(f)
  else:
    seg=x[int(len(x)*0.05):int(len(x)*0.95)]; _,p=welch(seg,sr,nperseg=8192); g=10*np.log10((sm(pref)+1e-20)/(sm(p)+1e-20))
  g-=np.median(g[(f>300)&(f<3000)]); g=np.clip(g,-9,9); g[f<70]=-20; g[f>11000]=-30
  FIR[k]=firwin2(2047,f/(sr/2),10**(g/20))
def piece(k,a,b,sa=None,sb=None):
  a,b=refine(k,a,b,sa,sb)
  pad=4000; s=int(a*sr); t=int(b*sr)
  x=SRC[k][max(0,s-pad):t+pad]; y=fftconvolve(x,FIR[k],'same')[s-max(0,s-pad):][:t-s]
  # speech level: RMS of active frames
  ee=env(y); act=ee>np.percentile(ee,60)-6
  rms=np.sqrt(np.mean(y[:len(ee)*FR].reshape(-1,FR)[act]**2))
  y=y*(10**(-20/20)/rms)
  fi=int(0.008*sr); fo=int(0.03*sr)
  y[:fi]*=np.linspace(0,1,fi); y[-fo:]*=np.linspace(1,0,fo)
  return y,(a,b)
def build(name,pieces):
  out=[];rng=np.random.default_rng(1)
  for n,(k,a,b,gap,sa,sb) in enumerate(pieces):
    y,ab=piece(k,a,b,sa,sb); print(k,(a,b),'->',ab)
    out.append(y)
    if n<len(pieces)-1: out.append(rng.normal(0,0.0004,int(gap*sr)))
  y=np.concatenate(out); wr('tmp_all.wav',y/ (abs(y).max()+1e-9)*0.7)
  subprocess.run(['ffmpeg','-loglevel','error','-y','-i','tmp_all.wav','-af','highpass=f=80,lowpass=f=11000,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=150:makeup=1,loudnorm=I=-14:TP=-1.0:LRA=5:linear=true','-ar','44100','-ac','1','-b:a','128k',name],check=True)
P=[('l1',0.44,2.92,0.03,0.30,2.94),('aov',0.05,1.20,0.10,0.0,1.23),('019',0.02,2.99,0.12,0.0,3.02),
   ('019',70.94,73.62,0.03,70.90,73.66),('eh',36.12,36.92,0.12,36.10,37.06),('aov',9.90,14.55,0.12,9.84,14.58),('aov',26.06,26.70,0,25.95,26.95)]
build('FEA-URA-reabertura-aovivo-v2.mp3',P)
