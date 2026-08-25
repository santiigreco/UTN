import json
import os
import re

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Load extracted exams text
with open('all_exam_texts.json', 'r', encoding='utf-8') as f:
    exam_texts = json.load(f)

print("Loaded slides and exam texts successfully.")
