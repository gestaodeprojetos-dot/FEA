---
name: fea-animacao-video
description: Cria vídeos e slides animados para a FEA e o Dr. João Pithon (teasers de app, catálogos de cursos, slides de pitch, animações de logo e pilares, painel de LED, Reels), com animação em HTML/GSAP renderizada quadro a quadro, som sincronizado e entrega pronta para PowerPoint, Drive e celular. Usar quando pedirem para animar slide, arte, logo ou apresentação, fazer teaser, vídeo de catálogo, versão Reels ou LED, colocar som ou efeito sonoro em animação, ou animar o deck pronto do designer.
---

# FEA · Animação de vídeo e slides

Método usado nos vídeos da FEA (teaser do Reology Map, catálogo de cursos da BFV, slides da Elite Mentoring, pitch animado do designer, pilares Elite Experience). A animação é uma página HTML com uma linha do tempo GSAP; um navegador sem tela fotografa cada quadro e o ffmpeg monta o MP4. Assim o resultado é exato, repetível e editável.

## 1. Antes de começar

1. Confirmar **o que é a peça, onde vai rodar e o formato**: telão (16:9), Reels/Stories (9:16), painel de LED (dimensão exata em px), PowerPoint (um vídeo por clique) ou celular.
2. Pegar a **identidade certa**. A FEA tem mais de uma (ver CLAUDE.md do projeto). Elite Mentoring: fundo `#011A24`, turquesa `#2DB9B3`/`#62B9B4`, ciano `#86F9F8`, Canela Deck + Galano Grotesque. Elite Experience (pilares): fundo rosa `#FFE2E9`, vinho `#9A2449`. Na dúvida, perguntar.
3. Se já existe arte do designer (vídeo, PPTX, PNG), **reproduzir o visual dela**: medir posições e cores num quadro em tamanho real antes de animar. Nunca inventar uma identidade nova por cima.
4. Fontes: a Canela Deck da pasta da marca é versão **Trial** (não comercial). Avisar e pedir a licença antes de peça pública.
5. Nada de imagem gerada por IA em entregável final (linha vermelha FEA).

## 2. O contrato da página de animação

Toda animação é um HTML que expõe:

```js
window.DURATION = 12;                 // segundos
window.seek = (t) => { tl.seek(t, false); desenharCanvas(t); };
window.ready = Promise.all([...document.images].map(i => i.decode().catch(() => {})));
window.STEPS = [2.2, 3.5, 4.9];       // opcional: fim de cada clique (PowerPoint)
window.LOOP = [3, 11];                // opcional: trecho que fecha em loop
```

Regras que evitam retrabalho:
- Tudo depende só de `t` (partículas com semente fixa, nada de `Math.random()` solto, nada de `requestAnimationFrame`). Para loops, usar movimentos com período exato.
- Quebrar texto em palavras só em espaço normal (`/[ \t\n]+/`), para respeitar `&nbsp;` em "R$&nbsp;300&nbsp;mil".
- Ao mudar de layout (16:9 → 9:16 → LED), **recalcular coordenadas de cursor e alvos** a partir da nova origem da transformação (`transform-origin`).
- Modelo pronto: `templates/FEA-template-animacao.html`.

## 3. Renderizar

```bash
# prévia de quadros soltos (conferir antes de renderizar tudo)
HTML=minha.html VW=1920 VH=1080 node scripts/fea_render.js preview 1,3.5,6
# vídeo completo, 4 processos em paralelo
HTML=minha.html VW=1920 VH=1080 FPS=30 node scripts/fea_render.js video saida.mp4 4
```

- **Painel de LED / resoluções enormes**: desenhar na metade do tamanho e usar `DPR=2` (ex.: 2016x672 com DPR 2 = 4032x1344). Fica nítido e leve de montar.
- **Reels 9:16**: texto no alto, conteúdo embaixo, aviso legal acima de ~330 px do rodapé (área coberta pelos botões do Instagram).
- Sempre montar uma **folha de contato** (quadros-chave lado a lado) e olhar antes de entregar.

## 4. PowerPoint: um vídeo por clique

Quem conduz o tempo é o palestrante. Para slides com várias entradas:

```bash
python3 scripts/fea_cortar_cliques.py minha.html saida/ 30
```

Gera `-clique-1.mp4`, `-clique-2.mp4`… (cada um começa onde o anterior parou), `-loop.mp4` se houver `LOOP` e um `-final.png` de reserva. No PowerPoint: um slide por vídeo, **Reprodução › Iniciar: Automaticamente**, **desmarcar "Retroceder após a reprodução"**, transição **Nenhuma**. Loop: segundo vídeo no mesmo slide com "Iniciar após anterior" + "Repetir até ser interrompido".

Contador ao vivo ("Restam X vagas") e QR code ficam **estáticos** no PowerPoint, nunca em vídeo.

## 5. Animar o deck pronto do designer (slides em imagem)

Quando o designer entrega um PPTX em que cada slide é uma imagem e as entradas viraram slides seguidos:

```bash
python3 scripts/fea_animar_deck.py pasta_imagens/ pasta_videos/          # usa o PLAN do script
python3 scripts/fea_montar_pptx.py original.pptx pasta_videos/ pasta_imagens/ "Nome · ANIMADO.pptx"
```

