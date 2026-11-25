# FEA · Diagnóstico rápido CS e Suporte: problemas x soluções do agente (25/11/2026)

Para: Grazi (Graziele Gomes de Almeida, Head de CS e Suporte). Documento só de leitura: nenhuma mensagem enviada, nada alterado em Drive, ClickUp, Hotmart ou na ferramenta.

Critério de sucesso: cada problema com um número verificável, cada solução com prazo realista e com o que depende da Grazi.

## Fontes lidas

| Fonte | Situação em 25/11 |
|---|---|
| Suporte Médico, Dr. Gian | 114 perguntas, 06/05 a 19/11/2026, última edição 23/11 |
| Suporte médico, Dr. Gustavo | 68 perguntas, 20/05 a 11/11/2026, última edição 19/11 |
| Suporte médico, Dra. Amanda | 134 perguntas, última edição 25/11 |
| Suporte médico, Dra. Laís | 250 perguntas, 03/03 a nov/2026, última edição 25/11 |
| joaopithon.com.br/suporte-medico | redireciona para uma página publicada no Claude ("Central de Dúvidas Clínicas"), com 450 registros embutidos |
| Documento da Central de Inteligência (Grazi) e análise anterior `FEA-cs-suporte-analise-pedido-grazi-2511.md` | lidos |

Método: leitura dos 4 docs exportados em texto, separação por bloco "Dúvida do aluno", classificação por palavra-chave (o modelo de formulário com "Fio de PDO?" e "teve febre?" foi descontado para não inflar categorias) e comparação de similaridade de texto entre perguntas. Contagens por tema são aproximadas (uma pergunta pode cair em mais de um tema). Nenhum dado pessoal de aluno ou paciente foi copiado para este arquivo.

## Números principais

- **566 perguntas** nos 4 docs; **25 sem resposta registrada** (Gian 4, Gustavo 1, Amanda 8, Laís 12).
- Distribuição: Laís 250 (44%), Amanda 134 (24%), Gian 114 (20%), Gustavo 68 (12%). Últimos 30 dias: **86 perguntas, 47 delas com a Dra. Laís (55%)**; últimos 7 dias: 17.
- Cursos de origem mais citados: FEP 257, FEB 77, Vitalício 97 (somando grafias), Pós 40.
- Temas mais recorrentes (perguntas que citam o tema): toxina botulínica 154, olheiras 107, edema ou inchaço 86, lábios 80, fios de PDO 57, rinomodelação 54, hialuronidase 52, nódulo pós-preenchimento 51, bioestimuladores 41, assimetria 25, ptose 16, necrose/isquemia/oclusão 15. **Todos os 12 temas aparecem nos 4 médicos.**
- Repetição de redação: **87 perguntas** têm texto muito parecido com outra (50 pares), **24 desses pares respondidos por médicos diferentes**.
- 282 perguntas (50%) são casos clínicos com fotos de antes e depois; todas as 566 trazem o nome do aluno no cabeçalho.
- Qualidade de registro: 17 perguntas com data ausente (8) ou impossível (9, ex.: ano 2916 ou data futura).
- Ferramenta: 450 registros, sendo 94 do catálogo de reologia e **356 vindos das respostas dos médicos**, contra 566 perguntas nos docs. Registro mais recente: 24/11; docs da Amanda e da Laís editados em 25/11. 31 registros já consolidam respostas de dois médicos. 16 categorias.
- Hotmart: **0 aulas indexadas por tema**; a API não devolve módulos e aulas pesquisáveis. Caso real de 25/11: "qual aula fala de flacidez após emagrecimento" (aluno da Pós) ficou sem resposta.

## Problemas x soluções

