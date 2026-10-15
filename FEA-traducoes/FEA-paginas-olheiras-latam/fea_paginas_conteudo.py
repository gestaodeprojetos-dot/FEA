# Conteúdo das páginas ES do Ebook Olheiras LATAM, fiel às copys da pasta
# https://drive.google.com/drive/folders/15RFlmEyX_sWqlCHJuL8ZPEo-YA0m8TgB
# Copy em espanhol (es-419, usted). Notas para o designer em português.
# Preço: formato LATAM em dólar (US$19,00, como nos criativos IFF5 LATAM); valor pendente.

PRECO = 'US$ [PRECIO]'
PRECO_DE = 'US$ [PRECIO ANTERIOR]'
WPP = '[WHATSAPP ES: CONFIRMAR]'
NOTA_PRECO = 'Preço em dólar no formato dos criativos LATAM (US$19,00). Valor do ebook ainda não definido pela gestão: trocar [PRECIO] e [PRECIO ANTERIOR] quando vier.'
EBOOK = 'Relleno Tridimensional de Ojeras: Una Guía Completa con la Metodología ARTI'
IDV_EBOOK = 'https://drive.google.com/file/d/1W2gI1BCdKl7BT55sMsUSsRj9Zh0xFj8f/view'
FOOTER = {'id': 'rodape', 'nome': 'Rodapé', 'tipo': 'footer', 'texto': ['Formação Especialista Academy · © 2026 · Todos los derechos reservados']}


def contato(produto):
    return {'id': 'duvidas', 'nome': 'Dúvidas', 'tipo': 'contact', 'titulo': '¿LE QUEDÓ ALGUNA DUDA?',
            'texto': [f'Si le quedó cualquier duda sobre la compra del {produto}, hable con mi equipo por WhatsApp.'],
            'cta': {'texto': '¡Quiero hablar con el equipo!', 'acao': WPP},
            'nota_designer': 'Botão abre o WhatsApp de atendimento em espanhol (número pendente).'}


MODULOS = [
    ('Introducción al Razonamiento Clínico para el Relleno de Ojeras', [
        'Comprenda cómo el proceso de envejecimiento impacta la región periorbitaria.',
        'Refuerce su base anatómica para diagnosticar correctamente cada caso.',
        'Aprenda a identificar la estructura ósea, los compartimentos de grasa y los ligamentos.']),
    ('Anatomía de la Región Infraorbitaria', [
        'Profundice en los detalles anatómicos más relevantes del área más delicada del rostro.',
        'Descubra cómo cada estructura influye en la elección del producto y de la técnica.']),
    ('Reología: La Elección del Producto de Relleno Ideal', [
        'Domine el concepto de Swelling Factor (SF) y su influencia en el resultado final.',
        'Aprenda a seleccionar los productos más adecuados para ojeras, evitando complicaciones.']),
    ('Técnica Avanzada de Relleno Tridimensional', [
        'Acceda al paso a paso detallado de la técnica ARTI.',
        'Aprenda a analizar y marcar los ligamentos con precisión.',
        'Descubra los puntos de acceso correctos (puntos de entrada).',
        'Domine la técnica de Layering (capas) para resultados naturales y duraderos.']),
    ('Intercurrencias y Manejo de Complicaciones', [
        'Técnicas de prevención del edema persistente.',
        'Cómo evitar y tratar el efecto Tyndall.',
        'Corrección de irregularidades de relieve.',
        'Manejo seguro de hematomas.',
        'Cuidados posprocedimiento que garantizan la satisfacción y la seguridad del paciente.']),
]

HERO_CLASSICO = {
    'id': 'hero', 'nome': 'Hero', 'tipo': 'hero',
    'titulo': 'Domine el procedimiento más desafiante de la armonización facial, el relleno de ojeras, con la metodología ARTI, y alcance resultados naturales, seguros y duraderos.',
    'texto': ['Esta guía revela cómo aplicar la metodología ARTI (Anatomía, Reología, Técnica e Intercurrencias) en el relleno de ojeras, la región más delicada del rostro, logrando resultados superiores donde la mayoría falla.'],
    'cta': {'texto': '¡Quiero dominar la técnica tridimensional!', 'acao': '#oferta'},
}

PASSOS = {'id': 'passos', 'nome': 'Oferta: 4 passos', 'tipo': 'steps', 'titulo': 'Domine el relleno tridimensional de ojeras en 4 pasos:',
          'itens': [{'titulo': 'Paso 01', 'texto': 'Anatomía detallada de la región infraorbitaria'},
                    {'titulo': 'Paso 02', 'texto': 'Reología y elección del producto de relleno ideal'},
                    {'titulo': 'Paso 03', 'texto': 'Técnica avanzada de relleno tridimensional (paso a paso)'},
                    {'titulo': 'Paso 04', 'texto': 'Intercurrencias y manejo de complicaciones'}]}

