#!/usr/bin/env python3
"""Gera os lotes (task.create_many) a partir do plano: grupos primeiro, depois as tarefas filhas."""
import json, sys
from datetime import date, datetime, timedelta, timezone
BRT = timezone(timedelta(hours=-3))
SPRINT = {"S1": ("2026-10-22", "2026-10-30"), "S2": ("2026-11-02", "2026-11-06"), "S3": ("2026-11-09", "2026-11-13")}


def ms(iso): return int(datetime.combine(date.fromisoformat(iso), datetime.min.time(), BRT).timestamp() * 1000)


p = json.load(open("FEA-plano-clickup-mtb-1126.json"))
# slides do evento: prontos na sexta anterior à aula
for s, gs in list(p["plano"].items()):
    for g, fs in gs.items():
        for f in list(fs):
            if f["ref"] == "86ahtp3vk":
                fs.remove(f); f.update(inicio="2026-11-02", fim="2026-11-06", sprint="S2")
                p["plano"]["S2"].setdefault("Design", []).append(f)
json.dump(p, open("FEA-plano-clickup-mtb-1126.json", "w"), ensure_ascii=False, indent=1)

modo = sys.argv[1]
if modo == "grupos":
    for s, gs in sorted(p["plano"].items()):
        tarefas = []
        for g, fs in gs.items():
            ini = min([f["inicio"] for f in fs] or [SPRINT[s][0]]); fim = max([f["fim"] for f in fs] or [SPRINT[s][1]])
            tarefas.append({"name": g, "start_date": ms(ini), "due_date": ms(fim), "due_date_time": False,
                            "description": f"Grupo de tarefas de {g} da sprint {s} do MTB 11/26."})
        print(s, p["listas"][s], json.dumps({"tasks": tarefas}, ensure_ascii=False))
elif modo == "filhas":
    grupos = json.load(open("FEA-grupos-clickup-mtb-1126.json"))  # {"S1|Design": id}
    s = sys.argv[2]
    tarefas = [{"name": f["nome"], "parent_task_id": grupos[f"{s}|{g}"], "start_date": ms(f["inicio"]),
                "due_date": ms(f["fim"]), "due_date_time": False, "description": f["descricao"]}
               for g, fs in p["plano"][s].items() for f in sorted(fs, key=lambda x: x["fim"])]
    json.dump({"tasks": tarefas}, open(f"/tmp/claude-0/-home-user-FEA/ce2ef478-67a4-5284-b1d6-9d4c8f98649b/scratchpad/lote_{s}.json", "w"), ensure_ascii=False)
    print(len(tarefas))