| # | Problema (evidência) | Solução do agente | Prazo | Depende da Grazi |
|---|---|---|---|---|
| 1 | Dúvida repetida volta ao médico: 87 perguntas quase iguais a outra; temas como toxina (154), olheiras (107) e hialuronidase (52) respondidos pelos 4 médicos | Consulta assistida: analista envia a dúvida, o agente devolve no formato do documento dela (resposta anterior, médico, data, fonte, aderência, se precisa de médico). Piloto com os 5 temas mais recorrentes | Piloto em 48h; todos os temas em 1 semana | Definir o grupo e o fluxo de consulta; quem valida aderência parcial (sugestão: Dra. Francine) |
| 2 | Carga concentrada: Dra. Laís com 44% do total e 55% dos últimos 30 dias | Relatório semanal agregado de volume por médico, dia e tema, para redistribuir a escala | 24h (primeira foto); semanal depois | Escala atual dos médicos |
| 3 | Ferramenta defasada e frágil: 356 registros dos médicos contra 566 perguntas, último registro 24/11, sem fonte e data visíveis por resposta, sem login nem histórico, hospedada fora do site | Auditoria de cobertura (quais perguntas dos docs não estão na base) e lista priorizada de melhorias, sem mexer em produção | Relatório de lacunas em 48h; proposta de melhoria em 1 semana | Quem mantém a ferramenta hoje e autorização da gestão para atualizar a base |
| 4 | 25 perguntas sem resposta registrada nos docs | Lista com médico, data e tema (sem nome do aluno) para cobrança na escala certa | 24h | Ok para encaminhar aos médicos |
| 5 | Registro inconsistente e com dado pessoal: 17 datas ausentes ou impossíveis; 566 perguntas com nome do aluno e 282 com fotos de paciente em docs abertos à equipe | Checklist de padrão de registro (data, médico, curso) e proposta de anonimização na base; sem alterar a formatação dos docs dos médicos | Checklist em 24h | Validar o padrão com os médicos |
| 6 | Aulas não pesquisáveis: 0 aulas indexadas por tema; pergunta sobre flacidez após emagrecimento sem resposta | Índice de aulas por tema e minutagem, a partir das transcrições ou dos arquivos de vídeo | Avaliação em 48h após receber o material; prazo final depois disso | Exportação da grade de módulos e aulas da Hotmart por produto, transcrições existentes ou acesso ao Drive da edição |
| 7 | Divergências não mapeadas: 24 pares de perguntas quase iguais respondidas por médicos diferentes, nenhum conferido | Lista lado a lado das respostas para validação médica | 48h | Quem valida (Dra. Francine ou médico responsável) |

Prazo final de cada frente só depois que a Grazi entregar os materiais e o agente avaliar o volume real.

## Limites que continuam valendo

Sem conduta nova, diagnóstico ou dose; suspeita de intercorrência vascular vai sempre para avaliação médica. Hotmart e Clint só leitura. Dados de aluno só em agregado. Nenhuma alteração na ferramenta em produção sem aprovação e teste.

## Versão WhatsApp

### Mensagem A (diagnóstico)

```
*Diagnóstico rápido · CS e Suporte Médico*

Li os 4 documentos de suporte médico e a ferramenta de suporte. O que os números mostram:

1. *Dúvida repetida volta ao médico:* 566 perguntas nos 4 documentos, 87 com texto quase igual a outra já respondida.

2. *Mesmos temas em todos os médicos:* toxina (154), olheiras (107), edema (86), hialuronidase (52) e nódulo (51) aparecem nos 4 documentos.

3. *Carga concentrada:* a Dra. Laís recebeu 44% do total e 55% das perguntas dos últimos 30 dias (47 de 86).

4. *Ferramenta defasada:* 356 respostas médicas na base contra 566 perguntas nos documentos, sem fonte e data visíveis em cada resposta.

5. *Perguntas sem resposta:* 25 sem resposta registrada.

6. *Registro inconsistente:* 17 perguntas sem data ou com data impossível, e todas trazem o nome do aluno.

7. *Aulas não pesquisáveis:* nenhuma aula da Hotmart indexada por tema; hoje não conseguimos dizer qual aula fala de flacidez após emagrecimento.

8. *Divergências não conferidas:* 24 pares de perguntas quase iguais respondidas por médicos diferentes, sem validação.
```

### Mensagem B (soluções)

```
*O que resolvo e em quanto tempo*

1. *Consulta assistida:* o analista envia a dúvida e eu devolvo a resposta anterior, o médico, a fonte e se precisa de médico.
*Prazo:* piloto com os 5 temas mais repetidos em 48h; todos os temas em 1 semana.
*Preciso de você:* definir o grupo de consulta e quem valida as respostas parciais.

2. *Mesmos temas:* base única por tema, para o analista resolver antes de acionar o médico.
*Prazo:* 1 semana.

3. *Carga dos médicos:* relatório de volume por médico, dia e tema.
*Prazo:* 24h.
*Preciso de você:* escala atual dos médicos.

4. *Ferramenta:* relatório do que está nos documentos e falta na base, com melhorias priorizadas.
*Prazo:* 48h.
*Preciso de você:* quem mantém a ferramenta hoje.

5. *Sem resposta:* lista das 25 perguntas por médico e data.
*Prazo:* 24h.

6. *Registro:* checklist padrão (data, médico, curso) e proposta de anonimização.
*Prazo:* 24h.

7. *Aulas:* índice por tema e minutagem.
*Prazo:* avaliação em 48h depois do material.
*Preciso de você:* grade de módulos e aulas da Hotmart por produto e as transcrições ou o acesso ao Drive da edição.

8. *Divergências:* respostas lado a lado para validação médica.
*Prazo:* 48h.

O prazo final de cada frente sai depois que eu receber e avaliar os materiais. 👍🏻
```
