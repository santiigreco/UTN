# 🎓 Guía Definitiva: Final de Instalaciones Industriales (UTN)

Este documento contiene los temas más importantes analizados de los parciales 2024/2025 y las respuestas desarrolladas con el rigor técnico necesario para aprobar el examen final.

---

## 🔝 Parte 1: Resumen de "Los Elegidos" (Temas que SIEMPRE están)

1.  **NPSH (ANPA):** La diferencia entre el disponible (tu instalación) y el requerido (la bomba). Si $ANPA_d < ANPA_r$, hay cavitación.
2.  **Ciclo de Refrigeración:** Dibujar el diagrama $T-s$ o $P-h$ y explicar las 4 etapas (Compresor, Condensador, Expansión, Evaporador).
3.  **Corrección del Factor de Potencia:** Por qué el $\cos \phi$ es bajo (motores subcargados, reactiva) y cómo se arregla (capacitores).
4.  **Caldera Escocesa Marina:** El dibujo de la caldera humotubular es un clásico. Conocer sus 3-4 sistemas de seguridad.
5.  **Instalación de Aire Comprimido:** El orden de los equipos (compresor -> enfriador -> tanque -> secador -> filtros).
6.  **Combustibles (PCI vs PCS):** La diferencia fundamental es si aprovechas el calor de condensación del agua formada.
7.  **Selección de Conductores:** El proceso de 3 pasos: Corriente de diseño -> Tabla -> Caída de tensión.
8.  **Motores MAT:** Funcionamiento por inducción, resbalamiento y el arranque estrella-triángulo.

---

## ✍️ Parte 2: El Examen Simulado (Respuestas Desarrolladas)

### 💧 TEMA: Conducción de Fluidos
**Pregunta:** *Explique el concepto de NPSH disponible y qué factores de la instalación lo afectan. ¿Cómo varía si succiono de un tanque enterrado?*

**Respuesta Técnica:**
El **NPSH Disponible (ANPA-d)** es la presión absoluta neta que queda en la brida de succión de la bomba por encima de la presión de vapor del líquido. Se calcula como:
$$ANPA_d = \frac{P_{atm} - P_{vap}}{\gamma} \pm z_1 - J_{1-2}$$
Factores que lo afectan:
*   **Presión Atmosférica:** A mayor altura geográfica, menor $P_{atm}$ y menor $ANPA_d$.
*   **Temperatura del líquido:** A mayor temperatura, sube la $P_{vap}$, disminuyendo el $ANPA_d$ (más riesgo de cavitación).
*   **Pérdidas de carga ($J$):** Filtros sucios o cañerías largas en succión bajan el $ANPA_d$.
*   **Posición ($z_1$):** Si el tanque está **enterrado** (bomba arriba), $z_1$ es negativo, restando presión y haciendo que el $ANPA_d$ sea crítico.

---

### ⚡ TEMA: Instalaciones Eléctricas / Motores
**Pregunta:** *¿Por qué es necesario corregir el Factor de Potencia en una planta industrial? Mencione tres equipos para hacerlo.*

**Respuesta Técnica:**
Un factor de potencia bajo (menor a 0.85/0.95 según la distribuidora) indica una alta circulación de **energía reactiva** que no produce trabajo útil. Es necesario corregirlo para:
1.  **Evitar multas y recargos** en la factura eléctrica.
2.  **Optimizar la capacidad de cables y transformadores** (menor corriente total para la misma potencia activa).
3.  **Reducir las caídas de tensión** y pérdidas por efecto Joule en las líneas.
**Equipos:** Bancos de capacitores (estáticos o automáticos), Motores Sincrónicos (sobreexcitados) y Compensadores Estáticos de VAR.

---

### 🔥 TEMA: Combustibles
**Pregunta:** *Defina Poder Calorífico de un combustible. Explique la diferencia técnica entre PCI y PCS.*

**Respuesta Técnica:**
El **Poder Calorífico (PC)** es la cantidad de energía liberada por la combustión completa de una unidad de masa (o volumen) de combustible.
*   **PCS (Superior):** Incluye el calor total de la reacción, incluyendo el calor latente de condensación del vapor de agua generado (el agua termina en estado líquido).
*   **PCI (Inferior):** No considera el calor de condensación del agua (el agua sale como vapor en los gases de escape).
En la práctica industrial, se suele usar el **PCI** porque las calderas convencionales no condensan el vapor de agua para evitar la formación de ácidos corrosivos en la chimenea (punto de rocío de ácidos).

---

### ❄️ TEMA: Refrigeración
**Pregunta:** *¿A qué se llama Sobrecalentamiento en el ciclo de refrigeración y dónde se mide? ¿Para qué sirve?*

**Respuesta Técnica:**
El **sobrecalentamiento** es el incremento de temperatura que sufre el vapor refrigerante una vez que se ha evaporado completamente. Se mide a la salida del evaporador (antes de entrar al compresor).
**Utilidad:** Es una medida de seguridad crítica para asegurar que **no ingrese refrigerante en estado líquido al compresor**. Las válvulas de expansión termostáticas (VET) controlan este valor (típicamente entre 5°C y 8°C) para maximizar la superficie de intercambio del evaporador sin poner en riesgo la integridad mecánica del compresor.

---

### 🌬️ TEMA: Aire Comprimido
**Pregunta:** *Explique las tres magnitudes de calidad de aire según la norma ISO 8573.*

**Respuesta Técnica:**
La norma clasifica la calidad del aire en función de tres contaminantes:
1.  **Partículas Sólidas:** Define el tamaño máximo (micras) y la concentración.
2.  **Agua (Humedad):** Define el punto de rocío a presión (PDP). A menor punto de rocío, más seco es el aire.
3.  **Contenido de Aceite:** Define la concentración residual de aerosoles y vapores de aceite (mg/m³).

---

### 💨 TEMA: Generación de Vapor
**Pregunta:** *Describa dos pruebas obligatorias que se deben realizar al indicador de nivel de una caldera.*

**Respuesta Técnica:**
Se deben realizar pruebas de purga para verificar que los conductos no estén obstruidos:
1.  **Prueba de Agua:** Se cierra el grifo superior (vapor) y se abre la purga. El nivel de agua debe bajar y, al cerrar la purga, debe subir rápidamente por el conducto inferior.
2.  **Prueba de Vapor:** Se cierra el grifo inferior (agua) y se abre la purga. Debe salir vapor seco. Esto asegura que el conducto de vapor hacia la zona alta del vidrio esté libre.

---
*Este documento es una síntesis de "lo que hay que saber" para el final. Si dominás estas 6 respuestas, tenés más de la mitad del examen adentro.*
