// FEA · Template de palco Elite Injectors Congress · painel de LED 4032 x 1344 px (3:1)
// Uso: PPTX_SKILL=<pasta skill pptx> node fea_gerar_template_palco_elite.js <pasta_assets> <saida.pptx>
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const A = process.argv[2] || "./assets";
const SAIDA = process.argv[3] || "FEA-elite-template-palco-LED-4032x1344.pptx";
const asset = (n) => path.join(A, n);

const px = (v) => v / 96;     // 1 px do painel = 1/96 pol (slide 42 x 14 pol = 4032 x 1344 px)
const pt = (v) => v * 0.75;   // tamanho de fonte em px do painel para pontos

// Paleta oficial do KV: Pantone 550 C, Cool Gray 1 C, Black 6 C (+ tom claro do gradiente do logo)
const THEME = {
  name: "Elite Injectors Congress · Palco LED",
  headFontFace: "Galano Grotesque SemiBold",
  bodyFontFace: "Galano Grotesque",
  colors: {
    dk1: "050C0F", lt1: "EBF2F5", dk2: "0D1B22", lt2: "D3EAF2",
    accent1: "7FB3C6", accent2: "D3EAF2", accent3: "3E6878",
    accent4: "BB3838", accent5: "9CA1A3", accent6: "4D5457",
    hlink: "7FB3C6", folHlink: "D3EAF2",
  },
};

const pres = new pptxgen();
pres.defineLayout({ name: "LED_4032x1344", width: 42, height: 14 });
pres.layout = "LED_4032x1344";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "FEA · Elite Injectors Congress";
pres.company = "Elite Injectors Congress";
pres.title = "Elite Injectors Congress · Template de palco LED 4032 x 1344";

// --- depuração: ONLY=01,02 gera só esses layouts ---
const ONLY = process.env.ONLY ? process.env.ONLY.split(",") : null;
if (ONLY) {
  const _dsm = pres.defineSlideMaster.bind(pres), _as = pres.addSlide.bind(pres), _sec = pres.addSection.bind(pres);
  const ok = (t) => ONLY.some((k) => t.startsWith(k));
  const nada = { addText() {}, addShape() {}, addNotes() {}, addImage() {} };
  pres.defineSlideMaster = (o) => { if (ok(o.title)) _dsm(o); };
  pres.addSlide = (o) => (ok(o.masterName) ? _as({ masterName: o.masterName }) : nada);
  pres.addSection = () => {};
}
const C = pres.SchemeColor;
const GELO = C.background1, GELO2 = C.background2, AZUL = C.accent1, VERMELHO = C.accent4, PRETO = C.text1;
const CARD = "0D1B22", SLOT = "0A161C";

const T_SB = "Galano Grotesque SemiBold", T_BD = "Galano Grotesque", T_MD = "Galano Grotesque Medium";
const CORPO = "Galano Grotesque", ROTULO = "Galano Grotesque Alt Medium", ROTULO_SB = "Galano Grotesque Alt SemiBold";

const bg = (nome) => ({ path: asset(nome) });
const LOGO = asset("FEA-elite-logo-claro.png"); // 3200 x 933
const LOGO_R = 933 / 3200;

