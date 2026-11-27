# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: Calculadora de nota final ponderada
Estudiante: Erick Santiago Marroquin Aldana
Fecha: 2026-11-25

## 1. Tabla de casos

Las pruebas están en `tests/` (`test_validar_notas.py`, `test_validar_porcentajes.py`, `test_calcular_nota_final.py`, `test_datos_sinteticos.py`). Cada fila de `@pytest.mark.parametrize` lleva el ID de esta tabla (por ejemplo `R1-L8`) como `id=` y como comentario. Total: 100 pruebas en `tests/` (138 con las 38 de las semanas 5 y 6, que siguen en `test_calculo.py` sin cambios).

### Regla R1: `validar_notas(notas)`: cada nota es un número (int o float, no bool), finito y está entre 0 y 5, ambos incluidos

**Regla completa (el oráculo):** tomada del contrato del README. Cada nota es `int` o `float` (no `bool`), finita (ni `nan` ni `inf`) y está entre 0 y 5 incluidos. Si no, lanza `ValueError`. Primero se revisa el tipo de todas las notas y después el rango. Si todo es válido devuelve `None`.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | int, float y tupla dentro de 0 a 5 | `[3]`, `[2.5, 4.75]`, `(0, 5.0, 1)` | `None` | test_notas_validas_devuelven_none[R1-P1..P3] |
| Partición inválida | Menor que 0 | `[-1]` | ValueError «La nota -1 está fuera de 0 a 5» | test_notas_invalidas_lanzan_value_error[R1-P4] |
| Partición inválida | Mayor que 5 | `[6]` | ValueError «La nota 6 está fuera de 0 a 5» | …[R1-P5] |
| Partición inválida | Texto, None, True, False | `["a"]`, `[None]`, `[True]`, `[False]` | ValueError «… no es un número válido» | …[R1-P6..P9] |
| Partición inválida | nan, inf, -inf | `[nan]`, `[inf]`, `[-inf]` | ValueError «… no es un número válido» | …[R1-P10..P12] |
| Orden de las reglas | Tipo antes que rango | `[6, "x"]` | ValueError sobre `'x'` (no sobre 6) | …[R1-P13] |
| Orden de las reglas | Dos fuera de rango | `[7, -2]` | ValueError sobre 7 (la primera) | …[R1-P14] |
| Límite | -0.01 / 0 / 0.01 | `[-0.01]` / `[0]` y `[0.0]` / `[0.01]` | error / None / None | …[R1-L1], test_notas_validas…[R1-L2, L3, L4] |
| Límite | 4.99 / 5 / 5.01 | `[4.99]` / `[5]` y `[5.0]` / `[5.01]` | None / None / error | …[R1-L5, L6, L7, L8] |
| Límite | bool junto a su vecino int | `[1, True]` | ValueError sobre `True` | …[R1-L9] |
| Extra mío | nan junto a un valor válido | `[4, nan]` | ValueError sobre `nan` | …[R1-X1] |

**Ambigüedades encontradas:** la lista vacía `[]` no está definida para `validar_notas` (la IA la propuso con «None, confirmar»). La saqué de la tabla; `calcular_nota_final` ya la rechaza antes con «Debe haber al menos una nota».

### Regla R2: `validar_porcentajes(porcentajes)`: cada porcentaje es número válido, mayor que 0 y la suma es 100 (tolerancia 1e-9)

