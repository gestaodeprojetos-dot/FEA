# Checklist do roteiro (etapa 1)

Antes de qualquer imagem ou prompt, passar o roteiro por esta lista e devolver à Keila só o que
precisa de decisão.

## Leitura
- Google Doc: `read_file_content` com `includeComments: true` (comentários da copy, como os da
  Adriane, mudam falas).
- Claude Docs (`claude.ai/artifact/<id>`): `Claude_Docs read` com `ref project`, depois o corpo
  da aba com `{"kind":"view"}`. Em releitura, `sinceRev` com a última `rev` lida. O doc pode ser
  só leitura: não tentar editar.

## Tabela que sai da leitura
| Cena | Tempo | Locação | Quem aparece | Fala (de quem) | Texto na tela | Objetos |

## Conferências
1. **Tempo das falas**: cada fala cabe na cena? Gerar a voz e medir (`ffprobe`). Se não cabe,
   propor corte da fala com o texto já reescrito.
2. **Quem fala**: listar todas as vozes. Voz que não é do Dr. João (narrador, "voz da missão")
   pede voz de terceiro no HeyGen.
3. **Texto na tela**: tudo que tem mais de 3 palavras vai para a edição. Palavra única em objeto
   (ex.: "CONFIDENCIAL") pode ir na imagem.
4. **Números e afirmações**: "+2.000 aplicações em 3 dias", "300 cadeiras", "primeiro evento
   que...": pedir a fonte antes de publicar (regra FEA: nunca inventar dado).
5. **Compliance FEA**: promessa de faturamento ou de resultado (CFM/CFO, Meta Ads) gera ressalva
   escrita para a Keila; ela decide.
6. **Figurino por cena**: o roteiro pode trocar a roupa no meio (blazer nas cenas 1 a 3, terno a
   partir do elevador). Cada troca é uma folha de figurino.
7. **Pessoas por plano**: mais de ~5 rostos num plano = risco alto; propor duplas e trios.
8. **Direitos**: homenagem a filme sem trilha, personagem ou logo do filme.
9. **Decisões em aberto**: listar e pedir uma por vez, com recomendação (ex.: clínica ou
   escritório). Se a Keila não responder, seguir a recomendação e dizer que seguiu.
