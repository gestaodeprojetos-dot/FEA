/*
  Ajuste 7: o seletor de país (bandeira + DDI) não pode sobrepor o número.
  O componente de telefone calcula o espaço do "+55" uma única vez, antes da fonte da página carregar;
  quando a fonte chega, o "+55" fica mais largo e encosta no número. Aqui o espaço é recalculado
  sempre que o seletor muda de tamanho (fonte carregada, troca de país, rotação da tela).
*/
(function () {
  function ajustar(input, seletor) {
    var largura = Math.ceil(seletor.getBoundingClientRect().width);
    if (largura > 0) input.style.setProperty('padding-left', (largura + 8) + 'px', 'important');
  }
  function iniciar() {
    var input = document.querySelector('#_form_38_ .iti input[type="tel"], #_form_38_ .iti input[name="phone-iti"]');
    var seletor = document.querySelector('#_form_38_ .iti__country-container');
    if (!input || !seletor) return false;
    ajustar(input, seletor);
    if ('ResizeObserver' in window) new ResizeObserver(function () { ajustar(input, seletor); }).observe(seletor);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ajustar(input, seletor); });
    return true;
  }
  var tentativas = 0;
  var t = setInterval(function () { if (iniciar() || ++tentativas > 100) clearInterval(t); }, 100);
})();
