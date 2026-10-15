# FEA · Revisão ES · Parte 5 (p. 149 a 185) · Relatório do revisor

REVISÃO: Livro *Intercorrências no Preenchimento com Ácido Hialurônico*, parte 5 (cap. 4.1 final a 5.3) · 05/10/2026
Cobertura: 429 ids de `parte5-pt-es.json`, todos lidos id a id contra o PT. O cabeçalho p172_00 não está no arquivo de revisão (é o cabeçalho corrido fixo, conferido direto em `traducao/parte5-es.json`, está correto). O arquivo de revisão vem sem bullets "•" e sem `<b>`; conferi que o texto ES dele é idêntico, caractere a caractere, ao `traducao/parte5-es.json` com essas marcas removidas, logo isso não é achado.

## VEREDITO: LIBERADO

| Nível | Resultado |
|---|---|
| Classe A (barreira clínica) | **0** BLOQUEANTE |
| Classe B (índice editorial) | **97,7 %** (418 de 428 segmentos limpos) · 1,92 achado por mil palavras (10 achados / 5.218 palavras) |
| Distribuição classe B | 9 GRAVE · 1 MENOR |
| Questões ao autor | 6 (não afetam o veredito) |
| Falsos positivos do auditor | 13 (12 GRAVE + 1 MENOR), todos descartados com regra proposta abaixo |

O índice só diz que o texto está limpo; o que garante que ele diz a mesma coisa do PT são as camadas 2 e 3, descritas a seguir, que não acharam divergência.

## Camadas executadas

**Camada 1, mecânica.** `auditar.py` sobre os 429 valores ES (um por linha): LIBERADO, 0 classe A, 97,2 %, 12 GRAVE + 1 MENOR. Os 13 são falsos positivos (ver «Ajustes no auditor»).

**Camada 2, segurança clínica (id a id contra o PT).** Conferidos todos os fármacos, doses, unidades, posologias, vias e durações: amoxicilina/ácido clavulánico 875/125 mg cada 12 h (7 a 10 e 10 a 14 días), metronidazol 400 mg cada 8 h, ceftriaxona 1 a 2 g/día IV, piperacilina/tazobactam 4,5 g cada 6 h IV, meropenem 1 g cada 8 h, prednisona 20 a 40 mg/día (3 a 5 e 5 a 7 días), triamcinolona 10 mg/mL intralesional cada 4 a 6 semanas, aciclovir 400 mg VO 3x/día e 2x/día (profilaxia 2 días antes, 5 a 7 días), valaciclovir 500 mg VO 2x/día e 1x/día, famciclovir 250 mg VO 2x/día, aciclovir crema al 5 % 5x/día, aciclovir IV 5 mg/kg cada 8 h, hialuronidasa 10 a 30 UTR, clorhexidina al 0,12 % 2x al día por 7 días, aguja de 18 G. Comparação automática de todos os números PT × ES: a única diferença é a conversão autorizada `12/12h → cada 12 h` (e 8/8, 6/6). EV → IV aplicado em p149_11, p149_12, p154_03, p170_11. Grafias obrigatórias corretas (triamcinolona, ácido clavulánico, carbapenémicos). Negações conferidas por varredura e leitura (no presenta, no fluctuante, no nodular, sin pus, sin vesículas, evitar antibióticos empíricos salvo…, solo en colecciones…, no es/fue necesaria la sutura, siempre que no haya riesgo). Lados e sentidos: p174_14 (inferior o medial), p175_03 (lateral o inferior), p175_05 (inferior), p183_04 (por encima / justo debajo), p185_03 (izquierdo/derecho, arriba/izquierda/derecha) todos preservados. Plano e camada: supraperióstico não aparece; «subcutáneo», «dermis», «capas», «planos superficiales» preservados. **Nenhuma divergência.**

