# Conteúdo das páginas ES do Ebook Olheiras LATAM, fiel às copys corrigidas de 20/10/2026
# (docs "FEA-ES | ..." da pasta 1. COPY / 1. PÁGINAS,
# https://drive.google.com/drive/folders/15RFlmEyX_sWqlCHJuL8ZPEo-YA0m8TgB).
# Copy em espanhol (es-419, usted). Notas para o designer em português.
# Regras: FEA-traducoes/FEA-olheiras-latam-drive/FEA-regras-correcao-copys-latam.md
# Preço (gestão, 05/10/2026): de US$47 por US$19 (60 % de descuento), pagamento único, sem parcelas.
# Upsell (gestão, 20/10/2026): US$97 à vista, sem parcelas.
# Autoridade (gestão, 20/10/2026): 9 países, más de 10.000 ml, más de 30.000 alumnos, +30 mil copias vendidas.
# Sem contagem regressiva nas páginas (urgência fabricada removida).

PRECO = 'US$19'
PRECO_DE = 'US$47'
DESCONTO = '60 % de descuento'
CONDICAO = 'Pago único con tarjeta de crédito o débito.'
PRECO_UPSELL = 'US$97'
CHECKOUT = '[LINK DEL CHECKOUT EN USD: PENDIENTE]'
CHECKOUT_UPSELL = '[LINK DEL CHECKOUT DEL UPSELL EN USD: PENDIENTE]'
WPP = '[WHATSAPP DE SOPORTE LATAM: PENDIENTE]'
CASO = '[NOMBRE DEL CASO CLÍNICO: A CONFIRMAR]'
NOME_UPSELL = '[NOMBRE DEL PRODUCTO DEL UPSELL EN ESPAÑOL: A CONFIRMAR]'
NOTA_PRECO = 'Preço definido pela gestão: de US$47 (riscado) por US$19, 60 % de desconto, pagamento único com cartão de crédito ou débito, sem parcelas.'
NOTA_AUTORIDADE = 'Números de autoridade padronizados pela gestão em 20/10/2026: 9 países, más de 10.000 ml, más de 30.000 alumnos, +30 mil copias vendidas.'
NOTA_DEPO = 'Print original em português com legenda ES "Testimonio original en portugués" (decisão da gestão em 05/10/2026). Conferir TCLE de fotos de paciente.'
EBOOK = 'Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI'
IDV_EBOOK = 'https://drive.google.com/file/d/1W2gI1BCdKl7BT55sMsUSsRj9Zh0xFj8f/view'
FOOTER = {'id': 'rodape', 'nome': 'Rodapé', 'tipo': 'footer', 'texto': ['Formación Especialista Academy · © 2026 · Todos los derechos reservados']}
SELOS = ['Hotmart', 'Garantía de 7 días']


def contato(sobre):
    return {'id': 'duvidas', 'nome': 'Dúvidas', 'tipo': 'contact', 'titulo': '¿LE QUEDÓ ALGUNA DUDA?',
            'texto': [f'Si le quedó cualquier duda sobre {sobre}, hable con mi equipo por WhatsApp: {WPP}'],
            'cta': {'texto': '¡Quiero hablar con el equipo!', 'acao': WPP},
            'nota_designer': 'Botão abre o WhatsApp de atendimento LATAM em espanhol (número pendente).'}


MODULOS = [
    ('Introducción al Razonamiento Clínico para el Relleno de Ojeras', [
        'Comprenda cómo el proceso de envejecimiento impacta la región periorbitaria.',
        'Refuerce su base anatómica para diagnosticar correctamente cada caso.',
        'Aprenda a identificar la estructura ósea, los compartimentos grasos y los ligamentos.']),
    ('Anatomía de la Región Infraorbitaria', [
        'Profundice en los detalles anatómicos más relevantes del área más delicada del rostro.',
        'Descubra cómo cada estructura influye en la elección del producto y de la técnica.']),
    ('Reología: La Elección del Producto de Relleno Ideal', [
        'Domine el concepto de Swelling Factor (SF) y su influencia en el resultado final.',
        'Aprenda a seleccionar los productos más adecuados para ojeras y a evitar intercurrencias.']),
    ('Técnica Avanzada de Relleno Tridimensional', [
        'Acceda al paso a paso detallado de la técnica ARTI.',
        'Aprenda a analizar y marcar los ligamentos con precisión.',
        'Descubra los puntos de acceso correctos (puntos de entrada).',
        'Domine la técnica de layering (por capas) para resultados naturales y duraderos.']),
    ('Intercurrencias y Manejo de Complicaciones', [
        'Técnicas de prevención del edema persistente.',
        'Cómo evitar y tratar el efecto Tyndall.',
        'Corrección de irregularidades de relieve.',
        'Manejo seguro de hematomas.',
        'Cuidados posprocedimiento orientados a la seguridad y la satisfacción del paciente.']),
]

