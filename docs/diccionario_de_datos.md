# Diccionario de datos

Este documento describe **todas las variables** de los archivos de datos del proyecto:

1. los archivos originales, tal como se descargaron del INDEC y del BCRA;
2. los archivos intermedios y la tabla de correspondencia propia;
3. la tabla de modelado, que es la que reciben los modelos.

De cada variable se indica qué significa, su tipo y su unidad, y si se usa o no en el proyecto (y por qué).

**Qué representa una fila de la tabla de modelado:** una división de la industria manufacturera en un mes *t*.

**Convención de tiempo:** el dato del IPI del mes *t* se publica en *t+2*. Ese es el **momento de la predicción**. El mes que se predice es *t+5*, 3 meses después de la decisión, y su resultado se conoce en *t+7*.

---

## 1. Datos originales (`data/raw/`)

Archivos públicos guardados sin modificar. Los enlaces de descarga, las fechas y el calendario de publicación están en [`01_datos_y_exploracion.md`](01_datos_y_exploracion.md).

### 1.1 `sh_ipi_manufacturero_2026.xls` — Índice de producción industrial manufacturero (INDEC)

- **Qué mide:** el volumen físico de producción de la industria manufacturera. Es un **índice**: 100 es el nivel promedio de 2004, así que un valor de 120 indica un 20% más de producción que en 2004. No está en pesos ni en unidades físicas.
- **Hojas:** Índice, Cuadros 1 a 8. **Se usa solo el Cuadro 2**: serie original (sin desestacionalizar), mensual, de enero 2016 a agosto 2026.
- **Estructura del Cuadro 2:** una fila por mes. La primera columna tiene el año (solo en enero) y el mes; los asteriscos marcan datos provisorios. Las 85 columnas de datos son decimales (índice base 2004 = 100):
  - **IPI Manufacturero (nivel general, código D):** no se usa como variable. El proyecto trabaja por división.
  - **16 divisiones (CLaNAE 2004):** **se usan**. Son la base de la variable objetivo y de las predictoras propias de cada división.
  - **68 subclases:** no se usan. El proyecto predice a nivel de división, y las subclases son el detalle que compone cada una.

| División (se usa) | Subclases incluidas en el cuadro (no se usan) |
|---|---|
| 15 Alimentos y bebidas | Carne vacuna (15111); Carne aviar (15112); Fiambres y embutidos (15113); Preparación de frutas, hortalizas y legumbres (15130); Molienda de oleaginosas (15140); Productos lácteos (15200); Molienda de cereales (15311/12/13/20); Galletitas, productos de panadería y pastas (15411/12/41/42); Azúcar, productos de confitería y chocolate (15420/30); Yerba mate, té y café (15491/2/3); Gaseosas, aguas, sodas, cervezas, jugos para diluir, sidras y bebidas espirituosas (15510/29/30/41/42/49); Vino (15521); Otros productos alimenticios (15120/330/499) |
| 16 Productos de tabaco | Preparación de hojas de tabaco (16001); Cigarrillos (16009) |
| 17 Productos textiles | Preparación de fibras de uso textil (17111/2); Hilados de algodón (17113); Tejidos y acabado de productos textiles (17114/15/20); Otros productos textiles (17210/20/30/90) |
| 18-19 Prendas de vestir, cuero y calzado | Prendas de vestir (18110/120/401/402/900); Curtido y artículos de cuero, excepto prendas (19110/20); Calzado y sus partes (19201/2/3/4) |
| 20-22 Madera, papel, edición e impresión | Madera y productos de madera y corcho, excepto muebles (20100/210/220/230/290); Papel y productos de papel (21010/20/91/99); Edición e impresión (22110/120/190/210/220) |
| 23 Refinación del petróleo, coque y combustible nuclear | Naftas (23200); Gasoil (23200); Fueloil (23200); Asfaltos (23200); Otros productos de la refinación del petróleo, coque y combustible nuclear (23100/200/300) |
| 24 Sustancias y productos químicos | Gases industriales (24111); Productos químicos básicos (2411, excepto 24111); Agroquímicos (24120/210); Materias primas plásticas y caucho sintético (24130); Pinturas (24220); Productos farmacéuticos (24231/2/3/9); Detergentes, jabones y productos personales (24241/9); Otros productos químicos (24290/300) |
| 25 Productos de caucho y plástico | Neumáticos (25110); Otros productos de caucho (25190); Manufacturas de plástico (25201/9) |
| 26 Productos minerales no metálicos | Vidrio y productos de vidrio (26101/2/9); Productos de arcilla y cerámica no refractaria (26910/30); Cemento (26941); Cal y yeso (26942); Artículos de cemento y de yeso (26951/9); Otros productos minerales no metálicos (26920/60/90) |
| 27 Industrias metálicas básicas | Industria siderúrgica (27100); Aluminio y otros metales no ferrosos (27201/9); Fundición de metales (27310/20) |
| 28 Productos de metal | Productos metálicos para uso estructural (28110); Envases metálicos (28991); Otros productos de metal y servicios de trabajo de metales (28120/130/910/920/930/999) |
| 29 Maquinaria y equipo | Maquinaria de uso general (29110/20/30/40/50/90); Maquinaria agropecuaria (29211/2/3); Otra maquinaria de uso especial (292, excepto 2921); Aparatos de uso doméstico (29300) |
| 30-33 Otros equipos, aparatos e instrumentos | Equipos y aparatos de informática, televisión y comunicaciones, y componentes electrónicos (30000/32100/200/300); Equipos y aparatos eléctricos (31100/200/300/400/500/900); Instrumentos médicos, ópticos y de precisión (33110/120/200/300/400) |
| 34 Vehículos automotores, carrocerías, remolques y autopartes | Vehículos automotores (34100); Carrocerías, remolques y semirremolques (34200); Autopartes (34300) |
| 35 Otro equipo de transporte | Motocicletas (35910); Otro equipo de transporte (35110/120/200/300/990) |
| 36-38 Muebles y colchones, y otras industrias manufactureras | Muebles y colchones (36101/2/3); Otras industrias manufactureras (36900); Reciclamiento y reparación, instalación y mantenimiento (37000/38000) |