BONUS = {'id': 'bonus', 'nome': 'Bônus', 'tipo': 'bonuses', 'titulo': '+03 Bonos Exclusivos',
         'itens': [{'titulo': f'Bono 0{i}', 'texto': f'Caso clínico {i}: [nombre del caso]'} for i in (1, 2, 3)],
         'nota_designer': 'Nome de cada caso clínico pendente na copy original (Adriane): manter o marcador até a copy definir.'}

OFERTA_47 = {'id': 'oferta', 'nome': 'Oferta especial', 'tipo': 'offer', 'titulo': 'Oferta Especial',
             'preco_de': PRECO_DE, 'preco': PRECO, 'prefixo_preco': 'Por solo', 'timer_min': 15,
             'cta': {'texto': 'Quiero mi e-book con descuento', 'acao': '[CHECKOUT HOTMART USD: CONFIRMAR]'},
             'selos': ['Hotmart', 'Garantía de 7 días'],
             'nota_designer': 'Cronômetro de 15 min (já funcionando no HTML). ' + NOTA_PRECO + ' No Brasil: de R$ 200,00 por R$ 47,00.'}

MENTOR_CLASSICO = {
    'id': 'mentor', 'nome': 'Autoridade', 'tipo': 'authority', 'titulo': '¡João Pithon, su mentor!',
    'texto': ['Soy el Dr. João Pithon, médico, coautor del libro Arquitetura Facial, coordinador de cursos y CEO del Instituto Pithon Napoli.',
              'Después de recorrer 7 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 7.000 ml aplicados sin intercurrencias.',
              'Ya he formado a más de 4.000 alumnos con estas técnicas. Mi metodología le permitirá ver una nueva forma de ofrecer resultados de excelencia en relleno.',
              'En 2019, tomé la decisión de trabajar con procedimientos mínimamente invasivos en la medicina estética. Esa elección transformó por completo mi vida.',
              'Seis años después, vivo una vida épica: con libertad financiera, experiencias únicas y la satisfacción de cuidar de mi familia como siempre lo soñé.',
              'La medicina estética es un campo próspero y transformador. Y yo le pregunto: ¿dónde quiere estar dentro de 6 años?'],
    'cta': {'texto': 'Quiero aprender con el Dr. João Pithon', 'acao': '#oferta'},
    'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João à direita'}],
    'nota_designer': 'Números de autoridade divergem entre as páginas (4.000, 20.000 e 30.000 alunos; 7, 8 e 9 países; 7.000 e 10.000 ml). Usar o dado que a gestão confirmar.'}

FAQ_CLASSICO = {'id': 'faq', 'nome': 'FAQ', 'tipo': 'faq', 'titulo': 'FAQ (Preguntas Frecuentes)',
                'itens': [{'titulo': '¿Cómo recibiré el e-book?', 'texto': 'Después de la compra, usted recibirá de inmediato el enlace para descargarlo en PDF.'},
                          {'titulo': '¿Tendré acceso de por vida?', 'texto': '¡Sí! El e-book es suyo para siempre.'},
                          {'titulo': '¿Hay garantía?', 'texto': 'Sí. Usted cuenta con 7 días de garantía incondicional. Si no queda satisfecho, le devolvemos su inversión.'},
                          {'titulo': '¿Necesito internet para acceder?', 'texto': 'Solo para descargarlo. Después, puede leerlo sin conexión en el celular, la tableta o la computadora.'}],
                'cta': {'texto': 'Quiero mi acceso ahora con Riesgo Cero', 'acao': '#oferta'}}

MODULOS_SEC = {'id': 'conteudo', 'nome': 'O que vai aprender', 'tipo': 'modules', 'titulo': 'Lo que usted aprenderá con este e-book',
               'texto': [f'El e-book {EBOOK} fue estructurado para brindarle claridad, seguridad y confianza en cada etapa del procedimiento.'],
               'itens': [{'titulo': t, 'lista': l} for t, l in MODULOS],
               'cta': {'texto': 'Quiero asegurar mi e-book ahora mismo', 'acao': '#oferta'},
               'nota_designer': 'Listas expansíveis (accordion), como sugere a copy.'}

TIMER_BAR = {'id': 'tarja', 'nome': 'Tarja vermelha com cronômetro', 'tipo': 'timer_bar', 'texto': ['Esta oferta termina en:'], 'timer_min': 15}