HERO_CLASSICO = {
    'id': 'hero', 'nome': 'Hero', 'tipo': 'hero',
    'titulo': 'Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y trabaje con seguridad, previsibilidad y resultados naturales y duraderos.',
    'texto': ['Esta guía muestra cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e Intercurrencias) en el relleno de ojeras, la región más delicada del rostro, con un razonamiento clínico que reduce el margen de error justo donde la mayoría falla.'],
    'cta': {'texto': '¡Quiero dominar la técnica tridimensional!', 'acao': '#oferta'},
}

PASSOS = {'id': 'passos', 'nome': 'Oferta: 4 passos', 'tipo': 'steps', 'titulo': 'Domine el relleno tridimensional de ojeras en 4 pasos:',
          'itens': [{'titulo': 'Paso 01', 'texto': 'Anatomía detallada de la región infraorbitaria'},
                    {'titulo': 'Paso 02', 'texto': 'Reología y elección del producto de relleno ideal'},
                    {'titulo': 'Paso 03', 'texto': 'Técnica avanzada de relleno tridimensional (paso a paso)'},
                    {'titulo': 'Paso 04', 'texto': 'Intercurrencias y manejo de complicaciones'}]}

BONUS = {'id': 'bonus', 'nome': 'Bônus', 'tipo': 'bonuses', 'titulo': '+03 Bonos Exclusivos',
         'itens': [{'titulo': f'Bono 0{i}', 'texto': f'Caso clínico {i}: {CASO}'} for i in (1, 2, 3)],
         'nota_designer': 'Ícone de presente antes do título. Nome de cada caso clínico pendente na copy: manter o marcador até a copy definir.'}

OFERTA_EBOOK = {'id': 'oferta', 'nome': 'Oferta especial', 'tipo': 'offer', 'titulo': 'Oferta Especial',
                'preco_de': PRECO_DE, 'preco': PRECO, 'prefixo_preco': 'Por solo', 'desconto': DESCONTO, 'condicao': CONDICAO,
                'cta': {'texto': 'Quiero mi e-book con descuento', 'acao': CHECKOUT},
                'selos': SELOS,
                'nota_designer': 'Ícone de bolsa de dinheiro antes do título. Bloco de oferta sem contagem regressiva (removida por ser urgência fabricada). ' + NOTA_PRECO}

MENTOR_CLASSICO = {
    'id': 'mentor', 'nome': 'Autoridade', 'tipo': 'authority', 'titulo': 'João Pithon, su mentor',
    'texto': ['Soy el Dr. João Pithon, médico, coautor del libro Arquitetura Facial, coordinador de cursos y CEO del Instituto Pithon Napoli.',
              'Después de recorrer 9 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 10.000 ml aplicados sin intercurrencias isquémicas.',
              'Ya he formado a más de 30.000 alumnos con estas técnicas. Mi metodología le permitirá ver una nueva forma de trabajar el relleno, con razonamiento anatómico y previsibilidad.',
              'Este e-book ya suma +30 mil copias vendidas.',
              'En 2019, decidí dedicarme a los procedimientos mínimamente invasivos en la medicina estética, con un foco claro: la anatomía como base de la seguridad. Desde entonces, estudio la región facial en cadáveres frescos para entender, capa por capa, dónde están las zonas de riesgo y cómo evitarlas.',
              'Es ese mismo razonamiento clínico el que comparto en este e-book, para que usted aplique la técnica con criterio, consistencia y previsibilidad en su práctica clínica.'],
    'cta': {'texto': 'Quiero aprender con el Dr. João Pithon', 'acao': '#oferta'},
    'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João à direita'}],
    'nota_designer': NOTA_AUTORIDADE + ' Bloco reescrito em tom médico-científico (anatomia, cadáver fresco, zonas de risco).'}

FAQ_CLASSICO = {'id': 'faq', 'nome': 'FAQ', 'tipo': 'faq', 'titulo': 'FAQ (Preguntas Frecuentes)',
                'itens': [{'titulo': '¿Cómo recibiré el e-book?', 'texto': 'Después de la compra, usted recibirá de inmediato el enlace para descargarlo en PDF.'},
                          {'titulo': '¿Tendré acceso de por vida?', 'texto': 'Sí. El e-book es suyo para siempre.'},
                          {'titulo': '¿Cuál es la forma de pago?', 'texto': 'Tarjeta de crédito o débito, en pago único, a través de Hotmart.'},
                          {'titulo': '¿Hay garantía?', 'texto': 'Sí. Usted cuenta con 7 días de garantía incondicional. Si no queda satisfecho, le devolvemos su inversión.'},
                          {'titulo': '¿Necesito internet para acceder?', 'texto': 'Solo para descargarlo. Después, puede leerlo sin conexión en el celular, la tableta o la computadora.'}],
                'cta': {'texto': 'Quiero mi acceso ahora con riesgo cero', 'acao': '#oferta'}}

MODULOS_SEC = {'id': 'conteudo', 'nome': 'O que vai aprender', 'tipo': 'modules', 'titulo': 'Lo que usted aprenderá con este e-book',
               'texto': [f'El e-book {EBOOK} fue estructurado para brindarle claridad, seguridad y confianza en cada etapa del procedimiento.'],
               'itens': [{'titulo': t, 'lista': l} for t, l in MODULOS],
               'cta': {'texto': 'Quiero asegurar mi e-book ahora mismo', 'acao': '#oferta'},
               'nota_designer': 'Listas expansíveis (accordion), como sugere a copy.'}