// ---------- helpers de layout ----------
const ph = (name, type, x, y, w, h, opts, prompt) => ({
  placeholder: { options: { name, type, x: px(x), y: px(y), w: px(w), h: px(h), margin: 0, ...opts }, text: prompt },
});
const txt = (name, x, y, w, h, prompt, o) => ph(name, "body", x, y, w, h, { valign: "top", align: "left", ...o }, prompt);
const logo = (x, y, w) => ({ image: { path: LOGO, x: px(x), y: px(y), w: px(w), h: px(w * LOGO_R) } });
const rotuloFixo = (texto, x, y, w, h, o) => ({
  text: { text: texto, options: { x: px(x), y: px(y), w: px(w), h: px(h), margin: 0, fontFace: ROTULO, fontSize: pt(46), color: "7FB3C6", charSpacing: 12, valign: "middle", ...o } },
});
const slot = (x, y, w, h, rotulo) => ({
  text: {
    text: rotulo,
    options: {
      shape: pres.ShapeType.roundRect, rectRadius: px(20), x: px(x), y: px(y), w: px(w), h: px(h),
      fill: { color: SLOT }, line: { color: "7FB3C6", width: 2.5, dashType: "dash", transparency: 45 },
      fontFace: ROTULO, fontSize: pt(38), color: "7FB3C6", charSpacing: 4, align: "center", valign: "middle",
    },
  },
});
const fotoPh = (name, x, y, w, h, prompt) => ph(name, "pic", x, y, w, h, {}, prompt);
const aviso = (x, y, w, align) => ({
  text: {
    text: "Resultados variam de acordo com cada paciente.",
    options: { x: px(x), y: px(y), w: px(w), h: px(56), margin: 0, align: align || "left", valign: "middle", fontFace: CORPO, fontSize: pt(36), color: "9CA1A3" },
  },
});

// ---------- LAYOUTS ----------
pres.defineSlideMaster({
  title: "01 Abertura", background: bg("FEA-elite-fundo-abertura.jpg"),
  objects: [
    txt("tagline", 516, 150, 3000, 90, "TAGLINE", { fontFace: ROTULO, fontSize: pt(54), color: GELO2, charSpacing: 16, align: "center", valign: "middle" }),
    logo(1016, 350, 2000),
    txt("data", 416, 1010, 3200, 100, "DATA · LOCAL", { fontFace: ROTULO, fontSize: pt(54), color: AZUL, charSpacing: 12, align: "center", valign: "middle" }),
  ],
});

pres.defineSlideMaster({
  title: "02 Palestrante", background: bg("FEA-elite-fundo-destaque.jpg"),
  objects: [
    slot(336, 168, 756, 1008, "FOTO DO PALESTRANTE\n756 x 1008 px · 3:4"),
    fotoPh("foto", 336, 168, 756, 1008, "Clique no ícone para inserir a foto"),
    ph("nome", "title", 1260, 500, 2500, 220, { fontFace: T_SB, fontSize: pt(170), color: GELO, valign: "middle", align: "left" }, "Nome do palestrante"),
    txt("credenciais", 1260, 740, 2500, 100, "Credenciais em uma linha", { fontFace: T_MD, fontSize: pt(64), color: AZUL, valign: "middle" }),
    txt("tema", 1260, 900, 2500, 150, "Tema da palestra", { fontFace: CORPO, fontSize: pt(56), color: GELO, valign: "top" }),
  ],
});

pres.defineSlideMaster({
  title: "03 Abertura de palestra", background: bg("FEA-elite-fundo-destaque.jpg"),
  objects: [
    ph("titulo", "title", 336, 450, 2650, 430, { fontFace: T_SB, fontSize: pt(170), color: GELO, valign: "top", align: "left", lineSpacingMultiple: 0.95 }, "Título da palestra"),
    txt("apoio", 336, 950, 2600, 100, "Palestrante", { fontFace: T_MD, fontSize: pt(64), color: AZUL, valign: "middle" }),
  ],
});

pres.defineSlideMaster({
  title: "04 Antes e depois", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    slot(336, 168, 756, 1008, "FOTO ANTES\n756 x 1008 px · 3:4"),
    slot(1140, 168, 756, 1008, "FOTO DEPOIS\n756 x 1008 px · 3:4"),
    { text: { text: "", options: { shape: pres.ShapeType.roundRect, rectRadius: px(20), x: px(2064), y: px(168), w: px(1632), h: px(1008), fill: { color: CARD }, line: { color: "7FB3C6", width: 1.5, transparency: 70 } } } },
    fotoPh("foto_antes", 336, 168, 756, 1008, "Foto ANTES"),
    fotoPh("foto_depois", 1140, 168, 756, 1008, "Foto DEPOIS"),
    ph("titulo", "title", 2160, 360, 1440, 250, { fontFace: T_SB, fontSize: pt(96), color: GELO, valign: "top", align: "left", lineSpacingMultiple: 0.95 }, "Título do caso"),
    txt("detalhes", 2160, 660, 1440, 440, "Região · técnica · plano · intervalo", { fontFace: CORPO, fontSize: pt(52), color: GELO, paraSpaceAfter: pt(22) }),
    aviso(2064, 1200, 1632, "right"),
  ],
});