**Camada 3, back-translation** dos trechos técnicos (fisiopatologia do abscesso e do granuloma, mecanismo de BDDE/DVS e «llave-cerradura» no ETIP, fisiopatologia do HSV-1, mecanismos de migração, técnica de drenagem com agulha 18 G, anatomia do edema órbito-malar com ligamento retenedor orbitario e cigomático-cutáneo, critérios de seleção reológica em p184_03). A retradução reproduz o PT em estrutura, ordem de passos e relação causal. Destaque: em p184_03 «partículas mayores y menor grado de reticulación» e «baja concentración de ácido hialurónico» voltam exatamente como no PT; em p183_04 a ordem «piel, músculo orbicular y, justo debajo, bolsas de grasa orbitaria profundas» está intacta.

**Camada 3b, mídia e QR.** A parte 5 não tem QR nem destino de vídeo na camada de texto, nem link anotado no PDF (p. 149 a 185; `inventario_midia.py original.pdf` não retorna ativo nessa faixa), e a planilha `FEA-Traducao-ES-Intercorrencias-Aulas-e-QR.xlsx` não tem linha para essas páginas. O único link é o do artigo científico na Figura 49 (PMC12439020), que se conserva. Nada a inventariar.

**Camada 4, voz nativa.** Texto de registro culto, passiva refleja e imperativo formal coerentes, sem tuteo. Conectores variados (por lo general 9×, sobre todo 5×, en especial 3×, además 1×, por lo tanto 1×); nenhum vício repetitivo. Hifenizações entre páginas (encap-/sulada, alopuri-/nol, significa-/tivamente) e capitular «L/as» resolvidas corretamente. O único ponto de consistência terminológica relevante é «relleno» × «producto de relleno» para *preenchedor* (achados GRAVE abaixo).

## Achados

Formato: `id | severidade | trecho ES | problema | correção proposta (texto ES completo do id corrigido)`

### BLOQUEANTE

Nenhum.

### GRAVE (inconsistência interna: *preenchedor* traduzido ora como «producto de relleno», ora como «relleno»)

O glossário núcleo fixa *preenchedor → producto de relleno* e *preenchimento → relleno*. A parte segue a regra em 19 ids e se afasta dela nos 9 abaixo, com o caso mais visível em p166_02, onde as duas formas aparecem no mesmo parágrafo. Nenhum caso muda o sentido clínico, já que «relleno dérmico» é uso corrente em espanhol para o produto. **Correção mais barata e recomendada:** registrar em `90-decisiones.md` que «relleno(s) dérmico(s)» é aceito para *preenchedor(es) dérmico(s)* e que «relleno» isolado é aceito para o produto quando o contexto não admite leitura de procedimento. Com essa decisão, os 9 achados caem. Se o autor preferir a uniformização estrita, os textos corrigidos são estes:

p152_06 | GRAVE | «acumulación de relleno» | *preenchedor* como «relleno», fora do padrão do glossário | Región malar y surco nasolabial: áreas propensas a edema y acumulación de producto de relleno.

p156_03 | GRAVE | «degradación del relleno» | idem | Respuesta inflamatoria estéril a productos de degradación del producto de relleno (ácido hialurónico fragmentado).

p165_05 | GRAVE | «aplicación de rellenos dérmicos» | idem | El edema tardío intermitente persistente (ETIP) es una intercurrencia no isquémica tardía caracterizada por episodios recurrentes de edema en el área tratada, que pueden surgir de semanas a meses después de la aplicación de productos de relleno dérmico. Se trata de un cuadro de naturaleza inflamatoria, por lo general autolimitado, pero que puede generar molestias al paciente y preocupación clínica, en especial por su recurrencia y por la dificultad de identificar un único factor desencadenante.

p166_02 | GRAVE | «con rellenos dérmicos … del producto de relleno» | as duas formas no mesmo parágrafo | El edema tardío intermitente persistente (ETIP) es una intercurrencia observada tras procedimientos estéticos con productos de relleno dérmico, en particular los de ácido hialurónico. Su etiología puede relacionarse con dos factores principales: la composición química del producto de relleno y la respuesta inmunológica del paciente.

