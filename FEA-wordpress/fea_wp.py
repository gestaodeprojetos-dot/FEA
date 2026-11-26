#!/usr/bin/env python3
"""FEA WordPress: acesso aos 5 sites pela REST API usando o usuário que já existe.

Login pelo wp-login.php (usuário e senha normais) + nonce da REST API, porque o
servidor da FEA não repassa o cabeçalho Authorization para o WordPress.
Credenciais lidas do ambiente, nunca hardcoded:
  WP_USER (ou WP_USER_<SITE>) e WP_PASS_<CHAVE>, chaves: SITE (principal), FEP, FEB, IFF, FEF, PL.
  Preferencial: WP_APP_PASSWORD_<SITE> (senha de aplicativo), SITE = MAIN, FEP, FEB, IFF, FEF, PL.

Uso:
  python3 fea_wp.py test                 # testa login em todos os sites
  python3 fea_wp.py pages <site>         # lista páginas
  python3 fea_wp.py posts <site>         # lista posts
  python3 fea_wp.py get <site> <page_id> # mostra uma página
"""
import http.cookiejar, json, os, re, sys, urllib.parse, urllib.request, urllib.error

SITES = {
    "MAIN": "https://joaopithon.com.br",
    "FEP": "https://fep.joaopithon.com.br",
    "FEB": "https://feb.joaopithon.com.br",
    "IFF": "https://iff.joaopithon.com.br",
    "FEF": "https://fef.joaopithon.com.br",
    "PL": "https://pl.joaopithon.com.br",
}
# ordem de tentativa das senhas por site
PASS_KEYS = {"MAIN": ["SITE"], "FEP": ["FEP", "SITE", "PL"], "FEB": ["FEB"], "IFF": ["IFF"], "FEF": ["FEF"], "PL": ["PL"]}
UA = "Mozilla/5.0 (fea-wp-client)"

class Session:
    def __init__(self, site):
        self.site, self.base = site, SITES[site]
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.nonce = None
        self.basic = None

    def _open(self, url, data=None, headers=None, method=None):
        req = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": UA, **(headers or {})})
        return self.op.open(req, timeout=40)

    def login(self):
        # 1) senha de aplicativo (Basic Auth): WP_APP_PASSWORD_<SITE>, WP_APP_PASSWORD, ou as WP_PASS_<CHAVE>
        import base64
        u = os.environ.get(f"WP_USER_{self.site}") or os.environ.get("WP_USER")
        cands = [f"WP_APP_PASSWORD_{self.site}", "WP_APP_PASSWORD"] + [f"WP_PASS_{k}" for k in PASS_KEYS[self.site]]
        for var in cands:
            pw = os.environ.get(var)
            if not (u and pw):
                continue
            self.basic = "Basic " + base64.b64encode(f"{u}:{pw}".encode()).decode()
            try:
                self.call("/wp/v2/users/me")
                self.key = var
                return self
            except urllib.error.HTTPError:
                self.basic = None
        # 2) login normal pelo wp-login.php (barrado por captcha da hospedagem a partir da nuvem)
        user = os.environ.get(f"WP_USER_{self.site}") or os.environ.get("WP_USER")
        keys = [k for k in PASS_KEYS[self.site] if os.environ.get(f"WP_PASS_{k}")]
        if not (user and keys):
            raise RuntimeError("sem credencial no ambiente")
        self._open(self.base + "/wp-login.php").read()  # cookie de teste
        for k in keys:
            form = urllib.parse.urlencode({"log": user, "pwd": os.environ[f"WP_PASS_{k}"], "rememberme": "forever",
                                           "wp-submit": "Log In", "redirect_to": self.base + "/wp-admin/", "testcookie": "1"}).encode()
            self._open(self.base + "/wp-login.php", data=form).read()
            if any(c.name.startswith("wordpress_logged_in") for c in self.jar):
                n = self._open(self.base + "/wp-admin/admin-ajax.php?action=rest-nonce").read().decode().strip()
                if re.fullmatch(r"[0-9a-f]{10}", n):
                    self.nonce, self.key = n, f"login WP_PASS_{k}"
                    return self
        raise RuntimeError("login recusado (usuário ou senha incorretos, ou 2FA/captcha no login)")

    def call(self, path, method="GET", data=None):
        r = self._open(self.base + "/wp-json" + path, method=method,
                       data=json.dumps(data).encode() if data is not None else None,
                       headers={**({"Authorization": self.basic} if self.basic else {"X-WP-Nonce": self.nonce}),
                                "Content-Type": "application/json"})
        return json.load(r)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    if cmd == "test":
        for s in SITES:
            try:
                ss = Session(s).login()
                me = ss.call("/wp/v2/users/me?context=edit")
                print(f"OK    {s:5} {SITES[s]}  usuário: {me.get('name')}  papéis: {me.get('roles')}  (via {ss.key})")
            except urllib.error.HTTPError as e:
                print(f"ERRO  {s:5} {SITES[s]}  HTTP {e.code}: {e.read()[:150].decode(errors='ignore')}")
            except Exception as e:
                print(f"ERRO  {s:5} {SITES[s]}  {e}")
    elif cmd in ("pages", "posts"):
        ss = Session(sys.argv[2].upper()).login()
        for it in ss.call(f"/wp/v2/{cmd}?per_page=100&status=any&context=edit&_fields=id,status,slug,title,modified"):
            print(f"{it['id']:>6}  {it['status']:8} {it['modified'][:10]}  /{it['slug']}  {it['title']['raw']}")
    elif cmd == "get":
        ss = Session(sys.argv[2].upper()).login()
        print(json.dumps(ss.call(f"/wp/v2/pages/{sys.argv[3]}?context=edit"), ensure_ascii=False, indent=2)[:5000])
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