def base(slug, nome, fonte, identidade, secoes, pend, produto=f'Ebook {EBOOK}'):
    return {'pagina': nome, 'slug': slug, 'produto': produto, 'mercado': 'LATAM', 'idioma': 'es-419',
            'tratamento': 'usted', 'fonte_copy': fonte, 'identidade_visual': identidade,
            'paleta_padrao_html': {'roxo': '#5B4599', 'azul_violeta': '#3846BB', 'lavanda': '#D0D1E9', 'alerta': '#BB3838', 'fundo': '#F9F9F9', 'borda': '#E9E9E9'},
            'tipografia': {'titulos': 'Sora 600-800', 'corpo': 'Montserrat 400-500'},
            'pendencias': pend, 'secoes': secoes}


PEND_COMUM = [NOTA_PRECO, 'Link de checkout Hotmart em USD.', 'WhatsApp de atendimento em espanhol.']

PAGINAS = []

PAGINAS.append(base('pagina-ventas', 'Página de ventas - eBook de Ojeras',
    'https://docs.google.com/document/d/1WAS9MpUjb-GUFCIh_Zr2ObHEVcqd8niRktByx2W2_b0/edit', IDV_EBOOK, [
    TIMER_BAR,
    dict(HERO_CLASSICO, midia=[{'tipo': 'mockup', 'descricao': 'Mockup ao lado com a capa ES do ebook (e foto do Dr. João, se der para compor). Capa real da edição ES, nunca gerada por IA.'}]),
    {'id': 'depoimentos', 'nome': 'Depoimentos', 'tipo': 'testimonials', 'titulo': 'Lo que dicen sobre la Técnica Tridimensional de Relleno de Ojeras.',
     'midia': [{'tipo': 'prints', 'descricao': 'Mesmos depoimentos e prints da página de vendas da Imersão de Olheiras'}],
     'cta': {'texto': 'Quiero resultados como estos', 'acao': '#oferta'},
     'nota_designer': 'Sem depoimento em espanhol: print original em português com legenda ES "Testimonio original en portugués" (decisão da gestão em 05/10/2026). Conferir TCLE de fotos de paciente.'},
    {'id': 'dor', 'nome': 'Obstáculos', 'tipo': 'pain', 'titulo': '¿Qué le impide alcanzar la excelencia en el relleno de ojeras?',
     'contras': ['Inseguridad ante complicaciones como edema, irregularidades o efecto Tyndall.', 'Dudas sobre el producto ideal, la profundidad y el abordaje correcto.', 'Resultados mediocres, sin naturalidad ni durabilidad.'],
     'subtitulo': 'Imagine ahora…',
     'pros': ['Elegir productos con fundamento científico.', 'Dominar la anatomía y aplicar con precisión absoluta.', 'Usar una técnica tridimensional validada y segura.']},
    {'id': 'passo-a-passo', 'nome': 'Conteúdo do ebook', 'tipo': 'features', 'titulo': 'El paso a paso de la técnica tridimensional en sus manos', 'texto': ['En el e-book, usted tendrá acceso a:'],
     'itens': [{'titulo': 'Revisión anatómica y reológica', 'texto': 'comprenda a fondo el comportamiento de los productos de relleno.'},
               {'titulo': 'Técnica Tridimensional', 'texto': 'paso a paso completo.'},
               {'titulo': 'Comparación con otras técnicas', 'texto': 'MD Codes y demás abordajes clásicos.'},
               {'titulo': 'Complicaciones y soluciones', 'texto': 'cómo diagnosticarlas y tratarlas con seguridad.'}],
     'cta': {'texto': 'Quiero aprender la técnica tridimensional ahora', 'acao': '#oferta'}},
    {'id': 'acesso', 'nome': 'Acesso', 'tipo': 'list', 'titulo': 'Estudie a su ritmo, con acceso inmediato y de por vida',
     'lista': ['E-book digital en PDF entregado inmediatamente después de la compra.', 'Lectura sencilla y práctica en cualquier dispositivo.', 'Estudio flexible, en sus tiempos.', 'Material de consulta permanente, basado en ciencia y práctica clínica.'],
     'cta': {'texto': 'Quiero mi acceso inmediato al e-book', 'acao': '#oferta'}},
    {'id': 'para-quem', 'nome': 'Para quem é', 'tipo': 'pain', 'titulo': '¿Este e-book es para usted?',
     'pros': ['Para inyectores que buscan la excelencia en el relleno de ojeras.', 'Para quienes buscan seguridad, confianza y previsibilidad en los resultados.', 'Para quienes entienden que la diferenciación proviene del dominio científico sumado a una práctica refinada.'],
     'contras': ['No es para quienes buscan atajos sin estudiar.', 'No es para quienes no están dispuestos a aplicar el conocimiento adquirido.', 'No es para quienes creen que la armonización facial es solo «inyectar producto», sin ciencia ni técnica.'],
     'ordem': 'pros_primeiro', 'cta': {'texto': 'Sí, quiero ser un Inyector de Élite', 'acao': '#oferta'}},
    MODULOS_SEC, PASSOS, BONUS, OFERTA_47,
    {'id': 'custo', 'nome': 'Custo de não comprar', 'tipo': 'pain', 'titulo': 'Créalo: ¡no comprar le sale más caro!',
     'contras': ['Seguir sin dominar esta técnica significa permanecer vulnerable a complicaciones, inseguridad y resultados por debajo del promedio.', 'Significa perder pacientes frente a quienes ya dominan la metodología.'],
     'pros': ['Con este e-book, usted tendrá en sus manos una guía definitiva para convertirse en referencia en relleno de ojeras, con seguridad y previsibilidad.'],
     'cta': {'texto': 'No quiero quedarme atrás, quiero mi e-book ahora', 'acao': '#oferta'}},
    MENTOR_CLASSICO, FAQ_CLASSICO, contato(f'e-book {EBOOK}'), FOOTER], PEND_COMUM))