### 1.2 `sh_capacidad_09_26.xls` — Utilización de la capacidad instalada en la industria (INDEC)

- **Qué mide:** qué porcentaje de la capacidad máxima de producción de las plantas se está usando. Por ejemplo, 60% significa que se produce el 60% de lo que se podría producir con las instalaciones existentes.
- **Hoja:** *UCI - NG y bloques* (la única). Una fila por mes, de enero 2016 a julio 2026, con el año en una fila aparte y asteriscos en los datos provisorios.

| Variable | Tipo | Unidad | ¿Se usa? |
|---|---|---|---|
| Período (año y mes) | texto | — | Sí, para armar la fecha |
| Nivel general | decimal | % | Sí: `uci_general`, `uci_general_dif_ia` |
| Productos alimenticios y bebidas | decimal | % | Sí (división 15) |
| Productos del tabaco | decimal | % | Sí (16) |
| Productos textiles | decimal | % | Sí (17 y, por aproximación, 18-19) |
| Papel y cartón | decimal | % | Sí, promediado con Edición e impresión (20-22) |
| Edición e impresión | decimal | % | Sí, promediado con Papel y cartón (20-22) |
| Refinación del petróleo | decimal | % | Sí (23) |
| Sustancias y productos químicos | decimal | % | Sí (24) |
| Productos de caucho y plástico | decimal | % | Sí (25) |
| Productos minerales no metálicos | decimal | % | Sí (26) |
| Industrias metálicas básicas | decimal | % | Sí (27) |
| Industria automotriz | decimal | % | Sí (34) |
| Metalmecánica excluida industria automotriz | decimal | % | Sí (28, 29, 30-33 y 35) |

Todas las columnas se usan. La correspondencia entre bloques y divisiones está en la sección 2.2.

### 1.3 `balanmensual.xls` — Balanza comercial argentina (INDEC)

- **Hoja:** *FOB-CIF* (la única). Una fila por mes, desde enero 1990. Las exportaciones se valúan FOB (valor de la mercadería en el puerto de salida) y las importaciones CIF (incluye seguro y flete hasta el país).

| Variable | Tipo | Unidad | ¿Se usa? |
|---|---|---|---|
| Período (año y mes) | texto | — | Sí, para armar la fecha |
| Exportaciones – total mensual | decimal | millones de USD | **Sí**: `expo_var_ia` |
| Exportaciones – total acumulado del año | decimal | millones de USD | No: repite la información mensual sumada |
| Exportaciones – variación % mensual | decimal | % | No: se calcula la variación interanual propia |
| Exportaciones – variación % acumulada | decimal | % | No: mismo motivo |
| Importaciones – total mensual | decimal | millones de USD | **Sí**: `impo_var_ia` |
| Importaciones – total acumulado del año | decimal | millones de USD | No |
| Importaciones – variación % mensual | decimal | % | No |
| Importaciones – variación % acumulada | decimal | % | No |
| Saldo (exportaciones − importaciones) | decimal | millones de USD | No: es la diferencia de dos variables que ya se usan |

