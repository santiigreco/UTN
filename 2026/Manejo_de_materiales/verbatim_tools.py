import json
import os
import re
import sys

# Set standard output encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Helper function to get exact slide verbatim
def get_slide_verbatim(filename_contains, slide_number):
    for fname, fdata in slides_data.items():
        if filename_contains.lower() in fname.lower():
            for s in fdata['slides']:
                if s['slide_no'] == slide_number:
                    return {
                        'file': fname,
                        'unit': fdata['unit'],
                        'slide_no': slide_number,
                        'text': s['text'].strip()
                    }
    return None

def search_slide_exact(pattern, filename_contains=None):
    results = []
    for fname, fdata in slides_data.items():
        if filename_contains and filename_contains.lower() not in fname.lower():
            continue
        for s in fdata['slides']:
            if re.search(pattern, s['text'], re.IGNORECASE):
                results.append({
                    'file': fname,
                    'unit': fdata['unit'],
                    'slide_no': s['slide_no'],
                    'text': s['text'].strip()
                })
    return results

print("Verbatim search tools ready.")
