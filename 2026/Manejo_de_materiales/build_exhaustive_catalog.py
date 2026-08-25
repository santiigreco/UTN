import json
import re
import os
import sys

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Load raw questions
with open('extracted_raw_questions_list.json', 'r', encoding='utf-8') as f:
    raw_questions = json.load(f)

code_map = {
    "UT01-01": "Introducci",
    "Tompkins": "Tompkins",
    "UT02-01": "Material a mover",
    "UT02-02": "Manejo manual de cargas",
    "UT08-11": "Localizaci",
    "UT08-21": "Gestion Ambiental",
    "UT08-31": "Codigos Urbanisticos",
    "UT08-41": "Edificios Industriales",
    "UT07-01": "Supply Chain",
    "UT07-02": "Operaci",
    "UT07-03": "Unidades de Carga",
    "UT07-04": "Dise",
    "UT07-05": "Sistemas de Almacenaje",
    "UT0910": "Distribucio",
    "Resumen_BR3": "Resumen_BR3"
}

def get_slide_text(code_hint, slide_num):
    hint = code_map.get(code_hint, code_hint)
    for fname, fdata in slides_data.items():
        if hint.lower() in fname.lower() or hint.lower() in fdata['path'].lower():
            for s in fdata['slides']:
                if s['slide_no'] == slide_num:
                    return {
                        'file': fname,
                        'unit': fdata['unit'],
                        'slide_no': slide_num,
                        'text': s['text'].strip()
                    }
    return None

def get_multiple_slides_text(code_hint, slide_nums):
    texts = []
    unit = ""
    full_fname = ""
    for snum in slide_nums:
        st = get_slide_text(code_hint, snum)
        if st:
            unit = st['unit']
            full_fname = st['file']
            texts.append(f"--- Diapositiva {snum} ---\n" + st['text'])
    return {
        'file': full_fname,
        'unit': unit,
        'slide_no': ", ".join(map(str, slide_nums)),
        'text': "\n\n".join(texts)
    }

