import json

with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

for k in slides_data.keys():
    print(repr(k))