pres.defineSlideMaster({
  title: "05 Antes e depois, 2 casos", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    slot(336, 120, 756, 1008, "CASO 1 · ANTES\n756 x 1008 px"),
    slot(1140, 120, 756, 1008, "CASO 1 · DEPOIS\n756 x 1008 px"),
    slot(2136, 120, 756, 1008, "CASO 2 · ANTES\n756 x 1008 px"),
    slot(2940, 120, 756, 1008, "CASO 2 · DEPOIS\n756 x 1008 px"),
    fotoPh("c1_antes", 336, 120, 756, 1008, "Caso 1 ANTES"),
    fotoPh("c1_depois", 1140, 120, 756, 1008, "Caso 1 DEPOIS"),
    fotoPh("c2_antes", 2136, 120, 756, 1008, "Caso 2 ANTES"),
    fotoPh("c2_depois", 2940, 120, 756, 1008, "Caso 2 DEPOIS"),
    txt("legenda1", 336, 1150, 1560, 70, "Legenda do caso 1", { fontFace: T_MD, fontSize: pt(48), color: AZUL, valign: "middle" }),
    txt("legenda2", 2136, 1150, 1560, 70, "Legenda do caso 2", { fontFace: T_MD, fontSize: pt(48), color: AZUL, valign: "middle" }),
    aviso(2136, 1240, 1560, "right"),
  ],
});

pres.defineSlideMaster({
  title: "06 Caso com foto complementar", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    slot(336, 120, 756, 1008, "FOTO ANTES\n756 x 1008 px · 3:4"),
    slot(1140, 120, 756, 1008, "FOTO DEPOIS\n756 x 1008 px · 3:4"),
    slot(2040, 120, 1656, 1008, "FOTO COMPLEMENTAR\n1656 x 1008 px"),
    fotoPh("foto_antes", 336, 120, 756, 1008, "Foto ANTES"),
    fotoPh("foto_depois", 1140, 120, 756, 1008, "Foto DEPOIS"),
    fotoPh("foto_extra", 2040, 120, 1656, 1008, "Foto complementar (paciente, perfil ou detalhe)"),
    txt("legenda1", 336, 1150, 1560, 70, "Legenda do caso", { fontFace: T_MD, fontSize: pt(48), color: AZUL, valign: "middle" }),
    txt("legenda2", 2040, 1150, 1656, 70, "Legenda da foto", { fontFace: T_MD, fontSize: pt(48), color: AZUL, valign: "middle" }),
    aviso(2040, 1240, 1656, "right"),
  ],
});

pres.defineSlideMaster({
  title: "07 Tela 16:9 central", background: bg("FEA-elite-fundo-centro.jpg"),
  objects: [
    { rect: { x: px(821), y: 0, w: px(2390), h: px(1344), fill: { color: "02080A" } } },
    { text: { text: "TELA 16:9 · 2390 x 1344 px\nslides do palestrante, câmera ou vídeo", options: { x: px(821), y: px(560), w: px(2390), h: px(224), align: "center", valign: "middle", fontFace: ROTULO, fontSize: pt(46), color: "7FB3C6", charSpacing: 4 } } },
    ph("tela", "body", 821, 0, 2390, 1344, { fontFace: CORPO, fontSize: pt(40), color: AZUL, align: "center", valign: "middle" }, "Insira aqui a imagem ou o vídeo 16:9"),
    logo(110, 570, 600),
    txt("info", 3311, 470, 601, 400, "Palestra e palestrante", { fontFace: T_MD, fontSize: pt(48), color: AZUL, valign: "middle", align: "right" }),
  ],
});

