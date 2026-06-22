# Guia de estudio - Investigacion Operativa - 1er parcial

Basada en:

- `2026/Inv_Operativa/invo.py/1er parcial`
- `2026/Inv_Operativa/1er Parcial de años anteriores-20260418`
- Apuntes propios de clase en `2026/Inv_Operativa/1P _ Apuntes operativa`

## 0. Mapa del parcial

En los parciales recientes se repite una estructura bastante clara:

| Tema | Que suelen pedir | Peso observado |
| --- | --- | --- |
| CPM / PERT | Grafo, fechas tempranas/tardias, margen total, camino critico, Gantt o correccion de red | Alto |
| Simulacion | Corridas Monte Carlo con tiempos exponenciales, comparacion con modelo teorico, stock/fila/espera | Alto |
| Nacimiento y muerte / Markov continuo | Matriz generadora, regimen permanente, servidores activos, Ley de Little | Medio |
| Filas de espera | M/M/1 o M/M/s, indicadores, estabilidad, costos o decision de agregar servidor | Medio |
| Markov discreto | Matriz de transicion, pasos, largo plazo, estado estacionario, ergodicidad | Medio |
| Teoria asociada | Justificar metodo, interpretar parametros, V/F | Acompana cada practico |

Orden recomendado para resolver el parcial:

1. Leer todos los puntos y marcar unidades: minutos, horas, dias.
2. Resolver primero lo que da datos para otro punto. En 2025, por ejemplo, `W` de filas/nacimiento-muerte alimentaba duraciones de CPM.
3. En cada ejercicio, escribir el modelo antes de calcular: `M/M/1`, `M/M/s`, cadena discreta, CTMC, CPM o PERT.
4. Dejar siempre una frase de interpretacion final: no alcanza con tirar un numero.

## 1. Simulacion y Monte Carlo

### Como reconocerlo

El enunciado dice cosas como:

- "Simule 5, 10 o 500 llegadas/corridas".
- "Llegan segun Poisson" o "tiempos entre arribos exponenciales".
- "Use numeros aleatorios".
- "Compare el resultado simulado con el modelo teorico".
- "Calcule tiempo de espera, stock, cantidad en sistema o si se rompe una condicion".

### Ideas base

Si los arribos siguen Poisson con tasa `lambda`, entonces el tiempo entre arribos sigue exponencial:

```text
T_arribo = ln(1 / U) / lambda
```

Si el servicio tiene tasa `mu`, entonces:

```text
T_servicio = ln(1 / U) / mu
```

Donde `U` es un numero aleatorio uniforme entre 0 y 1.

Si te dan tiempo medio, converti a tasa:

```text
lambda = 1 / tiempo_medio_entre_arribos
mu = 1 / tiempo_medio_de_servicio
```

Ejemplos:

- Llega 1 persona cada 20 minutos: `lambda = 3 personas/hora`.
- Atiende 1 cliente cada 10 minutos: `mu = 6 clientes/hora`.
- Procesa 20 cajas cada 2 horas: `mu = 10 cajas/hora`.

### Paso a paso para una simulacion de cola con un servidor

Arma una tabla con estas columnas:

| Columna | Que significa |
| --- | --- |
| `i` | numero de llegada |
| `U1` | aleatorio para llegada |
| `T entre arribos` | `ln(1/U1)/lambda` |
| `Llegada al sistema` | suma acumulada de tiempos entre arribos |
| `U2` | aleatorio para servicio |
| `T servicio` | `ln(1/U2)/mu` o valor segun tabla discreta |
| `Inicio servicio` | `max(llegada_i, fin_servicio_{i-1})` |
| `Espera Wq` | `inicio_servicio - llegada` |
| `Fin servicio` | `inicio_servicio + T_servicio` |
| `Tiempo en sistema Ws` | `fin_servicio - llegada` |
| `Lq` | cantidad esperando cuando llega |
| `L` | cantidad en sistema |

Resolucion:

