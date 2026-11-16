#!/usr/bin/env python3
"""Cliente uazapi (WhatsApp) do projeto FEA.

Biblioteca + linha de comando, sem dependências externas (só biblioteca padrão).
Contrato de referência: uazapi API 2.6.9 (https://docs.uazapi.com/openapi-bundled.json).

Credenciais lidas de variáveis de ambiente ou do arquivo .env ao lado deste script:
    FEA_UAZAPI_URL     Server URL da instância (ex.: https://SEU-SUBDOMINIO.uazapi.com)
    FEA_UAZAPI_TOKEN   token da instância (header `token`)
    FEA_UAZAPI_ADMIN   admintoken (opcional, só para comandos administrativos)

Segurança operacional: todo comando que envia mensagem ou altera configuração roda em
modo simulação por padrão e só executa de verdade com a flag --enviar.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TIPOS_MIDIA = ["image", "video", "videoplay", "document", "audio", "myaudio", "ptt", "ptv", "sticker"]
EVENTOS_WEBHOOK = ["connection", "history", "messages", "messages_update", "newsletter_messages",
                   "status_posts", "call", "contacts", "presence", "groups", "labels", "chats",
                   "chat_labels", "sender"]


# ---------------------------------------------------------------- configuração
def carregar_env(caminho: Path = AQUI / ".env") -> None:
    """Carrega KEY=VALUE do .env sem sobrescrever variáveis já definidas."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, v = linha.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class ErroUazapi(RuntimeError):
    def __init__(self, status: int, corpo: str, rota: str):
        self.status, self.corpo, self.rota = status, corpo, rota
        dica = {
            401: "token inválido ou de outro servidor (confira FEA_UAZAPI_URL + FEA_UAZAPI_TOKEN)",
            404: "rota ou recurso inexistente",
            429: "limite de requisições, aguarde e tente de novo",
        }.get(status, "")
        super().__init__(f"HTTP {status} em {rota}: {corpo[:300]} {('-> ' + dica) if dica else ''}")


# ---------------------------------------------------------------- cliente
class Uazapi:
    def __init__(self, url: str | None = None, token: str | None = None,
                 admintoken: str | None = None, timeout: int = 60, tentativas: int = 3):
        carregar_env()
        self.url = (url or os.environ.get("FEA_UAZAPI_URL", "")).rstrip("/")
        self.token = token or os.environ.get("FEA_UAZAPI_TOKEN", "")
        self.admintoken = admintoken or os.environ.get("FEA_UAZAPI_ADMIN", "")
        self.timeout, self.tentativas = timeout, tentativas
        if not self.url:
            raise SystemExit("Falta FEA_UAZAPI_URL (Server URL da instância) no .env")

    def _req(self, metodo: str, rota: str, corpo: dict | None = None, admin: bool = False):
        cabecalhos = {"Accept": "application/json"}
        if admin:
            if not self.admintoken:
                raise SystemExit("Falta FEA_UAZAPI_ADMIN no .env para este comando")
            cabecalhos["admintoken"] = self.admintoken
        else:
            if not self.token:
                raise SystemExit("Falta FEA_UAZAPI_TOKEN no .env")
            cabecalhos["token"] = self.token
        dados = None
        if corpo is not None:
            dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
            cabecalhos["Content-Type"] = "application/json"

        for tentativa in range(1, self.tentativas + 1):
            req = urllib.request.Request(self.url + rota, data=dados, method=metodo, headers=cabecalhos)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    txt = r.read().decode("utf-8", "replace")
                    return json.loads(txt) if txt.strip() else {}
            except urllib.error.HTTPError as e:
                txt = e.read().decode("utf-8", "replace")
                # Retry só em limite temporário/indisponibilidade, respeitando Retry-After
                if e.code in (429, 503) and tentativa < self.tentativas:
                    espera = float(e.headers.get("Retry-After") or 2 * tentativa)
                    time.sleep(min(espera, 60))
                    continue
                raise ErroUazapi(e.code, txt, rota) from None
            except urllib.error.URLError as e:
                if tentativa < self.tentativas and metodo == "GET":
                    time.sleep(2 * tentativa)
                    continue
                raise SystemExit(f"Falha de rede em {rota}: {e.reason}") from None

    # ---- instância
    def status(self):
        return self._req("GET", "/instance/status")

    def limites(self):
        return self._req("GET", "/instance/wa_messages_limits")

    def conectar(self, telefone: str | None = None):
        """Sem telefone: gera QR code. Com telefone: gera código de pareamento."""
        return self._req("POST", "/instance/connect", {"phone": telefone} if telefone else {})

    def listar_instancias(self):
        return self._req("GET", "/instance/all", admin=True)

    # ---- envio
    def enviar_texto(self, numero: str, texto: str, **extras):
        return self._req("POST", "/send/text", {"number": numero, "text": texto, **extras})

    def enviar_midia(self, numero: str, tipo: str, arquivo: str, legenda: str = "", **extras):
        """`arquivo` pode ser URL pública ou caminho local (convertido para base64)."""
        if tipo not in TIPOS_MIDIA:
            raise ValueError(f"tipo inválido: {tipo} (use {', '.join(TIPOS_MIDIA)})")
        corpo = {"number": numero, "type": tipo, "file": arquivo_para_payload(arquivo), **extras}
        if legenda:
            corpo["text"] = legenda
        if tipo == "document" and "docName" not in corpo and not arquivo.startswith("http"):
            corpo["docName"] = Path(arquivo).name
        return self._req("POST", "/send/media", corpo)

    # ---- contatos e grupos
    def verificar_numeros(self, numeros: list[str]):
        return self._req("POST", "/chat/check", {"numbers": numeros})

    def listar_grupos(self, busca: str = "", limite: int = 200, offset: int = 0):
        corpo = {"limit": limite, "offset": offset, "noParticipants": True}
        if busca:
            corpo["search"] = busca
        return self._req("POST", "/group/list", corpo)

    def info_grupo(self, jid: str):
        return self._req("POST", "/group/info", {"groupjid": jid})

    # ---- webhook
    def ver_webhook(self):
        return self._req("GET", "/webhook")

    def configurar_webhook(self, url: str, eventos: list[str], ignorar_api: bool = True):
        corpo = {"enabled": True, "url": url, "events": eventos}
        if ignorar_api:
            corpo["excludeMessages"] = ["wasSentByApi"]  # evita loop de resposta
        return self._req("POST", "/webhook", corpo)


