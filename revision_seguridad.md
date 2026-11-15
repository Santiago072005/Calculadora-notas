# Informe de revisión de código y seguridad

Proyecto: Calculadora de nota final ponderada (Python)
Estudiante: Erik Marroquinal
Fecha: 2026-11-14
Commit revisado: 05ad71f (cierre de la semana 5, antes de las correcciones)

## 1. Herramientas y criterios

- **Linter:** ruff 0.16.9 con las reglas E, F, B y S. Configuración en `pyproject.toml`. Antes de corregir dio 12 avisos; ahora da 0 (`ruff check --select E,F,B,S .`).
- **Auditoría de dependencias:** pip-audit 2.10.1 sobre `requirements-dev.txt`. Resultado: «No known vulnerabilities found».
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** Claude, con un prompt de revisión de tres criterios, tabla de hallazgos con línea y severidad y separación entre problemas seguros y sospechas (sección 3; entrada 11 de la bitácora).

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No: no hay base de datos, SQL, shell, `eval`, `exec` ni lectura de texto; solo aritmética | Sin hallazgos; las reglas S de ruff no dan avisos |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Búsqueda en todo el historial de Git sin coincidencias; `.env` está en `.gitignore`; se creó `.env.example` (H-10) |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No: el programa no guarda contraseñas ni usuarios | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | No: es una función pura, sin usuarios ni roles. El abuso que sí aplica son los datos inválidos | Pruebas de abuso agregadas para H-01 a H-03 |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí | Ninguna de ejecución (solo librería estándar). Las de desarrollo quedaron fijadas (H-10) y pip-audit no encontró vulnerabilidades |

## 2. Tabla de hallazgos

Las líneas son las del commit revisado, 05ad71f.

| Id | Archivo y línea | Problema | Categoría | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | calculo.py:15 | `nan` pasa la validación de rango y `calcular_nota_final([nan], [100])` devuelve `nan` | Validación de entrada (OWASP A04) | Media | `_es_numero_valido` exige número finito, antes del rango | 7349b46 (prueba en rojo: 4da2da7) |
| H-02 | calculo.py:15 y 23 | `True` se acepta como nota (da 1.0); un texto lanza `TypeError` y no el `ValueError` del contrato | Validación de entrada (OWASP A04) | Media | Se rechazan `bool` y tipos no numéricos con `ValueError` | 7349b46 |
| H-03 | calculo.py:12 (versión del agente) | `math.isfinite(10**400)` lanza `OverflowError` en lugar de `ValueError` | Validación de entrada | Baja | `try/except OverflowError` que devuelve «no es número válido» | 6b357cc (prueba en rojo: 336e791) |
| H-04 | calculo.py:41 | `round()` da 0.12 para 0.125 y 2.67 para 2.675, no el redondeo esperado de una nota | Error de lógica | Media | `Decimal` con `ROUND_HALF_UP` | 4fa49a0 (prueba en rojo: fdde059) |
| H-05 | calculo.py:40 | `zip()` sin `strict=` (B905) | Error probable | Baja | `zip(..., strict=True)` | 55ad303 |
| H-06 | calculo.py:40 | El literal 100 se repite en lugar de `TOTAL_PORCENTAJES` | Valor mágico | Baja | Se usa la constante | 4fa49a0 |
| H-07 | test_calculo.py:52 | Línea de 89 caracteres (E501) | Estilo | Baja | Se parte en dos líneas; misma comprobación | 3b2e1c2 |
| H-08 | .gitignore | `.ruff_cache/` no estaba excluida | Higiene del repositorio | Baja | Se agrega al `.gitignore` | f5063c0 |
| H-09 | raíz | No había `pyproject.toml` ni linter configurado | Configuración | Baja | Configuración de ruff (E, F, B, S) | 4866407 |
| H-10 | raíz | `pytest` sin versión fijada y sin `.env.example` | Componentes y configuración (OWASP A05 y A06) | Media | `requirements-dev.txt` con versiones exactas y `.env.example` | 064283f |
| H-11 | bitacora_ia.md:116 | Línea con solo `>` sobrante, visible en GitHub | Documentación | Baja | Se borra la línea | 1dd8ad6 |
| H-12 | calculo.py:13, 22 y 33 | Docstrings de una línea, sin qué recibe, qué devuelve ni qué errores lanza | Legibilidad | Baja | Docstrings completos, comparados con el código | 673d6ac |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad). No hubo hallazgos de severidad alta.

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 (10 avisos) | test_calculo.py:14, 19, 24, 29, 35, 40, 41, 46, 47 y 52 | `assert` es la forma normal de comprobar en pytest. Se ignora solo en `test_*.py` con `per-file-ignores` en `pyproject.toml` |

