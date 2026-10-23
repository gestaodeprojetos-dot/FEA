// FEA: baixa os 79 videos do banco direto para a pasta do Drive
// Como usar: cole tudo em script.google.com, selecione baixarVideos e clique em Executar.
// O script continua sozinho a cada minuto ate terminar (limite de 6 min por execucao do Google).

const PASTA_ID = '1CmFBx84RcKzJWaSXbHLCFqbfQe4v_Tds';

const VIDEOS = [
  ["FEA-video-001-aplicacao-moca-espalhando-protetor-solar-rosto.mp4", "https://cdn.coverr.co/videos/coverr-a-girl-rubbing-sun-protection-cream-on-her-face-8332/1080p.mp4"],
  ["FEA-video-002-aplicacao-mulher-mostrando-frasco-serum-facial-luz-sol.mp4", "https://cdn.coverr.co/videos/user-ai-generation-0IwhHACz2N6l/1080p.mp4"],
  ["FEA-video-003-aplicacao-maos-depois-aplicar-creme-close.mp4", "https://cdn.coverr.co/videos/user-ai-generation-kv9zE4fNgqFS/1080p.mp4"],
  ["FEA-video-004-aplicacao-celular-gravando-mulher-aplicando-skincare.mp4", "https://assets.mixkit.co/videos/50406/50406-720.mp4"],
  ["FEA-video-005-aplicacao-jovem-espalhando-espuma-skincare.mp4", "https://assets.mixkit.co/videos/50408/50408-720.mp4"],
  ["FEA-video-006-aplicacao-jovem-aplicando-produto-regiao-olhos.mp4", "https://assets.mixkit.co/videos/50413/50413-720.mp4"],
  ["FEA-video-007-aplicacao-mulher-abrindo-pote-hidratante-aplicar.mp4", "https://assets.mixkit.co/videos/50415/50415-1080.mp4"],
  ["FEA-video-008-aplicacao-celular-gravando-jovem-aplicando-hidratante-escuro.mp4", "https://assets.mixkit.co/videos/50416/50416-1080.mp4"],
  ["FEA-video-009-aplicacao-mulher-mostrando-como-usar-hidratante.mp4", "https://assets.mixkit.co/videos/50417/50417-1080.mp4"],
  ["FEA-video-010-aplicacao-jovem-usando-creme-facial.mp4", "https://assets.mixkit.co/videos/50422/50422-720.mp4"],
  ["FEA-video-011-aplicacao-influenciadora-gravando-video-hidratante-casa.mp4", "https://assets.mixkit.co/videos/50423/50423-1080.mp4"],
  ["FEA-video-012-aplicacao-jovem-espalhando-hidratante-mao.mp4", "https://assets.mixkit.co/videos/50424/50424-1080.mp4"],
  ["FEA-video-013-aplicacao-jovem-aplicando-creme-hidratante-rosto.mp4", "https://assets.mixkit.co/videos/50426/50426-720.mp4"],
  ["FEA-video-014-aplicacao-mulher-espalhando-hidratante-os-dedos.mp4", "https://assets.mixkit.co/videos/50427/50427-720.mp4"],
  ["FEA-video-015-aplicacao-homem-jovem-espelho-espalhando-produto-rosto.mp4", "https://assets.mixkit.co/videos/50756/50756-1080.mp4"],
  ["FEA-video-016-aplicacao-homem-jovem-aplicando-skincare-rosto.mp4", "https://assets.mixkit.co/videos/50757/50757-720.mp4"],
  ["FEA-video-017-aplicacao-jovem-roupao-aplicando-produto.mp4", "https://assets.mixkit.co/videos/51167/51167-1080.mp4"],
  ["FEA-video-018-aplicacao-jovem-sorrindo-roupao-aplicando-skincare.mp4", "https://assets.mixkit.co/videos/51168/51168-1080.mp4"],
  ["FEA-video-019-aplicacao-jovem-massageando-contorno-rosto.mp4", "https://assets.mixkit.co/videos/51171/51171-1080.mp4"],
  ["FEA-video-020-aplicacao-jovem-cuidando-pele-delicadeza.mp4", "https://assets.mixkit.co/videos/51172/51172-720.mp4"],
  ["FEA-video-021-aplicacao-jovem-aplicando-creme-olheira.mp4", "https://assets.mixkit.co/videos/51173/51173-720.mp4"],
  ["FEA-video-022-aplicacao-jovem-massageando-creme-rosto.mp4", "https://assets.mixkit.co/videos/51177/51177-720.mp4"],
  ["FEA-video-023-aplicacao-jovem-espelho-banheiro-aplicando-produto.mp4", "https://assets.mixkit.co/videos/51179/51179-1080.mp4"],
  ["FEA-video-024-aplicacao-jovem-espelho-banheiro-aplicando-produto-angulo-1.mp4", "https://assets.mixkit.co/videos/51181/51181-720.mp4"],
  ["FEA-video-025-aplicacao-jovem-espelho-banheiro-aplicando-produto-angulo-2.mp4", "https://assets.mixkit.co/videos/51182/51182-720.mp4"],
  ["FEA-video-026-aplicacao-jovem-aplicando-creme-facial-delicadeza.mp4", "https://assets.mixkit.co/videos/51185/51185-720.mp4"],
  ["FEA-video-027-aplicacao-jovem-roupao-aplicando-skincare.mp4", "https://assets.mixkit.co/videos/51187/51187-720.mp4"],
  ["FEA-video-028-mascara-jovem-aplicando-mascara-facial-escura.mp4", "https://assets.mixkit.co/videos/50407/50407-720.mp4"],
  ["FEA-video-029-mascara-celular-gravando-jovem-mascara-tecido.mp4", "https://assets.mixkit.co/videos/50411/50411-1080.mp4"],
  ["FEA-video-030-mascara-jovem-usando-mascara-tecido-antirrugas.mp4", "https://assets.mixkit.co/videos/50412/50412-720.mp4"],
  ["FEA-video-031-mascara-jovem-aplicando-mistura-escura-produtos-rosto.mp4", "https://assets.mixkit.co/videos/51180/51180-720.mp4"],
  ["FEA-video-032-mascara-jovem-colocando-mascara-facial-papel.mp4", "https://assets.mixkit.co/videos/51186/51186-720.mp4"],
  ["FEA-video-033-mascara-profissional-spa-aplicando-mascara-facial.mp4", "https://assets.mixkit.co/videos/52165/52165-720.mp4"],
  ["FEA-video-034-mascara-paciente-maca-mascara-recebendo-tratamento-aparelho.mp4", "https://assets.mixkit.co/videos/52166/52166-1080.mp4"],
  ["FEA-video-035-mascara-jovem-mascara-tecido-spa.mp4", "https://assets.mixkit.co/videos/52169/52169-1080.mp4"],
  ["FEA-video-036-limpeza-maquiadora-limpando-pele-cliente.mp4", "https://cdn.coverr.co/videos/coverr-makeup-artist-wipes-woman-s-skin-5060/1080p.mp4"],
  ["FEA-video-037-limpeza-removendo-maquiagem-olhos.mp4", "https://cdn.coverr.co/videos/coverr-wiping-eye-makeup-6262/1080p.mp4"],
  ["FEA-video-038-limpeza-jovem-limpando-rosto-toalha.mp4", "https://assets.mixkit.co/videos/50421/50421-720.mp4"],
  ["FEA-video-039-limpeza-jovem-limpando-rosto-algodao.mp4", "https://assets.mixkit.co/videos/51183/51183-1080.mp4"],
  ["FEA-video-040-limpeza-jovem-recebendo-limpeza-pele-profissional.mp4", "https://assets.mixkit.co/videos/52146/52146-1080.mp4"],
  ["FEA-video-041-espelho-close-rosto-homem-idoso.mp4", "https://cdn.coverr.co/videos/coverr-close-up-of-an-old-man-s-face-968/1080p.mp4"],
  ["FEA-video-042-espelho-pessoa-se-olhando-espelho.mp4", "https://cdn.coverr.co/videos/coverr-looking-in-the-mirror-2261/1080p.mp4"],
  ["FEA-video-043-espelho-rosto-homem-idoso.mp4", "https://cdn.coverr.co/videos/coverr-old-man-s-face-3379/1080p.mp4"],
  ["FEA-video-044-espelho-mulher-se-arrumando-diante-espelho.mp4", "https://assets.mixkit.co/videos/42733/42733-720.mp4"],
  ["FEA-video-045-espelho-mulher-adulta-se-olhando-espelho.mp4", "https://assets.mixkit.co/videos/4573/4573-720.mp4"],
  ["FEA-video-046-espelho-jovem-pe-diante-espelho-banheiro.mp4", "https://assets.mixkit.co/videos/51178/51178-720.mp4"],
  ["FEA-video-047-procedimento-dermatologista-removendo-pintas-laser.mp4", "https://assets.mixkit.co/videos/4746/4746-720.mp4"],
  ["FEA-video-048-procedimento-mulher-recebendo-tratamento-facial-spa.mp4", "https://assets.mixkit.co/videos/52141/52141-1080.mp4"],
  ["FEA-video-049-procedimento-mulher-tratamento-facial-laser.mp4", "https://assets.mixkit.co/videos/52153/52153-1080.mp4"],
  ["FEA-video-050-procedimento-profissional-aplicando-aparelho-led-rosto.mp4", "https://assets.mixkit.co/videos/52154/52154-720.mp4"],
  ["FEA-video-051-procedimento-mulher-mascara-led-vermelho-spa.mp4", "https://assets.mixkit.co/videos/52163/52163-1080.mp4"],
  ["FEA-video-052-procedimento-profissional-passando-eletrodo-vidro-rosto.mp4", "https://assets.mixkit.co/videos/52171/52171-720.mp4"],
  ["FEA-video-053-massagem-profissional-operando-aparelho-estetico-paciente.mp4", "https://assets.mixkit.co/videos/52142/52142-1080.mp4"],
  ["FEA-video-054-massagem-profissional-massageando-rosto-paciente-maca.mp4", "https://assets.mixkit.co/videos/52143/52143-1080.mp4"],
  ["FEA-video-055-massagem-mao-luva-massageando-rosto-paciente.mp4", "https://assets.mixkit.co/videos/52144/52144-1080.mp4"],
  ["FEA-video-056-massagem-limpeza-pele-espatula-ultrassonica.mp4", "https://assets.mixkit.co/videos/52145/52145-720.mp4"],
  ["FEA-video-057-massagem-aplicacao-produto-espatula-madeira-rosto.mp4", "https://assets.mixkit.co/videos/52148/52148-1080.mp4"],
  ["FEA-video-058-massagem-massagem-relaxante-rosto-as-maos.mp4", "https://assets.mixkit.co/videos/52150/52150-720.mp4"],
  ["FEA-video-059-massagem-close-pescoco-durante-massagem-facial.mp4", "https://assets.mixkit.co/videos/52151/52151-720.mp4"],
  ["FEA-video-060-massagem-close-rosto-paciente-olhos-fechados-maca.mp4", "https://assets.mixkit.co/videos/52152/52152-720.mp4"],
  ["FEA-video-061-massagem-massagem-facial-ferramenta-azul.mp4", "https://assets.mixkit.co/videos/52156/52156-720.mp4"],
  ["FEA-video-062-massagem-jovem-recebendo-massagem-facial.mp4", "https://assets.mixkit.co/videos/52157/52157-720.mp4"],
  ["FEA-video-063-massagem-profissional-deslizando-espatula-rosto-paciente.mp4", "https://assets.mixkit.co/videos/52158/52158-720.mp4"],
  ["FEA-video-064-massagem-rosto-mulher-durante-massagem-lifting-facial.mp4", "https://assets.mixkit.co/videos/52159/52159-720.mp4"],
  ["FEA-video-065-massagem-massagem-facial-ferramenta-esferica.mp4", "https://assets.mixkit.co/videos/52160/52160-1080.mp4"],
  ["FEA-video-066-massagem-profissional-luvas-fazendo-massagem-facial.mp4", "https://assets.mixkit.co/videos/52162/52162-720.mp4"],
  ["FEA-video-067-clinica-cientista-mascara-luvas-operando-equipamento-laboratori.mp4", "https://assets.mixkit.co/videos/4707/4707-1080.mp4"],
  ["FEA-video-068-clinica-corredor-hospital-profissional-fundo.mp4", "https://assets.mixkit.co/videos/4745/4745-1080.mp4"],
  ["FEA-video-069-clinica-equipe-recepcao-clinica.mp4", "https://assets.mixkit.co/videos/4766/4766-1080.mp4"],
  ["FEA-video-070-clinica-medica-sorrindo-jaleco.mp4", "https://assets.mixkit.co/videos/4775/4775-1080.mp4"],
  ["FEA-video-071-clinica-profissional-caminhando-corredor-clinica.mp4", "https://assets.mixkit.co/videos/4779/4779-1080.mp4"],
  ["FEA-video-072-ciencia-molecula-glicose-3d.mp4", "https://assets.mixkit.co/videos/3768/3768-1080.mp4"],
  ["FEA-video-073-ciencia-molecula-aminoacido-3d.mp4", "https://assets.mixkit.co/videos/3769/3769-1080.mp4"],
  ["FEA-video-074-ciencia-molecula-agua-3d-girando.mp4", "https://assets.mixkit.co/videos/3770/3770-1080.mp4"],
  ["FEA-video-075-ciencia-modelo-molecula-agua-3d.mp4", "https://assets.mixkit.co/videos/3771/3771-720.mp4"],
  ["FEA-video-076-ciencia-sangue-visto-microscopio.mp4", "https://assets.mixkit.co/videos/3952/3952-720.mp4"],
  ["FEA-video-077-ciencia-cientista-trabalhando-sangue-laboratorio.mp4", "https://assets.mixkit.co/videos/4711/4711-1080.mp4"],
  ["FEA-video-078-olhos-close-olho-detalhes-delicados.mp4", "https://cdn.coverr.co/videos/user-ai-generation-yvtSFIfk9O/1080p.mp4"],
  ["FEA-video-079-textura-gota-dourada-oleo-facial-caindo-conta-gotas.mp4", "https://cdn.coverr.co/videos/user-ai-generation-MzMzhNLHP3yP/1080p.mp4"]
];

