"""Gera a planilha de inventário dos QR codes do livro Intercorrências (FEA)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROXO, AZUL, LAV, CINZA, OFF = "5B4599", "3846BB", "D0D1E9", "E9E9E9", "F9F9F9"
F = "Montserrat"
fill = lambda c: PatternFill("solid", fgColor=c)
borda = Border(*(Side(style="thin", color=CINZA),) * 4)

D = "https://drive.google.com/file/d/"
Y = "https://www.youtube.com/watch?v="
SOARES = "Artigo de Danny J. Soares, Molecules 2022 (“Bridging a Century-Old Problem”, fisiopatologia da oclusão vascular por AH, FIVO)"
PATTERNS = "Artigo “Patterns of Filler-Induced Facial Skin Ischemia” (revisão de 243 casos, escala FOEM)"
RESTRITO = ("Arquivo com acesso restrito: quem escaneia sem estar na lista de convidados cai na tela “Você precisa de acesso”.",
            "No Drive: Compartilhar > Acesso geral > “Qualquer pessoa com o link” > Leitor. O QR não muda.")
SUMIU = ("Arquivo não encontrado: foi excluído, está na lixeira ou está num Drive pessoal sem compartilhamento. Nem a conta da gestão abre.",
         "Localizar o PDF do artigo, salvar na pasta de artigos do livro com acesso “Qualquer pessoa com o link”, gerar QR novo, substituir na arte e testar com o celular.")

# pág, seção, tipo, plataforma, rótulo no livro, o que o texto promete, destino real, url, status, problema, ação
rows = [
 (13,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo de Danny J. Soares sobre fisiopatologia da oclusão vascular por AH",SOARES+" · molecules-27-05398.pdf",D+"1tHj3C58l9NhqokvQBIisp-RO25MrDGfp/view","ATENÇÃO",*RESTRITO),
 (15,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Introdução ao raciocínio clínico de complicações agudas isquêmicas","Vídeo do Dr. João sobre raciocínio clínico nas complicações isquêmicas agudas","Vídeo “Introdução ao raciocínio clínico de complicações agudas isquêmicas” (canal João Pithon)",Y+"HW62ZM3NDC8","OK","",""),
 (18,"1.1 Oclusão vascular aguda","Artigo","YouTube","Saiba mais","Artigo científico do protocolo HDPH (Alta Dose de Hialuronidase Pulsada), de Claudio DeLorenzi","Vídeo “Revisão anatômica global da face - Vascularização” (o mesmo QR da pág. 29)",Y+"2Qoh7fWG5w4","ERRO",
  "QR trocado: o box promete o artigo HDPH de DeLorenzi, mas o QR abre um vídeo de anatomia vascular. Provável cópia do QR da pág. 29.",
  "Localizar o PDF do artigo HDPH (DeLorenzi), salvar no Drive com acesso “Qualquer pessoa com o link”, gerar QR novo, substituir na arte e testar com o celular."),
 (21,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo sobre a distribuição anatômica das áreas acometidas por isquemia cutânea (escala FOEM)",PATTERNS+" · 5. Patterns_of_Filler_Induced_Facial_Skin_Ischemia__A.15.pdf",D+"1F8aLFw8VV62JQngjfkHLNpHn2lr8jmjj/view","ATENÇÃO",*RESTRITO),
 (23,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “Ischemic Complications of Dermal Fillers” (Plastic and Aesthetic Research)","Não abre (arquivo não encontrado)",D+"1WPpBXXtYISZ68Pf8ak2V2kKkPcLS_GuK/view","ERRO",*SUMIU),
 (26,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “Patterns of Filler-Induced Facial Skin Ischemia” (243 casos, escala FOEM)",PATTERNS+" · 5. Patterns_of_Filler_Induced_Facial_Skin_Ischemia__A.15.pdf",D+"1F8aLFw8VV62JQngjfkHLNpHn2lr8jmjj/view","ATENÇÃO",*RESTRITO),
 (29,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Revisão anatômica global da face, vascularização","Vídeo de revisão anatômica da vascularização da face","Vídeo “Revisão anatômica global da face - Vascularização” (canal João Pithon)",Y+"2Qoh7fWG5w4","OK","",""),
 (30,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “Bridging a Century-Old Problem” (FIVO), mecanismos moleculares da oclusão vascular",SOARES+" · molecules-27-05398.pdf",D+"1tHj3C58l9NhqokvQBIisp-RO25MrDGfp/view","ATENÇÃO",*RESTRITO),
 (32,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Hialuronidase","Aula prática do Dr. João sobre uso clínico da hialuronidase","Vídeo “Hialuronidase” (canal João Pithon)",Y+"zb0ZWo29Pk8","OK","",""),
 (33,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “The Role of Hyaluronidase in the Treatment of Complications From HA Dermal Fillers”","Artigo de Cavallini et al., Aesthetic Surgery Journal 2013 (conteúdo conferido) · 4. HIALURONIDASE REVISAO.pdf",D+"19A8eYYAofI8Eiq4fIyk0kv-kJZf8aAvM/view?usp=drive_link","ATENÇÃO",*RESTRITO),
 (35,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Rinomodelação, protocolo e manejo de complicações","Aula sobre segurança e manejo de complicações na rinomodelação","Vídeo “Rinomodelação: Protocolo e manejo das complicações” (canal João Pithon)",Y+"w7ZawtnNb2o","OK","",""),
 (36,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “Consensus Guidelines for the Management of HA Filler-Induced Vascular Occlusion”","Não abre (arquivo não encontrado)",D+"11p9QK_qVuG__8htGvDWr3wPImLY-Ovbp/view","ERRO",*SUMIU),
 (37,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Mecanismos de segurança com cânulas","Aula sobre uso seguro de cânulas","Vídeo “Mecanismos de segurança com cânulas” (canal João Pithon)",Y+"_yWZEknxYqo","OK","",""),
 (40,"1.1 Oclusão vascular aguda","Artigo","Google Drive","Saiba mais","Artigo “Bridging a Century-Old Problem” (FIVO), implicações terapêuticas",SOARES+" · molecules-27-05398.pdf",D+"1tHj3C58l9NhqokvQBIisp-RO25MrDGfp/view","ATENÇÃO",*RESTRITO),
 (43,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Rinomodelação, agulha ou cânula","Aula sobre agulha ou cânula na rinomodelação","Vídeo “Rinomodelação agulha ou cânula?” (canal João Pithon)",Y+"NCHkXFLKZds","OK","",""),
 (45,"1.1 Oclusão vascular aguda","Vídeo","YouTube","Na prática: Vídeo Preenchimento full face guiado por ultrassom, ao vivo","Aula de preenchimento guiado por ultrassom","Vídeo “Preenchimento full face guiado por ultrassom ao vivo” (canal João Pithon)",Y+"QocyeCsLs9M","OK","",""),
 (61,"1.3 Amaurose aguda","Artigo","Google Drive","Saiba mais","Artigo de revisão das complicações isquêmicas dos preenchedores (necrose a eventos neuro-oftalmológicos)","Não abre (arquivo não encontrado)",D+"1WPpBXXtYISZ68Pf8ak2V2kKkPcLS_GuK/view","ERRO",*SUMIU),
 (63,"1.3 Amaurose aguda","Vídeo","YouTube","Na prática: Vídeo Amaurose, protocolo de manejo das complicações","Aula com o protocolo de conduta imediata na suspeita de amaurose","Vídeo “Amaurose: protocolo de manejo das complicações” (canal João Pithon)",Y+"GnGMUiPcoC0","OK","",""),
 (64,"1.3 Amaurose aguda","Artigo","Google Drive","Saiba mais: Oclusão arterial oftálmica e retiniana associada a preenchimentos faciais","Artigo com achados angiográficos cerebrais e oftálmicos em perda visual pós-preenchimento","Não abre (arquivo não encontrado)",D+"1k9pgxv8gf8-mBA-jTmHvmZ7dFqFcRbQs/view","ERRO",
  SUMIU[0]+" O mesmo QR está na pág. 68, com descrição de artigo parecida mas não idêntica: confirmar se é o mesmo artigo.",SUMIU[1]),
 (68,"1.3 Amaurose aguda","Artigo","Google Drive","Saiba mais","Artigo sobre achados angiográficos cerebrais na oclusão da artéria oftálmica (AH vs. gordura autóloga)","Não abre (arquivo não encontrado)",D+"1k9pgxv8gf8-mBA-jTmHvmZ7dFqFcRbQs/view","ERRO",
  SUMIU[0]+" Mesmo QR da pág. 64: confirmar se os dois boxes falam do mesmo artigo.",SUMIU[1]),
 (74,"1.3 Amaurose aguda","Vídeo","YouTube","Na prática: Vídeo 9, Complexo vascular nasoglabelar","Aula prática de dissecção do complexo vascular nasoglabelar","Vídeo “Complexo vascular nasoglabelar” (canal João Pithon)",Y+"YUirUEfaMjc","OK","",""),
 (79,"Capítulo 2 (abertura)","Vídeo","YouTube","Na prática: Vídeo 10, Complicações agudas não isquêmicas (parte 1)","Aula sobre intercorrências agudas não isquêmicas, parte 1","Vídeo “Complicações agudas não isquêmicas parte 1” (canal João Pithon)",Y+"XzONB5671uY","OK","",""),
 (80,"Capítulo 2 (abertura)","Vídeo","YouTube","Na prática: Vídeo 11, Complicações agudas não isquêmicas (parte 2)","Aula sobre intercorrências agudas não isquêmicas, parte 2","Vídeo “Complicações agudas não isquêmicas Parte 2” (canal João Pithon)",Y+"dh26SwtfD2U","OK","",""),
]

from collections import defaultdict
pags = defaultdict(list)
for r in rows: pags[r[7]].append(r[0])
STATUS_FMT = {"OK": (LAV, ROXO), "ATENÇÃO": ("FFF1CC", "7A5B00"), "ERRO": ("F6DADA", "BB3838")}

wb = Workbook()
ws = wb.active; ws.title = "QR codes"
ws.sheet_view.showGridLines = False
head = ["#","Pág.","Seção do livro","Tipo","Plataforma","Rótulo no livro","O que o texto do livro promete","Para onde o QR leva de fato","Link do QR","Repetido em","Abre sem login?","Revisão","Problema encontrado","Ação recomendada","Responsável","Data prevista","Status da correção"]
widths = [5,7,24,9,13,34,42,44,46,14,12,11,48,48,18,14,18]
ws["A1"] = "Inventário de QR Codes · Livro Intercorrências no Preenchimento com Ácido Hialurônico · Dr. João Pithon"
ws["A1"].font = Font(name=F, size=14, bold=True, color="FFFFFF")
ws["A2"] = ("23 QR codes lidos do PDF final (versão de 01/10/2026, 221 páginas) · todos os links testados sem login em 05/10/2026 · "
            "11 OK · 6 ATENÇÃO (artigo restrito) · 6 ERRO (QR trocado ou arquivo inexistente)")
ws["A3"] = ("Preencha só as colunas amarelas. O QR é imagem: trocar o arquivo de destino não muda o QR, mas se o LINK mudar a imagem tem de ser regerada, "
            "substituída na arte e conferida escaneando com o celular. Para os itens ATENÇÃO basta mudar o compartilhamento: o link e o QR continuam os mesmos.")
for r_, color, sz, it in ((1, ROXO, 14, False), (2, AZUL, 10, False), (3, LAV, 10, True)):
    ws.merge_cells(start_row=r_, start_column=1, end_row=r_, end_column=len(head))
    c = ws.cell(r_, 1); c.fill = fill(color)
    if r_ > 1: c.font = Font(name=F, size=sz, italic=it, color="FFFFFF" if r_ == 2 else "1E1B4B")
    c.alignment = Alignment(wrap_text=True, vertical="center", indent=1)
ws.row_dimensions[1].height = 30; ws.row_dimensions[2].height = 22; ws.row_dimensions[3].height = 36
HR = 5
for i, (h, w) in enumerate(zip(head, widths), 1):
    c = ws.cell(HR, i, h); c.font = Font(name=F, bold=True, color="FFFFFF", size=10)
    c.fill = fill(ROXO if i < 15 else AZUL); c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = borda
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[HR].height = 32
for n, r in enumerate(rows, 1):
    pag, sec, tipo, plat, rot, prom, dest, url, st, prob, acao = r
    outras = [p for p in pags[url] if p != pag]
    rep = ("pág. " + ", ".join(map(str, outras))) if outras else "não"
    aberto = "Sim" if plat == "YouTube" else "Não"
    vals = [n, pag, sec, tipo, plat, rot, prom, dest, url, rep, aberto, st, prob, acao, "", "", "pendente" if st != "OK" else "n/a"]
    R = HR + n
    for i, v in enumerate(vals, 1):
        c = ws.cell(R, i, v); c.font = Font(name=F, size=9); c.border = borda
        c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="center" if i in (1,2,4,10,11,12,16,17) else "left")
        c.fill = fill("FFFFFF" if n % 2 else OFF)
        if i >= 15: c.fill = fill("FFF8D6")
    lc = ws.cell(R, 9); lc.hyperlink = url; lc.font = Font(name=F, size=9, color=AZUL, underline="single")
    bg, fg = STATUS_FMT[st]; sc = ws.cell(R, 12); sc.fill = fill(bg); sc.font = Font(name=F, size=9, bold=True, color=fg)
    if aberto == "Não": ws.cell(R, 11).font = Font(name=F, size=9, bold=True, color="BB3838")
    if st == "ERRO": ws.cell(R, 8).font = Font(name=F, size=9, bold=True, color="BB3838")
ws.freeze_panes = ws.cell(HR + 1, 3)
ws.auto_filter.ref = f"A{HR}:{get_column_letter(len(head))}{HR+len(rows)}"

# Aba de links únicos
u = wb.create_sheet("Links únicos"); u.sheet_view.showGridLines = False
uh = ["Link do QR","Plataforma","Destino","Páginas","Qtd. de QR","Abre sem login?","Revisão"]
for i, (h, w) in enumerate(zip(uh, [52,13,60,16,10,13,11]), 1):
    c = u.cell(1, i, h); c.font = Font(name=F, bold=True, color="FFFFFF", size=10); c.fill = fill(ROXO)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); u.column_dimensions[get_column_letter(i)].width = w
seen = []
for r in rows:
    if r[7] in seen: continue
    seen.append(r[7])
for k, url in enumerate(seen, 2):
    r = next(x for x in rows if x[7] == url)
    st = "ERRO" if any(x[8] == "ERRO" for x in rows if x[7] == url and x[0] != 29) else r[8]
    if url.endswith("2Qoh7fWG5w4"): st = "OK"
    vals = [url, r[3], r[6], ", ".join(map(str, pags[url])), len(pags[url]), "Sim" if r[3] == "YouTube" else "Não", st]
    for i, v in enumerate(vals, 1):
        c = u.cell(k, i, v); c.font = Font(name=F, size=9); c.border = borda; c.alignment = Alignment(wrap_text=True, vertical="top")
    u.cell(k, 1).hyperlink = url; u.cell(k, 1).font = Font(name=F, size=9, color=AZUL, underline="single")
    bg, fg = STATUS_FMT[st]; u.cell(k, 7).fill = fill(bg); u.cell(k, 7).font = Font(name=F, size=9, bold=True, color=fg)
u.freeze_panes = "A2"

# Aba de resumo
s = wb.create_sheet("Resumo e pendências"); s.sheet_view.showGridLines = False
s.column_dimensions["A"].width = 58; s.column_dimensions["B"].width = 12; s.column_dimensions["C"].width = 70
def linha(rw, a, b="", c="", bold=False, bg=None, color="1E1B4B"):
    for i, v in enumerate((a, b, c), 1):
        cell = s.cell(rw, i, v); cell.font = Font(name=F, size=10, bold=bold, color=color); cell.alignment = Alignment(wrap_text=True, vertical="top")
        if bg: cell.fill = fill(bg)
N = len(rows); Rf, Rl = HR + 1, HR + N
linha(1, "Resumo da revisão dos QR codes", bold=True, bg=ROXO, color="FFFFFF")
linha(2, "Indicador", "Total", "Leitura", bold=True, bg=LAV)
ind = [
 ("Total de QR codes no PDF", f"=COUNTA('QR codes'!B{Rf}:B{Rl})", "Páginas 13 a 80. Das páginas 81 a 221 não há nenhum QR (conferido página a página)."),
 ("QR de vídeo (YouTube)", f"=COUNTIF('QR codes'!E{Rf}:E{Rl},\"YouTube\")", "12 QR para 11 vídeos únicos. Todos abrem sem login e o título bate com o texto, exceto o da pág. 18."),
 ("QR de artigo (Google Drive)", f"=COUNTIF('QR codes'!E{Rf}:E{Rl},\"Google Drive\")", "11 QR para 6 arquivos únicos. Nenhum abre para quem não está na lista de convidados."),
 ("OK", f"=COUNTIF('QR codes'!L{Rf}:L{Rl},\"OK\")", "Destino correto e acessível."),
 ("ATENÇÃO: artigo existe, mas com acesso restrito", f"=COUNTIF('QR codes'!L{Rf}:L{Rl},\"ATENÇÃO\")", "Págs. 13, 21, 26, 30, 33 e 40. Resolve mudando o compartilhamento de 3 arquivos, sem mexer na arte."),
 ("ERRO: QR quebrado ou trocado", f"=COUNTIF('QR codes'!L{Rf}:L{Rl},\"ERRO\")", "Págs. 18, 23, 36, 61, 64 e 68. Exige QR novo na arte."),
 ("Correções pendentes", f"=COUNTIF('QR codes'!Q{Rf}:Q{Rl},\"pendente\")", "Atualiza sozinho quando a coluna «Status da correção» muda. Use: pendente · em correção · corrigido e testado."),
]
for k, (a, b, c) in enumerate(ind, 3): linha(k, a, b, c)
k = 3 + len(ind) + 1
linha(k, "Prioridade de correção", bold=True, bg=ROXO, color="FFFFFF"); k += 1
prio = [
 "1. Pág. 18: o box «Saiba mais» promete o artigo HDPH (DeLorenzi), mas o QR abre o vídeo de vascularização da pág. 29. Precisa do PDF do artigo e de QR novo.",
 "2. Págs. 23 e 61 (mesmo link), 36, 64 e 68 (mesmo link): 3 arquivos de artigo não existem mais ou estão num Drive pessoal. Localizar os PDFs, subir na pasta de artigos com acesso público e regerar os QR.",
 "3. Págs. 64 e 68 usam o mesmo QR, mas os textos descrevem estudos levemente diferentes (achados angiográficos oftálmicos vs. cerebrais). Confirmar com a equipe médica se é o mesmo artigo antes de regerar.",
 "4. 3 artigos restritos (molecules-27-05398.pdf, Patterns of Filler-Induced..., 4. HIALURONIDASE REVISAO.pdf): mudar para «Qualquer pessoa com o link: Leitor». Corrige 6 QR de uma vez sem mexer na arte.",
 "5. Numeração dos vídeos: só os 3 últimos boxes têm número (Vídeo 9, 10 e 11). Os 9 anteriores não têm. Padronizar na diagramação: ou todos numerados, ou nenhum.",
 "6. Depois de corrigir, escanear de novo todos os QR com um celular deslogado do Google (ou aba anônima) antes de liberar o PDF.",
]
for p in prio: linha(k, p); s.merge_cells(start_row=k, start_column=1, end_row=k, end_column=3); s.row_dimensions[k].height = 32; k += 1
k += 1
linha(k, "Rastreamento de funil (oportunidade)", bold=True, bg=ROXO, color="FFFFFF"); k += 1
trk = [
 "Limitação atual: os QR apontam direto para YouTube e Drive, sem UTM nem redirecionador. Hoje não dá para saber quantos leitores escanearam cada QR, nem quais capítulos geram mais interesse.",
 "Oportunidade: ao regerar os 6 QR com erro, usar um link curto com redirecionamento (por exemplo, uma página em joaopithon.com.br/livro/qr-18) com UTM único por QR. Assim, trocar o destino no futuro não exige reimprimir o QR.",
 "Os vídeos do YouTube também podem levar card ou link na descrição para a próxima etapa do funil (Masterclass, FEA), medindo a passagem do livro para a captação.",
 "Sem métrica, otimização é palpite.",
]
for p in trk: linha(k, p); s.merge_cells(start_row=k, start_column=1, end_row=k, end_column=3); s.row_dimensions[k].height = 32; k += 1

wb.move_sheet("Resumo e pendências", offset=-2)
wb.active = 0
out = "FEA-Inventario-QR-Livro-Intercorrencias.xlsx"
wb.save(out); print(out, N)
