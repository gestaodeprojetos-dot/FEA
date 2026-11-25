#!/usr/bin/env python3
"""FEA WordPress: conexão via REST API + Application Passwords (sem plugin extra).

Credenciais lidas do ambiente (nunca hardcoded). Para cada site, procura primeiro
WP_USER_<SITE> / WP_APP_PASSWORD_<SITE> e depois o par genérico WP_USER / WP_APP_PASSWORD.
SITE = MAIN, FEP, FEB, IFF, FEF.

Uso:
  python3 fea_wp.py test                 # testa login em todos os sites
  python3 fea_wp.py pages <site>         # lista páginas (id, status, slug, título)
  python3 fea_wp.py posts <site>         # lista posts
  python3 fea_wp.py get <site> <page_id> # mostra uma página
"""
import base64, json, os, sys, urllib.request, urllib.error

SITES = {
    "MAIN": "https://joaopithon.com.br",
    "FEP": "https://fep.joaopithon.com.br",
    "FEB": "https://feb.joaopithon.com.br",
    "IFF": "https://iff.joaopithon.com.br",
    "FEF": "https://fef.joaopithon.com.br",
}

def load_dotenv():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))

def creds(site):
    u = os.environ.get(f"WP_USER_{site}") or os.environ.get("WP_USER")
    p = os.environ.get(f"WP_APP_PASSWORD_{site}") or os.environ.get("WP_APP_PASSWORD")
    return u, p

def call(site, path, method="GET", data=None):
    u, p = creds(site)
    if not (u and p):
        raise RuntimeError(f"sem credencial para {site}")
    req = urllib.request.Request(SITES[site] + "/wp-json" + path, method=method,
                                 data=json.dumps(data).encode() if data else None)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{u}:{p}".encode()).decode())
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "fea-wp-client")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    load_dotenv()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    if cmd == "test":
        for s in SITES:
            try:
                me = call(s, "/wp/v2/users/me?context=edit")
                print(f"OK    {s:5} {SITES[s]}  usuário: {me.get('name')}  papéis: {me.get('roles')}")
            except urllib.error.HTTPError as e:
                print(f"ERRO  {s:5} {SITES[s]}  HTTP {e.code}: {e.read()[:200].decode(errors='ignore')}")
            except Exception as e:
                print(f"FALTA {s:5} {SITES[s]}  {e}")
    elif cmd in ("pages", "posts"):
        site = sys.argv[2].upper()
        for it in call(site, f"/wp/v2/{cmd}?per_page=100&status=any&context=edit&_fields=id,status,slug,title,modified"):
            print(f"{it['id']:>6}  {it['status']:8} {it['modified'][:10]}  /{it['slug']}  {it['title']['raw']}")
    elif cmd == "get":
        site, pid = sys.argv[2].upper(), sys.argv[3]
        print(json.dumps(call(site, f"/wp/v2/pages/{pid}?context=edit"), ensure_ascii=False, indent=2)[:5000])
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
