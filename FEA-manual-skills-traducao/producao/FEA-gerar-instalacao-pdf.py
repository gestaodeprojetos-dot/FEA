# -*- coding: utf-8 -*-
"""Gera o guia de instalação das skills de tradução em PDF.

O conteúdo vive aqui; a identidade visual e a composição vivem no
`FEA_estilo.py`, compartilhado com os outros PDFs desta pasta.

Uso, a partir de FEA-manual-skills-traducao/:
    python3 producao/FEA-gerar-instalacao-pdf.py
"""
import os

import FEA_estilo as estilo

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

HTML = """
<h2>O que você vai instalar</h2>
<p>Duas skills do Claude Code que trabalham em sequência. Skill é uma pasta com
instruções que o Claude carrega sozinho quando o assunto aparece: você não
precisa chamar pelo nome, nem decorar comando.</p>
<table>
<tr><th>Skill</th><th>O que faz</th></tr>
<tr><td>fea-traduccion-es</td><td>Traduz qualquer peça do catálogo de português para espanhol latino-americano, com terminologia travada por glossário, e monta o arquivo final</td></tr>
<tr><td>fea-revision-es</td><td>Revisa a tradução às cegas, como par especialista, e emite veredito de liberação</td></tr>
</table>
<p class="nota">Tempo de instalação: cerca de cinco minutos. Você precisa do
arquivo <b>FEA-skills-traducao-es.zip</b> e do Claude Code já instalado na
máquina.</p>

<h2>Passo 1. Escolha onde instalar</h2>
<p>São dois lugares possíveis, e a escolha muda quem passa a ter as skills.</p>
<table>
<tr><th>Opção</th><th>Onde</th><th>Vale para</th></tr>
<tr><td>Pessoal</td><td>a pasta oculta .claude/skills dentro da sua pasta de usuário</td><td>todos os seus projetos, só na sua máquina</td></tr>
<tr><td>Por projeto</td><td>a pasta .claude/skills dentro do projeto</td><td>todo mundo que abrir aquele projeto, porque vai junto no Git</td></tr>
</table>
<p>Se você trabalha sozinho com vários projetos, use a pessoal. Se a equipe
compartilha um repositório, use a por projeto: assim ninguém mais precisa
instalar nada.</p>

<h2>Passo 2. Descompacte no lugar certo</h2>

<h3>No Mac ou no Linux</h3>
<p>Abra o Terminal e vá até a pasta onde está o zip. Se não souber ir por
comando, arraste a pasta para a janela do Terminal depois de digitar
<b>cd</b> e um espaço: o caminho aparece sozinho. Então rode, para a opção
pessoal:</p>
<pre class="cmd">mkdir -p ~/.claude/skills
unzip FEA-skills-traducao-es.zip -d ~/.claude/skills/</pre>
<p>Para a opção por projeto, com o terminal aberto na pasta do projeto:</p>
<pre class="cmd">mkdir -p .claude/skills
unzip FEA-skills-traducao-es.zip -d .claude/skills/</pre>

<h3>No Windows</h3>
<p>Clique com o botão direito no zip, escolha «Extrair tudo» e aponte para a
pasta de destino. Para a opção pessoal, cole este caminho na barra de
endereço do Explorador de Arquivos, criando as pastas que faltarem:</p>
<pre class="cmd">%USERPROFILE%\\.claude\\skills</pre>
<p>Para a opção por projeto, é a pasta <b>.claude\\skills</b> dentro do projeto.</p>

<h3>Como tem de ficar</h3>
<pre class="cmd">skills/
├── INSTALAR.md
├── fea-traduccion-es/
│   ├── SKILL.md
│   ├── FICHA.md
│   ├── references/   (6 arquivos)
│   └── scripts/      (12 arquivos)
└── fea-revision-es/
    ├── SKILL.md
    └── references/rubrica.md</pre>
<p class="nota"><b>Erro mais comum.</b> Descompactar e ficar com uma pasta a
mais no caminho, do tipo skills barra FEA-skills-traducao-es barra
fea-traduccion-es. O arquivo SKILL.md tem de estar a exatamente um nível
abaixo de skills. Se ficou uma pasta sobrando, arraste as duas pastas de skill
para cima e apague a intermediária.</p>

<h2>Passo 3. Instale as dependências</h2>
<p>As skills traduzem e revisam sem nada extra, mas as verificações automáticas
e o levantamento de texto dentro de imagem precisam destes programas.</p>
<pre class="cmd">pip install pymupdf opencv-python-headless python-docx openpyxl</pre>
<p>E o leitor de texto em imagem, que é o que encontra rótulo dentro de arte:</p>
<pre class="cmd"># Mac
brew install tesseract tesseract-lang

# Ubuntu ou Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por tesseract-ocr-spa</pre>
<p>No Windows, baixe o instalador do Tesseract pelo projeto oficial e marque os
idiomas português e espanhol durante a instalação.</p>
<p class="nota">Sem o Tesseract a tradução funciona, mas o levantamento de texto
dentro de imagem não roda. No ebook de olheiras essa camada escondia 194 linhas
em 29 páginas, incluindo o título da capa. Vale instalar.</p>

<h2>Passo 4. Reinicie e confirme</h2>
<p>Feche e abra o Claude Code. Para conferir que ele enxergou as skills, peça
qualquer coisa que as acione, por exemplo:</p>
<pre class="cmd">traduza este parágrafo para espanhol: o preenchimento
da região infraorbital exige conhecimento do plano
supraperiosteal.</pre>
<p>Se a skill carregou, a resposta vem com a terminologia do glossário e o
tratamento formal, e o Claude começa perguntando pelo material completo em vez
de traduzir solto. Se nada mudou, veja a última seção.</p>

<h3>Conferência mais direta, por linha de comando</h3>
<p>Salve duas linhas em espanhol num arquivo de texto e rode o auditor. Ele é
determinístico: mesma entrada, mesma saída, sem opinião.</p>
<pre class="cmd">python3 ~/.claude/skills/fea-traduccion-es/scripts/auditar.py texto_es.txt</pre>
<p>A resposta esperada é um veredito com índice e contagem por classe. Código
de saída 0 significa liberado ou liberado com ressalvas; 1 significa retido.
Isso serve também para travar publicação automática, se um dia a equipe quiser
ligar essa checagem ao fluxo de trabalho.</p>

<h2>Como usar no dia a dia</h2>
<p>Não se chama a skill pelo nome. Pede-se em linguagem natural e ela aparece
sozinha:</p>
<ul>
<li>«traduza esta copy para espanhol»</li>
<li>«levante os vídeos e os links deste material»</li>
<li>«revise esta tradução antes de eu publicar»</li>
</ul>
<p>A primeira coisa que acontece é a curadoria: a skill levanta o que existe no
material, separa o que traduz do que não traduz, e mostra o mapa <b>antes</b> de
traduzir qualquer palavra. Isso é de propósito, e é o que evita descobrir no
fim que metade da peça era arte, vídeo e link apontando para conteúdo em
português.</p>
<p>O que ajuda mandar junto com o material: onde a peça vai rodar, quem é o
leitor, limite de caracteres quando houver, os arquivos de arte e os links de
destino. O manual da skill tradutora detalha cada um.</p>

<h2>Se não funcionar</h2>
<table>
<tr><th>Sintoma</th><th>Causa provável</th><th>O que fazer</th></tr>
<tr><td>O Claude ignora a skill</td><td>caminho errado, com pasta sobrando</td><td>confira que SKILL.md está um nível abaixo de skills, como no desenho do passo 2</td></tr>
<tr><td>O Claude ignora a skill</td><td>não reiniciou</td><td>feche e abra o Claude Code</td></tr>
<tr><td>O auditor não roda</td><td>falta o pymupdf</td><td>rode de novo o pip install do passo 3</td></tr>
<tr><td>Não acha texto dentro de imagem</td><td>falta o Tesseract, ou faltam os idiomas</td><td>instale com os pacotes de português e espanhol</td></tr>
<tr><td>Não acha a pasta oculta</td><td>o sistema esconde pastas que começam com ponto</td><td>no Mac, Cmd + Shift + ponto no Finder; no Windows, ative «Itens ocultos» na aba Exibir</td></tr>
</table>
<p class="nota">Se travou em algo que não está nesta tabela, mande o print da
tela e o caminho onde você descompactou. Com essas duas informações dá para
responder sem adivinhação.</p>

<h2>Uma observação sobre manutenção</h2>
<p>As skills guardam o que aprendem: termo novo entra no glossário, decisão
nova entra no registro de decisões. Quem instalar uma cópia pessoal fica com a
versão do dia em que instalou e não recebe o que for acrescentado depois.</p>
<p>Por isso a opção por projeto é a melhor para equipe: as skills vão junto no
repositório, e todo mundo trabalha sempre com a mesma versão, a mais recente.
Em cópia pessoal, vale repetir o passo 2 sempre que sair uma atualização.</p>

<h2>Checklist rápido</h2>
<p>Para quem já instalou outras vezes e só quer conferir se não pulou nada.</p>
<table>
<tr><th>Feito</th><th>Item</th></tr>
<tr><td>[ ]</td><td>Decidi entre instalação pessoal e por projeto</td></tr>
<tr><td>[ ]</td><td>Descompactei e o SKILL.md ficou um nível abaixo de skills, sem pasta sobrando</td></tr>
<tr><td>[ ]</td><td>As duas pastas estão lá: fea-traduccion-es e fea-revision-es</td></tr>
<tr><td>[ ]</td><td>Rodei o pip install das quatro bibliotecas</td></tr>
<tr><td>[ ]</td><td>Instalei o Tesseract com português e espanhol</td></tr>
<tr><td>[ ]</td><td>Fechei e abri o Claude Code</td></tr>
<tr><td>[ ]</td><td>Testei com um pedido de tradução e a terminologia veio do glossário</td></tr>
<tr><td>[ ]</td><td>Rodei o auditor num texto de teste e saiu veredito</td></tr>
</table>
<p class="legenda">Guia produzido em 23 de setembro de 2026. As skills e este
guia ficam no repositório do projeto, na pasta FEA-manual-skills-traducao.</p>
"""

estilo.montar(
    saida='FEA-guia-instalacao-skills.pdf',
    titulo=['Instalar as skills', 'de tradução'],
    subtitulo=[
        'Guia passo a passo para o time colocar as duas skills',
        'de tradução e revisão para funcionar, em cerca de cinco',
        'minutos, com o que fazer se algo não pegar.',
    ],
    data='23 de setembro de 2026',
    html=HTML,
    rodape='Instalar as skills de tradução',
    metadados={
        'title': 'Guia de instalação das skills de tradução FEA',
        'author': 'FEA',
        'subject': 'Passo a passo para instalar fea-traduccion-es e fea-revision-es',
    },
)
