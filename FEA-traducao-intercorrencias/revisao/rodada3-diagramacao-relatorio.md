# FEA · Intercorrências ES · Revisão de diagramação (rodada 3, 05/10/2026)

Disparada pelo apontamento da Keila: «a página 23 ficou com diagramação comprometida no final da página».
A pág. 23 não era caso isolado. A varredura das 221 páginas, com checagens novas e olho página a página
(original ao lado), achou os defeitos abaixo. Todos corrigidos na causa (`traduzir_pdf.py` da skill),
não página a página.

## Defeitos encontrados

| Defeito | Páginas | Gravidade |
|---|---|---|
| Texto do quadro SAIBA MAIS vazando a borda direita | 23 | GRAVE |
| Itens de lista de uma linha avançando até a borda da folha (fora da mancha) | 150+ páginas com lista | GRAVE |
| Último item descendo até o fólio | 14, 66, 81, 86, 88, 94, 101, 109, 111, 139, 156, 168, 169, 189, 190 | GRAVE |
| Linha inteira da legenda sumida («bajo de complicaciones isquémicas y neurooftalmológicas») | 48 | CLASSE A (omissão) |
| Trecho de legenda sumido («un compromiso tisular más extenso») | 47 | CLASSE A (omissão) |
| Legenda partida em dois blocos sobrepostos | 47, 48 | GRAVE |
| Legenda atravessando o fio que fecha a figura | 62, 73 | GRAVE |
| Lista numerada embaralhada | 31, 41 | GRAVE |
| Quadro de duas colunas com frase partida e texto faltando | 29 | GRAVE |
| Subtítulo em negrito colado no item anterior | 65, 88, 107, 111, 119, 125, 126, 141, 178 | GRAVE |
| Rótulo «Abscesos definidos:» colado no item | 149, 151, 161 | MENOR |
| Subitens com hífen fundidos num parágrafo | 103, 105 | GRAVE |
| Marcador duplicado deslocado («⁝») | 89, 109, 122, 139, 148, 154 e outras | MENOR |
| «•☐» no lugar do marcador (linha em Arial Unicode) | 102 | GRAVE |
| Palavra inteira espremida no pé («significativamente») | 173 | GRAVE |

## Checagens finais no PDF entregue

- `conferir_perda.py`: 0 ids com palavra faltando (validado: acusa uma linha apagada de propósito).
- `conferir_sobreposicao.py`: 0 páginas com cruzamento de linhas ou texto sobre fio.
- `conferir_limites.py`: 0 linhas fora da mancha, de quadro, sobre imagem ou no pé; 0 marcadores duplicados.
- `conferir_fontes.py`: 0 glifos em fonte reserva.
- QR: 23 lidos por escaneamento, todos com o destino certo.
- Render das 221 páginas revisado em folhas de contato, com zoom nas páginas alteradas.

## Ressalva registrada

Em algumas páginas densas (ex.: 187) o espanhol, mais longo, usa a redução máxima permitida
(corpo −8 %, entrelinha até −16 %). Está dentro do limite da skill; 6 parágrafos usam redução
adicional do htmlbox de 1 a 5 % (págs. 19, 34, 48, 64, 122, 148).
