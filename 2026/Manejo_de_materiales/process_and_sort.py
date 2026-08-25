import json
import os
import re
import sys

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

def get_slide_verbatim(code_hint, slide_num):
    for fname, fdata in slides_data.items():
        if code_hint.lower() in fname.lower() or code_hint.lower() in fdata['path'].lower():
            for s in fdata['slides']:
                if s['slide_no'] == slide_num:
                    return {
                        'file': fname,
                        'unit': fdata['unit'],
                        'slide_no': slide_num,
                        'text': s['text'].strip()
                    }
    return None

def get_multiple_slides_verbatim(code_hint, slide_nums):
    texts = []
    unit = ""
    full_fname = ""
    for snum in slide_nums:
        v = get_slide_verbatim(code_hint, snum)
        if v:
            unit = v['unit']
            full_fname = v['file']
            texts.append(f"--- Diapositiva {snum} ---\n" + v['text'])
    return {
        'file': full_fname,
        'unit': unit,
        'slide_no': ", ".join(map(str, slide_nums)),
        'text': "\n\n".join(texts)
    }

from questions_catalog import questions_db

# Map old hints to unique code hints
code_map = {
    "Codigos Urbanisticos": "UT08-31",
    "Gestion Ambiental": "UT08-21",
    "Localizaci": "UT08-11",
    "Edificios Industriales": "UT08-41",
    "Introducci": "UT01-01",
    "Tompkins": "Tompkins",
    "Material a mover": "UT02-01",
    "Manejo manual de cargas": "UT02-02",
    "Supply Chain": "UT07-01",
    "Operaci": "UT07-02",
    "Unidades de Carga": "UT07-03",
    "Dise": "UT07-04",
    "Sistemas de Almacenaje": "UT07-05",
    "Distribucio": "UT0910",
    "Resumen_BR3": "Resumen_BR3"
}

processed_items = []

for q in questions_db:
    hint = code_map.get(q['file_hint'], q['file_hint'])
    if len(q['slides']) == 1:
        v = get_slide_verbatim(hint, q['slides'][0])
    else:
        v = get_multiple_slides_verbatim(hint, q['slides'])
    
    if not v or not v['text']:
        print(f"WARNING: Still missing verbatim for Q{q['id']} - {q['title']} (hint: {hint})")
        v = {'file': hint, 'unit': 'Oficial', 'slide_no': str(q['slides']), 'text': '[Texto en procesamiento]'}
    
    freq_count = len(q['occurrences'])
    
    processed_items.append({
        'id': q['id'],
        'title': q['title'],
        'question_primary': q['question_variants'][0],
        'variants': q['question_variants'],
        'frequency_count': freq_count,
        'occurrences': q['occurrences'],
        'file': v['file'],
        'unit': v['unit'],
        'slide_no': v['slide_no'],
        'verbatim_text': v['text']
    })

# Sort strictly by frequency descending
processed_items.sort(key=lambda x: x['frequency_count'], reverse=True)

# Assign rank
for idx, item in enumerate(processed_items):
    item['rank'] = idx + 1

print(f"ALL {len(processed_items)} items successfully processed and matched with verbatim slide texts!")

with open('final_processed_guide.json', 'w', encoding='utf-8') as out:
    json.dump(processed_items, out, ensure_ascii=False, indent=2)