**Regla completa (el oráculo):** cada porcentaje es número válido (igual que las notas), mayor que 0, y la suma difiere de 100 en 1e-9 o menos. Se revisa en orden: tipo, `<= 0`, suma. El mensaje de suma usa el formato `.10g` («90», «100.5»).

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Uno solo, varios enteros, decimales, tupla | `[100]`, `[30,20,50]`, `[33.3,33.3,33.4]`, `(60,40)` | `None` | test_porcentajes_validos_devuelven_none[R2-P1..P4] |
| Partición inválida | Tipo (texto, None, bool, nan, inf) | `["10",90]`, `[None,100]`, `[True,99]`, `[nan,100]`, `[inf]` | ValueError «El porcentaje … no es un número válido» | test_porcentajes_invalidos_lanzan_value_error[R2-P5..P8b] |
| Partición inválida | Cero o negativo (aunque la suma dé 100) | `[0,100]`, `[-10,110]` | ValueError «Cada porcentaje debe ser mayor que 0» | …[R2-P9, P10] |
| Partición inválida | Suma menor / mayor | `[50,40]`, `[60,40.5]` | «suman 90 %» / «suman 100.5 %» | …[R2-P11, P12] |
| Orden de las reglas | Tipo antes que `<= 0`; `<= 0` antes que suma | `[0,"a"]`, `[0,50]` | error de tipo; error de `<= 0` | …[R2-P13, P14] |
| Límite | 0 / 0.001 / -0.001 | `[0,100]` / `[0.001,99.999]` / `[-0.001,100.001]` | error / None / error | …[R2-L1 = P9], test_porcentajes_validos…[R2-L2], …[R2-L3] |
| Límite | Tolerancia 1e-9: desviación 1e-10 (válida), 2e-9 (inválida) | `[50,50.0000000001]`, `[50,50.000000002]`, `[50,49.999999998]` | None / error / error | …[R2-L4], test_suma_fuera_de_tolerancia_mensaje_con_prefijo[R2-L5, L6] |
| Límite | Suma 99.9999999, 99, 100 exacto, 101 | `[50,49.9999999]`, `[50,49]`, `[25,75]`, `[50,51]` | error con la suma / error / None / error | …[R2-L7, L9a], …[R2-L8], …[R2-L9b] |
| Extra mío | nan junto a un valor válido | `[50, nan]` | ValueError sobre `nan` | …[R2-X1] |
| Hallado al romper el código | Suma con ruido de coma flotante | `[33.3,33.3,33.3]` | «suman 99.9 %, deben sumar 100 %» | …[R2-M1] |

**Ambigüedades encontradas:** (1) `[]` en `validar_porcentajes` (la IA supuso «suman 0 %»): no está en la regla, la quité. (2) Con `.10g`, una suma de 100.000000002 se muestra como «suman 100 %, deben sumar 100 %», un mensaje confuso. El contrato manda `.10g` y las filas R2-L5/L6 solo exigen el prefijo «Los porcentajes suman»; lo dejo anotado como mejora posible.

### Regla R3: `calcular_nota_final(notas, porcentajes)`: combina varias condiciones y calcula la nota ponderada con 2 decimales (mitades hacia arriba)

**Regla completa (el oráculo):** devuelve `sum(nota * porcentaje / 100)` como `float` redondeado a 2 decimales con las mitades hacia arriba (0.125 da 0.13). Lanza `ValueError`, en este orden, si: (a) las listas están vacías; (b) tienen distinto tamaño; (c) hay una nota inválida (R1); (d) hay un porcentaje inválido o la suma no es 100 (R2). Acepta listas y tuplas.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Ejemplo del contrato | `[3.0,0,5.0]`, `[30,20,50]` | 3.4 | test_nota_final_valor_esperado[R3-P1] |
| Partición válida | Una nota, tuplas, promedio simple, todo 0, todo 5 | `[4.5]`/`[100]`, `(4,2)`/`(25,75)`, `[4,2]`/`[50,50]`, `[0,0]`, `[5,5]` | 4.5, 2.5, 3.0, 0.0, 5.0 | …[R3-P2, P3, P4, P8, P9] |
| Partición válida | Tipo de retorno | `[3]`, `[100]` | 3.0 y `type(...) is float` | test_nota_final_entera_se_devuelve_como_float |
| Límite de redondeo | 0.124 / 0.125 / 0.126 | `[1.24,0]`, `[1.25,0]`, `[1.26,0]` con `[10,90]` | 0.12 / 0.13 / 0.13 | …[R3-P5, P6, P7] |
| Límite de redondeo | Mitad que en binario queda por debajo | `[2.675]`, `[1.005]` con `[100]` | 2.68 y 1.01 | …[R3-M1, M2] (hallados al romper el código) |
| Límite | Una sola nota, extremos 0 y 5 | `[0]`/`[100]`, `[0,5]`/`[50,50]` | 0.0, 2.5 | …[R3-L1, L6] |
| Límite | Tamaño distinto por 1 (más porcentajes / más notas) | `[3]`/`[50,50]`, `[3,4]`/`[100]` | ValueError «Debe haber una nota por cada porcentaje» | test_nota_final_errores_con_mensaje_exacto[R3-L3, L4] |
| Límite | 5.01; suma 99 | `[5.01,0]`/`[50,50]`, `[3,3]`/`[50,49]` | errores de nota y de suma | …[R3-L5, L7] |
| Extra mío | Cada peso va con su nota | `[5,0]`/`[80,20]` y `[0,5]`/`[80,20]` | 4.0 y 1.0 | …valor_esperado[R3-X1a, X1b] |
| Extra mío | Entero gigante (`10**400`) | `[10**400]`, `[100]` | ValueError «La nota … no es un número válido» | test_nota_final_entero_gigante_no_es_numero_valido |

