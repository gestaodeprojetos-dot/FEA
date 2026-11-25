# FEA: ajustes da página MTB (Masterclass Toxina, live 9/11/2026 às 20h)

Página: https://feb.joaopithon.com.br/mtb/ (WordPress + Elementor, página ID 672, cache WP Rocket, Cloudflare na frente com HTML em modo DYNAMIC).

## Estado em 03/11/2026 (auditado na página no ar)

| Ajuste do briefing | Status |
|---|---|
| 2. Data do cartão sobre a foto | Já no ar: "9 de novembro, às 20h / Ao vivo, sem replay, no Zoom" |
| Alvo da contagem | Já no ar: 9/11/2026 20h Brasília |
| 1. Tarja do topo em 3 níveis | Falta: colar `FEA-mtb-1-tarja-topo.html` |
| 3. Tarja preta e dourada da Black | Falta: colar `FEA-mtb-3-tarja-black-friday.html` |
| 4. Quarto cartão | Falta: texto em `FEA-mtb-4-quarto-cartao.txt` |

## Passo a passo no Elementor (~15 min)

1. `feb.joaopithon.com.br/wp-admin` > Páginas > MTB > Editar com Elementor.
2. Tarja vermelha do topo: apagar o título "O treinamento gratuito começa em:" e o widget de contagem. Arrastar um widget **HTML** para dentro da tarja vermelha e colar o arquivo 1.
3. Apagar o título "Ninguém vai ficar para trás.". Arrastar um widget **HTML** para entre a subheadline ("As diferenças entre as 8 marcas...") e "Inscreva-se gratuitamente:". Colar o arquivo 3.
4. Em "O que você vai aprender?": botão direito no cartão "Marcas: Botox..." > Duplicar. Na cópia, trocar o texto pelo arquivo 4.
5. Pré-visualizar (ícone de olho) no modo celular. Se ok, Atualizar.
6. Barra superior do WordPress > WP Rocket > Limpar cache.
7. Cloudflare: não precisa purgar (o HTML da página não é cacheado lá, `cf-cache-status: DYNAMIC`).

Rollback: Elementor > Histórico > Revisões > voltar para a revisão anterior.

## Teste de primeira tela (simulação na página real, 03/11)

Fim do botão "CLIQUE AQUI PARA CONFIRMAR", em px, contra a altura visível:

| Aparelho (altura visível) | Antes | Depois | Botão na 1ª tela? |
|---|---|---|---|
| iPhone 13/14 (664) | 740 | 787 | Não antes, não depois |
| iPhone SE (568) | 794 | 841 | Não antes, não depois |
| Galaxy S9+ (658) | 794 | 841 | Não antes, não depois |
| Galaxy S24 (780) | 770 | 817 | Sim antes, **não depois** |
| Pixel 7 (839) | 720 | ~760 | Sim antes, sim depois |

A tarja do topo ficou com 56px nos celulares (era 60px) e em 56px também nos celulares largos, onde antes tinha 40px.
