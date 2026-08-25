import json
import re
import os
import sys

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Load raw sources
with open('all_raw_exam_sources.json', 'r', encoding='utf-8') as f:
    raw_sources = json.load(f)

# Let's write an algorithm to find all questions across all text files
# Questions typically start with numbers like "1)", "1.", "¿", or keywords like "Defina", "Indique", "Describa", "Enuncie", "Enumere", "Explique", etc.

question_patterns = [
    r'(?:^|\n)\s*(\d{1,2}[\.\)]\s*[A-Z¿¡][^\n\?]+\??)',
    r'(?:^|\n)\s*([¿¡][^\n\?]+\?)',
    r'(?:^|\n)\s*((?:Defina|Indique|Describa|Enuncie|Enumere|Explique|Cuáles|Cómo|Qué|Para qué|Mencione|Determinar)\s+[^\n\.\?]{15,}[\?\.]?)'
]

extracted_questions = []

for src_name, text in raw_sources.items():
    lines = text.split('\n')
    for line in lines:
        line_s = line.strip()
        if len(line_s) > 15:
            # Check if line looks like a question or exam prompt
            if re.match(r'^\d{1,2}[\.\)]\s+[A-Z¿¡]', line_s) or line_s.startswith('¿') or line_s.startswith('¡'):
                extracted_questions.append({
                    'source': src_name,
                    'text': line_s
                })
            elif any(line_s.lower().startswith(kw) for kw in ['defina', 'indique', 'describa', 'enuncie', 'enumere', 'explique', 'cuáles', 'cómo', 'para qué', 'mencione']):
                extracted_questions.append({
                    'source': src_name,
                    'text': line_s
                })

print(f"Extracted {len(extracted_questions)} raw question occurrences across all sources.")

with open('extracted_raw_questions_list.json', 'w', encoding='utf-8') as out:
    json.dump(extracted_questions, out, ensure_ascii=False, indent=2)