# ---------------------------------------------------------------- utilidades
def arquivo_para_payload(arquivo: str) -> str:
    if arquivo.startswith(("http://", "https://", "data:")):
        return arquivo
    p = Path(arquivo)
    if not p.exists():
        raise SystemExit(f"Arquivo não encontrado: {arquivo}")
    return base64.b64encode(p.read_bytes()).decode("ascii")


def normalizar_numero(n: str) -> str:
    """Mantém JIDs (@g.us, @s.whatsapp.net, @lid, @newsletter); limpa telefone e põe DDI 55."""
    n = n.strip()
    if "@" in n:
        return n
    digitos = re.sub(r"\D", "", n)
    if len(digitos) in (10, 11):  # DDD + número brasileiro sem DDI
        digitos = "55" + digitos
    return digitos


def checar_regra_fea(texto: str) -> list[str]:
    """Regras de escrita FEA aplicáveis a qualquer mensagem do projeto."""
    alertas = []
    if re.search(r"\bpra\b|\bpro\b", texto, re.IGNORECASE):
        alertas.append('usa "pra/pro"; a regra FEA exige "para"/"para o" por extenso')
    if "—" in texto:
        alertas.append("contém travessão em-dash (proibido no padrão FEA)")
    return alertas


def imprimir(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fea_uazapi", description="Cliente uazapi (WhatsApp) FEA")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="estado da instância (conectada, número, perfil)")
    sub.add_parser("limites", help="limites atuais de novas conversas no WhatsApp")
    sub.add_parser("instancias", help="lista instâncias do servidor (exige admintoken)")
    c = sub.add_parser("conectar", help="gera QR code ou código de pareamento")
    c.add_argument("--telefone", help="número para código de pareamento (sem isso, QR code)")
    c.add_argument("--enviar", action="store_true", help="executa de verdade")

    g = sub.add_parser("grupos", help="lista grupos (nome e JID)")
    g.add_argument("--busca", default="")
    g.add_argument("--json", action="store_true", help="saída completa em JSON")

    v = sub.add_parser("verificar", help="verifica se números têm WhatsApp")
    v.add_argument("numeros", nargs="+")

    for nome, ajuda in (("texto", "envia mensagem de texto"), ("midia", "envia mídia")):
        s = sub.add_parser(nome, help=ajuda)
        s.add_argument("numero", help="telefone (DDD+número) ou JID de grupo xxx@g.us")
        if nome == "texto":
            s.add_argument("mensagem", help='texto ou "@arquivo.txt" para ler de arquivo')
        else:
            s.add_argument("tipo", choices=TIPOS_MIDIA)
            s.add_argument("arquivo", help="URL pública ou caminho local")
            s.add_argument("--legenda", default="")
        s.add_argument("--mencionar", help="números separados por vírgula, ou all (só grupos)")
        s.add_argument("--enviar", action="store_true", help="envia de verdade (sem isso: simulação)")
        s.add_argument("--forcar", action="store_true", help="ignora alertas de regra de escrita FEA")

    w = sub.add_parser("webhook", help="vê ou configura o webhook da instância")
    w.add_argument("--url", help="URL que recebe os eventos (sem isso, só mostra o atual)")
    w.add_argument("--eventos", default="messages,connection",
                   help=f"lista separada por vírgula: {','.join(EVENTOS_WEBHOOK)}")
    w.add_argument("--enviar", action="store_true", help="aplica de verdade")

    a = ap.parse_args(argv)
    api = Uazapi()

    try:
        if a.cmd == "status":
            imprimir(api.status())
        elif a.cmd == "limites":
            imprimir(api.limites())
        elif a.cmd == "instancias":
            imprimir(api.listar_instancias())
        elif a.cmd == "conectar":
            if not a.enviar:
                print("[SIMULAÇÃO] geraria", "código de pareamento" if a.telefone else "QR code",
                      "(isso pode derrubar a sessão atual se já estiver conectada). Use --enviar.")
                return 0
            imprimir(api.conectar(a.telefone))
        elif a.cmd == "grupos":
            r = api.listar_grupos(a.busca)
            if a.json:
                imprimir(r)
            else:
                grupos = r.get("groups", r) if isinstance(r, dict) else r
                for gr in grupos or []:
                    print(f"{gr.get('JID') or gr.get('jid')}\t{gr.get('Name') or gr.get('name')}")
        elif a.cmd == "verificar":
            imprimir(api.verificar_numeros([normalizar_numero(n) for n in a.numeros]))
        elif a.cmd in ("texto", "midia"):
            numero = normalizar_numero(a.numero)
            extras = {"mentions": a.mencionar} if a.mencionar else {}
            if a.cmd == "texto":
                texto = a.mensagem
                if texto.startswith("@"):
                    texto = Path(texto[1:]).read_text(encoding="utf-8")
            else:
                texto = a.legenda
            alertas = checar_regra_fea(texto)
            for al in alertas:
                print(f"[ALERTA FEA] {al}", file=sys.stderr)
            if alertas and not a.forcar:
                print("Bloqueado. Corrija o texto ou use --forcar.", file=sys.stderr)
                return 2
            if not a.enviar:
                print(f"[SIMULAÇÃO] {a.cmd} para {numero}")
                if a.cmd == "midia":
                    print(f"  tipo={a.tipo} arquivo={a.arquivo}")
                print("  " + (texto or "(sem legenda)").replace("\n", "\n  "))
                print("Nada foi enviado. Repita com --enviar para enviar.")
                return 0
            if a.cmd == "texto":
                imprimir(api.enviar_texto(numero, texto, **extras))
            else:
                imprimir(api.enviar_midia(numero, a.tipo, a.arquivo, texto, **extras))
        elif a.cmd == "webhook":
            if not a.url:
                imprimir(api.ver_webhook())
                return 0
            eventos = [e.strip() for e in a.eventos.split(",") if e.strip()]
            invalidos = [e for e in eventos if e not in EVENTOS_WEBHOOK]
            if invalidos:
                raise SystemExit(f"Eventos inválidos: {invalidos}")
            if not a.enviar:
                print(f"[SIMULAÇÃO] webhook -> {a.url} eventos={eventos} (ignora msgs da API)")
                print("Webhook atual (será substituído):")
                imprimir(api.ver_webhook())
                return 0
            imprimir(api.configurar_webhook(a.url, eventos))
    except ErroUazapi as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
