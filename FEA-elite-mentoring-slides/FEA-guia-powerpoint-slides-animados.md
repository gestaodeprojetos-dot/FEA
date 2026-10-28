# FEA · Elite Mentoring · Slides animados para o PowerPoint

Vídeos animados de 19 slides do pitch da Elite Mentoring no Elite Injectors Congress (01 e 02/11/2026). A numeração é a da copy dos 78 slides. Todos os vídeos estão em 1920x1080, 60 fps, MP4 (H.264), sem áudio, com a identidade do KV: fundo `#011A24`, turquesa `#2DB9B3` / `#62B9B4`, ciano `#86F9F8`, Canela Deck e Galano Grotesque.

## Como funciona

O Dr. João conduz o tempo com o passador. Por isso cada slide com mais de um clique foi cortado em **um vídeo por clique**: `FEA-elite-slide-10-clique-1.mp4`, `-clique-2.mp4` e assim por diante. Cada vídeo começa exatamente onde o anterior terminou e para no último quadro, esperando o próximo clique. Na tela, a sequência parece uma animação só.

## Como montar no PowerPoint (por vídeo)

1. Crie **um slide do PowerPoint para cada vídeo** (o slide 10, que tem 5 cliques, vira 5 slides seguidos).
2. **Inserir › Vídeo › Este dispositivo** e escolha o arquivo.
3. Com o vídeo selecionado, em **Formato do vídeo › Tamanho**, deixe 33,867 x 19,05 cm (a tela inteira), posição 0 e 0.
4. Na guia **Reprodução**:
   - **Iniciar: Automaticamente**;
   - **desmarque "Retroceder após a reprodução"**, para o vídeo ficar parado no último quadro;
   - deixe "Ocultar quando não estiver em execução" e "Reproduzir em tela inteira" desmarcados.
5. Em **Transições**, use **Nenhuma** entre os slides de um mesmo bloco. Qualquer transição mostra um corte entre um clique e outro.
6. Clicar no passador avança para o slide seguinte, e o próximo vídeo começa sozinho.

## Slides com loop (15, 27 e 67)

O portal (15 e 27) e o "Bem-vinda, Clínica Elite" (67) têm um vídeo de entrada e um vídeo de loop, que fica girando enquanto o Dr. João fala (no 67, durante toda a fila no palco).

1. No mesmo slide do PowerPoint, insira primeiro o vídeo de entrada e depois o `-loop.mp4`, um em cima do outro e do mesmo tamanho.
2. Vídeo de entrada: **Iniciar: Automaticamente**.
3. Vídeo de loop: abra **Animações › Painel de animação**, clique no loop e escolha **Iniciar após anterior**. Em **Reprodução**, marque **Repetir até ser interrompido**.

O loop fecha sem salto: o último quadro emenda no primeiro.

## Lista de arquivos

| Slide da copy | Conteúdo | Vídeos |
|---|---|---|
| 02 | Raio-X da Clínica Elite (scanner) | 1 |
| 03 | 4 pilares subindo | 1 |
| 09 | Pilares com o campo da nota | 1 |
| 10 | Diagnóstico: as 4 faixas acendem | 5 cliques (título + 1 por faixa) |
| 12 | 3 passos com seta | 3 cliques |
| 13 | 3 degraus | 1 |
| 14 | 1h, depois "Sim. Feita do jeito certo." | 2 cliques |
| 15 | Portal: "Vamos voltar no tempo" | entrada + loop |
| 19 | Equação rostos = vidas = clínica | 1 |
| 27 | Portal: "Vamos voltar ao presente" | entrada + loop |
| 28 | Os 6 sins | 7 cliques (título + 1 por pergunta) |
| 46 | Quanto vale? (recibo até R$ 70.000) | 7 cliques (recibo + 5 itens + total) |
| 49 | Tem mais (usar também nos slides 52, 55, 57, 61 e 63) | 1 |
| 54 | Desafio Clínica Elite, R$ 300 mil | 1 |
| 58 | Segunda cadeira de graça | 1 |
| 59 | Por apenas R$ 35.000 (usar também no 48) | 1 |
| 60 | Revelação: R$ 25.000 | 1 |
| 62 | Garantia de 7 dias | 1 |
| 67 | Bem-vinda, Clínica Elite | entrada + loop |

Cada slide tem também um `-final.png` com o último quadro, para usar como capa do vídeo ou como reserva se o vídeo falhar no notebook do evento.

## Regras da copy aplicadas

- A marca Elite Mentoring só aparece a partir da oferta (slides 46 em diante). Antes disso, só as cores, sem logo nem monograma.
- Rodapé obrigatório "Os resultados dependem da implementação de cada aluno." nos slides de oferta (46, 54, 58, 59, 60, 62).
- Números grandes em azul-piscina e itens de lista entrando um a um.

## Pendências

- **Fonte Canela Deck:** a pasta "03 - TIPOGRAFIA" só tem a versão **Trial**, que não permite uso comercial. Confirmar com o designer se a licença foi comprada.
- **Dependem de material:** 23 (linha do tempo), 24 e 25 (datas com raio verde e vermelho), 37 (mentores com foto), 47 (cursos em cards, reaproveitando o carrossel da Black Friday), 71 (antes e hoje).
- **Fora dos vídeos de propósito:** QR codes e o contador "Restam X de 80 vagas" ficam estáticos no PowerPoint, para o time editar ao vivo.
- **Teste no local:** rodar a apresentação inteira no notebook do evento antes, de preferência com os vídeos incorporados ao arquivo (PowerPoint › Arquivo › Informações › Otimizar compatibilidade de mídia).

## Fonte (`fonte/`)

- `FEA-elite-slides.html`: todos os slides; cada um é escolhido por `?s=10`. `window.STEPS` marca o fim de cada clique e `window.LOOP` o trecho de loop.
- `fea_render_slides.py`: renderiza a 60 fps, corta um MP4 por clique, o loop e o PNG final (`python3 fea_render_slides.py saida 02 03 10`).
