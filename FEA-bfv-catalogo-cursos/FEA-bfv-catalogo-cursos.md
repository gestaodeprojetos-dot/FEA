# FEA · BFV 2026, catálogo de cursos animado

Vídeo 16:9 no estilo da referência (vídeo do Drive, aos 1:38:14): carrossel 3D com as capas do slide 11. Em cada curso com vídeo, a capa vai para a lateral e abre uma janela com trecho da aula, o tipo do curso, o número e o nome. Os cursos sem vídeo aparecem com a capa em destaque e o nome. No final, as capas se encaixam na vitrine do slide 11.

- **Identidade:** Black Friday Vitalícia (preto, dourado, ondas douradas, logo BFV), fontes Sora e Montserrat.
- **Capas:** recortadas do slide 11 da apresentação "BFV 2026 · Slides da live 19-10".
- **Trechos das aulas:** gravações de tela da plataforma feitas pela Keila em 20/10/2026, recortadas na área do player.

## Situação dos cursos

- **Arquivo:** `FEA-bfv-catalogo-cursos-16x9.mp4`, 1920x1080, 30 fps, 95 s, sem áudio.
- Os **19 itens** têm vídeo: 17 cursos com trecho de aula e 2 ebooks com as páginas rolando. O "+ Novos cursos" fecha o carrossel antes da vitrine final.
- Os trechos foram escolhidos pelo `fea_melhor_trecho.py`, que analisa quadro a quadro e só aceita janelas com movimento contínuo: sem carregamento, sem tela parada e sem corte para menus. Depois foram conferidos visualmente.
- As fontes são 6 gravações de tela feitas pela Keila em 20/10/2026, da plataforma e do Drive com as aulas editadas.

## Fonte

- `fonte/FEA-bfv-catalogo.html`: a animação. A lista `COURSES` define o título, o tipo e o clipe de cada curso. Os tempos (`STEP`, `OPEN`, `CLOSE`, `CLIP_MAX`) ficam logo abaixo.
- `fonte/frames.js`: número de quadros de cada clipe.
- `fonte/render_par.js`: renderização em 4 processos paralelos (`node render_par.js 30 saida.mp4 4`).
- `fonte/fea_melhor_trecho.py`: acha a melhor janela de N segundos num intervalo da gravação (`CROP` define a área do player).
- `fonte/fea_sheets.sh`: gera uma folha com 8 quadros de um vídeo do Drive, para escolher os trechos.

Os quadros dos clipes (`seq/`) e as capas não ficam no repositório, por causa do tamanho. Eles são gerados a partir das gravações.
