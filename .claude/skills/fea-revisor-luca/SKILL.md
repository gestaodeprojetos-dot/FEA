---
name: fea-revisor-luca
description: Revisor obrigatório de toda entrega para o Luca Yu (estrategista dono do projeto FEA). Usar SEMPRE antes de enviar, mostrar, pedir publicação ou dizer "pronto" sobre qualquer coisa que vá ao Luca, direta ou indiretamente (página, prévia, dash, planilha, doc, copy, slide, mensagem com links). Varre marcadores ([ ], A CONFIRMAR, tbd, lorem, "(a criar"), confere coerência do texto de ponta a ponta, números com a fonte, links, escrita FEA, identidade do evento e celular/desktop. Nada com marcador vai ao ar.
---

# FEA · Revisor Luca

Origem (Keila, 26/11/2026 20h50): a página `lp.joaopithon.com.br/elite/patrocinio-2027/` foi ao ar com "[número de parcelas]" na linha de pagamento. Quem viu primeiro foi o André. Erro nosso: marcador entre colchetes nunca pode chegar ao Luca nem ir ao ar, e o texto precisa ser coerente do início ao fim.

Esta skill roda **antes** de qualquer entrega ao Luca. Página também passa pela `fea-revisor-paginas` (nota de 0 a 100); esta aqui é o portão mínimo que vale para tudo (página, doc, dash, planilha, mensagem).

## Regra de bloqueio

Qualquer item marcado **BLOQUEIA** impede o envio e o pedido de publicação. Corrige primeiro ou, se faltar dado, leva a pergunta à gestão (e ao responsável) e entrega sem o trecho, com texto neutro que não minta (ex.: "saldo parcelado" em vez de "parcelado em [n]").

## Checklist obrigatório

### 1. Varredura de marcadores (BLOQUEIA)

Rodar no conteúdo final (HTML publicado ou da prévia, texto do doc, export da planilha):

```bash
curl -sL "<URL>" -o /tmp/pagina.html   # ou o arquivo local / export txt do doc
grep -n -o -i -E '.{0,60}(\[[^]]{1,60}\]|a confirmar|\btbd\b|lorem|ipsum|\(a criar|xxx|placeholder|a definir|todo:|fixme|\{\{[^}]*\}\}|__/__).{0,40}' /tmp/pagina.html
```

- Ignorar só falsos positivos técnicos (seletores CSS como `[hidden]`, `[data-...]`, atributos em JS). Todo resto conta.
- Também procurar classes e spans de marcador no HTML (`class="tbd"`, `class="placeholder"`) e texto em cor de destaque que só existe para marcar pendência.
- Doc Google: exportar (`/export?format=txt`) e rodar o mesmo grep. Planilha: ler todas as abas.

### 2. Coerência do texto de ponta a ponta (BLOQUEIA se contradiz)

Ler a peça inteira, do topo ao rodapé, como o Luca leria, e conferir:

- **Datas:** mesma data em todo lugar (topo, contagem, FAQ, rodapé), dia da semana certo, ano certo (2026 x 2027).
- **Números:** somas fecham (itens x total, entrada + saldo = preço, economia = total menos preço), percentuais e vagas iguais em todas as seções.
- **Nomes de produto e evento:** sempre o mesmo nome (ex.: Elite Injectors Congress x Elite Experience; "Combo 2 em 1: FEB + FEBio Vitalício"), nunca um produto no lugar de outro.
- **Promessas:** nada que se contradiga (ex.: "12 meses de acesso" numa seção e "sem prazo" em outra; "presencial e gratuito" x preço; "esgotado" x "vagas abertas").
- **Público certo:** profissional habilitado, tom médico-científico, Brasil ou Latam conforme a peça (Latam 100% em espanhol, sem boleto/pix).
- **Pessoas:** "Dr. João Pithon" por extenso; responsáveis e contatos atuais.

### 3. Números conferidos com a fonte (BLOQUEIA sem fonte)

Cada número (preço, parcelas, data, vagas, alunos 52.754, países 44, ml) tem fonte citada: briefing, planilha de Links úteis, planilha central do evento, mensagem do Luca (grupo e horário). Número sem fonte não entra: pergunta antes.

### 4. Links funcionando (BLOQUEIA se quebrado)

Abrir cada link e botão: status 200, destino certo (checkout com `off=` certo, WhatsApp com número oficial e mensagem com "para", grupo do evento certo, Zoom da edição atual). Nunca link de ClickUp para o Luca. Nunca link de prévia (`workers.dev`) dentro de página publicada.

### 5. Escrita FEA (BLOQUEIA)

- Zero travessão (U+2014) e meia-risca usada como travessão.
- Nunca "pra", sempre "para".
- Sem palavra-tell, sem dois espaços seguidos.

```bash
grep -n -o -E '.{0,30}(—| pra |^pra | pras ).{0,30}' /tmp/pagina.html
```

### 6. Identidade visual do evento

Cores, fontes e componentes da sala do produto/evento (Elite, Elite Experience, Black, FEB, FEBIO, PL...). Logo certa e legível. Documento de lançamento com a identidade do evento.

### 7. Teste celular e desktop

Página ou artefato: abrir em 390 px e 1440 px (se possível também 360 e WebKit). Sem rolagem lateral, sem texto cortado, sem rosto cortado, botão visível. Prints guardados no scratchpad.

### 8. Prévia aberta antes de enviar

Abrir de fato o link que vai ser enviado (não o local), com o compartilhamento liberado para quem recebe. Só depois montar a mensagem.

## Relatório do revisor (curto)

```
Revisor Luca · <entrega> · <link>
Bloqueios: nenhum | <lista com trecho exato>
Ajustar: <lista>
Conferido: marcadores · coerência · números (fontes) · links · escrita · identidade · 390/1440 · prévia aberta
```

Só com "Bloqueios: nenhum" a entrega segue para o Gestão FEA ou para o Luca.

## Aprender com cada erro

Todo erro que o Luca, o André ou a gestão apontarem numa entrega já revisada vira uma linha nova no checklist acima (o que passou, por que passou, qual verificação pega).