# Build exhaustive topic definitions with regex matchers against raw_questions
topics = [
    {
        "id": 1,
        "title": "Área de Mixtura de Usos en CABA: Definición, Clasificación (Áreas 1 a 4) y Ejemplos",
        "primary_q": "¿Qué define el área de mixtura según el Código Urbanístico de CABA? Indique ejemplos",
        "regex": r'mixtura|c[oó]digo urban[ií]stico|caba.*mixtura',
        "code_hint": "UT08-31",
        "slides": [13, 14],
        "manual_occurrences": ["1° Parcial 2026", "1° Parcial 26/06/2023 - Tema 2", "1° Parcial 08/07/2024 - Tema 2", "Recuperatorio 1°P 09/12/2024", "Recuperatorio 1°P 09/12/2025"]
    },
    {
        "id": 2,
        "title": "Gráfica de Relación de Actividades / Carta Muthed (SLP de Richard Muther)",
        "primary_q": "Para la gráfica de relación de actividades, indique qué representan: X1, X2, A y 1",
        "regex": r'carta muthed|relaci[oó]n de actividades|muther.*relaci|c[oó]digo de proximidad',
        "code_hint": "UT0910",
        "slides": [22, 23, 24],
        "manual_occurrences": ["1° Parcial 2026", "1° Parcial 13/06/2022 - Tema 2", "1° Parcial 26/06/2023 - Tema 2", "1° Parcial 08/07/2024 - Tema 2"]
    },
    {
        "id": 3,
        "title": "Nivel de Complejidad Ambiental (NCA): Polinomio, Parámetros y Categorías 1, 2 y 3",
        "primary_q": "¿Para qué se utiliza el Nivel de Complejidad Ambiental? Indique además los rangos que define",
        "regex": r'complejidad ambiental|nca|polinomio.*nca|categor[ií]a.*ambiental',
        "code_hint": "UT08-21",
        "slides": [22, 23, 24],
        "manual_occurrences": ["1° Parcial 2026", "1° Parcial 26/06/2023 - Tema 1", "1° Parcial 08/07/2024 - Tema 1", "Recuperatorio 1°P 09/12/2024"]
    },
    {
        "id": 4,
        "title": "Planeación de Instalaciones: Definición, Tareas, Objetivos y ¿Qué analiza, dimensiona y diseña?",
        "primary_q": "¿Qué analiza, dimensiona, diseña y selecciona la planeación de instalaciones?",
        "regex": r'planeaci[oó]n de instalaciones|analiza, dimensiona|objetivos de la planeaci',
        "code_hint": "Tompkins",
        "slides": [2, 6, 7],
        "manual_occurrences": ["1° Parcial 2026 (P9)", "1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2024", "Recuperatorio 1°P 09/12/2025"]
    },
    {
        "id": 5,
        "title": "Principio de Estandarización del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Estandarización de acuerdo con el MHI e indique dos puntos clave",
        "regex": r'principio de estandarizaci[oó]n|estandarizaci[oó]n.*mhi',
        "code_hint": "UT01-01",
        "slides": [18],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 6,
        "title": "Principio de Trabajo del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Trabajo de acuerdo con el MHI e indique dos puntos clave",
        "regex": r'principio de trabajo|trabajo.*mhi|simplificar.*movimiento',
        "code_hint": "UT01-01",
        "slides": [15],
        "manual_occurrences": ["1° Parcial 2026 (P7)", "Foto Manuscrita (P2)"]
    },
    {
        "id": 7,
        "title": "Principio de Planificación del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Planificación del MHI e indique sus puntos clave",
        "regex": r'principio de planificaci[oó]n|planificaci[oó]n.*mhi',
        "code_hint": "UT01-01",
        "slides": [14],
        "manual_occurrences": ["Finales Grimolizzi", "Resumen-de-Preguntas"]
    },
    {
        "id": 8,
        "title": "Principio de Ergonomía del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Ergonomía del MHI y cómo impacta en las operaciones",
        "regex": r'principio de ergonom[ií]a|ergonom[ií]a.*mhi',
        "code_hint": "UT01-01",
        "slides": [16],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 9,
        "title": "Principio de Carga Unitaria del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Carga Unitaria del MHI y sus ventajas",
        "regex": r'principio de carga unitaria|carga unitaria.*mhi',
        "code_hint": "UT01-01",
        "slides": [17],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 10,
        "title": "Principio de Utilización del Espacio del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Utilización del Espacio según el MHI",
        "regex": r'utilizaci[oó]n del espacio|espacio c[uú]bico.*mhi',
        "code_hint": "UT01-01",
        "slides": [19],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 11,
        "title": "Principio del Sistema del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio del Sistema del MHI y su enfoque integral",
        "regex": r'principio del sistema|sistema.*mhi',
        "code_hint": "UT01-01",
        "slides": [20],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 12,
        "title": "Principio de Automatización del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio de Automatización del MHI",
        "regex": r'principio de automatizaci[oó]n|automatizaci[oó]n.*mhi',
        "code_hint": "UT01-01",
        "slides": [21],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 13,
        "title": "Principio Ambiental y del Ciclo de Vida del Material Handling Institute (MHI)",
        "primary_q": "Enuncie el Principio Ambiental y del Costo del Ciclo de Vida según el MHI",
        "regex": r'principio ambiental|costo del ciclo de vida|ciclo de vida.*mhi',
        "code_hint": "UT01-01",
        "slides": [22, 23],
        "manual_occurrences": ["Finales Grimolizzi", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 14,
        "title": "Método de Alfred Weber para la Localización de Plantas: Etapas y Fundamento",
        "primary_q": "Weber fue el primero en introducir el análisis sistemático para la localización de plantas, describa cada una de las etapas del método de Weber",
        "regex": r'weber|tri[aá]ngulo de weber|etapas.*weber',
        "code_hint": "UT08-11",
        "slides": [4, 5],
        "manual_occurrences": ["1° Parcial 2026 (P8)", "Foto Manuscrita (P3)"]
    },
    {
        "id": 15,
        "title": "Clasificación del Uso del Suelo en PBA (Decreto Ley 8912/77): Áreas y Zonas",
        "primary_q": "La clasificación del uso del suelo en la PBA define áreas y zonas, indique los tipos de zonas que define esta clasificación",
        "regex": r'pba.*[aá]reas y zonas|8912|uso del suelo.*pba|zonas.*pba',
        "code_hint": "UT08-31",
        "slides": [4, 5, 6],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 16,
        "title": "Localización de Centros de Servicios (Consumo In Situ vs Prestados a Domicilio)",
        "primary_q": "Para el estudio de la localización de centros de servicios se dividen en dos clases principales. Indicar cuáles son y sus factores",
        "regex": r'centros de servicios|servicios in situ|consumen in situ',
        "code_hint": "UT08-11",
        "slides": [13, 14],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 17,
        "title": "Factores Críticos para Localización de Centros Comerciales y Locales Minoristas",
        "primary_q": "Enumerar 4 factores críticos para la localización de centros comerciales y locales minoristas",
        "regex": r'centros comerciales|locales minoristas|comerciales y minoristas',
        "code_hint": "UT08-11",
        "slides": [15],
        "manual_occurrences": ["1° Parcial 2026 (P12)", "1° Parcial Fotos Temas 1 y 2"]
    },
    {
        "id": 18,
        "title": "Método Funcional Basado en Costos para Localización de Planta (Función Objetivo Fi)",
        "primary_q": "Utilizando el método funcional basado en costos para localización de planta, indique qué valor toma Fi cuando la locación B es óptima",
        "regex": r'm[eé]todo funcional|funci[oó]n objetivo fi|f_i =|valor toma fi',
        "code_hint": "UT08-11",
        "slides": [12],
        "manual_occurrences": ["1° Parcial 13/06/2022", "Foto Manuscrita (P4)"]
    },
    {
        "id": 19,
        "title": "Pisos Industriales: Capas (Subrasante, Sub-base, Base) y Barrera de Vapor",
        "primary_q": "¿Cómo está conformada la base y sub base de un piso industrial y para qué se usa la barrera de vapor?",
        "regex": r'piso industrial|subrasante|barrera de vapor|sub base.*base',
        "code_hint": "UT08-41",
        "slides": [24, 25, 26, 27],
        "manual_occurrences": ["1° Parcial 2026 (P10)", "Foto Manuscrita (P5)", "1° Parcial 08/07/2024"]
    },
    {
        "id": 20,
        "title": "Hormigón Pretensado: Características, Componentes y Efecto que Busca",
        "primary_q": "Describa las características del hormigón pretensado y qué efecto busca",
        "regex": r'hormig[oó]n pretensado|componentes del hormig[oó]n pretensado|efecto busca.*pretensado',
        "code_hint": "UT08-41",
        "slides": [13, 14],
        "manual_occurrences": ["Recuperatorio 1°P 09/12/2024", "Foto Manuscrita (P6)"]
    },
    {
        "id": 21,
        "title": "Métodos No Cuantitativos de Distribución y Metodología SLP de Muther en sus 4 Etapas",
        "primary_q": "¿Cuáles son los métodos no cuantitativos de distribución y qué recomienda el método SLP de Muther?",
        "regex": r'm[eé]todos no cuantitativos|slp de muther|cuatro etapas.*muther|metodolog[ií]a recomienda aplicar',
        "code_hint": "UT0910",
        "slides": [12, 13, 14, 15],
        "manual_occurrences": ["1° Parcial 2026 (P2)", "Foto Manuscrita (P7)", "1° Parcial Fotos"]
    },
    {
        "id": 22,
        "title": "Factores de Distribución en Planta (Concepto y los 8 Factores de Muther / Tompkins)",
        "primary_q": "¿Cómo definiría los factores de distribución de planta? Indique al menos cuatro de estos factores",
        "regex": r'factores de distribuci[oó]n|factores que influyen en la distribuci|ocho factores',
        "code_hint": "UT0910",
        "slides": [5],
        "manual_occurrences": ["Foto Manuscrita (P8)", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 23,
        "title": "Consumo de Energía en Edificios Industriales: Distribución y Fuentes",
        "primary_q": "¿De dónde sale y cómo se distribuye el consumo de energía en los edificios industriales?",
        "regex": r'consumo de energ[ií]a.*edificio|aspecto ambiental m[aá]s relevante|distribuci[oó]n.*energ[ií]a.*edificio',
        "code_hint": "UT08-41",
        "slides": [33, 34],
        "manual_occurrences": ["1° Parcial 2026 (P3)", "1° Parcial Fotos"]
    },
    {
        "id": 24,
        "title": "Pasillos de Circulación en Planta y Almacenes: Características y Clasificación",
        "primary_q": "¿Qué características deben tener los pasillos de circulación y cómo se clasifican?",
        "regex": r'pasillos de circulaci[oó]n|caracter[ií]sticas de pasillos|clasificaci[oó]n.*pasillos',
        "code_hint": "UT07-04",
        "slides": [12, 13, 14],
        "manual_occurrences": ["1° Parcial 2026 (P4)", "1° Parcial Fotos"]
    },
    {
        "id": 25,
        "title": "Áreas y Zonas en el Diseño de Almacenes y Puertos de Carga y Descarga",
        "primary_q": "Además de la zona de carga y descarga propiamente dicha ¿Qué otras áreas comprende el diseño?",
        "regex": r'adem[aá]s de la zona de carga|otras [aá]reas.*comprende el dise[ñn]o|dise[ñn]o y dimensionamiento.*almac[eé]n',
        "code_hint": "UT07-04",
        "slides": [4, 5, 6],
        "manual_occurrences": ["Foto Manuscrita (P9)", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 26,
        "title": "Modelo Determinista / Abastecimiento por Lote: Premisas, Características y Costo C1",
        "primary_q": "Indique las características y premisas del modelo determinista y qué compone el costo unitario C1",
        "regex": r'modelo determinista|abastecimiento por lote|costo unitario de almacenamiento|t[eé]rmino c1',
        "code_hint": "UT07-01",
        "slides": [11, 12],
        "manual_occurrences": ["1° Parcial 09/12/2024", "Foto Manuscrita (P10)"]
    },
    {
        "id": 27,
        "title": "Unidad de Carga: Definición, Factores y Ventajas Logísticas",
        "primary_q": "Defina Unidad de Carga e indique sus principales ventajas logísticas y operativas",
        "regex": r'unidad de carga.*def[ií]nalo|definici[oó]n de unidad de carga|concepto de unidad de carga',
        "code_hint": "UT07-03",
        "slides": [3, 4, 5],
        "manual_occurrences": ["Foto Manuscrita (P11)", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 28,
        "title": "3 Métodos Básicos de Manejo de Materiales (Manual, Mecanizado y Automatizado)",
        "primary_q": "Describir los 3 métodos básicos de manejo de materiales y dar un ejemplo de cada uno",
        "regex": r'3 m[eé]todos b[aá]sicos de manejo|tres m[eé]todos.*manejo|manual, mecanizado y automatizado',
        "code_hint": "UT01-01",
        "slides": [8, 9, 10],
        "manual_occurrences": ["1° Parcial 2026 (P1)", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 29,
        "title": "Trabajo Muscular: Dinámico, Estático y Trabajo Manual Moderado",
        "primary_q": "Defina trabajo muscular estático, dinámico y moderado, indicando sus efectos en el cuerpo",
        "regex": r'trabajo muscular|trabajo est[aá]tico|trabajo din[aá]mico|trabajo moderado|trabajo manual moderado',
        "code_hint": "UT02-02",
        "slides": [4, 5, 6, 7, 11],
        "manual_occurrences": ["1° Parcial 2026 (P11)", "Foto Manuscrita (P12)", "1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025"]
    },
    {
        "id": 30,
        "title": "Administración de Supply Chain: Tipos de Riesgos y Matriz de Segmentación de Proveedores (Q / $)",
        "primary_q": "¿En qué tipos se dividen los riesgos en la cadena de suministro y cómo se segmentan los proveedores?",
        "regex": r'riesgos.*cadena de suministro|segmentaci[oó]n de proveedores|relaci[oó]n q/\$|proveedores estrat[eé]gicos',
        "code_hint": "UT07-01",
        "slides": [6, 7, 8, 9, 10],
        "manual_occurrences": ["1° Parcial 2026 (P6)", "1° Parcial Fotos", "2° Parcial 07/11/2022"]
    },
    {
        "id": 31,
        "title": "Esquema de Tareas en Almacenes: Proceso de Recepción y Despacho / Expedición",
        "primary_q": "Describa en un esquema las tareas en la actividad de recepción y de despacho de almacenes",
        "regex": r'actividad de recepci[oó]n|actividad de despacho|zona de despacho|esquema.*despacho',
        "code_hint": "UT07-02",
        "slides": [4, 5, 6, 11],
        "manual_occurrences": ["1° Parcial 2026 (P5)", "1° Parcial Fotos"]
    },
    {
        "id": 32,
        "title": "Industria 4.0 e Intralogística 4.0: Definición, Conceptos y Pilares Tecnológicos",
        "primary_q": "¿Qué es la industria 4.0 y consecuentemente la intralogística 4.0?",
        "regex": r'industria 4\.0|intralog[ií]stica 4\.0',
        "code_hint": "UT01-01",
        "slides": [3, 4, 5, 6],
        "manual_occurrences": ["Foto Manuscrita (P1)", "1° Parcial 09/12/2025", "1° Parcial Fotos"]
    },
    {
        "id": 33,
        "title": "Edificios de Hormigón Armado Prefabricado: Ventajas y Comportamiento Estructural",
        "primary_q": "Enumere las ventajas de los edificios de hormigón armado prefabricado",
        "regex": r'hormig[oó]n armado prefabricado|edificios de hormig[oó]n prefabricado|ventajas.*prefabricado',
        "code_hint": "UT08-41",
        "slides": [17],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 34,
        "title": "Normas LEED: Parámetros de Medición y Certificación Sustentable",
        "primary_q": "Las normas LEED miden una serie de parámetros de una construcción sustentable. Enumere al menos tres",
        "regex": r'normas leed|certificaci[oó]n leed|par[aá]metros.*leed',
        "code_hint": "UT08-41",
        "slides": [35, 36],
        "manual_occurrences": ["1° Parcial 26/06/2023", "1° Parcial 08/07/2024", "Recuperatorio 1°P 09/12/2024"]
    },
    {
        "id": 35,
        "title": "Patrones de Flujo Intra-Departamentales para Distribución por Procesos",
        "primary_q": "Indique los patrones de flujos intra departamentos para una distribución por procesos",
        "regex": r'flujos intra departamentos|patrones de flujo intra|flujo en l|flujo en u',
        "code_hint": "UT0910",
        "slides": [17, 18],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 36,
        "title": "Buenas Prácticas de Almacenamiento (BPA)",
        "primary_q": "Indique al menos tres buenas prácticas de almacenamiento",
        "regex": r'buenas pr[aá]cticas de almacenamiento|bpa.*almacen',
        "code_hint": "UT07-02",
        "slides": [14, 15],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial 26/06/2023", "1° Parcial 08/07/2024"]
    },
    {
        "id": 37,
        "title": "Envases según Clasificación Europea (Primario, Secundario, Terciario) y Rígidos vs Flexibles",
        "primary_q": "Defina envase primario, secundario y terciario según la directiva europea",
        "regex": r'envase primario|envase secundario|envase terciario|clasificaci[oó]n europea.*envase|envases r[ií]gidos',
        "code_hint": "UT07-03",
        "slides": [6, 7, 8, 9, 15],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial Fotos"]
    },
    {
        "id": 38,
        "title": "Estudio de Impacto Ambiental (EsIA) y Proceso Sostenible",
        "primary_q": "¿Qué proporciona y para qué sirve un estudio de impacto ambiental?",
        "regex": r'estudio de impacto ambiental|esia|proporciona.*impacto ambiental|proceso sostenible',
        "code_hint": "UT08-21",
        "slides": [6, 7, 8],
        "manual_occurrences": ["Recuperatorio 1°P 09/12/2024", "1° Parcial Fotos"]
    },
    {
        "id": 39,
        "title": "Método de Brown & Gibson: Factores Críticos, Objetivos y Subjetivos (Parámetro W)",
        "primary_q": "En el cálculo del valor relativo de los factores subjetivos en Brown-Gibson ¿Qué representa el parámetro W?",
        "regex": r'brown.*gibson|par[aá]metro w|factores subjetivos.*brown',
        "code_hint": "UT08-11",
        "slides": [9, 10, 11],
        "manual_occurrences": ["Recuperatorio 1°P 09/12/2024", "1° Parcial Fotos"]
    },
    {
        "id": 40,
        "title": "Distribución en Planta según Relación Volumen - Variedad de Productos",
        "primary_q": "Indicar cómo es la relación volumen de producción y variedad para cada tipo básico de distribución",
        "regex": r'volumen.*variedad|posici[oó]n fija|distribuci[oó]n celular|layout.*producto',
        "code_hint": "UT0910",
        "slides": [6, 7, 8, 9, 10],
        "manual_occurrences": ["1° Parcial Fotos", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 41,
        "title": "Ventajas y Desventajas de Distribución por Proceso (Funcional) vs por Producto (Línea)",
        "primary_q": "Enumerar dos ventajas y dos desventajas de la distribución por proceso y por producto",
        "regex": r'ventajas.*distribuci[oó]n por proceso|ventajas.*distribuci[oó]n por producto',
        "code_hint": "UT0910",
        "slides": [8, 10],
        "manual_occurrences": ["1° Parcial Fotos", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 42,
        "title": "Edificios de Construcción Híbrida: Definición y Ventajas",
        "primary_q": "Enumere las ventajas de los edificios de construcción híbrida",
        "regex": r'construcci[oó]n h[ií]brida|edificios de construcci[oó]n h[ií]brida',
        "code_hint": "UT08-41",
        "slides": [19],
        "manual_occurrences": ["1° Parcial Fotos", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 43,
        "title": "Factores de Localización Internacional a partir del año 2000 (Globalización)",
        "primary_q": "Indique al menos tres factores para la localización de plantas en un contexto internacional",
        "regex": r'a[ñn]os 2000|globalizaci[oó]n.*localizaci[oó]n|contexto internacional.*plantas',
        "code_hint": "UT08-11",
        "slides": [8],
        "manual_occurrences": ["1° Parcial Fotos", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 44,
        "title": "Responsables de Obra según el Código de Edificación de CABA para Obra Mayor",
        "primary_q": "¿Cuántos responsables de obra debe haber y cuáles son sus áreas de incumbencias para obra mayor en CABA?",
        "regex": r'responsables de obra|c[oó]digo de construcci[oó]n.*caba|permiso de obra mayor',
        "code_hint": "UT08-31",
        "slides": [17, 18],
        "manual_occurrences": ["1° Parcial Fotos", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 45,
        "title": "Unión Rígida vs Unión Elástica en Estructuras de Edificios Industriales",
        "primary_q": "Indicar la definición de unión rígida y de unión elástica",
        "regex": r'uni[oó]n r[ií]gida|uni[oó]n el[aá]stica|v[ií]nculo r[ií]gido',
        "code_hint": "UT08-41",
        "slides": [22],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial Fotos"]
    },
    {
        "id": 46,
        "title": "Principio de Distribución en Planta para la Integración de Conjunto",
        "primary_q": "Indicar el principio de distribución en planta para la integración de conjunto",
        "regex": r'integraci[oó]n de conjunto|principio.*integraci[oó]n',
        "code_hint": "UT0910",
        "slides": [4],
        "manual_occurrences": ["1° Parcial 13/06/2022", "1° Parcial Fotos"]
    },
    {
        "id": 47,
        "title": "Material a Granel: Características Primarias, Secundarias y Factores del Ángulo de Reposo",
        "primary_q": "Para un material a granel: características primarias, secundarias y factores del ángulo de reposo",
        "regex": r'material a granel|[aá]ngulo de reposo|caracter[ií]sticas primarias.*granel|escurrimiento.*granel',
        "code_hint": "UT02-01",
        "slides": [17, 18, 20, 21, 22],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "Parcial 12 Preguntas"]
    },
    {
        "id": 48,
        "title": "Número Mesh: Definición, Determinación y Relación con el Tamaño de Grano",
        "primary_q": "Defina número Mesh e indique cómo se determina y qué relación tiene con el tamaño de grano",
        "regex": r'n[uú]mero mesh|mesh.*grano|apertura de la malla mesh',
        "code_hint": "UT02-01",
        "slides": [23, 24, 25],
        "manual_occurrences": ["Recuperatorio 1°P 09/12/2025", "2° Parcial 07/11/2022", "2° Parcial 06/11/2023"]
    },
    {
        "id": 49,
        "title": "Transportadores Aéreos Power vs Power & Free: Sustentación, Troleys y Pasos",
        "primary_q": "Indicar diferencias de perfiles de sustentación, troleys y pasos en transportadores Power y Power & Free",
        "regex": r'power & free|power y power & free|troleys.*a[eé]reo|paso de la cadena armada',
        "code_hint": "Resumen_BR3",
        "slides": [40, 41, 42, 43],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "2° Parcial 07/11/2022"]
    },
    {
        "id": 50,
        "title": "Cables de Acero: Alma (Tipos y Función) y Factor de Relleno",
        "primary_q": "¿A qué se denomina alma en un cable de acero y qué es el factor de relleno?",
        "regex": r'cable de acero|alma.*cable|factor de relleno.*cable',
        "code_hint": "Resumen_BR3",
        "slides": [35, 36, 37],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "Recuperatorio 2°P 16/12/2024"]
    },
    {
        "id": 51,
        "title": "Tuberías y Cañerías: Número Schedule (SCH), Fórmula ASME y Tipos de Extremos",
        "primary_q": "Defina el N° SCH, fórmula ASME de espesor de pared y tipos de extremos de un tubo",
        "regex": r'schedule|sch|f[oó]rmula asme.*espesor|extremos de un tubo',
        "code_hint": "Resumen_BR3",
        "slides": [48, 49, 50, 51],
        "manual_occurrences": ["1° Parcial 07/07/2025", "2° Parcial 06/11/2023", "Parcial 12 Preguntas"]
    },
    {
        "id": 52,
        "title": "Válvulas: Clasificación y Regulación de Flujos (Esclusa, Globo, Aguja, Mariposa)",
        "primary_q": "¿Cómo se clasifican las válvulas y cuáles son aptas para regulación de flujo?",
        "regex": r'v[aá]lvulas|esclusa.*globo|regular flujos.*v[aá]lvula',
        "code_hint": "Resumen_BR3",
        "slides": [52, 53],
        "manual_occurrences": ["1° Parcial 07/07/2025", "2° Parcial 07/11/2022"]
    },
    {
        "id": 53,
        "title": "Sistemas de Almacenamiento por Bloques: Drive, Push-Back, Dinámicas y Pallet Shuttle",
        "primary_q": "Describa el funcionamiento de estanterías en bloque: Push-Back, Drive, Dinámicas y Pallet Shuttle",
        "regex": r'push-back|push back|drive-in|pallet shuttle|estanter[ií]as din[aá]micas|doble profundidad',
        "code_hint": "UT07-05",
        "slides": [4, 5, 6, 7, 8, 9, 10, 11],
        "manual_occurrences": ["2° Parcial 06/11/2023", "Recuperatorio 2°P 16/12/2024"]
    },
    {
        "id": 54,
        "title": "Sistemas de Transporte por Colchón de Aire: Fuerza de Sustentación y Sección de Fuga",
        "primary_q": "Defina la fuerza de sustentación y sección de fuga en un sistema de colchón de aire",
        "regex": r'colch[oó]n de aire|fuerza de sustentaci[oó]n.*aire|secci[oó]n de fuga',
        "code_hint": "Resumen_BR3",
        "slides": [45, 46],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "2° Parcial 06/11/2023"]
    },
    {
        "id": 55,
        "title": "Cintas y Bandas Transportadoras: Estaciones Superiores, Componentes y Elementos de Limpieza",
        "primary_q": "Indique las estaciones superiores, componentes y elementos de limpieza de una banda transportadora",
        "regex": r'banda transportadora|cinta transportadora|estaciones superiores.*cinta|rascador primario',
        "code_hint": "Resumen_BR3",
        "slides": [22, 23, 24, 25, 26],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "2° Parcial 07/11/2022", "2° Parcial 06/11/2023"]
    },
    {
        "id": 56,
        "title": "Elevadores de Cangilones: Clasificación y Tipos de Descarga (Gravedad Libre vs Gravedad Dirigida)",
        "primary_q": "En un elevador por cangilones continuo indique la diferencia entre descarga por gravedad libre y dirigida",
        "regex": r'cangilones|elevador.*cangilones|gravedad libre.*gravedad dirigida',
        "code_hint": "Resumen_BR3",
        "slides": [30, 31, 32],
        "manual_occurrences": ["Recuperatorio 1°P 09/12/2025", "Recuperatorio 2°P 16/12/2024", "Parcial 12 Preguntas"]
    },
    {
        "id": 57,
        "title": "Gestión de Residuos Peligrosos, Patogénicos, Aguas Residuales y Radiaciones",
        "primary_q": "Plan de Contingencia de residuos peligrosos, residuos patogénicos, aguas residuales y radiaciones",
        "regex": r'residuos peligrosos|residuos patog[eé]nicos|aguas residuales|radiaciones ionizantes',
        "code_hint": "UT08-21",
        "slides": [35, 36, 40, 41, 44, 45],
        "manual_occurrences": ["1° Parcial 07/07/2025", "Recuperatorio 1°P 09/12/2025", "Recuperatorio 2°P 16/12/2024"]
    },
    {
        "id": 58,
        "title": "Tornillos de Alta Resistencia: Inscripción 10.9, Tensión y Torque en Uniones Abulonadas",
        "primary_q": "Indique la resistencia de un tornillo 10.9 y cómo se ajusta una unión rígida sin torquímetro",
        "regex": r'10\.9|inscripci[oó]n.*10\.9|torque y tensi[oó]n|giro de tuerca',
        "code_hint": "UT08-41",
        "slides": [22, 23],
        "manual_occurrences": ["1° Parcial Fotos Tema 3", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 59,
        "title": "Vigas de Repartición: Anclaje Soldado vs Abulonado y Verificación Mecánica",
        "primary_q": "Ventajas y desventajas de vigas de repartición soldados vs abulonados para colgado de cargas",
        "regex": r'vigas de repartici[oó]n|perfiles ipn.*colgar|soldados.*abulonados',
        "code_hint": "UT08-41",
        "slides": [21, 22],
        "manual_occurrences": ["1° Parcial Fotos Tema 3", "Práctico Vigas de Repartición"]
    },
    {
        "id": 60,
        "title": "Método de Cribado para Localización de Plantas y Objetivos de Parques Industriales",
        "primary_q": "Pasos del Método de Cribado para localización y objetivos de los Parques Industriales",
        "regex": r'm[eé]todo de cribado|cribado.*localizaci[oó]n|parques industriales',
        "code_hint": "UT08-11",
        "slides": [6, 7],
        "manual_occurrences": ["1° Parcial Fotos Tema 3", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 61,
        "title": "Método CRAFT y Método de Adyacencias para Optimización de Layout",
        "primary_q": "Bases de cálculo del Método CRAFT y funcionamiento del Método de Adyacencias",
        "regex": r'm[eé]todo craft|m[eé]todo de adyacencias|intercambio de pares.*craft',
        "code_hint": "UT0910",
        "slides": [25, 26, 27],
        "manual_occurrences": ["1° Parcial Fotos Tema 3", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 62,
        "title": "Terminales Portuarias (Terminal Polivalente y Buques Petroleros)",
        "primary_q": "¿Qué tipo de carga maneja una terminal portuaria polivalente y qué tipos hay para petroleros?",
        "regex": r'terminal portuaria|puertos.*petroleros|monoboya|polivalente.*portuaria',
        "code_hint": "Resumen_BR3",
        "slides": [60, 61],
        "manual_occurrences": ["2° Parcial 06/11/2023", "Recuperatorio 2°P 16/12/2024"]
    },
    {
        "id": 63,
        "title": "Picking en Estanterías de Pequeñas Piezas (Hombre a Producto vs Producto a Hombre)",
        "primary_q": "Procesos de picking en estanterías de pequeñas piezas (mini-loads, carruseles, pick to light)",
        "regex": r'picking en las estanter[ií]as|peque[ñn]as piezas|hombre a producto|producto a hombre',
        "code_hint": "UT07-02",
        "slides": [8, 9, 10],
        "manual_occurrences": ["2° Parcial 06/11/2023"]
    },
    {
        "id": 64,
        "title": "Contaminantes Atmosféricos: Primarios vs Secundarios y Clases",
        "primary_q": "¿Cómo se clasifican los contaminantes atmosféricos? Indicar ejemplos de cada clase",
        "regex": r'contaminantes atmosf[eé]ricos|primarios y secundarios.*aire|emisiones.*atmosf[eé]ricas',
        "code_hint": "UT08-21",
        "slides": [46, 47],
        "manual_occurrences": ["2° Parcial 07/11/2022", "2° Parcial 06/11/2023"]
    },
    {
        "id": 65,
        "title": "Transportador de Piso Flat Top Liviano y Transportadores a Rodillos (Motor vs Cadena)",
        "primary_q": "Transportador Flat Top liviano y diferencia entre rodillo motorizado y accionado a cadena",
        "regex": r'flat top liviano|transportadores a rodillos|rodillo impulsado a motor|rodillo accionado a cadena',
        "code_hint": "Resumen_BR3",
        "slides": [15, 16, 17],
        "manual_occurrences": ["2° Parcial 07/11/2022", "Recuperatorio 2°P 16/12/2024"]
    },
    {
        "id": 66,
        "title": "Techos Flotantes en Tanques de Almacenamiento de Hidrocarburos",
        "primary_q": "¿Cuáles son los dos tipos de techos flotantes en los tanques de hidrocarburos?",
        "regex": r'techos flotantes|tanques de almacenamiento.*hidrocarburos|techo flotante interno',
        "code_hint": "Resumen_BR3",
        "slides": [57, 58],
        "manual_occurrences": ["2° Parcial 07/11/2022"]
    },
    {
        "id": 67,
        "title": "Permisos de Volcado de Efluentes en CABA y Provincia de Buenos Aires",
        "primary_q": "Autoridades para solicitar permisos de volcado de efluentes cloacales y pluviales en CABA y PBA",
        "regex": r'permiso de volcado|volcado de efluentes|aysa.*acumar|ada.*ina',
        "code_hint": "UT08-21",
        "slides": [37, 38],
        "manual_occurrences": ["Finales Grimolizzi 2024-2026", "Respuestas-MMyDP-Final"]
    },
    {
        "id": 68,
        "title": "Transelevadores vs Elevadores Trilaterales en Almacenes de Alta Densidad",
        "primary_q": "Indique al menos dos diferencias entre un transelevador (AS/RS) y un elevador trilateral",
        "regex": r'transelevador|elevador trilateral|carretilla trilateral',
        "code_hint": "UT07-05",
        "slides": [12, 13],
        "manual_occurrences": ["2° Parcial 06/11/2023", "Finales Grimolizzi"]
    },
    {
        "id": 69,
        "title": "Cross Docking: Tipos (Directo / Predistribuido vs Con Preclasificación)",
        "primary_q": "Clasificación de sistemas Cross Docking según la actividad realizada en el almacén",
        "regex": r'cross docking|cross-docking|predistribuido|preclasificaci[oó]n',
        "code_hint": "UT07-05",
        "slides": [3],
        "manual_occurrences": ["2p_apuntes_manejo", "Finales Grimolizzi"]
    },
    {
        "id": 70,
        "title": "Unidad Equivalente de Traslado en la Medición de Flujos",
        "primary_q": "En la medición de flujos se hace en términos de unidades equivalentes de traslado. ¿Cuál es su significado?",
        "regex": r'unidades equivalentes de traslado|unidad equivalente.*flujo',
        "code_hint": "UT0910",
        "slides": [16],
        "manual_occurrences": ["1° Parcial Fotos Tema 1", "Preguntas-1P-Manejo-LC"]
    },
    {
        "id": 71,
        "title": "Buque Interoceánico: Desglose de Costos de Viaje (Cargas Portuarias, Combustible y Tripulación)",
        "primary_q": "El armado de un buque interoceánico es U$D 450.000 ¿Qué rubros componen dicho costo?",
        "regex": r'buque interoce[aá]nico|450\.000|cargas portuarias, combustible',
        "code_hint": "Resumen_BR3",
        "slides": [62],
        "manual_occurrences": ["2° Parcial 07/11/2022"]
    },
    {
        "id": 72,
        "title": "Transpaletas y Autoelevadores: Clasificación y Principio de Estabilidad (Triángulo de Estabilidad)",
        "primary_q": "Clasificación de autoelevadores y principio del triángulo de estabilidad",
        "regex": r'autoelevador|tri[aá]ngulo de estabilidad|transpaleta|carretilla elevadora',
        "code_hint": "Resumen_BR3",
        "slides": [4, 5, 6],
        "manual_occurrences": ["Finales Grimolizzi", "Respuestas-MMyDP-Final"]
    },
    {
        "id": 73,
        "title": "Grúas Puente y Polipastos: Componentes y Tipos de Mecanismos",
        "primary_q": "Componentes principales de una grúa puente industrial y tipos de polipastos",
        "regex": r'gr[uú]a puente|polipasto|carro de traslaci[oó]n',
        "code_hint": "Resumen_BR3",
        "slides": [8, 9, 10],
        "manual_occurrences": ["Finales Grimolizzi", "Respuestas-MMyDP-Final"]
    },
    {
        "id": 74,
        "title": "Transportadores Neumáticos: Fase Densa vs Fase Diluida",
        "primary_q": "Diferencias operativas entre transporte neumático en fase densa y fase diluida",
        "regex": r'transporte neum[aá]tico|fase densa|fase diluida',
        "code_hint": "Resumen_BR3",
        "slides": [28, 29],
        "manual_occurrences": ["Finales Grimolizzi", "Respuestas-MMyDP-Final"]
    },
    {
        "id": 75,
        "title": "Transportadores de Tornillo Helicoidal / Sinfín: Capacidad y Aplicaciones",
        "primary_q": "Transportador de tornillo sinfín (hélice): diseño, paso y capacidad de transporte",
        "regex": r'tornillo sinf[ií]n|transportador helicoidal|h[eé]lice.*transporte',
        "code_hint": "Resumen_BR3",
        "slides": [33, 34],
        "manual_occurrences": ["Finales Grimolizzi", "Respuestas-MMyDP-Final"]
    }
]

# Calculate total occurrences for each topic by scanning raw_questions
processed_all = []

for t in topics:
    matched_occs = list(t.get('manual_occurrences', []))
    reg = re.compile(t['regex'], re.IGNORECASE)
    
    for q in raw_questions:
        if reg.search(q['text']):
            src_clean = os.path.basename(q['source'])
            desc = f"{src_clean}: {q['text'][:70]}..."
            if desc not in matched_occs:
                matched_occs.append(desc)
    
    # Slides verbatim
    code = t['code_hint']
    slides = t['slides']
    if len(slides) == 1:
        v = get_slide_text(code, slides[0])
    else:
        v = get_multiple_slides_text(code, slides)
    
    if not v or not v['text']:
        v = {'file': code, 'unit': 'Oficial', 'slide_no': str(slides), 'text': '[Texto en procesamiento]'}
    
    processed_all.append({
        'id': t['id'],
        'title': t['title'],
        'question_primary': t['primary_q'],
        'variants': [t['primary_q']] + [m for m in matched_occs if not m.endswith('...')][:4],
        'frequency_count': len(matched_occs),
        'occurrences': matched_occs[:12], # top occurrences list
        'file': v['file'],
        'unit': v['unit'],
        'slide_no': v['slide_no'],
        'verbatim_text': v['text']
    })

# Sort strictly by frequency descending
processed_all.sort(key=lambda x: x['frequency_count'], reverse=True)

# Assign rank
for idx, it in enumerate(processed_all):
    it['rank'] = idx + 1

print(f"Exhaustive database built with {len(processed_all)} topics!")
print("Top 10 highest frequency:")
for it in processed_all[:10]:
    print(f"  #{it['rank']} [Freq: {it['frequency_count']}] {it['title']}")

with open('master_catalog_exhaustive.json', 'w', encoding='utf-8') as out:
    json.dump(processed_all, out, ensure_ascii=False, indent=2)
