/**
 * DASHBOARD DE RESULTADOS DA PROVA — arquivo separado
 * Mentoria Imparavel — Pithon Napoli Experience
 *
 * COMO USAR
 * 1. No Apps Script, no painel da esquerda em "Arquivos", clique no "+"
 * 2. Escolha "Script" e chame o arquivo de  Dashboard
 * 3. Apague o  function myFunction() {}  que vier e cole ESTE arquivo
 * 4. Ctrl+S para salvar
 * 5. No dropdown do topo, selecione  criarDashboard  e clique em Executar
 *
 * Nao mexa no Codigo.gs — ele continua como esta. Este arquivo usa a
 * variavel QUESTOES que ja existe la (no Apps Script, arquivos do mesmo
 * projeto compartilham as variaveis globais).
 *
 * Precisa de pelo menos UMA resposta enviada para funcionar.
 */

// Formulario da prova que foi realmente criado.
// Se um dia voce gerar outro, troque o ID aqui.
var FORM_ID_PROVA = '1MTx6SasJPjcpFdKI0lltyt-WuM4L2GmciIn8ByjwfwU';

var ID_POS_DASH = 'POS-TI-2026';

// ============================ DASHBOARD =============================
/**
 * Monta a aba "Dashboard" (2a aba) da planilha de respostas, com os dados
 * agrupados: visao geral, distribuicao de notas, desempenho por bloco,
 * questoes mais erradas e mais acertadas, tabela completa e ranking.
 *
 * USO MANUAL: selecione  criarDashboard  e clique em Executar.
 *
 * USO AUTOMATICO: crie um gatilho (icone de RELOGIO no menu da esquerda):
 *   Funcao = criarDashboard | Origem = Do formulario | Evento = Ao enviar formulario
 * Assim o painel se atualiza sozinho a cada prova entregue.
 *
 * A aba e recriada do zero a cada execucao — nao edite nada dentro dela,
 * porque sera sobrescrito.
 */

var NOTA_CORTE_PCT = 60;   // % minimo para considerar aprovado