PAGINAS.append(base('pagina-ventas-corta', 'Página de ventas corta - eBook de Ojeras',
    'https://docs.google.com/document/d/1F9VOiWu9tZkOm8-F4WIoO9aMu4ouO-HFS1_v1p3x-tk/edit', IDV_EBOOK, [
    TIMER_BAR,
    dict(HERO_CLASSICO, midia=[{'tipo': 'mockup', 'descricao': 'Mockup abaixo com a capa ES do ebook. Capa real da edição ES, nunca gerada por IA.'}]),
    MODULOS_SEC, PASSOS, dict(BONUS, midia=[{'tipo': 'referencia', 'descricao': 'Seguir o exemplo visual do doc original em português'}]),
    OFERTA_47, MENTOR_CLASSICO, FAQ_CLASSICO, contato(f'e-book {EBOOK}'), FOOTER], PEND_COMUM))

ACESSO_LISTA = ['Libro digital completo con acceso de por vida', 'Metodología ARTI aplicada al relleno de ojeras', 'Técnica tridimensional paso a paso',
                'Razonamiento clínico estructurado', 'Revisión científica con artículos para descargar', 'Casos clínicos comentados', 'Videoclases explicativas',
                'Orientación clara sobre plano y ejecución']


def ancora(i):
    return {'id': f'oferta{"" if i == 1 else "-2"}', 'nome': 'Ancoragem de preço + compra', 'tipo': 'offer', 'titulo': 'Esto es todo a lo que tendrá acceso',
            'lista': ACESSO_LISTA, 'texto_ancora': 'Todo esto debería costar', 'preco_de': PRECO_DE, 'prefixo_preco': 'Pero hoy, usted accede por:', 'preco': PRECO,
            'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '[CHECKOUT HOTMART USD: CONFIRMAR]'},
            'nota_designer': NOTA_PRECO + ' No Brasil: de R$ 397,00 por 12 x R$ 10,03; confirmar se haverá parcelamento no LATAM. "Videoclases" só se as aulas ES estiverem prontas.'}


