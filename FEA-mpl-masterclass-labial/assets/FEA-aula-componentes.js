/*
  Componentes reaproveitáveis das páginas de masterclass FEA:
  barra fixa com contador, linha de data, tarja da oferta e linha final.
  Os textos vêm de FEA-aula-config.js. Não colocar texto de aula aqui.
*/
(function () {
  var C = window.FEA_AULA || {};
  var DIA = 86400000, FUSO_BR = 3 * 3600000; // Brasília = UTC-3 (sem horário de verão)

  function el(id) { return document.getElementById(id); }
  function dd(n) { return n < 10 ? '0' + n : '' + n; }
  function escapa(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function diaBR(ms) { return Math.floor((ms - FUSO_BR) / DIA); } // número do dia no calendário de Brasília

  var ICONES = {
    cadeado: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V7a5 5 0 0 0-5-5Zm-3 8V7a3 3 0 1 1 6 0v3H9Zm3 4a1.75 1.75 0 0 1 1 3.18V19h-2v-1.82A1.75 1.75 0 0 1 12 14Z"/></svg>',
    relogio: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 2a8 8 0 1 1 0 16 8 8 0 0 1 0-16Zm-1 3v6l5 3 1-1.7-4-2.4V7h-2Z"/></svg>'
  };

  /* Estado da barra para um instante qualquer (exposto para teste) */
  function estado(agora) {
    var inicio = Date.parse(C.inicio), fim = Date.parse(C.fimAoVivo || C.inicio);
    var f = (C.barra && C.barra.frases) || {};
    if (agora >= fim) return null;                                   // depois da aula: barra sai
    if (agora >= inicio) return { contador: 'Ao vivo agora', frase: f.aoVivo, relogio: false, aoVivo: true };
    var faltamDias = diaBR(inicio) - diaBR(agora);
    if (faltamDias >= 2) return { contador: 'Faltam ' + faltamDias + ' dias', frase: f.dias, relogio: false };
    if (faltamDias === 1) return { contador: 'Falta 1 dia', frase: f.amanha, relogio: false };
    var s = Math.max(0, Math.floor((inicio - agora) / 1000));
    return { contador: dd(Math.floor(s / 3600)) + 'h ' + dd(Math.floor(s % 3600 / 60)) + 'm ' + dd(s % 60) + 's', frase: f.hoje, relogio: true };
  }

  function barra() {
    var b = el('fea-barra'); if (!b) return;
    if (!C.barra || C.barra.exibir === false) { b.hidden = true; return; }
    var cont = b.querySelector('.fea-barra__contador'), frase = b.querySelector('.fea-barra__frase');
    var timer = null;
    function tick() {
      var e = estado(Date.now());
      if (!e) { b.hidden = true; if (timer) clearInterval(timer); return; }
      b.hidden = false;
      if (cont.textContent !== e.contador) cont.textContent = e.contador;
      if (frase.textContent !== (e.frase || '')) frase.textContent = e.frase || '';
      b.classList.toggle('is-relogio', !!e.relogio);
      b.classList.toggle('is-aovivo', !!e.aoVivo);
    }
    tick();
    timer = setInterval(tick, 1000);
    b.addEventListener('click', function () { rolarParaFormulario(); });
  }

  function linhaData() {
    var n = el('fea-linha-data'); if (!n) return;
    if (!C.linhaData || C.linhaData.exibir === false || !C.linhaData.texto) { n.hidden = true; return; }
    n.querySelector('span').textContent = C.linhaData.texto;
  }

  function tarja() {
    var n = el('fea-tarja'); if (!n) return;
    var t = C.tarja;
    if (!t || t.exibir === false || !t.texto) { n.hidden = true; return; }
    var html = escapa(t.texto);
    if (t.destaque && t.texto.indexOf(t.destaque) > -1) html = html.replace(escapa(t.destaque), '<strong>' + escapa(t.destaque) + '</strong>');
    n.style.setProperty('--tarja-cor', t.cor || '#E8142F');
    n.innerHTML = (ICONES[t.icone] || ICONES.cadeado) + '<p>' + html + '</p>';
  }

  function linhaFinal() {
    var n = el('fea-linha-final'); if (!n) return;
    if (!C.linhaFinal || C.linhaFinal.exibir === false || !C.linhaFinal.texto) { n.hidden = true; return; }
    n.textContent = C.linhaFinal.texto;
  }

  function rolarParaFormulario() {
    var alvo = document.getElementById('_form_38_') || document.getElementById('oferta');
    if (!alvo) return;
    var barraAltura = (el('fea-barra') && !el('fea-barra').hidden) ? el('fea-barra').offsetHeight : 0;
    var y = alvo.getBoundingClientRect().top + window.pageYOffset - barraAltura - 16;
    window.scrollTo({ top: y, behavior: 'smooth' });
    setTimeout(function () {
      var c = alvo.querySelector && alvo.querySelector('input[type="text"]:not([type="hidden"]), input[type="tel"]');
      if (c) c.focus({ preventScroll: true });
    }, 650);
  }

  window.FEA_COMPONENTES = { estado: estado, rolarParaFormulario: rolarParaFormulario, render: function (qual) {
    ({ barra: barra, linhaData: linhaData, tarja: tarja, linhaFinal: linhaFinal })[qual]();
  } };

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href="#oferta"]');
    if (!a) return;
    e.preventDefault(); rolarParaFormulario();
  });
})();