function criarDashboard() {
  var form = FormApp.openById(FORM_ID_PROVA);

  var destinoId = null;
  try { destinoId = form.getDestinationId(); } catch (e) { destinoId = null; }
  if (!destinoId) {
    throw new Error('O formulario ainda nao tem planilha de respostas vinculada.');
  }

  var ss = SpreadsheetApp.openById(destinoId);
  var respostas = ss.getSheets()[0];

  if (respostas.getLastRow() < 2) {
    throw new Error('Ainda nao ha respostas na planilha. O dashboard precisa de ' +
                    'pelo menos uma prova entregue.');
  }

  var dados = respostas.getRange(1, 1, respostas.getLastRow(), respostas.getLastColumn()).getValues();
  var cab = dados[0];
  var linhas = dados.slice(1);

  // ---- localiza colunas ----
  var colNome = -1;
  var colQuestao = {};   // numero da questao -> indice da coluna
  for (var c = 0; c < cab.length; c++) {
    var h = String(cab[c]).trim();
    if (colNome === -1 && h.toLowerCase().indexOf('nome completo') !== -1) { colNome = c; }
    var m = h.match(/^(\d+)\)/);
    if (m) { colQuestao[parseInt(m[1], 10)] = c; }
  }

  var mapaQ = {};
  for (var i = 0; i < QUESTOES.length; i++) { mapaQ[QUESTOES[i].n] = QUESTOES[i]; }

  var numeros = [];
  for (var n in colQuestao) { if (mapaQ[n]) { numeros.push(parseInt(n, 10)); } }
  numeros.sort(function (a, b) { return a - b; });

  if (!numeros.length) {
    throw new Error('Nao encontrei colunas de questoes na planilha. Confira se as ' +
                    'respostas vieram deste formulario.');
  }

  // ---- apura ----
  var stats = {};   // n -> {acertos, erros, escolhas{A..E}}
  for (var k = 0; k < numeros.length; k++) {
    stats[numeros[k]] = { acertos: 0, erros: 0, escolhas: { A: 0, B: 0, C: 0, D: 0, E: 0 } };
  }

  var alunos = [];
  for (var r = 0; r < linhas.length; r++) {
    var acertosAluno = 0;
    for (var j = 0; j < numeros.length; j++) {
      var nq = numeros[j];
      var resp = String(linhas[r][colQuestao[nq]] || '').trim();
      var letra = resp.charAt(0).toUpperCase();
      if (stats[nq].escolhas[letra] !== undefined) { stats[nq].escolhas[letra]++; }
      if (letra === mapaQ[nq].gab) { stats[nq].acertos++; acertosAluno++; }
      else if (resp) { stats[nq].erros++; }
    }
    alunos.push({
      nome: colNome !== -1 ? String(linhas[r][colNome] || '(sem nome)') : 'Aluno ' + (r + 1),
      acertos: acertosAluno,
      pct: numeros.length ? (acertosAluno / numeros.length * 100) : 0
    });
  }

  // ---- estatisticas gerais ----
  var notas = alunos.map(function (a) { return a.acertos; }).sort(function (x, y) { return x - y; });
  var total = notas.length;
  var soma = notas.reduce(function (s, v) { return s + v; }, 0);
  var media = soma / total;
  var mediana = total % 2 ? notas[(total - 1) / 2] : (notas[total / 2 - 1] + notas[total / 2]) / 2;
  var variancia = notas.reduce(function (s, v) { return s + Math.pow(v - media, 2); }, 0) / total;
  var desvio = Math.sqrt(variancia);
  var corte = numeros.length * NOTA_CORTE_PCT / 100;
  var aprovados = notas.filter(function (v) { return v >= corte; }).length;

  // ---- monta a aba ----
  var nomeAba = 'Dashboard';
  var antiga = ss.getSheetByName(nomeAba);
  if (antiga) { ss.deleteSheet(antiga); }
  var d = ss.insertSheet(nomeAba, 1);   // posicao 2

  d.getCharts().forEach(function (ch) { d.removeChart(ch); });

  var AZUL = '#1F4E79', CLARO = '#DEEAF6', CINZA = '#F2F2F2';
  var VERDE = '#C6EFCE', VERMELHO = '#FFC7CE';
  var L = 1;

  function titulo(txt, cols) {
    d.getRange(L, 1, 1, cols).merge().setValue(txt)
     .setFontSize(12).setFontWeight('bold').setFontColor('#FFFFFF')
     .setBackground(AZUL).setVerticalAlignment('middle');
    d.setRowHeight(L, 26);
    L += 1;
  }
  function cabecalho(arr) {
    d.getRange(L, 1, 1, arr.length).setValues([arr])
     .setFontWeight('bold').setBackground(CLARO)
     .setBorder(true, true, true, true, true, true);
    L += 1;
  }

  // Cabecalho geral
  d.getRange(L, 1, 1, 8).merge().setValue(ID_POS_DASH + ' — Painel de Resultados da Prova')
   .setFontSize(16).setFontWeight('bold').setFontColor('#FFFFFF').setBackground(AZUL)
   .setHorizontalAlignment('center').setVerticalAlignment('middle');
  d.setRowHeight(L, 40); L += 1;
  d.getRange(L, 1, 1, 8).merge()
   .setValue('Atualizado em ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'dd/MM/yyyy HH:mm') +
             '  ·  ' + total + ' prova(s) entregue(s)  ·  ' + numeros.length + ' questões  ·  ' +
             'nota de corte: ' + NOTA_CORTE_PCT + '%')
   .setFontStyle('italic').setFontColor('#555555').setHorizontalAlignment('center');
  L += 2;

  // ---- VISAO GERAL ----
  titulo('VISÃO GERAL', 8);
  var linhaKpiCab = L;
  cabecalho(['Respondentes', 'Média', 'Mediana', 'Desvio padrão',
             'Nota máxima', 'Nota mínima', 'Aprovados', '% Aprovação']);
  d.getRange(L, 1, 1, 8).setValues([[
    total,
    Number(media.toFixed(2)),
    Number(mediana.toFixed(2)),
    Number(desvio.toFixed(2)),
    notas[total - 1],
    notas[0],
    aprovados,
    Number((aprovados / total * 100).toFixed(1)) / 100
  ]]).setHorizontalAlignment('center').setBorder(true, true, true, true, true, true);
  d.getRange(L, 8).setNumberFormat('0.0%');
  d.getRange(L, 1, 1, 8).setFontSize(12).setFontWeight('bold');
  L += 2;

  // ---- DISTRIBUICAO DE NOTAS ----
  titulo('DISTRIBUIÇÃO DE NOTAS', 8);
  var faixas = [
    { rot: '0 a 49% (reprovado)', min: 0, max: 49.999 },
    { rot: '50 a 59%', min: 50, max: 59.999 },
    { rot: '60 a 69%', min: 60, max: 69.999 },
    { rot: '70 a 79%', min: 70, max: 79.999 },
    { rot: '80 a 89%', min: 80, max: 89.999 },
    { rot: '90 a 100%', min: 90, max: 100 }
  ];
  var linhaFaixaCab = L;
  cabecalho(['Faixa de desempenho', 'Alunos', '% do total']);
  var inicioFaixas = L;
  var valoresFaixa = faixas.map(function (f) {
    var q = alunos.filter(function (a) { return a.pct >= f.min && a.pct <= f.max; }).length;
    return [f.rot, q, q / total];
  });
  d.getRange(L, 1, valoresFaixa.length, 3).setValues(valoresFaixa)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 3, valoresFaixa.length, 1).setNumberFormat('0.0%');
  L += valoresFaixa.length;

  var gFaixa = d.newChart().asColumnChart()
    .addRange(d.getRange(inicioFaixas, 1, valoresFaixa.length, 2))
    .setOption('title', 'Alunos por faixa de desempenho')
    .setOption('legend', { position: 'none' })
    .setOption('colors', ['#1F4E79'])
    .setOption('width', 520).setOption('height', 260)
    .setPosition(linhaFaixaCab, 9, 0, 0)
    .build();
  d.insertChart(gFaixa);
  L += 2;

  // ---- DESEMPENHO POR BLOCO ----
  titulo('DESEMPENHO POR BLOCO TEMÁTICO', 8);
  var blocos = {}, ordemBlocos = [];
  for (var b = 0; b < numeros.length; b++) {
    var qb = mapaQ[numeros[b]];
    if (!blocos[qb.bloco]) { blocos[qb.bloco] = { q: 0, ac: 0, tot: 0 }; ordemBlocos.push(qb.bloco); }
    blocos[qb.bloco].q++;
    blocos[qb.bloco].ac += stats[numeros[b]].acertos;
    blocos[qb.bloco].tot += stats[numeros[b]].acertos + stats[numeros[b]].erros;
  }
  var linhaBlocoCab = L;
  cabecalho(['Bloco', 'Questões', '% de acerto']);
  var inicioBlocos = L;
  var valoresBloco = ordemBlocos.map(function (nb) {
    var o = blocos[nb];
    return [nb.replace(/^BLOCO [IVX]+ — /, ''), o.q, o.tot ? o.ac / o.tot : 0];
  });
  d.getRange(L, 1, valoresBloco.length, 3).setValues(valoresBloco)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 3, valoresBloco.length, 1).setNumberFormat('0.0%');
  L += valoresBloco.length;

  var gBloco = d.newChart().asBarChart()
    .addRange(d.getRange(inicioBlocos, 1, valoresBloco.length, 1))
    .addRange(d.getRange(inicioBlocos, 3, valoresBloco.length, 1))
    .setOption('title', '% de acerto por bloco')
    .setOption('legend', { position: 'none' })
    .setOption('colors', ['#2E75B6'])
    .setOption('width', 520).setOption('height', 300)
    .setPosition(linhaBlocoCab, 9, 0, 0)
    .build();
  d.insertChart(gBloco);
  L += 2;

  // ---- tabela por questao (base para os rankings) ----
  function linhaQuestao(nq) {
    var st = stats[nq], q = mapaQ[nq];
    var resp = st.acertos + st.erros;
    var pior = '', piorQtd = -1;
    for (var Lt in st.escolhas) {
      if (Lt !== q.gab && st.escolhas[Lt] > piorQtd) { piorQtd = st.escolhas[Lt]; pior = Lt; }
    }
    return [nq,
            q.bloco.replace(/^BLOCO [IVX]+ — /, ''),
            q.gab,
            st.acertos,
            st.erros,
            resp ? st.acertos / resp : 0,
            piorQtd > 0 ? pior + ' (' + piorQtd + ')' : '—'];
  }
  var CAB_Q = ['Questão', 'Bloco', 'Gabarito', 'Acertos', 'Erros', '% acerto', 'Distrator mais marcado'];

  var ordenadas = numeros.slice().sort(function (a, b) {
    var pa = stats[a].acertos / Math.max(1, stats[a].acertos + stats[a].erros);
    var pb = stats[b].acertos / Math.max(1, stats[b].acertos + stats[b].erros);
    return pa - pb;
  });

  // ---- MAIS ERRADAS ----
  titulo('10 QUESTÕES COM MAIS ERROS  (prioridade de revisão em aula)', 8);
  cabecalho(CAB_Q);
  var piores = ordenadas.slice(0, Math.min(10, ordenadas.length)).map(linhaQuestao);
  d.getRange(L, 1, piores.length, 7).setValues(piores)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 6, piores.length, 1).setNumberFormat('0.0%');
  d.getRange(L, 1, piores.length, 7).setBackground(VERMELHO);
  L += piores.length + 2;

  // ---- MAIS ACERTADAS ----
  titulo('10 QUESTÕES COM MAIS ACERTOS', 8);
  cabecalho(CAB_Q);
  var melhores = ordenadas.slice(-10).reverse().map(linhaQuestao);
  d.getRange(L, 1, melhores.length, 7).setValues(melhores)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 6, melhores.length, 1).setNumberFormat('0.0%');
  d.getRange(L, 1, melhores.length, 7).setBackground(VERDE);
  L += melhores.length + 2;

  // ---- TABELA COMPLETA ----
  titulo('DESEMPENHO EM TODAS AS ' + numeros.length + ' QUESTÕES', 8);
  cabecalho(CAB_Q);
  var todas = numeros.map(linhaQuestao);
  d.getRange(L, 1, todas.length, 7).setValues(todas)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 6, todas.length, 1).setNumberFormat('0.0%');
  var faixaPct = d.getRange(L, 6, todas.length, 1);
  var regras = [
    SpreadsheetApp.newConditionalFormatRule().whenNumberLessThan(0.5)
      .setBackground(VERMELHO).setRanges([faixaPct]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenNumberBetween(0.5, 0.8)
      .setBackground('#FFEB9C').setRanges([faixaPct]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThan(0.8)
      .setBackground(VERDE).setRanges([faixaPct]).build()
  ];
  d.setConditionalFormatRules(regras);
  L += todas.length + 2;

  // ---- RANKING ----
  titulo('RANKING DOS ALUNOS', 8);
  cabecalho(['#', 'Aluno', 'Acertos', 'Nota (%)', 'Situação']);
  var rank = alunos.slice().sort(function (a, b) { return b.acertos - a.acertos; })
    .map(function (a, i) {
      return [i + 1, a.nome, a.acertos, a.pct / 100,
              a.pct >= NOTA_CORTE_PCT ? 'Aprovado' : 'Reprovado'];
    });
  d.getRange(L, 1, rank.length, 5).setValues(rank)
   .setBorder(true, true, true, true, true, true);
  d.getRange(L, 4, rank.length, 1).setNumberFormat('0.0%');
  L += rank.length;

  // ---- acabamento ----
  d.setColumnWidth(1, 90);
  d.setColumnWidth(2, 300);
  d.setColumnWidth(3, 90);
  d.setColumnWidth(4, 90);
  d.setColumnWidth(5, 90);
  d.setColumnWidth(6, 100);
  d.setColumnWidth(7, 180);
  d.setHiddenGridlines(true);
  d.setFrozenRows(2);
  ss.setActiveSheet(d);

  var msg = 'Dashboard atualizado: ' + total + ' respondente(s), media ' +
            media.toFixed(2) + '/' + numeros.length + ', aprovacao ' +
            (aprovados / total * 100).toFixed(1) + '%.';
  Logger.log(msg);
  return msg;
}
