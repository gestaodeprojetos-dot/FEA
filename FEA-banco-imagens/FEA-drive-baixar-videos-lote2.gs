// FEA: baixa o lote 2 do banco de videos (96 videos, FEA-video-080 em diante) direto para a pasta do Drive
// Como usar: cole tudo em script.google.com, selecione baixarVideos e clique em Executar.
// O script continua sozinho a cada minuto ate terminar (limite de 6 min por execucao do Google).
// Pula o que ja estiver na pasta com o mesmo nome, entao pode rodar de novo sem duplicar.

const PASTA_ID = '1CmFBx84RcKzJWaSXbHLCFqbfQe4v_Tds';

const VIDEOS = [
  ["FEA-video-080-rugas-idosa-de-oculos-sorrindo-close.mp4", "https://videos.pexels.com/video-files/5270481/5270481-hd_1920_1080_25fps.mp4"],
  ["FEA-video-081-rugas-idosa-ajustando-oculos-sorrindo.mp4", "https://videos.pexels.com/video-files/5270484/5270484-hd_1920_1080_25fps.mp4"],
  ["FEA-video-082-rugas-idosa-de-oculos-escuros-close.mp4", "https://videos.pexels.com/video-files/5270508/5270508-hd_1920_1080_25fps.mp4"],
  ["FEA-video-083-rugas-idosa-de-jaqueta-de-couro-close.mp4", "https://videos.pexels.com/video-files/5270516/5270516-hd_1920_1080_25fps.mp4"],
  ["FEA-video-084-rugas-retrato-close-de-idosa.mp4", "https://videos.pexels.com/video-files/5524254/5524254-hd_1080_1920_24fps.mp4"],
  ["FEA-video-085-rugas-rosto-idoso-com-rugas-close.mp4", "https://videos.pexels.com/video-files/5534415/5534415-hd_1920_1080_30fps.mp4"],
  ["FEA-video-086-rugas-idosa-de-olhos-fechados-close.mp4", "https://videos.pexels.com/video-files/5991815/5991815-hd_1920_1080_25fps.mp4"],
  ["FEA-video-087-rugas-mulher-madura-na-luz-suave.mp4", "https://videos.pexels.com/video-files/6551000/6551000-hd_2048_1080_25fps.mp4"],
  ["FEA-video-088-rugas-idosa-sorrindo-close-vertical.mp4", "https://videos.pexels.com/video-files/6624505/6624505-hd_1080_1920_24fps.mp4"],
  ["FEA-video-089-rugas-idosa-tirando-mascara-dos-olhos.mp4", "https://videos.pexels.com/video-files/6872666/6872666-hd_1080_1920_24fps.mp4"],
  ["FEA-video-090-rugas-pele-enrugada-ao-redor-do-olho-macro.mp4", "https://videos.pexels.com/video-files/7298096/7298096-hd_1920_1080_30fps.mp4"],
  ["FEA-video-091-rugas-testa-enrugada-de-idoso-macro.mp4", "https://videos.pexels.com/video-files/7298115/7298115-hd_1920_1080_30fps.mp4"],
  ["FEA-video-092-rugas-olho-piscando-com-rugas-macro.mp4", "https://videos.pexels.com/video-files/7299471/7299471-hd_1080_1920_30fps.mp4"],
  ["FEA-video-093-rugas-rugas-de-idoso-com-oculos-macro.mp4", "https://videos.pexels.com/video-files/7299500/7299500-hd_1920_1080_30fps.mp4"],
  ["FEA-video-094-rugas-olho-e-textura-da-pele-madura.mp4", "https://videos.pexels.com/video-files/7477917/7477917-hd_1080_1920_24fps.mp4"],
  ["FEA-video-095-rugas-reflexo-de-olho-enrugado-no-espelho.mp4", "https://videos.pexels.com/video-files/7545829/7545829-hd_1920_1080_25fps.mp4"],
  ["FEA-video-096-rugas-rosto-de-idosa-close-emocao.mp4", "https://videos.pexels.com/video-files/8057768/8057768-hd_1920_1080_25fps.mp4"],
  ["FEA-video-097-rugas-idosa-close-expressao-profunda.mp4", "https://videos.pexels.com/video-files/8165113/8165113-hd_1920_1080_30fps.mp4"],
  ["FEA-video-098-rugas-idosa-pensativa-luz-natural.mp4", "https://videos.pexels.com/video-files/8165491/8165491-hd_1920_1080_30fps.mp4"],
  ["FEA-video-099-rugas-idosa-de-oculos-perfil-close.mp4", "https://videos.pexels.com/video-files/8528858/8528858-hd_2048_1080_25fps.mp4"],
  ["FEA-video-100-rugas-mulher-madura-de-oculos-sorrindo.mp4", "https://videos.pexels.com/video-files/8558862/8558862-hd_2048_1080_25fps.mp4"],
  ["FEA-video-101-rugas-idosa-sorrindo-para-camera.mp4", "https://videos.pexels.com/video-files/8724243/8724243-hd_2048_1080_25fps.mp4"],
  ["FEA-video-102-rugas-sorriso-com-rugas-visiveis-close.mp4", "https://videos.pexels.com/video-files/8724424/8724424-hd_2048_1080_25fps.mp4"],
  ["FEA-video-103-rugas-olhos-de-homem-maduro-piscando.mp4", "https://videos.pexels.com/video-files/8724517/8724517-hd_2048_1080_25fps.mp4"],
  ["FEA-video-104-rugas-idosa-com-lagrimas-close.mp4", "https://videos.pexels.com/video-files/8871837/8871837-hd_1920_1080_25fps.mp4"],
  ["FEA-video-105-rugas-mulher-madura-sorriso-suave-close.mp4", "https://videos.pexels.com/video-files/10251379/10251379-hd_2048_1080_25fps.mp4"],
  ["FEA-video-106-rugas-olhar-com-rugas-close.mp4", "https://videos.pexels.com/video-files/11120960/11120960-hd_1920_1080_30fps.mp4"],
  ["FEA-video-107-rugas-palpebra-com-rugas-macro.mp4", "https://videos.pexels.com/video-files/18622568/18622568-hd_1920_1080_60fps.mp4"],
  ["FEA-video-108-rugas-retrato-de-idosa-luzes-da-cidade.mp4", "https://videos.pexels.com/video-files/10224139/10224139-hd_1920_1080_30fps.mp4"],
  ["FEA-video-109-rugas-idosa-reflexiva-close.mp4", "https://videos.pexels.com/video-files/5265595/5265595-hd_2048_1080_25fps.mp4"],
  ["FEA-video-110-rugas-idosa-sorrindo-na-luz-do-dia.mp4", "https://videos.pexels.com/video-files/5516426/5516426-hd_1920_1080_30fps.mp4"],
  ["FEA-video-111-rugas-mulher-frustrada-com-rugas-no-espelho.mp4", "https://assets.mixkit.co/videos/4515/4515-720.mp4"],
  ["FEA-video-112-rugas-idoso-de-oculos-pensativo-close.mp4", "https://assets.mixkit.co/videos/49896/49896-720.mp4"],
  ["FEA-video-113-olheiras-homem-esfregando-o-olho-close.mp4", "https://videos.pexels.com/video-files/856002/856002-hd_1920_1080_24fps.mp4"],
  ["FEA-video-114-olheiras-mulher-aplicando-patch-preto-nos-olhos.mp4", "https://videos.pexels.com/video-files/3764060/3764060-hd_1080_1920_25fps.mp4"],
  ["FEA-video-115-olheiras-mulher-aplicando-patches-sob-os-olhos.mp4", "https://videos.pexels.com/video-files/4351118/4351118-hd_1080_1920_30fps.mp4"],
  ["FEA-video-116-olheiras-mascara-facial-e-patches-nos-olhos.mp4", "https://videos.pexels.com/video-files/4351138/4351138-hd_1920_1080_30fps.mp4"],
  ["FEA-video-117-olheiras-homem-com-patch-nos-olhos.mp4", "https://videos.pexels.com/video-files/5891041/5891041-hd_2048_1080_25fps.mp4"],
  ["FEA-video-118-olheiras-rosto-cansado-pouca-luz.mp4", "https://videos.pexels.com/video-files/6473120/6473120-hd_2048_1080_25fps.mp4"],
  ["FEA-video-119-olheiras-jovem-cansado-trabalhando-de-noite.mp4", "https://videos.pexels.com/video-files/6614770/6614770-hd_1920_1080_25fps.mp4"],
  ["FEA-video-120-olheiras-mulher-bocejando-e-esfregando-olhos.mp4", "https://videos.pexels.com/video-files/6658328/6658328-hd_2048_1080_25fps.mp4"],
  ["FEA-video-121-olheiras-olho-cansado-close.mp4", "https://videos.pexels.com/video-files/6764082/6764082-hd_2048_1080_25fps.mp4"],
  ["FEA-video-122-olheiras-aplicando-mascara-sob-os-olhos-close.mp4", "https://videos.pexels.com/video-files/6975311/6975311-hd_2048_1080_30fps.mp4"],
  ["FEA-video-123-olheiras-mulher-sorrindo-aplicando-patches.mp4", "https://videos.pexels.com/video-files/6975335/6975335-hd_2048_1080_30fps.mp4"],
  ["FEA-video-124-olheiras-patches-nos-olhos-rotina-matinal.mp4", "https://videos.pexels.com/video-files/7011147/7011147-hd_1080_1920_25fps.mp4"],
  ["FEA-video-125-olheiras-mulher-de-toalha-aplicando-patches.mp4", "https://videos.pexels.com/video-files/7191194/7191194-hd_1920_1080_30fps.mp4"],
  ["FEA-video-126-olheiras-olhos-com-olheiras-massagem.mp4", "https://videos.pexels.com/video-files/8075412/8075412-hd_2048_1080_25fps.mp4"],
  ["FEA-video-127-olheiras-duas-mulheres-com-patches-nos-olhos.mp4", "https://videos.pexels.com/video-files/8510168/8510168-hd_1080_1920_25fps.mp4"],
  ["FEA-video-128-olheiras-mulher-de-hijab-aplicando-patch.mp4", "https://videos.pexels.com/video-files/9218223/9218223-hd_1920_1080_30fps.mp4"],
  ["FEA-video-129-olheiras-aplicando-patch-dourado-sob-os-olhos.mp4", "https://videos.pexels.com/video-files/9698198/9698198-hd_1920_1080_25fps.mp4"],
  ["FEA-video-130-olheiras-mulher-madura-com-patch-sob-os-olhos.mp4", "https://videos.pexels.com/video-files/10222557/10222557-hd_1080_2048_25fps.mp4"],
  ["FEA-video-131-olheiras-olhar-azul-close-area-dos-olhos.mp4", "https://videos.pexels.com/video-files/29493260/12695456_2560_1440_25fps.mp4"],
  ["FEA-video-132-olheiras-olho-e-textura-da-pele-macro.mp4", "https://videos.pexels.com/video-files/8129455/8129455-hd_2048_1080_25fps.mp4"],
  ["FEA-video-133-olheiras-olho-e-pele-ao-redor-macro.mp4", "https://videos.pexels.com/video-files/7297804/7297804-hd_1920_1080_30fps.mp4"],
  ["FEA-video-134-olheiras-rosto-feminino-close-olhos-azuis.mp4", "https://videos.pexels.com/video-files/13770946/13770946-hd_1080_1920_24fps.mp4"],
  ["FEA-video-135-olheiras-patches-de-silicone-sob-os-olhos.mp4", "https://videos.pexels.com/video-files/4351021/4351021-hd_1080_1920_30fps.mp4"],
  ["FEA-video-136-olheiras-aplicando-patches-de-silicone.mp4", "https://videos.pexels.com/video-files/4351135/4351135-hd_1920_1080_30fps.mp4"],
  ["FEA-video-137-olheiras-mulher-madura-aplicando-patches.mp4", "https://videos.pexels.com/video-files/6724703/6724703-hd_1920_1080_24fps.mp4"],
  ["FEA-video-138-olheiras-colocando-patch-sob-os-olhos-close.mp4", "https://assets.mixkit.co/videos/51174/51174-720.mp4"],
  ["FEA-video-139-olheiras-massageando-patches-sob-os-olhos.mp4", "https://assets.mixkit.co/videos/51175/51175-720.mp4"],
  ["FEA-video-140-olheiras-patch-dourado-sob-os-olhos-vertical.mp4", "https://assets.mixkit.co/videos/51184/51184-720.mp4"],
  ["FEA-video-141-creme-mulher-madura-tocando-o-pescoco.mp4", "https://videos.pexels.com/video-files/3795653/3795653-hd_2048_1080_25fps.mp4"],
  ["FEA-video-142-creme-mulher-de-toalha-aplicando-creme.mp4", "https://videos.pexels.com/video-files/6925813/6925813-hd_1080_1920_25fps.mp4"],
  ["FEA-video-143-creme-aplicando-creme-em-frente-ao-espelho.mp4", "https://videos.pexels.com/video-files/6925814/6925814-hd_1080_1920_25fps.mp4"],
  ["FEA-video-144-creme-homem-aplicando-creme-no-rosto.mp4", "https://videos.pexels.com/video-files/4788008/4788008-hd_1080_2048_25fps.mp4"],
  ["FEA-video-145-creme-hidratante-facial-no-banheiro.mp4", "https://videos.pexels.com/video-files/4974671/4974671-hd_1920_1080_30fps.mp4"],
  ["FEA-video-146-creme-aplicando-creme-para-area-dos-olhos.mp4", "https://videos.pexels.com/video-files/4974672/4974672-hd_1920_1080_30fps.mp4"],
  ["FEA-video-147-creme-aplicando-produto-sob-os-olhos.mp4", "https://videos.pexels.com/video-files/5308682/5308682-hd_1920_1080_24fps.mp4"],
  ["FEA-video-148-creme-espalhando-creme-no-rosto.mp4", "https://videos.pexels.com/video-files/5308683/5308683-hd_1920_1080_24fps.mp4"],
  ["FEA-video-149-creme-mulher-aplicando-creme-facial-vertical.mp4", "https://videos.pexels.com/video-files/5927936/5927936-hd_1080_1920_25fps.mp4"],
  ["FEA-video-150-creme-creme-facial-close-rotina.mp4", "https://videos.pexels.com/video-files/6446127/6446127-hd_1920_1080_25fps.mp4"],
  ["FEA-video-151-creme-aplicando-creme-facial-close-longo.mp4", "https://videos.pexels.com/video-files/6666281/6666281-uhd_2732_1318_30fps.mp4"],
  ["FEA-video-152-creme-mulher-madura-aplicando-creme-em-casa.mp4", "https://videos.pexels.com/video-files/6724691/6724691-hd_1920_1080_24fps.mp4"],
  ["FEA-video-153-creme-mulher-madura-cuidando-da-pele.mp4", "https://videos.pexels.com/video-files/6724793/6724793-hd_1080_1920_24fps.mp4"],
  ["FEA-video-154-creme-mulher-madura-hidratando-area-dos-olhos.mp4", "https://videos.pexels.com/video-files/6724839/6724839-hd_1080_1920_24fps.mp4"],
  ["FEA-video-155-creme-mao-no-rosto-close-artistico.mp4", "https://videos.pexels.com/video-files/6730232/6730232-hd_2048_1080_25fps.mp4"],
  ["FEA-video-156-creme-ferramenta-de-massagem-facial.mp4", "https://videos.pexels.com/video-files/6933523/6933523-hd_1920_1080_25fps.mp4"],
  ["FEA-video-157-creme-jovem-aplicando-hidratante.mp4", "https://videos.pexels.com/video-files/6973456/6973456-hd_1920_1080_25fps.mp4"],
  ["FEA-video-158-creme-aplicando-produto-no-pescoco-espelho.mp4", "https://videos.pexels.com/video-files/7306059/7306059-hd_2048_1080_25fps.mp4"],
  ["FEA-video-159-creme-aplicando-creme-no-espelho-close.mp4", "https://videos.pexels.com/video-files/7306685/7306685-hd_2048_1080_25fps.mp4"],
  ["FEA-video-160-creme-aplicando-creme-vertical.mp4", "https://videos.pexels.com/video-files/7306686/7306686-hd_1080_2048_25fps.mp4"],
  ["FEA-video-161-creme-mulher-madura-tocando-o-rosto.mp4", "https://videos.pexels.com/video-files/7545934/7545934-hd_1080_1920_25fps.mp4"],
  ["FEA-video-162-creme-serum-anti-idade-em-pele-madura.mp4", "https://videos.pexels.com/video-files/7582851/7582851-hd_2048_1080_25fps.mp4"],
  ["FEA-video-163-creme-demonstrando-creme-no-estudio.mp4", "https://videos.pexels.com/video-files/9697675/9697675-hd_1920_1080_25fps.mp4"],
  ["FEA-video-164-creme-aplicando-creme-facial-close.mp4", "https://videos.pexels.com/video-files/9697778/9697778-hd_1920_1080_25fps.mp4"],
  ["FEA-video-165-creme-patches-e-locao-no-rosto.mp4", "https://videos.pexels.com/video-files/10159361/10159361-hd_2048_1080_25fps.mp4"],
  ["FEA-video-166-creme-mulher-madura-aplicando-produto-no-rosto.mp4", "https://videos.pexels.com/video-files/10222560/10222560-hd_2048_1080_25fps.mp4"],
  ["FEA-video-167-creme-mulher-madura-aplicando-skincare-close.mp4", "https://videos.pexels.com/video-files/10251377/10251377-hd_2048_1080_25fps.mp4"],
  ["FEA-video-168-creme-aplicando-produto-na-pele-close.mp4", "https://videos.pexels.com/video-files/16232980/16232980-hd_1080_1920_30fps.mp4"],
  ["FEA-video-169-creme-maos-com-creme-hidratante.mp4", "https://videos.pexels.com/video-files/6973464/6973464-hd_1080_1920_25fps.mp4"],
  ["FEA-video-170-creme-aplicando-produto-no-rosto-estudio.mp4", "https://videos.pexels.com/video-files/8141584/8141584-hd_2048_1080_25fps.mp4"],
  ["FEA-video-171-creme-gua-sha-no-espelho.mp4", "https://videos.pexels.com/video-files/7614377/7614377-hd_2048_1080_25fps.mp4"],
  ["FEA-video-172-textura-rosto-feminino-close-olhos-e-boca.mp4", "https://videos.pexels.com/video-files/5252984/5252984-hd_1920_1080_30fps.mp4"],
  ["FEA-video-173-textura-olho-macro-detalhes.mp4", "https://videos.pexels.com/video-files/7297802/7297802-hd_1920_1080_30fps.mp4"],
  ["FEA-video-174-textura-poros-da-pele-macro.mp4", "https://videos.pexels.com/video-files/7298014/7298014-hd_1920_1080_30fps.mp4"],
  ["FEA-video-175-textura-olho-com-sardas-close.mp4", "https://videos.pexels.com/video-files/7477164/7477164-hd_1080_1920_24fps.mp4"]
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
