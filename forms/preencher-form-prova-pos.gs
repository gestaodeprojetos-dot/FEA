/**
 * PREENCHE O GOOGLE FORMS DA PROVA DA POS — TECNICAS INJETAVEIS
 * Mentoria Imparavel — Pithon Napoli Experience
 *
 * Este script pega o SEU formulario em branco e insere as 40 questoes,
 * ja como questionario (quiz) autocorrigivel, com gabarito e explicacao.
 * As respostas dos alunos caem numa planilha vinculada.
 *
 * ---------------------------- COMO RODAR ----------------------------
 * 1. Abra  script.google.com  ->  Novo projeto
 * 2. Apague o conteudo padrao e cole ESTE arquivo inteiro
 * 3. No topo, selecione a funcao  preencherFormulario  e clique em Executar
 * 4. Autorize quando o Google pedir. Se aparecer "app nao verificado",
 *    clique em  Avancado  ->  Acessar o projeto (nao seguro)
 *    — e o seu proprio script, na sua conta
 * 5. Ao terminar, os links aparecem no Log (Ctrl+Enter) e chegam por e-mail
 *
 * Nao precisa editar nada para rodar. O ID do formulario em branco e o da
 * pasta ja estao preenchidos abaixo.
 * --------------------------------------------------------------------
 */

// ============================== CONFIG ==============================

var CONFIG = {

  // Formulario EM BRANCO que voce criou. O script escreve dentro dele.
  FORM_ID: '1NI4fXMCdU0efDH2hop9IbD9HPjd9ocCE_2fYgeoRMOI',

  // Se nao conseguir abrir o FORM_ID acima (conta errada, sem permissao de
  // edicao, ID invalido), cria um formulario NOVO em vez de parar com erro.
  // Deixe true para a prova sair de qualquer jeito.
  CRIAR_NOVO_SE_FALHAR: true,

  // Pasta "Diretorio do Formulario". O formulario e a planilha vao para ca.
  FOLDER_ID: '1P5Rl4qnDru-Wjk3hIDr9Q7UwFbN0d5Bp',

  // Identificador da turma/curso. Entra no titulo e no cabecalho.
  ID_POS: 'POS-TI-2026',

  TITULO_BASE: 'Prova Final — Pós-Graduação em Técnicas Injetáveis',

  PONTOS_POR_QUESTAO: 1,

  // ATENCAO: true apaga tudo o que ja existe no formulario antes de
  // escrever. Como o formulario esta em branco, e o comportamento certo.
  // Se um dia voce editar a prova a mao e rodar de novo, isso sobrescreve.
  LIMPAR_ANTES: true,

  // Secao inicial pedindo nome / CPF / turma
  INCLUIR_IDENTIFICACAO: true,

  COLETAR_EMAIL: true,

  // Exige login Google e 1 resposta por aluno.
  // Em conta Gmail comum pode nao ser aceito — o script avisa e segue.
  EXIGIR_LOGIN: true,

  EMBARALHAR_QUESTOES: false,

  // Uma pagina por bloco tematico (7 blocos). false = tudo numa pagina so.
  QUEBRA_POR_BLOCO: true,

  // Cria e vincula a planilha de respostas
  CRIAR_PLANILHA_RESPOSTAS: true,

  // Move formulario e planilha para FOLDER_ID
  MOVER_PARA_PASTA: true
};

// ========================= IMAGENS (opcional) =======================
/**
 * Mapa: numero da questao -> ID de uma imagem (PNG/JPG) no Drive.
 * Pegue o ID na URL:  drive.google.com/file/d/<<ID>>/view
 * Deixe {} para gerar sem imagens.
 *
 * LIMITACAO DO GOOGLE: o Apps Script nao anexa imagem DENTRO do bloco da
 * pergunta. A imagem entra como item logo ACIMA da questao, com legenda.
 *
 * Material de apoio ja existente na planilha de aulas, util para recortar:
 *   Q1-Q5    "Fisiologia do envelhecimento e anatomia facial" / "Anatomia facial completa"
 *   Q11-Q16  "Introducao ao preenchimento e industrializacao do AH"
 *   Q17-Q24  "Raciocinio clinico para o preenchimento de ..." (10 PDFs)
 *   Q25-Q31  "Amaurose - Protocolo" / "Complicacoes agudas isquemicas"
 *   Q32-Q36  "Estrutura quimica da polidioxanona"
 */
var IMAGENS = {
  // 18: 'COLE_AQUI_O_ID_DA_IMAGEM',
};

// ========================== DADOS DA PROVA ==========================

