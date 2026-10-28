# FEA · Teaser do app Reology Map (v2)

Teaser de 40 segundos do app **Reology Map** (reology.joaopithon.com.br), no formato do vídeo do ProHarmony Atlas mostrado aos 56:25 da referência: motion design sobre gravações reais do app, uma funcionalidade por cena, frases curtas e trilha marcada.

- **Arquivos:** `FEA-teaser-reology-map-16x9.mp4` (1920x1080) e `FEA-teaser-reology-map-9x16.mp4` (1080x1920, Reels e Stories), ambos com 40 s, 30 fps, AAC 256 kbps, -14 LUFS
- **Trilha:** `FEA-trilha-reology-map.wav`, original (ver abaixo)
- **Identidade:** a do próprio app, no tema escuro. Fundo `#111517`, texto `#EDF2F1`, cinza `#B3BFBE`, verde-menta `#A3D4C7`, verde profundo `#174F4A`, fonte Satoshi. As cores das faixas de G′ (azul, laranja e roxo) são as mesmas do app.
- **Telas:** capturadas em 20/10/2026 com o login da Keila, no modo escuro. O aviso "Modo revisão interna" e o menu Administração, que só aparecem para conta de equipe, foram escondidos.
- **Produtos e marcas:** aparecem sem desfoque, com liberação da Keila em 20/10/2026.

## Roteiro

Cada corte cai no tempo forte de um compasso (120 BPM, compasso de 2 s).

| Tempo | Cena | Texto na tela | Som |
|---|---|---|---|
| 0 a 4s | Abertura com o logo | Reology MAP · "Reologia aplicada, consulta consciente." | Drone grave, impacto leve no logo, pulso abafado e subida |
| 4 a 8s | Contadores | Catálogo técnico de preenchedores · 73 produtos · 21 marcas · 19 regiões faciais · "Tudo em um só lugar." | **Drop:** impacto grande, entram o bumbo e o baixo pulsante |
| 8 a 14s | Mapa facial, cursor clica no lábio | "Toque numa região do rosto." · "Da região à ficha, com a faixa de G′ indicada para cada área." | Entra o arpejo · **clique em 12,27s** |
| 14 a 18s | Ficha técnica com a caixa do produto, cursor troca de 0,7 Hz para 5 Hz | "Medições de laboratório, lote a lote." · "G′, G″, tan δ e η* em seis frequências, com radar de quatro eixos." | **Clique em 16,68s** |
| 18 a 22s | Mapa da Reologia (gráfico de dispersão) | "Cada ponto, um ensaio." · "74 ensaios a 0,7 Hz, organizados em cinco perfis reológicos." | Varredura e impacto no corte |
| 22 a 26s | Comparador com 3 produtos | "Compare lado a lado." · "Até quatro produtos, na mesma frequência, com a diferença calculada." | Varredura e impacto no corte |
| 26 a 30s | Biblioteca | "Entenda o que você está lendo." · "Conceitos de reologia, módulo a módulo, ligados às fichas." | Varredura e impacto no corte |
| 30 a 34s | Dois celulares | "Na palma da mão." · "A mesma consulta no consultório, no congresso ou no caminho." | Construção: caixa acelerando e subida |
| 34 a 40s | Assinatura | Logo · "Reologia aplicada, consulta consciente." · Regiões faciais · Produtos · Biblioteca de reologia · "Material educacional para profissionais habilitados. A decisão clínica final é do profissional." | Impacto final, acorde longo e fade |

## Trilha original

A trilha foi composta e sintetizada em código (`fonte/fea_trilha.py`), sem nenhuma amostra de áudio externa. Por isso não tem direito autoral de terceiros.

Ela segue o espírito da referência e se diferencia dela de propósito:

| | Referência (56:25) | Trilha FEA |
|---|---|---|
| Andamento | cerca de 118 a 120 BPM | 120 BPM |
| Tonalidade | perto de Lá menor / Fá | Ré menor, progressão Ré m, Si♭, Fá, Dó |
| Caráter | graves fortes pulsando em colcheias, escuro e constante | graves pulsando com sidechain, arpejo agudo, impactos e varreduras em cada corte |
| Estrutura | volume constante do início ao fim | intro contida, drop aos 4s, construção aos 30s e impacto final aos 34s |

O clique é um "tick" curto de interface, com estalo agudo e um leve corpo grave, mixado seco por cima da música e sincronizado com a animação do cursor.

## De onde vêm os números

Todos foram lidos no app em 20/10/2026, com acesso completo.

- **73 produtos:** página Produtos ("73 produtos disponíveis no seu acesso").
- **21 marcas:** filtro de marcas da página Produtos.
- **19 regiões faciais:** áreas numeradas do mapa. A home diz "20 regiões disponíveis", porque conta também "Qualidade de pele / hidratação", que não tem número no rosto.
- **74 ensaios em 5 perfis:** soma dos perfis P1 a P5 da página Mapa da Reologia (28 + 5 + 14 + 2 + 25).
- **6 frequências:** 0,01 / 0,1 / 0,7 / 1 / 5 / 10 Hz, na ficha de produto.

Os dados do app estão marcados como "em revisão". Se o catálogo mudar antes da publicação, os contadores precisam ser atualizados e o vídeo renderizado de novo.

## Pendências antes de publicar

1. **Foto do mapa facial:** a imagem é da equipe (está no app). Confirmar se a autorização de uso cobre material de divulgação.

## Versão Reels (9:16)

Mesmo roteiro, mesma trilha e cliques nos mesmos tempos (12,27 s e 16,68 s). O texto de cada cena fica no alto e a janela do app embaixo, mais estreita (905 px de largura interna, ampliada 1,08x) para as telas ficarem legíveis no celular. Na ficha técnica o enquadramento corre para a direita para mostrar a caixa do produto e o botão de 5 Hz. Os contadores ficam empilhados, os dois celulares lado a lado, e o aviso legal sobe para fora da área coberta pelos botões do Instagram.

## Como editar e renderizar de novo (`fonte/`)

- `fea_captura_telas.js` captura as telas logadas com Playwright (`BLUR=0` mantém produtos e marcas nítidos). Precisa de uma sessão salva (`state.json`), que não fica no repositório porque contém o cookie de login.
- `FEA-teaser-reology-map.html` é a animação, feita em GSAP. A tabela `WARP` alinha cada cena ao compasso da trilha.
- `FEA-teaser-reology-map-reels.html` é a versão vertical.
- `fea_render.js` renderiza o HTML quadro a quadro e gera o MP4 com o ffmpeg. `fea_render_paralelo.js` faz o mesmo com 4 processos (`HTML=FEA-teaser-reology-map-reels.html VW=1080 VH=1920 node fea_render_paralelo.js 30 saida.mp4 4`).
- `fea_trilha.py` gera a trilha (`python3 fea_trilha.py saida.wav`). Depois, normalizar com `ffmpeg -af "highpass=f=25,loudnorm=I=-14:TP=-1.0:LRA=11"` e juntar ao vídeo.