1. Converti todas las tasas a la misma unidad.
2. Genera o usa los numeros aleatorios dados.
3. Transforma `U` en tiempo exponencial con `ln(1/U)/tasa`.
4. Acumula los tiempos entre arribos. Este es el error mas comun: no se usa el tiempo suelto, se usa la suma acumulada.
5. Para cada llegada, calcula cuando puede empezar a ser atendida.
6. Si llega antes de que termine el servicio anterior, espera.
7. Calcula promedios: `promedio(Wq)`, `promedio(Ws)`, `promedio(Lq)`, `promedio(L)`.
8. Compara con el objetivo del enunciado: por ejemplo "espera menor a 8 minutos" o "no mas de 3 personas adentro".
9. Escribi conclusion: "Con estas corridas, el sistema parece/no parece cumplir; con mas corridas converge mejor".

### Si la variable es discreta

Ejemplo: cantidad de errores:

| Errores | Probabilidad | Acumulada | Intervalo |
| --- | ---: | ---: | --- |
| 0 | 0.70 | 0.70 | `0 <= U <= 0.70` |
| 1 | 0.10 | 0.80 | `0.70 < U <= 0.80` |
| 2 | 0.05 | 0.85 | `0.80 < U <= 0.85` |
| 3 | 0.10 | 0.95 | `0.85 < U <= 0.95` |
| 4 o mas | 0.05 | 1.00 | `0.95 < U <= 1.00` |

Pasos:

1. Armar probabilidad acumulada.
2. Convertir cada acumulado en intervalo.
3. Para cada `U`, buscar en que intervalo cae.
4. Promediar o contar lo que pide el enunciado.

### Tips de examen

- Si el enunciado dice Poisson, en simulacion casi siempre vas a samplear exponenciales para tiempos entre eventos.
- No uses la funcion de densidad para decidir intervalos. Usa la acumulada.
- `U = 0` no sirve para `ln(1/U)`. Si aparece 0, normalmente se reemplaza o se usa otro numero.
- Si comparas contra teoria, pocas corridas pueden diferir mucho. La justificacion correcta es que Monte Carlo converge al aumentar `N`.
- En Excel, el patron visto en resoluciones es:

```text
T = (1 / tasa) * LN(1 / U)
llegada_i = llegada_{i-1} + T_i
inicio_i = MAX(llegada_i, fin_{i-1})
espera_i = inicio_i - llegada_i
fin_i = inicio_i + servicio_i
```

## 2. Cadenas de Markov de parametro discreto

### Como reconocerlo

El enunciado habla de:

- Estados finitos: pisos, canchas, maquina normal/reparacion/fuera de servicio, fichas de un juego.
- Probabilidades de pasar de un estado a otro por ciclo, minuto, dia o semana.
- "A largo plazo", "estado estacionario", "matriz de transicion", "probabilidad luego de n pasos".

### Convencion importante

En la materia se usa normalmente:

- Filas: estado desde donde salgo.
- Columnas: estado al que llego.
- Cada fila suma 1.
- El vector de estado es fila.

```text
p(t+1) = p(t) * P
p(t+n) = p(t) * P^n
```

### Paso a paso para armar la matriz

1. Defini los estados y escribilos siempre en el mismo orden.
2. Para cada estado actual, completa una fila de la matriz.
3. Si falta una probabilidad, calculala como:

```text
faltante = 1 - suma(probabilidades conocidas de la fila)
```

4. Verifica que todas las filas sumen 1.
5. Arma el vector inicial.
6. Calcula lo pedido:
   - Un paso: `p0 * P`.
   - n pasos: `p0 * P^n`.
   - Transicion de i a j en n pasos: entrada `(i,j)` de `P^n`.
   - Largo plazo: estado estacionario.

### Estado estacionario

Se busca un vector `pi` tal que:

```text
pi = pi * P
sum(pi_i) = 1
```

Metodo practico:

