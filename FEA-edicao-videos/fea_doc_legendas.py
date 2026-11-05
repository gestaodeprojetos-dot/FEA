#!/usr/bin/env python3
"""Cria o Google Doc de revisão de legendas na subpasta de entrega (Drive).

Para cada vídeo do projeto: título, duração final, primeiras palavras e todas as legendas com o
tempo em que entram no vídeo (lidas do .ass gerado no render), mais os pontos para a Keila decidir.
A Keila (ou quem revisa) comenta direto no Doc; as correções voltam para o projeto.json.

Uso:
    python3 fea_doc_legendas.py projeto.json PASTA_DRIVE_ID "Nome do Doc" [--notas notas.json]

notas.json (opcional): {"N- Título": ["ponto para decidir", ...], ...}
Credenciais só pelas variáveis do ambiente (fea_drive.py).
"""
import html, json, os, re, subprocess, sys, uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fea_drive as fd  # noqa: E402


def ler_legendas(ass):
    titulo, leg = [], []
    for linha in open(ass, encoding="utf-8"):
        if not linha.startswith("Dialogue:"):
            continue
        p = linha.split(",", 9)
        txt = re.sub(r"\{[^}]*\}", "", p[9].strip()).replace("\\N", " ")
        (titulo if p[3] == "Titulo" else leg).append((p[1], txt))
    # o .ass tem 2 eventos por bloco de 2 linhas (uma por linha): junta pelo tempo de entrada
    blocos = []
    for t, txt in leg:
        if blocos and blocos[-1][0] == t:
            blocos[-1][1] += " / " + txt
        else:
            blocos.append([t, txt])
    return blocos


def duracao(ff, arq):
    r = subprocess.run([ff, "-i", arq], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def montar_html(cfg, nome_doc, notas):
    ff = cfg.get("ffmpeg", "ffmpeg")
    h = [f"<h1>{html.escape(nome_doc)}</h1>",
         "<p>Revisão das legendas: cada linha mostra o tempo em que a legenda entra no vídeo final. "
         "Comente direto na linha que precisa mudar. Grafia técnica conferida pela revisora automática "
         "(fea_revisar.py); regra de escrita FEA: sempre \"para\", nunca \"pra\".</p>"]
    for v in cfg["videos"]:
        nome = os.path.basename(v["saida"]).rsplit(".", 1)[0]
        ass = v["saida"].rsplit(".", 1)[0] + ".ass"
        blocos = ler_legendas(ass)
        d = duracao(ff, v["saida"]) if os.path.exists(v["saida"]) else 0
        h.append(f"<h2>{html.escape(nome)}</h2>")
        h.append(f"<p><b>Duração com CTA:</b> {int(d // 60)}:{d % 60:04.1f} &nbsp; "
                 f"<b>Bruto:</b> {html.escape(os.path.basename(v['entrada']))} &nbsp; "
                 f"<b>Título:</b> {html.escape(v['titulo'])} "
                 f"({'da imagem de títulos' if v.get('titulo_origem') == 'imagem' else 'criado pela transcrição, conferir'})</p>")
        for n in notas.get(nome, []):
            h.append(f"<p>&#9888; {html.escape(n)}</p>")
        h.append("<table border='1' cellpadding='4'><tr><th>Entra em</th><th>Legenda</th></tr>")
        for t, txt in blocos:
            h.append(f"<tr><td>{t[2:7]}</td><td>{html.escape(txt)}</td></tr>")
        h.append("</table>")
    return "<html><head><meta charset='utf-8'></head><body>" + "\n".join(h) + "</body></html>"


def criar_doc(tk, pasta, nome, conteudo_html):
    """Upload multipart convertendo HTML em Google Doc."""
    limite = uuid.uuid4().hex
    meta = json.dumps({"name": nome, "parents": [pasta], "mimeType": "application/vnd.google-apps.document"})
    corpo = (f"--{limite}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n"
             f"--{limite}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n").encode() + \
        conteudo_html.encode("utf-8") + f"\r\n--{limite}--\r\n".encode()
    r = fd.chamar(tk, "POST", fd.UPLOAD + "?uploadType=multipart&supportsAllDrives=true&fields=id",
                  cabecalhos={"Content-Type": f"multipart/related; boundary={limite}"}, bruto=corpo)
    return json.load(r)["id"]


def main(argv):
    notas = {}
    if "--notas" in argv:
        i = argv.index("--notas")
        notas = json.load(open(argv[i + 1], encoding="utf-8"))
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 3:
        sys.exit(__doc__)
    projeto, pasta, nome = argv
    cfg = json.load(open(projeto, encoding="utf-8"))
    tk, _ = fd.token()
    for velho in fd.listar(tk, pasta, nome):   # refaz o Doc com o mesmo nome (o antigo vai para a lixeira)
        fd.chamar(tk, "PATCH", f"{fd.API}/{velho['id']}?supportsAllDrives=true", corpo={"trashed": True})
    did = criar_doc(tk, pasta, nome, montar_html(cfg, nome, notas))
    print(f"OK: https://docs.google.com/document/d/{did}/edit")


if __name__ == "__main__":
    main(sys.argv[1:])
