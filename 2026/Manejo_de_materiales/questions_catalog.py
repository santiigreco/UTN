import json
import os
import re
import sys
import html

# Load extracted slides
with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

def get_verbatim(filename_part, slide_num):
    for fname, fdata in slides_data.items():
        if filename_part.lower() in fname.lower():
            for s in fdata['slides']:
                if s['slide_no'] == slide_num:
                    return {
                        'file': fname,
                        'unit': fdata['unit'],
                        'slide_no': slide_num,
                        'text': s['text'].strip()
                    }
    return None

def get_multiple_slides_verbatim(filename_part, slide_nums):
    texts = []
    unit = ""
    full_fname = ""
    for snum in slide_nums:
        v = get_verbatim(filename_part, snum)
        if v:
            unit = v['unit']
            full_fname = v['file']
            texts.append(f"--- Diapositiva {snum} ---\n" + v['text'])
    return {
        'file': full_fname,
        'unit': unit,
        'slide_no': ", ".join(map(str, slide_nums)),
        'text': "\n\n".join(texts)
    }

# Complete structured list of exam questions with exact frequency analysis and slide mapping
questions_db = [
    {
        "id": 1,
        "title": "Área de Mixtura de Usos en CABA: Definición y Aplicación",
        "question_variants": [
            "¿Qué define el área de mixtura según el Código Urbanístico de CABA? Indique ejemplos",
            "En CABA, ¿qué define el área de Mixtura y dónde se aplica?",
            "Definir mixtura de usos según el Código Urbanístico de CABA e indicar ejemplos."
        ],
        "occurrences": [
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "1° Parcial Fotos Tema 1 y Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3, 7)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 4, 12)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026 (Exámenes 2024/2025)"
        ],
        "file_hint": "Codigos Urbanisticos",
        "slides": [13, 14]
    },
    {
        "id": 2,
        "title": "Principio de Estandarización del Material Handling Institute (MHI)",
        "question_variants": [
            "Enuncie el Principio de Estandarización de acuerdo con lo desarrollado por el Material Handling Institute, e indique al menos dos puntos clave de este.",
            "Principio de Estandarización MHI: definición y puntos clave."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 1, 6)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 2, 8)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 2)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Introducci",
        "slides": [18]
    },
    {
        "id": 3,
        "title": "Nivel de Complejidad Ambiental (NCA): Utilidad, Parámetros y Rangos / Categorías",
        "question_variants": [
            "¿Para qué se utiliza el Nivel de Complejidad Ambiental? E indique además los rangos que este define.",
            "NCA: ¿Para qué sirve, cómo se calcula y cuáles son las 3 categorías de industrias?",
            "Fórmula polinómica del NCA y categorización de industrias (1°, 2° y 3° categoría)."
        ],
        "occurrences": [
            "1° Parcial 26/06/2023 - Tema 1",
            "1° Parcial 08/07/2024 - Tema 1",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 9)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 5, 14)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 7)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Gestion Ambiental",
        "slides": [22, 23, 24]
    },
    {
        "id": 4,
        "title": "Definición y Objetivos de la Planeación de Instalaciones",
        "question_variants": [
            "Defina Planeación de Instalaciones e indique al menos cuatro de tareas / objetivos que realiza.",
            "Indique al menos cuatro objetivos de la Planeación de Instalaciones.",
            "¿Cuáles son las etapas que definen la Planeación de Instalaciones y qué comprende cada una de ellas?"
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 1, 5)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 1, 7)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 1)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Tompkins",
        "slides": [2, 6, 7]
    },
    {
        "id": 5,
        "title": "Clasificación del Uso del Suelo en la Provincia de Buenos Aires (Decreto Ley 8912/77)",
        "question_variants": [
            "La clasificación del uso del suelo en la PBA define áreas y zonas, indique los tipos de zonas que define esta clasificación.",
            "Clasificación del suelo en PBA: Áreas (Urbana, Rural, Complementaria) y Zonas (Residencial, Comercial, Industrial, etc.)."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3, 8)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 4, 11)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Codigos Urbanisticos",
        "slides": [4, 5, 6]
    },
    {
        "id": 6,
        "title": "Localización de Centros de Servicios (Consumo In Situ vs Directo a Domicilio)",
        "question_variants": [
            "Para el estudio de la localización de centros de servicios se dividen en dos clases principales. Indicar cuáles son y describir los factores característicos de cada una de ellas.",
            "Localización de servicios: Servicios que se consumen in situ vs Servicios prestados directamente al cliente."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 7)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 10)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 4)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Localizaci",
        "slides": [13, 14]
    },
    {
        "id": 7,
        "title": "Edificios de Hormigón Armado Prefabricado: Ventajas y Características",
        "question_variants": [
            "Enumere las ventajas de los edificios de hormigón armado prefabricado.",
            "Ventajas de los edificios industriales prefabricados de hormigón armado."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 10)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 15)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 8)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Edificios Industriales",
        "slides": [17]
    },
    {
        "id": 8,
        "title": "Normas LEED (Liderazgo en Energía y Diseño Ambiental): Parámetros y Certificación",
        "question_variants": [
            "Las normas LEED miden y monitorean una serie de parámetros de una construcción sustentable. Enumere al menos tres de estos parámetros.",
            "Indique cuáles son los aspectos que evalúa y certifica la norma LEED en edificios sustentables."
        ],
        "occurrences": [
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 11)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 16)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 9)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Edificios Industriales",
        "slides": [35, 36]
    },
    {
        "id": 9,
        "title": "Gráfica de Relación de Actividades / Carta Muthed (SLP de Richard Muther)",
        "question_variants": [
            "Para la siguiente gráfica de relación de actividades, Indique qué representan: X1, X2, A y 1.",
            "Para el análisis de relación de actividades en la distribución de plantas, explique el código de proximidad (A, E, I, O, U, X) y las razones numéricas.",
            "¿Qué significa A, E, I, O, U, X en una tabla de relaciones de Richards Muther?"
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial Tema 1 y Tema 2 Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 12)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 18)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 10)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Distribucio",
        "slides": [22, 23, 24]
    },
    {
        "id": 10,
        "title": "Patrones de Flujo Intra-Departamentales para Distribución por Procesos",
        "question_variants": [
            "Indique los patrones de flujos intra departamentos, para una distribución de este por procesos.",
            "Flujo intra departamental en distribución funcional: flujo directo, en L, en U, circular, en S.",
            "Patrones de flujo de materiales dentro de un departamento."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 13)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 19)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 11)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Distribucio",
        "slides": [17, 18]
    },
    {
        "id": 11,
        "title": "Buenas Prácticas de Almacenamiento (BPA / Good Storage Practices)",
        "question_variants": [
            "Indique al menos tres buenas prácticas de almacenamiento.",
            "Enumere buenas prácticas en la gestión y operación de depósitos y almacenes."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6, 14)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 8, 20)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 12)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Operaci",
        "slides": [14, 15]
    },
    {
        "id": 12,
        "title": "Estructura de un Piso Industrial: Subrasante, Sub-base, Base y Capa de Rodadura",
        "question_variants": [
            "Para un piso industrial ¿Cómo está conformado el subrasante?",
            "Para un piso industrial ¿Cómo está conformada la base y la sub base?",
            "Capas que componen un piso o pavimento industrial de hormigón."
        ],
        "occurrences": [
            "1° Parcial 08/07/2024 - Tema 1 y 2",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 11)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 17)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 9)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Edificios Industriales",
        "slides": [24, 25, 26]
    },
    {
        "id": 13,
        "title": "Tipos de Envolventes y Envases según Clasificación Europea: Primario, Secundario y Terciario",
        "question_variants": [
            "Defina envase terciario según la clasificación europea.",
            "Defina envase secundario según la clasificación europea.",
            "Defina envase primario, secundario y terciario según la normativa de empaque.",
            "Defina los envases rígidos y los flexibles."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6, 15)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 8, 22)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 13)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Unidades de Carga",
        "slides": [6, 7, 8, 9]
    },
    {
        "id": 14,
        "title": "Estudio de Impacto Ambiental (EsIA): Concepto, Para qué sirve y Qué proporciona",
        "question_variants": [
            "¿Qué proporciona y para qué sirve un estudio de impacto ambiental?",
            "¿Qué entiende por Impacto Ambiental?",
            "Defina Proceso Sostenible / Gestión Sustentable e Impacto Ambiental."
        ],
        "occurrences": [
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 3",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3, 9)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 5, 13)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 7)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Gestion Ambiental",
        "slides": [6, 7, 8]
    },
    {
        "id": 15,
        "title": "Método de Brown & Gibson para Localización de Plantas (Parámetro W y Factores)",
        "question_variants": [
            "En el cálculo del valor relativo de los factores subjetivos en el método de Brown Gibson ¿Qué representa el parámetro W?",
            "Describa brevemente cómo funcionan (conceptual) cada uno de los modelos cuantitativos para la toma de decisión en la localización de planta.",
            "Método de Brown-Gibson: Factores Críticos, Factores Objetivos y Factores Subjetivos (W y K)."
        ],
        "occurrences": [
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 7)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 9)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 4)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Localizaci",
        "slides": [9, 10, 11]
    },
    {
        "id": 16,
        "title": "Esquema de Tareas en Almacenes: Proceso de Recepción y Proceso de Despacho / Expedición",
        "question_variants": [
            "Describa en un esquema las tareas que se realizan en la actividad de recepción de almacenes.",
            "Describa en un esquema las tareas que se realizan en la actividad de despacho de almacenes.",
            "Flujo operativo y tareas principales en Recepción y Expedición de un almacén."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "1° Parcial Fotos Tema 3",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6, 14)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 8, 21)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 12)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Operaci",
        "slides": [4, 5, 6, 11]
    },
    {
        "id": 17,
        "title": "Distribución en Planta según Relación Volumen - Variedad de Productos",
        "question_variants": [
            "Indicar como es esta relación volumen de producción y la variedad de productos para cada uno de los tipos básicos de distribución en planta.",
            "Tipos básicos de Layout (Posición Fija, Funcional/Proceso, Celular, Línea/Producto) en función del Volumen y la Variedad.",
            "Explicar en qué consiste la llamada Distribución por Posición Fija y en qué casos/actividades se aconseja/recomienda su utilización."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "1° Parcial Fotos Tema 3",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 12)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 18)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 10)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Distribucio",
        "slides": [6, 7, 8, 9, 10]
    },
    {
        "id": 18,
        "title": "Ventajas y Desventajas de la Distribución por Proceso (Funcional) y por Producto (Línea)",
        "question_variants": [
            "Enumerar dos ventajas y dos desventajas de la distribución por proceso.",
            "Enumerar dos ventajas y dos desventajas de la distribución por producto.",
            "Comparativa de ventajas y desventajas entre Layout Funcional y Layout en Línea."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 13)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 19)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 11)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Distribucio",
        "slides": [8, 10]
    },
    {
        "id": 19,
        "title": "Edificios de Construcción Híbrida: Definición y Ventajas",
        "question_variants": [
            "Enumere las ventajas de los edificios de construcción híbrida.",
            "¿Qué es un edificio industrial híbrido y cuáles son sus ventajas operativas y constructivas?"
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 10)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 16)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 8)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Edificios Industriales",
        "slides": [19]
    },
    {
        "id": 20,
        "title": "Factores de Localización Internacional a partir del año 2000 (Globalización)",
        "question_variants": [
            "En los años 2000 con la globalización, se introdujeron factores para la localización de plantas para el análisis en un contexto internacional. Indique al menos tres de estos factores.",
            "Factores de macro-localización global / internacional post-año 2000."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 7)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 9)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 4)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Localizaci",
        "slides": [8]
    },
    {
        "id": 21,
        "title": "Factores Críticos para la Localización de Centros Comerciales y Locales Minoristas",
        "question_variants": [
            "Enumere al menos cuatro factores críticos para la localización de centros comerciales y locales minoristas.",
            "Localización de locales comerciales y retail: factores determinantes."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 8)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 10)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Localizaci",
        "slides": [15]
    },
    {
        "id": 22,
        "title": "Responsables de Obra según el Código de Edificación de CABA",
        "question_variants": [
            "De acuerdo con el código de construcción de CABA ¿Cuántos responsables de obra debe haber y cuáles son sus áreas de incumbencias para un permiso de obra mayor?",
            "Responsables de obra en CABA para obra mayor: Proyectista, Director de Obra, Constructor, etc."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3, 8)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 4, 12)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Codigos Urbanisticos",
        "slides": [17, 18]
    },
    {
        "id": 23,
        "title": "Unión Rígida vs Unión Elástica en Estructuras de Edificios Industriales",
        "question_variants": [
            "Indicar la definición de unión rígida.",
            "Indicar la definición de unión elástica.",
            "Diferencias entre vínculos rígidos y elásticos en naves industriales."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 10)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 15)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 8)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Edificios Industriales",
        "slides": [22]
    },
    {
        "id": 24,
        "title": "Principio de Distribución en Planta de Integración de Conjunto",
        "question_variants": [
            "Indicar el principio de distribución en planta para la integración de conjunto.",
            "Principios de Distribución en Planta: Integración de Conjunto, Mínima Distancia, Circulación, Espacio Cúbico, Flexibilidad, Satisfacción y Seguridad."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 12)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 17)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 10)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Distribucio",
        "slides": [4]
    },
    {
        "id": 25,
        "title": "Trabajo Muscular: Estático vs Dinámico y Trabajo Moderado",
        "question_variants": [
            "Defina trabajo muscular estático y dinámico ¿Cuáles son las diferencias entre ellos?",
            "Defina Trabajo Moderado en función del gasto de energía, de un ejemplo e indique los efectos en el cuerpo humano.",
            "La realización de todo tipo de trabajo manual implica la ejecución de un Trabajo Muscular: clasificación y efectos."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 07/11/2022 - Tema 1",
            "Parcial 12 Preguntas Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 2)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Manejo manual de cargas",
        "slides": [4, 5, 6, 7, 11]
    },
    {
        "id": 26,
        "title": "Material a Granel: Características Primarias, Secundarias y Factores del Ángulo de Reposo",
        "question_variants": [
            "Para un material a granel ¿a qué corresponden las características primarias y secundarias? Indique cada una de las características primarias y secundarias.",
            "El ángulo de reposo de un material a granel, ¿Hasta cuántos grados puede variar? ¿Cuáles son los cinco factores que provocan esta variación?",
            "Para un material a granel defina escurrimiento y enumere los tipos de escurrimientos que hay."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "Parcial 12 Preguntas Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 2, 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Material a mover",
        "slides": [17, 18, 20, 21, 22]
    },
    {
        "id": 27,
        "title": "Número Mesh: Definición, Determinación y Relación con el Tamaño de Grano",
        "question_variants": [
            "Defina número Mesh e indique cómo se determina. Además, dados dos materiales a granel, A y B cuyos números Mesh son A > B. Indicar cuál de los materiales tiene mayor tamaño de grano.",
            "Determinar el diámetro del alambre de una malla Mesh 6, siendo la apertura de la malla 3,36mm.",
            "Defina el número Mesh y qué implica un número Mesh elevado respecto al tamaño de grano."
        ],
        "occurrences": [
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 07/11/2022 - Tema 1",
            "2° Parcial 06/11/2023 - Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Material a mover",
        "slides": [23, 24, 25]
    },
    {
        "id": 28,
        "title": "Transportadores Aéreos Power vs Power & Free: Componentes, Troleys y Pasos",
        "question_variants": [
            "Dos de los elementos más importantes en diseño estructural de los transportadores aéreos Power y Power & Free son el perfil de sustentación. Indicar las diferencias que existen en estos elementos entre estos transportadores y esquematizar ambos perfiles.",
            "Indique y describa los troleys utilizados en un sistema de transporte aéreo Power & Free.",
            "En un sistema aéreo del tipo Power se definen varios pasos. Indicar y describir cada uno de ellos (paso de cadena armada y paso del transporte)."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 07/11/2022 - Tema 1",
            "Parcial 12 Preguntas Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [40, 41, 42, 43]
    },
    {
        "id": 29,
        "title": "Cables de Acero: Alma (Tipos y Función) y Factor de Relleno",
        "question_variants": [
            "A qué se denomina alma en un cable de acero y cuántos tipos de estas se utilizan en la construcción de los cables.",
            "Defina factor de relleno de un cable de acero.",
            "Componentes de un cable de acero: alambre, cordón, alma, paso y factor de relleno."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Parcial 12 Preguntas Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [35, 36, 37]
    },
    {
        "id": 30,
        "title": "Tuberías y Cañerías: Número Schedule (SCH), Fórmula ASME y Tipos de Extremos",
        "question_variants": [
            "Defina el N° SCH y escriba la fórmula de cálculo / ¿Cuáles son los parámetros que intervienen en su cálculo?",
            "Indique el significado de cada uno de los parámetros que intervienen en el cálculo del espesor de pared de un caño, según la fórmula ASME.",
            "Indique cada uno de los diferentes extremos de un tubo y el uso más común de estos tipos de extremos."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "2° Parcial 06/11/2023 - Tema 1",
            "Parcial 12 Preguntas Fotos",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [48, 49, 50, 51]
    },
    {
        "id": 31,
        "title": "Válvulas: Clasificación y Regulación de Flujos",
        "question_variants": [
            "Indicar con cuáles de las siguientes válvulas se puede regular flujos: Esclusa, Globo, Aguja, Mariposa.",
            "En la conducción de fluidos ¿Cómo se clasifican las válvulas?"
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "2° Parcial 07/11/2022 - Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [52, 53]
    },
    {
        "id": 32,
        "title": "Sistemas de Almacenamiento por Bloques: Drive-In / Drive-Through, Push-Back, Dinámicas y Pallet Shuttle",
        "question_variants": [
            "Describa el funcionamiento del sistema de estanterías Push-Back y sus características logísticas.",
            "Describa las características y máquinas utilizadas para un sistema de estanterías de doble profundidad.",
            "Clasificación y funcionamiento de estanterías en bloque: Drive in, Push-back, Dinámicas a rodillos y Pallet Shuttle.",
            "Indique al menos dos diferencias entre un transelevador y un elevador trilateral."
        ],
        "occurrences": [
            "2° Parcial 06/11/2023 - Tema 1",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "2p_apuntes_manejo",
            "sistemas_almacenaje_pdf.txt",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Sistemas de Almacenaje",
        "slides": [4, 5, 6, 7, 8, 9, 10, 11]
    },
    {
        "id": 33,
        "title": "Sistemas de Transporte por Colchón de Aire: Fuerza de Sustentación y Sección de Fuga",
        "question_variants": [
            "Defina la fuerza de sustentación y la sección de fuga de un colchón de aire, indicando el significado de cada uno de los parámetros.",
            "¿Qué parámetros definen la fuerza de sustentación en un sistema de colchón de aire?"
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 06/11/2023 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [45, 46]
    },
    {
        "id": 34,
        "title": "Cintas y Bandas Transportadoras: Estaciones Superiores, Componentes y Limpieza",
        "question_variants": [
            "Indique los tipos de estaciones superiores que se utilizan en un sistema de cinta transportadoras, dando una descripción, indicando su ubicación y espaciamiento en el equipo.",
            "¿Qué Parámetros definen la selección de cada uno de los tres componentes de una banda transportadora?",
            "Indicar cuáles son los elementos de limpieza de una banda transportadora, y dónde se colocan tanto como respecto de las caras de la banda como de los tambores principal y de retorno."
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 07/11/2022 - Tema 1",
            "2° Parcial 06/11/2023 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [22, 23, 24, 25, 26]
    },
    {
        "id": 35,
        "title": "Elevadores de Cangilones: Clasificación y Tipos de Descarga",
        "question_variants": [
            "En un elevador por cangilones continuo indique la diferencia entre el sistema de descarga por gravedad libre y gravedad dirigida.",
            "Describa los diferentes tipos de Elevadores de Cangilones (espaciados, continuos, descarga centrífuga, etc.)."
        ],
        "occurrences": [
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Parcial 12 Preguntas Fotos",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [30, 31, 32]
    },
    {
        "id": 36,
        "title": "Gestión de Residuos Especiales / Peligrosos, Patogénicos y Aguas Residuales",
        "question_variants": [
            "Describa las características que debe tener un Plan de Contingencia para el almacenamiento de residuos peligrosos.",
            "Defina desperdicio, y explique la diferencia con residuo. Defina Residuos Patogénicos / de Salud.",
            "Enumere los principales contaminantes orgánicos e inorgánicos de las aguas residuales.",
            "En los residuos Radioactivos se habla de radiaciones Ionizantes y No Ionizantes ¿Cuál de estas difícilmente pueden afectar al estado natural de los seres vivos?"
        ],
        "occurrences": [
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Parcial 12 Preguntas Fotos",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Gestion Ambiental",
        "slides": [35, 36, 40, 41, 44, 45]
    },
    {
        "id": 37,
        "title": "Intralogística 4.0 e Industria 4.0: Definición y Concepto",
        "question_variants": [
            "¿Qué es la industria 4.0, y consecuentemente, la Intralogística 4.0?",
            "Indicar qué cuestiones conceptuales y puntuales hacen que el estudio de la Intralogística reemplace en la actualidad al tradicional tratado de Manejo de Materiales y Distribución en Planta."
        ],
        "occurrences": [
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "1° Parcial Fotos Tema 3",
            "Parcial 12 Preguntas Fotos",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Introducci",
        "slides": [3, 4, 5, 6]
    },
    {
        "id": 38,
        "title": "Terminales Portuarias: Terminal Polivalente y Buques Petroleros",
        "question_variants": [
            "¿Qué tipo de carga maneja una terminal portuaria polivalente?",
            "Indique los diferentes tipos de terminales portuarias para buques petroleros y descríbalas brevemente."
        ],
        "occurrences": [
            "2° Parcial 06/11/2023 - Tema 1",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Resumen_BR3",
        "slides": [60, 61]
    },
    {
        "id": 39,
        "title": "Supply Chain: Riesgos en la Cadena de Suministro y Segmentación de Proveedores",
        "question_variants": [
            "¿En qué tipos se dividen los riesgos en la administración de la cadena de suministros? Indicar al menos un ejemplo de cada tipo.",
            "En la segmentación de proveedores en la cadena de abastecimientos se utilizan como parámetros de evaluación el volumen de producto Q y el monto $. Indicar las cuatro categorías de la segmentación y cómo son la relación Q/$ en cada una de ellas."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 1",
            "2° Parcial 07/11/2022 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Supply Chain",
        "slides": [6, 7, 8, 9, 10]
    },
    {
        "id": 40,
        "title": "Planificación y Gestión de Stocks: Stock de Seguridad y Sistemas de Reposición",
        "question_variants": [
            "Defina stock de seguridad.",
            "En la planificación de materiales, indique cómo se clasifican los sistemas de reposición en función de la incertidumbre de demanda y el lead time.",
            "Indique al menos tres consideraciones a tener en cuenta en la planificación de los stocks estratégicos."
        ],
        "occurrences": [
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial Fotos Tema 1 y Tema 2",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "file_hint": "Supply Chain",
        "slides": [11, 12]
    }
]

print(f"Total structured questions configured: {len(questions_db)}")