- Extrair as imagens dos slides (`ppt/media` via relações de cada slide, salvas como `s001.jpg`, `s002.jpg`…) e medir a diferença entre slides seguidos: diferença pequena = entrada de elemento; grande = virada de tela.
- **Editar o dicionário `PLAN` no topo de `fea_animar_deck.py`** para o deck novo (número do slide de destino → estilo). O que está lá é o mapa do pitch Elite Mentoring de 129 slides.
- Estilos: `up` (pilares e barras sobem com linha de luz), `left` (itens de lista), `rise` (cartões), `pop`, `wipe` (linhas de recibo), `flash` (datas, preços, "Tem mais"), `push` (imagens de impacto), `scan` (abertura).
- **Conferir que cada vídeo começa idêntico ao slide anterior e termina idêntico ao slide do designer** (`scripts/fea_conferir.py`). Um erro já cometido: o flash começava clareado no quadro 0 e dava pulo no clique.
- **Nunca alterar o arquivo do designer**: gerar arquivo novo, em pasta separada, com o mesmo nome + "ANIMADO".
- Google Apresentações remove vídeos embutidos na conversão: para vídeo no telão, usar PowerPoint.

## 6. Som

Preferência registrada da Keila (nov/2026): **suave, sofisticado, sem exagero, sem som em tudo**. Som só no movimento principal (o que encaixa, o que é revelado); palavras e textos sem som.

1. **Primeira opção: biblioteca do HeyGen** (`search_audio_sounds`, `type: sound_effects`). Devolve `audio_url`, `duration` e `peak_offset`. Combinação aprovada para os pilares Elite: "Short airy whoosh" em cada encaixe + "Ethereal metallic chime" na revelação. Para anúncio pago, confirmar a licença do plano.
2. Alinhar pelo pico: começar cada efeito em `momento_do_movimento - peak_offset`. Mixar com `scripts/fea_som_mix.py cues.json saida.wav` (volume em dB, pan, passa-baixa opcional) e normalizar em torno de **-21 LUFS** para efeitos, -14 LUFS para trilha musical.
3. Síntese própria (numpy) só como plano B. Testes que **não agradaram**: sopro de ruído + toque grave, piano com acorde, clique metálico de encaixe, toques muito discretos de sino. Trilha musical sintetizada funcionou bem em teaser longo (120 BPM, cortes no tempo forte).
4. Conferir o tempo dos picos medindo o volume a cada 0,1 s antes de juntar ao vídeo.
5. Juntar: `ffmpeg -i video.mp4 -i som.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest final.mp4`.

## 7. Trechos de aula em vídeo (catálogos)

Para catálogos com aula passando dentro da janela, escolher trechos em que **a aula está acontecendo**, sem carregamento, vídeo parado ou menu:

```bash
CROP=810,300,28,262 python3 scripts/fea_melhor_trecho.py gravacao.mp4 inicio fim duracao
```

Ele analisa quadro a quadro e só aceita janelas com movimento contínuo. Depois extrair a sequência de imagens do trecho e trocá-las dentro da página a cada quadro.

## 8. Arquivos desta skill

| Arquivo | Para que serve |
|---|---|
| `scripts/fea_render.js` | Prévia de quadros e vídeo completo em paralelo (VW, VH, DPR, FPS, HTML) |
| `scripts/fea_cortar_cliques.py` | Um vídeo por clique + loop + PNG final, para PowerPoint |
| `scripts/fea_animar_deck.py` | Anima a passagem entre slides seguidos de um deck em imagem |
| `scripts/fea_montar_pptx.py` | Embute os vídeos num PPTX novo, tocando sozinhos e parando no último quadro |
| `scripts/fea_som_mix.py` | Mixa efeitos sonoros pelos picos, a partir de um `cues.json` |
| `scripts/fea_conferir.py` | Folha de contato, emenda de quadros e picos de som |
| `scripts/fea_melhor_trecho.py` | Acha o melhor trecho de uma gravação de aula |
| `templates/FEA-template-animacao.html` | Modelo com o contrato pronto (cliques, loop, partículas, texto) |
| `exemplos/FEA-exemplo-pilares-elite.html` | Exemplo real: círculos descendo, palavras escritas, Elite revelado |

Dependências: Node com Playwright (Chromium), ffmpeg, Python com numpy, scipy, Pillow e python-pptx.

## 9. Entrega

- **Drive**: subir com a API (token via `FEA_GDRIVE_*` no ambiente), upload resumável, e **conferir tamanho/MD5** depois. Só subir quando pedirem e na pasta que pedirem; arquivo do designer nunca é substituído.
- **Visualizador no navegador** (para a equipe ver no celular): carregar cada vídeo com `fetch` → `blob:` (o iPhone não toca vídeo de servidor sem Range), versão leve 720p/30 fps perfil Main, botão "Tocar" se o autoplay for bloqueado, e lista marcando o que é animado, a fazer e estático.
- Vídeo de LED muito largo não toca no celular nem na prévia do Drive: mandar também uma **prévia leve** (ex.: 1920x640) e orientar o técnico a baixar o original.
- Salvar fonte (HTML, scripts) no repositório com prefixo `FEA-`/`fea_`.

## 10. Checklist final

- [ ] Quadros-chave conferidos numa folha de contato
- [ ] Primeiro e último quadro batem com os slides vizinhos (quando é build)
- [ ] Cursor e cliques caem no alvo certo
- [ ] Som com picos no tempo certo, volume suave
- [ ] Preços, datas e nomes iguais à arte mais recente (já houve divergência de preço entre copy e arte final)
- [ ] Arquivo do designer intacto; entrega em pasta própria
- [ ] Português, sem travessão, sem "pra"
