import json
import re

with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Search helper
def search_slides(keywords, min_matches=1):
    results = []
    kw_lower = [k.lower() for k in keywords]
    for fname, fdata in slides_data.items():
        unit = fdata['unit']
        for s in fdata['slides']:
            stext = s['text']
            stext_lower = stext.lower()
            matches = sum(1 for kw in kw_lower if kw in stext_lower)
            if matches >= min_matches:
                results.append({
                    'file': fname,
                    'unit': unit,
                    'slide_no': s['slide_no'],
                    'matches': matches,
                    'text': stext
                })
    results.sort(key=lambda x: x['matches'], reverse=True)
    return results

print("Slides search engine loaded.")
