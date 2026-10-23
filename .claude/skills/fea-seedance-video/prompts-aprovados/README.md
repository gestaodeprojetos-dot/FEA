# Prompts aprovados

Cada arquivo guarda um prompt que **o usuário aprovou com palavras claras** ("ficou ótimo",
"perfeito", "deu certo"), exatamente como rodou, com a configuração, os anexos, o porquê de ter
funcionado e o que não copiar. É a fonte das "palavras exatas que funcionaram": antes de escrever
uma cena nova, procure aqui um aprovado parecido e parta dele.

Na prática, os prompts aprovados ficam entre ~1.000 e ~15.000 caracteres. Prompts de 15.000
caracteres ou mais quase nunca são aprovados.

## Índice

| Arquivo | Projeto | Situação que ele resolve | Modo | Duração |
|---|---|---|---|---|
| *(vazio: acrescente uma linha a cada aprovação)* | | | | |

## Como acrescentar um aprovado

Só quando o usuário aprovar com palavras claras. Ir para a cena seguinte sem comentar **não** é
aprovação, e "tá quase" também não.

1. Pegue o prompt **exatamente como rodou**. Se o Higgsfield estiver conectado, busque a geração
   (`show_generations`, tipo vídeo) e converta `<<<image_N>>>` para `@ImageN` e `<<<audio_N>>>`
   para `@AudioN`. Se não estiver, use o prompt da última versão entregue que ele confirmou ter
   rodado.
2. Crie `prompts-aprovados/<projeto>-<cena>-<assunto>.md` com: título, data, frase do usuário,
   configuração, anexos, id da geração, "Por que funcionou", "Cuidado ao reaproveitar" e o prompt.
3. Se o prompt tiver uma frase que depois se mostrou errada (por exemplo, um traço do rosto que a
   pessoa não tem), tire a frase da cópia e diga isso em "Cuidado ao reaproveitar".
4. Acrescente uma linha neste índice.