PAGINAS.append(base('pagina-ventas-nueva', '[NUEVA] Página de ventas - eBook de Ojeras',
    'https://docs.google.com/document/d/1c2iylqHqvLsE_J17v86vlbz7o80-SagRswZA9_42PX8/edit', IDV_EBOOK + ' (sem parecer Brasil na Copa)', [
    {'id': 'hero', 'nome': 'Bloco 1: vender sozinho', 'tipo': 'hero', 'eyebrow': '♾️ Acceso de por vida',
     'titulo': 'Evitar el relleno de ojeras le está haciendo perder pacientes, autoridad y dinero.',
     'texto': ['Reciba exactamente lo que necesita para tener más seguridad en:'],
     'lista': ['Técnicas de relleno de ojeras', 'Regiones anatómicas de riesgo', 'Plan para evitar el edema'],
     'subtitulo': 'Todo esto para entregar resultados más naturales, seguros y valorados por sus pacientes.',
     'texto_extra': 'Aunque hoy todavía tenga inseguridad o miedo a las intercurrencias.',
     'cta': {'texto': f'QUIERO DOMINAR LA TÉCNICA DE OJERAS POR SOLO {PRECO}', 'acao': '#oferta'},
     'midia': [{'tipo': 'mockup', 'descricao': 'Mockup com a capa ES do ebook'}],
     'nota_designer': 'UX segundo o JSON enviado no grupo; referência de leitura: bibliotecadecriativos.com.br. ' + NOTA_PRECO},
    {'id': 'depoimentos', 'nome': 'Bloco 2: depoimentos', 'tipo': 'testimonials',
     'midia': [{'tipo': 'prints', 'descricao': 'Depoimentos do doc original'}],
     'nota_designer': 'Print original em português com legenda ES "Testimonio original en portugués". Conferir TCLE.'},
    {'id': 'dor', 'nome': 'Bloco 3: dor latente', 'tipo': 'text', 'titulo': 'Lo sé… usted ya no soporta ver cómo su inseguridad le hace perder pacientes incluso antes de empezar…',
     'texto': ['Porque, en el fondo, usted siente:'],
     'citacoes': ['Yo quería transmitir confianza… pero ni yo confío en mí todavía.', 'Mientras yo tengo miedo… otras profesionales están creciendo.', 'Mi inseguridad me está haciendo perder dinero.', 'Si sigo así… voy a terminar abandonando el área.'],
     'texto_extra': 'Usted ya no soporta estudiar armonización facial, invertir en cursos y seguir sintiéndose insegura. Porque, en el fondo, sabe que no logra atraer pacientes justamente porque todavía no transmite confianza. ¿Me equivoco?',
     'midia': [{'tipo': 'foto', 'descricao': 'Paciente insatisfeita, como na página de referência (banco de imagem licenciado ou foto própria com autorização; nunca IA)'}]},
    {'id': 'transicao', 'nome': 'Bloco 4: transição', 'tipo': 'text',
     'texto': ['Porque la verdad es que casi nadie logra entregar un resultado realmente bonito, natural y seguro en ojeras.', 'La mayoría lo evita. Otras lo hacen mal. Y muchas ni siquiera tienen la seguridad para ofrecerlo.', 'Mientras tanto… la demanda no deja de crecer.']},
    {'id': 'passos', 'nome': 'Bloco 5: passo a passo', 'tipo': 'steps', 'titulo': 'Estos son los 4 pasos para que usted convierta el relleno de ojeras en su mayor diferencial dentro de la armonización facial:',
     'itens': [{'titulo': 'Paso 01', 'texto': 'Anatomía'}, {'titulo': 'Paso 02', 'texto': 'Reología'}, {'titulo': 'Paso 03', 'texto': 'Técnica'}, {'titulo': 'Paso 04', 'texto': 'Intercurrencias'}],
     'nota_designer': 'Didático e numerado, a partir do Figma do protocolo: https://www.figma.com/design/BKHNP6al3V5MhEDTnydQE5/FEP---PUBLIC?node-id=0-1 . Incluir o texto que já está na página atual (imagem no doc original).'},
    {'id': 'entregaveis', 'nome': 'Bloco 6: o que vai receber', 'tipo': 'list', 'titulo': f'Vea todo lo que va a recibir con el libro digital {EBOOK}',
     'lista': ['Acceso inmediato y de por vida al libro digital Relleno Tridimensional de Ojeras', 'Revisión científica con artículos para descargar', 'Casos clínicos comentados y videoclases explicativas'],
     'nota_designer': 'Visual como na referência do doc original.'},
    {'id': 'para-quem', 'nome': 'Bloco 7: para quem é', 'tipo': 'list', 'titulo': 'El libro digital Relleno Tridimensional de Ojeras es para usted que:',
     'lista': ['Evita hacer relleno de ojeras por inseguridad;', 'Quiere tener un diferencial real en la armonización facial;', 'Tiene miedo al edema e inseguridad sobre el plano correcto;', 'Siente que le falta confianza para indicar y ejecutar.'],
     'texto_extra': 'Si usted quiere dominar el relleno tridimensional de ojeras y destacarse en el mercado MUCHO más rápido. Dejar de ser “una inyectora más”… y convertirse en la profesional de élite que entrega un procedimiento que pocas logran ejecutar con confianza. ¡El libro digital Relleno Tridimensional de Ojeras es para usted!'},
    ancora(1),
    {'id': 'entrega', 'nome': 'Como recebe', 'tipo': 'features', 'titulo': '¡Compre ahora y reciba su libro en el correo electrónico de inmediato!',
     'itens': [{'titulo': 'Revise su correo electrónico', 'texto': 'En cuanto finalice la compra, recibirá su acceso por correo electrónico.'},
               {'titulo': 'Acceso al producto', 'texto': 'Recibirá todos los entregables de inmediato.'},
               {'titulo': '¡Todo listo!', 'texto': 'Todo organizado para facilitar el aprendizaje y permitir una aplicación práctica inmediata.'}]},
    {'id': 'decisao', 'nome': 'Bloco 10: conversa séria', 'tipo': 'options', 'titulo': 'Ahora usted tiene dos opciones:',
     'itens': [{'titulo': 'Opción 1', 'texto': 'Que la paciente salga insatisfecha y hable mal de usted con todo el mundo, y que usted tenga que abandonar el área porque no consigue pacientes.'},
               {'titulo': 'Opción 2', 'texto': 'Convertir el relleno de ojeras en su mayor diferencial dentro de la armonización facial y dominar una habilidad que pocos profesionales realmente poseen.'}],
     'texto_extra': f'Lo sé (y usted también lo sabe): la opción 2 es la más inteligente. Entonces haga clic en el botón de abajo y acceda ahora mismo al libro digital {EBOOK}.',
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '#oferta'}},
    {'id': 'mentor', 'nome': 'Bloco 11: autoridade', 'tipo': 'authority', 'eyebrow': f'El creador del libro {EBOOK}.',
     'texto': ['Soy el Dr. João Pithon, médico, profesor e investigador.',
               'Después de recorrer 9 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 10.000 ml aplicados sin intercurrencias isquémicas.',
               'Ya he formado a más de 30.000 alumnos con estas técnicas. Mi metodología le permitirá ver una nueva forma de ofrecer resultados de excelencia en relleno.',
               'Ahora le entrego un método simple y estructurado para que deje la improvisación y aplique con precisión anatómica y previsibilidad desde sus próximas consultas.'],
     'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João'}], 'nota_designer': MENTOR_CLASSICO['nota_designer']},
    ancora(2),
    {'id': 'faq', 'nome': 'Bloco 13: FAQ', 'tipo': 'faq', 'titulo': 'Preguntas frecuentes',
     'itens': [{'titulo': '¿Cuál es la forma de pago?', 'texto': 'Puede pagar con tarjeta de crédito. [CONFIRMAR MÉTODOS DE PAGO PARA LATAM]'},
               {'titulo': '¿El pago es seguro?', 'texto': 'Sí, el pago es 100% seguro: utilizamos una de las mayores plataformas de ventas del mundo, Hotmart.'},
               {'titulo': '¿Me sirve a mí?', 'texto': f'Sí, el libro digital {EBOOK} sirve para cualquier inyector, del principiante al avanzado.'},
               {'titulo': '¿Cómo voy a acceder al libro?', 'texto': 'En cuanto se confirme su pago, le enviaremos un correo electrónico con todos los datos de inicio de sesión para que acceda al producto junto con todos los bonos.'},
               {'titulo': '¿Por cuánto tiempo tengo acceso?', 'texto': f'Tendrá acceso de por vida al libro digital {EBOOK}.'}],
     'nota_designer': 'O original cita Pix, que não existe fora do Brasil: saiu até a gestão confirmar os meios de pagamento LATAM.'},
    FOOTER], PEND_COMUM + ['Os "insights para o copy" do doc (ruminações, hooks, eyebrows alternativos) ficaram fora da página: são material de apoio da copy, não blocos.']))