pres.defineSlideMaster({
  title: "08 Tela cheia 3:1", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    { text: { text: "IMAGEM OU VÍDEO EM TELA CHEIA\n4032 x 1344 px · proporção 3:1", options: { x: 0, y: px(560), w: 42, h: px(224), align: "center", valign: "middle", fontFace: ROTULO, fontSize: pt(54), color: "7FB3C6", charSpacing: 6 } } },
    ph("midia", "body", 0, 0, 4032, 1344, { fontFace: CORPO, fontSize: pt(40), color: AZUL, align: "center", valign: "middle" }, "Insira aqui a imagem ou o vídeo 4032 x 1344"),
  ],
});

pres.defineSlideMaster({
  title: "09 Três tópicos", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    ph("titulo", "title", 336, 150, 3360, 190, { fontFace: T_SB, fontSize: pt(120), color: GELO, valign: "middle", align: "left" }, "Título do bloco"),
  ],
});

pres.defineSlideMaster({
  title: "10 Alerta, zona de risco", background: bg("FEA-elite-fundo-alerta.jpg"),
  objects: [
    ph("titulo", "title", 336, 440, 1920, 420, { fontFace: T_SB, fontSize: pt(150), color: GELO, valign: "top", align: "left", lineSpacingMultiple: 0.95 }, "Título do alerta"),
    txt("texto", 336, 900, 1920, 240, "Texto de apoio", { fontFace: T_MD, fontSize: pt(60), color: GELO2 }),
  ],
});

pres.defineSlideMaster({
  title: "11 Citação", background: bg("FEA-elite-fundo-centro.jpg"),
  objects: [
    { image: { path: asset("FEA-elite-monograma.png"), x: px(336), y: px(400), w: px(471), h: px(400) } },
    ph("citacao", "body", 960, 290, 2740, 620, { fontFace: T_MD, fontSize: pt(104), color: GELO, valign: "middle", align: "left", lineSpacingMultiple: 1.05 }, "Citação em até três linhas"),
    txt("autor", 960, 970, 2400, 100, "AUTOR", { fontFace: ROTULO, fontSize: pt(58), color: AZUL, charSpacing: 10, valign: "middle" }),
  ],
});

pres.defineSlideMaster({
  title: "12 Intervalo", background: bg("FEA-elite-fundo-destaque.jpg"),
  objects: [
    logo(336, 170, 900),
    ph("titulo", "title", 336, 480, 2700, 330, { fontFace: T_SB, fontSize: pt(250), color: GELO, valign: "middle", align: "left" }, "Intervalo"),
    txt("retorno", 336, 840, 2700, 150, "Retornamos às 00h00", { fontFace: T_MD, fontSize: pt(96), color: AZUL, valign: "middle" }),
  ],
});

pres.defineSlideMaster({
  title: "13 QR code", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    { text: { text: "QR CODE\n864 x 864 px", options: { shape: pres.ShapeType.roundRect, rectRadius: px(28), x: px(2808), y: px(168), w: px(1008), h: px(1008), fill: { color: "EBF2F5" }, line: { type: "none" }, align: "center", valign: "middle", fontFace: ROTULO, fontSize: pt(46), color: "050C0F", charSpacing: 4 } } },
    fotoPh("qrcode", 2880, 240, 864, 864, "Insira o QR code (PNG quadrado)"),
    ph("titulo", "title", 336, 430, 2280, 420, { fontFace: T_SB, fontSize: pt(150), color: GELO, valign: "top", align: "left", lineSpacingMultiple: 0.95 }, "Chamada para ação"),
    txt("texto", 336, 900, 2280, 200, "Instrução de acesso", { fontFace: T_MD, fontSize: pt(64), color: AZUL }),
  ],
});