1. Escribi una ecuacion por estado desde `pi = piP`.
2. Reemplaza una ecuacion por `sum(pi_i)=1`.
3. Resolve el sistema.

Metodo Excel/Python:

1. Elevar `P` muchas veces: `P^20`, `P^50`, etc.
2. Si converge, las filas tienden al vector estacionario.

### Ergodicidad

Una cadena es ergodica si:

1. Es irreducible: todos los estados se comunican entre si.
2. Es aperiodica: no queda atrapada en ciclos obligatorios.

Para que sirve saberlo:

- Si es ergodica, existe un estacionario unico.
- El largo plazo no depende del estado inicial.

### Estados absorbentes

Un estado absorbente tiene:

```text
P_ii = 1
```

Ejemplo tipico: juego de fichas donde `0` es perder y `4` es ganar.

Pasos:

1. Defini estados: `0, 1, 2, 3, 4`.
2. Estados `0` y `4` son absorbentes.
3. Estados intermedios pasan a `i+1` o `i-1`.
4. La matriz queda con filas absorbentes en los extremos.

Tip: una cadena con absorbentes no suele tener estacionario unico tipo "largo plazo repartido"; a largo plazo termina en absorbentes. Si preguntan largo plazo, interpreta si quieren probabilidad de absorcion o matriz de transicion.

### Errores comunes

- Transponer la matriz: poner columnas como origen y filas como destino.
- Olvidar completar la probabilidad de quedarse en el mismo estado.
- Calcular `P*n` en lugar de `P^n`.
- Confundir "probabilidad en el tercer paso" con "probabilidad despues de tres transiciones".
- Decir que siempre hay estado estacionario. No siempre: se necesita condicion de convergencia.

## 3. Markov continuo y procesos de nacimiento y muerte

### Como reconocerlo

El enunciado habla de:

- Tasas de falla y reparacion.
- Cantidad de equipos activos, autos en taller, servidores funcionando.
- Capacidad finita del sistema.
- Matriz generadora, matriz infinitesimal o intensidad de transiciones.
- Regimen permanente.

### Diferencia clave con Markov discreto

En Markov discreto la matriz tiene probabilidades y las filas suman 1.

En Markov continuo la matriz generadora `Q` tiene tasas y las filas suman 0.

```text
q_ij >= 0 para i != j
q_ii = - suma(q_ij para j != i)
```

### Paso a paso para matriz generadora

1. Defini el estado como una cantidad: por ejemplo `n = cantidad de clientes`, `n = servidores activos`, `n = equipos rotos`.
2. Dibuja los estados posibles: `0, 1, 2, ..., N`.
3. Identifica nacimientos: transiciones `n -> n+1` con tasa `lambda_n`.
4. Identifica muertes: transiciones `n -> n-1` con tasa `mu_n`.
5. Completa la matriz:
   - Arriba de la diagonal: nacimientos.
   - Abajo de la diagonal: muertes.
   - Diagonal: negativo de la suma de la fila.
6. Verifica que cada fila sume 0.

### Regimen permanente en nacimiento y muerte

Para estados `0..N`:

```text
p_n = p_0 * productoria(lambda_i / mu_{i+1}) desde i=0 hasta n-1
sum(p_n) = 1
```

Si las tasas son constantes:

```text
p_n = p_0 * (lambda/mu)^n
p_0 = 1 / sum((lambda/mu)^n, n=0..N)
```

Ojo: en ejercicios de fallas/reparaciones, primero defini que significa "n". Si `n` es cantidad de servidores activos, las fallas bajan el estado y las reparaciones lo suben. Si `n` es cantidad de servidores caidos, pasa al reves. La formula funciona, pero las tasas quedan ubicadas distinto.

### Ley de Little

Se usa mucho para convertir cantidad promedio en tiempo promedio:

```text
L = lambda_efectiva * W
W = L / lambda_efectiva
```

En parciales 2025, el `W` calculado se usaba como duracion de una tarea del ejercicio CPM. No lo dejes en dias si CPM esta en horas.

