// FEA · mostrar a mensagem CITADA no conector WhatsApp FEA (uazapi) no Cloudflare
// Problema: quando a Keila responde citando uma mensagem, o ler_mensagens e o novidades
// devolvem só o texto dela, sem a mensagem citada.
//
// Como aplicar (2 minutos, no mesmo Worker do conector):
// 1. Colar a função `extrairCitacao` abaixo perto das outras funções auxiliares.
// 2. Nos pontos onde o ler_mensagens e o novidades montam cada mensagem de saída
//    (o objeto com id, data, de, tipo, texto), acrescentar:
//        citando: await extrairCitacao(msg, base, token),
//    onde `msg` é a mensagem crua da uazapi, e `base`/`token` são os mesmos
//    usados pelo transcrever_audio (env.UAZAPI_URL / env.UAZAPI_TOKEN ou equivalente).
// 3. Salvar e publicar (Deploy). Nada mais muda nas ferramentas.

async function extrairCitacao(msg, base, token) {
  try {
    // A uazapi guarda a citação em lugares diferentes conforme a versão:
    const ctx =
      msg?.content?.contextInfo ||
      msg?.message?.extendedTextMessage?.contextInfo ||
      msg?.contextInfo ||
      null;
    const idCitado = msg?.quoted || ctx?.stanzaId || null;
    if (!idCitado) return null;

    // 1º: texto que já vem junto na própria mensagem
    const q = ctx?.quotedMessage;
    let texto =
      q?.conversation ||
      q?.extendedTextMessage?.text ||
      q?.imageMessage?.caption ||
      q?.videoMessage?.caption ||
      q?.documentMessage?.fileName ||
      null;
    let tipo = q ? Object.keys(q)[0] : null;

    // 2º: se não veio, busca a mensagem citada pelo id
    if (!texto) {
      const r = await fetch(`${base}/message/find`, {
        method: "POST",
        headers: { "Content-Type": "application/json", token },
        body: JSON.stringify({ id: idCitado, limit: 1 }),
      });
      if (r.ok) {
        const d = await r.json();
        const m = (d.messages || d.data || [])[0] || d.message || null;
        texto = m?.text || m?.content?.text || m?.content?.caption || null;
        tipo = tipo || m?.messageType || null;
      }
    }
    return {
      id: idCitado,
      tipo,
      texto: texto ? String(texto).slice(0, 600) : "(mídia sem legenda)",
    };
  } catch (e) {
    return null;
  }
}
