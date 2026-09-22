# Optimización de Distribución en Planta: Floorplanning Convexo (CVXPY)

**Universidad Tecnológica Nacional - Facultad Regional Buenos Aires (UTN FRBA)**  
**Proyecto Final de Ingeniería Industrial (2026)**  
**Planta de Alimentos Libres de Gluten (Sin TACC)**  
**Modelo Exclusivo: 18 Sectores Totales**

---

## 1. Cumplimiento Estricto de Criterios del Proyecto

En concordancia con los lineamientos técnicos de la cátedra y lo desarrollado en [`metodo_muther`](../metodo_muther):

1. **Modelo Exclusivo de 18 Sectores**:  
   Se optimiza la totalidad de los 18 sectores oficiales de la nave industrial (incluyendo servicios auxiliares de Lavado/Scrap [16], Calidad Crudo [17] y Calidad Cocido [18]).
2. **Dimensiones Oficiales de Muther (Método Guerchet)**:  
   Cada departamento mantiene estrictamente las dimensiones de ancho ($w$) y largo ($h$) calculadas para el proyecto final, dado que ya contemplan las superficies estáticas, de gravitación y de evolución/circulación.
3. **Sin Pasillo Central Artificial ($\rho = 0.0\text{ m}$)**:  
   Los sectores se posicionan en contacto rasante directo (edge-to-edge), maximizando la compacidad y evitando holguras redundantes.
4. **Cadena Continua Rígida de Galletitas Acoplada**:  
   * **Moldeadora G [5]** acoplada rígidamente a la entrada del **Horno Túnel G [6]**: $x_5 + w_5 = x_6$, centros alineados en $Y$.
   * **Cinta de Enfriado G [7]** acoplada rígidamente a la salida del **Horno Túnel G [6]**: $x_6 + w_6 = x_7$, centros alineados en $Y$.
5. **Garantía Geométrica: Cero Solapamientos ($0.000000\text{ m}^2$)**:  
   Certificado mediante auditoría exhaustiva de los 153 pares de sectores, tanto en coordenadas de punto flotante de alta precisión como tras redondeo a centímetros.

---

## 2. Dimensiones Oficiales de los 18 Sectores

| N° | Sector / Departamento | Ancho $w$ (m) | Largo $h$ (m) | Área (m²) | Rotación 90° | Función / Proceso |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **1** | Depósito MP | 8.30 | 6.30 | 52.29 | Base | Recepción y Almacén Materia Prima |
| **2** | Aduana MP | 3.80 | 3.80 | 14.50 | Rotada (90°) | Control de Ingreso y Desinfección |
| **3** | Sección Pesado | 2.00 | 3.80 | 7.60 | Base | Pesaje y Fraccionamiento MP |
| **4** | Amasado G | 2.40 | 2.17 | 5.22 | Base | Amasado Línea Galletitas |
| **5** | Moldeado G | 2.50 | 2.32 | 5.80 | Base | Moldeado Galletitas (Acoplada a Horno) |
| **6** | Horno Túnel G | 8.60 | 2.30 | 19.78 | Base | Horno Túnel Continuo |
| **7** | Cinta Enfriado G | 7.00 | 1.19 | 8.34 | Base | Cinta de Enfriado (Acoplada a Horno) |
| **8** | Envasado 1° Galletitas | 4.30 | 4.00 | 17.20 | Rotada (90°) | Envasado Primario Galletitas |
| **9** | Batido Panif. | 2.20 | 1.85 | 4.08 | Base | Batido Línea Panificados |
| **10** | Dosificado P. | 2.00 | 1.50 | 3.00 | Base | Dosificado Panificados |
| **11** | Fermentado Panes | 1.50 | 1.23 | 1.85 | Base | Cámara Fermentación Panificados |
| **12** | Hornos Rotat. Panif. | 5.20 | 3.74 | 19.46 | Base | Hornos Rotativos Panificados |
| **13** | Enfriado Panificados | 2.65 | 2.00 | 5.30 | Base | Enfriado de Panificados |
| **14** | Envasado 1° Panif. | 4.80 | 4.84 | 23.23 | Rotada (90°) | Envasado Primario Panificados |
| **15** | Depósito PT | 12.00 | 15.60 | 187.20 | Base | Almacén Producto Terminado y Despacho |
| **16** | Lavado / Scrap | 2.90 | 2.00 | 5.80 | Base | Lavado de Bandejas y Retrabajo |
| **17** | Calidad Crudo | 1.50 | 2.10 | 3.15 | Rotada (90°) | Laboratorio Control Calidad Crudo |
| **18** | Calidad Cocido | 4.50 | 2.80 | 12.60 | Base | Laboratorio Control Calidad Cocido |

---

## 3. Resultados Globales de la Nave Industrial (18 Sectores - Minimización de Z)

| Parámetro Global | Valor Obtenido | Unidad | Observación Técnica |
|---|:---:|:---:|:---|
| **Ancho Total de Nave ($W$)** | **26.40** | **m** | Optimizado con solver CLARABEL |
| **Largo Total de Nave ($H$)** | **23.89** | **m** | Optimizado con solver CLARABEL |
| **Semiperímetro ($W + H$)** | **50.29** | **m** | Compacidad envolvente |
| **Perímetro Total de Nave** | **100.58** | **m** | Perímetro edilicio exterior |
| **Superficie Bruta Nave Industrial** | **630.67** | **m²** | Superficie compacta |
| **Superficie Neta Útil de Sectores** | **396.29** | **m²** | Sumatoria Guerchet 18 sectores |
| **Factor de Ocupación Neta** | **62.8** | **%** | Relación útil/bruta |
| **Solapamiento Total entre Bloques** | **0.000000** | **m² (CERO)** | **Cero absoluto certificado** |
| **Acople Moldeado [5] $\to$ Horno [6]** | **0.0000** | **m (Acople Rígido)** | Continuidad física de línea |
| **Acople Horno [6] $\to$ Cinta [7]** | **0.0000** | **m (Acople Rígido)** | Continuidad física de línea |
| **Costo Transporte Operativo ($Z$)** | **34,912.3** | **kg·m/mes** | **Mínimo global (sin banda motriz 5-6-7)** |
| **Costo Transporte Total ($Z$)** | **42,922.3** | **kg·m/mes** | Incluyendo avance interno en cocción |

---

## 4. Estructura de Archivos

```
metodo flooring plan/
│
├── ejecutar_floor_planning.py           # Script Python principal (autoejecutable en consola)
├── floor_planning_optimizacion.ipynb     # Cuaderno Jupyter interactivo paso a paso
├── README.md                             # Documentación técnica y métricas del modelo
│
├── graficos/                             # Salidas gráficas a 300 DPI
│   └── layout_floor_planning_18_sectores.png
│
├── reporte_floor_planning_18_sectores.xlsx  # Reporte de coordenadas en Excel
└── resultados_floor_planning_18_sectores.json # Coordenadas y métricas en formato JSON
```

---

## 5. Instrucciones de Ejecución

Para correr el optimizador desde la terminal:

```powershell
python ejecutar_floor_planning.py
```

O abrir y ejecutar directamente [`floor_planning_optimizacion.ipynb`](floor_planning_optimizacion.ipynb) en Jupyter Notebook o VS Code.
