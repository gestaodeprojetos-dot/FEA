---
name: fea-video-ia-producao
description: Produção completa de vídeo com IA dos experts da FEA (Dr. João Pithon, palestrantes, eventos como o Elite Experience), do roteiro ao rascunho aprovado, gastando o mínimo de créditos. Cobre leitura do roteiro do cliente, plano de clipes e custo no Higgsfield, kit de imagens no ChatGPT (cenário, figurino, objetos), elenco (fotos, alturas, autorização), vozes no HeyGen (clone do Dr. João e voz de terceiro), prompts no método da Ana (skill fea-seedance-video), protocolo de erro mínimo na geração, revisão quadro a quadro e entrega para edição. Use sempre que pedirem vídeo de IA, roteiro para vídeo de IA, voz do Dr. João, falas, áudio clonado, rascunho no Higgsfield, créditos, kit de imagens, figurino, cenário ou objeto para vídeo, ou quando um roteiro novo do Luca ou de outro membro chegar.
---

# fea-video-ia-producao

Linha de produção de vídeo de IA da FEA, montada no projeto "A missão Elite" (Elite Experience,
nov/2026). A skill **fea-seedance-video** continua sendo a dona do prompt de vídeo (método da Ana
Alice). Esta skill cuida de tudo o que vem antes e depois do prompt, e decide a ordem.

Regras de ouro aprendidas com a Keila:
- **"Não pode errar."** Cada geração custa crédito. Resolve-se com imagem e planejamento antes de
  gerar, nunca com "gere 2 versões e veja".
- **Rascunho primeiro, 1080p só no fim** e só onde tem rosto.
- **O Dr. João não grava áudio.** A voz vem do clone no HeyGen (`references/FEA-vozes-heygen.md`).
- **Automatizar o máximo.** O que o Claude consegue fazer sozinho (voz, conferência de imagem,
  upload, documento de prompts, revisão de quadros), ele faz sem pedir.
- Respostas em português, com tabelas e emojis, sem travessão, "para" por extenso em todo texto
  escrito. Na fala falada, "pra" só quando a Keila pedir (exceção registrada no projeto).

## O fluxo, em 8 etapas

| # | Etapa | O que fazer | Referência |
|---|---|---|---|
| 1 | **Roteiro** | Ler o roteiro do cliente inteiro (Google Doc: `read_file_content`; Claude Docs `claude.ai/artifact/...`: `Claude_Docs read`, nunca web-fetch). Listar cenas, falas de cada voz, texto de tela. Conferir se cada fala cabe no tempo da cena (2,5 palavras/s; melhor ainda, gerar a voz e medir). Separar números e afirmações para confirmar a fonte antes de publicar | `references/FEA-checklist-roteiro.md` |
| 2 | **Plano de clipes e custo** | Agrupar tomadas curtas (o Higgsfield cobra no mínimo 4 s), juntar cenas da mesma locação, tirar da IA o que é só edição (logo, contador, notificação). Fazer a conta de créditos e apresentar as opções | `references/FEA-custos-higgsfield.md` |
| 3 | **Kit de imagens** | Cenário vazio, figurino "fantasma", objetos (com texto curto já escrito), estado do objeto. Gerar no ChatGPT e conferir cada imagem antes de seguir | `references/FEA-templates-chatgpt.md` |
| 4 | **Elenco** | Card de identidade por pessoa (fotos reais), alturas, autorização de imagem, pedido de fotos | `references/FEA-elenco-e-equipe.md` |
| 5 | **Vozes** | Gerar as falas no HeyGen, medir a duração, mandar para a Keila ouvir, subir no Drive só depois de aprovado | `references/FEA-vozes-heygen.md` |
| 6 | **Prompts** | Escrever com a skill **fea-seedance-video** (Identity Card literal, cenário vazio como @Image1, anexos numerados). Entregar num Google Doc "prompts cena a cena" com anexos na ordem e configuração | skill fea-seedance-video |
| 7 | **Geração** | Protocolo de erro mínimo: print do painel de anexos antes de gerar, Draft 480p, uma cena por vez | `references/FEA-protocolo-geracao.md` |
| 8 | **Revisão e edição** | Extrair quadros e revisar (`scripts/fea_frames_rascunho.sh`). Defeito pequeno vai para a edição. Na edição: voz real por cima, textos, logo, insert do cartão | `references/FEA-protocolo-geracao.md` |

Ordem de produção: uma cena por vez, na ordem do vídeo, porque o que der certo vira modelo para a
próxima. Enquanto a Keila gera uma cena, o Claude prepara o kit e o prompt da seguinte.

## Onde fica cada coisa (Drive e repositório)

- Pasta de materiais do projeto no Drive: tudo o que é gerado ou recebido (imagens, áudios, doc de
  prompts). Nomes no padrão `FEA-<projeto>-<versão>-<item>.<ext>`.
- Versão antiga nunca é apagada: renomear para `[SUBSTITUÍDO pela vN]` (docs) ou `[NÃO USAR]`
  (arquivos), para ninguém anexar o arquivo errado no Higgsfield.
- Estado do projeto, decisões e IDs: `../fea-seedance-video/projetos/<projeto>.md`.
- Áudios: `FEA-<projeto>-video-ia/audios/` no repositório + pasta de materiais no Drive.
- Cards de rosto: `../fea-seedance-video/personagens/<nome>/card.md`.

## Armadilhas já vividas

| Armadilha | O que aconteceu | Como evitar |
|---|---|---|
| Arquivo "sumiu" do Drive | O cenário da biblioteca estava na **lixeira** (busca normal não acha) | `get_file_metadata` pelo ID mostra `trashed: true`; baixar e subir cópia nova |
| Conector do Higgsfield | Só lê (saldo, modelos, gerações); **não gera** | Gerar pelo site com protocolo, ou Claude Code no computador da Keila com `higgsfield auth login` (o login abre navegador; na nuvem não funciona) |
| Objeto que muda de forma | Duas imagens com gravadores diferentes no mesmo vídeo | **Um objeto oficial por vídeo**; imagem nova do mesmo objeto só a partir da oficial anexada |
| Envelope chato com objeto dentro | A IA "faz aparecer" o objeto do nada | Objeto que guarda outro precisa de volume na imagem |
| Fala maior que a cena | Voz da missão de 10,7 s numa cena de 7 s | Gerar a voz cedo, medir, avisar o autor do roteiro com proposta de corte |
| Roteiro novo no meio da produção | O Luca mudou o conceito inteiro depois do kit pronto | Antes de gerar, conferir se o roteiro mudou (ler o doc de novo, `sinceRev`) e avisar a Keila para segurar a geração |
| Pedido de print ou de áudio do Dr. | Ele não grava | Clone do HeyGen é o padrão; gravação real é bônus |
| Tom de voz animado | Clone padrão soa animado demais | `expressivenessBoost: 0`, frase inteira de uma vez |

## Ao terminar um projeto

Registrar no projeto o que foi aprovado (prompt, voz, imagem) e levar para esta skill só o que
vale para o próximo vídeo: uma linha na tabela certa, nunca um diário.
