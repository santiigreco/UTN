import os
import fitz
import json

parciales_files = [
    'Parciales/Preguntas-1P-Manejo-LC-TERMINADO.pdf',
    'Parciales/Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf',
    'Parciales/Resumen-de-Preguntas-Manejo-de-Materiales.pdf',
    'Parciales/FinalManejoGRIMO2025.pdf',
    'Parciales/Respuestas-MMyDP-Final.pdf',
    'Parciales/Respuestas-MMyDP-Para-el-final.pdf',
    'Finales/FINALES GRIMOLIZZI 2024,2025,2026.pdf'
]

results = {}
for p in parciales_files:
    if os.path.exists(p):
        doc = fitz.open(p)
        txt = ""
        for i, page in enumerate(doc):
            txt += f"\n--- Page {i+1} ---\n" + page.get_text()
        results[p] = {
            'pages': len(doc),
            'text': txt
        }

with open('all_exam_texts.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved all_exam_texts.json")