### Tips de examen

- La diagonal de `Q` siempre es negativa o cero.
- Las filas de `Q` suman 0, no 1.
- No mezcles tasas con probabilidades. Una tasa puede ser mayor que 1.
- En sistemas finitos, en los bordes no hay transicion hacia afuera. En `0` no hay muerte; en `N` no hay nacimiento.
- Si te piden "grafo asociado", dibuja nodos y flechas con tasas, no con probabilidades.

## 4. Filas de espera

### Como reconocerlo

El enunciado habla de:

- Llegadas Poisson.
- Tiempo de atencion exponencial.
- Uno o varios servidores.
- Clientes esperando.
- Agregar maquina, vendedor, tecnico, dron, operario.
- Indicadores `Lq`, `Ls`, `Wq`, `Ws`, `P0`, `rho`.

### Notacion Kendall

```text
M/M/1: llegadas Poisson, servicio exponencial, 1 servidor
M/M/s: llegadas Poisson, servicio exponencial, s servidores
```

### Paso cero: unidades

Antes de cualquier formula:

1. Elegi una unidad: horas suele ser la mas practica.
2. Converti `lambda` a clientes/hora.
3. Converti `mu` a clientes/hora por servidor.
4. Si hay `s` servidores, la capacidad total es `s * mu`, pero `mu` sigue siendo por servidor.

Ejemplos:

```text
1 cliente cada 12 min -> lambda = 5 clientes/hora
1 servicio cada 10 min -> mu = 6 clientes/hora
2 servidores -> capacidad total = 12 clientes/hora
```

### M/M/1

Condicion de estabilidad:

```text
rho = lambda / mu
rho < 1
```

Formulas:

```text
P0 = 1 - rho
Pn = rho^n * P0
Ws = 1 / (mu - lambda)
Wq = lambda / (mu * (mu - lambda))
Lq = lambda * Wq
Ls = lambda * Ws = rho / (1 - rho)
```

Interpretacion:

- `rho` alto: servidor muy ocupado.
- `rho >= 1`: sistema inestable, la cola tiende a crecer.
- `rho < 1` no significa que nunca haya fila. Significa que no explota en promedio.

### M/M/s

Con `s` servidores:

```text
rho = lambda / (s * mu)
```

Condicion:

```text
rho < 1
```

Formulas principales:

```text
P0 = 1 / [ sum_{n=0}^{s-1} ((lambda/mu)^n / n!)
           + ((lambda/mu)^s / (s! * (1-rho))) ]

Lq = P0 * ((lambda/mu)^s * rho) / (s! * (1-rho)^2)
Wq = Lq / lambda
Ws = Wq + 1/mu
Ls = lambda * Ws
```

### Si piden costo

El costo total suele ser:

```text
C_total = C_oportunidad + C_operativo
C_oportunidad = lambda * Ws * e
C_operativo = s * Cm
```

Pasos:

1. Calcular indicadores para `s=1`.
2. Calcular costo total.
3. Repetir para `s=2`, `s=3`, etc.
4. Elegir el menor costo o justificar si conviene agregar servidor.

### Si piden comparar formula vs simulacion

1. Calcula indicadores teoricos con M/M/1 o M/M/s.
2. Simula llegadas y servicios.
3. Promedia `Wq`, `Ws`, `Lq`, `L`.
4. Compara:
   - Si hay pocas corridas, puede haber diferencia por variabilidad.
   - Si hay muchas corridas, deberia acercarse.
5. Conclui si el sistema cumple la condicion del enunciado.

### Errores comunes

- Usar `mu` total en formulas que piden `mu` por servidor.
- Comparar minutos con horas.
- Decir que `rho < 1` implica que no hay espera.
- Olvidar que `Ws = Wq + 1/mu`.
- Usar `lambda` de arribos cuando el sistema tiene capacidad finita y la tasa efectiva cambia.

## 5. CPM - Metodo del Camino Critico

### Como reconocerlo

El enunciado da:

