import sys, pymupdf, cv2, numpy as np
from pyzbar import pyzbar
pdf=sys.argv[1]; off=int(sys.argv[2]) if len(sys.argv)>2 else 0
d=pymupdf.open(pdf); det=cv2.QRCodeDetector()
for p in d:
    found=set()
    for dpi in (200,300):
        pix=p.get_pixmap(dpi=dpi); img=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)
        g=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY if pix.n==3 else cv2.COLOR_RGBA2GRAY)
        for r in pyzbar.decode(g):
            if r.type=='QRCODE': found.add((r.data.decode(), r.rect.top//(dpi/72)))
        ok,vals,pts,_=det.detectAndDecodeMulti(g)
        if ok:
            for v,pt in zip(vals,pts):
                if v: found.add((v, int(pt[:,1].min()/(dpi/72))))
    urls={}
    for v,y in sorted(found,key=lambda x:x[1]): urls.setdefault(v,y)
    for v,y in urls.items(): print(f"{p.number+1+off}\t{int(y)}\t{v}")
