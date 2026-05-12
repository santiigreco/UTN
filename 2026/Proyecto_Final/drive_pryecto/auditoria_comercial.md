# Auditoría — Factibilidad Comercial (§3.1) — PROYECTO FINAL G8

## Planta de Alimentos Sin TACC ("Celi")

**Fecha:** 12 de mayo de 2026 | **Referencia:** Guía v17, UTN FRBA — Sección 3.1

---

## Checklist de Cobertura vs. Guía v17 §3.1

| # Guía | Requerimiento | Cubierto | Observación |
|---|---|---|---|
| 3.1.1 | Análisis de contexto (Macro entorno) | SI | Bien desarrollado |
| 3.1.2 | Variables Endógenas y Exógenas | SI | Listadas correctamente |
| 3.1.3 | Micro entorno: Porter | PARCIAL | Contenido presente pero no estructurado como 5 fuerzas de Porter |
| 3.1.4 | FODA / Diferenciación / Ventaja competitiva / Penetración / BCG | PARCIAL | FODA y Diferenciación OK. Falta BCG y estrategia de penetración explícita |
| 3.1.5 | Investigación de mercado | PARCIAL | Mercados cuantificados. Falta investigación primaria y ciclo de vida |
| 3.1.6 | Misión / Visión / Objetivos / Metas | SI | Completo |
| 3.1.7 | Macrolocalización | SI | Bien ejecutada, verificada aritméticamente |
| 3.1.8 | Mix de Marketing (4P) | SI | Producto, Precio, Promoción y Plaza desarrollados |
| 3.1.9 | Plan de Ventas | SI | En unidades y monetario a 10 años |

**Entregables requeridos:**

| Entregable | Presente | Observación |
|---|---|---|
| Market Share | PARCIAL | Declarado pero con errores numéricos |
| Estrategia y plan de acción comercial | SI | A través de las 4P y diferenciación |
| Proyección de ventas (Demanda) | SI | Tablas a 10 años |
| Costos Comerciales | SI | Sección 8 detallada |

---

## CRITICO — Errores que deben corregirse antes de entregar

### C1. Contradicción fatal: "Vegano" y "Libre de alérgenos" vs. Materias primas

La definición inicial establece textualmente: "libre de gluten, libre de alérgenos, formulación vegana".

Sin embargo, en Producto (§5.1) se listan como materias primas:

- **Huevo** — alérgeno mayor según ANMAT, NO vegano
- **Leche** — alérgeno mayor, NO vegano
- **Lecitina de soja** — alérgeno (soja es uno de los 8 alérgenos principales)

Esto es una contradicción directa que un jurado detecta inmediatamente. Destruye la credibilidad de la propuesta de valor, la estrategia de diferenciación y la segmentación del consumidor con "restricciones múltiples".

**Solución:** Clasificar cada SKU en una tabla que indique cuáles son veganos, cuáles contienen alérgenos y cuáles no. Reformular la definición inicial para que diga "línea de productos que incluye opciones veganas y libres de alérgenos", y no que TODOS lo son.

---

### C2. Market share año 10: el cálculo está mal

El documento declara alcanzar un **7,77% de market share** al año 10. Pero si el mercado crece al 4% anual (como ustedes mismos declaran), el denominador también crece:

| Parámetro | Valor documento | Valor recalculado |
|---|---|---|
| Mercado año 2 (base) | 7.321.640 kg | 7.321.640 kg |
| Mercado año 10 (4% anual, 8 años) | No calculado | ~10.020.170 kg |
| Producción año 10 | ~3.101k unidades | ~553.610 kg |
| **Market share real año 10** | **7,77%** | **~5,5%** |

**Causa:** Se calcula el share sobre el mercado estático del año 2 en vez del mercado que también crece. Para llegar a 7,77% la producción debería crecer a una tasa muy superior.

---

### C3. Ahorro logístico: error aritmético

El documento dice un "ahorro aproximado del 50%" entre logística propia ($119.960.000) y tercerizada ($66.000.000).

**Cálculo real:** (119.960.000 - 66.000.000) / 119.960.000 = **44,98% ≈ 45%**, no 50%.

Además, no se presenta el desglose de cómo se llega a ninguna de las dos cifras.

---

## INCONSISTENCIAS Y MEJORAS — Lógica que flaquea

