// FEA · ferramenta "baixar_midia" para o conector WhatsApp FEA (uazapi) no Cloudflare
// Colar no mesmo Worker onde já existe a ferramenta "transcrever_audio",
// logo abaixo dela, dentro do mesmo bloco onde as outras ferramentas são registradas.
//
// Usa a MESMA rota da uazapi que o transcrever_audio já usa (POST /message/download),
// só que sem transcrever: devolve o link do arquivo (imagem, vídeo, PDF, figurinha, documento).
// Com o link, o Claude baixa o arquivo, vê a imagem e extrai quadros e áudio do vídeo.
//
// ATENÇÃO: troque UAZAPI_URL e UAZAPI_TOKEN pelos nomes que o seu transcrever_audio
// já usa (copie a forma exata de lá: env.ALGUMA_COISA ou this.env.ALGUMA_COISA).

server.tool(
  "baixar_midia",
  "Baixa a mídia de uma mensagem do WhatsApp (imagem, vídeo, documento, figurinha) pelo ID " +
    "(campo id do ler_mensagens) e devolve o link do arquivo (válido por 2 dias) e o tipo. " +
    "Para vídeo, use transcrever=true para receber também o texto falado.",
  {
    id_mensagem: z.string().describe("ID da mensagem (campo id retornado por ler_mensagens)"),
    transcrever: z
      .boolean()
      .default(false)
      .describe("Só para vídeo com fala: devolve também a transcrição do áudio"),
  },
  async ({ id_mensagem, transcrever }) => {
    const base = env.UAZAPI_URL; // trocar pelo mesmo nome usado no transcrever_audio
    const token = env.UAZAPI_TOKEN; // trocar pelo mesmo nome usado no transcrever_audio

    const resp = await fetch(`${base}/message/download`, {
      method: "POST",
      headers: { "Content-Type": "application/json", token },
      body: JSON.stringify({
        id: id_mensagem,
        return_link: true,
        return_base64: false,
        generate_mp3: false,
        transcribe: false,
      }),
    });
    if (!resp.ok) {
      const erro = await resp.text();
      return { content: [{ type: "text", text: `Erro ${resp.status} ao baixar a mídia: ${erro}` }], isError: true };
    }
    const dados = await resp.json();
    const resultado = {
      id: id_mensagem,
      link: dados.fileURL || dados.url || dados.link || null,
      tipo: dados.mimetype || dados.mimeType || null,
    };

    // Vídeo com fala: reaproveita a transcrição do mesmo jeito que o transcrever_audio faz.
    // Se o seu transcrever_audio usa uma função própria (ex.: transcreverMp3), chame-a aqui
    // com o MP3 gerado pela uazapi.
    if (transcrever) {
      const respMp3 = await fetch(`${base}/message/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json", token },
        body: JSON.stringify({ id: id_mensagem, return_link: true, generate_mp3: true }),
      });
      if (respMp3.ok) {
        const mp3 = await respMp3.json();
        const linkMp3 = mp3.fileURL || mp3.url || mp3.link;
        if (linkMp3) {
          const audio = await (await fetch(linkMp3)).arrayBuffer();
          const whisper = await env.AI.run("@cf/openai/whisper", { audio: [...new Uint8Array(audio)] });
          resultado.transcricao = whisper.text || "";
        }
      }
    }

    return { content: [{ type: "text", text: JSON.stringify(resultado, null, 2) }] };
  }
);
