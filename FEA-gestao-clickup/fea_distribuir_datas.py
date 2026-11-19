"""FEA: distribui datas de um lançamento novo pelo padrão D-menos.

Lê a exportação das tarefas abertas do lançamento (CSV) e a tabela FEA-padrao-d-menos.csv,
e gera a proposta de datas e de sprint de cada tarefa.

Uso:
  python3 fea_distribuir_datas.py tarefas.csv --captacao 2026-10-27 --evento 2026-11-10 \
      [--hoje 2026-10-20] [--saida FEA-proposta-datas.csv]

O CSV de entrada precisa das colunas: id, name, parent_name, status, assignees, due_date.

Duas réguas:
  captacao: tarefas que montam a captação contam a partir do início da captação;
  evento:   setup, vendas e reta final contam a partir da live ou evento.
Prazo que cai no fim de semana vai para a sexta anterior.
Prazo que o padrão coloca antes de hoje vira "recuperar" com prazo amanhã.
"""
import argparse
import csv
import datetime as dt
import os
import re

PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FEA-padrao-d-menos.csv")


def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()


def carregar_padrao():
    pad = {}
    for r in csv.DictReader(open(PADRAO, encoding="utf-8")):
        pad[norm(r["tarefa"])] = (r["regua"], int(r["dias_da_regua"]))
    return pad


def achar(nome, pad):
    n = norm(nome)
    if n in pad:
        return pad[n]
    for k, v in pad.items():
        if n[:25] in k or k[:25] in n:
            return v
    return None


def dia_util_anterior(d):
    while d.weekday() > 4:
        d -= dt.timedelta(days=1)
    return d


def segunda(d):
    return d - dt.timedelta(days=d.weekday())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tarefas")
    ap.add_argument("--captacao", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--evento", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--hoje", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--saida", default="FEA-proposta-datas.csv")
    a = ap.parse_args()

    pad = carregar_padrao()
    amanha = a.hoje + dt.timedelta(days=1)
    while amanha.weekday() > 4:
        amanha += dt.timedelta(days=1)
    linhas = []
    for r in csv.DictReader(open(a.tarefas, encoding="utf-8")):
        if r["status"] in ("feito", "complete", "concluído"):
            continue
        achado = achar(r["name"], pad)
        if achado is None:
            linhas.append([r["id"], r["name"], r.get("parent_name", ""), r.get("assignees", ""),
                           r.get("due_date", ""), "", "", "", "SEM PAR: decidir pela corrente"])
            continue
        regua, dias = achado
        base = a.captacao if regua == "captacao" else a.evento
        prazo = dia_util_anterior(base + dt.timedelta(days=dias))
        nota = ""
        if prazo < a.hoje:
            nota, prazo = "RECUPERAR: o padrão já passou", amanha
        sprint = segunda(prazo).isoformat()
        linhas.append([r["id"], r["name"], r.get("parent_name", ""), r.get("assignees", ""),
                       r.get("due_date", ""), f"{regua} {dias:+d}", prazo.isoformat(), sprint, nota])

    linhas.sort(key=lambda x: (x[6] or "9999", x[2]))
    with open(a.saida, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "tarefa", "area", "responsavel", "prazo_atual", "regra",
                    "prazo_proposto", "sprint_semana_de", "observacao"])
        w.writerows(linhas)
    sem_par = sum(1 for x in linhas if x[8].startswith("SEM PAR"))
    recuperar = sum(1 for x in linhas if x[8].startswith("RECUPERAR"))
    print(f"{len(linhas)} tarefas | {recuperar} para recuperar | {sem_par} sem par | saída: {a.saida}")


if __name__ == "__main__":
    main()