pres.defineSlideMaster({
  title: "14 Patrocinadores", background: bg("FEA-elite-fundo-conteudo.jpg"),
  objects: [
    txt("titulo", 336, 130, 3360, 110, "PATROCINADORES", { fontFace: ROTULO, fontSize: pt(64), color: GELO2, charSpacing: 16, align: "center", valign: "middle" }),
    ...[0, 1].flatMap((r) => [0, 1, 2, 3, 4].map((c) => slot(336 + c * 690, 330 + r * 450, 600, 360, "LOGO"))),
  ],
});

pres.defineSlideMaster({
  title: "15 Encerramento", background: bg("FEA-elite-fundo-destaque.jpg"),
  objects: [
    logo(336, 170, 900),
    ph("titulo", "title", 336, 480, 2700, 330, { fontFace: T_SB, fontSize: pt(250), color: GELO, valign: "middle", align: "left" }, "Obrigado"),
    txt("texto", 336, 840, 2700, 150, "Mensagem final", { fontFace: T_MD, fontSize: pt(96), color: AZUL, valign: "middle" }),
  ],
});

pres.defineSlideMaster({ title: "16 Guia técnico", background: { color: "050C0F" }, objects: [] });

// ---------- helpers de slide ----------
const chip = (s, texto, x, y, estilo, w) => {
  const largura = w || Math.round(texto.length * 33 + 130);
  const cheio = estilo !== "contorno";
  const cor = estilo === "alerta" ? "BB3838" : "7FB3C6";
  s.addText(texto, {
    shape: pres.ShapeType.roundRect, rectRadius: px(44), x: px(x), y: px(y), w: px(largura), h: px(88),
    fill: cheio ? { color: cor } : { color: "050C0F", transparency: 25 },
    line: cheio ? { type: "none" } : { color: "EBF2F5", width: 3 },
    margin: 0, align: "center", valign: "middle",
    fontFace: ROTULO_SB, fontSize: pt(40), color: estilo === "alerta" ? "EBF2F5" : cheio ? "050C0F" : "EBF2F5", charSpacing: 6,
    objectName: "Etiqueta " + texto,
  });
};
const vazio = (s, nome) => s.addText("", { placeholder: nome });
const detalhes = (pares) =>
  pares.flatMap(([rot, val], i) => [
    { text: rot + "  ", options: { fontFace: T_MD, color: "7FB3C6" } },
    { text: val, options: { breakLine: i < pares.length - 1 } },
  ]);

// ---------- SLIDES ----------
let s;
pres.addSection({ title: "Abertura" });

s = pres.addSlide({ masterName: "01 Abertura", sectionTitle: "Abertura" });
s.addText("TENDÊNCIAS GLOBAIS. EVIDÊNCIAS REAIS.", { placeholder: "tagline" });
s.addText("01 E 02 DE NOVEMBRO DE 2026  ·  SHERATON SÃO PAULO WTC HOTEL", { placeholder: "data" });
s.addNotes("Vinheta de abertura do Elite Injectors Congress. Logo oficial (versão clara com gradiente) fixo no layout. Tagline e data editáveis.");

s = pres.addSlide({ masterName: "02 Palestrante", sectionTitle: "Abertura" });
vazio(s, "foto");
chip(s, "PALESTRANTE", 1260, 380, "cheio");
s.addText("Dr. João Pithon", { placeholder: "nome" });
s.addText("Credenciais do palestrante em uma linha", { placeholder: "credenciais" });
s.addText([{ text: "Tema  ", options: { fontFace: T_MD, color: "7FB3C6" } }, { text: "Título da palestra em uma linha" }], { placeholder: "tema" });
s.addNotes("Duplicar este slide para cada um dos especialistas. Foto em 3:4 (756 x 1008 px ou maior na mesma proporção): clique no ícone de imagem do espaço reservado, o PowerPoint recorta sozinho. Conferir nome e credenciais com a programação oficial.");

pres.addSection({ title: "Conteúdo" });

