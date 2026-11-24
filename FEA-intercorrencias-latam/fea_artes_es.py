"""Gera CAPA ARTI_02 ES e completa o banner ES (texto chapado). Uso: python3 -I fea_artes_es.py DIR_IMG DIR_SCRIPTS VF.ttf"""
import sys

import cv2
import numpy as np

D, SC, VF = sys.argv[1:4]
sys.path.insert(0, SC)
import fea_flat_text as ft  # noqa: E402

ft.VF = VF
log = []

# ---------- Banner: mockup já trocado (banner_step1.png); agora o bloco de texto da direita ----------
b = cv2.imread(f"{D}/banner_step1.png")
log.append("BANNER")
ft.replace_line(b, (1290, 210, 1845, 293), "orange", "INTERCORRÊNCIAS", "INTERCURRENCIAS", log=log)
ft.replace_line(b, (1290, 293, 1845, 330), "white", "NO PREENCHIMENTO COM ÁCIDO HIALURÔNICO",
                "EN EL RELLENO CON ÁCIDO HIALURÓNICO", weights=(600,), match_width=True, log=log)
ft.replace_line(b, (1314, 346, 1825, 378), "white", "DIAGNÓSTICO E CONDUTAS CLÍNICAS PARA COMPLICAÇÕES ESTÉTICAS",
                "DIAGNÓSTICO Y CONDUCTAS CLÍNICAS ANTE COMPLICACIONES ESTÉTICAS", xscale_mode=True, max_w=491, log=log)
cv2.imwrite(f"{D}/Banner 1920x640 ES.png", b)

# ---------- CAPA ARTI_02 (capa frontal reta) ----------
a = cv2.imread(f"{D}/arti2.png", cv2.IMREAD_UNCHANGED)
rgb = np.ascontiguousarray(a[:, :, :3])
log.append("CAPA ARTI_02")
ft.replace_line(rgb, (225, 84, 850, 172), "orange", "INTERCORRÊNCIAS", "INTERCURRENCIAS", log=log)
ft.replace_line(rgb, (225, 172, 850, 225), "white", "NO PREENCHIMENTO FACIAL", "EN EL RELLENO FACIAL", weights=(500, 600), match_width=True, log=log)
ft.replace_line(rgb, (249, 869, 831, 905), "white", "COMPLICAÇÕES NO PREENCHIMENTO COM ÁCIDO HIALURÔNICO",
                "COMPLICACIONES EN EL RELLENO CON ÁCIDO HIALURÓNICO", xscale_mode=True, max_w=555, log=log)
out = np.dstack([rgb, a[:, :, 3]]) if a.shape[2] == 4 else rgb
cv2.imwrite(f"{D}/CAPA ARTI_02 ES.png", out)
print("\n".join(log))
