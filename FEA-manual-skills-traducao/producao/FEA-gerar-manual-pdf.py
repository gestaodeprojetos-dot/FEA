# -*- coding: utf-8 -*-
"""Gera o manual da skill tradutora em PDF, identidade FEP Experience.

O conteúdo vive aqui; a identidade visual e a composição vivem no
`FEA_estilo.py`, compartilhado com os outros PDFs desta pasta.

Uso, a partir de FEA-manual-skills-traducao/:
    python3 producao/FEA-gerar-manual-pdf.py
"""
import os

import FEA_estilo as estilo

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

HTML = """
<h2>O que a skill garante</h2>
<p>Quatro coisas, em qualquer peça, do post de trinta palavras a apostila de
duzentas páginas.</p>
<ul>
<li><b>Terminologia travada por glossário.</b> O mesmo termo técnico sai igual
em todo o catálogo: no ebook, no criativo e no disparo. Nada de termo decidido
no improviso.</li>
<li><b>Espanhol que soa nativo, não traduzido.</b> Uma peça pode ter todos os
termos certos e ainda denunciar português na sintaxe, na pontuação e nos
conectores. O leitor percebe em três parágrafos.</li>
<li><b>Barreira clínica.</b> Dose, unidade, via, plano anatômico, lado e
sentido, contraindicação. Sempre que a peça tocar num desses, a conferência é item por item, mesmo num story.</li>
<li><b>Registro formal uniforme.</b> «usted» em tudo, sem mistura com «tu».
Vale também para copy de venda: no espanhol técnico latino-americano, tutear o
profissional soa amador.</li>
</ul>
<p class="nota">O material FEA é lido por injetores que vão reproduzir a
técnica em pacientes. Um termo trocado num criativo não é erro de estilo, é
perda de autoridade diante de um público que reconhece terminologia.</p>

<h2>Curadoria, antes de traduzir uma única palavra</h2>
<p>A pergunta que esta etapa responde: o que exatamente existe nesta peça, e o
que de tudo isso precisa de versão em espanhol?</p>
<p>Traduzir primeiro e inventariar depois produz retrabalho garantido. O texto
sai pronto, e só então se descobre que boa parte do material não é texto: e
arte, áudio, link e destino apontando para conteúdo em português.</p>

<h3>O que se levanta</h3>
<table>
<tr><th>O que é</th><th>Onde costuma estar escondido</th></tr>
<tr><td>Texto editável</td><td>o óbvio: corpo, título, legenda, assunto</td></tr>
<tr><td>Texto dentro de imagem</td><td>selo, rótulo, balão, thumbnail, card, capa, sobreposição de vídeo</td></tr>
<tr><td>Áudio e vídeo</td><td>fala do apresentador, legenda queimada, trilha com locução</td></tr>
<tr><td>Links e destinos</td><td>botão, QR, link de bio, redirecionador, checkout, formulário</td></tr>
<tr><td>Material de terceiros</td><td>artigo científico, prancha de atlas, citação, print de estudo</td></tr>
</table>
<p class="legenda">As quatro ultimas linhas são as que passam batido. Texto
dentro de imagem não aparece em nenhuma busca por texto; link em português
continua funcionando, só que leva o hispano-hablante para uma página que ele não lê.</p>

<h3>Cada item recebe uma marca</h3>
<ul>
<li><b>TRADUZ:</b> texto corrido, rótulo em português na arte, fala do autor,
CTA, assunto de e-mail.</li>
<li><b>NAO TRADUZ:</b> citação bibliográfica, artigo científico, marca, nome
comercial, princípio ativo, prancha de atlas de terceiros.</li>
<li><b>DECIDE O AUTOR:</b> rótulo em inglês dentro de arte de terceiros; slide
do próprio autor que já está em inglês; destino que aponta para material em
outro idioma.</li>
</ul>
<p>Item sem marca é item que vai dar problema depois. Nenhum fica sem.</p>

<h3>O mapa vai ao time antes de começar</h3>
<p>Com quatro informações: contagem por tipo, inventário dos ativos com link,
lista do que depende de decisão, e a estimativa do que não é tradução de
texto.</p>
<p>O último ponto é o que evita surpresa de orçamento. Traduzir a copy e
barato; regravar o vídeo, refazer o criativo e reconfigurar a página de destino
não são. Isso precisa estar na mesa antes da aprovacao, não depois.</p>
<p class="nota"><b>Fronteira do escopo.</b> A skill lista os ativos de mídia
com rótulo, assunto e link, para que sejam localizados depois. Ela não produz
vídeo, não legenda, não dubla e não desenha criativo: isso e decisão e execução
da FEA.</p>

<h2>As tres passagens</h2>
<p>Cada uma pega uma classe de erro diferente. Nenhuma substitui a outra, e
nenhuma se pula, nem numa peça curta.</p>
<h3>1. Tradução</h3>
<p>Por blocos de sentido, não linha a linha. Mantem estrutura, hierarquia e
registro formal. Sigla de autor e recalculada sem quebrar: se a sigla nasce das
iniciais das palavras, as palavras em espanhol tem de fechar a mesma sigla, e
às vezes isso decide qual sinônimo usar.</p>
<h3>2. Auditoria mecânica</h3>
<p>Um script determinístico varre resíduo de português, lusismo sintático,
falso amigo clínico, posologia, via de administração, ortotipografia e
tratamento. Roda em segundos e não tem opinião. Depois dele, varredura à mão do
que ele não modela: cada entrada do glossário, grafia de marca, e coerência do
mesmo termo ao longo de toda a peça.</p>
<h3>3. Back-translation dos trechos técnicos</h3>
<p>Retraduz para português só o que tem carga técnica (dose, diluição,
anatomia, passo a passo, manejo de complicação) e compara com o original. É
esta passagem que pega o erro silencioso: o número certo na estrutura errada, o
ligamento trocado, a ordem dos passos invertida, o «não» perdido. São erros que
o espanhol não denuncia, porque a frase fica perfeitamente legível dizendo
outra coisa.</p>
<p class="nota">Numa peça sem carga clínica, como um convite ou um lembrete de
aula, a passagem 3 leva um minuto porque não há o que conferir. Isso não é
motivo para pulá-la: é a verificação de que realmente não há.</p>

<h2>As regras que valem sempre</h2>
<p>Válidas em qualquer peça, sem exceção de formato ou de pressa.</p>
<ul>
<li><b>Citação bibliográfica não se traduz.</b> Título de artigo, revista,
autores, DOI, abstract. Ficam como estão.</li>
<li><b>Marca e princípio ativo não se traduzem.</b> Grafia exata, com o símbolo
de registro onde o original traz.</li>
<li><b>Erro de digitação do original se corrige em silêncio</b> no espanhol e se
lista à parte para o autor. Nunca se replica o erro por fidelidade, e nunca se
corrige sem avisar.</li>
<li><b>Nunca se inventa dose, unidade ou nome de produto</b> que não esteja no
original. Se o original e ambíguo, a tradução mantem a ambiguidade e sinaliza ao
autor. Desambiguar por conta própria é inventar conteúdo clínico.</li>
<li><b>Texto dentro de imagem exige leitura da imagem, não inspeçao.</b> Olhar a
peça e achar que viu tudo é o jeito mais comum de perder metade dos rótulos.</li>
<li><b>Termo novo entra no glossário.</b> Todo trabalho deixa depósito: termos
novos no módulo do tema, decisões no registro de decisões. Um glossário que não cresce é um glossário que vai sendo abandonado.</li>
</ul>

<h3>Converter números e formato</h3>
<table>
<tr><th>Item</th><th>Espanhol LatAm</th></tr>
<tr><td>Decimal</td><td>vírgula: 0,5 mL</td></tr>
<tr><td>Milhar</td><td>ponto: 1.000 UI</td></tr>
<tr><td>Unidade</td><td>espaço entre cifra e unidade, mL com L maiúsculo</td></tr>
<tr><td>Interrogação e exclamação</td><td>abrem com os sinais invertidos, inclusive em título de criativo e assunto de e-mail</td></tr>
<tr><td>Aspas</td><td>angulares no texto corrido</td></tr>
<tr><td>Data</td><td>23 de septiembre de 2026, sem ordinal</td></tr>
</table>

<h2>O que muda por tipo de peça</h2>
<p>O processo é o mesmo. O que muda é onde está o risco.</p>
<table>
<tr><th>Tipo de peça</th><th>O que a curadoria costuma achar</th><th>O que dá problema com mais frequência</th></tr>
<tr><td>Criativo</td><td>quase todo o texto está dentro da imagem; selo e rótulo esquecidos</td><td>texto longo demais: o espanhol corre 10% a 20% mais que o português e estoura a arte</td></tr>
<tr><td>Copy de página</td><td>CTA de botão, campo de formulário, texto de erro, depoimento, rodapé legal</td><td>ênfase comercial brasileira traduzida ao pé da letra; destino do botão continuar em português</td></tr>
<tr><td>Mensagem de disparo</td><td>assunto, pré-cabeçalho, link encurtado, assinatura</td><td>limite de caracteres; tuteo escapando no tom informal; link levando a página em português</td></tr>
<tr><td>Roteiro e legenda</td><td>fala, sobreposição na tela, card final</td><td>marcador de tempo não sobrevive a regravação, porque corte diferente move o trecho</td></tr>
<tr><td>Aula e apostila</td><td>infográfico, tabela de dose, referência bibliográfica</td><td>inconsistência interna: o mesmo termo com dois nomes em páginas diferentes</td></tr>
<tr><td>Texto longo diagramado</td><td>texto em arte, sumário, rótulo de figura</td><td>refluxo: o espanhol mais longo desarruma a página</td></tr>
</table>

<h3>Vale para toda peça curta</h3>
<p>O espanhol corre mais longo. Num ebook isso vira problema de diagramação;
num criativo, num botão e num assunto de e-mail vira texto cortado. Quando
houver limite de caracteres ou caixa fixa, informe o limite junto com o
material, e a skill ajusta a redação para caber, em vez de entregar algo que o
time descobre que não cabe.</p>

<h3>Vale para toda peça com link</h3>
<p>Link que funciona não quer dizer link certo. Um botão traduzido apontando
para a página em português não quebra nada, só entrega o lead numa página que
ele não lê. Todo destino entra no inventário com o link atual e o link em
espanhol, mesmo que o segundo ainda não exista.</p>

<h2>As armadilhas de marketing</h2>
<p>Os pontos em que a tradução correta ainda soa errada.</p>
<ul>
<li><b>Ênfase comercial brasileira não atravessa.</b> «Transforme sua carreira»,
«destrave seu potencial», «o segredo que ninguém te conta»: traduzidos ao pé da letra, soam infantis em espanhol técnico dirigido a médico. O equivalente não é
a tradução, é a promessa reescrita no registro que o público aceita.</li>
<li><b>Superlativo empilhado denuncia origem.</b> O português comercial acumula
intensificadores; o espanhol técnico corta. Uma frase com dois adjetivos de
reforço em português costuma sair melhor com nenhum.</li>
<li><b>Conector repetido é a marca registrada de texto traduzido.</b> «Además» e
«por lo tanto» abrindo paragrafo atras de paragrafo entregam o jogo, mesmo com
terminologia perfeita.</li>
<li><b>Tuteo escapa no tom informal.</b> É o erro mais comum em disparo de
WhatsApp: a peça inteira em «usted» e um «te esperamos» no fim. O material fica
com dois registros, e o leitor sente a costura.</li>
<li><b>Trocadilho e rima raramente sobrevivem.</b> Quando o criativo depende de
um jogo de palavras, a skill sinaliza e propõe alternativa, em vez de traduzir
literalmente e entregar algo sem graça fingindo que funcionou.</li>
<li><b>Referência cultural brasileira não é universal.</b> Data comemorativa,
gíria regional, formato de programa de TV, nome de banco ou de parcelamento.
Cada uma precisa de equivalente local ou de substituição, e LatAm não é um país só: o espanhol entregue é neutro justamente para não soar mexicano no Chile nem
argentino na Colômbia.</li>
</ul>
<p class="nota">Quando a peça for de marketing, diga na hora de pedir o objetivo
da peça e quem é o leitor. «Anúncio para médico já formado» e «captura para quem
nunca injetou» pedem dois registros diferentes, e a skill não adivinha qual é pelo texto em português.</p>

<h2>Como pedir</h2>
<p>Não se chama a skill pelo nome. Pede-se em linguagem natural e ela aparece
sozinha: «traduza esta copy para espanhol», «levante os links deste material»,
«revise esta tradução antes de eu publicar».</p>
<p>O que vale a pena mandar junto, porque a skill não adivinha pelo texto em
português:</p>
<table>
<tr><th>Informe</th><th>Por que muda a entrega</th></tr>
<tr><td>Onde a peça vai rodar</td><td>anúncio, página, WhatsApp e slide pedem redações diferentes</td></tr>
<tr><td>Quem é o leitor</td><td>médico formado, aluno iniciante ou público leigo mudam o registro</td></tr>
<tr><td>Limite de caracteres ou caixa fixa</td><td>o espanhol corre mais longo; com o limite, a skill escreve para caber</td></tr>
<tr><td>Os arquivos de arte, não só o texto</td><td>sem eles não se levanta o que está dentro da imagem</td></tr>
<tr><td>Os links de destino</td><td>para marcar quais precisam de versão em espanhol</td></tr>
<tr><td>Prazo e o que é negociável</td><td>define se a curadoria sai completa ou prioriza</td></tr>
</table>

<h3>O que volta</h3>
<ol>
<li>O mapa do material, antes de qualquer tradução, com o que traduz, o que não
traduz e o que depende de decisão.</li>
<li>A tradução, no formato pedido.</li>
<li>O inventário de mídia e links, com o que ainda precisa de versão em
espanhol.</li>
<li>A lista de correções do original, com os erros encontrados no português que
valem correção la tambem.</li>
</ol>
<p>Se durante a tradução aparecer item que a curadoria não pegou, o mapa e
atualizado. Não se resolve de improviso.</p>

<h2>Depois da tradução: a revisão</h2>
<p>Tradução própria não se auto-aprova. Ao fechar, o material passa para a skill
revisora, «fea-revision-es», que lê como par especialista e emite veredito. A
revisão é deliberadamente cega: recebe o texto em espanhol, o original em
português e os glossários, e nenhuma justificativa do tradutor. Quem traduz
acumula razões para as próprias escolhas, e essas razões cegam para o erro.</p>
<p>O veredito vem em dois níveis separados, e o percentual só existe no
segundo.</p>
<h3>Classe A, barreira clínica, tolerância zero</h3>
<p>Dose, concentração, unidade, posologia, via, nome de fármaco, plano
anatômico, camada, lado e sentido, negação, trecho omitido, alerta suavizado,
tuteo em material formal. Um único achado retém a entrega, qualquer que seja o
índice. Não se calcula percentual de segurança clínica.</p>
<h3>Classe B, índice editorial</h3>
<p>Terminologia fora do glossário, lusismo, inconsistência interna,
ortotipografia, registro, conector.</p>
<table>
<tr><th>Índice</th><th>Veredito</th><th>O que o time faz</th></tr>
<tr><td>95% ou mais</td><td>LIBERADO</td><td>publica, e os pontos anexos entram na proxima rodada</td></tr>
<tr><td>80% a 95%</td><td>COM RESSALVAS</td><td>publica, com os pontos priorizados a vista</td></tr>
<tr><td>abaixo de 80%</td><td>RETIDO</td><td>volta para tradução antes de publicar</td></tr>
</table>
<p class="legenda">A faixa do meio existe de propósito: imperfeição não trava
entrega. O que trava é classe A, e só ela.</p>
<p>Há ainda uma terceira categoria que não entra em nenhuma das duas: questão ao
autor, quando o original e ambíguo, se contradiz ou tem erro próprio. Não e
defeito de tradução e não afeta o veredito, tanto que uma peça pode sair
liberada com cinco questoes abertas.</p>

<h2>Onde ficam as skills</h2>
<p>As duas ficam em «.claude/skills/» no repositório do projeto, versionadas no
Git. Copiadas para «~/.claude/skills/» valem em qualquer projeto da pessoa.</p>
<table>
<tr><th>Pasta</th><th>O que tem dentro</th></tr>
<tr><td>fea-traduccion-es</td><td>SKILL.md com o processo, FICHA.md, 6 glossários em references, 12 scripts em scripts</td></tr>
<tr><td>fea-revision-es</td><td>SKILL.md com a revisão cega em quatro camadas, rubrica de severidade em references</td></tr>
</table>
<p>Dependências: «pip install pymupdf opencv-python-headless python-docx
openpyxl» e o tesseract com os pacotes de português e espanhol. Sem elas a
tradução funciona, mas as verificações automáticas e o levantamento de arte e
QR não rodam.</p>
"""

estilo.montar(
    saida='FEA-manual-skill-tradutora.pdf',
    titulo=['Manual da skill', 'tradutora'],
    subtitulo=[
        'Como o time usa a skill que traduz qualquer peça do catálogo',
        'de português para espanhol latino-americano: criativo, copy',
        'de página, mensagem de disparo, roteiro, legenda, e-mail,',
        'post, aula, apostila.',
    ],
    data='23 de setembro de 2026',
    html=HTML,
    rodape='Manual da skill tradutora',
    metadados={
        'title': 'Manual da skill tradutora PT para ES',
        'author': 'FEA',
        'subject': 'Como o time usa a skill fea-traduccion-es em qualquer material',
    },
)