### I1. Market share por categoría: desbalance extremo no justificado

El 7% agregado esconde una distribución muy despareja:

| Categoría | Share año 2 real | Observación |
|---|---|---|
| Galletitas dulces | ~22% | Se aspira a 24,58%. Casi 1/4 del mercado como empresa nueva |
| Galletitas saladas | ~0,85% | Insignificante |
| Panificados | ~3,4% | Moderado |

Declarar que se va a ser el 2do jugador del mercado de galletitas dulces sin TACC en el primer año operativo pleno contradice las propias barreras de entrada que se identifican en el documento.

---

### I2. Confusión entre market share inicial y final

El documento presenta tres cifras distintas sin aclarar la relación:

| Sección | Cifra | Contexto |
|---|---|---|
| §4.2 | 7% | "abarcar aproximadamente el 7% de market share" |
| §9 | 5,27% | "abarcar un 5,27% del mercado de manera inicial" |
| §6.3 SMART | 7% | "en un plazo de 10 años" |
| §9 final | 7,77% | "al final del ciclo de vida del proyecto (año 10)" |

Hay que unificar y ser preciso sobre cuál es el objetivo y cuál el punto de partida.

---

### I3. Consumo per cápita ENGHo: no aplica directamente al segmento sin TACC

Se usa la ENGHo del INDEC para estimar el consumo per cápita. Pero esa encuesta mide el consumo de la **población general** (productos con gluten). Un celíaco no consume la misma proporción de panificados que la población general: son más caros, menos disponibles y de diferente sabor/textura. Esto probablemente **sobreestima** la demanda de panificados.

**Sugerencia:** Reconocer esta limitación explícitamente o usar datos del Monitor de Alimentos Sin Gluten que ya se cita.

---

### I4. Exportación: promovida en macroentorno, descartada en plaza

En el macroentorno se dedican dos párrafos a la oportunidad de exportar a LATAM y EE.UU. Pero en Plaza se dice "Se ha definido una política de No Exportación". Si no van a exportar, el macroentorno no debería promoverla como oportunidad clave, o debe aclararse que es una oportunidad a futuro fuera del horizonte de 10 años.

---

### I5. Tasas de crecimiento reales no coinciden con las declaradas

| Período | Tasa declarada | Tasa real en tabla |
|---|---|---|
| Año 2 a 3 | 4,0% | 4,16% |
| Año 3 a 4 | 4,0% | 4,31% |
| Año 4 a 5 | 4,5% | 4,77% |
| Año 5 a 6 | 4,5% | 4,71% |
| Año 6 a 7 | 4,5% | 4,77% |

Las diferencias son menores pero sistemáticas (~0,3pp). Probablemente redondeo acumulativo, pero debería explicarse.

---

### I6. Fila "Total" en tabla de precios: sin sentido económico

La fila "TOTAL" muestra $22.615 en la columna de precio unitario. Es la suma de los 11 precios, lo cual no tiene significado. Debería ser un promedio ponderado o eliminarse.

---

### I7. Porter no está estructurado como las 5 Fuerzas

La guía pide "Micro entorno: Porter". El documento cubre los contenidos (competidores, sustitutos, proveedores, clientes, barreras), pero no se nombra el modelo, no está organizado con los 5 encabezados formales y falta la conclusión sobre intensidad de la rivalidad.

---

## DATOS Y DETALLES — Faltantes según la guía y ajustes menores

### D1. Falta: Análisis BCG (Boston Consulting Group)

La guía pide BCG en §3.1.4. Para 11 SKUs, categorizar cuáles son Estrellas, Vacas, Interrogantes o Perros aportaría al análisis de portfolio que también pide la sección de Precio.

### D2. Falta: Estrategia de penetración explícita

La guía pide "Penetración" en §3.1.4. El documento describe acciones comerciales pero no formaliza una estrategia de penetración como concepto (precios de penetración, ramp-up por canal, hitos de distribución).

### D3. Falta: Investigación primaria (Encuestas, Focus Group, Entrevistas)

La guía lista: "Encuestas, Focus, Entrevistas, Observación, Información histórica, Prueba piloto". El documento se basa exclusivamente en información secundaria. Una encuesta a consumidores celíacos o un focus group fortalecería la validación.

### D4. Falta: Ciclo de vida del producto

