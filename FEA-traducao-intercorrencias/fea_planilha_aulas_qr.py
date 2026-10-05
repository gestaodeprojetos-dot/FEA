#!/usr/bin/env python3
"""Planilha de curadoria da tradução ES do livro de Intercorrências.

Quatro abas: Resumo e prazo · Aulas para traduzir · QR para ajustar · Decisões pendentes.
Fonte dos dados: inventário de QR de 05/10/2026 (23 QR, págs. 13 a 80), auditoria de
02/10/2026, texto do livro (boxes "NA PRÁTICA" e "SAIBA MAIS") e catálogo de aulas da skill.
Páginas marcadas com "~" ainda precisam ser confirmadas com o PDF na Passagem 0.

Uso: python3 fea_planilha_aulas_qr.py FEA-Traducao-ES-Intercorrencias-Aulas-e-QR.xlsx
"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROXO, LAVANDA, AMARELO, VERMELHO = "5B4599", "D0D1E9", "FFF2CC", "BB3838"
YT = "https://www.youtube.com/watch?v="
DR = "https://drive.google.com/file/d/%s/view"

AULAS = [
    # pág, rótulo PT, rótulo ES proposto, catálogo, link atual
    ("15", "Introdução ao raciocínio clínico de complicações agudas isquêmicas",
     "Introducción al razonamiento clínico de las complicaciones agudas isquémicas",
     "Intercorrências e emergências médicas · Complicações isquêmicas agudas", YT + "HW62ZM3NDC8"),
    ("29 (e 18, por erro)", "Revisão anatômica global da face: vascularização",
     "Revisión anatómica global de la cara: vascularización",
     "Não localizada no catálogo com este título · confirmar", YT + "2Qoh7fWG5w4"),
    ("32", "Hialuronidase", "Hialuronidasa",
     "Provável: Hialuronidase (módulo de toxina/preenchimento) · confirmar", YT + "zb0ZWo29Pk8"),
    ("35", "Rinomodelação: protocolo e manejo de complicações",
     "Rinomodelación: protocolo y manejo de complicaciones",
     "Intercorrências e emergências médicas · Complicações isquêmicas agudas", YT + "w7ZawtnNb2o"),
    ("37", "Mecanismos de segurança com cânulas", "Mecanismos de seguridad con cánulas",
     "Não localizada no catálogo com este título · confirmar", YT + "_yWZEknxYqo"),
    ("43", "Rinomodelação: agulha ou cânula?", "Rinomodelación: ¿aguja o cánula?",
     "Não localizada no catálogo com este título · confirmar", YT + "NCHkXFLKZds"),
    ("45", "Preenchimento full face guiado por ultrassom, ao vivo",
     "Relleno full face guiado por ecografía, en vivo",
     "Não localizada no catálogo com este título · confirmar", YT + "QocyeCsLs9M"),
    ("63", "Amaurose: protocolo de manejo das complicações",
     "Amaurosis: protocolo de manejo de las complicaciones",
     "Intercorrências e emergências médicas · Complicações isquêmicas agudas", YT + "GnGMUiPcoC0"),
    ("74", "Vídeo 9: complexo vascular nasoglabelar", "Video 9: complejo vascular nasoglabelar",
     "Não localizada no catálogo com este título · confirmar", YT + "YUirUEfaMjc"),
    ("79", "Vídeo 10: complicações agudas não isquêmicas (parte 1)",
     "Video 10: complicaciones agudas no isquémicas (parte 1)",
     "Intercorrências e emergências médicas · Complicações agudas não isquêmicas · confirmar", YT + "XzONB5671uY"),
    ("80", "Vídeo 11: complicações agudas não isquêmicas (parte 2)",
     "Video 11: complicaciones agudas no isquémicas (parte 2)",
     "Intercorrências e emergências médicas · Complicações agudas não isquêmicas · confirmar", YT + "dh26SwtfD2U"),
]

MOL, PAT, HIA = DR % "1tHj3C58l9NhqokvQBIisp-RO25MrDGfp", DR % "1F8aLFw8VV62JQngjfkHLNpHn2lr8jmjj", \
    DR % "19A8eYYAofI8Eiq4fIyk0kv-kJZf8aAvM"
ISQ_OLD, OFT_OLD = DR % "1WPpBXXtYISZ68Pf8ak2V2kKkPcLS_GuK", DR % "1k9pgxv8gf8-mBA-jTmHvmZ7dFqFcRbQs"
ISQ_NEW, OFT_NEW = DR % "1IQ-osnYyMdlCR511_SwOqVRdPjxqD3AI", DR % "1DLM3QIm8ui-37tXlv33AazCSiK57hIgP"
HDPH_NEW, DEL14_NEW = DR % "13rcR4MVX0frvJp3wgtFD1ko9IWQFiyco", DR % "1g2G9VADj6u5qsG5G1Zwqv_0kcow2-Zgb"

ATENCAO = ("ATENÇÃO: artigo com acesso restrito", "Abrir o arquivo no Drive > Compartilhar > Acesso geral: «Qualquer pessoa com o link», leitor. "
           "Não mexe na arte, vale para PT e ES.", "Keila (dona do arquivo)")
ARTIGO_ES = "Não traduz (artigo científico fica em inglês, link igual)"
VIDEO_ES = "Regerar QR para a aula dublada quando o link ES existir"

QRS = [
    # pág, tipo, conteúdo, link atual, situação no original, ação no original, quem, link proposto, ação na versão ES
    ("13", "Artigo", "Soares, Molecules 2022, «Bridging a Century-Old Problem»", MOL, *ATENCAO, MOL, ARTIGO_ES),
    ("15", "Vídeo", "Introdução ao raciocínio clínico de complicações agudas isquêmicas", YT + "HW62ZM3NDC8",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("18", "Artigo (QR aponta para vídeo)", "DeLorenzi, protocolo HDPH (hialuronidase pulsada em alta dose)",
     YT + "2Qoh7fWG5w4", "ERRO: o box promete o artigo HDPH e o QR abre o vídeo de vascularização da pág. 29",
     "Gerar QR novo para o artigo HDPH e substituir na arte", "André Vivas (arte) · equipe médica confirma o artigo",
     HDPH_NEW + " (CONFIRMADO: DeLorenzi, High Dose Pulsed Hyaluronidase · QR pronto: FEA-QR-pag18-HDPH-DeLorenzi)", "FEITO na versão ES: QR regerado para o artigo HDPH"),
    ("21", "Artigo", "«Patterns of Filler-Induced Facial Skin Ischemia» (FOEM, 243 casos)", PAT, *ATENCAO, PAT, ARTIGO_ES),
    ("23", "Artigo", "«Ischemic Complications of Dermal Fillers» (Plast Aesthet Res)", ISQ_OLD,
     "ERRO: arquivo não existe mais (mesmo link da pág. 61)", "Gerar QR novo e substituir na arte",
     "André Vivas (arte)", ISQ_NEW + " (CONFIRMADO: Mehta et al. 2022 · QR pronto: FEA-QR-pag23-e-61)", "FEITO na versão ES: QR regerado (exceto pág. 36, falta o arquivo)"),
    ("26", "Artigo", "«Patterns of Filler-Induced Facial Skin Ischemia» (2ª citação)", PAT, *ATENCAO, PAT, ARTIGO_ES),
    ("29", "Vídeo", "Revisão anatômica global da face: vascularização", YT + "2Qoh7fWG5w4",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("30", "Artigo", "Soares, Molecules 2022 (mecanismos moleculares)", MOL, *ATENCAO, MOL, ARTIGO_ES),
    ("32", "Vídeo", "Hialuronidase", YT + "zb0ZWo29Pk8", "OK", "Nenhuma", "", "", VIDEO_ES),
    ("33", "Artigo", "Revisão sobre hialuronidase", HIA, *ATENCAO, HIA, ARTIGO_ES),
    ("35", "Vídeo", "Rinomodelação: protocolo e manejo de complicações", YT + "w7ZawtnNb2o",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("36", "Artigo", "DeLorenzi 2014, consenso para oclusão vascular por AH (rinomodelação)", DR % "11p9QK_qVuG__8htGvDWr3wPImLY-Ovbp",
     "ERRO: arquivo não existe mais", "Gerar QR novo e substituir na arte", "André Vivas (arte)",
     "FALTA O ARQUIVO: o box cita «Consensus Guidelines for the Management of HA Filler-Induced Vascular Occlusion», que não está no Drive (o delorenzi2014 é outro artigo). Subir o PDF na pasta de artigos.", "FEITO na versão ES: QR regerado (exceto pág. 36, falta o arquivo)"),
    ("37", "Vídeo", "Mecanismos de segurança com cânulas", YT + "_yWZEknxYqo", "OK", "Nenhuma", "", "", VIDEO_ES),
    ("40", "Artigo", "Soares, Molecules 2022 (fisiopatologia e manejo)", MOL, *ATENCAO, MOL, ARTIGO_ES),
    ("43", "Vídeo", "Rinomodelação: agulha ou cânula?", YT + "NCHkXFLKZds", "OK", "Nenhuma", "", "", VIDEO_ES),
    ("45", "Vídeo", "Preenchimento full face guiado por ultrassom, ao vivo", YT + "QocyeCsLs9M",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("61", "Artigo", "«Ischemic Complications of Dermal Fillers»", ISQ_OLD,
     "ERRO: arquivo não existe mais (mesmo link da pág. 23)", "Gerar QR novo e substituir na arte",
     "André Vivas (arte)", ISQ_NEW + " (CONFIRMADO · QR pronto: FEA-QR-pag23-e-61)", "FEITO na versão ES: QR regerado (exceto pág. 36, falta o arquivo)"),
    ("63", "Vídeo", "Amaurose: protocolo de manejo das complicações", YT + "GnGMUiPcoC0",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("64", "Artigo", "Oclusão arterial oftálmica e retiniana (achados angiográficos)", OFT_OLD,
     "ERRO: arquivo não existe mais (mesmo link da pág. 68)", "Gerar QR novo e substituir na arte",
     "André Vivas (arte) · equipe médica confirma o artigo", OFT_NEW + " (CONFIRMADO: Kim et al., J Korean Med Sci 2015 · QR pronto: FEA-QR-pag64-e-68)",
     "FEITO na versão ES: QR regerado (exceto pág. 36, falta o arquivo)"),
    ("68", "Artigo", "Achados angiográficos cerebrais na oclusão da artéria oftálmica", OFT_OLD,
     "ERRO: arquivo não existe mais (mesmo link da pág. 64)", "Gerar QR novo e substituir na arte",
     "André Vivas (arte)",
     OFT_NEW + " (CONFIRMADO: mesmo artigo da pág. 64 · QR pronto: FEA-QR-pag64-e-68)", "FEITO na versão ES: QR regerado (exceto pág. 36, falta o arquivo)"),
    ("74", "Vídeo", "Vídeo 9: complexo vascular nasoglabelar", YT + "YUirUEfaMjc", "OK", "Nenhuma", "", "", VIDEO_ES),
    ("79", "Vídeo", "Vídeo 10: complicações agudas não isquêmicas (parte 1)", YT + "XzONB5671uY",
     "OK", "Nenhuma", "", "", VIDEO_ES),
    ("80", "Vídeo", "Vídeo 11: complicações agudas não isquêmicas (parte 2)", YT + "dh26SwtfD2U",
     "OK", "Nenhuma", "", "", VIDEO_ES),
]

DECISOES = [
    ("Aulas dubladas", "Confirmar se as 11 aulas serão dubladas e publicadas no YouTube como não listadas, como no ebook "
     "de olheiras (18 aulas). A produção das aulas é da FEA, fora do escopo da skill.", "Keila", "Não trava o PDF"),
    ("Corrigir os 6 QR com ERRO no PT", "Recomendação: corrigir o original PT (André) e eu aplico os mesmos destinos "
     "na versão ES. Os links propostos estão na aba «QR para ajustar».", "Keila + equipe médica", "Não trava o PDF"),
    ("Artigo da pág. 36", "Subir o PDF do «Consensus Guidelines for the Management of Hyaluronic Acid Filler-Induced Vascular Occlusion» citado no box. Não existe no Drive.", "Keila / equipe médica", "Só o QR da pág. 36"),
    ("Numeração dos vídeos", "Só os 3 últimos boxes têm número (Vídeo 9, 10 e 11). Padronizar no ES: todos numerados "
     "ou nenhum. Recomendação: numerar todos de 1 a 11.", "Keila", "Não trava o PDF"),
    ("Título do livro em espanhol", "Proposta: «Intercurrencias en el relleno con ácido hialurónico: diagnóstico y "
     "conductas clínicas ante complicaciones estéticas» (mantém «Intercurrencias», como na sigla ARTI do ebook de olheiras).",
     "Keila", "Não trava o PDF"),
    ("Autor · tempo de reperfusão capilar (pág. 27)", "O PT diz «redução do tempo de reperfusão capilar» como sinal de isquemia; o correto é aumento (lentificação), como na pág. 14. O ES espelhou o original.", "Dr. João / equipe médica", "Prioridade clínica"),
    ("Autor · dose da hialuronidase (págs. 31, 41, 50)", "«Injetar 1.000 UTR/mL» informa a concentração, não a dose nem o volume.", "Dr. João / equipe médica", "Prioridade clínica"),
    ("Autor · piperacilina", "4,5 g num capítulo e 3,375 g em outro.", "Equipe médica", "Prioridade clínica"),
    ("Autor · janela da retina", "Quatro números diferentes para a janela de tempo da retina (30 min, 90 min, 4 h, 12 h) ao longo do livro.", "Equipe médica", "Revisar PT e ES"),
    ("Autor · figuras com título repetido", "Fig. 5, 27, 31 (legenda copiada da 30), 36, 43 repetido nas 44 e 45, 62 (Tyndall).", "André Vivas + equipe médica", "Revisar PT e ES"),
    ("Linha vermelha 7 · imagens geradas por IA", "Figuras 37, 39, 41, 52, 53, 61 e 62 declaram imagem criada ou adaptada por IA; a 53 vem de «busca na internet» (direito de uso).", "Keila + Dr. João", "Decisão editorial"),
    ("Autor · conceitos técnicos", "Er:YAG listado como «não ablativo»; Tyndall explicado como «refração»/«sombra»; triamcinolona «diluída» sem concentração final.", "Equipe médica", "Revisar PT e ES"),
    ("Artigos científicos", "Pela regra da skill, os 12 QR de artigo (contando a pág. 18 corrigida) ficam em inglês e com o mesmo link na versão ES.",
     "Informativo", "Nenhum"),
]


def cabecalho(ws, colunas, larguras):
    ws.append(colunas)
    for i, w in enumerate(larguras, 1):
        c = ws.cell(row=ws.max_row, column=i)
        c.font, c.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor=ROXO)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = f"A{ws.max_row + 1}"


def quebra(ws, desde):
    for row in ws.iter_rows(min_row=desde):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")


def main(saida):
    wb = Workbook()
    n_videos = sum(1 for q in QRS if q[1] == "Vídeo")
    n_art = len(QRS) - n_videos
    n_erro = sum(1 for q in QRS if q[4].startswith("ERRO"))
    n_aten = sum(1 for q in QRS if q[4].startswith("ATENÇÃO"))

    ws = wb.active
    ws.title = "Resumo e prazo"
    ws.append(["Tradução ES · Livro «Intercorrências no Preenchimento com Ácido Hialurônico» · Dr. João Pithon"])
    ws["A1"].font = Font(bold=True, size=14, color=ROXO)
    ws.append(["PDF original de 01/10/2026, 221 páginas · skills fea-traduccion-es e fea-revision-es · "
               "mesmo processo do ebook de olheiras · atualizado em 05/10/2026"])
    ws.append([])
    cabecalho(ws, ["Indicador", "Total", "Leitura"], [42, 10, 110])
    for linha in [
        ("Páginas do livro", 221, "3x o ebook de olheiras (74 págs.). Todos os QR estão entre as págs. 13 e 80."),
        ("Palavras de texto corrido", "36.081",
         "Contagem exata da camada de texto do PDF (fora o texto embutido em arte: capa, aberturas e 4 figuras, também traduzidos)."),
        ("QR codes no livro", len(QRS), f"{n_videos + 1} apontam hoje para vídeo (um deles por erro, pág. 18) e {n_art - 1} para artigo científico."),
        ("Aulas únicas para versão em espanhol", len(AULAS),
         "11 QR de vídeo válidos para 11 aulas. O QR da pág. 18 aponta para vídeo por erro (deveria ser artigo)."),
        ("QR a regerar na versão ES (aulas)", n_videos,
         "Na entrega v1 os QR de aula abrem a aula em PT. Quando os links das aulas dubladas existirem: ~2 h de trabalho."),
        ("QR com ERRO no original", n_erro, "Págs. 18, 23, 36, 61, 64 e 68. Na versão ES, 5 já foram regerados com o destino confirmado; falta só a 36 (arquivo do artigo inexistente). O PT continua com o erro até o André trocar."),
        ("QR com ATENÇÃO (artigo restrito)", n_aten,
         "Págs. 13, 21, 26, 30, 33 e 40: basta liberar o compartilhamento de 3 arquivos, sem mexer na arte."),
        ("QR de artigo na versão ES", n_art, "11 de artigo + o da pág. 18 depois de corrigido. Artigo científico fica em inglês e com o mesmo link (corrigido, quando for o caso)."),
        ("Decisões pendentes", len(DECISOES), "Ver aba «Decisões pendentes»."),
    ]:
        ws.append(list(linha))
    ws.append([])
    linha_crono = ws.max_row + 1
    cabecalho(ws, ["Etapa", "Duração", "Previsão (a partir da liberação do PDF)"], [42, 10, 110])
    ws.freeze_panes = "A5"
    for linha in [
        ("0. Curadoria: OCR das 221 págs., texto em arte, QR decodificados", "feito", "05/10/2026"),
        ("1. Tradução em 3 passagens (tradução, auditoria por script, back-translation)", "feito", "05/10/2026"),
        ("2. PDF em espanhol no próprio arquivo (fontes, texto, arte, verificação)", "feito", "05/10/2026"),
        ("3. Revisão cega (fea-revision-es) e correções", "feito", "05/10/2026 · 6 partes LIBERADAS, zero achado clínico"),
        ("Entrega do PDF ES na pasta 0. PDF", "feito", "05/10/2026, com os QR de aula ainda em PT"),
        ("4. QR das aulas em espanhol", "~2 h", "Depois que a FEA preencher os links das aulas dubladas na aba «Aulas para traduzir»"),
    ]:
        ws.append(list(linha))
    quebra(ws, 5)

    wa = wb.create_sheet("Aulas para traduzir")
    cabecalho(wa, ["Nº", "Página(s)", "Rótulo PT (box «Na prática»)", "Rótulo ES proposto", "Aula no catálogo",
                   "Link atual (PT)", "Link ES (preencher)", "Marcador de tempo", "Status"],
              [5, 14, 42, 42, 40, 44, 34, 18, 16])
    for i, (pag, pt, es, cat, link) in enumerate(AULAS, 1):
        wa.append([i, pag, pt, es, cat, link, "", "", "pendente (aula dublada)"])
    quebra(wa, 2)

    wq = wb.create_sheet("QR para ajustar")
    cabecalho(wq, ["Página", "Tipo", "Conteúdo", "Link atual", "Situação no original", "Ação no original",
                   "Quem resolve", "Link correto (proposto)", "Ação na versão ES", "Status da correção"],
              [8, 14, 40, 44, 36, 36, 28, 46, 36, 16])
    for q in QRS:
        wq.append(list(q) + ["pendente" if q[4] != "OK" else "ok"])
    quebra(wq, 2)

    wd = wb.create_sheet("Decisões pendentes")
    cabecalho(wd, ["Assunto", "O que precisa ser decidido", "Quem decide", "Impacto no prazo", "Resposta"],
              [28, 90, 24, 22, 40])
    for d in DECISOES:
        wd.append(list(d) + [""])
    quebra(wd, 2)

    for w, col, n, opcoes in ((wa, "I", len(AULAS), "pendente,em produção,pronto"),
                              (wq, "J", len(QRS), "pendente,em correção,corrigido e testado,ok")):
        status = DataValidation(type="list", formula1=f'"{opcoes}"')
        w.add_data_validation(status)
        status.add(f"{col}2:{col}{n + 1}")
    amarelo = PatternFill("solid", fgColor=AMARELO)
    for w, cols, n in ((wa, "GHI", len(AULAS)), (wq, "J", len(QRS)), (wd, "E", len(DECISOES))):
        for col in cols:
            for r in range(2, n + 2):
                w[f"{col}{r}"].fill = amarelo
    vermelho, lavanda = Font(bold=True, color=VERMELHO), PatternFill("solid", fgColor=LAVANDA)
    for r in range(2, len(QRS) + 2):
        if wq[f"E{r}"].value.startswith("ERRO"):
            wq[f"E{r}"].font = vermelho
        if wq[f"B{r}"].value == "Vídeo":
            wq[f"I{r}"].fill = lavanda
    wb.save(saida)
    print(saida, "·", len(AULAS), "aulas ·", len(QRS), "QR ·", n_erro, "erro ·", n_aten, "atenção")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "FEA-Traducao-ES-Intercorrencias-Aulas-e-QR.xlsx")
