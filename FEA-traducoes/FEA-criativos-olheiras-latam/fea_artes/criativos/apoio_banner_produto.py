"""_Banner do produto [Ebook] -> FEA-Banner do produto Ebook - LATAM.png.
A arte não tem copy fora do mockup do ebook (capa em português, x 1340 a 1740, y 40 a 640,
coordenadas aproximadas na resolução 1920 x 640). Pela regra 5, o mockup fica para a fase 2
(troca pela capa ES real); por ora a saída é o original, com nome LATAM, para o pacote ficar completo."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _fea_util_apoio import *

im = abrir(T + 'banner-produto.png')
print(salvar(im, 'FEA-Banner do produto Ebook - LATAM.png'), im.size)
