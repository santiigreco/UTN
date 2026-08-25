import json
import os
import re
import fitz

# Extract all text from all files in Parciales and Finales
all_questions_raw = []

def extract_from_pdf(path, label):
    doc = fitz.open(path)
    full_text = ""
    for i, page in enumerate(doc):
        full_text += f"\n--- Page {i+1} ---\n" + page.get_text()
    return full_text

# Check all files
sources = {}
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.pdf') and ('Parcial' in root or 'Final' in root or 'Parcial' in f or 'Final' in f):
            p = os.path.join(root, f)
            sources[p] = extract_from_pdf(p, f)

for f in ['finales_grimolizzi_pdf.txt', '1p_Apuntes_Manejo', '2p_apuntes_manejo']:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8', errors='ignore') as tf:
            sources[f] = tf.read()

print(f"Loaded {len(sources)} source files for exhaustive question extraction.")

# Save raw text
with open('all_raw_exam_sources.json', 'w', encoding='utf-8') as out:
    json.dump(sources, out, ensure_ascii=False, indent=2)
