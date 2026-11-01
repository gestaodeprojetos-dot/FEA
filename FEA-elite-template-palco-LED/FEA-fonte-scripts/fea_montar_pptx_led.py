# FEA · Monta o PPTX 4032x1344 de um palestrante: cada slide vira imagem no fundo Elite e os vídeos voltam ao lugar
import sys, os, glob, json, subprocess, zipfile, tempfile
from pptx import Presentation
from pptx.util import Emu
from lxml import etree
PX = 9525
WIN_X, WIN_W, WIN_H = 821, 2390, 1344
img_dir, saida = sys.argv[1], sys.argv[2]
videos = json.loads(sys.argv[3]) if len(sys.argv) > 3 else []   # [{slide, path, x,y,w,h (frações do slide 16:9)}]
tmp = tempfile.mkdtemp()
NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
def dur_ms(p):
    out = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip()
    try: return int(float(out)*1000)
    except: return 60000
def poster(p, w, h, k):
    out = f'{tmp}/poster{k}.jpg'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss','0.3','-i',p,'-frames:v','1','-vf',f'scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}',out])
    if not os.path.exists(out):
        from PIL import Image; Image.new('RGB',(w,h),(5,12,15)).save(out)
    return out
prs = Presentation()
prs.slide_width, prs.slide_height = Emu(4032*PX), Emu(1344*PX)
blank = prs.slide_layouts[6]
k = 0
for i, f in enumerate(sorted(glob.glob(f'{img_dir}/slide-*.jpg')), 1):
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(f, 0, 0, prs.slide_width, prs.slide_height)
    vs = [v for v in videos if v['slide'] == i]
    ids = []
    for v in vs:
        x = WIN_X + v['x']*WIN_W; y = v['y']*WIN_H; w = v['w']*WIN_W; h = v['h']*WIN_H
        # recorta o que passaria da janela 16:9 para não invadir as laterais
        x0, y0 = max(x, WIN_X), max(y, 0); x1, y1 = min(x+w, WIN_X+WIN_W), min(y+h, WIN_H)
        x, y, w, h = x0, y0, x1-x0, y1-y0
        k += 1
        mime = 'video/quicktime' if v['path'].lower().endswith('.mov') else 'video/mp4'
        mv = s.shapes.add_movie(v['path'], Emu(int(x*PX)), Emu(int(y*PX)), Emu(int(w*PX)), Emu(int(h*PX)),
                                poster_frame_image=poster(v['path'], int(w), int(h), k), mime_type=mime)
        ids.append((mv.shape_id, dur_ms(v['path'])))
    if ids:
        old = s.element.find(f'{{{NS}}}timing')
        if old is not None: s.element.remove(old)
        n = [2]
        def nid(): n[0] += 1; return n[0]
        clicks = ''.join(f'''<p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{nid()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par><p:cTn id="{nid()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{nid()}" dur="{d}" fill="hold"/><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>''' for sid, d in ids)
        media = ''.join(f'''<p:video><p:cMediaNode vol="80000"><p:cTn id="{nid()}" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cMediaNode></p:video>''' for sid, d in ids)
        xml = f'''<p:timing xmlns:p="{NS}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{clicks}</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>{media}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'''
        t = etree.fromstring(xml)
        ext = s.element.find(f'{{{NS}}}extLst')
        if ext is not None: ext.addprevious(t)
        else: s.element.append(t)
prs.save(saida)
print('ok', saida, len(prs.slides), 'slides,', k, 'vídeos')
