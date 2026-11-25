"""Monta a pasta public/ que vai para o Cloudflare: a página em /mpl/ e os arquivos em /mpl/assets/."""
import shutil, pathlib, re
AQUI = pathlib.Path(__file__).resolve().parent
ORIGEM = AQUI.parent
DEST = AQUI / 'public' / 'mpl'
if (AQUI / 'public').exists(): shutil.rmtree(AQUI / 'public')
(DEST / 'assets').mkdir(parents=True)
for f in (ORIGEM / 'assets').iterdir():
    shutil.copy2(f, DEST / 'assets' / f.name)
html = (ORIGEM / 'index.html').read_text(encoding='utf-8')
html = html.replace('"assets/', '"/mpl/assets/').replace("url(\"assets/", "url(\"/mpl/assets/")
assert 'assets/' not in re.sub(r'/mpl/assets/', '', html), 'sobrou caminho relativo'
(DEST / 'index.html').write_text(html, encoding='utf-8')
print('ok:', sorted(p.name for p in (DEST / 'assets').iterdir()))
