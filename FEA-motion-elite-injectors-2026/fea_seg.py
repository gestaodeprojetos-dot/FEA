import sys
from PIL import Image
from rembg import remove, new_session
S=sys.argv[1]
im=Image.open(f'{S}/src/descanso.png').convert('RGB')
crop=im.crop((1300,0,4032,1344))  # people region only
for model in ['birefnet-portrait','isnet-general-use']:
    try:
        sess=new_session(model)
        m=remove(crop, session=sess, only_mask=True)
        m.save(f'{S}/work/mask_{model}.png'); print('ok',model)
    except Exception as e: print('fail',model,e)