La guía pide "Ciclo de vida" en §3.1.5. No existe análisis del ciclo de vida del mercado sin TACC (¿crecimiento, madurez?). Justifica las tasas de crecimiento usadas.

### D5. Falta: Elasticidad precio-demanda

La guía pide "Elasticidad" en Precio. Se menciona cualitativamente que la demanda celíaca es inelástica y la saludable elástica, pero no se cuantifica ni analiza el impacto de variaciones de precio.

### D6. Falta: Análisis de portfolio de precios

La guía pide "Análisis de portfolio" en Precio. No se explica la lógica de pricing entre líneas (Gourmet vs. Estándar vs. Free) ni por qué las pepas ($1.800) son más baratas que polvorones sin azúcar ($2.070).

### D7. Factor multiplicador de 1,6 sin fuente

Se usa 1,6 sobre la población celíaca para estimar demanda periférica, diciendo que es "conservador" pero sin citar fuente. La diferencia entre 1,3 y 2,0 impacta el mercado potencial en ±25%.

### D8. Datos de Smams sin fuente citada

Se usan ventas 2025 de Smams (432 tn dulces, 307 tn saladas, 356 tn panificados). No se indica de dónde provienen. Para un trabajo académico toda cifra necesita fuente.

### D9. Precio diferencial "hasta 8 veces" sin fuente precisa

Se afirma que los productos sin gluten cuestan "hasta 8 veces" más que los convencionales. Probablemente cierto para pan francés pero no para todas las categorías. Citar fuente o moderar a un rango.

### D10. Nombre del proyecto inconsistente

La portada dice "Celi", en versiones previas aparecía "Naturalis". La guía pide "Marca e Imagen / Posicionamiento" en Promoción. Formalizar el nombre.

### D11. Falta: Comparativo con productos similares

La guía pide "Comparativo con productos similares" en Producto. No hay un cuadro formal Celi vs. Smams vs. Schar vs. Bio en ingredientes, gramaje, precio y atributos.

### D12. Falta: Empaque y etiqueta detallados

La guía pide "Presentación: Empaque y etiqueta". Se define el gramaje pero no el material del envase, tipo de sellado, información obligatoria en etiqueta (RNPA, RNE, logo Sin TACC, tabla nutricional), ni diseño visual.

---

## Resumen de Hallazgos

| Nivel | Cantidad | Impacto |
|---|---|---|
| CRITICO | 3 | Errores que invalidan argumentos clave |
| INCONSISTENCIAS | 7 | Debilitan coherencia interna |
| DATOS Y DETALLES | 12 | Variables que la guía pide y no están |
| **Total** | **22** | — |

---

## Lo que está bien hecho

1. **Macroentorno sólido** con datos actualizados (REM, Monitor MinSalud)
2. **Proveedores con nombre propio** — valioso y poco común
3. **Costos comerciales detallados** con valores referenciales reales
4. **Macrolocalización correcta** — verificada aritméticamente sin errores
5. **Plan de ventas a 10 años** con desglose por SKU
6. **Estrategia B2B realista** — demuestra conocimiento del retail
7. **FODA completa** — cubre fortalezas, debilidades, oportunidades y amenazas
8. **Estrategia de diferenciación bien argumentada** — exclusividad de planta, innovación sensorial

---

## Prioridades de corrección

| # | Acción | Esfuerzo | Impacto |
|---|---|---|---|
| 1 | Resolver contradicción vegano/alérgenos con tabla por SKU | Bajo | Altísimo |
| 2 | Recalcular market share año 10 sobre mercado creciente | Medio | Alto |
| 3 | Unificar cifras de market share (5,27% / 7% / 7,77%) | Bajo | Alto |
| 4 | Estructurar Porter como 5 fuerzas con encabezados | Medio | Alto |
| 5 | Agregar matriz BCG para los 11 SKUs | Medio | Medio |
| 6 | Agregar ciclo de vida del producto/mercado | Bajo | Medio |
| 7 | Agregar alguna investigación primaria (mínimo encuesta) | Alto | Alto |
| 8 | Corregir "50%" a "45%" en ahorro logístico | Bajo | Bajo |
| 9 | Agregar cuadro comparativo vs. competencia | Medio | Medio |
| 10 | Detallar empaque y etiqueta | Medio | Medio |