s = pres.addSlide({ masterName: "03 Abertura de palestra", sectionTitle: "Conteúdo" });
chip(s, "PALESTRA 01", 336, 330, "cheio");
s.addText("Título da palestra em até duas linhas", { placeholder: "titulo" });
s.addText("Nome do palestrante", { placeholder: "apoio" });
s.addNotes("Abertura de cada palestra. Título com no máximo duas linhas. Trocar o número na etiqueta azul.");

s = pres.addSlide({ masterName: "09 Três tópicos", sectionTitle: "Conteúdo" });
s.addText("Título do bloco em uma linha", { placeholder: "titulo" });
[
  ["01", "Evidência", "Texto de apoio em até três linhas, com fundamento técnico."],
  ["02", "Aplicação clínica", "Texto de apoio em até três linhas, com fundamento técnico."],
  ["03", "Segurança", "Texto de apoio em até três linhas, com fundamento técnico."],
].forEach(([n, t, d], i) => {
  const x = 336 + i * (1056 + 96);
  s.addShape(pres.ShapeType.roundRect, { x: px(x), y: px(420), w: px(1056), h: px(760), rectRadius: px(20), fill: { color: CARD }, line: { color: "7FB3C6", width: 1.5, transparency: 70 }, objectName: "Card " + n });
  s.addText(n, { x: px(x + 80), y: px(480), w: px(400), h: px(150), margin: 0, fontFace: T_SB, fontSize: pt(120), color: "7FB3C6", valign: "top", objectName: "Número " + n });
  s.addText(t, { x: px(x + 80), y: px(680), w: px(896), h: px(110), margin: 0, fontFace: T_SB, fontSize: pt(78), color: GELO, valign: "top", objectName: "Tópico " + n });
  s.addText(d, { x: px(x + 80), y: px(820), w: px(896), h: px(300), margin: 0, fontFace: CORPO, fontSize: pt(52), color: "D3EAF2", valign: "top", lineSpacingMultiple: 1.1, objectName: "Texto " + n });
});
s.addNotes("Três ideias-chave lado a lado. Para dois ou quatro tópicos, apague ou duplique um card e redistribua na largura. No máximo três linhas por card.");

s = pres.addSlide({ masterName: "10 Alerta, zona de risco", sectionTitle: "Conteúdo" });
chip(s, "ZONA DE RISCO", 336, 320, "alerta");
s.addText("Título do alerta em até duas linhas", { placeholder: "titulo" });
s.addText("Descreva a estrutura, o plano anatômico e a conduta em até duas linhas.", { placeholder: "texto" });
s.addShape(pres.ShapeType.roundRect, { x: px(2496), y: px(168), w: px(1200), h: px(1008), rectRadius: px(20), fill: { color: CARD }, line: { color: "BB3838", width: 4 }, objectName: "Card de risco" });
s.addText("Estruturas em risco", { x: px(2592), y: px(270), w: px(1008), h: px(110), margin: 0, fontFace: T_SB, fontSize: pt(72), color: GELO, valign: "top", objectName: "Título do card" });
s.addText(
  [
    { text: "Estrutura vascular 1", options: { bullet: { indent: 40 }, breakLine: true } },
    { text: "Estrutura vascular 2", options: { bullet: { indent: 40 }, breakLine: true } },
    { text: "Estrutura neural 1", options: { bullet: { indent: 40 } } },
  ],
  { x: px(2592), y: px(440), w: px(1008), h: px(620), margin: 0, fontFace: CORPO, fontSize: pt(56), color: GELO, valign: "top", paraSpaceAfter: pt(30), objectName: "Lista de estruturas" }
);
s.addNotes("Só para risco crítico: o vermelho fica reservado a isso. Revisar nomes das estruturas com o palestrante antes de exibir.");

s = pres.addSlide({ masterName: "11 Citação", sectionTitle: "Conteúdo" });
s.addText("Hoje, não faltam novos produtos, novas técnicas e novos protocolos. Falta saber em quais confiar.", { placeholder: "citacao" });
s.addText("DR. JOÃO PITHON", { placeholder: "autor" });
s.addNotes("Frase da carta de boas-vindas do Dr. João no Manual do Participante. Citação com no máximo três linhas.");

