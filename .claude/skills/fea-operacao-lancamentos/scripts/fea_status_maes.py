import json,urllib.request,time,sys
T=open('/root/.fea_clickup_token').read().strip()
def api(m,p,b=None):
    for i in range(5):
        try:
            r=urllib.request.Request('https://api.clickup.com/api/v2'+p,data=json.dumps(b).encode() if b is not None else None,headers={'Authorization':T,'Content-Type':'application/json'},method=m)
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(25); continue
            raise RuntimeError(e.read().decode())
ANDOU={'fazendo','em revisão','em ajuste','aprovado','feito','revisao','ajustar','complete'}
FOLDERS={'MEI':'1400270000005281','MPL':'1400270000005294','EEX':'1400270000005322','BF Brasil':'901318759044','BF Latam':'901318793839','MTB':'1400270000003387'}
DRY='--dry' in sys.argv; out=[]
for nm,F in FOLDERS.items():
    for L in api('GET',f'/folder/{F}/list?archived=false')['lists']:
        ts=[];pg=0
        while True:
            r=api('GET',f"/list/{L['id']}/task?subtasks=true&include_closed=true&page={pg}")
            ts+=r['tasks']
            if r.get('last_page',True) or not r['tasks']: break
            pg+=1
        kids={}
        for t in ts:
            if t.get('parent'): kids.setdefault(t['parent'],[]).append(t['status']['status'])
        stnames=[s['status'] for s in api('GET',f"/list/{L['id']}")['statuses']]
        for t in ts:
            if t.get('parent') or t['id'] not in kids: continue
            st=t['status']['status']
            if st in ('a fazer','to do','brifado') and any(k in ANDOU for k in kids[t['id']]):
                if 'fazendo' not in stnames: out.append((nm,L['name'],t['name'],'SEM STATUS fazendo')); continue
                if not DRY: api('PUT',f"/task/{t['id']}",{'status':'fazendo'})
                out.append((nm,L['name'],t['name'],t['id']))
for o in out: print(' | '.join(o))
print(len(out),'mães', 'simulado' if DRY else 'atualizadas')
