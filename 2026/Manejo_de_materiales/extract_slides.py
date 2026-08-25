import os
import fitz
import json

slides_data = {}

# 1. Extract official PPTs
ppt_dirs = ['Unidad 1', 'Unidad 2', 'Unidad 3', 'Unidad 7', 'Unidad 9']
for pdir in ppt_dirs:
    if os.path.exists(pdir):
        for f in os.listdir(pdir):
            if f.endswith('.pdf'):
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

# Also check root pdfs
for f in os.listdir('.'):
    if f.endswith('.pdf'):
        doc = fitz.open(f)
        slides = [{'slide_no': pno + 1, 'text': page.get_text()} for pno, page in enumerate(doc)]
        slides_data[f] = {'unit': 'General', 'path': f, 'total_slides': len(doc), 'slides': slides}

print(f"Total PPT files extracted: {len(slides_data)}")
for k, v in slides_data.items():
    print(f"  - {k}: {v['total_slides']} slides")

with open('extracted_slides.json', 'w', encoding='utf-8') as out:
    json.dump(slides_data, out, ensure_ascii=False, indent=2)
print("Saved extracted_slides.json successfully.")
