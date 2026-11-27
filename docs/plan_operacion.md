# Plan de operación

**Proyecto:** Calculadora de nota final ponderada. **Responsable:** Erick Santiago Marroquin Aldana (único autor y mantenedor).

Es un proyecto académico de una persona. El plan se limita a lo que se puede cumplir.

## 1. Qué hay que operar

Un programa de consola que corre en el computador de cada usuario. No hay servidor, base de datos ni cuentas, así que no hay disponibilidad que vigilar ni copias de seguridad de datos. El programa no guarda ni envía ninguna nota: los datos viven solo mientras el programa corre.

## 2. Datos personales

El programa no almacena datos personales. Los ejemplos del repositorio, las pruebas y las capturas usan datos sintéticos. La única información de una persona real es la entrevista de `docs/entrevista_modulo2.md`, que está anonimizada y se publicó con su autorización (confirmada el 26 de noviembre de 2026). Está conforme con la Ley 1581 de 2012 en lo que aplica a este proyecto.

## 3. Mantenimiento rutinario

| Tarea | Cuándo | Cómo |
|---|---|---|
| Revisar el pipeline | En cada push | Ver la pestaña Actions de GitHub; no se entrega con el pipeline en rojo |
| Auditar dependencias | Antes de cada entrega y cuando `pip-audit` avise | `pip-audit -r requirements-dev.txt`; subir la versión fijada en `requirements-dev.txt` |
| Actualizar herramientas | Cuando haya una corrección de seguridad | Cambiar la versión, correr las 156 pruebas y el linter |
| Subir la versión de Python | Cuando una versión salga de soporte | Cambiar `python-version` en `ci.yml` y `requires-python` en `pyproject.toml` |

## 4. Qué hacer ante un problema

1. **Un usuario reporta una nota incorrecta.** Pedir las notas y los porcentajes (de ejemplo, nunca datos reales de otra persona), reproducirlo, escribir primero una prueba que falle, corregir y hacer commit con la prueba en verde.
2. **Falla el pipeline.** Leer el paso que falló. Si es una vulnerabilidad, actualizar la dependencia; si es una prueba, no modificarla para que pase sin entender por qué falla.
3. **Un cambio rompió algo.** Volver con `git revert <hash>` (ver la guía de despliegue).

## 5. Quién responde por los errores

Responde el autor, no la IA. La IA propuso código y pruebas, pero cada sugerencia se revisó y quedó registrada en `bitacora_ia.md`. El README advierte que el programa es una ayuda y que quien lo usa debe comprobar sus resultados importantes.

## 6. Riesgos conocidos y pendientes

- La interfaz de consola no pasó una revisión de seguridad aparte (la revisión de la semana 6 fue sobre `calculo.py`).
- No hay versión para celular.
- Con una sola persona mantenedora, si el autor no está disponible no hay quien corrija. Por eso el código es pequeño, tiene docstrings y 156 pruebas que explican su comportamiento.