def base(slug, nome, fonte, identidade, secoes, pend, produto=f'Ebook {EBOOK}'):
    return {'pagina': nome, 'slug': slug, 'produto': produto, 'mercado': 'LATAM', 'idioma': 'es-419',
            'tratamento': 'usted', 'revisao': '20/10/2026', 'fonte_copy': fonte, 'identidade_visual': identidade,
            'paleta_padrao_html': {'roxo': '#5B4599', 'azul_violeta': '#3846BB', 'lavanda': '#D0D1E9', 'alerta': '#BB3838', 'fundo': '#F9F9F9', 'borda': '#E9E9E9'},
            'tipografia': {'titulos': 'Sora 600-800', 'corpo': 'Montserrat 400-500'},
            'pendencias': pend, 'secoes': secoes}


DOC = 'https://docs.google.com/document/d/{}/edit'
PEND_EBOOK = [CHECKOUT + ' (botão de compra do ebook, Hotmart em USD).']

PAGINAS = []

PAGINAS.append(base('pagina-ventas', 'Página de ventas - eBook de Ojeras',
    DOC.format('1DcfgS833430UPwl7_X1E9WLBkbWc2ek37udyS0ylLSE'), IDV_EBOOK + ' (versão ES)', [
    dict(HERO_CLASSICO, midia=[{'tipo': 'mockup', 'descricao': 'Mockup ao lado com a capa ES do ebook (e foto do Dr. João, se der para compor). Capa real da edição ES, nunca gerada por IA.'}]),
    {'id': 'depoimentos', 'nome': 'Depoimentos', 'tipo': 'testimonials', 'titulo': 'Lo que dicen sobre la Técnica Tridimensional de Relleno de Ojeras',
     'midia': [{'tipo': 'prints', 'descricao': 'Mesmos depoimentos e prints da página de vendas da Imersão de Olheiras'}],
     'cta': {'texto': 'Quiero aplicar la técnica con este nivel de previsibilidad', 'acao': '#oferta'},
     'nota_designer': NOTA_DEPO},
    {'id': 'dor', 'nome': 'Obstáculos', 'tipo': 'pain', 'titulo': '¿Qué le impide alcanzar la excelencia en el relleno de ojeras?',
     'contras': ['Inseguridad ante intercurrencias como edema, irregularidades o efecto Tyndall.', 'Dudas sobre el producto ideal, la profundidad y el abordaje correcto.', 'Resultados inconsistentes, sin naturalidad ni duración.'],
     'subtitulo': 'Imagine ahora:',
     'pros': ['Elegir productos con fundamento científico.', 'Dominar la anatomía y aplicar con precisión.', 'Usar una técnica tridimensional validada y segura.']},
    {'id': 'passo-a-passo', 'nome': 'Conteúdo do ebook', 'tipo': 'features', 'titulo': 'El paso a paso de la técnica tridimensional en sus manos', 'texto': ['En el e-book, usted tendrá acceso a:'],
     'itens': [{'titulo': 'Revisión anatómica y reológica', 'texto': 'comprenda a fondo el comportamiento de los productos de relleno.'},
               {'titulo': 'Técnica Tridimensional', 'texto': 'paso a paso completo.'},
               {'titulo': 'Comparación con otras técnicas', 'texto': 'MD Codes y demás abordajes clásicos.'},
               {'titulo': 'Intercurrencias y soluciones', 'texto': 'cómo diagnosticarlas y tratarlas con seguridad.'}],
     'cta': {'texto': 'Quiero aprender la técnica tridimensional ahora', 'acao': '#oferta'},
     'nota_designer': '"MD Codes" é método associado a uma marca (Allergan): confirmar com a gestão se pode ser citado na página LATAM.'},
    {'id': 'acesso', 'nome': 'Acesso', 'tipo': 'list', 'titulo': 'Estudie a su ritmo, con acceso inmediato y de por vida',
     'lista': ['E-book digital en PDF entregado inmediatamente después de la compra.', 'Lectura sencilla y práctica en cualquier dispositivo.', 'Estudio flexible, en sus tiempos.', 'Material de consulta permanente, basado en ciencia y práctica clínica.'],
     'cta': {'texto': 'Quiero mi acceso inmediato al e-book', 'acao': '#oferta'}},
    {'id': 'para-quem', 'nome': 'Para quem é', 'tipo': 'pain', 'titulo': '¿Este e-book es para usted?',
     'pros': ['Para inyectores que buscan la excelencia en el relleno de ojeras.', 'Para quienes buscan seguridad, confianza y previsibilidad en los resultados.', 'Para quienes entienden que la diferenciación proviene del dominio científico sumado a una práctica refinada.'],
     'contras': ['No es para quienes buscan atajos sin estudiar.', 'No es para quienes no están dispuestos a aplicar el conocimiento adquirido.', 'No es para quienes creen que la armonización facial es solo «inyectar producto», sin ciencia ni técnica.'],
     'ordem': 'pros_primeiro', 'cta': {'texto': 'Sí, quiero ser un inyector de excelencia', 'acao': '#oferta'}},
    MODULOS_SEC, PASSOS, BONUS, OFERTA_EBOOK,
    {'id': 'custo', 'nome': 'Custo de adiar', 'tipo': 'pain', 'titulo': 'Postergar también tiene un costo',
     'contras': ['Seguir sin dominar esta técnica significa trabajar expuesto a intercurrencias evitables, a la inseguridad en la indicación y a resultados poco previsibles.', 'Significa dejar de atender casos que hoy usted ya podría resolver con criterio técnico.'],
     'pros': ['Con este e-book, usted tendrá una guía de consulta para trabajar el relleno de ojeras con seguridad y previsibilidad.'],
     'cta': {'texto': 'Quiero mi e-book ahora', 'acao': '#oferta'}},
    MENTOR_CLASSICO, FAQ_CLASSICO, contato(f'la compra del e-book {EBOOK}'), FOOTER],
    PEND_EBOOK + [WPP, CASO + ' (3 bônus).', 'Depoimentos: prints em PT com legenda ES "Testimonio original en portugués".',
                  'Confirmar com a gestão se "MD Codes" (método associado à Allergan) pode ser citado na página LATAM.']))

