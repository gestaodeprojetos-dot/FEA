# Personagens

Uma pasta por personagem recorrente:

```
personagens/
  <nome>/
    card.md          o Identity Card (modelo abaixo)
    fotos/           fotos reais do rosto (várias, de ângulos diferentes) e, se tiver, de corpo
    roupas/          folhas de roupa sem rosto, uma por figurino
```

**O rosto vem só de fotos reais.** Uma folha de rosto gerada por IA "embeleza" e muda a pessoa:
nunca use como fonte de rosto. Para personagem inventado (um desenho, um animal, uma figura
histórica), aí sim a folha gerada é a identidade.

## Modelo de `card.md`

Escreva olhando as fotos, só o que aparece nelas. Esse texto entra literal em todo prompt.

```
# <Nome> — Identity Card (data)

Fotos a anexar: fotos/<arquivo>.jpg (…)

ANCHORS: os 2 ou 3 traços que mais diferenciam o rosto, com o lado e o lugar (ex.: sobrancelha
esquerda mais alta, vinco vertical entre as sobrancelhas).
PROPORTIONS: formato do rosto, largura do maxilar, distância dos olhos, nariz, boca.
FACE: bochechas, queixo, testa, orelhas, pele.
HAIR: cor, comprimento, textura, risca, volume, entradas.
MOUTH: lábios, cantos da boca em repouso, como sorri, se os dentes aparecem.
BUILD: porte, ombros, altura aproximada, mãos, postura.
PERMANENT: acessórios ou detalhes que aparecem sempre (brinco, esmalte, óculos).
AGE READ: faixa de idade aparente.
```

Negativas trazem o que negam ("sem tatuagem" fez aparecer tatuagem): descreva o que existe.
