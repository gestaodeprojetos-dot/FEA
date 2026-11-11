// Serve a página em código só em pl.joaopithon.com.br/mpl.
// Todo o resto do pl.joaopithon.com.br (inclusive /pesquisa-mpl/) continua indo para o WordPress.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/mpl') {           // /mpl -> /mpl/ mantendo UTMs
      url.pathname = '/mpl/';
      return Response.redirect(url.toString(), 301);
    }
    const resposta = await env.ASSETS.fetch(request);
    const r = new Response(resposta.body, resposta);
    if (url.pathname === '/mpl/' || url.pathname.endsWith('.html')) {
      r.headers.set('Cache-Control', 'public, max-age=0, must-revalidate'); // ajuste aparece na hora
    }
    return r;
  }
};
