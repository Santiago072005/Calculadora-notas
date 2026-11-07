# Calculadora de nota final

Programa pequeño en Python que recibe las notas de una materia con sus porcentajes y calcula la nota final ponderada, en escala de 0 a 5. Proyecto final del seminario de IA aplicada al ciclo de vida del software.

Diseño (ADR-001): módulo en capas, con la lógica de cálculo en `calculo.py`, sin base de datos. La interfaz de consola (`consola.py`) llegará en otra semana.

## Funcionalidad de la semana 5

### Historia de usuario

**HU-01 (necesidad N-01, prioridad Must).** Como estudiante, quiero ingresar mis notas con sus porcentajes para obtener mi nota final.

Criterio de aceptación:

- **Escenario 1: nota final.** Dado Parcial 3.0 con 30 %, Taller 0 con 20 % y Examen final 5.0 con 50 %, cuando calculo, entonces la nota final es 3.4.
- **Escenario 2 (error): datos inválidos.** Dado que los porcentajes son 30 %, 20 % y 40 %, cuando calculo, entonces veo «Los porcentajes suman 90 %, deben sumar 100 %» y no se calcula nada. La misma regla cubre una nota fuera de 0 a 5 (HU-03) y los demás datos inválidos del contrato.

### Contrato de la función

```python
def calcular_nota_final(notas: list[float], porcentajes: list[float]) -> float
```

**Qué recibe**

- `notas`: lista de notas, una por componente evaluado (parcial, taller, examen final...). Cada nota está entre 0 y 5, incluidos ambos extremos.
- `porcentajes`: lista de pesos, en porcentaje (30 significa 30 %), en el mismo orden que `notas`.

**Qué devuelve**

- La nota final, `sum(nota * porcentaje / 100)`, como `float` redondeado a 2 decimales.

**Supuestos**

- Hay al menos un componente y cada nota tiene su porcentaje (mismo tamaño de lista).
- Cada porcentaje es mayor que 0 y los porcentajes suman 100 %.
- La suma de porcentajes se compara con una tolerancia de `1e-9`, porque en Python `sum([3.1, 32.8, 64.1])` da `99.99999999999999`.
- La función no pide datos ni imprime nada; solo calcula y lanza errores (decisión de diseño: la entrada y salida van en `consola.py`).

**Errores.** En todos los casos lanza `ValueError` y no devuelve ninguna nota. Se revisa en este orden:

| Condición | Mensaje |
|---|---|
| Listas vacías | `Debe haber al menos una nota` |
| Distinto número de notas y porcentajes | `Debe haber una nota por cada porcentaje` |
| Una nota menor que 0 o mayor que 5 | `La nota {nota} está fuera de 0 a 5` |
| Un porcentaje menor o igual a 0 | `Cada porcentaje debe ser mayor que 0` |
| Los porcentajes no suman 100 | `Los porcentajes suman {suma} %, deben sumar 100 %` (`{suma}` con formato `:g`, por ejemplo `90`) |

**Casos límite**

- Una sola nota con 100 %.
- Todas las notas en 0 (resultado 0.0) y todas en 5 (resultado 5.0).
- Notas exactamente en 0 y en 5 (válidas); 5.5 y -0.1 (error).
- Porcentajes con decimales que suman 100 con error de punto flotante.
- Listas vacías y listas de distinto tamaño.

**Ejemplos**

| `notas` | `porcentajes` | Resultado |
|---|---|---|
| `[3.0, 0, 5.0]` | `[30, 20, 50]` | `3.4` |
| `[4.0, 3.5, 5.0]` | `[30, 20, 50]` | `4.4` |
| `[4.2]` | `[100]` | `4.2` |
| `[3.0, 4.0, 5.0]` | `[30, 20, 40]` | `ValueError: Los porcentajes suman 90 %, deben sumar 100 %` |
| `[3.0, 5.5]` | `[50, 50]` | `ValueError: La nota 5.5 está fuera de 0 a 5` |

### Cómo ejecutar las pruebas

```bash
pip install pytest
pytest
```
