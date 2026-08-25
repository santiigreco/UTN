import json
import os
import re
import sys

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Master database of questions covering all exams, parciales, 1P 2026, handwritten photos, finals, etc.
# Code mapping for fast slide lookup
code_map = {
    "UT01-01": "Introducci",
    "Tompkins": "Tompkins",
    "UT02-01": "Material a mover",
    "UT02-02": "Manejo manual de cargas",
    "UT08-11": "Localizaci",
    "UT08-21": "Gestion Ambiental",
    "UT08-31": "Codigos Urbanisticos",
    "UT08-41": "Edificios Industriales",
    "UT07-01": "Supply Chain",
    "UT07-02": "Operaci",
    "UT07-03": "Unidades de Carga",
    "UT07-04": "Dise",
    "UT07-05": "Sistemas de Almacenaje",
    "UT0910": "Distribucio",
    "Resumen_BR3": "Resumen_BR3"
}

def get_slide_text(code_key, slide_num):
    hint = code_map.get(code_key, code_key)
    for fname, fdata in slides_data.items():
        if hint.lower() in fname.lower() or hint.lower() in fdata['path'].lower():
            for s in fdata['slides']:
                if s['slide_no'] == slide_num:
                    return {
                        'file': fname,
                        'unit': fdata['unit'],
                        'slide_no': slide_num,
                        'text': s['text'].strip()
                    }
    return None

def get_slides_text(code_key, slide_nums):
    texts = []
    unit = ""
    full_fname = ""
    for snum in slide_nums:
        st = get_slide_text(code_key, snum)
        if st:
            unit = st['unit']
            full_fname = st['file']
            texts.append(f"--- Diapositiva {snum} ---\n" + st['text'])
    return {
        'file': full_fname,
        'unit': unit,
        'slide_no': ", ".join(map(str, slide_nums)),
        'text': "\n\n".join(texts)
    }

print("Slide retrieval engine configured.")
