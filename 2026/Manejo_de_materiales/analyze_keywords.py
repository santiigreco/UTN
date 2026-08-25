import json
import re
import os

with open('extracted_raw_questions_list.json', 'r', encoding='utf-8') as f:
    raw_q = json.load(f)

print(f"Total question occurrences: {len(raw_q)}")

# Let's inspect unique terms and concepts
keywords_map = {}
for item in raw_q:
    t = item['text'].lower()
    # clean up numbering
    t = re.sub(r'^\d+[\.\)]\s*', '', t).strip()
    words = re.findall(r'[a-záéíóúñ]{4,}', t)
    for w in words:
        keywords_map[w] = keywords_map.get(w, 0) + 1

sorted_kw = sorted(keywords_map.items(), key=lambda x: x[1], reverse=True)
print("Top 30 keywords across all questions:")
for w, c in sorted_kw[:30]:
    print(f"  {w}: {c}")
