import json
import html

# Load processed items
with open('final_processed_guide.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Helper function to categorize by unit for the unit filter
def get_category(item):
    u = item['unit'].lower()
    f = item['file'].lower()
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
    if freq >= 7:
        return ('critica', '🔥 MUY ALTA (7-9x)', '#ef4444', 'rgba(239, 68, 68, 0.15)')
    elif freq >= 5:
        return ('alta', '⚡ ALTA (5-6x)', '#f59e0b', 'rgba(245, 158, 11, 0.15)')
    elif freq >= 3:
        return ('media', '📌 MEDIA (3-4x)', '#06b6d4', 'rgba(6, 182, 212, 0.15)')
    else:
        return ('estandar', '🔹 REGULAR (2x)', '#8b5cf6', 'rgba(139, 92, 246, 0.15)')

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Guía Maestra de Estudio – Manejo de Materiales UTN</title>
  <meta name="description" content="Guía de estudio exhaustiva y ultra optimizada para parciales y finales de Manejo de Materiales y Distribución en Planta (UTN FRBA - Cátedra Grimolizzi). Ordenada por frecuencia exacta con respuestas verbatim oficiales." />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #090d16;
      --bg-surface: #0f172a;
      --bg-card: #131d33;
      --bg-card-hover: #17233e;
      --bg-card-border: #1e2c4f;
      --bg-quote: #0a0f1d;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: #3b82f6;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-indigo: #6366f1;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-red: #ef4444;
      
      --radius-lg: 16px;
      --radius-md: 10px;
      --radius-sm: 6px;
      --shadow-card: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.65;
      font-size: 15px;
      padding-bottom: 5rem;
      background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.06) 0px, transparent 50%);
      background-attachment: fixed;
    }

    /* Container */
    .app-container {
      max-width: 1160px;
      margin: 0 auto;
      padding: 1.5rem 1.25rem;
    }

    /* Header */
    header {
      background: linear-gradient(180deg, #131d33 0%, rgba(15, 23, 42, 0.95) 100%);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 2.5rem 2rem 2rem;
      margin-bottom: 2rem;
      position: relative;
      overflow: hidden;
      box-shadow: var(--shadow-card);
    }

    header::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
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
      background: rgba(59, 130, 246, 0.12);
      border: 1px solid rgba(59, 130, 246, 0.3);
      color: #93c5fd;
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .univ-tag::before {
      content: '●';
      color: var(--accent-blue);
      font-size: 0.7rem;
    }

    h1 {
      font-size: clamp(1.8rem, 3.5vw, 2.6rem);
      font-weight: 900;
      color: #ffffff;
      line-height: 1.2;
      margin-bottom: 0.75rem;
      letter-spacing: -0.02em;
    }

    h1 span {
      background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 50%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .header-desc {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 820px;
      line-height: 1.6;
      margin-bottom: 1.75rem;
    }

    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 0.85rem;
    }

    .stat-pill {
      background: rgba(10, 15, 29, 0.7);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0.85rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }

    .stat-pill .num {
      font-size: 1.4rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
    }

    .stat-pill .label {
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    /* Sticky Control Toolbar */
    .toolbar-sticky {
      position: sticky;
      top: 1rem;
      z-index: 1000;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 1rem 1.25rem;
      margin-bottom: 2rem;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.6);
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
      background: rgba(10, 15, 29, 0.9);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-md);
      color: var(--text-main);
      padding: 0.7rem 1rem 0.7rem 2.6rem;
      font-size: 0.95rem;
      font-family: inherit;
      transition: all 0.2s ease;
    }

    .search-input:focus {
      outline: none;
      border-color: var(--accent-blue);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
      background: #090d16;
    }

    .btn-tool {
      background: var(--bg-surface);
      border: 1px solid var(--bg-card-border);
      color: var(--text-main);
      padding: 0.68rem 1rem;
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
      border-color: var(--accent-blue);
      color: #60a5fa;
    }

    .btn-tool.active {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--accent-blue);
      color: #93c5fd;
    }

    /* Filter Pills */
    .filter-pills-row {
      display: flex;
      gap: 0.4rem;
      overflow-x: auto;
      padding-bottom: 0.25rem;
      scrollbar-width: thin;
    }

    .filter-pill {
      background: rgba(19, 29, 51, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }

    .filter-pill:hover {
      background: rgba(59, 130, 246, 0.15);
      color: #fff;
    }

    .filter-pill.active {
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
    }

    /* Counter indicator */
    .active-count {
      font-size: 0.85rem;
      color: var(--text-dim);
      font-weight: 500;
      margin-bottom: 1.25rem;
      padding-left: 0.5rem;
    }
    .active-count strong {
      color: #38bdf8;
    }

    /* Question Cards List */
    .cards-grid {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .question-card {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 1.75rem 2rem;
      box-shadow: var(--shadow-card);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }

    .question-card:hover {
      border-color: rgba(59, 130, 246, 0.4);
      background: var(--bg-card-hover);
      box-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6);
    }

    /* Card Header */
    .card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
      margin-bottom: 1.2rem;
      flex-wrap: wrap;
    }

    .title-group {
      flex: 1;
      min-width: 260px;
    }

    .meta-badges {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 0.6rem;
    }

    .rank-pill {
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.8rem;
      padding: 0.25rem 0.65rem;
      border-radius: var(--radius-sm);
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
    }

    .freq-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 0.25rem 0.65rem;
      border-radius: var(--radius-sm);
      border: 1px solid;
      letter-spacing: 0.03em;
    }

    .unit-badge {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.25rem 0.65rem;
      border-radius: var(--radius-sm);
    }

    .card-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.38;
      letter-spacing: -0.01em;
    }

    /* Occurrences Box */
    .occurrences-box {
      background: rgba(10, 15, 29, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 0.85rem 1.15rem;
      margin-bottom: 1.25rem;
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
      gap: 0.4rem;
    }

    .occ-chip {
      background: rgba(30, 41, 59, 0.8);
      color: #cbd5e1;
      font-size: 0.78rem;
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Response Box */
    .response-container {
      margin-bottom: 1.25rem;
    }

    .response-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.6rem;
    }

    .response-label {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .btn-copy {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 0.3rem 0.7rem;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      font-family: inherit;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-copy:hover {
      background: rgba(59, 130, 246, 0.15);
      color: #fff;
      border-color: var(--accent-blue);
    }

    .verbatim-block {
      background: var(--bg-quote);
      border: 1px solid #1e293b;
      border-left: 4px solid var(--accent-blue);
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      padding: 1.25rem 1.5rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      color: #e2e8f0;
      line-height: 1.7;
      white-space: pre-wrap;
      word-break: break-word;
      transition: filter 0.2s ease;
    }

    /* Flashcard blurred mode */
    body.flashcard-mode .verbatim-block {
      filter: blur(8px);
      user-select: none;
      cursor: pointer;
    }
    body.flashcard-mode .verbatim-block:hover {
      filter: blur(3px);
    }
    body.flashcard-mode .verbatim-block.revealed {
      filter: none;
      user-select: auto;
    }

    /* Source Box */
    .source-tag {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-md);
      padding: 0.6rem 1rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #94a3b8;
    }

    .source-tag strong {
      color: #38bdf8;
      font-weight: 600;
    }

    /* Variants Accordion */
    .variants-details {
      margin-top: 1rem;
      border-top: 1px dashed rgba(255, 255, 255, 0.08);
      padding-top: 0.85rem;
    }

    .variants-summary {
      font-size: 0.82rem;
      color: var(--text-dim);
      font-weight: 600;
      cursor: pointer;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: color 0.2s;
    }

    .variants-summary:hover {
      color: #cbd5e1;
    }

    .variants-list {
      list-style-type: disc;
      padding-left: 1.5rem;
      margin-top: 0.5rem;
      font-size: 0.83rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    /* Print styling */
    @media print {
      body {
        background: #ffffff !important;
        color: #000000 !important;
      }
      .toolbar-sticky, .univ-tag, .btn-copy, .filter-pills-row {
        display: none !important;
      }
      header {
        background: none !important;
        border: 1px solid #000 !important;
        color: #000 !important;
      }
      h1 span {
        -webkit-text-fill-color: #000 !important;
      }
      .question-card {
        background: #ffffff !important;
        border: 1px solid #ccc !important;
        color: #000000 !important;
        box-shadow: none !important;
        page-break-inside: avoid;
        margin-bottom: 1.5rem;
      }
      .card-title {
        color: #000000 !important;
      }
      .verbatim-block {
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
      <div style="font-size: 0.82rem; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">Ciclo Lectivo 2024 / 2025 / 2026</div>
    </div>
    <h1>Manejo de Materiales <span>& Distribución en Planta</span></h1>
    <p class="header-desc">
      Guía Maestra de Estudio estructurada rigurosamente por <strong>frecuencia de aparición</strong> en parciales y recuperatorios históricos. Todas las respuestas corresponden a la <strong>transcripción literal exacta (verbatim)</strong> de las presentaciones oficiales de la cátedra.
    </p>

    <div class="stats-row">
      <div class="stat-pill">
        <span class="num">40</span>
        <span class="label">Preguntas Clave</span>
      </div>
      <div class="stat-pill">
        <span class="num">9x</span>
        <span class="label">Frecuencia Máxima</span>
      </div>
      <div class="stat-pill">
        <span class="num">100%</span>
        <span class="label">Literal Verbatim PPT</span>
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
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar concepto, palabra clave, norma, tema..." oninput="handleSearch()" />
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
      <button class="filter-pill" onclick="setUnitFilter('u1', this)">U1: Intralogística</button>
      <button class="filter-pill" onclick="setUnitFilter('u2', this)">U2: Material a Mover & Cargas</button>
      <button class="filter-pill" onclick="setUnitFilter('u3', this)">U3: Localización, Edificios & Ambiental</button>
      <button class="filter-pill" onclick="setUnitFilter('u7', this)">U7: Almacenes & Supply Chain</button>
      <button class="filter-pill" onclick="setUnitFilter('u9', this)">U9: Distribución en Planta</button>
      <button class="filter-pill" onclick="setUnitFilter('equipos', this)">Equipos & Manutención</button>
    </div>
  </div>

  <div class="active-count" id="activeCounter">
    Mostrando <strong id="visibleCount">40</strong> preguntas de 40
  </div>

  <!-- Cards Grid -->
  <main class="cards-grid" id="cardsGrid">
"""

for item in items:
    cat = get_category(item)
    freq_class, freq_label, freq_color, freq_bg = get_freq_level(item['frequency_count'])
    
    # Occurrences chips
    occ_chips = "".join([f'<span class="occ-chip">{html.escape(o)}</span>' for o in item['occurrences']])
    
    # Variants
    variants_li = "".join([f'<li>{html.escape(v)}</li>' for v in item['variants']])
    
    # Search data string
    search_str = f"{item['rank']} {item['title']} {item['question_primary']} {item['unit']} {item['file']} {item['verbatim_text']} {' '.join(item['occurrences'])}"
    
    html_template += f"""
    <article class="question-card" data-cat="{cat}" data-freq="{item['frequency_count']}" data-search="{html.escape(search_str)}">
      <div class="card-top">
        <div class="title-group">
          <div class="meta-badges">
            <span class="rank-pill">#{item['rank']}</span>
            <span class="freq-badge" style="color: {freq_color}; background: {freq_bg}; border-color: {freq_color}40;">
              {freq_label} • {item['frequency_count']} apariciones
            </span>
            <span class="unit-badge">{html.escape(item['unit'])}</span>
          </div>
          <h2 class="card-title">{item['rank']}. {html.escape(item['title'])}</h2>
        </div>
      </div>

      <div class="occurrences-box">
        <div class="occ-title">
          <span>📊</span> Tomada en los siguientes exámenes:
        </div>
        <div class="occ-chips">
          {occ_chips}
        </div>
      </div>

      <div class="response-container">
        <div class="response-header">
          <div class="response-label">
            <span>📖</span> Transcripción Textual del PPT Oficial:
          </div>
          <button class="btn-copy" onclick="copyQuote(this)">Copiar texto</button>
        </div>
        <blockquote class="verbatim-block" onclick="revealCard(this)">{html.escape(item['verbatim_text'])}</blockquote>
      </div>

      <div class="source-tag">
        <span>📍 <strong>Fuente oficial:</strong> {html.escape(item['unit'])} / {html.escape(item['file'])} (Diapositiva {html.escape(str(item['slide_no']))})</span>
      </div>

      <details class="variants-details">
        <summary class="variants-summary">
          <span>▶</span> Ver redacciones y enunciados en los parciales ({len(item['variants'])})
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
    document.querySelectorAll('.verbatim-block').forEach(b => b.classList.remove('revealed'));
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

function copyQuote(btn) {
  const block = btn.closest('.response-container').querySelector('.verbatim-block');
  if (block) {
    navigator.clipboard.writeText(block.innerText).then(() => {
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

print("Saved ultra styled Guia_Maestra_Parciales_Manejo_de_Materiales.html successfully!")
