/**
 * ACESSOS — prova protegida, planilha e perguntas abertas ao time
 * Mentoria Imparavel — Pithon Napoli Experience
 *
 * COMO USAR
 * 1. No Apps Script, painel da esquerda em "Arquivos" -> "+" -> "Script"
 * 2. Nome do arquivo:  Acessos
 * 3. Apague o  function myFunction() {}  e cole ESTE arquivo
 * 4. Ctrl+S
 * 5. No dropdown, selecione  configurarAcessos  e clique em Executar
 *
 * O QUE ELE FAZ
 *   PROVA (link do aluno) ... exige login Google, 1 resposta por pessoa,
 *                             todas as questoes obrigatorias, sem edicao
 *                             depois de enviar
 *   PLANILHA ............... qualquer pessoa com o link EDITA
 *   PERGUNTAS (formulario) . qualquer pessoa com o link EDITA
 *
 * Os dois niveis sao independentes: liberar a edicao do formulario para o
 * time nao afeta o link do aluno, que continua exigindo login para responder.
 */

// ============================== OPCOES ==============================

var ACESSO = {

  ID_FORM: '1MTx6SasJPjcpFdKI0lltyt-WuM4L2GmciIn8ByjwfwU',

  // ------------------- A PROVA (para o aluno) -----------------------

  EXIGIR_LOGIN: true,               // aluno precisa estar logado
  COLETAR_EMAIL: true,              // registra o e-mail de quem respondeu
  UMA_RESPOSTA_POR_PESSOA: true,    // resposta unica
  PERMITIR_EDITAR_RESPOSTA: false,  // nao pode alterar depois de enviar
  TODAS_OBRIGATORIAS: true,         // nenhuma questao pode ficar em branco

  // ---------------- ACESSO DA EQUIPE (por link) ---------------------
  // 'EDITOR' | 'LEITOR' | 'PRIVADO'
  //
  // NOTA: em 'EDITOR', qualquer pessoa com o link do formulario ve o
  // gabarito das 40 questoes, e qualquer pessoa com o link da planilha ve
  // e pode alterar CPF e notas dos alunos. E o acesso total pedido — mande
  // esses dois links so para a equipe, nunca para os alunos.

  ACESSO_PLANILHA: 'EDITOR',
  ACESSO_FORMULARIO: 'EDITOR',

  // IDs de outros arquivos do Drive para liberar junto (docs da prova,
  // planilhas de apoio). Ex.: ['1abc...', '1def...']
  ARQUIVOS_EXTRA: []
};

// ============================== SCRIPT ==============================

