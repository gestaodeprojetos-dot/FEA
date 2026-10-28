# FEA: edição LATAM Black Friday Total

Scripts da edição dos criativos em espanhol da Black Friday Total (LATAM), no estilo dos criativos do Elite Injectors Congress.

| Arquivo | Para quê |
|---|---|
| `fea_bft_edit.py` | Motor: legenda em caixa alta com palavra dourada, card do topo com a logo, telas cheias (checklist, número de clases, data do en vivo, arte Combo Total), botão "MÁS INFORMACIÓN" e cartela final |
| `fea_bft_plan.py` | Monta o spec a partir das palavras em espanhol (posiciona cards, telas cheias e botão pelo que o Dr. fala) |
| `fea_dinamico.py` | Corte dinâmico: remove as pausas acima de 0,12 s do vídeo dublado e remapeia os tempos das palavras |
| `fea_align.py` | Alinha o roteiro em espanhol revisado aos tempos do Whisper (legenda com o texto exato) |
| `fea_endcard.py` | Gera a cartela final padrão: logo Black Friday Total com impacto + "Toca en Más información" digitado com som de teclado |
| `assets/` | Logo, arte Combo Total (oficial, do Drive da campanha), fontes Montserrat, cartela final e som do finalzinho padrão |

Fluxo: roteiro ES revisado (SRT com tempos do PT) → HeyGen `precision`, "Spanish (Latin America)", `srt_role=output`, `enable_dynamic_duration=false` → Whisper ES + `fea_align.py` → `fea_dinamico.py` (sem silêncio) → `fea_bft_plan.py` → `fea_bft_edit.py`.

Regras de acabamento (Keila, 26/10/2026): sem silêncio no vídeo, legenda sempre do mesmo tamanho e sem zoom, render no fps original do HeyGen (25 fps).