### 1.4 `com3500.xls` — Tipo de cambio de referencia, Comunicación "A" 3500 (BCRA)

- **Qué mide:** el tipo de cambio mayorista oficial (**pesos por dólar**) que publica el Banco Central cada día hábil.

| Hoja | Variable | Tipo | Unidad | ¿Se usa? |
|---|---|---|---|---|
| *TCR diario y TCNPM* | Fecha | fecha | día | Sí |
| *TCR diario y TCNPM* | Tipo de cambio de referencia | decimal | pesos por dólar | **Sí**: se promedia por mes y se calculan `tc_var_ia` y `tc_var_3m` |
| *TCR diario y TCNPM* | Tipo de cambio nominal promedio mensual | decimal | pesos por dólar | No: se recalcula desde la serie diaria (coincide con este valor) |
| *Serie de TCNPM* | Mes / tipo de cambio nominal promedio mensual | fecha / decimal | pesos por dólar | No: algunas fechas están cargadas como texto; se usa la serie diaria |

### 1.5 `series.xlsm` — Series monetarias y financieras (BCRA)

- **Hojas:** dt, BASE MONETARIA, RESERVAS, DEPOSITOS, PRESTAMOS, TASAS DE MERCADO, INSTRUMENTOS DEL BCRA, NOTAS, API_Series. **Se usa solo *TASAS DE MERCADO***: una fila por día hábil, con 25 series de tasas y montos.
- Las otras hojas (base monetaria, reservas, depósitos, préstamos, instrumentos del BCRA) **no se usan**. El proyecto toma una sola tasa como indicador del costo del dinero, y agregar más variables monetarias con un valor por mes sumaría variables muy correlacionadas apoyadas en los mismos pocos ciclos.

**Variables de la hoja *TASAS DE MERCADO*.** Todas son decimales. Las tasas se expresan como TNA (tasa nominal anual) o TEA (tasa efectiva anual), en %.

| Variable | Unidad | ¿Se usa? |
|---|---|---|
| Fecha | día | Sí |
| Plazos fijos en pesos: total, personas humanas, prestadoras de servicios financieros, otras personas jurídicas | % TNA | No |
| Plazos fijos en dólares: total, personas humanas, personas jurídicas | % TNA | No |
| TAMAR en pesos: total (TNA), bancos privados (TNA y TEA) | % | No: se publica desde octubre 2024, no cubre el período |
| BADLAR en pesos: total (TNA) | % TNA | No: se usa la de bancos privados |
| **BADLAR en pesos: bancos privados (TNA)** | % TNA | **Sí**: `badlar`, `badlar_dif_ia` |
| BADLAR en pesos: bancos privados (TEA) | % TEA | No: misma tasa expresada de otra forma |
| TM20 en pesos: total (TNA), bancos privados (TNA y TEA) | % | No: otra tasa mayorista de depósitos, similar a la BADLAR (que se usa) |
| Préstamos personales en pesos | % TNA | No |
| Adelantos en cuenta corriente en pesos | % TNA | No |
| Call en pesos hasta 15 días, entre bancos privados (BAIBAR): tasa y monto operado | % TNA / millones de $ | No |
| Call en pesos hasta 15 días, total: tasa y monto operado | % TNA / millones de $ | No |
| Pases entre terceros a 1 día: tasa y monto operado | % TNA / millones de $ | No |
| Depósitos a la vista remunerados, prestadoras de servicios financieros | % TNA | No |

La **BADLAR** es la tasa que pagan los bancos por depósitos a plazo fijo de más de un millón de pesos, a 30-35 días. Se usa como referencia del costo del financiamiento.

---

## 2. Archivos derivados y externos

### 2.1 `data/processed/ipi_divisiones_mensual.csv` — IPI en formato largo

Paso intermedio generado por [`dataset.py`](../contraccion_industrial/dataset.py) a partir del Cuadro 2 del IPI. Tiene una fila por división y mes (2.048 filas).

| Columna | Tipo | Descripción |
|---|---|---|
| `fecha` | fecha | Mes de referencia |
| `codigo_division` | texto | Código de la división (CLaNAE 2004) |
| `division` | texto | Nombre de la división |
| `ipi` | decimal | Índice de producción industrial, base 2004 = 100 |