function configurarAcessos() {
  var relato = [];

  function tentar(rotulo, fn) {
    try {
      fn();
      relato.push('OK      ' + rotulo);
    } catch (e) {
      relato.push('FALHOU  ' + rotulo + '  ->  ' + e);
    }
  }

  var form = FormApp.openById(ACESSO.ID_FORM);

  // ---------------- prova ----------------
  // Ordem importa: login primeiro, porque coletar e-mail e limitar
  // resposta dependem dele.
  tentar('exigir login do aluno',
         function () { form.setRequireLogin(ACESSO.EXIGIR_LOGIN); });
  tentar('coletar e-mail do respondente',
         function () { form.setCollectEmail(ACESSO.COLETAR_EMAIL); });
  tentar('limitar a 1 resposta por pessoa',
         function () { form.setLimitOneResponsePerUser(ACESSO.UMA_RESPOSTA_POR_PESSOA); });
  tentar('bloquear edicao da resposta apos o envio',
         function () { form.setAllowResponseEdits(ACESSO.PERMITIR_EDITAR_RESPOSTA); });
  tentar('aceitar respostas',
         function () { form.setAcceptingResponses(true); });

  // ---------------- obrigatoriedade ----------------
  if (ACESSO.TODAS_OBRIGATORIAS) {
    var itens = form.getItems();
    var marcadas = 0, jaEstavam = 0;
    for (var i = 0; i < itens.length; i++) {
      var it = itens[i], tipo = it.getType();
      var alvo = null;
      if (tipo === FormApp.ItemType.MULTIPLE_CHOICE) { alvo = it.asMultipleChoiceItem(); }
      else if (tipo === FormApp.ItemType.CHECKBOX)   { alvo = it.asCheckboxItem(); }
      else if (tipo === FormApp.ItemType.LIST)       { alvo = it.asListItem(); }
      else if (tipo === FormApp.ItemType.TEXT)       { alvo = it.asTextItem(); }
      else if (tipo === FormApp.ItemType.PARAGRAPH_TEXT) { alvo = it.asParagraphTextItem(); }
      else if (tipo === FormApp.ItemType.SCALE)      { alvo = it.asScaleItem(); }
      else if (tipo === FormApp.ItemType.GRID)       { alvo = it.asGridItem(); }
      else if (tipo === FormApp.ItemType.DATE)       { alvo = it.asDateItem(); }
      if (!alvo) { continue; }   // cabecalhos, imagens e quebras de pagina
      if (alvo.isRequired()) { jaEstavam++; }
      else { alvo.setRequired(true); marcadas++; }
    }
    relato.push('OK      obrigatoriedade: ' + marcadas + ' marcada(s) agora, ' +
                jaEstavam + ' ja estava(m) — total ' + (marcadas + jaEstavam) +
                ' pergunta(s) obrigatoria(s)');
  }

  // ---------------- compartilhamento ----------------
  function permissaoDe(nivel) {
    return nivel === 'EDITOR' ? DriveApp.Permission.EDIT : DriveApp.Permission.VIEW;
  }
  function liberar(rotulo, fileId, nivel) {
    if (nivel === 'PRIVADO') { relato.push('OK      ' + rotulo + ' mantido PRIVADO'); return; }
    tentar(rotulo + ' liberado por link (' + nivel + ')', function () {
      DriveApp.getFileById(fileId)
              .setSharing(DriveApp.Access.ANYONE_WITH_LINK, permissaoDe(nivel));
    });
  }

  liberar('formulario / perguntas', ACESSO.ID_FORM, ACESSO.ACESSO_FORMULARIO);

  var destinoId = null;
  try { destinoId = form.getDestinationId(); } catch (e) { destinoId = null; }
  if (destinoId) {
    liberar('planilha de respostas', destinoId, ACESSO.ACESSO_PLANILHA);
  } else {
    relato.push('AVISO   formulario sem planilha de respostas vinculada');
  }

  for (var k = 0; k < ACESSO.ARQUIVOS_EXTRA.length; k++) {
    liberar('arquivo extra ' + ACESSO.ARQUIVOS_EXTRA[k],
            ACESSO.ARQUIVOS_EXTRA[k], ACESSO.ACESSO_PLANILHA);
  }

  // ---------------- resultado ----------------
  var saida =
    'ACESSOS CONFIGURADOS\n\n' +
    relato.join('\n') + '\n\n' +
    '============================================================\n' +
    'PARA OS ALUNOS  (exige login, resposta unica)\n' +
    form.getPublishedUrl() + '\n\n' +
    'PARA A EQUIPE — editar as perguntas\n' +
    form.getEditUrl() + '\n\n' +
    'PARA A EQUIPE — planilha de respostas e dashboard\n' +
    (destinoId ? SpreadsheetApp.openById(destinoId).getUrl() : '(nenhuma)') + '\n' +
    '============================================================\n\n' +
    'Os dois links da equipe dao acesso ao gabarito e as notas.\n' +
    'Nao envie nenhum deles para alunos.\n';

  Logger.log(saida);
  return saida;
}

/** Confere quantas perguntas estao obrigatorias, sem alterar nada. */
function conferirObrigatorias() {
  var form = FormApp.openById(ACESSO.ID_FORM);
  var itens = form.getItems(FormApp.ItemType.MULTIPLE_CHOICE);
  var faltando = [];
  for (var i = 0; i < itens.length; i++) {
    var mc = itens[i].asMultipleChoiceItem();
    if (!mc.isRequired()) { faltando.push(mc.getTitle().substring(0, 40)); }
  }
  Logger.log('Questoes de multipla escolha: ' + itens.length +
             '  |  nao obrigatorias: ' + faltando.length +
             (faltando.length ? '\n' + faltando.join('\n') : ''));
}

/** Fecha a prova: para de aceitar novas respostas. */
function encerrarProva() {
  var form = FormApp.openById(ACESSO.ID_FORM);
  form.setAcceptingResponses(false);
  form.setCustomClosedFormMessage(
    'A prova foi encerrada. Em caso de dúvida, procure a coordenação.');
  Logger.log('Prova encerrada — o formulario nao aceita mais respostas.');
}
