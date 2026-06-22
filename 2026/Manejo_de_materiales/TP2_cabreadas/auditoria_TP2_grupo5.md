# Auditoria TP2 - Edificios Industriales - Grupo 5

Archivo auditado: `TP2 Edificios Industriales.pdf`
Consigna contrastada: `TP- Edificios Industriales.pdf`
Fecha de auditoria: 2026-06-22

## Resumen ejecutivo

- El informe no esta listo para entregar sin correcciones: hay errores de datos de grupo, una conclusion incorrecta en el Ejercicio 2, un dimensionamiento nodal invalido en el Ejercicio 3, una seccion de costos/desperdicio incompleta en el Ejercicio 4 y falta resolver P.1.5.
- La consigna plantea P.1.1, P.1.2, P.1.3, P.1.4 y P.1.5. El PDF entregable solo desarrolla ejercicios 1 a 4.
- Para grupo 5, los datos correctos son:
  - P.1.1: Q=3900 kg, nodo max=400 kg, sigma adm=1000 kg/cm2, sin coeficientes.
  - P.1.2: Q=3800 kg, nodo max=450 kg, sigma adm=1000 kg/cm2, coef nodos=1.25, sin coeficiente de vigas.
  - P.1.3: Q=2660 kg, nodo max=430 kg, sigma adm=1000 kg/cm2, coef nodos=1.50, coef vigas=1.80.
  - P.1.4: Q1=1200 kg, Q2=1800 kg, nodo max=430 kg, sigma adm=1000 kg/cm2, coef nodos=1.50, coef vigas=1.50.
  - P.1.5: Q=2400 kg, nodo max=400 kg, sigma adm=1000 kg/cm2, coef nodos=0.10, sin coeficiente de vigas, con nodos prohibidos N1-N3, N23-N25, N26 y N28.

## Observaciones generales

- La caratula no deja totalmente claro que el grupo de tabla usado es el grupo 5. Figura algo como `[N 545]`; conviene normalizarlo para que no parezca que se uso otro grupo.
- El indice omite P.1.5 y no refleja una resolucion completa de todos los enunciados de la consigna.
- En varios ejercicios se escribe "Nro niveles = 2^n", pero conceptualmente debe ser "Nro de nodos = 2^n", donde `n` es la cantidad de niveles de reparto.
- Falta una verificacion final ordenada por ejercicio: carga maxima resultante en nodo, capacidad admisible del nodo y condicion cumple/no cumple.
- Las imagenes estan, pero muchas formulas no definen claramente que distancia corresponde a cada tramo. Conviene agregar una tabla corta con luces, distancias a cargas y reacciones para que el docente pueda seguir el calculo sin interpretar colores.

## Ejercicio 1 - P.1.1

### Datos

Los datos usados coinciden con grupo 5:

- Q=3900 kg.
- Carga maxima por nodo=400 kg.
- Sigma admisible=1000 kg/cm2.
- Sin coeficiente de seguridad para nodos ni para vigas.

### Errores / puntos a corregir

- La formula de cantidad de niveles esta mal redactada: el que debe cumplir potencia de 2 es el numero de nodos, no el numero de niveles.
- No se muestra una verificacion final explicita de carga por nodo contra la capacidad admisible.
- La seleccion de perfil esta muy justa y debe escribirse con unidad y columna correcta de la tabla: `Wnec = 780 cm3`, no solo "x=781.9".
- Falta aclarar que IPN 320 se toma por `Wx=781.9 cm3`.
- La resolucion es valida solo si la geometria dibujada realmente deja la carga centrada en la viga final de 8 m. El informe deberia explicitar esa luz y esas distancias.

### Correccion / cierre recomendado

- Cantidad minima de nodos: `3900 / 400 = 9.75`, se redondea a 16 nodos, por lo tanto 4 niveles.
- Si el reparto queda simetrico, cada nodo final toma `3900 / 16 = 243.75 kg`, menor que 400 kg. Cumple.
- Para la viga de ultimo nivel, si se mantiene una luz de 8 m con carga centrada:
  - `Mmax = 3900 * 800 / 4 = 780000 kgcm`.
  - `Wnec = 780000 / 1000 = 780 cm3`.
  - Perfil minimo por tabla: IPN 320, `Wx=781.9 cm3`.

## Ejercicio 2 - P.1.2

### Datos

Hay un error importante de dato:

- El informe usa coeficiente de seguridad para nodos = 1.50.
- La tabla de grupo 5 indica coeficiente de seguridad para nodos = 1.25.

El resto coincide:

- Q=3800 kg.
- Carga maxima por nodo=450 kg.
- Sigma admisible=1000 kg/cm2.

### Errores / puntos a corregir

