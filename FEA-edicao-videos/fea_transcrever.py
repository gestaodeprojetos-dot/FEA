import sys, json
from faster_whisper import WhisperModel
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', download_root='models', cpu_threads=4)
prompt = "Harmonização orofacial, preenchimento com ácido hialurônico, full face, olheiras, bigode chinês, têmporas, pertuito labial, comissura, pré-jowl, sulco nasolabial, SANEP, anestesia, mentoniano, bolus, retroinjeção, cânula, agulha, mL."
for w in sys.argv[1:]:
    segs, info = m.transcribe(w, language='pt', word_timestamps=True, initial_prompt=prompt, vad_filter=False)
    out = []
    for s in segs:
        out.append({'start': s.start, 'end': s.end, 'text': s.text, 'words': [{'s': x.start, 'e': x.end, 'w': x.word} for x in s.words]})
    name = w.split('/')[-1].replace('.wav', '')
    json.dump(out, open(f'tr/{name}.json', 'w'), ensure_ascii=False, indent=1)
    print(name, 'done', flush=True)
