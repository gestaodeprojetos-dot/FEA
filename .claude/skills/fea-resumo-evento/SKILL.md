---
name: fea-resumo-evento
description: Monta o vídeo-resumo vertical (9:16, ~45 s) de um evento presencial da FEA (FEP Experience, imersões IFF5/IFF10/IAR/PSP, congressos) a partir das gravações de celular, com título e legenda no padrão dos Reels, falas reais legendadas, trilha que abaixa quando alguém fala e cartela final com a logo. Usar quando a Keila pedir "resumo do evento", "vídeo do evento", "aftermovie", "melhores momentos" da imersão ou do FEP Experience.
---

# FEA: vídeo-resumo de evento

Ideia tirada do guia "O Seu Editor de Vídeo de IA" (estudado em 06/11/2026), adaptada ao padrão FEA. Script: `FEA-edicao-videos/fea_resumo_evento.py` (o docstring tem o formato do `projeto_resumo.json`).

## Entrada que preciso

1. Pasta do Drive com os vídeos e fotos do evento.
2. Pasta de destino e nome do arquivo.
3. **Trilha com licença de uso comercial** (arquivo enviado pela Keila ou pela equipe). Sem trilha licenciada, o vídeo sai só com o áudio real do evento: nunca usar música de terceiros sem licença.
4. Logo da FEA ou do evento (PNG), para a cartela final.

Se faltar a trilha ou a logo, fazer o resto e pedir só o que falta.

## Fluxo

1. **Baixar e listar**: `python3 FEA-edicao-videos/fea_drive.py baixar PASTA_ID destino/` e `listar`.
2. **Folha de contato** de cada vídeo (`fea_folha.sh`) e **transcrição** das falas (`fea_transcrever.py`, ou `fea_transcrever_scribe.py` se a chave da ElevenLabs estiver configurada).
3. **Escolher os momentos** e contar a história em ~45 s (entre 30 s e 1 min):
   - abertura: chegada, ambiente, o laboratório;
   - meio: Dr. João conduzindo, prática, falas curtas e fortes de alunos e do Dr. (2 a 4 s cada);
   - ápice: o melhor momento (reação, aplauso, depoimento curto);
   - fecho: turma reunida e cartela final com a logo.
   Trechos de fala com `legendas` (tempo a partir do início do trecho, texto da transcrição). Vídeo deitado de palco ou slide: `"encaixe": "desfoque"`.
4. **Prévia**: `python3 FEA-edicao-videos/fea_resumo_evento.py projeto_resumo.json --previa` e mosaico de quadros para conferir.
5. **Final**: sem `--previa` (H.264 CRF 18, 1080x1920, 30 fps, AAC 192k). Vídeo HDR do iPhone é convertido sozinho para SDR.
6. **Revisão** antes de subir (checklist abaixo), depois `fea_drive.py upload` e linha na planilha de controle de edições.
7. **Legenda do post** com a skill `fea-legenda-post`.

## Linha vermelha específica de evento

- **Cadáver fresco**: em conteúdo público, só com disclaimer, ou não usar (decidir com a Keila). Grupo fechado de alunos pode.
- **Paciente modelo** (imersões com prática em paciente): rosto só com autorização de imagem. Na dúvida, usar trecho em que o rosto não aparece ou perguntar.
- **Alunos**: confirmar com a Keila se o termo do evento cobre uso de imagem em post público.
- Nada de sangue, intercorrência ou cara de dor (mesmas regras dos Reels).
- Fala com promessa de resultado estético ou ataque a concorrente não entra, mesmo que seja emocionante.
- Sem imagem gerada por IA, sem efeito chamativo: cortes secos no ritmo da fala e da trilha.

## Checklist antes de subir

- [ ] 30 a 60 s, 1080x1920, H.264 (o script avisa fora da faixa).
- [ ] Título nos 3 s iniciais, legenda só depois do título, texto com as correções FEA (nunca "pra").
- [ ] Toda fala que aparece está legendada e sincronizada (conferir 3 quadros).
- [ ] Trilha licenciada e abaixando nas falas (ouvir os trechos com fala).
- [ ] Linha vermelha de evento conferida trecho por trecho na folha de contato.
- [ ] Cartela final com a logo, sem texto cortado.