var QUESTOES = [
  {
    "n": 1,
    "bloco": "BLOCO I — ANATOMIA E FISIOLOGIA DO ENVELHECIMENTO",
    "stmt": "Uma paciente de 55 anos queixa-se de aprofundamento progressivo do sulco nasolabial e sensação de \"queda\" da face média. Ao exame, observa-se projeção malar reduzida, alargamento da abertura piriforme e retrusão do terço médio, com pele de boa qualidade e sem excesso cutâneo importante.\nConsiderando a fisiologia do envelhecimento facial, assinale a alternativa mais adequada:",
    "opts": {
      "A": "O sulco nasolabial deve ser preenchido diretamente com grande volume de produto de alto G', pois a causa primária é a perda de volume no próprio sulco.",
      "B": "O envelhecimento facial é predominantemente cutâneo, de modo que apenas bioestimuladores e tecnologias resolveriam o quadro.",
      "C": "O tratamento deve iniciar obrigatoriamente pelo terço inferior, pois o envelhecimento progride sempre no sentido caudocranial.",
      "D": "A reabsorção óssea não é relevante após os 50 anos, pois o pico de perda mineral ocorre apenas na sétima década.",
      "E": "A reabsorção óssea maxilar e o alargamento da abertura piriforme reduzem o suporte estrutural do terço médio; o planejamento deve priorizar a reposição de suporte profundo antes de abordar o sulco diretamente."
    },
    "gab": "E",
    "exp": "O envelhecimento facial é multifatorial e ocorre em todas as camadas — óssea, ligamentar, muscular, gordurosa e cutânea. A reabsorção da maxila, o aumento do ângulo da abertura piriforme e a retrusão do terço médio reduzem o suporte estrutural, e o sulco nasolabial é consequência dessa perda. Tratar o sulco isoladamente com grandes volumes gera resultado artificial e peso na face média; o raciocínio correto é repor suporte profundo (área malar, piriforme) e só então refinar o sulco."
  },
  {
    "n": 2,
    "bloco": "BLOCO I — ANATOMIA E FISIOLOGIA DO ENVELHECIMENTO",
    "stmt": "Sobre os compartimentos de gordura facial e sua importância no planejamento do preenchimento full face, assinale a alternativa correta:",
    "opts": {
      "A": "A gordura facial é uma camada única e homogênea, o que permite aplicação de produto em qualquer plano com resultado equivalente.",
      "B": "Os septos entre compartimentos não têm relevância clínica, já que o produto se difunde livremente entre eles.",
      "C": "Os compartimentos profundos devem ser evitados por serem avasculares e não responderem ao preenchimento.",
      "D": "A reposição volumétrica deve ser sempre superficial, pois o compartimento profundo não influencia a projeção facial.",
      "E": "A gordura facial organiza-se em compartimentos superficiais e profundos separados por septos; o envelhecimento cursa com atrofia dos compartimentos profundos e ptose/pseudo-hipertrofia dos superficiais, orientando reposição preferencialmente profunda."
    },
    "gab": "E",
    "exp": "A gordura facial é compartimentalizada, com compartimentos superficiais e profundos delimitados por septos e ligamentos de retenção. Com o envelhecimento há atrofia seletiva dos compartimentos profundos (como o deep medial cheek fat e o compartimento suborbicular) e descida dos superficiais, o que gera perda de projeção e acúmulo em regiões inferiores. Por isso a reposição estrutural é preferencialmente profunda, com refinamento superficial pontual."
  },
  {
    "n": 3,
    "bloco": "BLOCO I — ANATOMIA E FISIOLOGIA DO ENVELHECIMENTO",
    "stmt": "Durante o planejamento de um procedimento na região temporal, o conhecimento dos planos anatômicos é determinante para a segurança. Assinale a alternativa correta:",
    "opts": {
      "A": "A região temporal é considerada área de baixo risco, pois não apresenta estruturas vasculares relevantes.",
      "B": "A artéria temporal superficial corre profundamente ao músculo temporal, tornando o plano subcutâneo o de maior risco vascular.",
      "C": "A aplicação deve ser sempre realizada no plano intramuscular, por ser o único plano com ausência de vasos.",
      "D": "A região temporal apresenta múltiplos planos (subcutâneo, fáscia temporal superficial com a artéria temporal superficial, fáscia temporal profunda e plano supraperiosteal); o plano supraperiosteal profundo e o subdérmico superficial são os habitualmente utilizados, com aspiração e técnica cuidadosa.",
      "E": "O plano supraperiosteal deve ser evitado por estar em contato direto com a artéria temporal superficial."
    },
    "gab": "D",
    "exp": "A região temporal é anatomicamente estratificada: pele, subcutâneo, fáscia temporal superficial (onde trafega a artéria temporal superficial), fáscia temporal profunda, músculo temporal e plano supraperiosteal. Os planos mais utilizados com segurança são o supraperiosteal profundo (com agulha perpendicular até o osso) e o subdérmico superficial com cânula. O plano intermediário, onde corre a artéria temporal superficial e há comunicações com o sistema oftálmico, é o de maior risco."
  },
  {
    "n": 4,
    "bloco": "BLOCO I — ANATOMIA E FISIOLOGIA DO ENVELHECIMENTO",
    "stmt": "Uma paciente de 40 anos apresenta olheira profunda com sulco lacrimal marcado. Sobre a anatomia da região infraorbitária aplicada ao preenchimento, assinale a alternativa correta:",
    "opts": {
      "A": "O ligamento orbicular retentor não influencia a formação do sulco lacrimal, sendo a olheira exclusivamente pigmentar.",
      "B": "A artéria angular e o forame infraorbitário não representam risco nessa região, dispensando cuidados técnicos.",
      "C": "A região deve ser preenchida superficialmente com produto de alto G' para maior sustentação e durabilidade.",
      "D": "O sulco lacrimal decorre da aderência do ligamento orbicular retentor associada à atrofia do compartimento suborbicular; o preenchimento deve ser profundo, supraperiosteal, com pequenos volumes e produto de baixo swelling factor.",
      "E": "A presença de bolsas de gordura herniadas é indicação preferencial para grandes volumes de preenchedor na região."
    },
    "gab": "D",
    "exp": "O sulco lacrimal resulta da aderência do ligamento orbicular retentor somada à atrofia do compartimento gorduroso suborbicular e à perda de suporte ósseo. O preenchimento deve ser profundo (supraperiosteal), com volumes pequenos e produto de baixo G' e baixo swelling factor, para evitar edema persistente, efeito Tyndall e irregularidades. Bolsas herniadas volumosas são, em geral, indicação cirúrgica e não de preenchimento."
  },
  {
    "n": 5,
    "bloco": "BLOCO I — ANATOMIA E FISIOLOGIA DO ENVELHECIMENTO",
    "stmt": "Sobre a anatomia vascular do nariz e sua implicação na rinomodelação, assinale a alternativa correta:",
    "opts": {
      "A": "A vascularização nasal é terminal e independente do sistema carotídeo interno, o que elimina o risco de amaurose.",
      "B": "A aplicação em ponta e asa nasal é a mais segura, por serem regiões de vascularização abundante e colateral.",
      "C": "O maior risco vascular está na base da columela, região sem anastomoses com o sistema oftálmico.",
      "D": "A artéria dorsal do nariz e os ramos da artéria angular apresentam anastomoses com o sistema oftálmico, tornando a rinomodelação um dos procedimentos de maior risco de complicação isquêmica grave, incluindo amaurose.",
      "E": "O uso de cânula elimina completamente o risco vascular na rinomodelação."
    },
    "gab": "D",
    "exp": "O dorso nasal é irrigado pela artéria dorsal do nariz (ramo da oftálmica, do sistema carotídeo interno) e por ramos da artéria angular, com rica rede anastomótica com o sistema oftálmico. Isso torna a rinomodelação um procedimento de alto risco para embolização retrógrada e amaurose. A técnica segura envolve plano supraperiosteal/supracondral na linha média, pequenos volumes, injeção lenta, baixa pressão e aspiração — e a ponta e as asas nasais são áreas de risco elevado, não reduzido."
  },
  {
    "n": 6,
    "bloco": "BLOCO II — TOXINA BOTULÍNICA: BASES BIOQUÍMICAS E FARMACOLÓGICAS",
    "stmt": "Sobre o mecanismo de ação da toxina botulínica tipo A, assinale a alternativa correta:",
    "opts": {
      "A": "A toxina bloqueia diretamente os receptores nicotínicos pós-sinápticos, impedindo a ligação da acetilcolina.",
      "B": "A toxina promove destruição irreversível da placa motora, o que explica a permanência do efeito.",
      "C": "A toxina age bloqueando os canais de cálcio voltagem-dependentes, sem interferir no complexo SNARE.",
      "D": "A toxina inibe a síntese de acetilcolina no corpo neuronal, reduzindo sua disponibilidade.",
      "E": "A toxina atua na clivagem da proteína SNAP-25, componente do complexo SNARE, impedindo a fusão das vesículas e a liberação de acetilcolina na fenda sináptica."
    },
    "gab": "E",
    "exp": "A toxina botulínica tipo A liga-se seletivamente ao terminal nervoso colinérgico, é internalizada e sua cadeia leve cliva a SNAP-25, proteína do complexo SNARE responsável pela ancoragem e fusão das vesículas de acetilcolina à membrana pré-sináptica. Sem a liberação do neurotransmissor, não há contração muscular. O efeito é temporário: ocorre brotamento axonal e regeneração da placa motora, o que restabelece a função."
  },
  {
    "n": 7,
    "bloco": "BLOCO II — TOXINA BOTULÍNICA: BASES BIOQUÍMICAS E FARMACOLÓGICAS",
    "stmt": "Sobre a estrutura molecular e as propriedades bioquímicas da toxina botulínica, assinale a alternativa correta:",
    "opts": {
      "A": "A molécula ativa é formada por uma cadeia pesada, responsável pela ligação ao terminal nervoso e internalização, e uma cadeia leve, com atividade enzimática sobre as proteínas SNARE, podendo estar associada a proteínas acessórias complexantes.",
      "B": "A toxina é composta por uma cadeia única, sem subunidades funcionais distintas.",
      "C": "As proteínas complexantes são responsáveis pela atividade enzimática da toxina.",
      "D": "A cadeia leve é responsável pela ligação ao receptor pré-sináptico e a cadeia pesada pela clivagem da SNAP-25.",
      "E": "O peso molecular do complexo é irrelevante do ponto de vista clínico e imunológico."
    },
    "gab": "A",
    "exp": "A neurotoxina é uma proteína di-cadeia: a cadeia pesada (~100 kDa) faz o reconhecimento do receptor no terminal colinérgico e a translocação, e a cadeia leve (~50 kDa) é uma metaloprotease zinco-dependente que cliva a SNAP-25. As proteínas complexantes (hemaglutininas e não-hemaglutininas) protegem a molécula, mas não têm atividade enzimática; a carga proteica total é um dos fatores discutidos na imunogenicidade e formação de anticorpos neutralizantes."
  },
  {
    "n": 8,
    "bloco": "BLOCO II — TOXINA BOTULÍNICA: BASES BIOQUÍMICAS E FARMACOLÓGICAS",
    "stmt": "Sobre a reconstituição e o manuseio da toxina botulínica, assinale a alternativa correta:",
    "opts": {
      "A": "A reconstituição deve ser feita com água destilada, pois o soro fisiológico inativa a molécula.",
      "B": "A agitação vigorosa do frasco é recomendada para garantir a homogeneização completa do produto.",
      "C": "A diluição não interfere na área de difusão do produto, sendo indiferente o volume utilizado.",
      "D": "A reconstituição é realizada com soro fisiológico 0,9%, injetado lentamente pela parede do frasco, com homogeneização suave; maiores diluições aumentam a área de difusão e podem ser úteis em técnicas superficiais, enquanto menores diluições favorecem maior precisão pontual.",
      "E": "Após reconstituída, a toxina perde totalmente a atividade em duas horas, devendo ser descartada nesse intervalo."
    },
    "gab": "D",
    "exp": "A reconstituição é feita com solução fisiológica 0,9%, deixando o vácuo do frasco aspirar o diluente ou injetando-o lentamente pela parede, evitando espuma. A agitação vigorosa pode desnaturar a proteína. O volume de diluição é uma ferramenta clínica: diluições maiores ampliam a difusão (úteis em mesobotox, espasmos e hiperidrose), enquanto diluições menores concentram o efeito e aumentam a precisão em músculos específicos."
  },
  {
    "n": 9,
    "bloco": "BLOCO II — TOXINA BOTULÍNICA: BASES BIOQUÍMICAS E FARMACOLÓGICAS",
    "stmt": "Sobre a fisiologia da contração muscular e sua relação com a ação da toxina, assinale a alternativa correta:",
    "opts": {
      "A": "O influxo de cálcio no terminal pré-sináptico é dispensável para a liberação de acetilcolina.",
      "B": "A contração muscular independe da interação actina-miosina quando há bloqueio colinérgico.",
      "C": "A acetilcolina atua diretamente sobre o retículo sarcoplasmático, sem intermediação de receptores de membrana.",
      "D": "A toxina impede a despolarização da fibra muscular, sem qualquer relação com a liberação vesicular.",
      "E": "O potencial de ação despolariza o terminal, abre canais de cálcio voltagem-dependentes e o influxo de cálcio desencadeia a fusão das vesículas mediada pelo complexo SNARE, com liberação de acetilcolina — etapa exatamente onde a toxina interfere."
    },
    "gab": "E",
    "exp": "A sequência fisiológica é: potencial de ação → despolarização do terminal → abertura de canais de cálcio voltagem-dependentes → influxo de cálcio → fusão vesicular mediada pelo complexo SNARE (SNAP-25, sintaxina e VAMP) → liberação de acetilcolina → ligação aos receptores nicotínicos → despolarização da fibra → liberação de cálcio do retículo sarcoplasmático → interação actina-miosina. A toxina atua precisamente na etapa de fusão vesicular, ao clivar a SNAP-25."
  },
  {
    "n": 10,
    "bloco": "BLOCO II — TOXINA BOTULÍNICA: BASES BIOQUÍMICAS E FARMACOLÓGICAS",
    "stmt": "Sobre indicações e contraindicações do uso de toxina botulínica, assinale a alternativa correta:",
    "opts": {
      "A": "A miastenia gravis e a síndrome de Eaton-Lambert são contraindicações, assim como infecção ativa no local de aplicação; o uso de aminoglicosídeos pode potencializar o efeito da toxina e deve ser considerado na anamnese.",
      "B": "A gestação é uma indicação segura, desde que utilizadas doses reduzidas.",
      "C": "Doenças neuromusculares não representam contraindicação, pois a toxina age apenas localmente e sem repercussão sistêmica.",
      "D": "O uso concomitante de aminoglicosídeos reduz o efeito da toxina, exigindo aumento das doses.",
      "E": "A presença de infecção ativa no sítio de aplicação não contraindica o procedimento, desde que se utilize antissepsia rigorosa."
    },
    "gab": "A",
    "exp": "São contraindicações ao uso da toxina: doenças da junção neuromuscular (miastenia gravis, síndrome de Eaton-Lambert, esclerose lateral amiotrófica), hipersensibilidade a componentes da fórmula, infecção ativa no local de aplicação, gestação e lactação (por ausência de estudos de segurança). Aminoglicosídeos e outros agentes que interferem na transmissão neuromuscular podem potencializar o efeito da toxina, o que deve ser identificado na anamnese."
  },
  {
    "n": 11,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Um paciente masculino de 45 anos deseja definição de mandíbula e projeção de mento. Considerando as propriedades reológicas dos preenchedores, assinale a alternativa mais adequada:",
    "opts": {
      "A": "Deve-se optar por produto de baixo G' e alto tan delta, por se adaptarem melhor às áreas de grande movimentação.",
      "B": "Produtos de baixo swelling factor são contraindicados em mandíbula, por não gerarem projeção.",
      "C": "A escolha do produto é indiferente, desde que o volume total seja adequado.",
      "D": "A escolha deve recair sobre produto de alto G' (módulo elástico), aplicado em plano profundo supraperiosteal, por oferecer maior resistência à deformação e sustentação estrutural.",
      "E": "Deve-se utilizar produto de altíssima coesividade e baixo G' aplicado no plano subdérmico, para melhor definição de contorno."
    },
    "gab": "D",
    "exp": "O G' (módulo elástico) expressa a capacidade do gel de resistir à deformação e retornar à forma original. Regiões que exigem sustentação estrutural e projeção sobre plano ósseo — mandíbula, mento, arco zigomático — pedem produtos de alto G', aplicados em plano profundo supraperiosteal. Produtos de baixo G' e alto tan delta são mais fluidos e indicados para áreas de grande mobilidade ou planos superficiais, como lábios e correções finas."
  },
  {
    "n": 12,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Sobre a relação entre G' e coesividade dos preenchedores, assinale a alternativa correta:",
    "opts": {
      "A": "O G' expressa resistência à deformação e a coesividade expressa a força de união interna do gel (capacidade de não se fragmentar); produtos podem combinar alto G' com alta coesividade, o que favorece projeção com integridade do bloco de produto.",
      "B": "A coesividade indica a resistência à deformação, enquanto o G' expressa a capacidade do gel de se manter íntegro.",
      "C": "G' e coesividade são sinônimos e sempre variam na mesma direção.",
      "D": "Produtos de alta coesividade devem ser evitados em qualquer região da face, por gerarem nódulos.",
      "E": "A coesividade não tem qualquer aplicação prática na escolha do preenchedor."
    },
    "gab": "A",
    "exp": "São propriedades distintas e complementares. O G' mede a elasticidade — quanto o gel resiste a ser deformado por forças externas. A coesividade mede a força de coesão interna, ou seja, o quanto o gel permanece como bloco único sem se dispersar. Produtos com alto G' associado a boa coesividade sustentam projeção estruturada sem se fragmentar, sendo ideais para áreas de suporte ósseo."
  },
  {
    "n": 13,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Sobre o swelling factor (capacidade de hidratação/inchaço) dos preenchedores, assinale a alternativa correta:",
    "opts": {
      "A": "Produtos de alto swelling factor são os mais indicados para região infraorbitária, por conferirem hidratação local.",
      "B": "Produtos de baixo swelling factor são contraindicados na face, sendo restritos a uso corporal.",
      "C": "O swelling factor é irrelevante clinicamente, pois o produto não interage com o meio tecidual.",
      "D": "Todo ácido hialurônico apresenta o mesmo swelling factor, independentemente do processo de reticulação.",
      "E": "O swelling factor expressa a capacidade do gel de captar água após a implantação; produtos de baixo swelling factor são preferíveis em áreas de pele fina e baixa tolerância a edema, como região infraorbitária e pálpebra."
    },
    "gab": "E",
    "exp": "O swelling factor traduz a hidrofilia do gel — sua capacidade de captar água e expandir após a implantação. Em regiões de pele fina, drenagem linfática delicada e baixa tolerância a edema, como a região infraorbitária e a pálpebra inferior, produtos de alto swelling factor causam edema persistente e resultado desarmônico. Nessas áreas o produto de escolha tem baixo G', baixa hidrofilia e boa integração tecidual."
  },
  {
    "n": 14,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Sobre o tan delta dos preenchedores, assinale a alternativa correta:",
    "opts": {
      "A": "O tan delta é a razão entre o módulo viscoso (G'') e o módulo elástico (G'); valores mais altos indicam comportamento mais viscoso/fluido, com melhor adaptação a áreas de grande movimentação.",
      "B": "O tan delta é a razão entre G' e G'', sendo que valores altos indicam maior rigidez do produto.",
      "C": "Produtos de alto tan delta são os mais indicados para projeção de mento e ângulo mandibular.",
      "D": "O tan delta não se relaciona com o comportamento dinâmico do gel na face.",
      "E": "Quanto maior o tan delta, maior a capacidade do produto de resistir à deformação."
    },
    "gab": "A",
    "exp": "O tan delta é definido como G''/G', isto é, a razão entre o componente viscoso e o elástico. Valores baixos indicam comportamento predominantemente elástico (mais sólido, maior sustentação); valores altos indicam comportamento mais viscoso e fluido, com maior capacidade de adaptação ao movimento. Por isso produtos de alto tan delta são interessantes em áreas dinâmicas, e não para projeção estrutural."
  },
  {
    "n": 15,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Uma paciente solicita preenchimento labial com resultado natural, preservando a mobilidade e a expressividade da boca. Assinale a alternativa mais adequada quanto à escolha do produto:",
    "opts": {
      "A": "Produto de alto G' e alta coesividade, em plano supraperiosteal, para maior durabilidade.",
      "B": "Produto de altíssimo swelling factor, para potencializar o volume com menor quantidade aplicada.",
      "C": "Bioestimuladores de colágeno injetáveis são a primeira escolha para volumização labial.",
      "D": "Qualquer produto de preenchimento pode ser utilizado, desde que a técnica seja com cânula.",
      "E": "Produto de baixo a médio G', com bom tan delta e boa integração tecidual, aplicado no plano adequado do corpo labial, priorizando naturalidade e mobilidade."
    },
    "gab": "E",
    "exp": "Os lábios são estruturas dinâmicas, de mobilidade intensa e pele/mucosa fina. O produto ideal tem G' baixo a médio, boa capacidade de adaptação ao movimento (tan delta favorável), baixo a moderado swelling factor e boa integração tecidual, evitando aspecto de bloco, nódulos e rigidez. Produtos de alto G' e alta coesividade, próprios para suporte ósseo, geram resultado rígido e artificial nessa região. Bioestimuladores não têm indicação para volumização labial."
  },
  {
    "n": 16,
    "bloco": "BLOCO III — REOLOGIA DO ÁCIDO HIALURÔNICO",
    "stmt": "Sobre a hialuronidase e seu preparo, assinale a alternativa correta:",
    "opts": {
      "A": "A hialuronidase atua degradando o ácido hialurônico por hidrólise das ligações glicosídicas, sendo eficaz tanto sobre o AH endógeno quanto sobre o reticulado; em eventos isquêmicos, a conduta exige doses altas e repetidas até a resolução clínica.",
      "B": "A hialuronidase atua apenas sobre o ácido hialurônico endógeno, não tendo efeito sobre produtos reticulados.",
      "C": "Em complicação isquêmica, deve-se utilizar dose única e baixa, aguardando 72 horas para reavaliação.",
      "D": "A hialuronidase é contraindicada em qualquer complicação vascular, pelo risco de piora da isquemia.",
      "E": "O teste de sensibilidade é obrigatório e deve preceder o uso mesmo em situações de emergência isquêmica."
    },
    "gab": "A",
    "exp": "A hialuronidase é uma enzima que hidrolisa as ligações glicosídicas do ácido hialurônico, atuando também sobre géis reticulados — com eficácia variável conforme o grau de reticulação e a concentração do produto. Em evento isquêmico agudo, trata-se de emergência: a conduta é infiltração precoce, em doses altas e repetidas, em toda a área de comprometimento vascular e ao longo do trajeto arterial, com reavaliações seriadas. Em emergência, não se posterga a aplicação para realizar teste de sensibilidade."
  },
  {
    "n": 17,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre o preparo e a execução dos pertuitos e o manuseio da cânula no preenchimento full face, assinale a alternativa correta:",
    "opts": {
      "A": "O pertuito deve ser realizado com a mesma cânula que será utilizada, dispensando agulha prévia.",
      "B": "A cânula deve ser introduzida com movimentos rápidos e firmes, para vencer a resistência tecidual.",
      "C": "O número de pertuitos deve ser o maior possível, para reduzir o trajeto da cânula.",
      "D": "O pertuito é confeccionado com agulha de calibre igual ou superior ao da cânula, respeitando pontos de entrada planejados; a cânula deve ser progredida no plano correto, de forma lenta e sem forçar resistências, permitindo o acesso a múltiplas áreas por um mesmo ponto.",
      "E": "O uso de cânula dispensa o conhecimento anatômico, pois o instrumento é atraumático e não atinge vasos."
    },
    "gab": "D",
    "exp": "O pertuito é feito com agulha de calibre compatível (igual ou maior que o da cânula) em pontos de entrada planejados para permitir acesso a várias regiões com o mínimo de perfurações. A cânula deve progredir lentamente no plano desejado; resistência súbita indica plano incorreto ou estrutura interposta e exige reposicionamento. A cânula reduz — mas não elimina — o risco vascular, e o conhecimento anatômico permanece indispensável."
  },
  {
    "n": 18,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Uma paciente de 48 anos apresenta sulco nasolabial profundo associado a perda de projeção malar e flacidez do terço médio. Assinale a alternativa mais adequada quanto ao raciocínio clínico:",
    "opts": {
      "A": "Repor primeiramente o suporte estrutural do terço médio (área malar e abertura piriforme), reavaliando o sulco após esse aporte, e realizar apenas o refinamento residual necessário.",
      "B": "Preencher exclusivamente o sulco nasolabial com grande volume, por ser a queixa principal da paciente.",
      "C": "Iniciar o tratamento pelo terço inferior, independentemente da queixa e do exame.",
      "D": "Contraindicar o preenchimento, pois flacidez é indicação exclusiva de tratamento cirúrgico.",
      "E": "Aplicar produto de baixo G' em plano superficial ao longo de todo o sulco, para maior naturalidade."
    },
    "gab": "A",
    "exp": "O sulco nasolabial é, na maioria dos casos, consequência da perda de suporte do terço médio e da descida dos compartimentos gordurosos, e não uma depressão isolada. O raciocínio clínico correto trata a causa: reposição estrutural profunda em área malar e região piriforme, reavaliação da projeção do sulco e refinamento residual apenas se necessário. Preencher o sulco diretamente com grandes volumes gera peso, aspecto artificial e agravamento a médio prazo."
  },
  {
    "n": 19,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre o preenchimento de mento, pré-jowl e sulco labiomentoniano, assinale a alternativa correta:",
    "opts": {
      "A": "A região deve ser tratada exclusivamente com produtos de baixo G' em plano subdérmico.",
      "B": "O pré-jowl não tem relevância estética, pois não influencia o contorno mandibular.",
      "C": "O mento deve ser projetado apenas no sentido vertical, sem considerar a projeção anterior.",
      "D": "O planejamento deve considerar mento, pré-jowl e sulco labiomentoniano como uma unidade de contorno: produto de alto G' em plano profundo supraperiosteal no mento e no pré-jowl restabelece a linha mandibular contínua e suaviza o sulco labiomentoniano.",
      "E": "O sulco labiomentoniano deve ser preenchido isoladamente com grandes volumes, por ser a estrutura determinante do terço inferior."
    },
    "gab": "D",
    "exp": "O contorno do terço inferior depende da relação entre mento, pré-jowl e linha mandibular. A depressão pré-jowl quebra a continuidade da mandíbula e acentua a jowl; a projeção adequada do mento (nos sentidos anterior e vertical, conforme a análise) e o preenchimento do pré-jowl com produto de alto G' em plano supraperiosteal restauram a linha contínua e suavizam secundariamente o sulco labiomentoniano, que raramente deve ser abordado de forma isolada e volumosa."
  },
  {
    "n": 20,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre a anatomia vascular dos lábios aplicada ao preenchimento labial, assinale a alternativa correta:",
    "opts": {
      "A": "As artérias labiais superior e inferior apresentam trajeto constante e sempre submucoso, o que torna o plano submucoso o mais seguro.",
      "B": "O risco vascular no preenchimento labial é inexistente, dada a rica circulação colateral da região.",
      "C": "A vascularização labial é exclusivamente derivada da artéria maxilar, sem contribuição da artéria facial.",
      "D": "As artérias labiais são ramos da artéria facial, com trajeto variável (submucoso, intramuscular ou subcutâneo) em relação ao músculo orbicular da boca; essa variabilidade exige técnica cuidadosa, pequenos volumes, injeção lenta e baixa pressão.",
      "E": "O plano de aplicação é irrelevante, desde que se utilize cânula."
    },
    "gab": "D",
    "exp": "As artérias labiais superior e inferior originam-se da artéria facial e apresentam trajeto anatomicamente variável em relação ao músculo orbicular da boca — podem correr submucosas, intramusculares ou, menos frequentemente, subcutâneas. Essa variabilidade impede que se considere qualquer plano absolutamente seguro. A prevenção baseia-se em conhecimento anatômico, injeção lenta, pequenos volumes, baixa pressão, aspiração quando com agulha e atenção a sinais precoces de comprometimento vascular."
  },
  {
    "n": 21,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre o raciocínio clínico e a técnica na rinomodelação, assinale a alternativa mais adequada:",
    "opts": {
      "A": "A rinomodelação pode ser realizada com grandes volumes no dorso, desde que aplicados rapidamente para reduzir o desconforto.",
      "B": "A aplicação em ponta e asa nasal é preferencial por serem regiões de menor risco vascular.",
      "C": "O uso prévio de vasoconstritor na região elimina o risco de embolização.",
      "D": "A rinomodelação é indicada para todos os casos de deformidade nasal, inclusive para redução do volume nasal.",
      "E": "A técnica segura envolve plano profundo supraperiosteal/supracondral na linha média, uso de pequenos volumes, injeção lenta e com baixa pressão, aspiração prévia, atenção a sinais de isquemia e reconhecimento de que se trata de procedimento de alto risco."
    },
    "gab": "E",
    "exp": "A rinomodelação está entre os procedimentos de maior risco de complicação isquêmica grave, incluindo necrose de dorso/ponta e amaurose, pelas anastomoses com o sistema oftálmico. A técnica segura exige plano profundo na linha média (supraperiosteal/supracondral), volumes pequenos e fracionados, injeção lenta e com baixa pressão, aspiração e vigilância contínua. É um procedimento aditivo: não reduz volume nasal, e narizes muito volumosos ou com pele muito espessa têm indicação limitada. O vasoconstritor não previne embolização — pode inclusive mascarar sinais precoces de isquemia."
  },
  {
    "n": 22,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre o preenchimento de têmporas, assinale a alternativa correta:",
    "opts": {
      "A": "A região temporal deve ser preenchida sempre no plano intermediário, onde corre a artéria temporal superficial, por ser o plano de maior estabilidade do produto.",
      "B": "Os planos de escolha são o supraperiosteal profundo (agulha perpendicular até contato ósseo, em ponto seguro previamente demarcado) ou o subdérmico superficial com cânula; a região exige atenção às comunicações vasculares com o sistema oftálmico.",
      "C": "A depressão temporal não influencia a percepção de envelhecimento facial, sendo o preenchimento apenas opcional e estético.",
      "D": "Deve-se utilizar produto de baixíssimo G' e alto swelling factor para preencher grandes volumes de uma só vez.",
      "E": "O preenchimento temporal é isento de risco vascular, pois se trata de área periférica da face."
    },
    "gab": "B",
    "exp": "A atrofia temporal contribui de forma importante para o aspecto envelhecido, ao estreitar o terço superior e acentuar o rebordo orbitário lateral. Os planos utilizados com segurança são o supraperiosteal profundo — com agulha perpendicular até o osso, em ponto demarcado longe do trajeto da artéria temporal superficial — ou o subdérmico superficial com cânula. O plano intermediário, onde trafega a artéria temporal superficial e há anastomoses com o sistema oftálmico, é o de maior risco."
  },
  {
    "n": 23,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre a documentação fotográfica e a avaliação prévia no preenchimento full face, assinale a alternativa correta:",
    "opts": {
      "A": "A documentação fotográfica é dispensável quando há termo de consentimento assinado.",
      "B": "A avaliação deve ser realizada apenas em repouso, pois a análise dinâmica não influencia o planejamento do preenchimento.",
      "C": "A avaliação dinâmica é útil apenas para toxina botulínica, não tendo aplicação no preenchimento.",
      "D": "As fotografias devem ser realizadas apenas após o procedimento, para demonstrar o resultado.",
      "E": "A documentação fotográfica padronizada (mesma distância, iluminação, ângulos e posicionamento) associada à avaliação estática e dinâmica é parte essencial do planejamento, da comunicação com o paciente e da segurança médico-legal."
    },
    "gab": "E",
    "exp": "A documentação fotográfica padronizada é ferramenta clínica, de comunicação e de proteção médico-legal. Deve ser realizada antes, durante o acompanhamento e após o procedimento, mantendo constantes distância, iluminação, fundo, ângulos e posicionamento da cabeça. A avaliação deve contemplar tanto o repouso quanto a dinâmica, pois o comportamento muscular e a movimentação influenciam a escolha do produto, do plano e do volume também no preenchimento."
  },
  {
    "n": 24,
    "bloco": "BLOCO IV — RACIOCÍNIO CLÍNICO E TÉCNICAS PARA O PREENCHIMENTO FULL FACE",
    "stmt": "Sobre a indicação e as contraindicações do preenchimento labial, assinale a alternativa correta:",
    "opts": {
      "A": "O preenchimento está indicado em qualquer paciente que deseje aumento de volume, independentemente do exame físico.",
      "B": "Herpes labial ativo, infecção local, expectativa irreal do paciente e distorções anatômicas não corrigíveis por preenchimento constituem contraindicações ou exigem adiamento; o exame físico deve avaliar proporção, projeção, altura do filtro, exposição dentária e qualidade tecidual.",
      "C": "O antecedente de herpes labial de repetição contraindica definitivamente o procedimento.",
      "D": "A avaliação da proporção entre lábio superior e inferior é irrelevante, pois a proporção ideal é sempre 1:1.",
      "E": "Pacientes com lábio superior alongado devem receber grandes volumes no lábio superior para compensar a proporção."
    },
    "gab": "B",
    "exp": "O preenchimento labial exige avaliação criteriosa: proporção entre lábios, projeção, altura do filtro, exposição dentária, qualidade da pele e mucosa, e expectativa do paciente. São contraindicações absolutas ou relativas a infecção ativa, herpes em atividade (o antecedente de herpes recorrente não contraindica, mas indica profilaxia antiviral), doenças autoimunes descompensadas e expectativas irreais. Lábio superior alongado tratado com grande volume tende a piorar o aspecto, sendo caso de indicação técnica distinta."
  },
  {
    "n": 25,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Durante um preenchimento de sulco nasolabial, a paciente refere dor intensa e desproporcional ao procedimento, e observa-se palidez cutânea imediata com posterior aspecto reticulado violáceo na região. Assinale a alternativa mais adequada quanto à conduta:",
    "opts": {
      "A": "Trata-se de reação vasovagal esperada; deve-se apenas interromper o procedimento e observar por 24 horas.",
      "B": "O quadro sugere hematoma; a conduta é compressa fria e observação ambulatorial.",
      "C": "Trata-se de complicação isquêmica aguda; deve-se interromper imediatamente a aplicação e iniciar hialuronidase em altas doses na área comprometida e ao longo do trajeto arterial, com massagem, calor local e reavaliações seriadas até a resolução.",
      "D": "Deve-se aguardar 48 horas para confirmar o diagnóstico antes de iniciar a hialuronidase.",
      "E": "A conduta é aplicar corticoide intralesional e antibiótico, reservando a hialuronidase para casos refratários."
    },
    "gab": "C",
    "exp": "Dor desproporcional, palidez (blanqueamento) imediata e livedo reticular são sinais clássicos de comprometimento vascular arterial. Trata-se de emergência: a aplicação deve ser interrompida imediatamente e a hialuronidase infiltrada precocemente, em altas doses, em toda a área isquêmica e ao longo do trajeto da artéria acometida, com reaplicações seriadas conforme a evolução clínica. Medidas adjuvantes incluem massagem vigorosa, calor local e vasodilatação. O atraso na conduta é o principal determinante de necrose e sequela."
  },
  {
    "n": 26,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Sobre a amaurose como complicação de preenchimento facial, assinale a alternativa correta:",
    "opts": {
      "A": "A amaurose é sempre reversível com hialuronidase retrobulbar, desde que aplicada em até 24 horas.",
      "B": "Decorre de embolização retrógrada para a artéria oftálmica e seus ramos; costuma manifestar-se de forma imediata, com dor intensa e perda visual, tem prognóstico reservado e janela terapêutica muito curta, exigindo medidas imediatas e encaminhamento emergencial ao oftalmologista.",
      "C": "A amaurose ocorre apenas em preenchimentos de região periorbitária, não sendo descrita em glabela ou nariz.",
      "D": "O quadro tem instalação tardia, geralmente entre 48 e 72 horas após o procedimento.",
      "E": "Não há necessidade de encaminhamento especializado, pois o manejo é integralmente ambulatorial."
    },
    "gab": "B",
    "exp": "A amaurose resulta da embolização retrógrada de produto para a artéria oftálmica através de anastomoses do sistema carotídeo externo com o interno. As áreas de maior risco são glabela, nariz, região periorbitária e sulco nasolabial. A apresentação é tipicamente imediata, com dor ocular intensa, perda visual e podendo associar-se a oftalmoplegia e sinais cutâneos. A retina tolera isquemia por período muito curto, o que confere prognóstico reservado; a conduta envolve medidas imediatas e encaminhamento emergencial ao oftalmologista. A prevenção — conhecimento anatômico, plano correto, pequenos volumes, baixa pressão — é a principal estratégia."
  },
  {
    "n": 27,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Sobre as complicações agudas não isquêmicas dos preenchedores, assinale a alternativa correta:",
    "opts": {
      "A": "Edema, equimose e hematoma são complicações agudas não isquêmicas, geralmente autolimitadas; já a infecção precoce cursa com sinais flogísticos e exige antibioticoterapia, sendo essencial diferenciá-las do evento isquêmico.",
      "B": "Todo edema após preenchimento deve ser tratado com hialuronidase em altas doses.",
      "C": "Equimose e hematoma são sinais patognomônicos de comprometimento arterial.",
      "D": "A infecção precoce deve ser tratada exclusivamente com corticoide, para reduzir a inflamação local.",
      "E": "Complicações agudas não isquêmicas exigem sempre remoção cirúrgica do produto."
    },
    "gab": "A",
    "exp": "As complicações agudas não isquêmicas incluem edema, eritema, equimose, hematoma, assimetrias, irregularidades e infecção precoce. A maioria é autolimitada e responde a medidas conservadoras. A infecção precoce cursa com dor, calor, rubor, edema progressivo e eventualmente secreção, exigindo antibioticoterapia. O ponto crítico é o diagnóstico diferencial com o evento isquêmico — este cursa com dor desproporcional, palidez inicial, livedo reticular e evolução para necrose, e demanda hialuronidase imediata."
  },
  {
    "n": 28,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Uma paciente retorna oito meses após preenchimento facial com nódulos endurecidos, dolorosos, com sinais inflamatórios locais e sem sinais de isquemia. Assinale a alternativa mais adequada:",
    "opts": {
      "A": "O quadro é compatível com evento isquêmico tardio; a conduta é hialuronidase em altas doses e vasodilatação.",
      "B": "Trata-se de reação esperada ao produto, não havendo necessidade de intervenção.",
      "C": "O quadro sugere complicação tardia não isquêmica, com possível componente inflamatório/infeccioso e formação de biofilme; a conduta inclui antibioticoterapia adequada e, conforme a evolução, hialuronidase, evitando o uso isolado e precoce de corticoide.",
      "D": "A conduta imediata é a infiltração de corticoide intralesional em dose alta, como primeira e única medida.",
      "E": "A remoção cirúrgica imediata dos nódulos é a conduta de escolha em todos os casos."
    },
    "gab": "C",
    "exp": "Nódulos inflamatórios tardios podem ter etiologia imunomediada ou infecciosa, frequentemente associada a biofilme. Por esse motivo, o uso isolado e precoce de corticoide é inadequado: se houver componente infeccioso, pode agravar o quadro. A abordagem inicial privilegia antibioticoterapia (comumente macrolídeos e/ou quinolonas, conforme protocolo), com uso de hialuronidase para remoção do produto quando indicado, e o corticoide reservado para casos comprovadamente inflamatórios não infecciosos e após controle do quadro."
  },
  {
    "n": 29,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Sobre nódulos relacionados a bioestimuladores de colágeno injetáveis, assinale a alternativa correta:",
    "opts": {
      "A": "Nódulos por bioestimuladores respondem prontamente à hialuronidase, assim como os de ácido hialurônico.",
      "B": "A prevenção depende de técnica adequada — diluição e reconstituição corretas, plano de aplicação apropriado, volumes distribuídos e massagem quando indicada; o manejo é distinto do ácido hialurônico, pois a hialuronidase não degrada esses produtos, podendo envolver medidas locais, corticoide e antibiótico conforme a natureza do nódulo.",
      "C": "Nódulos por bioestimuladores são sempre infecciosos e exigem drenagem cirúrgica.",
      "D": "A ocorrência de nódulos independe da técnica de aplicação e da diluição empregada.",
      "E": "O uso de bioestimuladores é contraindicado na face pelo risco inevitável de nódulos."
    },
    "gab": "B",
    "exp": "Bioestimuladores como PLLA, CaHA e PCL não são degradados pela hialuronidase. A prevenção de nódulos depende diretamente da técnica: reconstituição e tempo de hidratação adequados, diluição correta, escolha do plano, distribuição homogênea do produto, evitar áreas de alta mobilidade e realizar massagem quando o protocolo do produto indicar. O manejo diferencia nódulos precoces por acúmulo de produto (massagem, diluição local) de nódulos inflamatórios tardios ou infecciosos (antibiótico, corticoide conforme o caso), sendo distinto do manejo aplicado ao ácido hialurônico."
  },
  {
    "n": 30,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Sobre a conduta diante do acometimento da artéria temporal durante um procedimento, assinale a alternativa correta:",
    "opts": {
      "A": "Trata-se de situação sem repercussão clínica, dada a circulação colateral da região.",
      "B": "A conduta é apenas compressão local prolongada, sem necessidade de outras medidas.",
      "C": "O acometimento pode cursar com sangramento importante e/ou comprometimento vascular; a conduta envolve compressão imediata e sustentada, avaliação de sinais de isquemia no território irrigado e, havendo suspeita de embolização por preenchedor, uso de hialuronidase com reavaliações seriadas.",
      "D": "Deve-se realizar imediatamente ligadura cirúrgica da artéria em ambiente ambulatorial.",
      "E": "A hialuronidase é contraindicada em qualquer intercorrência da região temporal."
    },
    "gab": "C",
    "exp": "A artéria temporal superficial é superficial e calibrosa, e sua punção pode gerar sangramento significativo e hematoma volumoso. A conduta imediata é compressão firme e sustentada no local. Havendo injeção intravascular de preenchedor, o risco inclui isquemia no território irrigado e, por anastomoses, comprometimento de territórios mais nobres — situação em que se aplica hialuronidase em altas doses com reavaliação clínica seriada. O reconhecimento precoce dos sinais é determinante para o desfecho."
  },
  {
    "n": 31,
    "bloco": "BLOCO V — INTERCORRÊNCIAS E EMERGÊNCIAS MÉDICAS",
    "stmt": "Sobre o reconhecimento e o manejo da anafilaxia em consultório, assinale a alternativa correta:",
    "opts": {
      "A": "O tratamento de primeira linha é o corticoide endovenoso, seguido de anti-histamínico.",
      "B": "A adrenalina deve ser administrada por via endovenosa em bolus como primeira medida em todos os casos.",
      "C": "O tratamento de primeira linha é a adrenalina por via intramuscular na face anterolateral da coxa (vasto lateral), com posicionamento adequado do paciente, suporte de vias aéreas e oxigênio, acesso venoso e acionamento do serviço de emergência; corticoide e anti-histamínico são medidas adjuvantes.",
      "D": "A anafilaxia exige obrigatoriamente a presença de lesões cutâneas para o diagnóstico.",
      "E": "Após a resposta inicial à adrenalina, o paciente pode ser liberado imediatamente, sem período de observação."
    },
    "gab": "C",
    "exp": "A anafilaxia é diagnóstico clínico e emergencial, e pode ocorrer mesmo sem manifestações cutâneas. O tratamento de primeira linha é a adrenalina intramuscular na face anterolateral da coxa (0,3–0,5 mg em adultos, repetível a cada 5–15 minutos conforme resposta), associada a posicionamento do paciente, oxigênio, suporte ventilatório, acesso venoso e reposição volêmica. Corticoides e anti-histamínicos são adjuvantes e não substituem a adrenalina. Pelo risco de reação bifásica, é obrigatório período de observação e encaminhamento a serviço de emergência."
  },
  {
    "n": 32,
    "bloco": "BLOCO VI — FIOS DE COLÁGENO",
    "stmt": "Sobre a estrutura química e a degradação da polidioxanona (PDO), assinale a alternativa correta:",
    "opts": {
      "A": "A PDO é um polímero não absorvível, o que garante a permanência do efeito de tração.",
      "B": "A PDO é um polímero absorvível degradado por hidrólise de suas ligações éster, com absorção completa em torno de 6 a 8 meses; o estímulo inflamatório controlado desencadeia neocolagênese, cujo efeito clínico persiste além da absorção física do fio.",
      "C": "A degradação da PDO ocorre por ação enzimática específica, sendo acelerada pela hialuronidase.",
      "D": "A absorção completa da PDO ocorre em aproximadamente 30 dias, o que limita sua indicação clínica.",
      "E": "A PDO não gera resposta tecidual, atuando apenas por efeito mecânico de sustentação."
    },
    "gab": "B",
    "exp": "A polidioxanona é um polímero sintético absorvível, degradado por hidrólise das ligações éster da cadeia, com absorção completa em torno de 6 a 8 meses. Sua permanência gera resposta inflamatória controlada, com recrutamento de fibroblastos, angiogênese e deposição de matriz extracelular. O resultado clínico deriva da combinação entre o efeito mecânico inicial (mais relevante nos fios de tração) e a neocolagênese, que sustenta o resultado por período superior ao da presença física do fio."
  },
  {
    "n": 33,
    "bloco": "BLOCO VI — FIOS DE COLÁGENO",
    "stmt": "Sobre a cronologia histológica da resposta tecidual aos fios de PDO, assinale a alternativa correta:",
    "opts": {
      "A": "O pico de neocolagênese ocorre nas primeiras 48 horas, decaindo progressivamente a partir daí.",
      "B": "Não há alteração histológica detectável antes de 12 meses da aplicação.",
      "C": "Nos primeiros meses predomina a resposta inflamatória com colágeno tipo III, que é progressivamente substituído por colágeno tipo I, mais organizado e resistente, com maturação da matriz ao longo dos meses subsequentes e resultado clínico que se prolonga além da absorção do fio.",
      "D": "O colágeno tipo I é depositado imediatamente após a inserção do fio, sem fase inflamatória prévia.",
      "E": "A resposta histológica é idêntica para fios lisos e fios de tração, tanto em intensidade quanto em cronologia."
    },
    "gab": "C",
    "exp": "A resposta segue o padrão clássico de reparo tecidual: fase inflamatória inicial, seguida de fase proliferativa com deposição de colágeno tipo III — mais frouxo e desorganizado — e posterior fase de remodelação, com substituição progressiva por colágeno tipo I, mais espesso, organizado e resistente. Essa maturação ocorre ao longo dos meses, o que explica a melhora progressiva da qualidade e da sustentação da pele mesmo após a absorção completa do material."
  },
  {
    "n": 34,
    "bloco": "BLOCO VI — FIOS DE COLÁGENO",
    "stmt": "Uma paciente de 50 anos apresenta flacidez moderada do terço médio com ptose de bola de Bichat e sulco nasogeniano acentuado, além de pele com perda de firmeza difusa. Sobre a indicação dos fios, assinale a alternativa mais adequada:",
    "opts": {
      "A": "Fios lisos isolados são a melhor indicação, pois promovem tração vetorial e reposicionamento tecidual.",
      "B": "O fio de tração está indicado quando há necessidade de reposicionamento tecidual com vetor definido, enquanto o fio liso atua predominantemente na bioestimulação e melhora da qualidade da pele; os dois podem ser combinados conforme o diagnóstico.",
      "C": "Fios de tração são indicados apenas para pacientes com flacidez grave e excesso cutâneo importante.",
      "D": "A indicação de fios independe do grau de flacidez e da qualidade da pele.",
      "E": "Fios de tração e fios lisos têm exatamente a mesma indicação e o mesmo mecanismo de ação."
    },
    "gab": "B",
    "exp": "São ferramentas com propósitos distintos. O fio de tração (espiculado, com garras/cones) promove reposicionamento tecidual segundo vetores planejados, sendo indicado em ptose e flacidez moderada com tecido passível de tração. O fio liso atua essencialmente por bioestimulação, melhorando firmeza, textura e qualidade da pele, sem tração significativa. O diagnóstico correto define a escolha, e a associação das duas modalidades é frequente. Flacidez grave com excesso cutâneo importante é indicação cirúrgica, não de fios."
  },
  {
    "n": 35,
    "bloco": "BLOCO VI — FIOS DE COLÁGENO",
    "stmt": "Sobre o planejamento e a execução de fios de tração para lifting do terço médio, assinale a alternativa correta:",
    "opts": {
      "A": "Os vetores devem ser sempre horizontais, independentemente da anatomia e do padrão de ptose.",
      "B": "A ativação das garras é dispensável, pois a tração ocorre passivamente pela simples inserção do fio.",
      "C": "O planejamento define pontos de entrada, vetores e plano de inserção (subcutâneo adequado); após o posicionamento, realiza-se a ativação das garras com tração controlada e checagem de simetria, corrigindo pregueamento e irregularidades ainda no intraoperatório.",
      "D": "O fio deve ser inserido no plano intradérmico, para garantir maior fixação.",
      "E": "A simetria deve ser avaliada apenas no retorno de 30 dias, não sendo possível qualquer ajuste durante o procedimento."
    },
    "gab": "C",
    "exp": "O resultado depende do planejamento prévio: marcação dos pontos de entrada e de ancoragem, definição dos vetores conforme o padrão de ptose e escolha do plano subcutâneo adequado. Após o posicionamento do fio, a ativação das garras com tração controlada é etapa determinante, seguida da checagem imediata de simetria e da correção de pregueamentos e irregularidades ainda no intraoperatório. Inserção intradérmica gera irregularidade, dimpling e risco de extrusão."
  },
  {
    "n": 36,
    "bloco": "BLOCO VI — FIOS DE COLÁGENO",
    "stmt": "Sobre as complicações relacionadas aos fios e seu manejo, assinale a alternativa correta:",
    "opts": {
      "A": "Dimpling, pregueamento, assimetria, extrusão e desconforto à mímica são complicações possíveis; a maioria decorre de plano inadequado, vetor mal planejado ou tração excessiva, e o manejo varia de massagem e observação a liberação de pontos de aderência ou remoção do fio.",
      "B": "A extrusão do fio é evento sem relevância clínica, dispensando qualquer conduta.",
      "C": "Complicações com fios são sempre definitivas, não havendo possibilidade de correção.",
      "D": "O dimpling indica necessariamente infecção do trajeto e exige antibioticoterapia endovenosa.",
      "E": "A ocorrência de assimetria só pode ser corrigida por procedimento cirúrgico aberto."
    },
    "gab": "A",
    "exp": "As complicações mais frequentes são dimpling, pregueamento cutâneo, assimetrias, dor ou desconforto à mímica, palpação do fio, extrusão e, menos comumente, infecção. A maior parte relaciona-se a plano de inserção superficial demais, vetor mal planejado ou tração excessiva. O manejo é escalonado: massagem, observação e orientação nos casos leves; liberação de aderências ou de pontos de fixação nos casos persistentes; e remoção do fio nas extrusões e nos casos refratários. Sinais infecciosos exigem antibioticoterapia e reavaliação."
  },
  {
    "n": 37,
    "bloco": "BLOCO VII — BIOESTIMULADORES E INTRADERMOTERAPIA",
    "stmt": "Sobre os bioestimuladores de colágeno injetáveis, assinale a alternativa correta:",
    "opts": {
      "A": "Todos os bioestimuladores têm mecanismo idêntico e podem ser reconstituídos e aplicados da mesma forma.",
      "B": "O ácido poli-L-lático (PLLA), a hidroxiapatita de cálcio (CaHA) e a policaprolactona (PCL) atuam por estímulo à neocolagênese mediado por resposta inflamatória controlada, mas diferem em reconstituição, tempo de hidratação, plano de aplicação, imediatismo do efeito volumétrico e duração.",
      "C": "A hidroxiapatita de cálcio não apresenta qualquer efeito volumétrico imediato.",
      "D": "O ácido poli-L-lático produz resultado volumétrico imediato e definitivo já na primeira sessão.",
      "E": "Bioestimuladores são degradáveis por hialuronidase, o que facilita a reversão de resultados indesejados."
    },
    "gab": "B",
    "exp": "Os três principais bioestimuladores compartilham o princípio de induzir neocolagênese por resposta inflamatória controlada, mas têm comportamentos distintos. O PLLA exige reconstituição e tempo de hidratação adequados, tem efeito volumétrico inicial transitório (pelo diluente) e resultado progressivo em sessões seriadas. A CaHA tem efeito volumétrico imediato somado ao bioestímulo e pode ser diluída conforme o objetivo. A PCL associa efeito imediato do veículo com estímulo prolongado. Nenhum deles é degradado por hialuronidase."
  },
  {
    "n": 38,
    "bloco": "BLOCO VII — BIOESTIMULADORES E INTRADERMOTERAPIA",
    "stmt": "Sobre o uso de bioestimuladores líquidos (hiperdiluídos) de colágeno, assinale a alternativa correta:",
    "opts": {
      "A": "A hiperdiluição transforma o bioestimulador em preenchedor estrutural, sendo indicada para projeção óssea.",
      "B": "A hiperdiluição não altera o comportamento do produto no tecido, servindo apenas para reduzir custo por sessão.",
      "C": "A hiperdiluição amplia a distribuição do produto e favorece o bioestímulo difuso com menor efeito volumétrico, sendo útil para melhora da qualidade da pele e de áreas extensas, exigindo plano de aplicação e técnica adequados para reduzir risco de nódulos.",
      "D": "O bioestimulador hiperdiluído deve ser aplicado no plano supraperiosteal profundo em todos os casos.",
      "E": "A hiperdiluição elimina o risco de nódulos, dispensando cuidados técnicos."
    },
    "gab": "C",
    "exp": "A hiperdiluição aumenta o volume do veículo em relação à quantidade de partículas, permitindo distribuição mais ampla e homogênea do estímulo com menor efeito volumétrico. É estratégia útil para melhora global da qualidade da pele e para tratar áreas extensas — face, pescoço, colo, braços e abdome. O raciocínio é de bioestímulo difuso, e não de projeção estrutural. A técnica, o plano e a distribuição homogênea permanecem determinantes para reduzir o risco de nódulos."
  },
  {
    "n": 39,
    "bloco": "BLOCO VII — BIOESTIMULADORES E INTRADERMOTERAPIA",
    "stmt": "Sobre a intradermoterapia e seus fundamentos, assinale a alternativa correta:",
    "opts": {
      "A": "A intradermoterapia atua exclusivamente por efeito volumétrico, sem estímulo à renovação tecidual.",
      "B": "O fototipo do paciente é irrelevante no planejamento, pois o risco de hiperpigmentação pós-inflamatória é inexistente.",
      "C": "A técnica consiste na aplicação de ativos no plano intradérmico, promovendo estímulo tecidual e ação farmacológica local; o planejamento deve considerar histologia, fase de cicatrização, fototipo e risco de hiperpigmentação pós-inflamatória, sobretudo em fototipos altos.",
      "D": "A intradermoterapia é contraindicada em qualquer paciente com fototipo acima de III.",
      "E": "A profundidade de aplicação não influencia o resultado nem o risco de complicações."
    },
    "gab": "C",
    "exp": "A intradermoterapia baseia-se na entrega de ativos diretamente na derme, associando estímulo mecânico e ação farmacológica local, com indicações que vão da biorevitalização ao tratamento de cicatrizes e discromias. O planejamento exige compreensão da histologia cutânea, das fases da cicatrização e do fototipo do paciente: fototipos mais altos apresentam maior risco de hiperpigmentação pós-inflamatória, o que exige ajuste de profundidade, intensidade, intervalo entre sessões e preparo/manutenção domiciliar — mas não constitui contraindicação absoluta."
  },
  {
    "n": 40,
    "bloco": "BLOCO VII — BIOESTIMULADORES E INTRADERMOTERAPIA",
    "stmt": "Uma paciente de 45 anos apresenta rugas estáticas profundas em fronte, que persistem mesmo após tratamento prévio adequado com toxina botulínica. Assinale a alternativa mais adequada:",
    "opts": {
      "A": "A conduta correta é aumentar progressivamente as doses de toxina botulínica até a resolução completa das rugas estáticas.",
      "B": "Rugas estáticas não respondem isoladamente à toxina, pois refletem dano dérmico estabelecido; técnicas como o line lifting — preenchimento superficial da ruga com produto adequado — atuam de forma complementar, sendo relevantes o planejamento e o conforto anestésico da região.",
      "C": "Rugas estáticas em fronte são contraindicação absoluta a qualquer procedimento injetável.",
      "D": "O tratamento de escolha é o preenchimento profundo supraperiosteal da fronte com produto de alto G'.",
      "E": "A associação entre toxina botulínica e técnicas de preenchimento superficial deve ser evitada, pelo risco de antagonismo entre os procedimentos."
    },
    "gab": "B",
    "exp": "A toxina botulínica atua sobre a componente dinâmica da ruga, reduzindo a contração muscular que a origina e a mantém. Rugas estáticas já representam dano dérmico estruturado, com perda de colágeno e sulco estabelecido, e por isso não se resolvem apenas com aumento de dose — estratégia que, além de ineficaz para esse componente, aumenta o risco de ptose e aspecto pesado. O line lifting propõe o tratamento superficial da própria ruga com produto adequado, associado ao controle da dinâmica com toxina, e o planejamento inclui o conforto anestésico da fronte."
  }
];