PAGINAS.append(base('pagina-ventas-corta', 'Página de ventas corta - eBook de Ojeras',
    DOC.format('1Vbpklmy46mTIQizp5eSsf1OKcVFQXA0dLnXFTY3-U-w'), IDV_EBOOK + ' (versão ES)', [
    dict(HERO_CLASSICO, midia=[{'tipo': 'mockup', 'descricao': 'Mockup abaixo com a capa ES do ebook Relleno Tridimensional de Ojeras (versão ES da pasta 2. ARTES). Capa real da edição ES, nunca gerada por IA.'}]),
    MODULOS_SEC, PASSOS,
    dict(BONUS, midia=[{'tipo': 'referencia', 'descricao': 'Exemplo de cards de bônus com casos clínicos: usar a versão ES da pasta 2. ARTES'}]),
    dict(OFERTA_EBOOK, midia=[{'tipo': 'referencia', 'descricao': 'Exemplo visual do bloco de preço, sem contagem regressiva: usar a versão ES da pasta 2. ARTES'}]),
    MENTOR_CLASSICO, FAQ_CLASSICO, contato(f'la compra del e-book {EBOOK}'), FOOTER],
    PEND_EBOOK + [WPP, CASO + ' (3 bônus).']))

ACESSO_LISTA = ['Libro digital completo con acceso de por vida', 'Metodología ARTI aplicada al relleno de ojeras', 'Técnica tridimensional paso a paso',
                'Razonamiento clínico estructurado', 'Revisión científica con artículos para descargar', 'Casos clínicos comentados', 'Videoclases explicativas',
                'Orientación clara sobre plano y ejecución']


def ancora(i):
    return {'id': f'oferta{"" if i == 1 else "-2"}', 'nome': 'Ancoragem de preço + compra', 'tipo': 'offer', 'titulo': 'Esto es todo a lo que tendrá acceso:',
            'lista': ACESSO_LISTA, 'preco_de': PRECO_DE, 'prefixo_preco': 'Por', 'preco': PRECO, 'desconto': DESCONTO, 'condicao': CONDICAO,
            'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': CHECKOUT},
            'nota_designer': NOTA_PRECO + ' "Videoclases" só se as aulas ES estiverem prontas.'}