### 2.2 `data/external/correspondencia_division_bloque.csv` — divisiones y bloques de capacidad

Tabla armada para este proyecto. El INDEC publica la capacidad instalada en 12 bloques, que no coinciden uno a uno con las 16 divisiones del IPI.

| Columna | Tipo | Descripción |
|---|---|---|
| `codigo_division` | texto | Código de la división del IPI |
| `division` | texto | Nombre de la división |
| `bloque_capacidad` | texto | Bloque de capacidad instalada asignado |
| `criterio` | texto | Cómo se hizo la asignación: directa, aproximada (sin bloque propio), promedio de dos bloques o bloque que agrupa varias divisiones |

**Nota sobre 20-22 (Madera, papel, edición e impresión).** Se usa el promedio simple de los bloques *Papel y cartón* y *Edición e impresión*. Es una **aproximación propia**, no una medición oficial: no está ponderada y no incluye la madera, que no tiene bloque propio. Que esta variable muestre una asociación predictiva no demuestra que los sectores sean equivalentes.

---

## 3. Tabla de modelado: `data/processed/tabla_modelo.csv`

- **Unidad de análisis:** división industrial × mes.
- **Filas:** 2.048 (16 divisiones × 128 meses, enero 2016 a agosto 2026).
- **Columnas:** 24.
- **Generada por:** [`features.py`](../contraccion_industrial/features.py).

La columna **Rol** indica para qué se usa cada variable:

| Rol | Significado |
|---|---|
| ID | Identifica la fila |
| Control | Separación temporal de los datos; no se usa para predecir |
| Predictora | Entra en los modelos |
| Objetivo | Lo que se predice |
| Auxiliar | Sirve para calcular otras columnas o para describir; no entra en los modelos |

Los rangos y los faltantes están calculados sobre la tabla completa.

### Identificación

| Columna | Rol | Tipo | Unidad | Descripción | Fuente | Rango / valores | Faltantes |
|---|---|---|---|---|---|---|---|
| `fecha` | ID | fecha | mes | Mes de referencia del dato del IPI (*t*). Siempre el día 1. | — | 01/2016 a 08/2026 | 0 |
| `codigo_division` | ID | texto | — | Código de la división según la CLaNAE 2004 (ver sección 1.1). | INDEC | 16 valores | 0 |
| `division` | ID | texto | — | Nombre de la división. | INDEC | 16 valores | 0 |
| `bloque_capacidad` | Auxiliar | texto | — | Bloque de capacidad instalada asignado a la división (ver sección 2.2). | Asignación propia | 12 valores | 0 |

### Variables del IPI (por división)

Fuente: INDEC, IPI manufacturero, hoja *Cuadro 2* (`sh_ipi_manufacturero_2026.xls`). Todas se conocen en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango observado | Faltantes |
|---|---|---|---|---|---|---|
| `ipi` | Auxiliar | decimal | índice, base 2004 = 100 | Índice de producción industrial de la división en *t*. Mide volumen físico. | 14,5 a 216,9 | 0 |
| `ipi_var_ia` | Predictora | decimal | proporción (0,05 = +5%) | Variación interanual: IPI(*t*) / IPI(*t-12*) − 1. | −0,89 a 7,55 | 192 |
| `ipi_var_ia_lag1` | Predictora | decimal | proporción | Variación interanual de *t-1*. | −0,89 a 7,55 | 208 |
| `ipi_var_ia_lag2` | Predictora | decimal | proporción | Variación interanual de *t-2*. | −0,89 a 7,55 | 224 |
| `ipi_var_ia_cambio3m` | Predictora | decimal | diferencia de proporciones | Aceleración: `ipi_var_ia`(*t*) − `ipi_var_ia`(*t-3*). | −7,09 a 7,39 | 240 |
| `contraccion_hoy` | Predictora (y modelo de referencia) | binaria | 0 / 1 | 1 si IPI(*t*) < IPI(*t-12*), es decir, si la división está en contracción interanual en el último dato publicado. | 0 / 1 | 192 |

Los valores extremos (+755%, −89%) son reales: corresponden al cierre de abril-mayo de 2020 y al rebote de abril de 2021 contra esa base casi nula. No se corrigen.