// ============================== SCRIPT ==============================

/** Aplica configuracao opcional sem derrubar a execucao. */
function aplicar_(fn, nome) {
  try {
    fn();
  } catch (e) {
    Logger.log('AVISO: "' + nome + '" nao foi aplicado nesta conta. ' +
               'Ajuste manualmente nas configuracoes do formulario. Detalhe: ' + e);
  }
}

function preencherFormulario() {
  var titulo = CONFIG.ID_POS + ' — ' + CONFIG.TITULO_BASE;

  var form = null;
  var criouNovo = false;

  if (CONFIG.FORM_ID) {
    try {
      form = FormApp.openById(CONFIG.FORM_ID);
      Logger.log('Formulario existente aberto: ' + CONFIG.FORM_ID);
    } catch (e) {
      Logger.log('AVISO: nao consegui abrir o formulario ' + CONFIG.FORM_ID + '.');
      Logger.log('Causa mais comum: a conta Google logada aqui nao e a dona do ' +
                 'formulario, ou nao tem permissao de EDICAO nele.');
      Logger.log('Detalhe: ' + e);
      if (!CONFIG.CRIAR_NOVO_SE_FALHAR) {
        throw new Error('Rode o script na MESMA conta dona do formulario, ou ' +
                        'deixe CRIAR_NOVO_SE_FALHAR = true para gerar um novo.');
      }
    }
  }

  if (!form) {
    form = FormApp.create(titulo);
    criouNovo = true;
    Logger.log('Formulario NOVO criado: ' + form.getId());
  }

  // ---- limpeza ----
  if (CONFIG.LIMPAR_ANTES) {
    aplicar_(function () { form.deleteAllResponses(); }, 'deleteAllResponses');
    var itens = form.getItems();
    for (var k = itens.length - 1; k >= 0; k--) {
      form.deleteItem(itens[k]);
    }
    Logger.log('Formulario limpo: ' + itens.length + ' item(ns) removido(s).');
  }

  // ---- cabecalho ----
  form.setTitle(titulo);
  form.setDescription(
    'ID da Pós: ' + CONFIG.ID_POS + '\n\n' +
    'Avaliação final com ' + QUESTOES.length + ' questões de múltipla escolha ' +
    '(alternativas A a E), valendo ' + CONFIG.PONTOS_POR_QUESTAO + ' ponto cada — ' +
    'total de ' + (QUESTOES.length * CONFIG.PONTOS_POR_QUESTAO) + ' pontos.\n\n' +
    'Leia cada caso com atenção e assinale a alternativa mais adequada. ' +
    'Há apenas uma resposta correta por questão.'
  );

  form.setIsQuiz(true);
  form.setShuffleQuestions(CONFIG.EMBARALHAR_QUESTOES);
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);

  aplicar_(function () { form.setCollectEmail(CONFIG.COLETAR_EMAIL); }, 'setCollectEmail');
  aplicar_(function () { form.setPublishingSummary(false); }, 'setPublishingSummary');
  if (CONFIG.EXIGIR_LOGIN) {
    aplicar_(function () { form.setRequireLogin(true); }, 'setRequireLogin');
    aplicar_(function () { form.setLimitOneResponsePerUser(true); }, 'setLimitOneResponsePerUser');
  }

  // ---- identificacao do aluno ----
  if (CONFIG.INCLUIR_IDENTIFICACAO) {
    form.addSectionHeaderItem()
        .setTitle('Identificação')
        .setHelpText('Preencha seus dados antes de iniciar a prova.');
    form.addTextItem().setTitle('Nome completo').setRequired(true);
    form.addTextItem().setTitle('CPF').setRequired(true);
    form.addTextItem().setTitle('Turma / ID da Pós').setRequired(false)
        .setHelpText('Referência: ' + CONFIG.ID_POS);
  }

  // ---- questoes ----
  var blocoAtual = '';
  var totalPontos = 0;
  var imagensOk = 0;
  var imagensFalhas = [];
  var letras = ['A', 'B', 'C', 'D', 'E'];

  for (var i = 0; i < QUESTOES.length; i++) {
    var q = QUESTOES[i];

    if (CONFIG.QUEBRA_POR_BLOCO && q.bloco !== blocoAtual) {
      blocoAtual = q.bloco;
      form.addPageBreakItem().setTitle(blocoAtual);
    }

    if (IMAGENS[q.n]) {
      try {
        form.addImageItem()
            .setTitle('Imagem de apoio — questão ' + q.n)
            .setImage(DriveApp.getFileById(IMAGENS[q.n]).getBlob())
            .setAlignment(FormApp.Alignment.CENTER)
            .setWidth(520);
        imagensOk++;
      } catch (e) {
        imagensFalhas.push(q.n);
        Logger.log('AVISO: imagem da questao ' + q.n + ' nao carregou (ID: ' +
                   IMAGENS[q.n] + '). ' + e);
      }
    }

    var item = form.addMultipleChoiceItem();
    item.setTitle(q.n + ') ' + q.stmt);
    item.setRequired(true);
    item.setPoints(CONFIG.PONTOS_POR_QUESTAO);
    totalPontos += CONFIG.PONTOS_POR_QUESTAO;

    var escolhas = [];
    for (var j = 0; j < letras.length; j++) {
      var L = letras[j];
      escolhas.push(item.createChoice(L + ') ' + q.opts[L], L === q.gab));
    }
    item.setChoices(escolhas);

    var feedback = FormApp.createFeedback()
        .setText('Resposta correta: ' + q.gab + '\n\n' + q.exp)
        .build();
    item.setFeedbackForIncorrect(feedback);
    item.setFeedbackForCorrect(feedback);
  }

  // ---- planilha de respostas ----
  var linkPlanilha = '(nao criada)';
  if (CONFIG.CRIAR_PLANILHA_RESPOSTAS) {
    var destinoExistente = null;
    try { destinoExistente = form.getDestinationId(); } catch (e) { destinoExistente = null; }

    if (destinoExistente) {
      linkPlanilha = SpreadsheetApp.openById(destinoExistente).getUrl() + '  (ja existia)';
    } else {
      var ss = SpreadsheetApp.create(CONFIG.ID_POS + ' — Respostas da Prova');
      form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
      linkPlanilha = ss.getUrl();
      if (CONFIG.MOVER_PARA_PASTA) {
        aplicar_(function () {
          DriveApp.getFileById(ss.getId()).moveTo(DriveApp.getFolderById(CONFIG.FOLDER_ID));
        }, 'mover planilha para a pasta');
      }
    }
  }

  // ---- pasta ----
  if (CONFIG.MOVER_PARA_PASTA) {
    aplicar_(function () {
      DriveApp.getFileById(form.getId()).moveTo(DriveApp.getFolderById(CONFIG.FOLDER_ID));
    }, 'mover formulario para a pasta');
  }

  // ---- resumo ----
  var resumo =
    'FORMULARIO PREENCHIDO\n\n' +
    'Titulo ..........: ' + titulo + '\n' +
    'Origem ..........: ' + (criouNovo
        ? 'FORMULARIO NOVO — nao consegui abrir o FORM_ID configurado'
        : 'formulario existente ' + CONFIG.FORM_ID) + '\n' +
    'ID da Pos .......: ' + CONFIG.ID_POS + '\n' +
    'Questoes ........: ' + QUESTOES.length + '\n' +
    'Pontuacao total .: ' + totalPontos + '\n' +
    'Imagens .........: ' + imagensOk +
      (imagensFalhas.length ? '  (falharam: ' + imagensFalhas.join(', ') + ')' : '') + '\n\n' +
    'LINK PARA O ALUNO: ' + form.getPublishedUrl() + '\n' +
    'Link de EDICAO ..: ' + form.getEditUrl() + '\n' +
    'Planilha ........: ' + linkPlanilha + '\n\n' +
    'Quando a nota e liberada ao aluno so da para definir na interface:\n' +
    'abra o formulario -> Configuracoes -> Testes -> "Divulgar nota".\n';

  Logger.log(resumo);
  aplicar_(function () {
    MailApp.sendEmail(Session.getActiveUser().getEmail(),
                      '[' + CONFIG.ID_POS + '] Prova pronta no Google Forms', resumo);
  }, 'enviar e-mail de resumo');

  return resumo;
}

/** Conferencia rapida: imprime o gabarito no Log. */
function conferirGabarito() {
  var linhas = ['GABARITO (' + QUESTOES.length + ' questoes)'];
  var contagem = {};
  for (var i = 0; i < QUESTOES.length; i++) {
    linhas.push(QUESTOES[i].n + ' -> ' + QUESTOES[i].gab);
    contagem[QUESTOES[i].gab] = (contagem[QUESTOES[i].gab] || 0) + 1;
  }
  linhas.push('Distribuicao: ' + JSON.stringify(contagem));
  Logger.log(linhas.join('\n'));
}

/** Apaga todas as respostas ja recebidas. Use so para reaplicar a prova. */
function limparRespostas() {
  FormApp.openById(CONFIG.FORM_ID).deleteAllResponses();
  Logger.log('Respostas apagadas.');
}
