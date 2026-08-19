# Template de SOP

Usar sempre que a Keila pedir para "documentar um processo", "criar checklist" ou "montar procedimento", de qualquer cliente ou projeto, não só FEA.

```
═══ FLUXOGRAMA: [NOME DO PROCESSO] ═══
INÍCIO → [Etapa 1] → [Etapa 2] → decisão (SIM/NÃO com caminhos) → [Checkpoint] → [Etapa N] → FIM → [resultado esperado]
DEPENDÊNCIAS EXTERNAS: [etapa] depende de [pessoa/sistema/aprovação]

═══ SOP: [NOME DO PROCESSO] ═══
VERSÃO: 1.0 · DATA DE CRIAÇÃO: [data] · ÚLTIMA REVISÃO: [data]
RESPONSÁVEL PELO DOCUMENTO: [nome/cargo] · FREQUÊNCIA: [diária/semanal/mensal/por demanda]
TEMPO TOTAL ESTIMADO: [xx min/h]

── OBJETIVO ── [o que esse processo realiza, 1-2 frases]
── ESCOPO ── dentro: [...] / fora: [...]
── PRÉ-REQUISITOS ── [ ] acesso/ferramenta/login/aprovação necessários
── RESPONSÁVEIS ── executor: [...] · aprovador: [...] · ponto de dúvida: [...]

── PASSO A PASSO ──
ETAPA N: [nome] — tempo: ~X min — ferramenta: [...] — responsável: [...]
  N.1 [ação específica no imperativo] — onde: Menu > Opção > Campo
  N.2 [ação específica] — dica: [...]
  N.3 [ação específica] — atenção: [...]
  RESULTADO ESPERADO DA ETAPA: [...]

◆ CHECKPOINT (a cada 3-5 etapas): [ ] condição 1 OK? [ ] condição 2 OK?
  Se algo falhar → [voltar para etapa X / contatar Y]

◆ CHECKPOINT FINAL: [ ] resultado confere · [ ] nenhuma etapa pulada · [ ] pessoa notificada · [ ] registrado em [local]

── ERROS COMUNS ──
ERRO N: [descrição] — quando acontece: [...] — como identificar: [...] — como resolver: [...] — como prevenir: [...]

── CHECKLIST RÁPIDO (versão resumida p/ quem já conhece) ──
[ ] pré-requisito 1 [ ] pré-requisito 2
[ ] Etapa 1 (~Xmin) [ ] Etapa 2 (~Xmin) [ ] ◆ Checkpoint [ ] Etapa 3 (~Xmin)
[ ] verificação final · [ ] registro feito · [ ] pessoa notificada
TEMPO TOTAL: ~XX min

── MÉTRICAS ── tempo médio de execução · taxa de erro (meta) · ciclo de revisão (a cada 30/60/90 dias ou X execuções)
```

## Regras não-negociáveis ao aplicar este template

- Nível de detalhe para quem nunca fez o processo, nunca "configure o sistema", sempre "abra X > clique Y > preencha Z".
- Tempo estimado obrigatório em toda etapa.
- Checkpoint de qualidade a cada 3 a 5 etapas.
- Mínimo de 5 erros comuns documentados (quando acontece, como identificar, como resolver, como prevenir).
- Processo grande (20 ou mais etapas): quebrar em sub-processos com SOPs separados, o "pai" referencia os "filhos".
- Se o processo relatado for ineficiente, documentar o "como é" e sugerir o "como deveria ser".
- Processo que envolve múltiplas pessoas ou áreas: usar **Swimlane** (raia por responsável). Processo complexo com múltiplos elos: mapear **SIPOC** (Suppliers, Inputs, Process, Outputs, Customers).
- Sempre entregar os dois formatos juntos: SOP completo e checklist rápido.

Observação sobre o bloco em código: o template usa travessão como separador visual dentro do gabarito impresso. Em prosa e copy, a regra de estilo continua valendo: nada de em-dash.
