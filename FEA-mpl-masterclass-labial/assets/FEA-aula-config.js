/*
  CONFIGURAÇÃO DA AULA: este é o único arquivo que muda de uma aula para outra.
  Para reaproveitar a página em outra masterclass, troque só os textos e as datas abaixo.
  Datas sempre com o fuso de Brasília (-03:00) escrito no final.
*/
window.FEA_AULA = {
  // Início da aula. O contador da barra lê esta data.
  inicio: '2026-11-19T20:00:00-03:00',

  // Até quando a barra mostra "Ao vivo agora". Depois disso a barra some sozinha.
  // A duração da aula não veio no briefing: 23h é um valor provisório, confirmar.
  fimAoVivo: '2026-11-19T23:00:00-03:00',

  // Linha de data abaixo do primeiro botão (ajuste 2)
  linhaData: {
    exibir: true,
    texto: 'Quinta, 19 de novembro, às 20h. Ao vivo e gratuita, sem gravação, em sala fechada no Zoom.'
  },

  // Barra fixa do topo (ajuste 1). O contador é automático; aqui ficam só as frases de cada momento.
  barra: {
    exibir: true,
    frases: {
      dias:   'Esta é a live de encerramento da Black Friday Vitalícia.',   // faltando 2 dias ou mais
      amanha: 'Amanhã é a live de encerramento da Black Friday Vitalícia.', // faltando 1 dia
      hoje:   'É hoje a live de encerramento da Black Friday Vitalícia.',   // no dia, até o horário da aula
      aoVivo: 'A live de encerramento começou.'                            // durante a aula
    }
  },

  // Tarja abaixo da linha de data (ajuste 3)
  tarja: {
    exibir: true,
    texto: 'Você vem pela aula. Mas ela é também a live de encerramento da Black Friday Vitalícia: é nela que você recebe a condição final, e é nessa noite que as vagas fecham.',
    destaque: 'live de encerramento da Black Friday Vitalícia', // trecho do texto que fica em negrito na cor da tarja
    cor: '#E8142F',      // vermelho de urgência da página (um tom mais fechado, para ler bem em texto pequeno)
    icone: 'cadeado'     // 'cadeado' ou 'relogio'
  },

  // Linha acima do botão final (ajuste 5)
  linhaFinal: {
    exibir: true,
    texto: 'Fica até o fim. É no final que você recebe a condição de encerramento da Black Friday.'
  }
};
