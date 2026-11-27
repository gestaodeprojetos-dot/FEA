#!/usr/bin/env python3
"""Transcreve o começo de vídeos/áudios (identificar de que artigo um vídeo fala, achar take, conferir fala).
Uso: python3 fea_transcrever_trecho.py arquivo1.mp4 [arquivo2.mov ...] [--seg 150] [--modelo small]
Usa numpy como entrada: o faster-whisper desta máquina quebra ao abrir arquivo direto (erro metadata_errors do av).
"""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
a = sys.argv[1:]; seg = '150'; mod = 'small'
if '--seg' in a: i = a.index('--seg'); seg = a[i + 1]; del a[i:i + 2]
if '--modelo' in a: i = a.index('--modelo'); mod = a[i + 1]; del a[i:i + 2]
m = WhisperModel(mod, compute_type='int8')
for f in a:
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-t', seg, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True).stdout
    segs, _ = m.transcribe(np.frombuffer(raw, np.int16).astype(np.float32) / 32768, language='pt')
    print('##', f, '\n', ' '.join(s.text.strip() for s in segs))
