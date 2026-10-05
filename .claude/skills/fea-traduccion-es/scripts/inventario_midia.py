#!/usr/bin/env python3
"""
Inventário de mídia e QR Codes de um PDF — vídeos, artigos e destinos.

Uso:
    python3 inventario_midia.py material.pdf [--json]

Por que este script existe: nos materiais FEA os botões de vídeo são ARTE, não
anotação de link. O destino real está codificado dentro da imagem do QR Code.
Sem decodificar, o inventário de mídia é impossível de levantar — e todo vídeo
que precisa de versão espanhola passa despercebido.

Saída: página, tipo de destino, URL, e marcador de tempo quando houver.
Classificar Drive em vídeo ou artigo exige os metadados do Drive (mimeType);
o script sinaliza quais IDs consultar.
"""
import sys, json, re
try:
    import pymupdf, cv2, numpy as np
except ImportError:
    sys.exit('requer: pip install pymupdf opencv-python-headless')

def inventaria(caminho):
    doc = pymupdf.open(caminho)
    det = cv2.QRCodeDetector()
    achados = []

    # 1) anotações de link (quando existirem)
    for i, p in enumerate(doc):
        for l in p.get_links():
            uri = l.get('uri') or ''
            if uri:
                achados.append(dict(pagina=i+1, origem='anotacao', uri=uri))

    # 2) QR Codes — o caminho que realmente funciona nestes materiais
    for i, p in enumerate(doc):
        for dpi in (300, 450):          # 300 resolve a maioria; 450 pega QR pequeno
            pix = p.get_pixmap(dpi=dpi)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            img = cv2.cvtColor(img, {1: cv2.COLOR_GRAY2BGR, 3: cv2.COLOR_RGB2BGR,
                                     4: cv2.COLOR_RGBA2BGR}[pix.n])
            ok, infos, _, _ = det.detectAndDecodeMulti(img)
            if ok:
                novos = [t for t in infos if t.strip()]
                if novos:
                    for t in novos:
                        if not any(a['uri'] == t and a['pagina'] == i+1 for a in achados):
                            achados.append(dict(pagina=i+1, origem='qr', uri=t))
                    break

    for a in achados:
        u = a['uri']
        if 'youtube.com' in u or 'youtu.be' in u:
            a['tipo'] = 'video_youtube'; a['traduzir'] = True
        elif 'drive.google.com' in u:
            a['tipo'] = 'drive_a_classificar'; a['traduzir'] = None
            m = re.search(r'/d/([\w-]+)', u)
            a['drive_id'] = m.group(1) if m else None
        else:
            a['tipo'] = 'outro'; a['traduzir'] = None
        m = re.search(r'[?&]t=(\d+)', u)
        if m: a['timestamp_s'] = int(m.group(1))
    return achados

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    ach = inventaria(sys.argv[1])
    if '--json' in sys.argv:
        print(json.dumps(ach, ensure_ascii=False, indent=1)); return

    yt  = [a for a in ach if a['tipo'] == 'video_youtube']
    dr  = [a for a in ach if a['tipo'] == 'drive_a_classificar']
    ts  = [a for a in ach if 'timestamp_s' in a]
    unicos = {a['uri'] for a in ach}

    print('INVENTÁRIO DE MÍDIA — %s\n' % sys.argv[1])
    print('  %d destinos, %d únicos' % (len(ach), len(unicos)))
    print('  %d YouTube (traduzir)' % len(yt))
    print('  %d Google Drive (classificar vídeo vs artigo pelos metadados)' % len(dr))
    print('  %d com marcador de tempo ?t= — RECALCULAR na versão ES\n' % len(ts))

    for a in sorted(ach, key=lambda x: (x['pagina'], x['uri'])):
        t = ' [t=%ds ← recalcular]' % a['timestamp_s'] if 'timestamp_s' in a else ''
        print('  P%-3d %-22s %s%s' % (a['pagina'], a['tipo'], a['uri'][:70], t))

    if dr:
        print('\nIDs do Drive a classificar por mimeType:')
        for i in sorted({a.get('drive_id') for a in dr if a.get('drive_id')}):
            print('   ', i)

    # reaproveitamento: mesmo destino em mais de uma página
    from collections import defaultdict
    onde = defaultdict(set)
    for a in ach: onde[a['uri']].add(a['pagina'])
    rep = {u: p for u, p in onde.items() if len(p) > 1}
    if rep:
        print('\nREAPROVEITAMENTO — 1 ativo atende vários QR:')
        for u, p in rep.items():
            print('    páginas %s → %s' % (sorted(p), u[:60]))
        print('  Atenção: nº de ativos a produzir ≠ nº de QR a regerar.')

if __name__ == '__main__': main()