### Variable objetivo y control temporal

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango / valores | Faltantes |
|---|---|---|---|---|---|---|
| **`objetivo`** | **Objetivo** | binaria | 0 / 1 | **1 si IPI(*t+5*) < IPI(*t-7*)**: contracción interanual del mes *t+5*, 3 meses después de la decisión. | 0 / 1 | 192 (ver `estado_etiqueta`) |
| `mes_decision` | Control | fecha | mes | *t+2*: se publica el IPI de *t* y se hace la predicción. | 03/2016 a 10/2026 | 0 |
| `mes_etiqueta_conocida` | Control | fecha | mes | *t+7*: se publica el IPI de *t+5* y se conoce el resultado. Una fila entra en el entrenamiento solo si este mes es anterior al corte. | 08/2016 a 03/2027 | 0 |
| `estado_etiqueta` | Control | texto | — | `observada`: el objetivo ya se conoce (1.856 filas). `pendiente`: el IPI de *t+5* todavía no se publicó (80 filas, abril a agosto 2026). `sin_base`: no hay dato de *t-7* (112 filas, enero a julio 2016). | 3 valores | 0 |

### Capacidad instalada

Fuente: INDEC, utilización de la capacidad instalada en la industria (`sh_capacidad_09_26.xls`, hoja *UCI - NG y bloques*). Se usa con un mes de rezago (dato de *t-1*), por prudencia: así queda disponible con seguridad en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango observado | Faltantes |
|---|---|---|---|---|---|---|
| `uci_bloque` | Predictora | decimal | % | Utilización de la capacidad del bloque asignado, en *t-1*. Para 20-22 es el promedio simple de dos bloques: una aproximación propia (ver sección 2.2). | 0,0 a 97,1 | 16 |
| `uci_bloque_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual: `uci_bloque`(*t-1*) − `uci_bloque`(*t-13*). | −58,6 a 65,7 | 208 |
| `uci_general` | Predictora | decimal | % | Utilización de la capacidad, nivel general de la industria, en *t-1*. Es igual para las 16 divisiones de un mes. | 42,0 a 69,6 | 16 |
| `uci_general_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual del nivel general. | −19,6 a 21,2 | 208 |

### Variables macroeconómicas

Tienen un solo valor por mes, igual para las 16 divisiones. Todas están publicadas en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Fuente | Rango observado | Faltantes |
|---|---|---|---|---|---|---|---|
| `tc_var_ia` | Predictora | decimal | proporción | Variación interanual del tipo de cambio mayorista de referencia (Com. A 3500), promedio mensual calculado desde la serie diaria. Es **nominal**. | BCRA, `com3500.xls` | 0,04 a 3,49 | 0 |
| `tc_var_3m` | Predictora | decimal | proporción | Variación del tipo de cambio promedio contra 3 meses antes. Nominal. | BCRA, `com3500.xls` | −0,06 a 1,36 | 0 |
| `badlar` | Predictora | decimal | % TNA | Tasa BADLAR de bancos privados, promedio mensual de la serie diaria. Nominal. | BCRA, `series.xlsm` (hoja *TASAS DE MERCADO*) | 19,2 a 129,4 | 0 |
| `badlar_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual de la BADLAR. | BCRA, `series.xlsm` | −93,2 a 60,2 | 0 |
| `expo_var_ia` | Predictora | decimal | proporción | Variación interanual de las exportaciones FOB (millones de USD). | INDEC, `balanmensual.xls` | −0,36 a 0,86 | 0 |
| `impo_var_ia` | Predictora | decimal | proporción | Variación interanual de las importaciones CIF (millones de USD). | INDEC, `balanmensual.xls` | −0,37 a 0,79 | 0 |

### Faltantes y filas modelables

- Los faltantes de las variables interanuales y de los rezagos están al **comienzo** de la serie: hacen falta 12 a 15 meses previos.
- Los faltantes del objetivo están al comienzo (`sin_base`) y al **final** (`pendiente`).
- **Filas modelables:** 1.728. Son las filas con objetivo observado y sin faltantes en las predictoras, de abril 2017 a marzo 2026. Enero a marzo de 2017 se excluyen por falta de historia, sin imputar (función `excluir_sin_historia` de [`particiones.py`](../contraccion_industrial/modeling/particiones.py)).
### Columnas que no son predictoras

`fecha`, `codigo_division` y `division` identifican la fila. `objetivo` es lo que se predice. `mes_decision`, `mes_etiqueta_conocida` y `estado_etiqueta` sirven para separar los datos en el tiempo. `ipi` es un nivel con escala propia de cada división; su información entra en las variaciones interanuales. `bloque_capacidad` es una etiqueta de texto cuya información ya está en las columnas de capacidad. Ninguna predictora usa información posterior al momento de la predicción (*t+2*).
