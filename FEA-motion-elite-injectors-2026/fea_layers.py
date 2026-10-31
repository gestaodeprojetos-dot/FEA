import sys, numpy as np, cv2
S=sys.argv[1]
img=cv2.imread(f'{S}/src/descanso.png', cv2.IMREAD_COLOR)  # BGR
H,W=img.shape[:2]
# people alpha
m=cv2.imread(f'{S}/work/mask_birefnet-portrait.png',0)
pa=np.zeros((H,W),np.uint8); pa[:,1300:]=m
cv2.imwrite(f'{S}/work/people_alpha.png',pa)
# logo alpha: luminance in box
x0,y0,x1,y1=230,500,1200,830
box=img[y0:y1,x0:x1].astype(np.float32)
lum=box.mean(2)
bgl=np.percentile(lum,30)
a=np.clip((lum-(bgl+18))/(150-(bgl+18)),0,1)
la=np.zeros((H,W),np.float32); la[y0:y1,x0:x1]=a
cv2.imwrite(f'{S}/work/logo_alpha.png',(la*255).astype(np.uint8))
print('bg lum',bgl)
# plate: inpaint people + logo (at 1/4 res), keep original outside
hole=(cv2.dilate(((pa>5)).astype(np.uint8),np.ones((9,9),np.uint8))|cv2.dilate((la>0.01).astype(np.uint8),np.ones((31,31),np.uint8))).astype(np.uint8)*255
hole=cv2.dilate(hole,np.ones((41,41),np.uint8))
sm=cv2.resize(img,(W//4,H//4),interpolation=cv2.INTER_AREA)
hs=cv2.resize(hole,(W//4,H//4),interpolation=cv2.INTER_NEAREST)
inp=cv2.inpaint(sm,hs,25,cv2.INPAINT_TELEA)
inp=cv2.GaussianBlur(inp,(0,0),6)
up=cv2.resize(inp,(W,H),interpolation=cv2.INTER_CUBIC)
tight=(cv2.dilate((pa>8).astype(np.uint8),np.ones((7,7),np.uint8))|cv2.dilate((la>0.01).astype(np.uint8),np.ones((9,9),np.uint8)))*255
hf=cv2.GaussianBlur(tight.astype(np.uint8),(0,0),2).astype(np.float32)[...,None]/255
plate=(img*(1-hf)+up*hf).astype(np.uint8)
cv2.imwrite(f'{S}/work/plate.png',plate)
cv2.imwrite(f'{S}/work/plate_prev.jpg',cv2.resize(plate,(2016,672)))
cv2.imwrite(f'{S}/work/logo_prev.jpg',cv2.resize((la*255).astype(np.uint8)[y0:y1,x0:x1],None,fx=0.5,fy=0.5))