function baixarVideos() {
  const inicio = Date.now();
  const pasta = DriveApp.getFolderById(PASTA_ID);
  const existentes = new Set();
  const arquivos = pasta.getFiles();
  while (arquivos.hasNext()) existentes.add(arquivos.next().getName());

  let novos = 0;
  const falhas = [];
  for (const [nome, url] of VIDEOS) {
    if (existentes.has(nome)) continue;
    if (Date.now() - inicio > 4.5 * 60 * 1000) {
      agendarContinuacao_();
      Logger.log('Pausa para continuar em 1 minuto. Novos nesta rodada: ' + novos);
      return;
    }
    try {
      const resposta = UrlFetchApp.fetch(url, { muteHttpExceptions: true, followRedirects: true });
      if (resposta.getResponseCode() !== 200) {
        falhas.push(nome + ' (HTTP ' + resposta.getResponseCode() + ')');
        continue;
      }
      pasta.createFile(resposta.getBlob().setName(nome));
      novos++;
    } catch (e) {
      falhas.push(nome + ': ' + e.message);
    }
  }
  removerGatilhos_();
  Logger.log('Concluido. Novos nesta rodada: ' + novos + '. Total na pasta: ' + (existentes.size + novos));
  if (falhas.length) Logger.log('Falharam (rode de novo para tentar outra vez):\n' + falhas.join('\n'));
}

function agendarContinuacao_() {
  removerGatilhos_();
  ScriptApp.newTrigger('baixarVideos').timeBased().after(60 * 1000).create();
}

function removerGatilhos_() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'baixarVideos')
    .forEach(t => ScriptApp.deleteTrigger(t));
}
