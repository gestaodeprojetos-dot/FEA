import sys, subprocess, numpy as np
from resemblyzer import VoiceEncoder
def load(f, tel=True):
    af = "highpass=f=250,lowpass=f=3500,aresample=8000,aresample=16000" if tel else "aresample=16000"
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-af',af,'-f','s16le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
enc=VoiceEncoder('cpu', verbose=False)
ref=enc.embed_utterance(load(sys.argv[1]))
for f in sys.argv[2:]:
    e=enc.embed_utterance(load(f)); print(f"{f:28s} similaridade com a voz original: {float(np.dot(ref,e)):.3f}")