PAGINAS.append(base('pagina-upsell-cpx', 'Página de Upsell - CPX',
    'https://docs.google.com/document/d/1aSJo7XbjbAOpMuFhbrYG1a_5BKd6y5jxzyvhUjdApgg/edit', 'Identidade do CPX: https://joaopithon.com.br/cpx/', [
    {'id': 'tarja', 'nome': 'Tarja vermelha', 'tipo': 'alert_bar', 'texto': ['Atención, no cierre ni actualice esta página.']},
    {'id': 'progresso', 'nome': 'Barra de progresso', 'tipo': 'progress_bar', 'texto': ['Procesando su compra'], 'valor': 90},
    {'id': 'video', 'nome': 'Vídeo', 'tipo': 'video', 'titulo': 'Tengo una oportunidad todavía mejor para usted.', 'subtitulo': 'Vea el video a continuación para descubrirla:',
     'midia': [{'tipo': 'video', 'descricao': 'Vídeo de vendas do CPX (o mesmo da página de vendas). Versão ES traduzida no HeyGen, se houver.'}]},
    {'id': 'oferta', 'nome': 'Bônus + compra', 'tipo': 'offer', 'eyebrow': 'Bono exclusivo:', 'titulo': 'Relleno Full Face guiado por ultrasonido en vivo',
     'preco_de': PRECO_DE, 'prefixo_preco': 'Por', 'preco': PRECO,
     'cta': {'texto': 'COMPRAR AHORA', 'acao': '[CHECKOUT UPSELL USD: CONFIRMAR]'}, 'selos': ['Hotmart', 'Garantía de 7 días'],
     'midia': [{'tipo': 'imagem', 'descricao': 'Imagem do bônus (doc original)'}],
     'nota_designer': 'Preço do CPX em dólar pendente. No Brasil: de R$ 497 por 12 x R$ 30,72; confirmar se haverá parcelamento no LATAM.'},
    contato('Curso de Relleno Express [CONFIRMAR NOMBRE DEL PRODUCTO EN ESPAÑOL]'), FOOTER],
    ['Preço do CPX em dólar.', 'Link de checkout do upsell em USD.', 'Nome do produto em espanhol.', 'WhatsApp de atendimento em espanhol.'],
    produto='CPX, Curso de Relleno Express (upsell do Ebook Ojeras)'))

