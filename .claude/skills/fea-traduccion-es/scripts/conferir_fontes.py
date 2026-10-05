# -*- coding: utf-8 -*-
"""Caca fonte de recurso no PDF pronto. Roda SEMPRE antes de entregar.

Por que existe: a fusao dos subconjuntos embutidos devolve os glifos que o
PORTUGUES usou. Se o espanhol precisa de uma letra que o portugues nunca
escreveu naquele corte, ela nao esta la — e o motor cai numa fonte de recurso
(Noto Serif, Droid, Fallback...) SEM AVISAR NADA.

No ebook de olheiras isso deixou tres letras serifadas no meio de palavras em
negrito — 'Piel y tejido', 'Almohadillas' — porque a Helvetica Neue Bold nao
tinha 'h', 'j' nem 'y'. Passou por toda a auditoria: o texto extraido esta
certo, a terminologia esta certa, so o DESENHO da letra esta errado.

Conferir a cobertura ANTES de compor nao resolve: o mapa de blocos nao diz
qual corte cada bloco usa, e o cmap mente (declara codepoint com contorno
vazio). Por isso a conferencia e aqui, no arquivo pronto, onde nao ha duvida.

Quando acusar: descubra o corte que faltou, doe o glifo da Medium ou da
Regular da mesma familia com doar_glifos.py (--engrossar = diferenca de haste
entre os dois cortes, medida no 'l', em 1000/em) e recomponha.

Excecao: se o glifo de recurso ficou no fluxo mas esta COBERTO por mascara e
redesenhado certo por cima (acontece quando o texto vive dentro de um Form
XObject com o paragrafo inteiro, e reescrever o XObject sairia mais caro que
o defeito), registre a excecao num JSON e passe em --ignorar. Cada excecao
exige motivo escrito. Sem o arquivo, qualquer fonte de recurso reprova.

Uso:
    python3 conferir_fontes.py saida.pdf [--esperadas Helvetica,Playfair,Guardian]
                                         [--ignorar excecoes.json]
"""
import sys, json, argparse
import pymupdf

# o que qualquer motor usa quando nao acha o glifo
RECURSO = ('noto', 'droid', 'dejavu', 'liberation', 'freeserif', 'freesans',
           'fallback', 'unifont', 'arialmt', 'timesnewroman')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--ignorar', default='',
                    help='JSON com as excecoes ja conferidas a olho')
    ap.add_argument('--esperadas', default='',
                    help='familias do projeto, separadas por virgula; '
                         'qualquer fonte fora da lista tambem e acusada')
    a = ap.parse_args()

    esperadas = [e.strip().lower() for e in a.esperadas.split(',') if e.strip()]
    perdoados = set()
    if a.ignorar:
        for e in json.load(open(a.ignorar))['excecoes']:
            if not e.get('motivo'):
                sys.exit('excecao sem motivo escrito: %r' % e)
            perdoados.add((e['pagina'], e['texto']))
    doc = pymupdf.open(a.pdf)
    achados = []

    for i in range(doc.page_count):
        for b in doc[i].get_text('dict')['blocks']:
            if b['type']:
                continue
            for l in b['lines']:
                linha = ''.join(s['text'] for s in l['spans'])
                for s in l['spans']:
                    if not s['text'].strip():
                        continue
                    f = s['font'].split('+')[-1].lower()
                    suspeita = any(r in f for r in RECURSO) or (
                        esperadas and not any(e in f for e in esperadas))
                    if suspeita and (i + 1, s['text']) not in perdoados:
                        achados.append({
                            'pagina': i + 1, 'fonte': s['font'],
                            'texto': s['text'], 'corpo': round(s['size'], 1),
                            'na_linha': linha.strip()[:80],
                        })

    print(json.dumps({'paginas': doc.page_count,
                      'excecoes_aceitas': len(perdoados),
                      'spans_suspeitos': len(achados),
                      'achados': achados}, ensure_ascii=False, indent=1))
    if achados:
        print('\nFONTE DE RECURSO NO ARQUIVO — nao entregue assim.', file=sys.stderr)
        for x in achados:
            print('  p%-3d %-22s %r  em %r' % (x['pagina'], x['fonte'],
                                               x['texto'], x['na_linha']),
                  file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
