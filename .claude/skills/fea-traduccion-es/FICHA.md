# Ficha técnica — sistema de tradução FEA para espanhol

Resumo objetivo do que o sistema é, o que faz e sobre que base ele traduz.
Escrito para ser entendido por quem não é da área técnica.

---

## O que é

Duas ferramentas que trabalham em sequência dentro do Claude Code:

1. **`fea-traduccion-es`** — traduz.
2. **`fea-revision-es`** — revisa e libera ou retém a entrega.

Não é tradutor automático. É um processo com terminologia travada, verificação
automatizada e revisão crítica, desenhado para material clínico onde um erro de
tradução tem consequência em paciente.

## Sobre que base ela traduz

Toda a terminologia foi extraída do **material real da FEA**, não de dicionário
genérico nem de literatura de terceiros. As fontes:

| Fonte | O que forneceu |
|---|---|
| **Ebook «Preenchimento Tridimensional de Olheiras»** (74 pág.) | Terminologia de ácido hialurônico, reologia, anatomia infraorbital, ligamentos, técnica de pertuitos |
| **Ebook «Intercorrências com Preenchimento»** (30 complicações, ~20.000 palavras) | Farmacologia de emergência, doses, vias, protocolos PDRR e PithonNapoli, 30 intercorrências |
| **Planilha de produção do catálogo** | Mapa de 684 aulas em 62 módulos — usado para dimensionar o escopo |
| **Google Drive da FEA** | Classificação real dos 32 destinos de QR Code do ebook |

Termos que não vieram desse material estão **marcados como pendentes de
confirmação**. A ficha não finge cobertura que não tem.

## O que o sistema faz, em ordem

1. **Extrai o texto** do material, incluindo o que está dentro de imagens (usa
   OCR — sem isso, 194 linhas do ebook de olheiras ficariam invisíveis,
   inclusive o título da capa).
2. **Traduz** com terminologia travada por glossário, no espanhol
   latino-americano, com registro de professor de congresso.
3. **Audita por script** — 45 regras automáticas de resíduo de português,
   erro de sintaxe, falso amigo clínico, dose, via de administração e
   ortotipografia.
4. **Retraduz de volta** os trechos técnicos e compara com o original — é o
   passo que pega o erro invisível: número certo na estrutura errada, passo
   invertido, «não» perdido.
5. **Inventaria vídeos e QR Codes**, listando o que precisa de versão espanhola.
6. **Revisa** com uma segunda ferramenta independente, que não conhece as
   justificativas de quem traduziu.
7. **Libera ou retém**, e entrega a lista de pontos para análise.

## Como decide se pode entregar

Dois níveis separados, de propósito:

| Nível | O que cobre | Regra |
|---|---|---|
| **Segurança clínica** | dose, via, fármaco, plano anatômico, lado, negação, omissão | **Zero tolerância.** Um erro retém a entrega |
| **Qualidade editorial** | terminologia, estilo, pontuação | **≥ 95 % libera** · 80–95 % libera com ressalvas · < 80 % retém |

Segurança clínica **não entra em percentual**: material com 99 % e uma dose
trocada não está 99 % bom, está errado no ponto que importa.

A entrega **nunca trava por imperfeição**. Na faixa 80–95 % o material sai, com
os pontos anexos.

## O que já foi verificado na prática

| Verificação | Resultado |
|---|---|
| Ebook de olheiras traduzido | 68 páginas, 8.056 palavras em espanhol |
| Auditoria automática | **0 erro clínico · 0 grave · 0 menor — índice 100 %** |
| Defeito encontrado pelo próprio auditor | 1 erro de sintaxe na pág. 21, corrigido |
| Texto em arte levantado por OCR | 194 linhas em 29 páginas que a extração normal não via |
| QR Codes decodificados e classificados | 32 destinos: 19 vídeos a traduzir, 10 artigos que permanecem em inglês |
| Falha de barreira clínica testada | Erro de via de administração retém a entrega mesmo com índice em 100 % |

## Cobertura atual

| Área | Estado |
|---|---|
| Ácido hialurônico, reologia, olheiras | ✅ pronto |
| Intercorrências, doses, emergências | ✅ pronto |
| Anatomia facial, técnica, registro clínico, linguagem comercial | ✅ pronto (núcleo) |
| Voz nativa e estilo | ✅ pronto |
| Toxina, bioestimuladores, fios, corporais, tecnologias, dermatologia, gestão | ⬜ aguardando material com texto |

## O que ela não faz

- Não corrige a clínica do autor — discordância vira pergunta, não correção.
- Não converte dose nem unidade.
- Não traduz artigo científico citado.
- Não reescreve em silêncio: toda alteração é reportada.
- Não dubla nem legenda vídeo — **lista** o que precisa e como localizar.
