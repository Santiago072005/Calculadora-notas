# Bitácora de uso de IA

Proyecto: Calculadora de nota final ponderada (Python)
Estudiante: Erik Marroquinal
Funcionalidad: HU-01 Calcular la nota final ponderada
Asistente usado: Claude (modo agente), en sesiones separadas: una para revisar el contrato y las pruebas y otra para implementar; el refactor se hizo en la sesión principal

## Entradas

### Entrada 1

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt: «Revisa mi contrato y mis pruebas. ¿Qué casos importantes faltan o qué prueba está mal escrita o es ambigua? Propón como máximo 5 mejoras, cada una con el nombre de la prueba y por qué. No escribas la implementación.» Sugerencia 1 del asistente: agregar `test_error_si_un_porcentaje_es_negativo` con `[120, -20]`.
- **Decisión:** Aceptada
- **Por qué:** Solo probaba el porcentaje 0; con `[120, -20]` la suma da 100, así que únicamente la regla «mayor que 0» lo detecta. Un `if p == 0` habría pasado todas mis pruebas.
- **Verificación:** Agregué la prueba antes del commit en rojo y comprobé que fallaba con la función sin implementar; con la implementación pasa.
- **Commit relacionado:** 8265d2c (Pruebas en rojo)

### Entrada 2

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia 2 del mismo prompt: probar la suma por encima de 100 (`[50, 50.5]`, mensaje «suman 100.5 %») y, al final de la respuesta, probar que la tolerancia de 1e-9 rechaza `[50, 49.999999]`.
- **Decisión:** Aceptada
- **Por qué:** Solo tenía la suma por debajo (90). Estas pruebas cubren el exceso, el formato de la suma con decimales y el límite de la tolerancia que escribí en el contrato.
- **Verificación:** Dos pruebas nuevas, en rojo antes del código y en verde después.
- **Commit relacionado:** 8265d2c y ab5ab90

### Entrada 3

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia 3: `test_orden_de_validacion`, parametrizada, con casos que rompen dos reglas a la vez (`[]` con `[50]`, `[6.0]` con `[90]`, `[3.0]` con `[0]`).
- **Decisión:** Aceptada
- **Por qué:** El README fija el orden de los errores y ninguna prueba lo comprobaba; sin ella cualquier orden pasaba las demás pruebas.
- **Verificación:** Corrí la prueba en rojo y luego con la implementación; verifiqué a mano que cada caso rompe dos reglas.
- **Commit relacionado:** 8265d2c y ab5ab90

### Entrada 4

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia 4: reemplazar `test_resultado_redondeado_a_dos_decimales` porque sería «frágil», con `[3.5, 4.1]` y `[50, 50]`.
- **Decisión:** Aceptada con cambios
- **Por qué:** No acepté reemplazarla: sin `round` esa prueba falla, porque 3.5599999999999996 no es 3.56, y eso es justo lo que quiero comprobar. Sí acepté la parte útil: agregué una prueba con una nota de tres decimales (`3.333` da `3.33`) para que el redondeo se vea con otro dato.
- **Verificación:** Comprobé en Python que `3.7*0.33 + 4.1*0.33 + 2.9*0.34` da 3.5599999999999996, y que la prueba nueva falla sin el redondeo.
- **Commit relacionado:** 8265d2c

### Entrada 5

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia 5: comprobar que el resultado es `float` y que el mensaje de nota fuera de rango incluya el valor.
- **Decisión:** Aceptada con cambios
- **Por qué:** El contrato promete `float` y `== 0.0` también pasa con un `int`. Lo apliqué solo en las pruebas de 0 y de 5, donde importa, no en todas. El mensaje con el valor sí lo exigí en las dos notas inválidas (5.5 y -0.1), como dice la tabla de errores.
- **Verificación:** Corrí las pruebas en rojo y en verde; el `isinstance` y los textos exactos pasan con la implementación.
- **Commit relacionado:** 8265d2c

### Entrada 6

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt: «Implementa calcular_nota_final en calculo.py siguiendo el contrato del README y haz que pasen todas las pruebas. Solo librería estándar. No modifiques ni borres ninguna prueba ni el README; edita solo calculo.py. Ejecuta pytest y corrige hasta que pasen. Al final, aparte del código, lista como máximo 4 sugerencias opcionales de mejora que NO aplicaste.»
- **Decisión:** Aceptada
- **Por qué:** Cumple el contrato y el ADR-001 (solo librería estándar, lógica sin `input` ni `print`). Leí cada línea: valida en el orden del README, usa `math.isclose` con tolerancia 1e-9 en lugar de comparar con `== 100`, y calcula `sum(nota * porcentaje / 100)` con `round(..., 2)`.
- **Verificación:** 20 pruebas en verde con `pytest`. Comparé el archivo de pruebas y el README con las copias originales y no cambiaron.
- **Commit relacionado:** ab5ab90 (Implementación, pruebas en verde)