- Tabla de tareas.
- Predecesoras.
- Duracion.
- Pedido de grafo, fechas tempranas/tardias, margenes, camino critico o Gantt.

### Vocabulario de la materia

En la teoria aparece:

```text
Ft_i = fecha temprana del evento i
FT_i = fecha tardia del evento i
D_ij = duracion de la tarea i-j
MT_ij = margen total
ML_ij = margen libre
MI_ij = margen independiente
```

Formulas:

```text
MT_ij = FT_j - Ft_i - D_ij
ML_ij = Ft_j - Ft_i - D_ij
MI_ij = Ft_j - FT_i - D_ij
```

Tarea critica:

```text
MT = 0
```

### Paso a paso practico con tabla de tareas

Si el enunciado viene como tabla `Actividad - Predecesoras - Duracion`, resolve asi:

1. Lista tareas sin predecesoras: arrancan en tiempo 0.
2. Para cada tarea:

```text
Inicio temprano (ES) = max(fin temprano de predecesoras)
Fin temprano (EF) = ES + duracion
```

3. La duracion minima del proyecto es el mayor `EF` final.
4. Hacia atras:

```text
Fin tardio (LF) = min(inicio tardio de sucesoras)
Inicio tardio (LS) = LF - duracion
```

5. Margen total:

```text
MT = LS - ES = LF - EF
```

6. Camino critico: tareas con `MT = 0`, conectadas de inicio a fin.
7. Si piden Gantt:
   - A fecha temprana: cada tarea arranca en `ES`.
   - A fecha tardia: cada tarea arranca en `LS`.

### Si piden grafo con tareas como flechas

La teoria de la materia usa nodos como eventos y arcos como tareas.

Pasos:

1. Crea un nodo inicial.
2. Dibuja tareas sin predecesoras saliendo del inicio.
3. Las tareas que dependen de otra salen del nodo donde termina su predecesora.
4. Si una tarea depende de varias, no puede arrancar hasta que todas confluyan.
5. Si el grafo no permite representar bien una dependencia, agrega tarea ficticia de duracion 0.

### Tareas ficticias

Se usan para representar precedencias sin agregar tiempo real.

Reglas:

- Duracion 0.
- Pueden estar en el camino critico si su margen total es 0.
- No representan trabajo real.
- Sirven para que dos tareas no queden con la misma cola y cabeza si tienen dependencias distintas.

### Como detectar una red mal confeccionada

Revisa:

- Una tarea no puede iniciar antes de que terminen todas sus predecesoras.
- No deben aparecer ciclos.
- Inicio y fin deben ser eventos puntuales.
- Tareas distintas no deberian quedar indistinguibles si tienen distinta dependencia.
- Si una tarea tiene predecesoras `C, D, E`, el grafo debe obligarla a esperar a las tres.

### Tips de examen

- Si te quedas sin tiempo, al menos calcula `ES`, `EF`, `LS`, `LF`, `MT`. El camino critico sale de ahi.
- No marques camino critico solo por "el camino mas largo visual"; justificá con `MT = 0`.
- En una bifurcacion hacia adelante se usa maximo. En la vuelta hacia atras se usa minimo.
- Si una duracion viene de otro punto, resolve ese punto antes o usa el valor fallback si el enunciado lo da.

## 6. PERT

### Como reconocerlo

El enunciado da tres tiempos:

```text
to = optimista
tn = normal / mas probable
tp = pesimista
```

Y pide riesgo, desvio, probabilidad de terminar antes de una fecha o comparar proyectos.

### Paso a paso

1. Para cada tarea calcula tiempo esperado:

```text
Te = (to + 4*tn + tp) / 6
```

2. Calcula desvio de cada tarea:

```text
sigma = (tp - to) / 6
varianza = sigma^2
```

3. Usa `Te` como duracion y resolve CPM.
4. Identifica camino critico.
5. Para el proyecto:

