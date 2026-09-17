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
6. **Configuración CERO Cruces Totales (Conexión Centralizada de Calidad Cocido [18])**:  
   * **Calidad Cocido [18] Centralizado (Integración Panificados + Galletitas)**:
     * Se posiciona en el **centro neurálgico** entre ambas líneas de producción cocidas ($x = 14.21\text{ m}$, $y = 6.05\text{ m}$).
     * **Conexión con Panificados**: Comparte su frontera oeste con **Enfriado de Panificados [13]**. Las muestras de panificados cocidos ($[13] \to [18]$, 3 kg/mes) pasan en forma directa e inmediata a través del tabique compartido (flecha corta hacia la derecha).
     * **Conexión con Galletitas**: Comparte su frontera este con **Envasado 1° Galletitas [8]**. Las muestras de galletitas ($[8] \to [18]$, 3 kg/mes) pasan en forma directa e inmediata a través del tabique compartido (flecha corta hacia la izquierda).
     * **Resultado**: **Ninguna línea queda desconectada**. Ambas líneas de producto cocido descargan muestras en el laboratorio sin circular por pasillos ni cruzarse con ninguna otra operación.
   * **Lavado / Scrap [16]**:
     * Ubicado contiguo al oeste de Enfriado Panificados [13], liberando el corredor vertical directo para el flujo de producto hacia Envasado 1° Panificados $[13] \to [14]$.
   * **Calidad Crudo [17]**:
     * Centralizado contiguo entre Amasado Galletitas [4] y Batido Panificados [9] para los productos crudos.
   * **Flujos Productivos Principales (14 Aristas)**: Circulan de manera **100% planar y laminar**, con **0 cruces** y **0 cortes de recuadros**.

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

## 3. Resultados Globales de la Nave Industrial (Cero Cruces y Cero Cortes)

| Parámetro Global | Valor Obtenido | Unidad | Observación Técnica |
|---|:---:|:---:|:---|
| **Cruces en Flujos Productivos Principales** | **0** | **cruces** | **0 cruces certificado (Flujo planar estricto)** |
| **Cruces en Flujos Secundarios de Apoyo** | **0** | **cruces** | **0 cruces certificado (Conexiones directas adyacentes)** |
| **Flechas que Atraviesan Sectores Intermedios** | **0** | **cortes** | **Ninguna flecha atraviesa otro departamento** |
| **Cruces Totales en el Plano Visual** | **0** | **cruces** | **Ningún vector de transporte se intersecta** |
| **Conexión Calidad Cocido [18]** | **Doble Adyacencia** | - | **Contiguo a Panificados [13] y Galletitas [8]** |
| **Costo Transporte Operativo ($Z_{\text{operativo}}$)** | **41,903.8** | **kg·m/mes** | **Óptimo global convexo (CVXPY / CLARABEL)** |
| **Costo Transporte Total ($Z_{\text{total}}$)** | **49,913.8** | **kg·m/mes** | Incluye banda continua motorizada (5-6-7) |
| **Solapamiento Total entre Bloques** | **0.000000** | **m² (CERO)** | **Cero absoluto certificado (153 pares auditados)** |
| **Ancho Total de Nave ($W$)** | **26.86** | **m** | Ancho óptimo de nave |
| **Largo Total de Nave ($H$)** | **24.45** | **m** | Largo óptimo de nave |
| **Semiperímetro ($W + H$)** | **51.31** | **m** | Compacidad envolvente |
| **Superficie Bruta Nave Industrial** | **656.71** | **m²** | Envolvente compacta |
| **Superficie Neta Útil de Sectores** | **396.29** | **m²** | Sumatoria Guerchet 18 sectores |
| **Factor de Ocupación Neta** | **60.3** | **%** | Relación útil/bruta |
| **Acople Moldeado [5] $\to$ Horno [6]** | **0.0000** | **m (Acople Rígido)** | Continuidad física de línea |
| **Acople Horno [6] $\to$ Cinta [7]** | **0.0000** | **m (Acople Rígido)** | Continuidad física de línea |

---

## 4. Estructura de Archivos

```
metodo_floor_plan_cero_cruces/
│
├── ejecutar_floor_planning.py           # Script Python principal (auditoría de solapamientos y cruces)
├── floor_planning_optimizacion.ipynb     # Cuaderno Jupyter interactivo paso a paso
├── README.md                             # Documentación técnica y auditoría matemática
│
├── graficos/                             # Salidas gráficas a 300 DPI
│   └── layout_floor_planning_18_sectores.png
│
├── reporte_floor_planning_18_sectores.xlsx  # Reporte de coordenadas y auditoría en Excel
└── resultados_floor_planning_18_sectores.json # Coordenadas y métricas en formato JSON
```


---

## 5. Instrucciones de Ejecución

Para correr el optimizador desde la terminal:

```powershell
python ejecutar_floor_planning.py
```

O abrir y ejecutar directamente [`floor_planning_optimizacion.ipynb`](floor_planning_optimizacion.ipynb) en Jupyter Notebook o VS Code.
