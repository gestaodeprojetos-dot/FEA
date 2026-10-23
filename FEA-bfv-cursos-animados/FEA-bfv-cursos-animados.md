# FEA · BFV 2026, vitrine de cursos animada (slide 11)

Versão animada do slide 11 da apresentação "BFV 2026 · Slides da live 19-10" (vitrine com 19 cursos e o card "+ Novos cursos"), para inserir na apresentação no lugar da imagem estática.

- **Arquivo:** `FEA-bfv-cursos-animados-16x9.mp4` (1920x1080, 60 fps, 24 s, sem áudio)
- **Identidade:** a da campanha Black Friday Vitalícia, com fundo preto e marrom, ondas douradas e o logo BFV, igual ao slide original.

## Sequência

| Tempo | O que acontece |
|---|---|
| 0 a 1,6s | Fundo surge do preto, ondas douradas começam a se expandir, logo BFV entra e o carrossel desliza da direita |
| 1,6 a 15,3s | **Uma capa por vez** passa pelo centro, na ordem do slide: FEP, Especialista em Botox, Fios, Corporal, Escultura Labial, FEAnatomy, FEBio, Complicações, Rinomodelação, Olheiras, Preenchimento Labial, PLX, Full Face (2), Atenda todo Santo dia, CPX, CTX, Preenchimento Tridimensional de Olheiras, Intercorrências e, por último, + Novos cursos. A capa da vez fica grande, iluminada, com moldura e brilho dourados; as outras ficam em fila, inclinadas e escurecidas dos lados, com reflexo no chão. Cerca de 0,7s por capa. |
| 16,3 a 18,6s | Todas as capas voam até a posição exata no slide e se juntam na vitrine, com um clarão dourado ao encaixar |
| 18,9 a 20,3s | Uma varredura de luz percorre a vitrine da esquerda para a direita |
| 19,2s em diante | O contorno tracejado do card "+ Novos cursos" passa a andar e pulsar |
| até 24s | A vitrine fica parada, com as ondas se movendo devagar |

O último quadro reproduz a composição do slide original. Assim, se o vídeo parar no fim, a tela continua igual ao slide.

## Como usar no Google Apresentações

1. Suba o MP4 no Drive.
2. Vá ao slide 11 e use Inserir > Vídeo > Google Drive.
3. Estique o vídeo para ocupar o slide inteiro.
4. Em Opções de formatação > Reprodução de vídeo, escolha "Reproduzir (automaticamente)".

## Fonte

As capas foram recortadas da imagem do próprio slide (não há capas individuais na apresentação) e ampliadas 2x. O fundo foi redesenhado em código no mesmo estilo, porque apagar os cards da imagem original deixava marcas visíveis.

Para editar: `fonte/FEA-bfv-cursos.html` (o tempo por capa fica em `STEP`, o tamanho da capa em destaque em `FOCUS_SCALE` e o início da montagem em `T0`). Para renderizar de novo: `HTML=FEA-bfv-cursos.html node fea_render.js video 60 saida.mp4`.