PAGINAS.append(base('pagina-ventas-nueva', '[NUEVA] Página de ventas - eBook de Ojeras',
    DOC.format('1pB0_8kKRS-VI3xZ8kOCDhcEoBqdJzvTJ5MvfYLruCJc'), IDV_EBOOK + ' (versão ES; evitar a combinação verde e amarelo de camisa de futebol)', [
    {'id': 'hero', 'nome': 'Bloco 1: vender sozinho', 'tipo': 'hero', 'eyebrow': '♾️ Acceso de por vida',
     'titulo': 'Evitar el relleno de ojeras por falta de previsibilidad está limitando su práctica clínica.',
     'texto': ['Reciba exactamente lo que necesita para trabajar con más seguridad en:'],
     'lista': ['Técnica de relleno de ojeras', 'Zonas de riesgo anatómicas', 'Plan para evitar el edema'],
     'subtitulo': 'Todo esto para entregar resultados naturales y seguros, con un razonamiento clínico que usted puede reproducir caso a caso.',
     'texto_extra': 'Incluso si hoy todavía tiene dudas sobre el plano correcto o sobre cómo evitar intercurrencias isquémicas.',
     'cta': {'texto': f'QUIERO DOMINAR LA TÉCNICA DE OJERAS POR SOLO {PRECO}', 'acao': CHECKOUT},
     'midia': [{'tipo': 'mockup', 'descricao': 'Mockup com a capa ES do ebook'}],
     'nota_designer': 'Seguir a estrutura da imagem de referência do copywriter (versão ES na pasta 2. ARTES) e o UX do JSON enviado no grupo do projeto; referência de leitura: bibliotecadecriativos.com.br. ' + NOTA_PRECO},
    {'id': 'depoimentos', 'nome': 'Bloco 2: depoimentos', 'tipo': 'testimonials',
     'midia': [{'tipo': 'prints', 'descricao': 'Depoimentos de alunos em print (versão ES da pasta 2. ARTES)'}],
     'nota_designer': NOTA_DEPO},
    {'id': 'dor', 'nome': 'Bloco 3: dor latente', 'tipo': 'list',
     'titulo': 'Usted ya estudió armonización facial, ya invirtió en cursos y, aun así, cuando aparece un paciente con ojeras, la indicación genera duda.',
     'texto': ['Porque sabe que la región infraorbitaria no perdona improvisación:'],
     'lista': ['¿En qué plano depositar el producto?', '¿Qué producto de relleno elegir para no provocar edema persistente o efecto Tyndall?', '¿Cómo reconocer a tiempo una intercurrencia isquémica?', '¿Cómo explicarle al paciente qué esperar del procedimiento?'],
     'texto_extra': 'Sin respuestas claras a estas preguntas, la seguridad que usted transmite en la evaluación se resiente, y el paciente lo percibe.',
     'midia': [{'tipo': 'imagem', 'descricao': 'Esquema anatômico da região infraorbitária com camadas e zonas de risco (versão ES da pasta 2. ARTES)'}],
     'nota_designer': 'Dor reescrita em registro técnico (plano, edema, Tyndall, intercorrência isquêmica). Sem foto de paciente insatisfeita.'},
    {'id': 'transicao', 'nome': 'Bloco 4: transição', 'tipo': 'text',
     'texto': ['Pocos profesionales logran un resultado natural, seguro y previsible en ojeras. Muchos evitan el procedimiento y otros lo ejecutan sin un criterio anatómico claro.', 'Mientras tanto, la demanda de pacientes que buscan tratar las ojeras sigue creciendo.']},
    {'id': 'passos', 'nome': 'Bloco 5: passo a passo', 'tipo': 'steps', 'titulo': 'Estos son los 4 pasos para que usted convierta el relleno de ojeras en su mayor diferencial dentro de la armonización facial:',
     'itens': [{'titulo': 'Paso 01', 'texto': 'Anatomía'}, {'titulo': 'Paso 02', 'texto': 'Reología'}, {'titulo': 'Paso 03', 'texto': 'Técnica'}, {'titulo': 'Paso 04', 'texto': 'Intercurrencias'}],
     'midia': [{'tipo': 'imagem', 'descricao': 'Bloco de copy da página atual sobre a metodologia ARTI (versão ES da pasta 2. ARTES)'}],
     'nota_designer': 'Didático e numerado, a partir do Figma do protocolo: https://www.figma.com/design/BKHNP6al3V5MhEDTnydQE5/FEP---PUBLIC?node-id=0-1 (preparar a versão ES do esquema).'},
    {'id': 'entregaveis', 'nome': 'Bloco 6: o que vai receber', 'tipo': 'list', 'titulo': f'Vea todo lo que va a recibir con el libro digital {EBOOK}.',
     'lista': ['Acceso inmediato y de por vida al libro digital Relleno Tridimensional de Ojeras', 'Revisión científica con artículos para descargar', 'Casos clínicos comentados y videoclases explicativas'],
     'midia': [{'tipo': 'imagem', 'descricao': 'Mockup visual dos entregáveis (versão ES da pasta 2. ARTES)'}]},
    {'id': 'para-quem', 'nome': 'Bloco 7: para quem é', 'tipo': 'list', 'titulo': 'El libro digital Relleno Tridimensional de Ojeras es para usted si:',
     'lista': ['Evita hacer relleno de ojeras por inseguridad técnica;', 'Quiere tener un diferencial real en la armonización facial;', 'Tiene dudas sobre el plano correcto y quiere prevenir el edema;', 'Siente que le falta criterio clínico para indicar y ejecutar.'],
     'texto_extra': 'Si usted quiere dominar el relleno tridimensional de ojeras con un razonamiento anatómico que pueda reproducir en cada caso, y ofrecer un procedimiento que pocos profesionales ejecutan con previsibilidad, el libro digital Relleno Tridimensional de Ojeras es para usted.',
     'nota_designer': 'Linguagem neutralizada para usted (público de médicos, dentistas e biomédicos de ambos os sexos).'},
    ancora(1),
    {'id': 'entrega', 'nome': 'Como recebe', 'tipo': 'features', 'titulo': 'Compre ahora y reciba su acceso por correo electrónico de inmediato.',
     'itens': [{'titulo': 'Revise su correo electrónico', 'texto': 'En cuanto finalice la compra, recibirá su acceso por correo electrónico.'},
               {'titulo': 'Acceso al producto', 'texto': 'Recibirá todos los entregables de inmediato.'},
               {'titulo': 'Todo listo', 'texto': 'Todo organizado para facilitar el aprendizaje y permitir una aplicación práctica inmediata.'}],
     'midia': [{'tipo': 'icones', 'descricao': 'Ícones dos 3 passos de acesso (e-mail, produto, pronto), versão ES da pasta 2. ARTES'}]},
    {'id': 'decisao', 'nome': 'Bloco 10: conversa séria', 'tipo': 'options', 'titulo': 'Ahora usted tiene dos opciones:',
     'itens': [{'titulo': 'Opción 1', 'texto': 'Seguir evitando el relleno de ojeras, o ejecutarlo sin un criterio anatómico claro y con mayor exposición a intercurrencias evitables.'},
               {'titulo': 'Opción 2', 'texto': 'Convertir el relleno de ojeras en su mayor diferencial dentro de la armonización facial y dominar una habilidad que pocos profesionales realmente poseen.'}],
     'texto_extra': f'Usted sabe cuál de las dos protege mejor a su paciente y a su práctica clínica. Haga clic en el botón de abajo y acceda ahora al libro digital {EBOOK}.',
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '#oferta'}},
    {'id': 'mentor', 'nome': 'Bloco 11: autoridade', 'tipo': 'authority', 'eyebrow': f'El creador del libro {EBOOK}.',
     'texto': ['Soy el Dr. João Pithon, médico, profesor e investigador.',
               'Después de recorrer 9 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 10.000 ml aplicados sin intercurrencias isquémicas.',
               'Ya he formado a más de 30.000 alumnos con estas técnicas. Mi metodología le permitirá ver una nueva forma de trabajar el relleno, con razonamiento anatómico y previsibilidad.',
               'Este e-book ya suma +30 mil copias vendidas.',
               'Ahora le entrego un método claro y estructurado para que deje la improvisación y aplique con precisión anatómica y previsibilidad desde sus próximas consultas.'],
     'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João'}], 'nota_designer': NOTA_AUTORIDADE},
    ancora(2),
    {'id': 'faq', 'nome': 'Bloco 13: FAQ', 'tipo': 'faq', 'titulo': 'Preguntas frecuentes',
     'itens': [{'titulo': '¿Cuál es la forma de pago?', 'texto': 'Puede pagar con tarjeta de crédito o débito, en pago único.'},
               {'titulo': '¿El pago es seguro?', 'texto': 'Sí, el pago es 100 % seguro: utilizamos Hotmart, una de las mayores plataformas de ventas digitales del mundo.'},
               {'titulo': '¿Me sirve a mí?', 'texto': f'Sí. El libro digital {EBOOK} está dirigido a profesionales habilitados que realizan procedimientos inyectables, desde quienes están empezando hasta los más experimentados.'},
               {'titulo': '¿Cómo voy a acceder al libro?', 'texto': 'En cuanto se confirme su pago, le enviaremos un correo electrónico con los datos de acceso al producto y a todos los bonos.'},
               {'titulo': '¿Por cuánto tiempo tengo acceso?', 'texto': f'Tendrá acceso de por vida al libro digital {EBOOK}.'}],
     'midia': [{'tipo': 'selo', 'descricao': 'Selo de garantia de 7 dias e logo Hotmart (versão ES da pasta 2. ARTES)'}],
     'nota_designer': 'Pagamento: cartão de crédito ou débito via Hotmart (meio de pagamento instantâneo brasileiro removido).'},
    FOOTER],
    PEND_EBOOK + ['Depoimentos: prints em PT com legenda ES "Testimonio original en portugués".', 'Versão ES do esquema do Figma do protocolo (bloco 5).',
                  'Imagens de referência do copywriter: versão ES na pasta 2. ARTES.',
                  'Os "insights para o copy" do doc PT (ruminações, pior cenário, hooks) ficaram fora da página: são material de apoio da copy, não blocos.']))