- La capacidad de trabajo por nodo no es `450/1.50 = 300 kg`, sino `450/1.25 = 360 kg`.
- La conclusion "los nodos 13, 14, 15 y 16 estan excedidos" es incorrecta para grupo 5.
- Con el dato correcto, la maxima carga nodal calculada por ustedes es `350.3125 kg`, menor que `360 kg`; por lo tanto el sistema si cumple en nodos.
- El informe no selecciona perfil IPN para P.1.2, aunque la consigna pide seleccionarlo para cada problema.
- Hay errores de escritura/arreglos en ecuaciones:
  - En Nivel 3 aparece una mezcla de `2.5 m` y `2.95 m`; el resultado `840.75 kg` corresponde a usar `2.95 m`, no `2.5 m`.
  - En Nivel 3, para una reaccion se escribe una resta con `1187.5`, pero el resultado correcto se obtiene restando `1401.25`.
  - En Nivel 1 se escribe `430.375/2`, pero el valor previo era `420.375`; el resultado `210.1875` corresponde a `420.375/2`.

### Correccion / cierre recomendado

- Capacidad admisible de trabajo por nodo: `450 / 1.25 = 360 kg`.
- Nodos necesarios: `3800 / 360 = 10.56`, se redondea a 16 nodos, o sea 4 niveles.
- Con las reacciones calculadas en el informe, la maxima carga final es `350.3125 kg`, entonces cumple.
- Para la viga de ultimo nivel, con la geometria dibujada de luz 8 m y carga a 5 m de un apoyo y 3 m del otro:
  - `Mmax = 3800 * 5 * 3 / 8 = 7125 kgm = 712500 kgcm`.
  - `Wnec = 712500 / 1000 = 712.5 cm3`.
  - Perfil minimo por tabla: IPN 320, `Wx=781.9 cm3`.

## Ejercicio 3 - P.1.3

### Datos

Los datos transcriptos coinciden con grupo 5:

- Q=2660 kg.
- Carga maxima por nodo=430 kg.
- Sigma admisible=1000 kg/cm2.
- Coeficiente de seguridad para nodos=1.50.
- Coeficiente de seguridad para vigas=1.80.

### Errores / puntos a corregir

- El calculo de cantidad de nodos ignora el coeficiente de seguridad para nodos.
- El informe calcula `2660/430 = 6.18 -> 8 nodos`, pero debia calcularse con capacidad de trabajo:
  - `430 / 1.50 = 286.67 kg/nodo`.
  - `2660 / 286.67 = 9.28`, por lo que la primera potencia de 2 suficiente es 16 nodos, no 8.
- La estructura dibujada con 8 nodos no cumple:
  - Nodos con `595.84 kg` superan `286.67 kg`.
  - Nodos con `468 kg` superan `286.67 kg`.
- Falta la verificacion nodal, que habria mostrado inmediatamente que el esquema es invalido.
- La seleccion de perfil esta mal:
  - Se escribe `2660 * 400 / 1000 = 780`, pero aritmeticamente eso da `1064`, no `780`.
  - La linea parece copiada del Ejercicio 1.
  - Se ignora el coeficiente de seguridad para vigas `1.80`.
  - La distancia `400 cm` no corresponde a la viga final dibujada, que trabaja con una luz de 2.5 m y una carga excentrica.

### Correccion / cierre recomendado

- Redisenar el sistema con al menos 16 nodos y volver a calcular reacciones. Por la excentricidad, no alcanza con contar nodos: hay que verificar el nodo mas cargado.
- Si solo se evaluara la viga final actualmente dibujada, con luz 2.5 m y carga a 1.1 m de un apoyo:
  - Reacciones: `RA=1489.6 kg`, `RB=1170.4 kg`.
  - `Mmax = 1489.6 * 1.1 m = 1638.56 kgm = 163856 kgcm`.
  - Aplicando coeficiente de vigas 1.80: `Wnec = 163856 * 1.80 / 1000 = 294.94 cm3`.
  - Por tabla alcanzaria IPN 240 (`Wx=354.2 cm3`) para esa viga puntual.
- Pero como el esquema nodal es invalido, el perfil final debe recalcularse despues del nuevo redisenio.

## Ejercicio 4 - P.1.4

### Datos

Hay un error de dato:

- El informe usa carga maxima por nodo = 450 kg.
- La tabla de grupo 5 indica carga maxima por nodo = 430 kg.

El resto coincide:

- Q1=1200 kg.
- Q2=1800 kg.
- Sigma admisible=1000 kg/cm2.
- Coeficiente de seguridad para nodos=1.50.
- Coeficiente de seguridad para vigas=1.50.

### Errores / puntos a corregir

- La capacidad de trabajo por nodo debe ser `430/1.50 = 286.67 kg`, no `450/1.50 = 300 kg`.
- El error no cambia la cantidad minima de nodos: `3000/286.67 = 10.47`, se redondea a 16 nodos.
- Falta explicitar la verificacion nodal final. Con los valores del informe, el maximo nodo final es `218.75 kg`, por lo que cumpliria incluso con el dato correcto de 430 kg.
- En Nivel 1 hay errores de tipeo:
  - Se escribe `738.5/2 = 218.75`, pero deberia ser `437.5/2 = 218.75`.
  - Lo mismo se repite para el otro ramal B.
