import json
import html
import re

# Load exhaustive processed items
with open('master_catalog_exhaustive.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

def get_category(item):
    u = item['unit'].lower()
    f = item['file'].lower()
    t = item['title'].lower()
    if 'unidad 1' in u or 'ut01' in f or 'tompkins' in f:
        return 'u1'
    elif 'unidad 2' in u or 'ut02' in f:
        return 'u2'
    elif 'unidad 3' in u or 'ut08' in f:
        return 'u3'
    elif 'unidad 7' in u or 'ut07' in f:
        return 'u7'
    elif 'unidad 9' in u or 'ut09' in f or 'distribucio' in f:
        return 'u9'
    else:
        return 'equipos'

def get_freq_level(freq):
    if freq >= 10:
        return ('critica', f'🔥 CRÍTICA ({freq}x)', '#ef4444', 'rgba(239, 68, 68, 0.12)')
    elif freq >= 6:
        return ('alta', f'⚡ MUY ALTA ({freq}x)', '#f59e0b', 'rgba(245, 158, 11, 0.12)')
    elif freq >= 3:
        return ('media', f'📌 ALTA ({freq}x)', '#06b6d4', 'rgba(6, 182, 212, 0.12)')
    else:
        return ('estandar', f'🔹 MEDIA ({freq}x)', '#8b5cf6', 'rgba(139, 92, 246, 0.12)')

def format_rich_answer(text):
    slides = text.split('--- Diapositiva ')
    sections = []
    
    for s in slides:
        s = s.strip()
        if not s:
            continue
        
        m = re.match(r'^(\d+)\s*---?\s*\n?(.*)', s, re.DOTALL)
        slide_num = ""
        body = s
        if m:
            slide_num = f"Diapositiva {m.group(1)}"
            body = m.group(2).strip()
        
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        
        sec_html = ""
        if slide_num:
            sec_html += f'<div class="slide-indicator"><span class="slide-num-pill">Diapositiva {html.escape(m.group(1))}</span></div>'
        
        in_list = False
        buf = []
        
        for line in lines:
            # Formula detection
            if any(sym in line for sym in [' = ', ' + ', ' - ', ' · ', 'Σ', 'Π', 'NCA =', 'SCH =', 't =', 'Fi =', 'Fs =', 'k =', 'MPLi']) and len(line) < 140 and not line.endswith('.'):
                if in_list:
                    buf.append('</ul>')
                    in_list = False
                buf.append(f'<div class="formula-box"><span class="formula-label">FÓRMULA / ECUACIÓN:</span><code class="formula-code">{html.escape(line)}</code></div>')
            # List item
            elif line.startswith(('•', '', '►', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', 'a)', 'b)', 'c)', 'd)', 'e)')):
                if not in_list:
                    buf.append('<ul class="rich-list">')
                    in_list = True
                clean_item = re.sub(r'^[•►\-\*]\s*', '', line)
                if ':' in clean_item and not clean_item.startswith('http'):
                    parts = clean_item.split(':', 1)
                    buf.append(f'<li><strong class="item-keyword">{html.escape(parts[0].strip())}:</strong> {html.escape(parts[1].strip())}</li>')
                else:
                    buf.append(f'<li>{html.escape(clean_item)}</li>')
            # Heading / Subtitle
            elif (line.isupper() and len(line) < 55) or line.endswith(':') or (len(line) < 40 and not line.endswith('.')):
                if in_list:
                    buf.append('</ul>')
                    in_list = False
                buf.append(f'<h4 class="content-heading">{html.escape(line)}</h4>')
            # Regular paragraph
            else:
                if in_list:
                    buf.append('</ul>')
                    in_list = False
                # Highlight keywords if needed
                buf.append(f'<p class="rich-paragraph">{html.escape(line)}</p>')
        
        if in_list:
            buf.append('</ul>')
            in_list = False
            
        sec_html += "\n".join(buf)
        sections.append(sec_html)
        
    return "\n<div class='slide-sep'></div>\n".join(sections)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Guía Maestra de Estudio – Manejo de Materiales UTN FRBA</title>
  <meta name="description" content="Guía maestra de estudio exhaustiva y optimizada para parciales y finales de Manejo de Materiales y Distribución en Planta (UTN FRBA). Tipografía premium, 75 temas consolidados y respuestas según PPT oficial." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0e17;
      --bg-surface: #111827;
      --bg-card: #151f32;
      --bg-card-hover: #19263e;
      --bg-card-border: rgba(255, 255, 255, 0.08);
      --bg-answer: #0d1424;
      --border-subtle: rgba(255, 255, 255, 0.06);
      
      --text-main: #f1f5f9;
      --text-body: #cbd5e1;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --accent-primary: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-indigo: #6366f1;
      
      --radius-lg: 16px;
      --radius-md: 10px;
      --radius-sm: 6px;
      --shadow-card: 0 12px 32px -4px rgba(0, 0, 0, 0.45);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.7;
      font-size: 15.5px;
      padding-bottom: 5rem;
      background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.06) 0px, transparent 50%);
      background-attachment: fixed;
    }

    .app-container {
      max-width: 1140px;
      margin: 0 auto;
      padding: 1.75rem 1.25rem;
    }

    /* Header */
    header {
      background: linear-gradient(180deg, #151f32 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 2.75rem 2.25rem 2.25rem;
      margin-bottom: 2rem;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow-card);
    }

    header::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0; height: 4px;
      background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981, #f59e0b, #ef4444);
    }

    .header-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.25rem;
    }

    .univ-tag {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(59, 130, 246, 0.14);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #93c5fd;
      padding: 0.35rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .univ-tag::before {
      content: '●';
      color: var(--accent-primary);
      font-size: 0.7rem;
    }

    h1 {
      font-size: clamp(1.9rem, 3.8vw, 2.75rem);
      font-weight: 900;
      color: #ffffff;
      line-height: 1.2;
      margin-bottom: 0.85rem;
      letter-spacing: -0.025em;
    }

    h1 span {
      background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .header-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 860px;
      line-height: 1.65;
      margin-bottom: 1.85rem;
    }

    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 0.85rem;
    }

    .stat-pill {
      background: rgba(10, 14, 23, 0.75);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0.85rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }

    .stat-pill .num {
      font-size: 1.45rem;
      font-weight: 800;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #38bdf8;
    }

    .stat-pill .label {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Toolbar */
    .toolbar-sticky {
      position: sticky;
      top: 1rem;
      z-index: 1000;
      background: rgba(17, 24, 39, 0.94);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 1rem 1.25rem;
      margin-bottom: 2rem;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.65);
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }

    .toolbar-main-row {
      display: flex;
      gap: 0.75rem;
      align-items: center;
      flex-wrap: wrap;
    }

    .search-wrapper {
      flex: 1;
      min-width: 280px;
      position: relative;
    }

    .search-icon {
      position: absolute;
      left: 1rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.95rem;
      pointer-events: none;
    }

    .search-input {
      width: 100%;
      background: rgba(10, 14, 23, 0.9);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-md);
      color: var(--text-main);
      padding: 0.72rem 1rem 0.72rem 2.6rem;
      font-size: 0.95rem;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    .search-input:focus {
      outline: none;
      border-color: var(--accent-primary);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
      background: #0a0e17;
    }

    .btn-tool {
      background: var(--bg-surface);
      border: 1px solid var(--bg-card-border);
      color: var(--text-main);
      padding: 0.7rem 1.05rem;
      border-radius: var(--radius-md);
      font-size: 0.85rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .btn-tool:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-primary);
      color: #60a5fa;
    }

    .btn-tool.active {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--accent-primary);
      color: #93c5fd;
    }

    .filter-pills-row {
      display: flex;
      gap: 0.45rem;
      overflow-x: auto;
      padding-bottom: 0.25rem;
      scrollbar-width: thin;
    }

    .filter-pill {
      background: rgba(21, 31, 50, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      padding: 0.38rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }

    .filter-pill:hover {
      background: rgba(59, 130, 246, 0.18);
      color: #ffffff;
    }

    .filter-pill.active {
      background: var(--accent-primary);
      color: #ffffff;
      border-color: var(--accent-primary);
      box-shadow: 0 2px 10px rgba(59, 130, 246, 0.4);
    }

    .active-count {
      font-size: 0.85rem;
      color: var(--text-dim);
      font-weight: 500;
      margin-bottom: 1.25rem;
      padding-left: 0.5rem;
    }
    .active-count strong { color: #38bdf8; }

    /* Cards Grid */
    .cards-grid {
      display: flex;
      flex-direction: column;
      gap: 1.75rem;
    }

    .question-card {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 1.85rem 2.2rem;
      box-shadow: var(--shadow-card);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }

    .question-card:hover {
      border-color: rgba(59, 130, 246, 0.45);
      background: var(--bg-card-hover);
      box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.65);
    }

    /* Card Top */
    .card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
    }

    .title-group { flex: 1; min-width: 260px; }

    .meta-badges {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 0.65rem;
    }

    .rank-pill {
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      color: #ffffff;
      font-weight: 800;
      font-size: 0.82rem;
      padding: 0.25rem 0.7rem;
      border-radius: var(--radius-sm);
      letter-spacing: 0.02em;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
    }

    .freq-badge {
      font-size: 0.78rem;
      font-weight: 700;
      padding: 0.25rem 0.7rem;
      border-radius: var(--radius-sm);
      border: 1px solid;
      letter-spacing: 0.02em;
    }

    .unit-badge {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.25rem 0.7rem;
      border-radius: var(--radius-sm);
    }

    .card-title {
      font-size: 1.28rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.4;
      letter-spacing: -0.015em;
    }

    /* Occurrences Box */
    .occurrences-box {
      background: rgba(10, 14, 23, 0.65);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0.85rem 1.25rem;
      margin-bottom: 1.35rem;
    }

    .occ-title {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #60a5fa;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .occ-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }

    .occ-chip {
      background: rgba(30, 41, 59, 0.85);
      color: #cbd5e1;
      font-size: 0.79rem;
      padding: 0.25rem 0.65rem;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.07);
    }

    /* Response Container */
    .response-container { margin-bottom: 1.35rem; }

    .response-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.65rem;
    }

    .response-label {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }

    .btn-copy {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 0.32rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      font-family: inherit;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-copy:hover {
      background: rgba(59, 130, 246, 0.2);
      color: #ffffff;
      border-color: var(--accent-primary);
    }

    /* New Answer Box with Premium Typography */
    .answer-box {
      background: var(--bg-answer);
      border: 1px solid #1e293b;
      border-left: 4px solid var(--accent-primary);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 1.4rem 1.65rem;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 0.95rem;
      color: var(--text-body);
      line-height: 1.75;
      transition: filter 0.25s ease;
    }

    body.flashcard-mode .answer-box {
      filter: blur(9px);
      user-select: none;
      cursor: pointer;
    }
    body.flashcard-mode .answer-box:hover { filter: blur(3px); }
    body.flashcard-mode .answer-box.revealed { filter: none; user-select: auto; }

    /* Rich text typography inside answer box */
    .slide-indicator {
      margin-bottom: 0.6rem;
      margin-top: 0.4rem;
    }
    .slide-num-pill {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.3);
      padding: 0.15rem 0.55rem;
      border-radius: 4px;
    }

    .slide-sep {
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
      margin: 1.25rem 0;
    }

    .content-heading {
      font-size: 0.98rem;
      font-weight: 700;
      color: #ffffff;
      margin: 0.8rem 0 0.4rem;
    }

    .rich-paragraph {
      margin-bottom: 0.65rem;
      color: var(--text-body);
    }

    .rich-list {
      list-style: none;
      padding-left: 0;
      margin: 0.6rem 0 0.8rem;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }

    .rich-list li {
      position: relative;
      padding-left: 1.35rem;
      color: var(--text-body);
    }

    .rich-list li::before {
      content: '▸';
      position: absolute;
      left: 0;
      top: 0;
      color: #38bdf8;
      font-weight: bold;
      font-size: 1rem;
    }

    .item-keyword {
      color: #ffffff;
      font-weight: 700;
    }

    .formula-box {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: var(--radius-sm);
      padding: 0.65rem 1rem;
      margin: 0.75rem 0;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }

    .formula-label {
      font-size: 0.68rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #38bdf8;
      text-transform: uppercase;
    }

    .formula-code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.92rem;
      font-weight: 600;
      color: #f8fafc;
    }

    /* Source Box */
    .source-tag {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-md);
      padding: 0.65rem 1.15rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.84rem;
      color: #94a3b8;
    }

    .source-tag strong { color: #38bdf8; font-weight: 700; }

    /* Variants Accordion */
    .variants-details {
      margin-top: 1.1rem;
      border-top: 1px dashed rgba(255, 255, 255, 0.08);
      padding-top: 0.85rem;
    }

    .variants-summary {
      font-size: 0.83rem;
      color: var(--text-dim);
      font-weight: 600;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: color 0.2s;
    }

    .variants-summary:hover { color: #cbd5e1; }

    .variants-list {
      list-style-type: disc;
      padding-left: 1.5rem;
      margin-top: 0.55rem;
      font-size: 0.85rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    @media print {
      body { background: #ffffff !important; color: #000000 !important; }
      .toolbar-sticky, .univ-tag, .btn-copy, .filter-pills-row { display: none !important; }
      header { background: none !important; border: 1px solid #000 !important; color: #000 !important; }
      h1 span { -webkit-text-fill-color: #000 !important; }
      .question-card {
        background: #ffffff !important;
        border: 1px solid #ccc !important;
        color: #000000 !important;
        box-shadow: none !important;
        page-break-inside: avoid;
        margin-bottom: 1.5rem;
      }
      .card-title { color: #000000 !important; }
      .answer-box {
        background: #f8fafc !important;
        color: #0f172a !important;
        border-left: 4px solid #000 !important;
        filter: none !important;
      }
    }
  </style>
</head>
<body>

<div class="app-container">
  
  <header>
    <div class="header-top">
      <div class="univ-tag">UTN FRBA • Cátedra Grimolizzi</div>
      <div style="font-size: 0.82rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">Banco Maestro Exhaustivo • Ciclo 2024 / 2025 / 2026</div>
    </div>
    <h1>Manejo de Materiales <span>& Distribución en Planta</span></h1>
    <p class="header-desc">
      Guía Maestra de Estudio con <strong>75 temas y preguntas consolidadas</strong> a partir de <strong>1° y 2° Parciales, Recuperatorios, 1P 2026, Fotos Manuscritas y Exámenes Finales</strong>. Formato optimizado para máxima legibilidad pedagógica respetando fielmente las diapositivas de la cátedra.
    </p>

    <div class="stats-row">
      <div class="stat-pill">
        <span class="num">75</span>
        <span class="label">Preguntas Totales</span>
      </div>
      <div class="stat-pill">
        <span class="num">25x</span>
        <span class="label">Frecuencia Máxima</span>
      </div>
      <div class="stat-pill">
        <span class="num">100%</span>
        <span class="label">Contenido Oficial PPT</span>
      </div>
      <div class="stat-pill">
        <span class="num">6</span>
        <span class="label">Unidades Temáticas</span>
      </div>
    </div>
  </header>

  <!-- Sticky Controls Toolbar -->
  <div class="toolbar-sticky">
    <div class="toolbar-main-row">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar concepto, fórmula, autor (Weber, Muther, LEED), norma o palabra clave..." oninput="handleSearch()" />
      </div>
      
      <button id="btnStudyMode" class="btn-tool" onclick="toggleStudyMode()">
        <span>👁️</span> Modo Autoevaluación
      </button>

      <button id="btnToggleAll" class="btn-tool" onclick="toggleAllVariants()">
        <span>📑</span> Variantes de Parcial
      </button>

      <button class="btn-tool" onclick="window.print()">
        <span>🖨️</span> Imprimir / PDF
      </button>
    </div>

    <div class="filter-pills-row">
      <button class="filter-pill active" onclick="setUnitFilter('all', this)">Todas (75)</button>
      <button class="filter-pill" onclick="setUnitFilter('top', this)">🔥 Top Frecuencia (≥10x)</button>
      <button class="filter-pill" onclick="setUnitFilter('u1', this)">U1: Intralogística & MHI</button>
      <button class="filter-pill" onclick="setUnitFilter('u2', this)">U2: Material a Mover & Carga Física</button>
      <button class="filter-pill" onclick="setUnitFilter('u3', this)">U3: Localización, Edificios & Ambiental</button>
      <button class="filter-pill" onclick="setUnitFilter('u7', this)">U7: Almacenes & Supply Chain</button>
      <button class="filter-pill" onclick="setUnitFilter('u9', this)">U9: Distribución en Planta</button>
      <button class="filter-pill" onclick="setUnitFilter('equipos', this)">Equipos & Manutención</button>
    </div>
  </div>

  <div class="active-count" id="activeCounter">
    Mostrando <strong id="visibleCount">75</strong> preguntas de 75
  </div>

  <!-- Cards Grid -->
  <main class="cards-grid" id="cardsGrid">
"""

for item in items:
    cat = get_category(item)
    freq_class, freq_label, freq_color, freq_bg = get_freq_level(item['frequency_count'])
    
    occ_chips = "".join([f'<span class="occ-chip">{html.escape(o)}</span>' for o in item['occurrences']])
    variants_li = "".join([f'<li>{html.escape(v)}</li>' for v in item['variants']])
    
    # Format rich answer
    rich_ans_html = format_rich_answer(item['verbatim_text'])
    
    search_str = f"{item['rank']} {item['title']} {item['question_primary']} {item['unit']} {item['file']} {item['verbatim_text']} {' '.join(item['occurrences'])}"
    
    html_template += f"""
    <article class="question-card" data-cat="{cat}" data-freq="{item['frequency_count']}" data-search="{html.escape(search_str)}">
      <div class="card-top">
        <div class="title-group">
          <div class="meta-badges">
            <span class="rank-pill">#{item['rank']}</span>
            <span class="freq-badge" style="color: {freq_color}; background: {freq_bg}; border-color: {freq_color}40;">
              {freq_label} • {item['frequency_count']} registros
            </span>
            <span class="unit-badge">{html.escape(item['unit'])}</span>
          </div>
          <h2 class="card-title">{item['rank']}. {html.escape(item['title'])}</h2>
        </div>
      </div>

      <div class="occurrences-box">
        <div class="occ-title">
          <span>📊</span> Apariciones en exámenes (Parciales, Recuperatorios y Finales):
        </div>
        <div class="occ-chips">
          {occ_chips}
        </div>
      </div>

      <div class="response-container">
        <div class="response-header">
          <div class="response-label">
            <span>📖</span> Respuesta oficial según presentación de la cátedra:
          </div>
          <button class="btn-copy" onclick="copyAnswer(this)">Copiar texto</button>
        </div>
        <div class="answer-box" onclick="revealCard(this)">
          {rich_ans_html}
        </div>
      </div>

      <div class="source-tag">
        <span>📍 <strong>Fuente oficial:</strong> {html.escape(item['unit'])} / {html.escape(item['file'])} (Diapositiva {html.escape(str(item['slide_no']))})</span>
      </div>

      <details class="variants-details">
        <summary class="variants-summary">
          <span>▶</span> Ver redacciones y enunciados en los exámenes ({len(item['variants'])})
        </summary>
        <ul class="variants-list">
          {variants_li}
        </ul>
      </details>
    </article>
"""

html_template += """
  </main>
</div>

<script>
let currentUnitFilter = 'all';

function handleSearch() {
  applyFilters();
}

function setUnitFilter(unit, btn) {
  currentUnitFilter = unit;
  document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}

function applyFilters() {
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  const cards = document.querySelectorAll('.question-card');
  let visible = 0;

  cards.forEach(card => {
    const text = card.getAttribute('data-search').toLowerCase();
    const cat = card.getAttribute('data-cat');
    const freq = parseInt(card.getAttribute('data-freq') || '0', 10);

    const matchesQuery = !query || text.includes(query);
    let matchesUnit = false;

    if (currentUnitFilter === 'all') {
      matchesUnit = true;
    } else if (currentUnitFilter === 'top') {
      matchesUnit = (freq >= 10);
    } else {
      matchesUnit = (cat === currentUnitFilter);
    }

    if (matchesQuery && matchesUnit) {
      card.style.display = 'block';
      visible++;
    } else {
      card.style.display = 'none';
    }
  });

  document.getElementById('visibleCount').textContent = visible;
}

function toggleStudyMode() {
  const body = document.body;
  const btn = document.getElementById('btnStudyMode');
  body.classList.toggle('flashcard-mode');
  if (body.classList.contains('flashcard-mode')) {
    btn.classList.add('active');
    btn.innerHTML = '<span>👁️</span> Salir Autoevaluación';
  } else {
    btn.classList.remove('active');
    btn.innerHTML = '<span>👁️</span> Modo Autoevaluación';
    document.querySelectorAll('.answer-box').forEach(b => b.classList.remove('revealed'));
  }
}

function revealCard(el) {
  if (document.body.classList.contains('flashcard-mode')) {
    el.classList.toggle('revealed');
  }
}

let variantsOpen = false;
function toggleAllVariants() {
  variantsOpen = !variantsOpen;
  const details = document.querySelectorAll('.variants-details');
  details.forEach(d => {
    d.open = variantsOpen;
  });
  const btn = document.getElementById('btnToggleAll');
  if (variantsOpen) {
    btn.classList.add('active');
  } else {
    btn.classList.remove('active');
  }
}

function copyAnswer(btn) {
  const box = btn.closest('.response-container').querySelector('.answer-box');
  if (box) {
    navigator.clipboard.writeText(box.innerText).then(() => {
      const originalText = btn.innerText;
      btn.innerText = '✓ ¡Copiado!';
      btn.style.borderColor = '#10b981';
      btn.style.color = '#10b981';
      setTimeout(() => {
        btn.innerText = originalText;
        btn.style.borderColor = '';
        btn.style.color = '';
      }, 2000);
    });
  }
}
</script>

</body>
</html>
"""

with open('Guia_Maestra_Parciales_Manejo_de_Materiales.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Saved beautifully styled Guia_Maestra_Parciales_Manejo_de_Materiales.html successfully!")