## 3. Revisión con IA

**Prompt usado:** «Revisa este código con tres criterios: (1) corrección y pruebas, (2) diseño y legibilidad, (3) seguridad (inyección, secretos, contraseñas, control de acceso y dependencias; si un punto no aplica, di por qué). Entrega una tabla de hallazgos con archivo:línea, problema, severidad y corrección sugerida. Separa en dos secciones los problemas SEGUROS y las SOSPECHAS. No inventes líneas ni funciones que no existan.» Detalle en la entrada 11 de la bitácora.

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| `nan` se acepta como nota (la IA lo puso en severidad alta) | Real (H-01); la dejé en media | Ejecuté `calcular_nota_final([nan], [100])` y devolvió `nan`. Baja a media porque no expone datos ni da acceso |
| Redondeo de `round()` (0.125, 2.675, 1.005) | Real (H-04) | Ejecuté 0.125 → 0.12, 3.125 → 3.12 y 2.675 → 2.67 |
| `True` aceptado y texto lanza `TypeError` | Real (H-02) | Ejecuté `[True]` → 1.0 y `['3']` → `TypeError` |
| No hay pruebas de `nan`, `inf`, `bool` ni tipos | Real | Revisé `test_calculo.py`: no existían; se agregaron 13 pruebas de abuso |
| Literal 100 en lugar de la constante | Real (H-06) | Línea 40 de calculo.py |
| `pytest` sin versión fijada | Real (H-10) | No había `requirements*.txt` |
| `.ruff_cache` no está en `.gitignore` | Real (H-08) | Leí `.gitignore` |
| Un iterador como `iter([3])` lanza `TypeError` | Real, menor; se documenta (ver pendientes) | Ejecuté `calcular_nota_final(iter([3.0]), [100])` |
| `[3.0], [100.0000000001]` devuelve 3.0, tolerancia «demasiado estricta» | Falso positivo | Es el comportamiento del contrato: tolerancia de 1e-9 por el error de punto flotante |
| El README dice «menor o igual a 0» y el mensaje «mayor que 0» | Falso positivo | Es coherente: la IA misma dice que no requiere acción |
| La validación de tipos podría delegarse a `consola.py` | Falso positivo | Ya se valida en `calculo.py`; la consola se construye después |
| `bitacora_ia.md` podría tener datos personales | Falso positivo | Busqué correos, teléfonos, cédulas y claves en la bitácora y el README: solo están mi nombre y el enlace del repositorio |

**Lo que la IA no encontró:** la línea `>` sobrante en la bitácora publicada (H-11); que faltaba `.env.example`, que la tarea exige (H-10); los avisos B905 y E501 de ruff (H-05 y H-07), que salieron del linter y no de su revisión; y, al revisar el código que escribió el agente, que `math.isfinite(10**400)` lanza `OverflowError` (H-03).

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| Un iterador o generador como `notas` lanza `TypeError` | El contrato dice «lista o tupla» y está documentado en el README y el docstring; convertirlo con `list()` queda como mejora menor | Decidirlo cuando se construya `consola.py` |
| `consola.py` (leer los datos y mostrar avisos) | Es otra funcionalidad (semanas siguientes) | Al leer texto, convertir con `float()` y capturar `ValueError` antes de llamar a `calculo.py` |
| Confirmar el criterio de redondeo (mitades hacia arriba) y si hay notas con más de 1 decimal | Es una pregunta para el cliente (P-02 de los requisitos) | Preguntarlo al docente o al cliente |
| pip-audit solo cubre herramientas de desarrollo | No hay dependencias de ejecución | Volver a auditar si se agrega alguna |

**Claves expuestas:** Ninguna. Busqué `password`, `secret`, `api_key`, `token` y llaves privadas en todo el historial de Git (`git log --all -p`) sin coincidencias, y no hay archivos `.env` versionados.
