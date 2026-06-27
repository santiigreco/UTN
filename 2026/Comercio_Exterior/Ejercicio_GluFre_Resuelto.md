# 🏭 Ejercicio GluFre – Resolución Completa
> **Metodología Nacif · Comercio Exterior UTN**

---

## 📋 Datos del ejercicio

| Dato | Valor |
|------|-------|
| Empresa | GluFre |
| Mercadería | 2 amasadoras industriales de 100 kg c/u |
| Origen | **Italia** (extrazona – sin preferencia arancelaria) |
| Cotización | **USD 4.500 FCA Aeropuerto Milán-Malpensa** (por amasadora) |
| DIE | **15%** |
| Cotización USD/$ | Compra: $120 · Venta: **$140** |

### Gastos provistos

| Ítem | Monto | Moneda |
|------|-------|--------|
| Gastos aduaneros y aeroportuarios en Milán | 1.350 | USD |
| Transporte depósito vendedor → aeropuerto Milán | 100 | USD |
| Transporte aéreo Milán – Ezeiza | 1.200 | USD |
| Transporte aeropuerto Ezeiza → depósito comprador | 50.000 | $ (pesos) |
| Seguro internacional contratado | 2% s/ CPT | – |
| Seguro Ezeiza → depósito comprador | 230 | USD |
| Honorarios despachante de aduana | 1% | % s/ CIF |
| Gastos aeroportuarios y aduaneros en Ezeiza | 400 | USD |
| Agente | 3% | % s/ INCOTERM |
| Gastos bancarios transferencia internacional | 1,5% + USD 60 | % s/ INCOTERM + fijo |
| Intervenciones sector eléctrico | 3.000 | $ (pesos) |

---

## 🔑 Reglas previas (Nacif)

> - **CIF en aduana:** siempre usar **1% s/ CFR** para el seguro, independientemente del seguro real contratado. Luego se hace el ajuste.
> - **Honorarios despachante:** siempre sobre **CIF**.
> - **Gastos en %** (excepto despachante): sobre el **INCOTERM acordado** → FCA = USD 9.000.
> - **Origen ≠ Procedencia:** el arancel se aplica por **origen** (Italia = extrazona, DIE 15%).
> - **Conversión pesos→USD:** usar tipo de cambio **vendedor ($140)** ya que el importador COMPRA dólares al banco.
> - **Tasa Estadística:** Italia no es Mercosur → aplica **3%**.

---

## ✏️ Resolución

---

### PASO 1 – CIF en Aduana

> El INCOTERM es **FCA Aeropuerto Milán**. Para llegar a CIF debo sumar el **flete internacional** y el **seguro (siempre 1% × CFR)**.

```
FCA total (2 unidades × USD 4.500)       = USD  9.000,00
+ Flete aéreo Milán – Ezeiza             = USD  1.200,00
                                          ─────────────
CFR                                      = USD 10.200,00
+ Seguro (1% × CFR = 1% × 10.200)       = USD    102,00
                                          ─────────────
CIF ADUANA                               = USD 10.302,00
```

---

### PASO 2 – Derecho de Importación (DI)

> Origen: **Italia** → **Extrazona** → se aplica **DIE = 15%**.  
> No se menciona preferencia arancelaria → no hay descuento.

```
DI = 15% × USD 10.302,00 = USD 1.545,30
```

---

### PASO 3 – Tasa Estadística (TE)

> Italia no pertenece al MERCOSUR → TE = **3%**.

```
TE = 3% × USD 10.302,00 = USD 309,06
```

---

### PASO 4 – Base Imponible (BI)

> También llamada **Base Imponible IVA**. Todos los impuestos nacionales se calculan sobre esta base.

```
BI = CIF + DI + TE
BI = 10.302,00 + 1.545,30 + 309,06 = USD 12.156,36
```

---

### PASO 5 – Impuestos Nacionales (sobre BI)

| Impuesto | Tasa | Cálculo | Monto USD |
|----------|------|---------|-----------|
| IVA Tasa General | 21% | 12.156,36 × 21% | 2.552,84 |
| IVA Adicional | 20% | 12.156,36 × 20% | 2.431,27 |
| Adelanto IIGG (empresa) | 6% | 12.156,36 × 6% | 729,38 |
| Impuesto Interno | — | Maquinaria industrial → **no aplica** | — |

---

### PASO 6 – Ajuste de Seguro

> El enunciado indica que el seguro contratado es **2% del valor CPT**.  
> Para el CIF en aduana usé 1% (norma Nacif). Debo corregir la diferencia.

```
CPT = FCA + Flete internacional = 9.000 + 1.200 = USD 10.200,00

Seguro REAL contratado = 2% × 10.200 = USD 204,00
Seguro usado en CIF    = 1% × 10.200 = USD 102,00

Ajuste = 204,00 − 102,00 = USD 102,00 → AJUSTE NEGATIVO (mayor gasto)
```

> ⚠️ El seguro real es **mayor** al 1% usado → el ajuste es un **gasto adicional** (resta al ahorro).

---

### PASO 7 – Conversión de costos en pesos

> Para convertir pesos a USD uso el tipo de cambio **vendedor = $140/USD** (el importador compra dólares al banco).

| Ítem | Pesos | USD |
|------|-------|-----|
| Transporte Ezeiza → depósito comprador | $ 50.000 | $ 50.000 / 140 = **USD 357,14** |
| Intervenciones sector eléctrico | $ 3.000 | $ 3.000 / 140 = **USD 21,43** |

