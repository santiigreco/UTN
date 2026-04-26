# 📋 Informe de Estudio: Instalaciones Industriales (UTN)
## Análisis de Temas Clave para el Examen Final

Este documento resume los temas recurrentes en los parciales y ejercicios de TPs, organizados para facilitar el estudio del examen final.

---

### 1. Mecánica de los Fluidos y Bombeo
El eje del primer parcial y una base fundamental del final.

*   **ANPA / NPSH:** Saber definir el **Disponible** (instalación) y el **Requerido** (bomba).
    *   *Concepto Clave:* El disponible debe ser al menos un 10% superior al requerido para evitar la **cavitación**.
    *   *Variables:* Si la bomba está por encima de la fuente de agua ($z_1$ negativo), el NPSH disponible disminuye.
*   **Pérdidas de Carga:** 
    *   **Primarias:** Por rozamiento en tramos rectos. Dependen del material y el régimen (Reynolds).
    *   **Secundarias:** Por accesorios (válvulas, codos). Se calculan con el coeficiente $K$ o longitud equivalente ($L_e$).
*   **Curva de la Instalación:** Gráfico de Carga vs Caudal. Su intersección con la curva de la bomba da el **punto de trabajo real**.
*   **Diagrama de Camerer:** Sirve para encontrar el **diámetro económico** de la cañería, equilibrando costos de inversión y costos operativos (energía).

### 2. Aire Comprimido y Gases Industriales
*   **Esquema de Instalación:** Compresor -> Post-enfriador -> Separador de humedad -> Tanque receptor -> Secador -> Filtros -> Consumidores.
*   **Calidad del Aire (ISO 8573):** Se analiza por contenido de **Sólidos (polvo)**, **Líquidos (agua)** y **Gaseosos (aceite)**.
*   **Leyes de Gases:** Manejo de PV=nRT y corrección de caudales (CNPT a condiciones de servicio).
*   **Seguridad en Cilindros:** Reconocer el código **NFPA 704** (diamante de colores: Azul-Salud, Rojo-Inflamabilidad, Amarillo-Reactividad, Blanco-Especial).

### 3. Generación y Conducción de Vapor
*   **Calderas:** Estudiar a fondo la **Escocesa Marina** (Humotubular). Saber identificar sus partes: hogar, tubos de humo, cámara de humo, domo, válvulas de seguridad.
*   **Elementos de Seguridad:** Válvula de alivio, indicador de nivel (mínimo 2, uno de tubo de vidrio), manómetro con tubo sifón (para proteger el dial del calor).
*   **Trampas de Vapor:** Su función es eliminar el condensado y aire sin dejar escapar el vapor.
    *   **Tipos:** Termostáticas, mecánicas (flotador o cubeta invertida) y termodinámicas.

### 4. Instalaciones Eléctricas y Motores
*   **Selección de Conductores:**
    1.  Calcular corriente de diseño ($I_t$).
    2.  Seleccionar sección por tabla de fabricante según método de instalación.
    3.  Verificar caída de tensión ($\Delta U < 3\%$ o $5\%$).
*   **Protecciones:**
    *   **Termomagnética:** Protege al cable por sobrecargas (efecto térmico) y cortocircuitos (efecto magnético).
    *   **Diferencial:** Protege a las personas detectando fugas de corriente a tierra.
*   **Factor de Potencia (cos φ):** 
    *   *¿Por qué corregir?* Para evitar multas, sobrecalentamiento de cables y pérdida de capacidad en transformadores.
    *   *Equipos:* Banco de capacitores, motores sincrónicos, compensadores estáticos.
*   **Motores (MAT):** 
    *   **Arranque Estrella-Triángulo:** Reduce la corriente de arranque a $1/3$. Solo para motores con 6 bornas accesibles.
    *   **Variador de Frecuencia:** Permite control de velocidad y ahorro energético.
*   **Armónicos:** Distorsión de la onda generada por equipos electrónicos (variadores, UPS, luminarias LED). Se mitigan con filtros.

### 5. Luminotecnia
*   **Magnitudes Magnéticas:**
    *   **Flujo $(\text{lm})$:** Potencia luminosa total emitida.
    *   **Intensidad $(\text{cd})$:** Luz en una dirección específica.
    *   **Iluminancia $(\text{lux})$:** Luz que cae sobre una superficie ($E = \Phi / A$).
    *   **Luminancia $(\text{cd/m}^2)$:** Brillo percibido (luz reflejada).
*   **Índice de Reproducción Cromática (IRC):** Capacidad de la luz para mostrar los colores reales (escala 0-100).
*   **Diseño:** Método del flujo total para determinar cantidad de artefactos.

### 6. Refrigeración Industrial
*   **Ciclo de Compresión:** Compresión -> Condensación -> Expansión -> Evaporación.
    *   *Sobrecalentamiento:* Fundamental para asegurar que al compresor no ingrese líquido.
*   **Torres de Enfriamiento:** Se usan para enfriar el agua del condensador.
    *   *Tipos:* Tiro natural (pulverización/paneles), Tiro forzado (ventilador abajo), Tiro inducido (ventilador arriba).
*   **Balance Térmico:** Suma de calor por transmisión a través de paredes + infiltración de aire + carga del producto + calor de personas/motores.

---

## 💡 Preguntas Rápidas de Repaso

1.  **¿Qué pasa si aumento el caudal en una bomba?** El NPSH requerido sube y el disponible baja (más riesgo de cavitación).
2.  **¿Diferencia entre caño (pipe) y tubo (tube)?** El caño tiene medidas nominales; el tubo coincide su diámetro nominal con el externo real. Utilizado en intercambiadores.
3.  **¿Para qué sirve el condensador en un ciclo combinado?** Para convertir el vapor de salida de la turbina en agua para reiniciar el ciclo Rankine.
4.  **¿Qué es el "Arranque Suave"?** Un equipo electrónico que sube la tensión gradualmente para evitar golpes mecánicos y picos de corriente.

---
*Este informe fue generado analizando tus parciales 2024/2025 y los TPs de la carpeta actual.*
