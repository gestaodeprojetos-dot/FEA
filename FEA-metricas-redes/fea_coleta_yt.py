import openpyxl, subprocess, json, csv
from concurrent.futures import ThreadPoolExecutor
ws=openpyxl.load_workbook('FEA-planilha.xlsx',data_only=True)['POSTAGENS YOUTUBE']
rows=[(i,r) for i,r in enumerate(ws.iter_rows(min_row=2,values_only=True),start=2) if r[6]]
def get(item):
    i,r=item
    try:
        o=subprocess.run(['yt-dlp','--skip-download','-q','--no-warnings','--print','%(.{title,view_count,like_count,comment_count,upload_date,duration})j',r[6]],capture_output=True,text=True,timeout=90).stdout.strip()
        return i,r,json.loads(o.splitlines()[-1])
    except Exception as e: return i,r,{'erro':str(e)[:80]}
with ThreadPoolExecutor(8) as ex: res=list(ex.map(get,rows))
with open('FEA-metricas-youtube.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['linha_planilha','nome','link','titulo_youtube','data_publicacao','duracao_s','visualizacoes','curtidas','comentarios','erro'])
    for i,r,d in res: w.writerow([i,r[0],r[6],d.get('title'),d.get('upload_date'),d.get('duration'),d.get('view_count'),d.get('like_count'),d.get('comment_count'),d.get('erro','')])
print(sum(1 for *_,d in res if d.get('view_count') is not None),'de',len(res))
