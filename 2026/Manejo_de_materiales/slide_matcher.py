import json
import os
import re
import sys

# Set standard output encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 1. Load slides data
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Helper to find verbatim slide text
def find_slide(keywords, excluded_words=[], target_file=None):
    best = None
    best_score = 0
    for fname, fdata in slides_data.items():
        if target_file and target_file.lower() not in fname.lower():
            continue
        unit = fdata['unit']
        for s in fdata['slides']:
            text = s['text']
            t_lower = text.lower()
            if any(ew.lower() in t_lower for ew in excluded_words):
                continue
            score = sum(1 for kw in keywords if kw.lower() in t_lower)
            if score > best_score:
                best_score = score
                best = {
                    'file': fname,
                    'unit': unit,
                    'slide_no': s['slide_no'],
                    'text': text.strip(),
                    'score': score
                }
    return best

print("Slide finder ready.")
