import os
import re
import json
import fitz

# Let's inspect how questions are formatted in all the exam files
with open('all_raw_exam_sources.json', 'r', encoding='utf-8') as f:
    raw_sources = json.load(f)

print(f"Total raw sources loaded: {len(raw_sources)}")
for k, text in raw_sources.items():
    print(f"File: {k} | Length: {len(text)} chars")