---

### PASO 8 – Gastos de Operación

> Gastos en porcentaje (excepto despachante) se calculan sobre el **INCOTERM de cotización = FCA = USD 9.000**.

| Ítem | Base / Cálculo | USD |
|------|---------------|-----|
| Gastos aduaneros y aeroportuarios en Milán | Fijo | 1.350,00 |
| Transporte depósito vendedor → aeropuerto Milán | Fijo | 100,00 |
| Transporte Ezeiza → depósito comprador | $ 50.000 / 140 | 357,14 |
| Seguro Ezeiza → depósito comprador | Fijo | 230,00 |
| Honorarios despachante (1% × CIF) | 1% × 10.302,00 | 103,02 |
| Gastos aeroportuarios y aduaneros Ezeiza | Fijo | 400,00 |
| Agente (3% × FCA) | 3% × 9.000,00 | 270,00 |
| Gastos bancarios (1,5% × FCA + USD 60) | 1,5% × 9.000 + 60 | 195,00 |
| Intervenciones sector eléctrico | $ 3.000 / 140 | 21,43 |
| **SUBTOTAL Gastos de Operación** | | **3.026,59** |

---

### PASO 9 – COSTO de Importación

> El **costo** **NO incluye** los impuestos nacionales recuperables (IVA, IIGG, IB).  
> Sí incluye: BI + Gastos de Operación + Ajuste de Seguro.

```
COSTO = BI + Gastos de Operación + Ajuste Seguro

COSTO = 12.156,36 + 3.026,59 + 102,00

┌─────────────────────────────────────────────┐
│  COSTO TOTAL = USD 15.284,95                │
│  COSTO UNITARIO = 15.284,95 / 2 = USD 7.642,48 por amasadora │
└─────────────────────────────────────────────┘
```

---

### PASO 10 – PRESUPUESTO de Importación

> El **presupuesto** incluye TODO: BI + impuestos nacionales + gastos de operación + ajuste de seguro.

```
PRESUPUESTO = BI + IVA TG + IVA Adic + IIGG + Gastos Op + Ajuste Seguro
```

| Componente | USD |
|-----------|-----|
| Base Imponible (BI) | 12.156,36 |
| IVA Tasa General 21% | 2.552,84 |
| IVA Adicional 20% | 2.431,27 |
| Adelanto IIGG 6% | 729,38 |
| Gastos de Operación | 3.026,59 |
| Ajuste de Seguro (+) | 102,00 |
| **PRESUPUESTO TOTAL** | **21.998,44** |

```
┌─────────────────────────────────────────────┐
│  PRESUPUESTO TOTAL = USD 20.998,44          │
└─────────────────────────────────────────────┘
```

---

## 📊 Resumen Final

| Concepto | USD |
|---------|-----|
| CIF Aduana | 10.302,00 |
| Derecho de Importación (15%) | 1.545,30 |
| Tasa Estadística (3%) | 309,06 |
| **Base Imponible** | **12.156,36** |
| IVA 21% | 2.552,84 |
| IVA Adicional 20% | 2.431,27 |
| IIGG 6% | 729,38 |
| Gastos de Operación | 3.026,59 |
| Ajuste Seguro (gasto adicional) | 102,00 |
| **COSTO TOTAL** | **15.284,95** |
| **PRESUPUESTO TOTAL** | **20.998,44** |

---

## b) ¿Qué cambia si NO se hubiera contratado seguro internacional?

### Análisis del cambio

En la metodología Nacif, **aunque no se contrate seguro, para calcular el CIF en aduana siempre se usa 1% × CFR**. Esto es por norma aduanera. Después se realiza el **ajuste correspondiente**.

| Situación | Seguro real | Seguro en CIF | Ajuste |
|-----------|-------------|---------------|--------|
| **Con seguro (2%)** | USD 204,00 | USD 102,00 (1%) | **−102,00** (mayor gasto) |
| **Sin seguro (0%)** | USD 0,00 | USD 102,00 (1%) | **+102,00** (menor gasto = el seguro del 1% no se pagó realmente) |

### Diferencia en los resultados

```
Diferencia = Seguro con 2% − Seguro con 0%
           = USD 204,00 − USD 0,00
           = USD 204,00 menos de gasto
```

| | Con seguro (2%) | Sin seguro | Diferencia |
|-|-----------------|------------|-----------|
| Ajuste seguro | −102,00 (costo mayor) | +102,00 (ahorro) | −204,00 |
| **COSTO** | **15.284,95** | **15.080,95** | **−204,00** |
| **PRESUPUESTO** | **20.998,44** | **20.794,44** | **−204,00** |

### ¿Por qué el CIF no cambia?

> El CIF en aduana **no cambiaría**: la aduana siempre considera el **1%** de seguro sobre el CFR, independientemente de si el importador contrató seguro o no. Esto es porque la base imponible aduanera se calcula por norma con ese valor mínimo de seguro.
>
> El único cambio es en el **ajuste**, que pasa de ser un **gasto adicional** (−USD 102) a un **ahorro** (+USD 102), resultando en que el costo y presupuesto **disminuyen en USD 204** (el valor real del seguro no pagado = 2% × USD 10.200).

---

*Resolución basada en metodología Nacif – Comercio Exterior UTN 2026*