pres.addSection({ title: "Casos clínicos" });

s = pres.addSlide({ masterName: "04 Antes e depois", sectionTitle: "Casos clínicos" });
vazio(s, "foto_antes"); vazio(s, "foto_depois");
chip(s, "ANTES", 376, 208, "contorno", 250);
chip(s, "DEPOIS", 1180, 208, "cheio", 270);
chip(s, "CASO CLÍNICO", 2160, 240, "contorno");
s.addText("Título do caso em até duas linhas", { placeholder: "titulo" });
s.addText(detalhes([["Região", "preencher"], ["Técnica", "preencher"], ["Plano", "preencher"], ["Intervalo", "preencher"]]), { placeholder: "detalhes" });
s.addNotes("Fotos antes e depois em 3:4, mesmo enquadramento, luz e distância. Não citar marca de produto sem aprovação. O aviso de que resultados variam por paciente é fixo no layout.");

s = pres.addSlide({ masterName: "05 Antes e depois, 2 casos", sectionTitle: "Casos clínicos" });
["c1_antes", "c1_depois", "c2_antes", "c2_depois"].forEach((n) => vazio(s, n));
[[336, "ANTES", "contorno", 250], [1140, "DEPOIS", "cheio", 270], [2136, "ANTES", "contorno", 250], [2940, "DEPOIS", "cheio", 270]].forEach(([x, t, e, w]) => chip(s, t, x + 40, 160, e, w));
s.addText("Caso 1 · região tratada", { placeholder: "legenda1" });
s.addText("Caso 2 · região tratada", { placeholder: "legenda2" });
s.addNotes("Dois casos lado a lado. Fotos em 3:4.");

s = pres.addSlide({ masterName: "06 Caso com foto complementar", sectionTitle: "Casos clínicos" });
vazio(s, "foto_antes"); vazio(s, "foto_depois"); vazio(s, "foto_extra");
chip(s, "ANTES", 376, 160, "contorno", 250);
chip(s, "DEPOIS", 1180, 160, "cheio", 270);
s.addText("Caso · região tratada", { placeholder: "legenda1" });
s.addText("Paciente no dia do procedimento", { placeholder: "legenda2" });
s.addNotes("Mesmo formato da referência enviada: par antes e depois à esquerda e uma foto horizontal à direita.");

pres.addSection({ title: "Apoio" });

s = pres.addSlide({ masterName: "07 Tela 16:9 central", sectionTitle: "Apoio" });
vazio(s, "tela");
s.addText([{ text: "Título da palestra", options: { color: "EBF2F5", fontFace: T_SB, breakLine: true } }, { text: "Nome do palestrante" }], { placeholder: "info" });
s.addNotes("Para slides dos palestrantes (16:9), câmera ao vivo ou vídeo. Janela central de 2390 x 1344 px; laterais mantêm a marca. Em mesa de corte (vMix, Resolume, ProPresenter), usar a prévia PNG deste slide como fundo e posicionar a entrada 16:9 no centro.");

s = pres.addSlide({ masterName: "08 Tela cheia 3:1", sectionTitle: "Apoio" });
vazio(s, "midia");
s.addNotes("Imagem ou vídeo no tamanho exato do painel: 4032 x 1344 px. Conteúdo 16:9 aqui fica distorcido ou cortado; para 16:9 use o layout 07.");

s = pres.addSlide({ masterName: "13 QR code", sectionTitle: "Apoio" });
vazio(s, "qrcode");
chip(s, "ACESSE AGORA", 336, 320, "cheio");
s.addText("Chamada para ação em até duas linhas", { placeholder: "titulo" });
s.addText("Aponte a câmera do celular para o QR code ao lado.", { placeholder: "texto" });
s.addNotes("Cada QR com UTM único (utm_source=palco, utm_medium=led, utm_campaign=elite-injectors-2026, utm_content=nome-do-slide) para medir acessos vindos do telão. Sem métrica, otimização é palpite. Testar a leitura a 15 metros antes de abrir as portas.");

