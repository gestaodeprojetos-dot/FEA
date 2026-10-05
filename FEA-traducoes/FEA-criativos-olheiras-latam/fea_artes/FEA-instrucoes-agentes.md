# FEA · Instruções para recompor artes do Ebook Olheiras em espanhol (LATAM)

Você recebe um lote de artes do Brasil e entrega a versão em espanhol de cada uma, trocando **única e exclusivamente a copy**. Foto, layout, cores, fontes, ícones e logos ficam idênticos ao original.

## Regras inegociáveis
1. **Nunca IA generativa** para imagem (nem para "limpar" fundo). Apagar texto só com `apagar()` (inpainting clássico OpenCV) ou repintando caixa chapada com `preencher()`.
2. **Copy oficial**: use a tradução que já existe em `../FEA-copy-criativos-final.py` (lista `C`, pares PT→ES por criativo). Não reescreva. Se a arte tiver texto que não está lá, traduza seguindo a skill `/home/user/FEA/.claude/skills/fea-traduccion-es` (leia `references/00-nucleo.md` e `references/90-decisiones.md`): espanhol neutro LATAM, tratamento **usted**, tom médico-científico, "relleno de ojeras", "inyector", "Más información", "zonas de riesgo", sem travessão.
3. **Preço em dólar**: todo R$ vira o valor de `precos.json` (hoje placeholders `US$ [PRECIO]`, `US$ [PRECIO ANTERIOR]`, `[X] %`). Leia sempre de `PRECOS[...]`, nunca escreva o valor fixo no script: quando a gestão definir o preço, `rodar_todos.py` regera tudo. Mapa: R$ 97 / R$ 97,00 → `preco`; R$ 200 riscado → `de_200`; R$ 297 riscado → `de_297`; 76% → `pct_desconto`. Os marcadores `[PRECIO EN MONEDA LOCAL: ...]` do doc de copy **não** entram na arte.
4. **Depoimento em print** (mensagem de aluno, WhatsApp, Instagram): o print fica **original em português**. Abaixo dele (ou na área livre mais próxima) entra uma legenda pequena em espanhol: `Testimonio original en portugués: «<tradução>»`, na fonte do corpo da arte, cor discreta. Nunca traduzir dentro do print.
5. **Mockup do ebook** (capa ou página do livro em português dentro da arte): NÃO mexa na capa/página agora. Traduza o resto e registre no relatório as coordenadas aproximadas do mockup (fase 2, troca pela capa ES real).
6. Capa de material de terceiros em inglês (Allergan) e QR Code: ficam como estão; registre no relatório.
7. Selo "O PRIMEIRO & MAIS VENDIDO · +30 MIL CÓPIAS VENDIDAS" → `MÉTODO EXCLUSIVO DEL DR. JOÃO PITHON · +30 MIL COPIAS VENDIDAS` (decisão de universalização). Se não couber, reduza a fonte do selo, não corte texto.
8. Nomes: arquivo de saída = `FEA-` + nome original com `PTO` → `PTO-LATAM` (ex.: `FEA-Ads 03 - PTO-LATAM - Feed.png`; `FEA-Ads 31 Feed - PTO-LATAM.png`). Para os jpg `[FEED] ADS 02.jpg` → `FEA-[FEED] ADS 02 - LATAM.jpg`. Mesmo formato do original (png→png, jpg→jpg) e mesma resolução.

## Ferramentas
- Baixar do Drive: `mcp__Google_Drive__download_file_content` com o fileId (carregue a ferramenta com ToolSearch `select:mcp__Google_Drive__download_file_content`). O resultado grande é salvo num arquivo JSON; decodifique com `decodificar_download(json_salvo, 'trabalho/<nome>.png')` da lib. Trabalhe em `fea_artes/trabalho/`.
- Ver a imagem: gere `previa(im, 'trabalho/x-prev.jpg')` e abra com Read. Para medir, recorte regiões e amplie.
- Biblioteca: `fea_artes/fea_arte_lib.py` (abrir, medir, caixas_cor, calibrar, apagar, preencher, cor_texto, escrever, alargar_caixa, texto_rotacionado, previa, salvar, baixar_fonte). Exemplo completo e testado: `../fea_recompor_ads06_ads09.py` (Ads 06 e 09).
- Fontes em `fea_artes/fontes` (Montserrat, Roboto, Roboto Condensed). Outras: `baixar_fonte('poppins')` etc. (npm @expo-google-fonts). Identifique a fonte comparando o render do texto PT original com o recorte da arte; calibre o tamanho pela largura medida.
- Python: Pillow, OpenCV, numpy já instalados.

## Método (o que funcionou no Ads 06 e 09)
1. Baixe Feed e Story, gere prévia, leia a copy na imagem e confira com o par PT→ES do doc.
2. Para cada bloco de texto: meça as linhas (`medir`), descubra fonte e cor, apague (`apagar` em fundo foto/degradê/semitransparente; `preencher` em caixa chapada), escreva o ES com `escrever` mantendo centro/alinhamento e linha de base. Se o ES for mais longo: quebre linhas como o original quebraria; se não couber, reduza a fonte no máximo 15 %; caixa chapada pode alargar (`alargar_caixa`).
3. Story costuma ter o mesmo layout deslocado: reaproveite medidas com offset, mas confira.
4. Um script por criativo em `fea_artes/criativos/<nome_curto>.py` gerando Feed e Story (lê `PRECOS`), rodável sozinho a partir de `fea_artes/` (`python3 criativos/ads03.py`). O script lê os originais de `trabalho/` (deixe os originais baixados lá).
5. **Controle de qualidade obrigatório** (olhe cada saída com Read, em tamanho cheio por regiões): nenhum resquício de letra PT, sem mancha de inpainting visível, acentos e ñ corretos, nada cortado ou encostando em borda, alinhamento igual ao original, nenhuma palavra em português (exceto print de depoimento e nome próprio). Refaça até passar.

## Relatório final (responda só isto, em português)
Tabela por arquivo: nome de saída · status (pronto / pronto com placeholder de preço / fase 2 mockup / bloqueado) · observações (texto novo traduzido por você, decisões, coordenadas de mockup, QR, dúvidas). Não faça commit nem upload: o coordenador junta tudo.
