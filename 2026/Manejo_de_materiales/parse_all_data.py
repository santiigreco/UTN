import os
import sys
import fitz
import json

# Set standard output encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

slides_data = {}

# 1. Official PPTs
ppt_dirs = ['Unidad 1', 'Unidad 2', 'Unidad 3', 'Unidad 7', 'Unidad 9']
for pdir in ppt_dirs:
    if os.path.exists(pdir):
        for f in os.listdir(pdir):
            if f.lower().endswith('.pdf'):
                fpath = os.path.join(pdir, f)
                doc = fitz.open(fpath)
                slides = []
                for pno, page in enumerate(doc):
                    slides.append({
                        'slide_no': pno + 1,
                        'text': page.get_text()
                    })
                slides_data[f] = {
                    'unit': pdir,
                    'path': fpath,
                    'total_slides': len(doc),
                    'slides': slides
                }

# Root summary pdf
for f in os.listdir('.'):
    if f.lower().endswith('.pdf'):
        doc = fitz.open(f)
        slides = [{'slide_no': pno + 1, 'text': page.get_text()} for pno, page in enumerate(doc)]
        slides_data[f] = {'unit': 'General', 'path': f, 'total_slides': len(doc), 'slides': slides}

with open('extracted_slides.json', 'w', encoding='utf-8') as out:
    json.dump(slides_data, out, ensure_ascii=False, indent=2)

print(f"Extracted {len(slides_data)} slide/material files.")

# 2. Extract Parciales & Finales files
exams_data = {}
exam_sources = [
    'Parciales',
    'Finales',
    '.'
]

for src in ['Parciales', 'Finales']:
    if os.path.exists(src):
        for f in os.listdir(src):
            fpath = os.path.join(src, f)
            if f.lower().endswith('.pdf'):
                doc = fitz.open(fpath)
                pages = []
                for pno, page in enumerate(doc):
                    pages.append({
                        'page_no': pno + 1,
                        'text': page.get_text()
                    })
                exams_data[f] = {
                    'folder': src,
                    'path': fpath,
                    'total_pages': len(doc),
                    'pages': pages
                }

# Check text files in root
for f in ['finales_grimolizzi_pdf.txt', '1p_Apuntes_Manejo', '2p_apuntes_manejo']:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as tf:
            exams_data[f] = {
                'folder': 'Root',
                'path': f,
                'total_pages': 1,
                'pages': [{'page_no': 1, 'text': tf.read()}]
            }

with open('extracted_exams.json', 'w', encoding='utf-8') as out:
    json.dump(exams_data, out, ensure_ascii=False, indent=2)

print(f"Extracted {len(exams_data)} exam/notes files.")