### Entrada 7

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia opcional 1 del asistente: con el formato `:g`, una suma de 99.999999 se muestra como «100» y el mensaje «suman 100 %, deben sumar 100 %» confunde.
- **Decisión:** Aceptada con cambios
- **Por qué:** Era un defecto real del mensaje. El asistente decía que corregirlo contradecía el README; lo resolví actualizando el contrato (formato `.10g`) en el mismo commit en vez de dejar el defecto. Primero escribí una prueba que lo reproduce.
- **Verificación:** La prueba nueva `test_mensaje_muestra_la_suma_con_precision_suficiente` falló con el código del asistente (mostraba «100») y pasó después del cambio; las 21 pruebas pasan.
- **Commit relacionado:** ab204c7 (prueba en rojo) y b123cd9 (corrección)

### Entrada 8

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia opcional 2 y 4: rechazar `NaN`, `bool` y tipos no numéricos en notas y porcentajes, y agregar pruebas para eso.
- **Decisión:** Rechazada
- **Por qué:** No está en el contrato de esta funcionalidad: la función recibe números. El texto que no es número lo debe detener `solicitar_datos` de la capa de consola (HU-01), que aún no se construye. Anoto el riesgo: hoy `float('nan')` pasa la validación de rango.
- **Verificación:** Lo comprobé en Python (`nan < 0 or nan > 5` es `False`). Queda como pendiente para `consola.py`.
- **Commit relacionado:** Sin commit (decisión de alcance)

### Entrada 9

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Sugerencia opcional 3: reemplazar `ValueError` por una excepción propia `DatosInvalidosError(ValueError)`.
- **Decisión:** Rechazada
- **Por qué:** Es más código del que necesita un programa pequeño (RNF-03 y atributo de simplicidad del diseño). `ValueError` ya cumple el contrato y la interfaz de consola puede capturarlo; si luego necesito distinguir errores, la agrego.
- **Verificación:** Revisé que el contrato del README y las 21 pruebas solo piden `ValueError`.
- **Commit relacionado:** Sin commit (decisión de diseño)

### Entrada 10

- **Fecha:** 2026-11-07
- **Prompt o sugerencia:** Prompt: «Refactoriza calculo.py: elimina los valores mágicos y separa las validaciones de notas y de porcentajes como en la sección 6 del diseño. No cambies el comportamiento ni las pruebas.»
- **Decisión:** Aceptada
- **Por qué:** Las constantes `NOTA_MINIMA`, `NOTA_MAXIMA`, `TOTAL_PORCENTAJES`, `TOLERANCIA_SUMA` y `DECIMALES` reemplazan a 0, 5, 100, 1e-9 y 2. `validar_notas` y `validar_porcentajes` son las funciones públicas del diseño y dejan `calcular_nota_final` más corta.
- **Verificación:** Corrí las 21 pruebas antes y después: pasan sin modificarlas, y `git diff` confirma que `test_calculo.py` no cambió en este commit.
- **Commit relacionado:** 52ab817 (Refactor)

## Resumen

| Decisión | Cantidad |
|---|---|
| Aceptadas | 5 (entradas 1, 2, 3, 6 y 10) |
| Aceptadas con cambios | 3 (entradas 4, 5 y 7) |
| Rechazadas | 2 (entradas 8 y 9) |

## Errores que atraparon las pruebas

- **Mensaje de error engañoso.** El código del asistente pasó las 20 pruebas a la primera, pero una de sus sugerencias opcionales señaló que con el formato `:g` una suma de 99.999999 se mostraría como «100». Escribí `test_mensaje_muestra_la_suma_con_precision_suficiente`, falló con «Los porcentajes suman 100 %, deben sumar 100 %» y lo corregí cambiando a `.10g` (commits ab204c7 y b123cd9).
- **Hueco en mis propias pruebas.** La revisión del asistente mostró que con solo la prueba del porcentaje 0 una validación `if p == 0` habría pasado todo; agregué el porcentaje negativo antes del commit en rojo.
- **No hubo ninguna prueba modificada para que el código pasara.** Las pruebas solo se ampliaron antes del primer commit y con la prueba nueva del commit ab204c7.

## Reflexión final (5 a 8 líneas)

>

El asistente me ayudó más a pensar en casos de prueba que yo no había visto, como un porcentaje negativo o qué error debe salir primero cuando hay dos a la vez. El código que generó pasó todas las pruebas a la primera, y yo las ejecuté en mi computador para comprobarlo. Aun así, una sugerencia suya me llevó a escribir una prueba nueva, y esa prueba atrapó un error: el mensaje decía «suman 100 %» cuando la suma real era 99.999999. Lo corregí cambiando el formato del número. No acepté validar `NaN` ni crear una excepción propia, porque era más código del que necesita un programa pequeño y lo de `NaN` le toca a la consola. La próxima vez probaría el programa con datos reales desde el principio y revisaría los mensajes de error con el mismo cuidado que los resultados.
