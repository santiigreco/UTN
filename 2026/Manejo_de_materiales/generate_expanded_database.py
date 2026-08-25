import json
import os
import re
import sys

with open('extracted_slides.json', 'r', encoding='utf-8') as f:
    slides_data = json.load(f)

# Helper function
def get_slide_text(code_hint, slide_num):
    for fname, fdata in slides_data.items():
        if code_hint.lower() in fname.lower() or code_hint.lower() in fdata['path'].lower():
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

# Complete master database with all questions
master_catalog = [
    # 1
    {
        "id": 1,
        "title": "Área de Mixtura de Usos en CABA: Definición, Clasificación y Ejemplos",
        "question_variants": [
            "¿Qué define el área de mixtura según el Código Urbanístico de CABA? Indique ejemplos",
            "En CABA, ¿qué define el área de Mixtura y dónde se aplica?",
            "Definir mixtura de usos según el Código Urbanístico de CABA e indicar ejemplos de áreas 1, 2, 3 y 4."
        ],
        "occurrences": [
            "1° Parcial 2026 (Recopilación)",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "1° Parcial Fotos Tema 1 y Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 3, 7)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 4, 12)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-31",
        "slides": [13, 14]
    },
    # 2
    {
        "id": 2,
        "title": "Gráfica de Relación de Actividades / Carta Muthed (SLP de Richard Muther)",
        "question_variants": [
            "Para la siguiente gráfica de relación de actividades, Indique qué representan: X1, X2, A y 1.",
            "Para el análisis de relación de actividades en la distribución de plantas, explique el código de proximidad (A, E, I, O, U, X) y las razones numéricas.",
            "¿Qué significa A, E, I, O, U, X en una tabla de relaciones de Richards Muther?"
        ],
        "occurrences": [
            "1° Parcial 2026",
            "1° Parcial 13/06/2022 - Tema 2",
            "1° Parcial 26/06/2023 - Tema 2",
            "1° Parcial 08/07/2024 - Tema 2",
            "1° Parcial Fotos Tema 1 y 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5, 12)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7, 18)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 10)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT0910",
        "slides": [22, 23, 24]
    },
    # 3
    {
        "id": 3,
        "title": "Nivel de Complejidad Ambiental (NCA): Utilidad, Parámetros y Categorías",
        "question_variants": [
            "¿Para qué se utiliza el Nivel de Complejidad Ambiental? E indique además los rangos que este define.",
            "NCA: ¿Para qué sirve, cómo se calcula y cuáles son las 3 categorías de industrias?",
            "Fórmula polinómica del NCA y categorización de industrias (1°, 2° y 3° categoría)."
        ],
        "occurrences": [
            "1° Parcial 2026",
            "1° Parcial 26/06/2023 - Tema 1",
            "1° Parcial 08/07/2024 - Tema 1",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 9)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 5, 14)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 7)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-21",
        "slides": [22, 23, 24]
    },
    # 4
    {
        "id": 4,
        "title": "Planeación de Instalaciones: Definición, Tareas y ¿Qué analiza, dimensiona, diseña y selecciona?",
        "question_variants": [
            "Defina Planeación de Instalaciones e indique al menos cuatro de tareas / objetivos que realiza.",
            "¿Qué analiza, dimensiona, diseña y selecciona la planeación de instalaciones?",
            "Indique al menos cuatro objetivos de la Planeación de Instalaciones.",
            "¿Cuáles son las etapas que definen la Planeación de Instalaciones y qué comprende cada una de ellas?"
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 9)",
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 1, 5)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 1, 7)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 1)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "Tompkins",
        "slides": [2, 6, 7]
    },
    # 5
    {
        "id": 5,
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
        "code_hint": "UT01-01",
        "slides": [18]
    },
    # 6
    {
        "id": 6,
        "title": "Principio de Trabajo del Material Handling Institute (MHI)",
        "question_variants": [
            "Enuncie el Principio de Trabajo de acuerdo con lo desarrollado por el MHI, e indique al menos dos puntos clave de este.",
            "Enunciar principio de trabajo MHI.",
            "Principio de Trabajo MHI: simplificar, reducir distancias y movimientos."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 7)",
            "Foto Parcial Manuscrito (Pregunta 2)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 1)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 2)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT01-01",
        "slides": [15]
    },
    # 7
    {
        "id": 7,
        "title": "Método de Alfred Weber para la Localización de Plantas: Etapas y Fundamento",
        "question_variants": [
            "Weber fue el primero en introducir el análisis sistemático para la localización de plantas, describa cada una de las etapas del método desarrollado por Weber para la localización de la planta.",
            "Etapas para localización de Weber.",
            "Modelo del Triángulo de Weber y costos de transporte."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 8)",
            "Foto Parcial Manuscrito (Pregunta 3)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-11",
        "slides": [4, 5]
    },
    # 8
    {
        "id": 8,
        "title": "Clasificación del Suelo en PBA (Decreto Ley 8912/77): Áreas y Zonas",
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
        "code_hint": "UT08-31",
        "slides": [4, 5, 6]
    },
    # 9
    {
        "id": 9,
        "title": "Localización de Centros de Servicios (Consumo In Situ vs Prestados a Domicilio)",
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
        "code_hint": "UT08-11",
        "slides": [13, 14]
    },
    # 10
    {
        "id": 10,
        "title": "Factores Críticos para la Localización de Centros Comerciales y Locales Minoristas",
        "question_variants": [
            "Enumerar 4 factores críticos para la localización de centros comerciales y locales minoristas.",
            "Enumere al menos cuatro factores críticos para la localización de centros comerciales y locales minoristas.",
            "Localización de locales comerciales y retail: factores determinantes."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 12)",
            "1° Parcial Fotos Tema 1",
            "1° Parcial Fotos Tema 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 8)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 10)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-11",
        "slides": [15]
    },
    # 11
    {
        "id": 11,
        "title": "Método Funcional Basado en Costos para Localización de Planta (Función Objetivo Fi)",
        "question_variants": [
            "Utilizando el método funcional basado en costos para la localización de la planta según la función objetivo Fi = Π (SAi / SBi)^Pi ... Indique que valor toma Fi cuando la locación B es la óptima.",
            "Utilizando el Método Funcional basado en costos para la localización de planta, el cálculo de la función objetivo Fi = Π (SAi / SBi)^Pi Fi > 1, Fi = 1, o Fi < 1. Indicar que valor toma Fi cuando la locación A es la óptima."
        ],
        "occurrences": [
            "1° Parcial 13/06/2022 - Tema 2",
            "Foto Parcial Manuscrito (Pregunta 4)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-11",
        "slides": [12]
    },
    # 12
    {
        "id": 12,
        "title": "Pisos Industriales: Capas (Subrasante, Sub-base, Base) y Barrera de Vapor",
        "question_variants": [
            "Piso industrial base y sub base de qué están hechos",
            "Para el piso industrial: ¿Para qué se usa la barrera de vapor y de qué material está hecha?",
            "Para un piso industrial ¿Cómo está conformado el subrasante?",
            "Para un piso industrial ¿Cómo está conformada la base y la sub base?"
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 10)",
            "Foto Parcial Manuscrito (Pregunta 5)",
            "1° Parcial 08/07/2024 - Temas 1 y 2",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4, 11)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6, 17)",
            "Resumen-de-Preguntas-Manejo-de-Materiales.pdf (Pág 9)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-41",
        "slides": [24, 25, 26, 27]
    },
    # 13
    {
        "id": 13,
        "title": "Hormigón Pretensado: Características, Componentes y Efecto que Busca",
        "question_variants": [
            "Describa las características del hormigón pretensado y qué efecto busca.",
            "Describa el funcionamiento de cada uno de los componentes del hormigón pretensado.",
            "Hormigón pretensado en vigas y cubiertas industriales."
        ],
        "occurrences": [
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "Foto Parcial Manuscrito (Pregunta 6)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-41",
        "slides": [13, 14]
    },
    # 14
    {
        "id": 14,
        "title": "Métodos No Cuantitativos y Metodología SLP de Muther en sus 4 Etapas",
        "question_variants": [
            "Cuáles son los métodos no cuantitativos de distribución",
            "El método SLP de Muther en cada una de sus cuatro etapas ¿Qué metodología recomienda aplicar para la toma de decisión y desarrollo de la etapa?",
            "Indique y describa cada uno de los métodos no cuantificables para la distribución de planta."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 2)",
            "Foto Parcial Manuscrito (Pregunta 7)",
            "1° Parcial Fotos Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT0910",
        "slides": [12, 13, 14, 15]
    },
    # 15
    {
        "id": 15,
        "title": "Factores de Distribución en Planta (Concepto y los 8 Factores de Muther / Tompkins)",
        "question_variants": [
            "¿Cómo definiría los factores de distribución de planta? Indique al menos cuatro de estos factores.",
            "Factores que influyen en la distribución en planta: Material, Maquinaria, Hombre, Movimiento, Espera, Servicio, Edificio, Cambio."
        ],
        "occurrences": [
            "Foto Parcial Manuscrito (Pregunta 8)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT0910",
        "slides": [5]
    },
    # 16
    {
        "id": 16,
        "title": "Consumo de Energía en Edificios Industriales: Distribución y Fuentes",
        "question_variants": [
            "De dónde sale el consumo de energía de edificio",
            "El consumo de energía de los edificios representa el aspecto ambiental más relevante. Indicar en qué se distribuye este consumo.",
            "Eficiencia energética y distribución del consumo en edificios industriales."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 3)",
            "1° Parcial Fotos Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-41",
        "slides": [33, 34]
    },
    # 17
    {
        "id": 17,
        "title": "Pasillos de Circulación en Planta y Almacenes: Características y Clasificación",
        "question_variants": [
            "Características de pasillos y clasificación",
            "Qué características deben tener los pasillos de circulación y cómo se clasifican",
            "Pasillos principales, secundarios y de servicio: diseño y normas de seguridad."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 4)",
            "1° Parcial Fotos Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-04",
        "slides": [12, 13, 14]
    },
    # 18
    {
        "id": 18,
        "title": "Áreas y Zonas en el Diseño de Almacenes y Puertos de Carga y Descarga",
        "question_variants": [
            "Además de la zona de carga y descarga propiamente dicha ¿Qué otras áreas o partes de las plantas comprende el diseño?",
            "Diseño y dimensionamiento de almacenes: zonas de muelles, playa de maniobras, staging, almacenamiento y servicios."
        ],
        "occurrences": [
            "Foto Parcial Manuscrito (Pregunta 9)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-04",
        "slides": [4, 5, 6]
    },
    # 19
    {
        "id": 19,
        "title": "Modelo Determinista / Abastecimiento por Lote: Premisas, Características y Costo C1",
        "question_variants": [
            "Indique las características y premisas del modelo determinista o abastecimiento por lote para la planificación de stock.",
            "En el cálculo del modelo de abastecimiento por lote aparece el término C1 costo unitario de almacenamiento ¿Qué parámetros componen este costo?"
        ],
        "occurrences": [
            "1° Parcial 09/12/2024 (Recuperatorio)",
            "Foto Parcial Manuscrito (Pregunta 10)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-01",
        "slides": [11, 12]
    },
    # 20
    {
        "id": 20,
        "title": "Unidad de Carga: Definición, Tipos y Funciones",
        "question_variants": [
            "Unidad de carga, defínalo.",
            "Defina Unidad de Carga e indique sus principales ventajas logísticas y operativas.",
            "Concepto de unidad de carga, cohesión y resistencia al transporte."
        ],
        "occurrences": [
            "Foto Parcial Manuscrito (Pregunta 11)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-03",
        "slides": [3, 4, 5]
    },
    # 21
    {
        "id": 21,
        "title": "3 Métodos Básicos de Manejo de Materiales (Manual, Mecanizado y Automatizado)",
        "question_variants": [
            "3 métodos básicos de manejo describir y dar ejemplo de cada uno",
            "Clasificación de los métodos de manejo de materiales: manual, mecanizado y automatizado con ejemplos."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 1)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 1)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT01-01",
        "slides": [8, 9, 10]
    },
    # 22
    {
        "id": 22,
        "title": "Trabajo Muscular: Dinámico, Estático y Trabajo Manual Moderado",
        "question_variants": [
            "Definir trabajo muscular dinámico",
            "Describa el trabajo manual moderado e indique los efectos en el cuerpo.",
            "Defina trabajo muscular estático y dinámico ¿Cuáles son las diferencias entre ellos?",
            "Defina Trabajo Moderado en función del gasto de energía, de un ejemplo e indique los efectos en el cuerpo humano."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 11)",
            "Foto Parcial Manuscrito (Pregunta 12)",
            "1° Parcial 07/07/2025 - Curso 5053",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "2° Parcial 07/11/2022 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT02-02",
        "slides": [4, 5, 6, 7, 11]
    },
    # 23
    {
        "id": 23,
        "title": "Administración de la Cadena de Suministro: Tipos de Riesgos y Ejemplos",
        "question_variants": [
            "Cuáles son los tipos de riesgos de administración en la cadena de suministro y ejemplos",
            "¿En qué tipos se dividen los riesgos en la administración de la cadena de suministros? Indicar al menos un ejemplo de cada tipo."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 6)",
            "1° Parcial Fotos Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-01",
        "slides": [6, 7]
    },
    # 24
    {
        "id": 24,
        "title": "Esquema de Actividades en la Zona de Despacho / Expedición de Almacenes",
        "question_variants": [
            "Esquema de las actividades zona de despacho",
            "Describa en un esquema las tareas que se realizan en la actividad de despacho de almacenes.",
            "Flujo de expedición de pedidos en depósitos."
        ],
        "occurrences": [
            "1° Parcial 2026 (Pregunta 5)",
            "1° Parcial Fotos Tema 1",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 6, 14)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-02",
        "slides": [11]
    },
    # 25
    {
        "id": 25,
        "title": "Industria 4.0 e Intralogística 4.0: Definición y Pilares Tecnológicos",
        "question_variants": [
            "¿Qué es la industria 4.0? y ¿la intralogística 4.0?",
            "Indicar qué cuestiones conceptuales y puntuales hacen que el estudio de la Intralogística reemplace en la actualidad al tradicional tratado de Manejo de Materiales y Distribución en Planta."
        ],
        "occurrences": [
            "Foto Parcial Manuscrito (Pregunta 1)",
            "1° Parcial 09/12/2025 (Recuperatorio)",
            "1° Parcial Fotos Tema 3",
            "Parcial 12 Preguntas Fotos",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT01-01",
        "slides": [3, 4, 5, 6]
    },
    # 26
    {
        "id": 26,
        "title": "Edificios de Hormigón Armado Prefabricado: Ventajas y Comportamiento Estructural",
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
        "code_hint": "UT08-41",
        "slides": [17]
    },
    # 27
    {
        "id": 27,
        "title": "Normas LEED: Parámetros de Medición y Certificación Sustentable",
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
        "code_hint": "UT08-41",
        "slides": [35, 36]
    },
    # 28
    {
        "id": 28,
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
        "code_hint": "UT0910",
        "slides": [17, 18]
    },
    # 29
    {
        "id": 29,
        "title": "Buenas Prácticas de Almacenamiento (BPA)",
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
        "code_hint": "UT07-02",
        "slides": [14, 15]
    },
    # 30
    {
        "id": 30,
        "title": "Envases según Clasificación Europea (Primario, Secundario, Terciario) y Rígidos vs Flexibles",
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
        "code_hint": "UT07-03",
        "slides": [6, 7, 8, 9, 15]
    },
    # 31
    {
        "id": 31,
        "title": "Estudio de Impacto Ambiental (EsIA) y Proceso Sostenible",
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
        "code_hint": "UT08-21",
        "slides": [6, 7, 8]
    },
    # 32
    {
        "id": 32,
        "title": "Método de Brown & Gibson: Factores Críticos, Objetivos y Subjetivos (Parámetro W)",
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
        "code_hint": "UT08-11",
        "slides": [9, 10, 11]
    },
    # 33
    {
        "id": 33,
        "title": "Esquema de Tareas en el Proceso de Recepción de Almacenes",
        "question_variants": [
            "Describa en un esquema las tareas que se realizan en la actividad de recepción de almacenes.",
            "Flujo operativo y tareas principales en Recepción de un almacén."
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
        "code_hint": "UT07-02",
        "slides": [4, 5, 6]
    },
    # 34
    {
        "id": 34,
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
        "code_hint": "UT0910",
        "slides": [6, 7, 8, 9, 10]
    },
    # 35
    {
        "id": 35,
        "title": "Ventajas y Desventajas de Distribución por Proceso (Funcional) vs por Producto (Línea)",
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
        "code_hint": "UT0910",
        "slides": [8, 10]
    },
    # 36
    {
        "id": 36,
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
        "code_hint": "UT08-41",
        "slides": [19]
    },
    # 37
    {
        "id": 37,
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
        "code_hint": "UT08-11",
        "slides": [8]
    },
    # 38
    {
        "id": 38,
        "title": "Responsables de Obra según el Código de Edificación de CABA para Obra Mayor",
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
        "code_hint": "UT08-31",
        "slides": [17, 18]
    },
    # 39
    {
        "id": 39,
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
        "code_hint": "UT08-41",
        "slides": [22]
    },
    # 40
    {
        "id": 40,
        "title": "Principio de Distribución en Planta para la Integración de Conjunto",
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
        "code_hint": "UT0910",
        "slides": [4]
    },
    # 41
    {
        "id": 41,
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
        "code_hint": "UT02-01",
        "slides": [17, 18, 20, 21, 22]
    },
    # 42
    {
        "id": 42,
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
        "code_hint": "UT02-01",
        "slides": [23, 24, 25]
    },
    # 43
    {
        "id": 43,
        "title": "Transportadores Aéreos Power vs Power & Free: Sustentación, Troleys y Pasos",
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
        "code_hint": "Resumen_BR3",
        "slides": [40, 41, 42, 43]
    },
    # 44
    {
        "id": 44,
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
        "code_hint": "Resumen_BR3",
        "slides": [35, 36, 37]
    },
    # 45
    {
        "id": 45,
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
        "code_hint": "Resumen_BR3",
        "slides": [48, 49, 50, 51]
    },
    # 46
    {
        "id": 46,
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
        "code_hint": "Resumen_BR3",
        "slides": [52, 53]
    },
    # 47
    {
        "id": 47,
        "title": "Sistemas de Almacenamiento por Bloques: Drive, Push-Back, Dinámicas y Pallet Shuttle",
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
        "code_hint": "UT07-05",
        "slides": [4, 5, 6, 7, 8, 9, 10, 11]
    },
    # 48
    {
        "id": 48,
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
        "code_hint": "Resumen_BR3",
        "slides": [45, 46]
    },
    # 49
    {
        "id": 49,
        "title": "Cintas y Bandas Transportadoras: Estaciones Superiores, Componentes y Elementos de Limpieza",
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
        "code_hint": "Resumen_BR3",
        "slides": [22, 23, 24, 25, 26]
    },
    # 50
    {
        "id": 50,
        "title": "Elevadores de Cangilones: Clasificación y Tipos de Descarga (Gravedad Libre vs Gravedad Dirigida)",
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
        "code_hint": "Resumen_BR3",
        "slides": [30, 31, 32]
    },
    # 51
    {
        "id": 51,
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
        "code_hint": "UT08-21",
        "slides": [35, 36, 40, 41, 44, 45]
    },
    # 52
    {
        "id": 52,
        "title": "Tornillos de Alta Resistencia: Inscripción 10.9, Tensión y Torque en Uniones Abulonadas",
        "question_variants": [
            "Indique el valor de resistencia (en N/mm²) a la rotura del material de un tornillo en cuya cabeza se encuentra la siguiente inscripción: 10.9",
            "Explique, para una unión de piezas con diseño abulonado, qué diferencias existe entre torque y tensión indicando, además, cómo se lleva a cabo, sin el uso de un torquímetro, el ajuste de una unión abulonada del tipo rígida (método del giro de tuerca)."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 3 (Preguntas 8 y 10)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 6)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-41",
        "slides": [22, 23]
    },
    # 53
    {
        "id": 53,
        "title": "Vigas de Repartición: Anclaje Soldado vs Abulonado y Resistencia Estructural",
        "question_variants": [
            "Explicar las ventajas y desventajas de un sistema de vigas de repartición ancladas mediante sistemas soldados en vez de abulonados indicando, además, cuándo y por qué motivo en particular se utiliza este tipo de solución.",
            "Vigas de repartición de perfiles IPN para colgado de cargas industriales (ejercicio práctico y teórico)."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 3 (Pregunta 9)",
            "Parcial Práctico Vigas de Repartición (Foto)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 4)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-41",
        "slides": [21, 22]
    },
    # 54
    {
        "id": 54,
        "title": "Método de Cribado para Localización de Plantas y Objetivos de Parques Industriales",
        "question_variants": [
            "Indicar los pasos (en secuencia ordenada) a cumplir para la localización de una planta mediante el uso del Método de Cribado.",
            "Indicar cuáles son los objetivos básicos que se pretenden alcanzar mediante la creación y uso de Parques Industriales."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 3 (Preguntas 3 y 4)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 2, 3)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 3, 4)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-11",
        "slides": [6, 7]
    },
    # 55
    {
        "id": 55,
        "title": "Método CRAFT y Método de Adyacencias para Diseño de Layout",
        "question_variants": [
            "Explique las bases de cálculo, básicas, para definir el funcionamiento del Método CRAFT.",
            "Explique qué es, matemáticamente hablando, el llamado Método de Adyacencias para el diseño de un lay-out indicando con un ejemplo, además, cómo se construye para el mismo una Tabla de Relaciones."
        ],
        "occurrences": [
            "1° Parcial Fotos Tema 3 (Preguntas 6 y 7)",
            "Preguntas-1P-Manejo-LC-TERMINADO.pdf (Pág 5)",
            "Preguntas-a-desarrollar-manejo-1Parcial-2023.pdf (Pág 7)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT0910",
        "slides": [25, 26, 27]
    },
    # 56
    {
        "id": 56,
        "title": "Terminales Portuarias (Polivalente y Buques Petroleros)",
        "question_variants": [
            "¿Qué tipo de carga maneja una terminal portuaria polivalente?",
            "Indique los diferentes tipos de terminales portuarias para buques petroleros y descríbalas brevemente."
        ],
        "occurrences": [
            "2° Parcial 06/11/2023 - Tema 1",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "Resumen_BR3",
        "slides": [60, 61]
    },
    # 57
    {
        "id": 57,
        "title": "Picking en Estanterías de Pequeñas Piezas: Métodos y Tipos",
        "question_variants": [
            "Indicar los procesos de picking en las estanterías de pequeñas piezas, describiendo cada uno de estos.",
            "Picking hombre a producto vs producto a hombre (mini-load, carruseles horizontales/verticales, pick to light)."
        ],
        "occurrences": [
            "2° Parcial 06/11/2023 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT07-02",
        "slides": [8, 9, 10]
    },
    # 58
    {
        "id": 58,
        "title": "Contaminantes Atmosféricos: Clasificación (Primarios y Secundarios) y Ejemplos de Clases",
        "question_variants": [
            "¿Cómo se clasifican los contaminantes atmosféricos? Indicar además un ejemplo de cada una de las Clases.",
            "Contaminantes primarios y secundarios del aire."
        ],
        "occurrences": [
            "2° Parcial 07/11/2022 - Tema 1",
            "2° Parcial 06/11/2023 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "UT08-21",
        "slides": [46, 47]
    },
    # 59
    {
        "id": 59,
        "title": "Transportador de Piso Flat Top Liviano y Transportadores a Rodillos",
        "question_variants": [
            "Describa el transportador de piso tipo Flat Top liviano",
            "Describa características y funcionamiento de los Transportadores a rodillos",
            "¿Cuál es la diferencia entre un transportador a rodillo impulsado a motor y un transportador a rodillo accionado a cadena?"
        ],
        "occurrences": [
            "2° Parcial 07/11/2022 - Tema 1",
            "2° Parcial 16/12/2024 (Recuperatorio)",
            "Parcial 12 Preguntas Fotos",
            "Finales Grimolizzi 2024, 2025, 2026"
        ],
        "code_hint": "Resumen_BR3",
        "slides": [15, 16, 17]
    },
    # 60
    {
        "id": 60,
        "title": "Techos Flotantes en Tanques de Hidrocarburos y Permisos de Volcado de Efluentes",
        "question_variants": [
            "¿Cuáles son los dos tipos de techos flotantes en los tanque de almacenamientos de hidrocarburos?",
            "Autoridades para pedir permiso de volcado de efluentes en CABA y PBA (cloacal y pluvial)."
        ],
        "occurrences": [
            "2° Parcial 07/11/2022 - Tema 1",
            "Finales Grimolizzi 2024, 2025, 2026 (Exámenes Finales)"
        ],
        "code_hint": "Resumen_BR3",
        "slides": [57, 58]
    }
]

# Process and extract verbatim
processed_guide = []
for item in master_catalog:
    code = item['code_hint']
    slides = item['slides']
    if len(slides) == 1:
        v = get_slide_text(code, slides[0])
    else:
        v = get_multiple_slides_text(code, slides)
    
    if not v or not v['text']:
        print(f"Warning: No verbatim found for {item['id']} {item['title']}")
        v = {'file': code, 'unit': 'Oficial', 'slide_no': str(slides), 'text': '[Texto en procesamiento]'}
    
    processed_guide.append({
        'id': item['id'],
        'title': item['title'],
        'question_primary': item['question_variants'][0],
        'variants': item['question_variants'],
        'frequency_count': len(item['occurrences']),
        'occurrences': item['occurrences'],
        'file': v['file'],
        'unit': v['unit'],
        'slide_no': v['slide_no'],
        'verbatim_text': v['text']
    })

# Sort strictly by frequency descending
processed_guide.sort(key=lambda x: x['frequency_count'], reverse=True)

# Assign rank
for i, it in enumerate(processed_guide):
    it['rank'] = i + 1

print(f"MASTER CATALOG: Processed and sorted {len(processed_guide)} questions completely!")

with open('master_catalog_processed.json', 'w', encoding='utf-8') as out:
    json.dump(processed_guide, out, ensure_ascii=False, indent=2)
