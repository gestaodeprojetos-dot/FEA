"""FEA, cliente da API Hotmart.

Lê credenciais do ambiente (nunca hardcoded):
  HOTMART_CLIENT_ID, HOTMART_CLIENT_SECRET
  HOTMART_BASIC (opcional; se ausente, é gerado a partir de id:secret)

Uso:
  python fea_hotmart.py teste            # valida a conexão (gera token)
  python fea_hotmart.py vendas [dias]    # histórico de vendas dos últimos N dias (padrão 7)
"""
import base64, json, os, sys, time, urllib.parse, urllib.request

AUTH_URL = "https://api-sec-vlc.hotmart.com/security/oauth/token"
API = "https://developers.hotmart.com"


def _env(nome):
    v = os.environ.get(nome)
    if not v:
        sys.exit(f"Variável {nome} não definida no ambiente.")
    return v


def token():
    cid, sec = _env("HOTMART_CLIENT_ID"), _env("HOTMART_CLIENT_SECRET")
    basic = os.environ.get("HOTMART_BASIC") or base64.b64encode(f"{cid}:{sec}".encode()).decode()
    q = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": cid, "client_secret": sec})
    req = urllib.request.Request(f"{AUTH_URL}?{q}", method="POST",
                                 headers={"Authorization": f"Basic {basic.removeprefix('Basic ')}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["access_token"]


def get(path, params=None, tk=None):
    url = f"{API}{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tk or token()}",
                                               "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def vendas(dias=7):
    tk, fim = token(), int(time.time() * 1000)
    params = {"start_date": fim - dias * 86400000, "end_date": fim, "max_results": 50}
    itens = []
    while True:
        d = get("/payments/api/v1/sales/history", params, tk)
        itens += d.get("items", [])
        nxt = d.get("page_info", {}).get("next_page_token")
        if not nxt:
            return itens
        params["page_token"] = nxt


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "teste"
    if cmd == "teste":
        token()
        print("Conexão com a Hotmart OK.")
    elif cmd == "vendas":
        v = vendas(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
        print(json.dumps(v, ensure_ascii=False, indent=2))
        print(f"\nTotal: {len(v)} vendas", file=sys.stderr)
