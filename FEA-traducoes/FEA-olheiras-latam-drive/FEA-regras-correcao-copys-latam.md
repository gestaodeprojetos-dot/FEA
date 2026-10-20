# FEA · Regras para traduzir e corrigir as copys do Ebook Olheiras LATAM (out/2026)

Fonte das decisões: Keila (gestão), conversa de 05/10 e 20/10/2026. Auditoria do Drive em `/tmp/claude-0/-home-user-FEA/6500f297-8601-53d4-bc7c-33986b7f95c3/scratchpad/drive-audit.md`.

## Idioma e tom
- Espanhol neutro LATAM, tratamento **usted**, seguindo a skill `/home/user/FEA/.claude/skills/fea-traduccion-es` (ler `SKILL.md`, `references/00-nucleo.md` e `references/90-decisiones.md` antes de traduzir). Termos travados: "relleno de ojeras", "inyector", "zonas de riesgo", "Más información", "intercurrencias" conforme o glossário da skill.
- Tom médico-científico, par profissional. Nada de tom motivacional ("vida épica", "libertad financiera", "transforme su vida"), nada de dor emocional pesada ("me siento una basura", "arruinarle la cara"), nada de promessa estética garantida. Reescrever esses trechos para o registro técnico (segurança, previsibilidade, raciocínio clínico, evitar intercurrencias isquémicas).
- Zero travessão (em-dash). Zero "pra" (vale para textos internos em PT).
- Emojis: só os permitidos no original e escritos corretamente (✅ ✔️ 👉 📌 etc.). Nunca deixar sequências corrompidas tipo "ð¨", "ðð½".
- E-mail no padrão Dr. João: abre "Hola, aquí el Dr. João Pithon." (ou "Olá, Dr. João Pithon aqui." traduzido), CTA `>> ACCIÓN <<`, assinatura "Un abrazo," + "Dr. João Pithon".

## Preço (definido pela gestão em 05/10/2026)
- Ebook: **de US$47 por US$19** (60 % de descuento). Onde o original tiver R$ 47, R$ 97, R$ 200, R$ 297, R$ 397 ou 76 %, usar US$19 (preço) e US$47 (preço "de", riscado) e 60 %.
- Parcelamento: não usar (ticket de US$19 é à vista). Remover "12 x R$ ...".
- Upsell: **US$97** (decisão da gestão em 20/10/2026, equivalente ao R$ 497 do Brasil). Sem parcelas.
- Nome do upsell em espanhol: **Curso de Relleno Express** (decisão 20/10/2026).
- Nunca deixar R$ nem `[PRECIO EN MONEDA LOCAL...]` no texto final.

## Números de autoridade (não definidos para LATAM)
- Decisão 20/10/2026 (gestão autorizou): usar os números da versão mais recente do Brasil (página NUEVA, 14/05/2026): **más de 30.000 alumnos**, **9 países**, **10.000 ml**; ebook **+30 mil copias vendidas**. Substituir 4.000 / 20.000 alumnos, 7 / 8 países e 7.000 ml.

## Resíduos do Brasil (remover ou trocar por marcador)
- Pix e boleto: remover; meio de pagamento = tarjeta de crédito/débito (Hotmart). Eventos de automação de Pix/boleto: remover.
- Checkout BR (`pay.hotmart.com/S97800165C...`) → `[LINK DEL CHECKOUT EN USD: PENDIENTE]`.
- WhatsApp +55 (qualquer número BR) → `[WHATSAPP DE SOPORTE LATAM: PENDIENTE]`.
- Check-in/obrigado BR (`eb.joaopithon.com.br/ebook-pto-obrigado/`) → `[LINK DE LA PÁGINA DE GRACIAS LATAM: PENDIENTE]`.
- Grupo WhatsApp BR → `[LINK DEL GRUPO LATAM: PENDIENTE]`.
- Hotmart Club `pt-br` → mesma URL com `/es/`.
- suporte@joaopithon.com.br → `[E-MAIL DE SOPORTE LATAM: PENDIENTE]`.
- "Curso de Preenchimento Express" → `[NOMBRE DEL PRODUCTO DEL UPSELL EN ESPAÑOL: A CONFIRMAR]`.
- "no solo de Brasil", "Ningún otro lugar de Brasil" → universalizar ("ningún otro programa enseña...").
- Rodapé "Formação Especialista Academy" → "Formación Especialista Academy".
- Tags de automação: prefixo `[OLHEIRAS-LATAM]`.

## Linha vermelha FEA
- Marca de produto sem aprovação (ex.: "LG en Corea"): remover. Capa Allergan nos criativos: decisão da gestão de manter (05/10), não mexer.
- Urgência: nos criativos a gestão manteve "48 horas", "SOLO HOY" (05/10). Nas **páginas**, remover cronômetro de 15 min e "por tiempo limitado" fabricado; manter só prazo real se existir.
- Imagens do original: onde o doc PT tem imagem, escrever `[IMAGEN: <descrição curta>, usar la versión ES de la carpeta 2. ARTES]`.
- Depoimentos (prints): ficam em PT na arte com legenda ES; na copy, citar como "Testimonio original en portugués".

## Formato dos docs no Drive
- Criar como Google Doc (upload `text/html` sem `disableConversionToGoogleType`), título `FEA-ES | <nome>`, na mesma pasta do doc que substitui.
- Topo do doc: bloco interno em PT "Notas para a equipe" listando marcadores pendentes e decisões aplicadas (curto). Corpo: só a copy em espanhol.
- O conector não edita doc existente: criar o novo, conferir o conteúdo com `read_file_content`, e só então mandar o antigo para a lixeira com `trash_file`.
- Registrar cada troca (id antigo → id novo, título, pasta) no JSON de mapeamento indicado na tarefa.
