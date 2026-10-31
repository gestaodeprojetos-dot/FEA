# FEA · Pós-processamento do PPTX: espaços reservados de foto viram tipo "pic" com cantos arredondados
import re, sys, zipfile, shutil, os
src, dst = sys.argv[1], sys.argv[2]
zin = zipfile.ZipFile(src)
files = {n: zin.read(n) for n in zin.namelist()}
EMU_PX = 9525
pic_idx = {}  # layout -> set(idx)
def fix_layout(name, xml):
    out = []; idxs = set()
    for sp in re.split(r'(?=<p:sp>)', xml):
        m = re.search(r'<p:ph\s+idx="(\d+)"\s+hasCustomPrompt="1"\s*/>', sp)
        if m and 'type=' not in m.group(0):
            idxs.add(m.group(1))
            sp = sp.replace(m.group(0), f'<p:ph type="pic" idx="{m.group(1)}" hasCustomPrompt="1"/>')
            ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', sp)
            r = 20 * EMU_PX; adj = int(r / min(int(ext.group(1)), int(ext.group(2))) * 100000)
            sp = re.sub(r'<a:prstGeom prst="rect">\s*<a:avLst>\s*</a:avLst>\s*</a:prstGeom>|<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>',
                        f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst></a:prstGeom>', sp, count=1)
        out.append(sp)
    pic_idx[name] = idxs
    return ''.join(out)
for n in list(files):
    if re.match(r'ppt/slideLayouts/slideLayout\d+\.xml$', n):
        x = re.sub(r'\s*\n\s*', ' ', files[n].decode()).replace('<p:ph ', '<p:ph ')
        x = re.sub(r'<p:ph\s+', '<p:ph ', x); x = re.sub(r'\s+/>', '/>', x)
        files[n] = fix_layout(n, x).encode()
n_fix = 0
for n in list(files):
    m = re.match(r'ppt/slides/slide(\d+)\.xml$', n)
    if not m: continue
    rels = files[f'ppt/slides/_rels/slide{m.group(1)}.xml.rels'].decode()
    lay = 'ppt/slideLayouts/' + re.search(r'slideLayouts/(slideLayout\d+\.xml)', rels).group(1)
    x = re.sub(r'<p:ph\s+', '<p:ph ', files[n].decode()); x = re.sub(r'\s+/>', '/>', x); x = re.sub(r'\n\s*', ' ', x)
    for idx in pic_idx.get(lay, ()):
        pat = f'<p:ph idx="{idx}" hasCustomPrompt="1"/>'
        if pat in x: x = x.replace(pat, f'<p:ph type="pic" idx="{idx}"/>'); n_fix += 1
    files[n] = x.encode()
# Renomeia mídias com nomes inválidos em part name (":" e "#" vindos do título do layout)
ren = {}
for i, n in enumerate(sorted(x for x in files if x.startswith('ppt/media/') and not x.endswith('/')), 1):
    ext = n.rsplit('.', 1)[-1].lower()
    novo = f'ppt/media/fea_elite_{i:02d}.{ext}'
    ren[n] = novo
for velho, novo in ren.items():
    files[novo] = files.pop(velho)
    vb, nb = velho.split('/')[-1], novo.split('/')[-1]
    for n in list(files):
        if n.endswith('.rels'):
            d = files[n].decode()
            if '../media/' + vb in d: files[n] = d.replace('../media/' + vb + '"', '../media/' + nb + '"').encode()
order = [ren.get(n, n) for n in zin.namelist() if not n.endswith('/')]
tmp = dst + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in order: z.writestr(n, files[n])
shutil.move(tmp, dst)
print('mídias renomeadas:', len(ren), '| layouts com foto:', {k.split('/')[-1]: sorted(v) for k, v in pic_idx.items() if v}, '| slides corrigidos:', n_fix)
