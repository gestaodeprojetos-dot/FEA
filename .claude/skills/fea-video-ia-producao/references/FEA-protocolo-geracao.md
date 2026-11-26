# Geração e revisão (etapas 7 e 8)

## Quem gera
- O conector Higgsfield desta conversa só lê (saldo, modelos, gerações). Não gera.
- A CLI `higgsfield` gera, mas o login (`higgsfield auth login`) abre o navegador: funciona só
  numa sessão do Claude Code no computador da Keila (Claude Desktop ou `claude remote-control`).
  Nunca imprimir o token.
- Sem isso, a Keila gera pelo site seguindo o doc de prompts.

## Protocolo de erro mínimo (Keila: "não pode errar")
1. Toda referência conferida por imagem antes (texto, marca, física, coerência entre objetos).
2. **Antes de cada geração, print do painel de anexos** para o Claude conferir ordem e quantidade.
3. Gestos difíceis simplificados antes de gerar: cordão já solto, objeto já na mão, mão de
   terceiro só antebraço, grupo grande em duplas e trios.
4. Uma cena por vez; o aprovado vira modelo.
5. Defeito pequeno vai para a edição (cortar o take, cobrir com insert), não para nova geração.
6. Rascunho revisado quadro a quadro antes de qualquer refação.

## Configuração padrão no Higgsfield
Seedance 2.5 · Reference (Omni Reference) · Draft 480p · duração inteira · 9:16 · áudio ligado ·
1 vídeo · melhorar prompt desligado.

## Doc de prompts cena a cena (entrega)
Google Doc na pasta de materiais, criado com `create_file` (`text/markdown`), uma seção por cena:
anexos na ordem (`@ImageN` → nome do arquivo e pasta), duração, custo, o que entra na edição, e o
prompt num bloco. Atualização = doc novo "(vN)" e o antigo renomeado `[SUBSTITUÍDO pela vN]`
(o conector não edita conteúdo de arquivo).

## Revisão do rascunho
`scripts/fea_frames_rascunho.sh video.mp4` extrai um quadro a cada 0,5 s numa folha de contato.
Conferir, nesta ordem: rosto (âncoras do card), mãos, objetos (forma, quantidade, texto), logo,
figurino, continuidade entre takes, fala (boca e tempo), música (não pode ter). Dizer à Keila:
usar como está / usar cortando X / refazer só o take Y (com a frase trocada).
