/**
 * LIBERA O ACESSO PUBLICO — prova e planilha
 * Mentoria Imparavel — Pithon Napoli Experience
 *
 * COMO USAR
 * 1. No Apps Script, painel da esquerda em "Arquivos" -> "+" -> "Script"
 * 2. Nome do arquivo:  Acessos
 * 3. Apague o  function myFunction() {}  e cole ESTE arquivo
 * 4. Ctrl+S
 * 5. No dropdown, selecione  liberarAcessos  e clique em Executar
 *
 * Depois de rodar, o link do aluno funciona para QUALQUER PESSOA, sem
 * login e sem conta Google.
 *
 * >>> LEIA O AVISO SOBRE A PLANILHA NO BLOCO OPCOES ABAIXO <<<
 */

// ============================== OPCOES ==============================

var ACESSO = {

  // Formulario da prova
  ID_FORM: '1MTx6SasJPjcpFdKI0lltyt-WuM4L2GmciIn8ByjwfwU',

  // ---------------------- FORMULARIO (a prova) ----------------------

  // false = qualquer pessoa responde, sem login e sem conta Google.
  // E isto que torna o link 100% aberto.
  EXIGIR_LOGIN: false,

  // false = nao coleta e-mail automaticamente.
  // Precisa ser false quando EXIGIR_LOGIN e false (sem login nao ha e-mail).
  // A identificacao passa a vir dos campos Nome / CPF do proprio formulario.
  COLETAR_EMAIL: false,

  // false = a mesma pessoa pode responder mais de uma vez.
  // Sem login o Google nao consegue limitar isso de verdade.
  UMA_RESPOSTA_POR_PESSOA: false,

  // true = o aluno pode voltar e alterar a resposta depois de enviar
  PERMITIR_EDITAR_RESPOSTA: true,

  // ------------------- PLANILHA DE RESPOSTAS ------------------------
  //
  // ATENCAO — pense antes de deixar 'EDITOR' ou 'LEITOR':
  // a planilha contem o CPF e a nota de todos os alunos, e a aba Dashboard
  // mostra o gabarito de todas as questoes. Um aluno com esse link ve as
  // respostas certas e os dados dos colegas. Em 'EDITOR' ele ainda pode
  // apagar ou alterar notas.
  //
  // Opcoes:
  //   'PRIVADO' = ninguem de fora acessa (recomendado)
  //   'LEITOR'  = qualquer pessoa com o link visualiza
  //   'EDITOR'  = qualquer pessoa com o link edita
  ACESSO_PLANILHA: 'PRIVADO'
};

// ============================== SCRIPT ==============================

function liberarAcessos() {
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

  // ---- formulario ----
  // Sem login nao existe e-mail nem controle de resposta unica.
  // Desliga na ordem certa para o Google nao recusar a combinacao.
  if (!ACESSO.EXIGIR_LOGIN) {
    tentar('desligar limite de 1 resposta por pessoa',
           function () { form.setLimitOneResponsePerUser(false); });
    tentar('desligar coleta de e-mail',
           function () { form.setCollectEmail(false); });
    tentar('desligar exigencia de login  (link fica publico)',
           function () { form.setRequireLogin(false); });
  } else {
    tentar('exigir login',
           function () { form.setRequireLogin(true); });
    tentar('coletar e-mail',
           function () { form.setCollectEmail(ACESSO.COLETAR_EMAIL); });
    tentar('limite de 1 resposta por pessoa',
           function () { form.setLimitOneResponsePerUser(ACESSO.UMA_RESPOSTA_POR_PESSOA); });
  }

  tentar('permitir editar resposta apos envio = ' + ACESSO.PERMITIR_EDITAR_RESPOSTA,
         function () { form.setAllowResponseEdits(ACESSO.PERMITIR_EDITAR_RESPOSTA); });

  tentar('aceitar respostas',
         function () { form.setAcceptingResponses(true); });

  // ---- planilha ----
  var destinoId = null;
  try { destinoId = form.getDestinationId(); } catch (e) { destinoId = null; }

  if (!destinoId) {
    relato.push('AVISO   formulario sem planilha de respostas vinculada');
  } else if (ACESSO.ACESSO_PLANILHA === 'PRIVADO') {
    relato.push('OK      planilha mantida PRIVADA (nenhuma alteracao)');
  } else {
    var permissao = ACESSO.ACESSO_PLANILHA === 'EDITOR'
      ? DriveApp.Permission.EDIT
      : DriveApp.Permission.VIEW;
    tentar('planilha liberada para qualquer pessoa com o link (' + ACESSO.ACESSO_PLANILHA + ')',
           function () {
             DriveApp.getFileById(destinoId)
                     .setSharing(DriveApp.Access.ANYONE_WITH_LINK, permissao);
           });
  }

  // ---- resultado ----
  var linkAluno = form.getPublishedUrl();
  var linkPlanilha = destinoId ? SpreadsheetApp.openById(destinoId).getUrl() : '(nenhuma)';

  var saida =
    'ACESSOS ATUALIZADOS\n\n' +
    relato.join('\n') + '\n\n' +
    '------------------------------------------------------------\n' +
    'LINK PARA ENVIAR AOS ALUNOS (abre sem login):\n' +
    linkAluno + '\n\n' +
    'Planilha de respostas (' + ACESSO.ACESSO_PLANILHA + '):\n' +
    linkPlanilha + '\n' +
    '------------------------------------------------------------\n\n' +
    'Confira abrindo o link do aluno numa janela anonima (Ctrl+Shift+N).\n' +
    'Se pedir login, alguma linha acima aparece como FALHOU — provavelmente\n' +
    'uma restricao da conta Workspace. Nesse caso abra o formulario ->\n' +
    'Configuracoes -> Respostas e desmarque as opcoes de e-mail e login.\n';

  Logger.log(saida);
  return saida;
}

/** Fecha a prova: para de aceitar novas respostas. */
function encerrarProva() {
  var form = FormApp.openById(ACESSO.ID_FORM);
  form.setAcceptingResponses(false);
  form.setCustomClosedFormMessage(
    'A prova foi encerrada. Em caso de dúvida, procure a coordenação.');
  Logger.log('Prova encerrada — o formulario nao aceita mais respostas.');
}
