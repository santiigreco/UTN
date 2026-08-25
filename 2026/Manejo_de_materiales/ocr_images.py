import os
import sys
from PIL import Image
import pytesseract

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Check if tesseract is installed in typical paths
tess_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\santi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
]
for p in tess_paths:
    if os.path.exists(p):
        pytesseract.pytesseract.tesseract_cmd = p
        print(f"Found tesseract at {p}")
        break

parciales_dir = 'Parciales'
jpgs = [f for f in os.listdir(parciales_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print(f"Found {len(jpgs)} images in {parciales_dir}")

ocr_results = {}
for img_name in jpgs:
    img_path = os.path.join(parciales_dir, img_name)
    try:
        txt = pytesseract.image_to_string(Image.open(img_path), lang='spa')
        ocr_results[img_name] = txt.strip()
        print(f"--- {img_name} ---")
        print(txt[:200] if txt else "[NO TEXT DETECTED]")
    except Exception as e:
        print(f"Error OCR on {img_name}: {e}")

import json
with open('extracted_ocr_images.json', 'w', encoding='utf-8') as f:
    json.dump(ocr_results, f, ensure_ascii=False, indent=2)
print("Saved extracted_ocr_images.json")
