"""Gera os estáticos novos do MTB 11/26 (copies de FEA-copies-novas-mtb-1126.md) sobre artes aprovadas
da campanha e, com --subir, envia para as pastas de criativos prontos no Drive.

Uso: python3 fea_lote_criativos_novos.py PASTA_TRABALHO [--subir]
PASTA_TRABALHO precisa ter editadas/ (artes com a data nova)."""
import json, os, sys, uuid
sys.path.insert(0, "/home/user/FEA/FEA-MTB-11-26"); sys.path.insert(0, "/home/user/FEA/FEA-edicao-videos")
from fea_criativo_novo import criar

CAPTACAO = "1HA7W8B2uasswkqgWI1AXiQZFrr96pZdV"   # 01. CAPTAÇÃO/ESTÁTICOS
LEMBRETE = "1NWyLybtsqN6DwcoJC93tOZWsQqY6LFLl"   # 02. LEMBRETE
DATA = ("Segunda, 09/11 • 20h", "online, AO VIVO e sem replay")
# (nome, pasta, modelo story, título, apoio, data)
PECAS = [
    ("Ads 46", CAPTACAO, "Ads 36", "Quanto do seu resultado com toxina ainda depende de [sorte]?",
     "Veja o raciocínio clínico por trás de dose, ponto e profundidade.", DATA),
    ("Ads 47", CAPTACAO, "Ads 39", "Toxina botulínica começa na [anatomia], não na agulha.",
     "Terço superior, sorriso gengival, bruxismo, enxaqueca e hiperidrose.", DATA),
    ("Ads 48", CAPTACAO, "Ads 36", "O paciente voltou [antes do esperado]?",
     "Diluição, dose e escolha do ponto pesam tanto quanto o produto.", DATA),
    ("Ads 49", CAPTACAO, "Ads 39", "Qual toxina usar em [cada paciente]?",
     "As principais toxinas do Brasil comparadas lado a lado, com critério de escolha.", DATA),
    ("Ads 50", CAPTACAO, "Ads 36", "Uma noite sobre toxina [estética e funcional].",
     "9 técnicas avançadas com o raciocínio anatômico da dissecção em cadáver fresco.", DATA),
    ("Ads 51", CAPTACAO, "Ads 39", "Bruxismo e sorriso gengival pedem [mais do que protocolo].",
     "Avaliação muscular antes de definir ponto e unidade, com foco em segurança.", DATA),
    ("Ads 015 - É nesta segunda", LEMBRETE, "Ads 36", "É nesta [segunda-feira].",
     "Masterclass em Toxina Botulínica. Separe a noite: não haverá replay.", DATA),
    ("Ads 016 - Hoje", LEMBRETE, "Ads 39", "[Hoje], às 20h.",
     "Confira o link de acesso no grupo do WhatsApp e no seu e-mail.", ("Hoje, 09/11 • 20h", DATA[1])),
    ("Ads 017 - Começa em poucas horas", LEMBRETE, "Ads 36", "Começa em [poucas horas].",
     "Às 20h eu entro ao vivo. Ainda dá tempo de se inscrever.", ("Hoje, 09/11 • 20h", DATA[1])),
]


def nome_arquivo(nome, formato):
    base, _, resto = nome.partition(" - ")
    return f"{base} {formato}{' - ' + resto if resto else ''} - MTB.png"


def subir_png(tk, pasta, caminho):
    from fea_drive import chamar, UPLOAD
    b = uuid.uuid4().hex
    meta = json.dumps({"name": os.path.basename(caminho), "parents": [pasta]})
    corpo = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n--{b}\r\nContent-Type: image/png\r\n\r\n").encode() \
        + open(caminho, "rb").read() + f"\r\n--{b}--".encode()
    return json.load(chamar(tk, "POST", UPLOAD + "?uploadType=multipart&supportsAllDrives=true&fields=id,webViewLink",
                            bruto=corpo, cabecalhos={"Content-Type": f"multipart/related; boundary={b}"}))


if __name__ == "__main__":
    trab = sys.argv[1]; os.makedirs(f"{trab}/novos", exist_ok=True)
    feitos = []
    for nome, pasta, story, titulo, apoio, data in PECAS:
        for formato, modelo in (("Story", story), ("Feed", "Ads 37")):
            saida = f"{trab}/novos/{nome_arquivo(nome, formato)}"
            criar(f"{trab}/editadas/{modelo} {formato} - MTB.png", titulo, apoio, *data, saida)
            feitos.append((pasta, saida)); print("gerado", os.path.basename(saida))
    if "--subir" in sys.argv:
        from fea_drive import token
        tk, _ = token()
        links = {os.path.basename(s): subir_png(tk, p, s)["webViewLink"] for p, s in feitos}
        json.dump(links, open(f"{trab}/novos/links.json", "w"), ensure_ascii=False, indent=1)
        print(len(links), "enviados")