- La seleccion de perfil IPN 340 es defendible con la geometria planteada:
  - Reacciones de la viga final: `RA=1250 kg`, `RB=1750 kg`.
  - Momentos: `M1=500000 kgcm`, `M2=525000 kgcm`.
  - Con coeficiente de vigas 1.50: `Wnec = 525000 * 1.50 / 1000 = 787.5 cm3`.
  - IPN 320 no alcanza (`Wx=781.9 cm3`), por lo tanto IPN 340 (`Wx=923.5 cm3`) es el primer perfil que cumple.

### Costos, compras, peso y desperdicio

Esta parte esta incompleta respecto de la consigna adicional.

- Se indica un proveedor/link, pero no se informa precio unitario, fecha de consulta, moneda ni condicion de compra.
- No se calcula el costo del material.
- No se calcula el costo total del sistema. Solo se calcula mano de obra.
- No se calcula desperdicio en metros, peso, porcentaje y costo.
- La compra propuesta es inconsistente: se dice `60.9 m / 12 m = 5.075 vigas`, luego "se compran 5 vigas de 12 metros y una de 1 metro". Si la medida comercial es 12 m, normalmente se comprarian 6 barras de 12 m, salvo que el proveedor venda cortes por metro. Eso debe justificarse.
- El peso total se calcula con 58 m, pero antes se habia sumado 5% extra y se habia llegado a 60.9 m.
  - Peso con 58 m: `67.9 * 58 = 3938.2 kg`.
  - Peso con 60.9 m: `67.9 * 60.9 = 4135.11 kg`.
  - Peso si se compran 61 m: `67.9 * 61 = 4141.9 kg`.
  - Peso si se compran 6 barras de 12 m: `67.9 * 72 = 4888.8 kg`.
- Falta un plan de corte que respete la restriccion de no mas de una union soldada por tramo de VRC.
- Las horas de mano de obra no estan justificadas con criterio o rendimiento. La suma da 70 h y el calculo `70 * 35 = 2450 USD` esta bien, pero queda aislado porque falta material y desperdicio.

### Correccion / cierre recomendado

- Corregir dato de nodo maximo a 430 kg.
- Agregar verificacion nodal: `max nodo = 218.75 kg < 286.67 kg`, cumple.
- Mantener IPN 340 si se conserva la geometria de viga final.
- Completar compra y costo:
  - Definir si se compra por barra comercial de 12 m o por metro.
  - Registrar precio unitario y fecha.
  - Hacer plan de corte.
  - Calcular material comprado, material usado, recortes reutilizables, desperdicio neto en m/kg/%/$.
  - Calcular costo material + costo mano de obra + costo total.

## Ejercicio faltante - P.1.5

### Datos grupo 5

- Q=2400 kg.
- Carga maxima por nodo=400 kg.
- Sigma admisible=1000 kg/cm2.
- Coeficiente de seguridad para nodos=0.10.
- Sin coeficiente de seguridad para vigas.
- Nodos no utilizables: N1, N2, N3, N23, N24, N25, N26 y N28.

### Error principal

- El ejercicio no esta resuelto en el entregable.

### Que hay que corregir

- Incorporar P.1.5 completo: planta, vista A, vista B, calculo de reacciones, verificacion nodal y perfil IPN de la viga final.
- Aclarar la interpretacion del coeficiente 0.10. Como es menor a 1, no puede usarse mecanicamente igual que los coeficientes 1.25, 1.50, etc. de ejercicios anteriores sin explicar el criterio.
- Si se interpreta como factor de disponibilidad de carga en nodo, la capacidad por nodo seria `400 * 0.10 = 40 kg`, y `2400/40 = 60 nodos`, imposible con la geometria disponible y con nodos prohibidos. En ese caso debe explicarse una solucion estructural: refuerzo de cabreadas, redistribucion a otros elementos, cambio de punto de anclaje o aumento de capacidad, sin modificar arbitrariamente coeficientes.
- Si el docente pretendia otra interpretacion, debe quedar escrita porque el numero 0.10 es ambiguo frente al metodo usado en los ejercicios 2, 3 y 4.

## Lista priorizada de correcciones antes de entregar

1. Agregar el ejercicio P.1.5 completo o justificar por que no aplica. Segun la consigna, aplica.
2. Corregir Ejercicio 3: recalcular cantidad de nodos con coeficiente 1.50 y redisenar. El esquema actual no cumple.
3. Corregir Ejercicio 2: coeficiente correcto 1.25, capacidad 360 kg/nodo, conclusion pasa de "no cumple" a "cumple"; agregar perfil IPN 320.
4. Corregir Ejercicio 4: carga maxima por nodo 430 kg, no 450 kg; agregar verificacion nodal.
5. Completar costos/desperdicio del Ejercicio 4: precio material, compra comercial, plan de corte, peso comprado/usado, desperdicio en peso/porcentaje/costo y costo total.
6. Revisar todos los textos copiados: hay lineas con resultados incompatibles con las cuentas, especialmente perfil del Ejercicio 3 y reacciones con valores mal tipeados.
7. Agregar tabla resumen final por ejercicio: nodos usados, max nodo, capacidad admisible, cumple/no cumple, Wnec, IPN seleccionado.