PAGINAS.append(base('pagina-upsell-cpx', 'Página de Upsell - CPX',
    DOC.format('1POTRhQRTJOpUOrjYIYMjsdLt1A2h0eCQDltpAyDbb3A'), 'Identidade do CPX: https://joaopithon.com.br/cpx/', [
    {'id': 'tarja', 'nome': 'Tarja vermelha', 'tipo': 'alert_bar', 'texto': ['Atención, no cierre ni actualice esta página.']},
    {'id': 'progresso', 'nome': 'Barra de progresso', 'tipo': 'progress_bar', 'texto': ['Procesando su compra'], 'valor': 90,
     'nota_designer': 'Decisão da gestão pendente: a barra "Procesando su compra 90 %" simula um status que não existe. Alternativa recomendada: «Su compra del e-book fue confirmada. Antes de cerrar esta página, vea esta oportunidad complementaria.»'},
    {'id': 'video', 'nome': 'Vídeo', 'tipo': 'video', 'titulo': 'Tengo una oportunidad todavía mejor para usted.', 'subtitulo': 'Vea el video a continuación para conocerla:',
     'midia': [{'tipo': 'video', 'descricao': 'Vídeo de vendas do CPX (o mesmo da página de vendas). Confirmar versão em espanhol.'}]},
    {'id': 'oferta', 'nome': 'Bônus + compra', 'tipo': 'offer', 'eyebrow': 'Bono exclusivo:', 'titulo': 'Relleno Full Face guiado por ultrasonido en vivo',
     'prefixo_preco': 'Por', 'preco': PRECO_UPSELL,
     'cta': {'texto': 'COMPRAR AHORA', 'acao': CHECKOUT_UPSELL}, 'selos': SELOS,
     'midia': [{'tipo': 'imagem', 'descricao': 'Arte do bônus Relleno Full Face guiado por ultrasonido en vivo (versão ES da pasta 2. ARTES)'}],
     'nota_designer': 'Preço do upsell definido pela gestão em 20/10/2026: US$97 à vista, sem parcelas e sem preço "de".'},
    contato(f'la inscripción en el {NOME_UPSELL}'), FOOTER],
    [NOME_UPSELL, WPP, CHECKOUT_UPSELL,
     'Confirmar se o upsell CPX entra no funil LATAM e se o vídeo de vendas do CPX terá versão em espanhol.',
     'Decisão da gestão sobre a barra "Procesando su compra 90 %" (alternativa sugerida na nota do bloco).'],
    produto=f'CPX, {NOME_UPSELL} (upsell do Ebook Ojeras)'))