**Ambigüedades encontradas:** `notas=[]` con `porcentajes=[100]`: la regla (a) dice «listas vacías» (plural) y no aclara qué mensaje sale si solo una está vacía. La saqué de las pruebas; el código revisa `not notas` primero.

#### Tabla de decisión de R3 (condiciones en orden estricto; «-» = no importa)

| Regla | C1 listas vacías | C2 tamaños distintos | C3 nota inválida | C4 porcentaje inválido (tipo o ≤ 0) | C5 suma ≠ 100 | Acción | Pruebas |
|---|---|---|---|---|---|---|---|
| D1 | Sí | - | - | - | - | «Debe haber al menos una nota» | R3-D1 |
| D2 | No | Sí | - | - | - | «Debe haber una nota por cada porcentaje» | R3-D2a (nota 9 inválida también), R3-D2b (porcentaje 0 también) |
| D3 | No | No | Sí | - | - | error de la nota (tipo antes que rango) | R3-D3a (porcentaje 0 también), D3b, D3c, D3d |
| D4 | No | No | No | Sí | - | error del porcentaje (tipo o ≤ 0) | R3-D4a, D4b, D4c (suma 100 pero hay negativo) |
| D5 | No | No | No | No | Sí | «Los porcentajes suman X %, deben sumar 100 %» | R3-D5a (90), D5b (100.5) |
| D6 | No | No | No | No | No | devuelve la nota redondeada | R3-P1 |

Las 6 reglas cubren todas las combinaciones posibles porque cada condición se evalúa solo si las anteriores fueron «No». Las filas D2a, D2b y D3a combinan dos condiciones a la vez para confirmar el orden.

## 2. Pruebas de la IA descartadas o corregidas

**Prompt usado:** se hicieron dos peticiones a la IA: una para proponer casos desde la regla (bitácora, entrada 16) y otra para escribir las pruebas desde mi tabla revisada (entrada 17); una tercera generó los datos sintéticos (entrada 18). La IA devolvió unas 85 filas de propuesta y 5 archivos de pruebas, y yo revisé cada una con las tres preguntas: ¿el esperado sale de la regla?, ¿fallaría si el código estuviera roto?, ¿cubre algo que las otras no?

| Prueba generada | Decisión | Por qué | En su lugar |
|---|---|---|---|
| Propuesta de casos R1-P15 (`[]` en validar_notas → None), R2-P15 (`[]` → «suman 0 %») y R3-L9 (`[]` con `[100]`) | Descartada | El esperado era un supuesto de la IA; la regla no lo define (pregunta 1) | Los anoté como ambigüedades en la sección 1 |
| Propuesta R2-L5/L6: mensaje exacto «suman 100 %, deben sumar 100 %» | Corregida | Fijar ese texto confuso como esperado sería aprobar un defecto de presentación (el esperado saldría del código, no de la regla) | Solo se exige el prefijo «Los porcentajes suman» |
| `R3-D6`: `[3.0,0,5.0]`, `[30,20,50]` → 3.4 | Descartada | Es la misma entrada y esperado de R3-P1; no cubre nada nuevo (pregunta 3) | Se queda R3-P1 |
| Pruebas con `==` en R3 (en vez de `pytest.approx`) | Conservada | Los esperados ya tienen 2 decimales; con `approx` y su tolerancia 0.12 y 0.13 casi no se distinguen, y esas pruebas existen justo para el redondeo (pregunta 2) | Se mantiene `==`; `approx` solo en los datos sintéticos |
| `test_cursos_sinteticos` y `test_textos_invalidos_como_nota`: un bucle `for` dentro de una sola prueba | Corregida | El primer fallo escondía el resto y no dejaba ver qué curso o texto falló | Fixtures con `params` (`curso`, `texto_invalido`): una prueba por caso con nombre |
| Fixture `textos_invalidos` (lista) | Descartada | Quedó sin uso al pasar a `texto_invalido` | Se borró |
| Todas las pruebas de comparación de mensajes con `re.escape` | Conservada, con límite | `match` busca el texto dentro del mensaje, no lo exige completo; sirve para detectar cambios de número o palabra, pero no un texto añadido al final | Lo anoto como límite; ningún mutante de mensaje sobrevivió salvo el de `.10g` (sección 3) |

**Decisión:** Conservada la mayor parte de las filas de R1 a R3, Corregida la de los datos sintéticos y el mensaje R2-L5/L6, Descartada R3-D6, la fixture sin uso y los tres casos ambiguos.

## 3. Romper el código a propósito