p166_03 | GRAVE | «en los rellenos … Los rellenos con menor cantidad» | idem | En primer lugar, se cree que la presencia de agentes reticulantes, como el BDDE (1,4-butanodiol diglicidil éter) y la DVS (divinilsulfona), en el ácido hialurónico puede desencadenar una respuesta inflamatoria crónica. Cuanto mayor es la concentración de residuos de estos agentes en los productos de relleno, más pronunciada puede ser la respuesta inflamatoria, lo que conduce al ETIP. Los productos con menor cantidad de residuos de estos agentes están menos modificados y, por lo tanto, son menos propensos a inducir inflamación.

p166_04 | GRAVE | «contra el relleno … reaccionan con el relleno» | idem | Además, las infecciones bacterianas o virales pueden actuar como desencadenantes del ETIP. Se cree que, en casos de inmunosupresión o desequilibrio inmunológico, el organismo puede iniciar una respuesta inmunológica contra el producto de relleno mediante un mecanismo de “llave-cerradura”, en el que los anticuerpos formados para combatir una infección también reaccionan con el producto y causan los signos inflamatorios.

p167_04 | GRAVE | «procedimiento con relleno dérmico» | idem | Figura 51. Imágenes clínicas que muestran episodios de edema recurrente en región labial tras un procedimiento con producto de relleno dérmico. Se observa aumento de volumen difuso, con discreto eritema, compatible con un cuadro de edema tardío intermitente persistente (ETIP), caracterizado por una respuesta inflamatoria no infecciosa, de inicio tardío y evolución recurrente. Fuente: archivo personal / banco de imágenes de los autores.

p173_04 | GRAVE | «procedimientos con rellenos dérmicos» | idem | En este contexto, manifestaciones como la migración del ácido hialurónico, la formación de nódulos, el edema persistente, las alteraciones pigmentarias y los efectos ópticos, como el efecto Tyndall, reflejan no solo la interacción entre producto y tejido, sino también la precisión técnica de la aplicación. Comprender estos fenómenos es fundamental para un diagnóstico adecuado, un manejo correcto y la prevención de resultados estéticos indeseables, con mayor previsibilidad y seguridad en los procedimientos con productos de relleno dérmico.

p184_02 | GRAVE | «producto de relleno en exceso … los rellenos tienen mayor longevidad» | as duas formas no mesmo parágrafo | En muchos casos, el fenómeno se relaciona con la presencia de producto de relleno en exceso o inadecuado para la región. Esto ocurre porque, en la región infraorbitaria, estos productos tienen mayor longevidad debido a las características anatómicas locales y permanecen activos durante años.

### MENOR

p170_05 | MENOR | «Indicar que evite la manipulación» | sem o objeto «al paciente», o sujeito de «evite» fica indeterminado; destoa de p177_12, que traz «Indicar al paciente que no masajee…» | Indicar al paciente que evite la manipulación y el contacto directo (riesgo de autoinoculación o transmisión).

## Pontos para análise (ordenados por custo de não corrigir)

1. **«relleno» × «producto de relleno»** (9 ids acima). Maior custo porque o padrão se repete nas partes seguintes; resolver por decisão de glossário antes da parte 6.
2. **Notação de frequência «3x/día», «2x/día», «1x/día», «5x/día», «2x al día»** (p169_23, p169_24, p169_25, p170_03, p170_09, p170_10, p182_05). Não é erro e espelha a variação do próprio PT («2x/dia» e «2x ao dia»), por isso não contei como achado. A forma mais nativa em texto clínico hispano é «3 veces al día» ou «cada 8 h». Proponho decisão de glossário (abaixo) e aplicação uniforme no livro todo de uma vez, não só nesta parte.
3. **p170_05** (MENOR acima), correção de uma linha.

## Questões ao autor (não afetam o veredito)