s = pres.addSlide({ masterName: "14 Patrocinadores", sectionTitle: "Apoio" });
s.addText("PATROCINADORES", { placeholder: "titulo" });
s.addNotes("Colar os logos oficiais (PNG transparente, versão clara) sobre os espaços. Confirmar com a organização a lista e a ordem de cotas antes de exibir.");

s = pres.addSlide({ masterName: "12 Intervalo", sectionTitle: "Apoio" });
s.addText("Intervalo", { placeholder: "titulo" });
s.addText("Retornamos às 00h00", { placeholder: "retorno" });
s.addNotes("Atualizar o horário de retorno a cada intervalo, conforme o minuto a minuto.");

pres.addSection({ title: "Encerramento" });

s = pres.addSlide({ masterName: "15 Encerramento", sectionTitle: "Encerramento" });
s.addText("Obrigado", { placeholder: "titulo" });
s.addText("Ciência é o único caminho.", { placeholder: "texto" });
s.addNotes("Encerramento com o mantra do congresso.");

pres.addSection({ title: "Técnico, não exibir" });

s = pres.addSlide({ masterName: "16 Guia técnico", sectionTitle: "Técnico, não exibir" });
const LINHAS = ["A", "B", "C", "D"];
for (let r = 0; r < 4; r++) {
  for (let c = 0; c < 24; c++) {
    s.addShape(pres.ShapeType.rect, {
      x: px(c * 168), y: px(r * 336), w: px(168), h: px(336),
      fill: { color: (r + c) % 2 === 0 ? "050C0F" : "0D1B22" }, line: { color: "7FB3C6", width: 1, transparency: 70 },
    });
    s.addText(LINHAS[r] + (c + 1), { x: px(c * 168), y: px(r * 336 + 16), w: px(168), h: px(56), margin: 0, align: "center", fontFace: ROTULO, fontSize: pt(34), color: "7FB3C6" });
  }
}
s.addShape(pres.ShapeType.rect, { x: px(821), y: 0, w: px(2390), h: px(1344), fill: { type: "none" }, line: { color: "EBF2F5", width: 4, dashType: "dash" }, objectName: "Zona 16:9" });
s.addShape(pres.ShapeType.rect, { x: px(336), y: px(168), w: px(3360), h: px(1008), fill: { type: "none" }, line: { color: "7FB3C6", width: 6, dashType: "lgDash" }, objectName: "Área segura de texto" });
s.addText(
  [
    { text: "GUIA TÉCNICO · NÃO EXIBIR NO EVENTO", options: { fontFace: T_SB, fontSize: pt(64), color: "EBF2F5", breakLine: true } },
    { text: "Painel 4032 x 1344 px · proporção 3:1 · 24 x 4 módulos de 168 x 336 px", options: { breakLine: true } },
    { text: "Tracejado azul: área segura de texto (336 px nas laterais, 168 px em cima e embaixo)", options: { breakLine: true } },
    { text: "Tracejado claro: janela 16:9 central de 2390 x 1344 px" },
  ],
  {
    shape: pres.ShapeType.roundRect, rectRadius: px(20), x: px(1008), y: px(392), w: px(2016), h: px(560),
    fill: { color: "050C0F", transparency: 5 }, line: { color: "7FB3C6", width: 3 }, margin: px(48),
    fontFace: CORPO, fontSize: pt(42), color: "D3EAF2", align: "center", valign: "middle", paraSpaceAfter: pt(14), objectName: "Legenda do guia",
  }
);
s.addNotes("Slide de conferência com o operador do LED: mesma grade de módulos (A1 a D24) do teste do painel. Não exibir para o público.");

(async () => {
  await pres.writeFile({ fileName: SAIDA });
  if (!process.env.NOTHEME) await applyTheme(SAIDA, THEME);
  console.log("gerado:", SAIDA);
})();
