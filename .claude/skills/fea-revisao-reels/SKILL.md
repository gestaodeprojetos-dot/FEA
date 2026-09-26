---
name: fea-revisao-reels
description: Revisora rigorosa dos Reels de procedimento da FEA (Dr. João Pithon) antes da entrega. Confere vídeo por vídeo, regra por regra, tudo o que a Keila já pediu (formato, título, legenda, cortes, começo e fim na fala, sangue, dor, conversa, grafias técnicas) e só libera o que passa em todos os itens. Usar sempre depois de editar vídeos com a skill fea-edicao-reels, antes de enviar, e quando a Keila pedir para revisar, conferir, auditar ou checar vídeos editados.
---

# FEA: revisão rigorosa de Reels

Nenhum vídeo vai para a Keila sem passar por esta revisão. A revisão tem 2 partes, e as duas são obrigatórias:
- **automática:** o script mede áudio, legenda e arquivo;
- **visual:** eu olho os quadros.

Um vídeo com qualquer ERRO volta para a edição. Cada ATENÇÃO precisa ser resolvida: corrigir, ou registrar por que está certa.

## Como rodar

```
python3 FEA-edicao-videos/fea_revisar.py projeto1.json [projeto2.json ...] --folhas PASTA_FOLHAS
```

O script usa o `projeto.json` da edição (brutos, transcrição, cortes e saída). Ele imprime, por vídeo, `OK` ou `REPROVADO`, com a lista de ERRO e ATENÇÃO. Com `--folhas`, gera uma folha de contato de cada vídeo final, com 1 quadro a cada 2 segundos.

## Checklist completo (o que cada regra exige)

| # | Regra da Keila | Como é conferida | Nível |
|---|---|---|---|
| 1 | H.264, nunca HEVC (tela preta no computador dela) | codec do arquivo | ERRO |
| 2 | 1080x1920, abaixo de 30 MB | resolução e tamanho | ERRO |
| 3 | Máximo 3 min, senão Parte 1 e Parte 2 com a cartela "Parte 2 no perfil" | duração e cartela | ERRO |
| 4 | Título exatamente o da imagem, nos 3 primeiros segundos, Montserrat ExtraBold 116 | texto do .ass contra o projeto | ERRO |
| 4b | Título certo para o conteúdo: a imagem pode estar na ordem de postagem e não na dos arquivos | conferir a tabela arquivo -> título -> frase do Dr. | revisão manual |
| 5 | Legenda só depois do título, nunca duas ao mesmo tempo | tempos do .ass | ERRO |
| 6 | Nada de palavra solta na legenda sem o Dr. falando | voz no áudio durante cada legenda | ERRO |
| 7 | Palavra curta piscando sozinha | duração da legenda de 1 palavra | ATENÇÃO |
| 8 | Nunca "pra" ou "pro" (sempre "para"); sem a interjeição "ó" | texto da legenda | ERRO |
| 9 | Grafias: G' (nunca "gelinho"), pré-jowl (nunca "prédio"), cânula 22x70, G' e G'', mL, "ideia" | texto da legenda | ERRO |
| 10 | Começa quando o Dr. começa a falar | silêncio no início (máx. 0,8 s) | ERRO |
| 11 | Não termina com o início de outra palavra | som subindo no último instante | ERRO |
| 12 | Não termina com frase pela metade | última palavra e a seguinte no bruto | ATENÇÃO |
| 13 | Corte no respiro, sem pedaço de palavra | voz dos dois lados do ponto, no bruto | ATENÇÃO (ouvir) |
| 14 | Só corta quando o Dr. não está fazendo nada: técnica sem fala fica | trecho de mais de 8 s sem fala (conferir se é parado ou técnica) e total cortado do bruto | ATENÇÃO |
| 14b | Vídeo não pode ficar picotado: técnica cortada é reprovação | proporção do bruto mantida (abaixo de 60% = conferir cada corte nos quadros) | ATENÇÃO |
| 15 | Cortar espelho, "fecha o olho", conversa pessoal e histórico da paciente, dor e medo fora de contexto técnico, falas que atacam colegas | palavras-chave nas falas mantidas | ATENÇÃO |
| 16 | Tudo que dá errado sai: sangue escorrendo, agulha estourando, intercorrência | folha de contato (visual) | revisão visual |
| 17 | Cara ou gemido de dor: cortar, silenciar ou dar zoom | folha de contato e som sem fala | revisão visual |
| 18 | Conversa de fundo: cortar ou silenciar | voz sem fala transcrita | revisão visual e de áudio |

## Revisão visual (obrigatória, não pular)

1. Abrir a folha de contato de cada vídeo final (em `--folhas`).
2. Procurar:
   - sangue **escorrendo** (gota que desce pelo queixo ou lábio, gaze ou cotonete encharcado em primeiro plano);
   - cara de dor ou olhos apertados;
   - espelho;
   - luva tapando a imagem por muito tempo;
   - agulha ou cânula com problema;
   - outra pessoa falando ou aparecendo sem motivo.
3. Gotinha pequena no ponto da picada **fica** (decisão da Keila em 24/09/2026). Só sai o que escorre.
4. Achou algo: extrair 1 quadro por segundo do trecho (`-ss INICIO -t DUR -vf fps=1,scale=120:213,tile=15x2`) para achar início e fim exatos, cortar no projeto e gerar o vídeo de novo.
5. A marcação de caneta vermelha na pele **não é sangue**: conferir antes de cortar.

## Como resolver cada ATENÇÃO

- **Frase pela metade no final:** ler as últimas palavras e a seguinte. Se a frase terminou ("bem feito"), está certo. Se não terminou, encerrar na última frase completa.
- **Fala contínua no corte:** o encaixe automático não achou respiro. Ouvir e, se precisar, mover o ponto manualmente para o espaço entre duas palavras.
- **Mais de 8 s sem fala:** olhar os quadros. Se o Dr. está fazendo o procedimento, fica (mesmo sendo o outro lado). Só sai se ele está parado, esperando, ou procurando o pertuito sem conseguir.
- **Cortes de trecho sem fala (revisão inversa):** para cada trecho cortado do bruto, olhar os quadros. Se o Dr. estava fazendo a técnica, o corte está errado: devolver o trecho.
- **Palavra-chave de fala:** ler o contexto.
  - Fica: "dor" técnica ("a lidocaína ácida arde", "sem dor, certo?") e "cirurgia" técnica ("depois das cirurgias o paciente tem fibrose").
  - Sai: conversa sobre a paciente ("ela tava morrendo de medo", "fez cirurgia há pouco tempo?").
- **Palavra piscando:** aceitável se é fala real, mas conferir se não é a transcrição inventando palavra.

## Antes de entregar

- [ ] Todos os vídeos com `OK` no script (0 ERRO).
- [ ] Cada ATENÇÃO resolvida ou justificada.
- [ ] Folha de contato de todos os vídeos olhada.
- [ ] Títulos conferidos contra a imagem de títulos da pasta.
- [ ] Grafias novas que a Keila corrigiu adicionadas em `CORRECOES` (`fea_editar_video.py`) e na tabela acima.
- [ ] Relato para a Keila: o que foi corrigido na revisão, vídeo por vídeo.

## Quando a Keila pedir uma regra nova

Adicionar a regra nos 3 lugares, para nenhuma ficar só na conversa:
1. a regra de edição na skill `fea-edicao-reels`;
2. a verificação em `fea_revisar.py` (em `PROIBIDO_LEGENDA`, `FALA_SUSPEITA` ou um teste novo);
3. a linha na tabela do checklist acima.
