# Calculadora de nota final

## 1. Qué es

Programa pequeño en Python que recibe las notas de una materia con sus porcentajes y calcula la nota final ponderada, en escala de 0 a 5. Lo escribí para que los estudiantes de mi curso dejen de equivocarse al calcular a mano cuando cada componente pesa distinto (por ejemplo, parcial 30 %, taller 20 % y examen final 50 %).

Estado: está lista la capa de cálculo (`calculo.py`, HU-01 con las validaciones de HU-02 y HU-03 y el aporte de cada nota, HU-04) y la interfaz de consola (`consola.py`). Diseño (ADR-001): módulo en capas, sin base de datos y sin dependencias de ejecución.

## 2. Requisitos

- Python 3.10 o superior.
- Para ejecutar el programa no se necesita instalar nada más (solo usa la librería estándar).
- Para las pruebas y el linter: `pytest`, `ruff` y `pip-audit`, con versiones fijadas en `requirements-dev.txt`.

## 3. Instalación

```bash
git clone https://github.com/Santiago072005/Calculadora-notas.git
cd Calculadora-notas
python -m venv .venv
# Windows: .venv\Scripts\activate     Linux o macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 4. Ejecución

Con el entorno activado (o con `.venv\Scripts\python.exe` en Windows), abre la consola interactiva:

```bash
python consola.py
```

El programa pregunta cuántas evaluaciones hay y, para cada una, su nombre, su nota (0 a 5) y su porcentaje; acepta coma decimal («4,5»). Muestra una tabla con el aporte de cada nota y la nota final, o el mensaje de error si los datos no son válidos. Ejemplo con dos evaluaciones (`4,5` al 40 % y `3` al 60 %): nota final 3.6.

La función también se puede usar directamente desde Python:

```bash
python -c "from calculo import calcular_nota_final; print(calcular_nota_final([3.0, 0, 5.0], [30, 20, 50]))"
```

Debe imprimir `3.4`. Si los datos no son válidos, lanza `ValueError` con un mensaje que dice cuál dato falló.

## 5. Pruebas

```bash
pytest
```

Debe terminar con `38 passed`. Para el linter y la auditoría de dependencias:

```bash
ruff check --select E,F,B,S .
pip-audit -r requirements-dev.txt
```

## 6. Estructura

| Archivo | Qué contiene |
|---|---|
| `calculo.py` | `calcular_nota_final`, `calcular_aportes`, `validar_notas` y `validar_porcentajes` |
| `consola.py` | Capa de consola: pide los datos y muestra el resultado o el error |
| `test_calculo.py` | 38 pruebas con pytest: normales, de límite, de error y de abuso |
| `pyproject.toml` | Configuración de ruff (reglas E, F, B y S) y de pytest |
| `requirements.txt` | Sin dependencias de ejecución |
| `requirements-dev.txt` | Herramientas de desarrollo con versión fijada |
| `.env.example` | Indica que el proyecto no usa variables de entorno |
| `bitacora_ia.md` | Bitácora de uso de IA (semanas 5 y 6) |
| `revision_seguridad.md` | Informe de revisión de código y seguridad (semana 6) |
| `tests/` | 118 pruebas por particiones, valores límite y tabla de decisión, con datos sintéticos (semana 7) |
| `registro_pruebas.md` | Tabla de casos, pruebas de la IA revisadas, código roto a propósito y datos de prueba (semana 7) |

## 7. Uso de IA

Usé Claude como asistente de código para revisar mis pruebas, implementar la función, hacer una segunda revisión de código y de seguridad y corregir hallazgos. Las pruebas se escribieron antes que el código, cada hallazgo de la IA se verificó ejecutando el código y ninguna prueba se modificó para que pasara. El detalle de cada sugerencia (aceptada, ajustada o rechazada) está en [`bitacora_ia.md`](bitacora_ia.md) y la revisión en [`revision_seguridad.md`](revision_seguridad.md).

## 8. Autor y licencia

Autor: Erick Santiago Marroquin Aldana, estudiante del seminario de IA aplicada al ciclo de vida del software. Licencia: MIT (ver `LICENSE`).

---

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

- `notas`: lista o tupla de notas, una por componente evaluado (parcial, taller, examen final...). Cada nota es un número (`int` o `float`, no `bool`), finito, entre 0 y 5, incluidos ambos extremos.
- `porcentajes`: lista de pesos, en porcentaje (30 significa 30 %), en el mismo orden que `notas`.

**Qué devuelve**

- La nota final, `sum(nota * porcentaje / 100)`, como `float` redondeado a 2 decimales, con las mitades hacia arriba (0.125 da 0.13).

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
| Una nota que no es número válido (`nan`, `inf`, `True`, texto, `None`...) | `La nota {nota!r} no es un número válido` |
| Una nota menor que 0 o mayor que 5 | `La nota {nota} está fuera de 0 a 5` |
| Un porcentaje que no es número válido | `El porcentaje {porcentaje!r} no es un número válido` |
| Un porcentaje menor o igual a 0 | `Cada porcentaje debe ser mayor que 0` |
| Los porcentajes no suman 100 | `Los porcentajes suman {suma} %, deben sumar 100 %` (`{suma}` con formato `.10g`, por ejemplo `90`, `100.5` o `99.999999`) |

**Casos límite**

- Una sola nota con 100 %.
- Todas las notas en 0 (resultado 0.0) y todas en 5 (resultado 5.0).
- Notas exactamente en 0 y en 5 (válidas); 5.5 y -0.1 (error).
- Porcentajes con decimales que suman 100 con error de punto flotante.
- Listas vacías y listas de distinto tamaño.
- Datos que no son números válidos: `nan`, `inf`, `True`, texto, `None` y enteros demasiado grandes (semana 6).
- Mitades al redondear: `0.125`, `3.125` y `2.675` dan `0.13`, `3.13` y `2.68` (semana 6).

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