Una modificación a la vez en `calculo.py`, `python3 -m pytest tests -q`, y luego `git restore calculo.py`. Al terminar, `git status` limpio y las 138 pruebas en verde.

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| `nota > NOTA_MAXIMA` por `nota >= NOTA_MAXIMA` | calculo.py:51 | Sí, 12 pruebas, entre ellas R3-P1 | Nada: la suite protege el 5 como válido |
| `porcentaje <= 0` por `porcentaje < 0` | calculo.py:75 | Sí, 3 pruebas (R3-D4a, R2-P9, R2-L1) | Nada: protege el borde del 0 |
| `return` del cálculo cambiado por la constante `return 3.0` | calculo.py:115 | Sí, 21 pruebas | Nada |
| `ROUND_HALF_UP` por `ROUND_HALF_EVEN` | calculo.py:115 | Sí, R3-P6 (0.125 daría 0.12) | Nada |
| `nota < NOTA_MINIMA` por `nota <= NOTA_MINIMA` | calculo.py:51 | Sí, 14 pruebas | Nada |
| `TOLERANCIA_SUMA` de 1e-9 a 1e-6 | calculo.py:9 | Sí, R2-L7 y otras 2 | Nada |
| `TOLERANCIA_SUMA` de 1e-9 a 1e-11 | calculo.py:9 | Sí, R2-L4 | Nada |
| Quitar `rel_tol=0` en `math.isclose` | calculo.py:78 | Sí, R2-L5, R2-L7 y 1 más | Nada |
| Validar porcentajes antes que notas | calculo.py:109 | Sí, R3-D3a | Nada |
| Aceptar `bool` (quitar `isinstance(valor, bool) or`) | calculo.py:24 | Sí, 5 pruebas (R3-D3d, R1-P8…) | Nada |
| `zip(notas, reversed(porcentajes))` (pesos desalineados) | calculo.py:113 | Sí, 12 pruebas (R3-P1, R3-X1a…) | Nada |
| `len(notas) != len(porcentajes)` por `<` | calculo.py:107 | Sí, R3-L4 y R3-D2b | Nada |
| `DECIMALES = 3` | calculo.py:10 | Sí, 5 pruebas (R3-P5, P6…) | Nada |
| `Decimal(str(nota)) * Decimal(str(porcentaje)) / 100` por `Decimal(nota * porcentaje / 100)` (usar float) | calculo.py:112 | **No: sobrevivió, 97 en verde** | Agregué R3-M1 (`[2.675]` → 2.68) y R3-M2 (`[1.005]` → 1.01); repetí el cambio y ahora falla 2 pruebas |
| `{suma:.10g}` por `{suma}` en el mensaje de la suma | calculo.py:80 | **No: sobrevivió, 97 en verde** | Agregué R2-M1 (`[33.3,33.3,33.3]` → «suman 99.9 %»); repetí el cambio y ahora falla 1 prueba |

Mi primer intento de cambiar el redondeo a `ROUND_HALF_EVEN` no era una prueba válida: no importé el nombre, falló todo por `NameError` y eso no demuestra nada. Lo repetí con la importación y ahí falló solo R3-P6.

Los dos mutantes que sobrevivieron eran huecos reales de mi tabla: la IA y yo elegimos números que daban lo mismo con `float` y con `Decimal`, y sumas sin ruido de coma flotante. Las filas R3-M1, R3-M2 y R2-M1 se agregaron en el commit db2cc52. No modifiqué ninguna prueba para que pasara y no encontré ningún defecto en el código.

## 4. Datos de prueba

**Origen:** sintéticos generados con IA (entrada 18 de la bitácora) y revisados a mano; los esperados los comprobé con la cuenta a mano de cada fila. Confirmo que no hay datos de personas reales.

**Casos difíciles incluidos:**
- Nombres ficticios con tilde y ñ («María José Pérez», «Nicolás Muñoz», «Jhon Édinson Ñáñez», «Ángel Ñungo»), con apóstrofo («Sofía D'Ávila»), texto vacío (`""`) y un solo carácter (`"X"`).
- Teléfonos falsos con formato «300 000 0000» y «3000000001»; no son números reales ni se usan en el cálculo.
- Notas en cero, nota 5, un solo componente al 100 %, cuatro componentes y un caso de mitad que sube (4.5×5 % + 5.0×95 % = 4.975 → 4.98).
- Textos que alguien podría teclear como nota: «4,5» (coma decimal), vacío, espacio, «cinco», «4.5» (texto), «5 » (con espacio), «None».

**Fixture:** `tests/conftest.py` (`cursos_sinteticos`, `curso` y `texto_invalido`) y `tests/test_datos_sinteticos.py` (17 pruebas: 10 cursos y 7 textos).
