# FEA · Contagem regressiva Elite Injectors Congress

Evento: **01 e 02 de novembro de 2026 · WTC Sheraton, São Paulo**
Base de copy: doc "3. Copy de criativos de lembrete - Elite Injectors Congress".

Cada dia tem 4 arquivos: feed (1080x1350) e stories (1080x1920), cada um em **PNG** (imagem) e **MP4** (vídeo de 10 s com trilha).
Os arquivos ficam em `output/feed/` e `output/stories/`, nomeados pela data de postagem.

| Data | Arte | Legenda sugerida (feed) |
|------|------|-------------------------|
| 21/10 | Faltam 11 dias | Faltam 11 dias para o Elite Injectors Congress. Dois dias de imersão presencial sobre tendências globais, evidências reais e aplicação clínica, no WTC Sheraton, São Paulo. Toque no link da bio e confira os detalhes da sua inscrição. |
| 22/10 | Faltam 10 dias | Faltam 10 dias. Separe os dias 01 e 02 de novembro na agenda: o Elite Injectors Congress está chegando. Toque no link da bio e garanta a sua vaga. |
| 23/10 | Faltam 9 dias | Faltam 9 dias para reunir evidência científica e aplicação clínica no mesmo palco. Elite Injectors Congress · 01 e 02 de novembro · WTC Sheraton, São Paulo. |
| 24/10 | Faltam 8 dias | Faltam 8 dias. Já planejou sua chegada ao WTC Sheraton, em São Paulo? Toque no link da bio e confira os detalhes. |
| 25/10 | Faltam 7 dias | Faltam 7 dias. Comece a se organizar: ✔ confirme sua inscrição ✔ separe os dias 01 e 02 de novembro na agenda ✔ planeje sua chegada ao WTC Sheraton, São Paulo. |
| 26/10 | Faltam 6 dias | Faltam 6 dias para o Elite Injectors Congress. Toque no link da bio e confira tudo o que você vai viver nos dias 01 e 02 de novembro. |
| 27/10 | Faltam 5 dias | Faltam 5 dias. Já convidou um colega para viver essa experiência com você? Elite Injectors Congress · 01 e 02 de novembro · WTC Sheraton, São Paulo. |
| 28/10 | Faltam 4 dias | Faltam 4 dias para dois dias que podem mudar a sua prática profissional. Toque no link da bio e confira os detalhes. |
| 29/10 | Faltam 3 dias | Faltam 3 dias para o Elite Injectors Congress. Toque no link da bio e revise as informações do seu ingresso. |
| 30/10 | Faltam 2 dias | Faltam 2 dias. O Elite Injectors Congress está quase aí. Toque no link da bio e confira os últimos detalhes. |
| 31/10 | Falta 1 dia | É amanhã! O que levar: ✔ seu ingresso (Passaporte Elite ou Elite VIP) ✔ documento com foto ✔ vontade de aprender com evidência. Nos vemos no WTC Sheraton, São Paulo. |
| 01/11 | É hoje | É hoje! O Elite Injectors Congress começa agora, no WTC Sheraton, São Paulo. Nos vemos lá. |

## Observações de uso

- **Trilha:** original, sintetizada para este projeto (sem direito autoral de terceiros), sincronizada com a animação: tique-taque, impacto quando o número entra (2 s) e segundo impacto na logo (4,6 s). Para ganhar alcance orgânico no Reels, dá para trocar por um áudio da biblioteca do Instagram mantendo o vídeo.
- **Stories:** o texto respeita as zonas seguras (topo 250 px e base 270 px livres para a interface do Instagram e o sticker de link).
- **Fontes:** Canela Deck e Galano Grotesque vêm da pasta de identidade do congresso. A Canela na pasta é versão *Trial*: para anúncio pago, confirmar com o designer se a licença comercial foi adquirida.
- **Reeditar uma peça:** `src/FEA-contagem.html` (textos em `TAGS`), depois `python3 src/fea_trilha.py` e `node src/fea_render.js --days 5 --fmt feed` com um servidor local na pasta `src` (`python3 -m http.server 8765`). As fontes não vão para o Git, baixar da pasta 03 - TIPOGRAFIA do Drive para `src/assets/`.