```text
media_proyecto = suma(Te de tareas criticas)
varianza_proyecto = suma(varianzas de tareas criticas)
sigma_proyecto = sqrt(varianza_proyecto)
```

6. Si piden probabilidad de terminar antes de `T`:

```text
Z = (T - media_proyecto) / sigma_proyecto
P(T_proyecto <= T) = Phi(Z)
```

### PERT vs CPM

CPM:

- Tiempos conocidos/deterministicos.
- Sirve para calendarizar y encontrar camino critico.
- No mide riesgo temporal.

PERT:

- Tiempos estimados/probabilisticos.
- Usa optimista, mas probable y pesimista.
- Permite calcular dispersion y probabilidad de cumplir una fecha.

Frase de examen:

> Uso CPM cuando las duraciones son conocidas o suficientemente confiables. Uso PERT cuando las duraciones son inciertas y necesito incorporar riesgo mediante tiempo esperado y dispersion.

## 7. Teoria corta que suele acompanar los practicos

### Etapas de un estudio de simulacion

Orden razonable:

1. Definir el sistema.
2. Definir el modelo.
3. Recolectar datos.
4. Validar el modelo.
5. Ejecutar corridas.
6. Analizar resultados.
7. Implementar o ajustar.

Tip: si el resultado no valida contra experto o realidad, no "se fuerza"; se revisa informacion, supuestos, distribuciones y logica.

### Markov discreto vs continuo

| Aspecto | Discreto | Continuo |
| --- | --- | --- |
| Parametro | pasos, dias, semanas, ciclos | tiempo continuo |
| Matriz | probabilidades `P` | tasas `Q` |
| Filas suman | 1 | 0 |
| Diagonal | probabilidad de permanecer | tasa negativa de salida |
| Ejemplo | ascensor por hora, cancha por semana | fallas y reparaciones |

### Filas vs nacimiento y muerte

Filas de espera:

- Caso particular de nacimiento y muerte.
- Se enfoca en clientes, espera, servidores e indicadores operativos.
- Suele asumir cola infinita salvo que digan capacidad finita.

Nacimiento y muerte:

- Mas general.
- Sirve para estados de cantidad en sistemas finitos o infinitos.
- Se modela con tasas de subida y bajada de estado.

### Interpretacion de rho

```text
rho = utilizacion del sistema
```

- Cerca de 0: mucha capacidad ociosa.
- Cerca de 1: sistema muy cargado.
- Mayor o igual a 1: inestable si la cola es infinita.

## 8. Checklists rapidos por ejercicio

### Simulacion

- [ ] Converti tasas a la misma unidad.
- [ ] Use acumulada o transformada inversa.
- [ ] Acumule tiempos de llegada.
- [ ] Use `MAX(llegada, fin anterior)` para inicio de servicio.
- [ ] Calcule espera y fin de servicio.
- [ ] Compare promedios con objetivo.
- [ ] Aclare que con mas corridas mejora la convergencia.

### Markov discreto

- [ ] Defini estados en orden.
- [ ] Filas son origen, columnas destino.
- [ ] Cada fila suma 1.
- [ ] Complete probabilidades faltantes.
- [ ] Use `p(t+n)=p(t)P^n`.
- [ ] Para largo plazo resolvi `pi=piP` y `sum pi=1`.
- [ ] Verifique ergodicidad si corresponde.

### Markov continuo / nacimiento-muerte

- [ ] Defini que representa el estado `n`.
- [ ] Identifique nacimientos y muertes.
- [ ] Arme `Q` con tasas, no probabilidades.
- [ ] Diagonal negativa igual a la suma de salidas.
- [ ] Filas suman 0.
- [ ] Para regimen permanente, normalice probabilidades.
- [ ] Use Ley de Little con unidades correctas.

### Filas

- [ ] Identifique `M/M/1` o `M/M/s`.
- [ ] Calcule `lambda` y `mu` en la misma unidad.
- [ ] Calcule `rho`.
- [ ] Si `rho >= 1`, declare inestabilidad.
- [ ] Calcule `Wq`, `Ws`, `Lq`, `Ls`.
- [ ] Si hay costos, compare escenarios de cantidad de servidores.
- [ ] Interprete el resultado en lenguaje del problema.

