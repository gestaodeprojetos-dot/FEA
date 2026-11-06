import sys, subprocess, numpy as np
def load(f):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
bands=[(80,300),(300,1000),(1000,2000),(2000,3400),(3400,5000),(5000,8000)]
for f in sys.argv[1:]:
    a=load(f); S=np.abs(np.fft.rfft(a))**2; fr=np.fft.rfftfreq(len(a),1/16000)
    tot=S[(fr>80)].sum(); cen=(fr*S).sum()/S.sum()
    print(f"{f[-45:]:>45} centroide={cen:5.0f}Hz "+" ".join(f"{lo}-{hi}:{10*np.log10(S[(fr>=lo)&(fr<hi)].sum()/tot):5.1f}dB" for lo,hi in bands))
