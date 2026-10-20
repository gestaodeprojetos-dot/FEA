# FEA · Teaser do app Reology Map (v1)

Teaser de 38 segundos do app **Reology Map** (reology.joaopithon.com.br), no formato do vídeo do ProHarmony Atlas mostrado aos 56:25 da referência: motion design sobre gravações reais do app, uma funcionalidade por cena e frases curtas.

- **Arquivo:** `FEA-teaser-reology-map-16x9.mp4` (1920x1080, 30 fps, sem áudio)
- **Identidade:** a do próprio app, no tema escuro. Fundo `#111517`, texto `#EDF2F1`, cinza `#B3BFBE`, verde-menta `#A3D4C7`, verde profundo `#174F4A`, fonte Satoshi. As cores das faixas de G′ (azul, laranja e roxo) são as mesmas do app.
- **Telas:** capturadas em 20/10/2026 com o login da Keila, no modo escuro. O aviso "Modo revisão interna" e o menu Administração, que só aparecem para conta de equipe, foram escondidos.
- **Marcas:** nomes de marca e fotos de caixa de produto estão desfocados (linha vermelha 3 da FEA). Os nomes das linhas de produto continuam legíveis.

## Roteiro

| Tempo | Cena | Texto na tela |
|---|---|---|
| 0 a 3,4s | Abertura com o logo | Reology MAP · "Reologia aplicada, consulta consciente." |
| 3,4 a 7,8s | Contadores | Catálogo técnico de preenchedores · 73 produtos · 21 marcas · 19 regiões faciais · "Tudo em um só lugar." |
| 7,8 a 13s | Mapa facial, cursor clica no lábio | "Toque numa região do rosto." · "Da região à ficha, com a faixa de G′ indicada para cada área." |
| 13 a 18s | Ficha técnica, troca de 0,7 Hz para 5 Hz | "Medições de laboratório, lote a lote." · "G′, G″, tan δ e η* em seis frequências, com radar de quatro eixos." |
| 18 a 22s | Mapa da Reologia (gráfico de dispersão) | "Cada ponto, um ensaio." · "74 ensaios a 0,7 Hz, organizados em cinco perfis reológicos." |
| 22 a 26,2s | Comparador com 3 produtos | "Compare lado a lado." · "Até quatro produtos, na mesma frequência, com a diferença calculada." |
| 26,2 a 29,4s | Biblioteca | "Entenda o que você está lendo." · "Conceitos de reologia, módulo a módulo, ligados às fichas." |
| 29,4 a 33,4s | Dois celulares | "Na palma da mão." · "A mesma consulta no consultório, no congresso ou no caminho." |
| 33,4 a 38s | Assinatura | Logo · "Reologia aplicada, consulta consciente." · Regiões faciais · Produtos · Biblioteca de reologia · "Material educacional para profissionais habilitados. A decisão clínica final é do profissional." |

## De onde vêm os números

Todos foram lidos no app em 20/10/2026, com acesso completo.

- **73 produtos:** página Produtos ("73 produtos disponíveis no seu acesso").
- **21 marcas:** filtro de marcas da página Produtos.
- **19 regiões faciais:** áreas numeradas do mapa. A home diz "20 regiões disponíveis", porque conta também "Qualidade de pele / hidratação", que não tem número no rosto.
- **74 ensaios em 5 perfis:** soma dos perfis P1 a P5 da página Mapa da Reologia (28 + 5 + 14 + 2 + 25).
- **6 frequências:** 0,01 / 0,1 / 0,7 / 1 / 5 / 10 Hz, na ficha de produto.

Os dados do app estão marcados como "em revisão". Se o catálogo mudar antes da publicação, os contadores precisam ser atualizados e o vídeo renderizado de novo.

## Pendências antes de publicar

1. **Trilha sonora:** o vídeo foi entregue sem áudio. Falta escolher uma trilha licenciada (a edição pode inserir).
2. **Aprovação de marca:** confirmar com o Dr. João se as marcas podem aparecer legíveis. Se puderem, basta recapturar as telas com `BLUR=0`.
3. **Foto do mapa facial:** a imagem é da equipe (está no app). Confirmar se a autorização de uso cobre material de divulgação.
4. **Versão vertical 9:16** para Reels e Stories, se for usada.

## Como editar e renderizar de novo (`fonte/`)

- `fea_captura_telas.js` captura as telas logadas com Playwright. Precisa de uma sessão salva (`state.json`), que não fica no repositório porque contém o cookie de login.
- `FEA-teaser-reology-map.html` é a animação, feita em GSAP. Os tempos e os textos de cada cena ficam nesse arquivo.
- `fea_render.js` renderiza o HTML quadro a quadro e gera o MP4 com o ffmpeg.
