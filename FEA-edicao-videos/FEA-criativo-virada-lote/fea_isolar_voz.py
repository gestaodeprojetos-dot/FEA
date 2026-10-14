"""FEA: isola a voz do doutor (tira vento e ruído) com DeepFilterNet. Uso: python3 fea_isolar_voz.py ENT.wav SAI.wav [...]
WAV mono 48 kHz. Instalar: torch e torchaudio (CPU), deepfilternet, soundfile; o modelo DeepFilterNet3.zip vem de
raw.githubusercontent.com/Rikorose/DeepFilterNet/main/models/ para ~/.cache/DeepFilterNet (o link do github.com dá 403).
O deepfilternet rebaixa o numpy para 1.x e quebra o scipy: depois de instalar, pip install "numpy>=2.1,<2.4"."""
import sys, numpy as np, soundfile as sf, torch
from df.enhance import enhance, init_df
model, st, _ = init_df()
for ent, sai in zip(sys.argv[1::2], sys.argv[2::2]):
    a, sr = sf.read(ent, dtype='float32'); assert sr == st.sr(), sr
    if a.ndim > 1: a = a.mean(1)
    y = enhance(model, st, torch.from_numpy(a)[None])[0].numpy()
    sf.write(sai, y, sr); print('ok', sai)
