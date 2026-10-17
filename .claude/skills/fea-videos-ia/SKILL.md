---
name: fea-videos-ia
description: Método para produzir vídeo com IA na FEA (Dr. João Pithon) - ficha de referência de edição, mapeamento de bruto e emoção por trecho para VSL e vídeo de lançamento, checklist de ideia/roteiro/visual para briefing de gravação, regras de roteiro para voz sintética (HeyGen, ElevenLabs) e limites de compliance para criação 100% IA e clone. Usar quando a Keila pedir VSL, vídeo de lançamento, storyboard, roteiro de vídeo, vídeo com IA, avatar ou clone do Dr. João, ou editar vídeo num formato novo que ainda não tem padrão salvo.
---

# FEA: vídeo com IA

Base: aula da Júlia Wolf Cruz assistida em 17/10/2026. Resumo completo e triagem em `FEA-aprendizados/FEA-aula-videos-ia-julia-wolf.md`. Reels de procedimento continuam com `fea-edicao-reels`; esta skill cobre o resto.

## Limites FEA (checar antes de tudo)

- **Imagem ou vídeo gerado por IA nunca vai para entregável final** (linha vermelha nº 7). Higgsfield e similares só para storyboard e mockup interno, marcados como tal.
- **Clone do Dr. João (avatar ou voz): não criar** sem aprovação expressa da Keila e do Dr. João. Se pedirem, levantar antes: compliance CFM/CFO, disclaimer, risco de reputação, e o limite técnico atual (boca e dentes falham em fala acima de ~40 s).
- B-roll só com material real: aula, procedimento, depoimento autorizado, mídia de cadáver fresco com disclaimer quando o público não for técnico fechado.
- Tom e escrita FEA valem para legenda, texto na tela e roteiro: "para" (nunca "pra"), sem em-dash, sem promessa estética.

## Edição de formato novo (VSL, masterclass, depoimento, lançamento)

1. **Ficha de referência.** Se a Keila mandar um vídeo modelo, baixar (yt-dlp; se o YouTube bloquear o servidor, pedir o MP4 no Drive) e extrair: ritmo e duração média dos cortes, respiro entre falas, se corta a palavra no fim ou antes, texto e imagem sobre a tela (frequência, posição, fonte), trilha (estilo, volume, entra quando), cor/filtro, abertura e fechamento. Salvar em `FEA-edicao-videos/FEA-ficha-ref-<formato>.md` e reler em toda edição daquele formato.
2. **Mapear o bruto** a partir da transcrição (`fea_transcrever.py`): marcar raciocínio abandonado e recomeçado (descartar a primeira tentativa inteira), repetição, erro e trechos que ficariam mais claros em outra ordem. **Reordenar fala do Dr. João só com aprovação**, porque altera conteúdo clínico.
3. **Emoção de cada trecho.** Tabela por trecho: o que está acontecendo com o espectador, o que ele precisa sentir para o próximo trecho funcionar, que elemento entrega isso (texto, dado, B-roll real, nenhum). Mapear também o estágio de consciência dominante (ver `CLAUDE.md`).
4. **Montar** (FFmpeg + legenda ASS do padrão FEA; Remotion só se houver muitos elementos sobre a tela).
5. **Revisão:** legenda, tempo dos cortes, texto na tela contra a linha vermelha.

## Briefing de vídeo gravado (ou storyboard interno)

Responder tudo antes de roteirizar. Ideia mal amarrada é o que mais desperdiça tempo de gravação e crédito.

- **Ideia:** com quem fala (persona e estágio de consciência)? qual mídia? sensação desejada? o que quebra o padrão do feed? sobre o que a história realmente é? protagonista? outros personagens? ambientes? objetos de destaque? arco narrativo? referências visuais?
- **Roteiro:** onde publica; pessoa real ou não; tem narração? (se tem, gravar ou gerar o áudio primeiro, ele define o tempo das cenas). Quebrar em cenas sempre que muda lugar, momento, quem está no quadro ou ação principal. Para cada cena: lugar, momento, quem está, o que faz, roupa, quem está ao redor.
- **Visual:** luz, cor (dominantes, apoio, temperatura, contraste dentro da paleta FEA), lente e profundidade de campo, composição, movimento de câmera, energia, textura, cenário.
- **Por cena:** quadro inicial, quadro final, movimento de câmera.
- Entregar para gravação (Gabriel Napoli, Weslei Sousa) como tabela de cenas. Trilha sonora decidida no início e aplicada só no final.

Se for storyboard gerado por IA: gerar primeiro os assets (ambiente vazio, character sheet, objetos recorrentes, base composta) numa pasta com subpasta de aprovados, e só depois animar. Marcar tudo como "mockup interno, não publicar".

## Texto para voz sintética (HeyGen, ElevenLabs, dublagem)

- Ler a documentação atualizada da plataforma antes de escrever o texto.
- Pontuação muda a fala: vírgula e ponto são direção de pausa.
- Números por extenso.
- Quebra de linha onde a pessoa respira.
- Sigla e termo em inglês: escrever como deve soar (ex.: HOF, PDO, TCLE) e testar.
- Uma instrução de direção de voz por bloco.
- Ouvir o áudio antes de gerar o vídeo.

## Orçamento

Vídeo com IA tem refação. Em qualquer estimativa de custo ou prazo, incluir margem para gerações descartadas e informar o custo de crédito da ferramenta (pesquisar o preço vigente, nunca supor).
