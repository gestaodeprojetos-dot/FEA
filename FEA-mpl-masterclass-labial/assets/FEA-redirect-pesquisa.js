/* Redirecionamento pós-inscrição para a pesquisa, levando e-mail, telefone e UTMs (copiado da página no ar em 10/11/2026) */
(function () {
  if (window.__avRedirectInit) return;
  window.__avRedirectInit = true;

  const FORM_ID = '38';
  const DESTINO = 'https://pl.joaopithon.com.br/pesquisa-mpl/';

  const REDIRECT_STORAGE_KEY = 'av_ac_redirect_form_' + FORM_ID;
  const UTM_STORAGE_PREFIX = 'av_utm_';

  function salvarUtmsDaUrl() {
    try {
      new URLSearchParams(window.location.search).forEach(function (value, key) {
        if (key.toLowerCase().startsWith('utm_') && value) {
          sessionStorage.setItem(UTM_STORAGE_PREFIX + key, value);
        }
      });
    } catch (e) {}
  }

  function getForm() {
    return document.getElementById('_form_' + FORM_ID + '_');
  }

  function getCampo(form, seletores) {
    if (!form) return '';
    for (const seletor of seletores) {
      const campo = form.querySelector(seletor);
      if (campo && campo.value) return campo.value.trim();
    }
    return '';
  }

  function getTelefone(form) {
    if (!form) return '';

    const campoTelefone = form.querySelector(
      'input[name="phone"], input[type="tel"], input[name*="telefone"], input[name*="phone"]'
    );
    if (!campoTelefone) return '';

    let telefone = campoTelefone.value.trim();

    try {
      if (window.intlTelInputGlobals && window.intlTelInputGlobals.getInstance(campoTelefone)) {
        const iti = window.intlTelInputGlobals.getInstance(campoTelefone);
        const numeroCompleto = iti.getNumber();
        if (numeroCompleto) return numeroCompleto;

        const pais = iti.getSelectedCountryData();
        if (pais && pais.dialCode && telefone && !telefone.startsWith('+')) {
          telefone = '+' + pais.dialCode + telefone;
        }
      }
    } catch (e) {}

    telefone = telefone.replace(/[^\d+]/g, '');
    if (telefone && !telefone.startsWith('+')) {
      telefone = '+55' + telefone.replace(/^0+/, '');
    }
    return telefone;
  }

  function adicionarUtmsNaUrl(url) {
    new URLSearchParams(window.location.search).forEach(function (value, key) {
      if (key.toLowerCase().startsWith('utm_') && value) {
        url.searchParams.set(key, value);
      }
    });

    try {
      for (let i = 0; i < sessionStorage.length; i++) {
        const storageKey = sessionStorage.key(i);
        if (storageKey && storageKey.startsWith(UTM_STORAGE_PREFIX)) {
          const utmKey = storageKey.replace(UTM_STORAGE_PREFIX, '');
          const utmValue = sessionStorage.getItem(storageKey);
          if (utmValue && !url.searchParams.has(utmKey)) {
            url.searchParams.set(utmKey, utmValue);
          }
        }
      }
    } catch (e) {}
  }

  function montarUrlRedirect(form) {
    const url = new URL(DESTINO);

    const email = getCampo(form, ['input[name="email"]', 'input[type="email"]']);
    const telefone = getTelefone(form);

    if (email) url.searchParams.set('email', email);
    if (telefone) url.searchParams.set('telefone', telefone);

    adicionarUtmsNaUrl(url);
    return url.toString();
  }

  salvarUtmsDaUrl();

  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (form && form.id === '_form_' + FORM_ID + '_') {
      try {
        sessionStorage.setItem(REDIRECT_STORAGE_KEY, montarUrlRedirect(form));
      } catch (err) {}
    }
  }, true);

  const aguardarActiveCampaign = setInterval(function () {
    if (typeof window._show_thank_you !== 'function') return;

    if (window._show_thank_you.__avRedirectWrapped) {
      clearInterval(aguardarActiveCampaign);
      return;
    }

    const showThankYouOriginal = window._show_thank_you;

    window._show_thank_you = function (id) {
      const retorno = showThankYouOriginal.apply(this, arguments);

      if (String(id) === FORM_ID) {
        let redirectUrl = '';
        try {
          redirectUrl = sessionStorage.getItem(REDIRECT_STORAGE_KEY);
        } catch (e) {}

        if (!redirectUrl) redirectUrl = montarUrlRedirect(getForm());

        setTimeout(function () {
          window.location.href = redirectUrl;
        }, 300);
      }

      return retorno;
    };

    window._show_thank_you.__avRedirectWrapped = true;
    clearInterval(aguardarActiveCampaign);
  }, 50);

  setTimeout(function () {
    clearInterval(aguardarActiveCampaign);
  }, 10000);
})();
