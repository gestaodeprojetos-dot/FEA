"""Conferência automática do PDF traduzido: linhas que se cruzam e texto que invade
traço/retângulo desenhado, comparando página a página com o original."""
import pymupdf, sys, json
def linhas(p):
    out=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            t=''.join(s['text'] for s in l['spans']).strip()
            if t and t not in ('•',): out.append((pymupdf.Rect(l['bbox']),t))
    return out
def cruzam(ls):
    n=0
    for i,(a,_) in enumerate(ls):
        for b,_ in ls[i+1:]:
            r=a & b
            if not r.is_empty and r.width>2 and r.height>2: n+=1
    return n
def invade(p, ls):
    n=0
    for d in p.get_drawings():
        for it in d['items']:
            if it[0]=='l':
                y=(it[1].y+it[2].y)/2; x0,x1=sorted((it[1].x,it[2].x))
                if abs(it[1].y-it[2].y)<1 and x1-x0>30:
                    for r,_ in ls:
                        if r.y0+2<y<r.y1-2 and r.x1>x0 and r.x0<x1: n+=1
    return n
o=pymupdf.open(sys.argv[1]); t=pymupdf.open(sys.argv[2])
ruins=[]
for i in range(len(o)):
    lo,lt=linhas(o[i]),linhas(t[i])
    co,ct=cruzam(lo),cruzam(lt); io,it=invade(o[i],lo),invade(t[i],lt)
    if ct>co or it>io: ruins.append((i+1,ct-co,it-io))
print(len(ruins),'paginas com problema:',ruins)
