"""FEA: monta o áudio da URA só com a voz real do Dr. João (trechos de gravações originais).
Cada trecho: corte no ponto de menor energia perto da marca, banda e codec de telefone,
equalização casada com o áudio original da URA e volume igualado."""
import subprocess, sys, json, numpy as np, wave
SR=16000
def load(f, ss=None, to=None):
    cmd=['ffmpeg','-loglevel','error']+(['-ss',str(ss)] if ss is not None else [])+(['-to',str(to)] if to is not None else [])+['-i',f,'-ac','1','-ar',str(SR),'-f','s16le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.int16).astype(np.float32)/32768
def vale(a, t, raio=0.15):
    """ponto de menor energia (janela 20 ms) a até `raio` s de t"""
    h=int(0.01*SR); c=int(t*SR); best=c; bm=1e9
    for p in range(max(h,c-int(raio*SR)), min(len(a)-h,c+int(raio*SR)), h//2):
        e=np.mean(a[p-h:p+h]**2)
        if e<bm: bm, best = e, p
    return best
def tel(a):
    """passa pela mesma cadeia de telefone do original (8 kHz, MP3 24 kbps)"""
    p=subprocess.run(['ffmpeg','-loglevel','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af','highpass=f=200,lowpass=f=3600','-ar','8000','-b:a','24k','-f','mp3','-'],input=a.astype(np.float32).tobytes(),capture_output=True).stdout
    return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-f','mp3','-i','-','-ar',str(SR),'-ac','1','-f','s16le','-'],input=p,capture_output=True).stdout,np.int16).astype(np.float32)/32768
def espectro(a, n=512):
    fr=np.lib.stride_tricks.sliding_window_view(a,n)[::n//2]*np.hanning(n); S=np.abs(np.fft.rfft(fr,axis=1))
    en=(fr**2).mean(1); return S[en>np.percentile(en,50)].mean(0)
def casar(a, ref_esp, n=512):
    """equaliza `a` para ter o mesmo envelope espectral médio da referência"""
    g=ref_esp/(espectro(a,n)+1e-9); g=np.convolve(g,np.ones(9)/9,'same'); g=np.clip(g,0.25,4)
    h=np.fft.irfft(g); h=np.roll(h,n//2)*np.hanning(len(h))
    return np.convolve(a,h,'same')
def rms(a):
    fr=a[:len(a)//320*320].reshape(-1,320); e=np.sqrt((fr**2).mean(1)); return np.sqrt((e[e>0.02]**2).mean())
def fade(a,ms=12):
    n=int(SR*ms/1000); a=a.copy(); a[:n]*=np.linspace(0,1,n); a[-n:]*=np.linspace(1,0,n); return a

plano=json.load(open(sys.argv[1]))   # [{"arq","ini","fim","pausa_depois"}]
orig=plano[0]['arq']; ref=load(orig); ref_esp=espectro(ref); ref_rms=rms(ref)
partes=[]
for p in plano:
    a=load(p['arq']); i=int(p['ini']*SR) if p.get('exato_ini') else vale(a,p['ini']); f=vale(a,p['fim'])
    seg=a[i:f]
    if p['arq']!=orig:
        seg=tel(seg); seg=casar(seg,ref_esp); seg=tel(seg)
    seg=seg*ref_rms/rms(seg)
    partes += [fade(seg), np.zeros(int(SR*p.get('pausa_depois',0.15)),np.float32)]
out=np.concatenate(partes)
w=wave.open(sys.argv[2],'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes()); w.close()
print('duração', round(len(out)/SR,2),'s')