[1] p149_12 e p154_05 · Piperacilina/tazobactam **4,5 g cada 6 h** nesta parte; o módulo 15 do glossário registra 3,375 g para outro trecho do livro. A tradução está fiel ao PT. Confirmar se a diferença entre capítulos é intencional (as duas posologias existem na prática, mas o leitor vai notar).

[2] p175_12 · «sombra bajo los ojos (“efecto Tyndall”)». O efeito Tyndall é descrito na literatura como coloração azulada, não como sombra. A tradução é fiel; o ponto é do original.

[3] p162_16 · «Triamcinolona 10 mg/mL, diluida» sem concentração final nem volume (e p159_06 cita triamcinolona sem dose). Fiel ao PT, mas incompleto como protocolo.

[4] p168_03 (Figura 52) e p177_06 (Figura 53) · Fontes declaradas como «Adaptado por IA». A regra FEA proíbe imagem clínica gerada ou adaptada por IA generativa em entregável final. Em p177_06 a fonte é ainda «imagen de caso clínico disponible en búsqueda en internet», o que levanta questão de direito de uso e de autorização do paciente. Decisão editorial do autor, vale para o original PT também.

[5] p182_05 e p185_03 · Marcas citadas no texto e nas legendas (Periogard, Juvederm Volbela®). A regra FEA pede aprovação para menção de marca de ácido hialurônico; vale confirmar, e checar se o nome comercial do enxaguatório é o mesmo nos mercados LatAm-alvo. Na mesma linha, p170_13 cita «dipirona», nome usado em parte da América Latina; no México e na Colômbia o uso corrente é «metamizol». Sugestão: «metamizol (dipirona)».

[6] p185_03 · Referência Cavallieri et al. com páginas «218-2222» (provável 218-222). Referência não se traduz nem se corrige na tradução; corrigir no original se confirmado.

## Propostas de glossário

| Termo | Proposta | Onde registrar |
|---|---|---|
| preenchedor dérmico | aceitar «relleno dérmico» como equivalente de «producto de relleno dérmico»; «relleno» isolado aceito para o produto quando não houver ambiguidade com o procedimento | `90-decisiones.md` |
| 3x/dia, 2x/dia, 2x ao dia | «3 veces al día», «2 veces al día» (ou manter «Nx/día» como decisão registrada, uniforme em todo o livro) | `15-intercurrencias.md` §6 e `90-decisiones.md` |
| ultrassom (exame) / ultrassonográfico | «ecografía» / «ecográfico» (usado de forma consistente nesta parte; distinguir de «ultrasonido microenfocado», que é tecnologia) | `15-intercurrencias.md` |
| abscesso estéril, necrose liquefativa, sinais flogísticos, multisseptado, partes moles, coleção purulenta | absceso estéril, necrosis licuefactiva, signos flogísticos, multitabicado, partes blandas, colección purulenta | `15-intercurrencias.md` §4 |
| dipirona | «metamizol (dipirona)» na 1ª ocorrência | `15-intercurrencias.md` §6 |
| festoon | conservar em inglês entre aspas, como no PT; considerar glosa «(bolsa malar)» na 1ª ocorrência | `15-intercurrencias.md` |

## Ajustes no auditor (`auditar.py`)

| Falso positivo | Ocorrências | Regra proposta |
|---|---|---|
| «decimal com ponto» em numeração de seção | 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3 (8) | ignorar `^\d+\.\d+(\.\d+)?\s+[A-ZÁÉÍÓÚÑ]` (número de seção seguido de título em maiúscula) |
| «el mismo» como pronome | p161_07, p169_13, p175_15 («en el mismo sitio») (3) | tratar `el mismo` / `la misma` seguido de substantivo como uso adjetival; no mínimo acrescentar `sitio|lugar|punto|paciente|día|plano` à lista de exceção |
| «decimal com ponto» e «aspas retas» em referência bibliográfica | p185_03 (volume «9.3» e título entre aspas retas) (2) | ignorar o trecho a partir de `Fuente: adaptado de` quando seguido de padrão de citação (`et al.`, ano entre parênteses, `: \d+-\d+`) |