### CPM / PERT

- [ ] Liste predecesoras.
- [ ] Forward pass: maximo de predecesoras.
- [ ] Backward pass: minimo de sucesoras.
- [ ] Calcule margen total.
- [ ] Camino critico = `MT = 0`.
- [ ] Si es PERT, primero calcule `Te` y `sigma`.
- [ ] Si piden probabilidad, use normal con `Z`.

## 9. Plan de estudio recomendado

### Dia 1 - Simulacion y filas

1. Repasar transformada inversa exponencial.
2. Hacer una tabla de simulacion de 10 llegadas a mano/Excel.
3. Resolver M/M/1 con los mismos datos.
4. Comparar simulacion vs teoria.
5. Repetir con M/M/2.

### Dia 2 - Markov

1. Armar matrices de transicion discretas.
2. Hacer ejercicios de `P^n`.
3. Resolver estacionario con sistema de ecuaciones.
4. Practicar un ejemplo absorbente.
5. Armar una matriz generadora `Q` de nacimiento y muerte.

### Dia 3 - CPM / PERT

1. Resolver un CPM completo desde tabla de predecesoras.
2. Practicar grafo con tareas ficticias.
3. Calcular margenes total y libre.
4. Resolver un PERT con `to`, `tn`, `tp`.
5. Calcular probabilidad de terminar antes de una fecha.

### Dia 4 - Parcial mixto

1. Tomar un parcial 2024 o 2025.
2. Resolverlo en tiempo.
3. Corregir contra la resolucion.
4. Marcar errores por tipo: unidades, matriz, formula, interpretacion.
5. Rehacer solo los puntos fallados.

## 10. Frases utiles para justificar

- "El sistema es estable porque `rho < 1`; esto no implica ausencia de fila, sino que la cola no crece indefinidamente en promedio."
- "La simulacion puede diferir del valor teorico por la cantidad limitada de corridas y por la variabilidad de los numeros aleatorios."
- "La matriz de transicion esta bien definida porque cada fila suma 1."
- "La matriz generadora esta bien definida porque las tasas fuera de la diagonal son no negativas y cada fila suma 0."
- "La tarea es critica porque su margen total es cero; cualquier retraso retrasa la finalizacion del proyecto."
- "PERT es mas adecuado que CPM cuando los tiempos son inciertos porque permite incorporar dispersion y riesgo."

## 11. Mini formulario

```text
Exponencial:
T = ln(1/U) / tasa

M/M/1:
rho = lambda/mu
P0 = 1-rho
Wq = lambda / (mu*(mu-lambda))
Ws = 1/(mu-lambda)
Lq = lambda*Wq
Ls = lambda*Ws

M/M/s:
rho = lambda/(s*mu)
P0 = 1 / [sum_{n=0}^{s-1} ((lambda/mu)^n/n!) + ((lambda/mu)^s/(s!*(1-rho)))]
Lq = P0*((lambda/mu)^s*rho)/(s!*(1-rho)^2)
Wq = Lq/lambda
Ws = Wq + 1/mu
Ls = lambda*Ws

Markov discreto:
p(t+n) = p(t)*P^n
pi = pi*P
sum(pi)=1

Markov continuo:
q_ii = -sum(q_ij, j != i)
filas de Q suman 0

Nacimiento-muerte:
p_n = p_0 * productoria(lambda_i / mu_{i+1})
sum(p_n)=1

CPM:
EF = ES + duracion
ES = max(EF predecesoras)
LS = LF - duracion
LF = min(LS sucesoras)
MT = LS - ES = LF - EF

PERT:
Te = (to + 4*tn + tp)/6
sigma = (tp - to)/6
varianza = sigma^2
Z = (T_objetivo - media_proyecto)/sigma_proyecto
```

