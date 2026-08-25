import json
import html

# Load curated 1P items
with open('primer_parcial_curated_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Sort items by frequency descending
items.sort(key=lambda x: len(x['occurrences']), reverse=True)
for idx, it in enumerate(items):
    it['rank'] = idx + 1
    it['freq_count'] = len(it['occurrences'])

def get_freq_level(freq):
    if freq >= 7:
        return ('critica', f'🔥 CRÍTICA ({freq}x)', '#ef4444', 'rgba(239, 68, 68, 0.12)')
    elif freq >= 5:
        return ('alta', f'⚡ MUY ALTA ({freq}x)', '#f59e0b', 'rgba(245, 158, 11, 0.12)')
    elif freq >= 3:
        return ('media', f'📌 ALTA ({freq}x)', '#06b6d4', 'rgba(6, 182, 212, 0.12)')
    else:
        return ('estandar', f'🔹 MEDIA ({freq}x)', '#8b5cf6', 'rgba(139, 92, 246, 0.12)')

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Guía Maestra 1° Parcial – Manejo de Materiales UTN FRBA</title>
  <meta name="description" content="Guía maestra de estudio definitiva y optimizada exclusivamente para el PRIMER PARCIAL de Manejo de Materiales y Distribución en Planta (UTN FRBA - Cátedra Grimolizzi). Preguntas ordenadas por frecuencia con respuestas redactadas con criterio técnico oficial." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0e17;
      --bg-surface: #111827;
      --bg-card: #141f33;
      --bg-card-hover: #18263f;
      --bg-card-border: rgba(255, 255, 255, 0.08);
      --bg-answer: #0d1527;
      --border-subtle: rgba(255, 255, 255, 0.06);
      
      --text-main: #f8fafc;
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
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.7;
      font-size: 15.5px;
      padding-bottom: 5rem;
      background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.09) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.07) 0px, transparent 50%);
      background-attachment: fixed;
    }

    .app-container {
      max-width: 1140px;
      margin: 0 auto;
      padding: 1.75rem 1.25rem;
    }

    /* Header */
    header {
      background: linear-gradient(180deg, #141f33 0%, rgba(15, 23, 42, 0.95) 100%);
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
      color: #38bdf8;
    }

    .stat-pill .label {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Sticky Toolbar */
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

    /* Pedagogical Answer Box */
    .answer-box {
      background: var(--bg-answer);
      border: 1px solid #1e293b;
      border-left: 4px solid var(--accent-primary);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 1.4rem 1.65rem;
      font-size: 0.96rem;
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

    .ans-lead {
      margin-bottom: 0.75rem;
      color: #f1f5f9;
      font-weight: 500;
    }

    .ans-sub {
      font-size: 0.98rem;
      font-weight: 800;
      color: #38bdf8;
      margin: 1rem 0 0.5rem;
      letter-spacing: -0.01em;
    }

    .ans-list {
      list-style: none;
      padding-left: 0;
      margin: 0.5rem 0 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .ans-list li {
      position: relative;
      padding-left: 1.4rem;
      color: var(--text-body);
    }

    .ans-list li::before {
      content: '▸';
      position: absolute;
      left: 0;
      top: 0;
      color: #38bdf8;
      font-weight: bold;
      font-size: 1.05rem;
    }

    .ans-list li strong {
      color: #ffffff;
      font-weight: 700;
    }

    .formula-box {
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: var(--radius-sm);
      padding: 0.75rem 1.15rem;
      margin: 0.85rem 0;
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
    }

    .formula-label {
      font-size: 0.7rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #38bdf8;
      text-transform: uppercase;
    }

    .formula-code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.96rem;
      font-weight: 600;
      color: #f8fafc;
    }

    /* Source Tag */
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
      <div style="font-size: 0.82rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">Guía Oficial 1° Parcial • Ciclo 2024 / 2025 / 2026</div>
    </div>
    <h1>Guía Maestra <span>1° Parcial: Manejo de Materiales</span></h1>
    <p class="header-desc">
      Banco consolidado exclusivo para el <strong>PRIMER PARCIAL</strong> (Unidades 1, 2, 3, 7 y 9). Incluye el examen <strong>1P 2026, fotos manuscritas de parciales y recuperatorios</strong>, con respuestas redactadas con <strong>alto criterio pedagógico y fidelidad conceptual a las diapositivas oficiales</strong>.
    </p>

    <div class="stats-row">
      <div class="stat-pill">
        <span class="num">40</span>
        <span class="label">Preguntas 1° Parcial</span>
      </div>
      <div class="stat-pill">
        <span class="num">9x</span>
        <span class="label">Frecuencia Máxima</span>
      </div>
      <div class="stat-pill">
        <span class="num">100%</span>
        <span class="label">Criterio Oficial PPT</span>
      </div>
      <div class="stat-pill">
        <span class="num">5</span>
        <span class="label">Unidades Evaluadas</span>
      </div>
    </div>
  </header>

  <!-- Sticky Controls Toolbar -->
  <div class="toolbar-sticky">
    <div class="toolbar-main-row">
      <div class="search-wrapper">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar por tema (Weber, Mixtura, NCA, Muther, LEED, Pretensado, Tornillos)..." oninput="handleSearch()" />
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
      <button class="filter-pill active" onclick="setUnitFilter('all', this)">Todas (40)</button>
      <button class="filter-pill" onclick="setUnitFilter('top', this)">🔥 Top Frecuencia (≥6x)</button>
      <button class="filter-pill" onclick="setUnitFilter('u1_intra', this)">U1: Intralogística & MHI</button>
      <button class="filter-pill" onclick="setUnitFilter('u2_material', this)">U2: Material & Cargas</button>
      <button class="filter-pill" onclick="setUnitFilter('u3_localiz', this)">U3: Localización de Plantas</button>
      <button class="filter-pill" onclick="setUnitFilter('u3_edificios', this)">U3: Edificios Industriales</button>
      <button class="filter-pill" onclick="setUnitFilter('u3_urbano', this)">U3: Códigos Urbanísticos</button>
      <button class="filter-pill" onclick="setUnitFilter('u3_ambiental', this)">U3: Gestión Ambiental</button>
      <button class="filter-pill" onclick="setUnitFilter('u7_supply', this)">U7: Supply Chain</button>
      <button class="filter-pill" onclick="setUnitFilter('u7_almacenes', this)">U7: Almacenes & Carga</button>
      <button class="filter-pill" onclick="setUnitFilter('u9_layout', this)">U9: Distribución (Layout)</button>
    </div>
  </div>

  <div class="active-count" id="activeCounter">
    Mostrando <strong id="visibleCount">40</strong> preguntas de 40
  </div>

  <!-- Cards Grid -->
  <main class="cards-grid" id="cardsGrid">
"""

for item in items:
    freq_class, freq_label, freq_color, freq_bg = get_freq_level(item['freq_count'])
    occ_chips = "".join([f'<span class="occ-chip">{html.escape(o)}</span>' for o in item['occurrences']])
    variants_li = "".join([f'<li>{html.escape(v)}</li>' for v in item['variants']])
    
    search_str = f"{item['rank']} {item['title']} {item['question']} {item['unit']} {item['file']} {item['answer_html']} {' '.join(item['occurrences'])}"
    
    html_template += f"""
    <article class="question-card" data-cat="{item['category']}" data-freq="{item['freq_count']}" data-search="{html.escape(search_str)}">
      <div class="card-top">
        <div class="title-group">
          <div class="meta-badges">
            <span class="rank-pill">#{item['rank']}</span>
            <span class="freq-badge" style="color: {freq_color}; background: {freq_bg}; border-color: {freq_color}40;">
              {freq_label} • {item['freq_count']} apariciones
            </span>
            <span class="unit-badge">{html.escape(item['unit'])}</span>
          </div>
          <h2 class="card-title">{item['rank']}. {html.escape(item['title'])}</h2>
        </div>
      </div>

      <div class="occurrences-box">
        <div class="occ-title">
          <span>📊</span> Pregunta tomada en los siguientes parciales y recuperatorios:
        </div>
        <div class="occ-chips">
          {occ_chips}
        </div>
      </div>

      <div class="response-container">
        <div class="response-header">
          <div class="response-label">
            <span>📖</span> Respuesta Modelo para Examen (Criterio Oficial de Cátedra):
          </div>
          <button class="btn-copy" onclick="copyAnswer(this)">Copiar respuesta</button>
        </div>
        <div class="answer-box" onclick="revealCard(this)">
          {item['answer_html']}
        </div>
      </div>

      <div class="source-tag">
        <span>📍 <strong>Referencia oficial PPT:</strong> {html.escape(item['unit'])} / {html.escape(item['file'])} (Diapositiva {html.escape(item['slides'])})</span>
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
      matchesUnit = (freq >= 6);
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

# Write to both the specific 1P file and the main guide
with open('Guia_1er_Parcial_Maestra.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('Guia_Maestra_Parciales_Manejo_de_Materiales.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Saved dedicated 1° Parcial guide with curated answers successfully!")
