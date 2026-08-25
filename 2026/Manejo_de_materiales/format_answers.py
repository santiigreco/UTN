import json
import re
import html

# Load exhaustive processed items
with open('master_catalog_exhaustive.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Function to clean and nicely format the PPT text into human-friendly, beautiful HTML
def format_answer_html(text, item_id, title):
    # Remove slide header noise like "--- Diapositiva X ---" into nice subheaders
    # Replace bullet marks
    
    # Split slides if multiple
    slides = text.split('--- Diapositiva ')
    
    formatted_sections = []
    for s in slides:
        s = s.strip()
        if not s:
            continue
        
        # Check if starts with slide number
        m = re.match(r'^(\d+)\s*---?\s*\n?(.*)', s, re.DOTALL)
        slide_num = ""
        slide_content = s
        if m:
            slide_num = f"Diapositiva {m.group(1)}"
            slide_content = m.group(2).strip()
        
        # Clean lines
        lines = [l.strip() for l in slide_content.split('\n') if l.strip()]
        
        section_html = ""
        if slide_num:
            section_html += f'<div class="slide-subheading"><span class="slide-badge">📍 {html.escape(slide_num)}</span></div>'
        
        in_list = False
        content_buffer = []
        
        for line in lines:
            # Detect formulas
            if re.search(r'(=|Π|Σ|NCA =|SCH =|t =|Fi =|Fs =|k =|MPL)', line) and len(line) < 120 and ('=' in line or 'Π' in line or 'Σ' in line):
                if in_list:
                    content_buffer.append('</ul>')
                    in_list = False
                content_buffer.append(f'<div class="formula-callout"><code>{html.escape(line)}</code></div>')
            # Detect bullet points
            elif line.startswith(('•', '', '►', '-', '*', '1.', '2.', '3.', '4.', '5.', 'a)', 'b)', 'c)', 'd)')):
                if not in_list:
                    content_buffer.append('<ul class="answer-list">')
                    in_list = True
                clean_bullet = re.sub(r'^[•►\-\*]\s*', '', line)
                
                # Highlight key term before colon
                if ':' in clean_bullet and not clean_bullet.startswith('http'):
                    parts = clean_bullet.split(':', 1)
                    bullet_html = f'<li><strong>{html.escape(parts[0].strip())}:</strong> {html.escape(parts[1].strip())}</li>'
                else:
                    bullet_html = f'<li>{html.escape(clean_bullet)}</li>'
                content_buffer.append(bullet_html)
            # Detect section subtitles in PPT
            elif (line.isupper() and len(line) < 60) or line.endswith(':') or (len(line) < 45 and not line.endswith('.')):
                if in_list:
                    content_buffer.append('</ul>')
                    in_list = False
                content_buffer.append(f'<h4 class="answer-subtitle">{html.escape(line)}</h4>')
            # Regular text paragraph
            else:
                if in_list:
                    content_buffer.append('</ul>')
                    in_list = False
                content_buffer.append(f'<p class="answer-p">{html.escape(line)}</p>')
        
        if in_list:
            content_buffer.append('</ul>')
            in_list = False
            
        section_html += "\n".join(content_buffer)
        formatted_sections.append(section_html)
        
    return "\n<hr class='slide-divider'/>\n".join(formatted_sections)

print("Answer formatter ready.")