PAGINAS.append(base('copy-pagina-ebook', 'Copy Página eBook Ojeras (headlines + blocos)',
    'https://docs.google.com/document/d/1v-gq1sJjdatMomxQkThTJSERjOuFqiUAlBjroz7u0no/edit', IDV_EBOOK, [
    {'id': 'hero', 'nome': 'Hero com 3 variações de headline', 'tipo': 'headline_variants',
     'itens': [{'titulo': 'Headline 1', 'texto': 'Convierta el relleno de ojeras en su mayor diferencial dentro de la armonización facial al dominar una habilidad que pocos profesionales realmente poseen.'},
               {'titulo': 'Headline 2', 'texto': 'Domine el relleno de ojeras con seguridad y convierta una de las técnicas más temidas de la armonización facial en su mayor diferencial profesional.'},
               {'titulo': 'Headline 3', 'texto': 'Convierta el relleno de ojeras en su principal diferencial al dominar la técnica tridimensional y actuar con mayor previsibilidad.'}],
     'subtitulo': 'Un método simple y estructurado para que usted deje atrás la improvisación y aplique con precisión anatómica y previsibilidad desde sus próximas consultas.',
     'cta': {'texto': f'QUIERO DOMINAR LA TÉCNICA TRIDIMENSIONAL POR SOLO {PRECO}', 'acao': '#oferta'},
     'nota_designer': 'Headline 1 ativa no HTML; as outras ficam como variação para teste A/B. ' + NOTA_PRECO},
    {'id': 'verdade', 'nome': 'Bloco 2', 'tipo': 'text', 'eyebrow': 'LA VERDAD DE LA QUE POCOS HABLAN',
     'texto': ['El relleno de ojeras no es una técnica difícil.', 'Es impredecible para quien no tiene un razonamiento clínico estructurado.', 'Y es precisamente esa imprevisibilidad la que genera:'],
     'lista': ['Miedo al edema', 'Inseguridad sobre el plano correcto', 'Dudas en el diagnóstico', 'Resultados inconsistentes', 'Falta de confianza para indicar y ejecutar'],
     'texto_extra': 'Por eso, muchos profesionales evitan la ojera; y pocos realmente la dominan.'},
    {'id': 'arti', 'nome': 'Bloco 3: metodologia ARTI', 'tipo': 'text', 'eyebrow': 'LA METODOLOGÍA ARTI',
     'texto': ['En este material, usted aplica la metodología ARTI, un paso a paso estructurado para convertir el relleno de ojeras en un diferencial real en su práctica clínica.',
               'Un contenido pionero en el que describimos, por primera vez, un razonamiento distinto del que practica la mayoría de los profesionales en el mundo.',
               'Nuestro protocolo se basa en el uso estratégico de productos de relleno con:'],
     'lista': ['Alto G’', 'Menor higroscopicidad (menor atracción de agua)', 'Partículas más grandes y más estables', 'Conexiones más estables entre las cadenas de ácido hialurónico'],
     'midia': [{'tipo': 'imagem', 'descricao': 'Imagem da metodologia ARTI: Anatomía, Reología, Técnica e Intercurrencias (versão ES)'}],
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '#oferta'}},
    {'id': 'diferencial', 'nome': 'Bloco 4', 'tipo': 'text', 'eyebrow': 'EL DIFERENCIAL',
     'texto': ['La mayoría de los profesionales evita la ojera. Pocos realmente la dominan.', 'Y precisamente por eso, quien la ejecuta con previsibilidad se diferencia.'],
     'lista': ['Mayor precisión técnica', 'Mayor previsibilidad de resultado', 'Reducción significativa del edema', 'Resultados naturales y consistentes']},
    {'id': 'anatomia', 'nome': 'Bloco 5', 'tipo': 'text',
     'texto': ['Asociado a esto, realizamos una revisión anatómica profunda de la región, basada en estudios con cadáveres frescos, que permitió identificar:'],
     'lista': ['La capa ideal de aplicación', 'Una técnica tridimensional más precisa', 'Variación estratégica entre 3 y 4 puntos de entrada', 'Mayor control del plano y de la distribución']},
    {'id': 'industria', 'nome': 'Bloco 6', 'tipo': 'text',
     'texto': ['Este enfoque viene llamando la atención incluso de la industria de productos de relleno, como LG en Corea, que inició revisiones reológicas para aumentar la precisión de las indicaciones clínicas de sus materiales.'],
     'cta': {'texto': 'QUIERO CONVERTIR LA OJERA EN MI DIFERENCIAL', 'acao': '#oferta'},
     'nota_designer': 'Cita fabricante (LG). Regra FEA: marca só com aprovação; confirmar com a gestão antes de publicar.'},
    {'id': 'aplicacao', 'nome': 'Bloco 7', 'tipo': 'text', 'eyebrow': 'RESULTADO PRÁCTICO Y APLICACIÓN INMEDIATA',
     'texto': ['Este no es un material teórico y extenso.', 'Es un contenido clínico, directo y aplicable.', 'Usted puede aplicar el razonamiento desde sus próximas consultas.']},
    {'id': 'para-quem', 'nome': 'Bloco 8', 'tipo': 'list', 'eyebrow': 'PARA QUIÉN ES', 'titulo': 'Este material es para profesionales que:',
     'lista': ['Evitan realizar relleno de ojeras por inseguridad', 'Ya lo realizan, pero sin previsibilidad clínica', 'Quieren reducir el riesgo y mejorar el control técnico', 'Buscan más seguridad y confianza en la ejecución', 'Quieren un diferencial real en la armonización facial']},
    {'id': 'oferta', 'nome': 'Bloco 9', 'tipo': 'offer', 'eyebrow': 'LO QUE USTED VA A RECIBIR',
     'lista': ACESSO_LISTA[1:], 'texto_ancora': 'Todo organizado para facilitar el aprendizaje y permitir una aplicación práctica inmediata.',
     'preco': PRECO, 'prefixo_preco': 'Acceso de por vida por',
     'cta': {'texto': 'QUIERO CONVERTIRME EN REFERENTE EN OJERAS', 'acao': '[CHECKOUT HOTMART USD: CONFIRMAR]'},
     'midia': [{'tipo': 'imagem', 'descricao': 'Imagem do doc original (mockup dos entregáveis em ES)'}], 'nota_designer': NOTA_PRECO},
    {'id': 'depoimentos', 'nome': 'Bloco 10', 'tipo': 'testimonials', 'midia': [{'tipo': 'prints', 'descricao': 'Manter os depoimentos, removendo os indicados no vídeo enviado pela gestão'}],
     'nota_designer': 'Print original em português com legenda ES "Testimonio original en portugués". Conferir TCLE.'},
    {'id': 'mentor', 'nome': 'Bloco 11: autoridade', 'tipo': 'authority', 'titulo': '¡João Pithon, su mentor!',
     'texto': ['Soy el Dr. João Pithon, médico, profesor e investigador.',
               'Después de recorrer 8 países como investigador científico, le presentaré las técnicas refinadas de relleno que validé con más de 10.000 ml aplicados sin intercurrencias isquémicas.',
               'Ya he formado a más de 20.000 alumnos con estas técnicas. Mi metodología le permitirá descubrir una nueva forma de ofrecer resultados de excelencia en relleno.',
               'En 2019, tomé la decisión de trabajar con procedimientos mínimamente invasivos en la medicina estética. Esa elección transformó por completo mi vida.',
               'Seis años después, vivo una vida con libertad financiera, experiencias únicas y la satisfacción de cuidar de mi familia como siempre soñé.',
               'La armonización facial es un campo próspero y transformador. Y me pregunto: ¿dónde quiere estar usted dentro de 6 años?'],
     'cta': {'texto': 'QUIERO DOMINAR LA TÉCNICA TRIDIMENSIONAL', 'acao': '#oferta'},
     'midia': [{'tipo': 'foto', 'descricao': 'Foto do Dr. João'}], 'nota_designer': MENTOR_CLASSICO['nota_designer']},
    {'id': 'manter', 'nome': 'Bloco final', 'tipo': 'placeholder', 'midia': [{'tipo': 'bloco', 'descricao': 'MANTER o bloco atual da página (imagem no doc original)'}]},
    FOOTER], PEND_COMUM + ['Citação ao fabricante LG (bloco 6) precisa de aprovação.']))
