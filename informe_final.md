# Informe final del proyecto integrador

Proyecto: Calculadora de nota final ponderada (Python)  
Estudiante: Erik Marroquinal  
Repositorio: [github.com/Santiago072005/Calculadora-notas](https://github.com/Santiago072005/Calculadora-notas)  
Fecha: 2026-11-26

## 1. Resumen

Los estudiantes de mi curso calculan la nota final a mano y se equivocan porque cada componente pesa distinto. Construí una calculadora de nota final ponderada en Python (notas de 0 a 5, porcentajes que suman 100) con un asistente de código, Claude, y usé la IA en las seis fases del ciclo: propuesta, requisitos, diseño, código, pruebas y revisión de operación y seguridad. El estado final es la capa de cálculo `calculo.py`, con 138 pruebas que pasan, 100 % de cobertura de sus líneas y ramas, `ruff` sin avisos, `pip-audit` sin vulnerabilidades y un pipeline de CI que ejecuta las tres comprobaciones. La interfaz de consola (`consola.py`) **no está construida**, así que hoy el programa no se puede usar desde el teclado; lo explico en la sección 5. El resultado principal de la verificación: la IA se equivocó en cinco puntos de cuatro fases distintas (sección 4), y cada error lo encontró una comprobación que no dependía de ella: contraste con mi propuesta, comparación con el ADR, una prueba que falla, un linter o romper el código a propósito.

## 2. Problema y usuario

**Quién tiene el problema.** Los estudiantes de mi curso. Según mi propuesta de proyecto, «a veces se equivocan porque cada materia tiene un peso distinto» y «es fácil olvidar un porcentaje y obtener una nota final incorrecta». Hoy lo resuelven con calculadora o a mano (por ejemplo parcial 30 %, taller 20 %, examen final 50 %).

**Qué necesita.** Una nota final correcta con cada peso, un aviso claro cuando los datos están mal escritos y una forma de comprobar el resultado contra el cálculo a mano. El criterio de éxito de la propuesta es: «Sabré que la IA funcionó si el programa da la misma nota que mi cálculo a mano en al menos 5 ejemplos y si todas las pruebas pasan».

**Evidencia.** Las citas de la propuesta (módulo 1) y las necesidades, historias de usuario (HU-01 a HU-04) y requisitos no funcionales (RNF-01 a RNF-04) que salen de ellas están en la sección 1 del [documento de diseño](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx). Entrevista del módulo 2: <mark>PENDIENTE: enlazar aquí el documento de la entrevista</mark>.

## 3. La IA en el ciclo de vida

Asocio cada semana de trabajo con la fase por su contenido: la semana 5 es código y también pruebas (pruebas escritas antes que el código), la semana 6 es revisión de código, seguridad y mantenimiento (operación) y la semana 7 es pruebas. Cada enlace va a un archivo o commit del repositorio.

| Fase | Qué hice con IA | Herramienta | Evidencia | Cómo verifiqué |
|---|---|---|---|---|
| 1. Fundamentos | Definí el problema, el usuario y el criterio de éxito de la propuesta; el asistente de código previsto es Claude | Claude | [Documento de diseño, sección 1 (citas)](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx) | Cada requisito posterior cita una frase de la propuesta |
| 2. Requisitos | Adaptar el formato de requisitos de la semana 3 a la calculadora: 3 necesidades, 4 historias y 4 RNF | Claude | [Documento de diseño, sección 1](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx) | Comparé cada requisito con las citas de mi propuesta; lo que no tenía cita quedó como supuesto (caso 1) |
| 3. Diseño | Tres alternativas con matriz ponderada, diagramas C4 en Mermaid, modelo de datos, API y ADR-001 | Claude | [Documento de diseño](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx), [diagramas](https://github.com/Santiago072005/Calculadora-notas/tree/main/docs/diagramas) | Revisé cada diagrama contra el ADR y cada puntaje contra los requisitos; 4 rondas de prompts (caso 2) |
| 4. Código | Implementar `calcular_nota_final` a partir de mi contrato y mis pruebas, refactorizar y corregir | Claude (modo agente) | [calculo.py](https://github.com/Santiago072005/Calculadora-notas/blob/main/calculo.py), [bitácora, entradas 6 a 10 y 12](https://github.com/Santiago072005/Calculadora-notas/blob/main/bitacora_ia.md) | Leí el código línea por línea y corrí las pruebas; no se modificó ninguna prueba para que pasara (casos 3 y 4) |
| 5. Pruebas | Primero 20 pruebas en rojo (semana 5); luego 100 pruebas con particiones de equivalencia, valores límite y tabla de decisión, y datos sintéticos (semana 7) | Claude y pytest | [test_calculo.py](https://github.com/Santiago072005/Calculadora-notas/blob/main/test_calculo.py), [tests/](https://github.com/Santiago072005/Calculadora-notas/tree/main/tests), [registro_pruebas.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/registro_pruebas.md) | Revisé cada prueba generada con tres preguntas y rompí el código 15 veces para ver si las pruebas fallaban (caso 5) |
| 6. Operación | Revisión de código y seguridad, dependencias fijadas, `.env.example`, README, licencia y pipeline de CI (que en su primera ejecución encontró un problema de auditoría en Python 3.10, ver pendientes) | Claude, ruff, pip-audit | [revision_seguridad.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/revision_seguridad.md), [ci.yml](https://github.com/Santiago072005/Calculadora-notas/blob/main/.github/workflows/ci.yml) | Ejecuté cada hallazgo de la IA en Python; de 12 hallazgos de la IA, 8 eran reales y 4 falsos positivos |

## 4. Verificación: lo que la IA hizo mal y cómo lo encontré

### Caso 1: requisitos que no salían de mi propuesta

- **Fase:** requisitos.
- **Qué propuso la IA:** un primer borrador de requisitos con datos que mi propuesta no dice, como que el programa funciona sin internet y un presupuesto.
- **Qué estaba mal:** eran inventados; un requisito sin una frase de mi propuesta no tiene dueño ni se puede aceptar.
- **Cómo lo detecté:** al comparar cada requisito con las citas de la propuesta que adjunté con el documento de la semana 3.
- **Qué hice:** rehíce los requisitos con citas. «Sin internet» quedó como RNF-03 marcado «supuesto a confirmar» y como pregunta pendiente P-01. Evidencia: sección 1 del [documento de diseño](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx).

### Caso 2: un diagrama que contradecía mi decisión de diseño

- **Fase:** diseño.
- **Qué propuso la IA:** diagramas C4 con una base de datos y un sistema externo de la plantilla, y una matriz de decisión donde la exactitud no era igual en las tres alternativas.
- **Qué estaba mal:** el ADR-001 decide no usar base de datos ni servicios externos, y la exactitud no depende de la arquitectura, así que la alternativa A estaba hecha artificialmente débil.
- **Cómo lo detecté:** revisión de cada diagrama contra el ADR y de cada puntaje contra los requisitos, con un prompt de revisión aparte (prompts 3 y 4 del registro).
- **Qué hice:** quité la base de datos, el sistema externo y el actor «Autor», puse la exactitud igual en las tres alternativas y agregué `mostrar_error` a la capa de consola, que nadie mostraba. Evidencia: secciones 2, 3 y 7 del [documento de diseño](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx).

### Caso 3: mensaje de error engañoso y redondeo con `round()`

- **Fase:** código.
- **Qué propuso la IA:** una implementación que pasó mis 20 pruebas a la primera. Usaba el formato `:g` para mostrar la suma y `round(..., 2)` para redondear.
- **Qué estaba mal:** con `:g`, una suma de 99.999999 se mostraba como «Los porcentajes suman 100 %, deben sumar 100 %». Y `round()` da 0.12 para 0.125, 3.12 para 3.125 y 2.67 para 2.675, cuando quien calcula a mano espera 0.13, 3.13 y 2.68.
- **Cómo lo detecté:** la propia IA lo señaló como sugerencia opcional; escribí primero una prueba que lo reproduce y falló. Con el redondeo escribí tres pruebas que fallaron con `round()`.
- **Qué hice:** cambié a `.10g` (prueba en rojo [ab204c7](https://github.com/Santiago072005/Calculadora-notas/commit/ab204c7), corrección [b123cd9](https://github.com/Santiago072005/Calculadora-notas/commit/b123cd9)) y a `Decimal` con `ROUND_HALF_UP` (rojo [deec35f](https://github.com/Santiago072005/Calculadora-notas/commit/deec35f), verde [6251a3c](https://github.com/Santiago072005/Calculadora-notas/commit/6251a3c)). Bitácora, entradas 7 y 13.

### Caso 4: un error en el código que escribió el agente

- **Fase:** código (revisión de la semana 6).
- **Qué propuso la IA:** la función `_es_numero_valido`, que rechaza `nan`, `inf`, `bool` y texto. Las 12 pruebas nuevas pasaron.
- **Qué estaba mal:** `math.isfinite(10**400)` lanza `OverflowError` en lugar del `ValueError` que promete el contrato.
- **Cómo lo detecté:** revisé su diff línea por línea; escribí una prueba que lo reproduce y falló.
- **Qué hice:** `try/except OverflowError` ([e28caf0](https://github.com/Santiago072005/Calculadora-notas/commit/e28caf0) en rojo, [f821ffd](https://github.com/Santiago072005/Calculadora-notas/commit/f821ffd) en verde). Verifiqué además con `diff` que el agente solo cambió `calculo.py`. Bitácora, entrada 12; informe de seguridad, hallazgo H-03.

### Caso 5: pruebas de la IA que pasaban pero no protegían

- **Fase:** pruebas.
- **Qué propuso la IA:** 83 pruebas a partir de mi tabla de casos, todas en verde a la primera.
- **Qué estaba mal:** que pasen no prueba que sirvan. Al romper `calculo.py` a propósito, 2 de 15 cambios no hicieron fallar nada: usar `float` en lugar de `Decimal` y quitar el formato `.10g` del mensaje. Mis casos y los de la IA daban lo mismo con las dos versiones.
- **Cómo lo detecté:** cambio manual de una línea cada vez, `pytest` y `git restore calculo.py`.
- **Qué hice:** agregué `[2.675]` → 2.68, `[1.005]` → 1.01 y `[33.3, 33.3, 33.3]` → «suman 99.9 %»; repetí los cambios y ahora fallan ([db2cc52](https://github.com/Santiago072005/Calculadora-notas/commit/db2cc52)). Además descarté una prueba repetida y cambié los bucles `for` de los datos sintéticos por una prueba por caso. Detalle en [registro_pruebas.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/registro_pruebas.md), sección 3.

## 5. Estado final del sistema

- **Arquitectura:** módulo en capas sin base de datos ni servicios externos (ADR-001, [documento de diseño](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx), secciones 2 a 4). Capa de cálculo `calculo.py` (funciones puras: `validar_notas`, `validar_porcentajes`, `calcular_nota_final`) y, en el diseño, una capa de consola `consola.py`, la única que usaría `input` y `print`. Se eligió sobre un script de un solo archivo y sobre una aplicación web porque la exactitud y la facilidad de prueba pesan 5 y esta alternativa permite probar el cálculo sin teclado (94 puntos contra 93 del script).

![Diagrama de componentes del diseño (semana 4): `consola.py` está diseñada pero no construida; `calculo.py` y las pruebas están terminadas](docs/diagramas/comp_c.png)

- **Funcionalidades terminadas:** la capa de cálculo cubre HU-01 (calcular la nota final: `[3.0, 0, 5.0]` con `[30, 20, 50]` da 3.4), HU-02 (aviso cuando los porcentajes no suman 100) y HU-03 (aviso cuando una nota está fuera de 0 a 5), como funciones que devuelven la nota o lanzan `ValueError` con el mensaje exacto. No está terminada HU-04 (mostrar el aporte de cada nota) ni la capa de consola, así que el estudiante todavía no puede usar el programa desde la terminal.
- **Pruebas:** 138 pruebas en `pytest` (38 de las semanas 5 y 6 y 100 de la semana 7 en `tests/`) y cobertura de `calculo.py` del 100 % de líneas y ramas (39 instrucciones y 22 ramas, medido con `pytest --cov`). `ruff` con reglas E, F, B y S da 0 avisos y `pip-audit` no encuentra vulnerabilidades. El [pipeline de CI](https://github.com/Santiago072005/Calculadora-notas/blob/main/.github/workflows/ci.yml) ejecuta `ruff` y las pruebas con cobertura en Python 3.10 y 3.12, y `pip-audit` solo en 3.12; Su última ejecución, sobre el commit [c849902](https://github.com/Santiago072005/Calculadora-notas/commit/c849902e3ef58795cdf6ed4c029e3ae0128b7fa3), terminó en verde en 18 segundos: [ejecución 45890679915](https://github.com/Santiago072005/Calculadora-notas/actions/runs/45890679915). Antes de subirlo corrí los mismos tres pasos en un entorno limpio con las versiones fijadas de `requirements-dev.txt` (ruff 0.16.9, pytest 9.1.1, pytest-cov 7.1.0, pip-audit 2.10.1): 138 pruebas, 100 % de cobertura, 0 avisos y sin vulnerabilidades. La cobertura del 100 % no demuestra que no haya errores: por eso rompí el código a propósito (sección 4, caso 5).
- **Pendientes:** (1) `consola.py` y HU-04: no alcanzaron en las semanas del curso; sin ellos RNF-01 (5 ejemplos contra cálculo a mano) y RNF-04 solo se verifican a nivel de función. (2) RNF-03 (funciona sin internet) y P-01 siguen como supuesto, sin confirmar. (3) Un iterador o generador como lista de notas lanza `TypeError`; el contrato dice «lista o tupla» y está documentado. (4) El mensaje de suma de 100.000000002 se ve «suman 100 %, deben sumar 100 %» por el formato `.10g`. (5) P-02: si se admiten notas con más de un decimal, que debe responder el docente. (6) `pip-audit` no se ejecuta en Python 3.10: en la primera ejecución del pipeline halló `filelock` 4.1.0 con 17 vulnerabilidades, dependencia indirecta de `pip-audit`; la versión corregida (4.2.1) exige Python 3.11 o superior. El programa no usa esa librería (solo la estándar), así que lo audité solo en 3.12 y lo dejé comentado en `ci.yml`.

## 6. Reflexión ética y legal

| Principio | Decisión en mi proyecto | Evidencia |
|---|---|---|
| Datos personales (Ley 1581 de 2012) | El programa no guarda nombres, códigos ni contraseñas (ADR-001, sin base de datos). Las pruebas usan solo datos sintéticos: nombres y teléfonos inventados, con casos difíciles como tildes, ñ y apóstrofo. Busqué correos, teléfonos, cédulas y claves en el repositorio y en el historial de Git sin coincidencias | [registro_pruebas.md, sección 4](https://github.com/Santiago072005/Calculadora-notas/blob/main/registro_pruebas.md), [revision_seguridad.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/revision_seguridad.md), [tests/conftest.py](https://github.com/Santiago072005/Calculadora-notas/blob/main/tests/conftest.py) |
| Sesgo | El redondeo escolar (mitades hacia arriba) lo decidí yo y lo documenté; el `round()` por defecto de Python habría dado a estudiantes con notas como 3.125 una décima de centésima menos que su cálculo a mano. Los textos como «4,5» (coma decimal, habitual en Colombia) se rechazan con un mensaje, no se interpretan a ciegas | Commit [6251a3c](https://github.com/Santiago072005/Calculadora-notas/commit/6251a3c), prueba `texto_invalido` en [tests/](https://github.com/Santiago072005/Calculadora-notas/tree/main/tests) |
| Transparencia | Cada sugerencia de la IA tiene una entrada en la bitácora con prompt, decisión, razón y verificación (18 entradas: 7 aceptadas, 8 aceptadas con cambios, 3 rechazadas). 27 de los 28 commits llevan la línea `Co-Authored-By: Claude` | [bitacora_ia.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/bitacora_ia.md) |
| Responsabilidad | Yo respondo por el resultado: ninguna prueba se modificó para que el código pasara, cada hallazgo de la IA se ejecutó antes de aceptarlo y rechacé sugerencias que agregaban alcance (excepción propia, dejar la validación de tipos solo en la consola: la validé en `calculo.py`) | Bitácora, entradas 8, 9 y 14; [revision_seguridad.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/revision_seguridad.md), sección 3 |
| Propiedad intelectual y política de uso | Licencia MIT a mi nombre. El proyecto declara que el código y los borradores los generó Claude bajo mi dirección y que yo los revisé. Las herramientas de desarrollo son pytest, ruff y pytest-cov (licencia MIT según `pip show`) y pip-audit. No copié código de terceros ni usé datos de otros estudiantes | [LICENSE](https://github.com/Santiago072005/Calculadora-notas/blob/main/LICENSE), [README, sección de uso de IA](https://github.com/Santiago072005/Calculadora-notas/blob/main/README.md) |

**El dilema más importante: cuánto delegar y cómo decirlo.** En varios momentos le pedí a la IA que redactara por mí, incluso «como si lo hubiera hecho yo»: el documento de diseño, las respuestas de la bitácora y la reflexión de la semana 5. Eso choca con lo que el curso evalúa, que es que yo pueda explicar cada decisión y cada valor esperado. Lo resolví de tres formas: declaro aquí que esas redacciones fueron borradores de la IA que adapté; separo en la bitácora lo que propuso la IA de lo que decidí yo (aceptada, con cambios o rechazada, y por qué); y preparé la sustentación de modo que cada cifra de este informe se pueda reproducir con un comando del README. Lo que no puedo delegar es la decisión de qué aceptar, y por eso las partes que más pesan (elegir la alternativa B, rechazar la excepción propia, exigir el redondeo escolar) tienen una razón escrita.

## 7. Aprendizajes

- **Qué sé hacer ahora.** Escribir pruebas antes del código y ver que fallen; derivar casos con particiones, valores límite y tablas de decisión; usar `git restore` para romper el código a propósito y comprobar que las pruebas protegen; revisar un diff buscando lo que la IA no probó; y usar un linter, `pip-audit` y un pipeline como segunda opinión que no depende de la IA.
- **En qué confié de más.** En que «todo en verde» significa «bien»: la IA pasó mis 20 pruebas y las 83 suyas a la primera y aun así había un mensaje engañoso, un redondeo equivocado y dos huecos en las pruebas. También confié de más en la redacción de la IA: cuando no tenía la fuente, inventó requisitos.
- **Qué haría distinto.** Probar con datos reales desde el principio, construir `consola.py` antes de pulir la capa de cálculo para tener algo que un estudiante pueda usar, pedir a la IA que cite siempre de qué frase de mi propuesta sale cada requisito y poner el pipeline de CI desde la primera semana en lugar de al final.

## 8. Anexos

- Bitácora de uso de IA: [bitacora_ia.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/bitacora_ia.md)
- Documento de diseño (módulo 3): [docs/Marroquinal_Erik_S4_Diseno.docx](https://github.com/Santiago072005/Calculadora-notas/blob/main/docs/Marroquinal_Erik_S4_Diseno.docx) y [diagramas](https://github.com/Santiago072005/Calculadora-notas/tree/main/docs/diagramas)
- Código y contrato (módulo 4): [calculo.py](https://github.com/Santiago072005/Calculadora-notas/blob/main/calculo.py), [README.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/README.md)
- Revisión de código y seguridad (módulo 6): [revision_seguridad.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/revision_seguridad.md)
- Pruebas (módulo 5): [registro_pruebas.md](https://github.com/Santiago072005/Calculadora-notas/blob/main/registro_pruebas.md) y [tests/](https://github.com/Santiago072005/Calculadora-notas/tree/main/tests)
- Pipeline (módulo 6): [.github/workflows/ci.yml](https://github.com/Santiago072005/Calculadora-notas/blob/main/.github/workflows/ci.yml) y [última ejecución en verde](https://github.com/Santiago072005/Calculadora-notas/actions/runs/45890679915)
