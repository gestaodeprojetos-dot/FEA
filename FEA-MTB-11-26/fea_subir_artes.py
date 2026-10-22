"""Substitui o conteúdo das artes copiadas no Drive pelas versões com a data nova (mesmo id e link)."""
import io, json, sys, unicodedata
from PIL import Image
sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_drive import token, chamar, UPLOAD

pasta = sys.argv[1]  # pasta de trabalho com auditoria/ocr_datas.json e editadas/
dados = json.load(open(f"{pasta}/auditoria/ocr_datas.json"))
mapa = {v["id"]: v for v in json.load(open("/home/user/FEA/FEA-MTB-11-26/FEA-mapa-drive-mtb-1126.json")).values()}
tk, _ = token()
for fid, v in dados.items():
    nome = unicodedata.normalize("NFC", v["caminho"].split("/")[-1])
    mime = mapa[fid]["mime"]
    im = Image.open(f"{pasta}/editadas/{nome.rsplit('.', 1)[0]}.png").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=95) if mime == "image/jpeg" else im.save(buf, "PNG", optimize=True)
    chamar(tk, "PATCH", f"{UPLOAD}/{fid}?uploadType=media&supportsAllDrives=true", bruto=buf.getvalue(),
           cabecalhos={"Content-Type": mime})
    print("ok", nome)