PAGINAS.append(base('copy-pagina-ebook', 'Copy Página eBook Ojeras (headlines + blocos)',
    DOC.format('1_Af60zj_W4Cld_q9JDKi9-ispKT2HUTLqxtw43wHEqg'), IDV_EBOOK + ' (versão ES)', [
    {'id': 'hero', 'nome': 'Hero com 3 variações de headline', 'tipo': 'headline_variants',
     'itens': [{'titulo': 'Headline 1', 'texto': 'Convierta el relleno de ojeras en su mayor diferencial dentro de la armonización facial al dominar una habilidad que pocos profesionales realmente poseen.'},
               {'titulo': 'Headline 2', 'texto': 'Domine el relleno de ojeras con seguridad y convierta una de las técnicas más temidas de la armonización facial en su mayor diferencial profesional.'},
               {'titulo': 'Headline 3', 'texto': 'Convierta el relleno de ojeras en su principal diferencial al dominar la técnica tridimensional y actuar con mayor previsibilidad.'}],
     'subtitulo': 'Un método claro y estructurado para que usted deje atrás la improvisación y aplique con precisión anatómica y previsibilidad desde sus próximas consultas.',
     'cta': {'texto': f'QUIERO DOMINAR LA TÉCNICA TRIDIMENSIONAL POR SOLO {PRECO}', 'acao': CHECKOUT},
     'apos_cta': [f'De {PRECO_DE}', f'Por {PRECO} ({DESCONTO}). {CONDICAO}'],
     'nota_designer': 'Headline 1 ativa no HTML; as outras ficam como variação para teste A/B. Abaixo do botão: preço "de" riscado e preço "por". ' + NOTA_PRECO},
    {'id': 'verdade', 'nome': 'Bloco 2', 'tipo': 'text', 'eyebrow': 'LA VERDAD DE LA QUE POCOS HABLAN',
     'texto': ['El relleno de ojeras exige técnica, y se vuelve impredecible para quien no tiene un razonamiento clínico estructurado.', 'Es precisamente esa imprevisibilidad la que genera:'],
     'lista': ['Miedo al edema', 'Inseguridad sobre el plano correcto', 'Dudas en el diagnóstico', 'Resultados inconsistentes', 'Falta de confianza para indicar y ejecutar'],
     'texto_extra': 'Por eso, muchos profesionales evitan tratar ojeras, y pocos realmente dominan el procedimiento.'},
    {'id': 'arti', 'nome': 'Bloco 3: metodologia ARTI', 'tipo': 'text', 'eyebrow': 'LA METODOLOGÍA ARTI',
     'texto': ['En este material, usted aplica la metodología ARTI, un paso a paso estructurado para convertir el relleno de ojeras en un diferencial real en su práctica clínica.',
               'Un contenido pionero en el que describimos, por primera vez, un razonamiento distinto del que practica la mayoría de los profesionales en el mundo.',
               'Nuestro protocolo se basa en el uso estratégico de productos de relleno con:'],
     'lista': ['Alto G’', 'Menor higroscopicidad (menor atracción de agua)', 'Partículas más grandes y más estables', 'Conexiones más estables entre las cadenas de ácido hialurónico'],
     'midia': [{'tipo': 'imagem', 'descricao': 'Esquema da metodologia ARTI: Anatomía, Reología, Técnica e Intercurrencias (versão ES da pasta 2. ARTES)'}],
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '#oferta'}},
    {'id': 'diferencial', 'nome': 'Bloco 4', 'tipo': 'text', 'eyebrow': 'EL DIFERENCIAL',
     'texto': ['La mayoría de los profesionales evita tratar ojeras y pocos realmente dominan el procedimiento. Por eso, quien lo ejecuta con previsibilidad se diferencia.'],
     'lista': ['Mayor precisión técnica', 'Mayor previsibilidad de resultado', 'Reducción significativa del edema', 'Resultados naturales y consistentes']},
    {'id': 'anatomia', 'nome': 'Bloco 5', 'tipo': 'text',
     'texto': ['Asociado a esto, realizamos una revisión anatómica profunda de la región, basada en estudios con cadáveres frescos, que permitió identificar:'],
     'lista': ['La capa ideal de aplicación', 'Una técnica tridimensional más precisa', 'Variación estratégica entre 3 y 4 puntos de entrada', 'Mayor control del plano y de la distribución']},
    {'id': 'industria', 'nome': 'Bloco 6', 'tipo': 'text',
     'texto': ['Este enfoque viene despertando el interés incluso de la industria de productos de relleno, que ya inició revisiones reológicas para aumentar la precisión de las indicaciones clínicas de sus materiales.'],
     'cta': {'texto': 'QUIERO CONVERTIR LAS OJERAS EN MI DIFERENCIAL', 'acao': '#oferta'},
     'nota_designer': 'Citação da fabricante removida (linha vermelha FEA: marca só com aprovação). Confirmar com o Dr. João se a afirmação pode ir ao ar sem fonte.'},
    {'id': 'aplicacao', 'nome': 'Bloco 7', 'tipo': 'text', 'eyebrow': 'RESULTADO PRÁCTICO Y APLICACIÓN INMEDIATA',
     'texto': ['Este no es un material teórico y extenso. Es un contenido clínico, directo y aplicable, para que usted aplique el razonamiento desde sus próximas consultas.']},
    {'id': 'para-quem', 'nome': 'Bloco 8', 'tipo': 'list', 'eyebrow': 'PARA QUIÉN ES', 'titulo': 'Este material es para profesionales que:',
     'lista': ['Evitan realizar relleno de ojeras por inseguridad', 'Ya lo realizan, pero sin previsibilidad clínica', 'Quieren reducir el riesgo y mejorar el control técnico', 'Buscan más seguridad y confianza en la ejecución', 'Quieren un diferencial real en la armonización facial']},
    {'id': 'oferta', 'nome': 'Bloco 9', 'tipo': 'offer', 'eyebrow': 'LO QUE USTED VA A RECIBIR',
     'lista': ACESSO_LISTA[1:], 'texto_ancora': 'Todo organizado para facilitar el aprendizaje y permitir una aplicación práctica inmediata.',
     'preco_de': PRECO_DE, 'preco': PRECO, 'prefixo_preco': 'Por', 'desconto': DESCONTO, 'condicao': CONDICAO,
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': CHECKOUT},
     'midia': [{'tipo': 'imagem', 'descricao': 'Mockup dos entregáveis: e-book, artigos, videoaulas (versão ES da pasta 2. ARTES)'}],
     'nota_designer': 'Trocar o texto do botão anterior por este. ' + NOTA_PRECO},
    {'id': 'depoimentos', 'nome': 'Bloco 10', 'tipo': 'testimonials', 'midia': [{'tipo': 'prints', 'descricao': 'Carrossel de depoimentos, removendo os indicados no vídeo enviado ao designer'}],
     'nota_designer': NOTA_DEPO},
    {'id': 'mentor', 'nome': 'Bloco 11: autoridade', 'tipo': 'authority', 'titulo': 'João Pithon, su mentor',
     'texto': ['Soy el Dr. João Pithon, médico, profesor e investigador.',
               'Después de recorrer 9 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 10.000 ml aplicados sin intercurrencias isquémicas.',
               'Ya he formado a más de 30.000 alumnos con estas técnicas. Mi metodología le permitirá descubrir una nueva forma de trabajar el relleno, con razonamiento anatómico y previsibilidad.',
               'Este e-book ya suma +30 mil copias vendidas.',
               'En 2019, decidí dedicarme a los procedimientos mínimamente invasivos en la medicina estética, con un foco claro: la anatomía como base de la seguridad. Desde entonces, estudio la región facial en cadáveres frescos para entender, capa por capa, dónde están las zonas de riesgo y cómo evitarlas.',
               'Es ese mismo razonamiento clínico el que comparto en este material, para que usted aplique la técnica con criterio, consistencia y previsibilidad en su práctica clínica.'],
     'cta': {'texto': 'QUIERO DOMINAR LA TÉCNICA TRIDIMENSIONAL', 'acao': '#oferta'},
     'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João'}], 'nota_designer': NOTA_AUTORIDADE},
    {'id': 'manter', 'nome': 'Bloco 12', 'tipo': 'placeholder', 'midia': [{'tipo': 'bloco', 'descricao': 'MANTER o bloco final da página atual (garantia e rodapé), versão ES da pasta 2. ARTES'}],
     'nota_designer': 'No original PT este era um segundo "Bloco 11" (numeração duplicada).'},
    FOOTER],
    PEND_EBOOK + ['Bloco 6: confirmar com o Dr. João se a afirmação sobre a revisão reológica da indústria pode ir ao ar sem fonte.',
                  'Depoimentos: prints em PT com legenda ES "Testimonio original en portugués".']))
