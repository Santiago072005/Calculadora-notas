# Guía de despliegue

**Proyecto:** Calculadora de nota final ponderada. **Autor:** Erick Santiago Marroquin Aldana.

## 1. Qué se despliega

Un programa de consola en Python sin base de datos, sin servidor y sin dependencias de ejecución (decisión del [ADR-001](Marroquinal_Erik_S4_Diseno.docx)). «Desplegar» significa dejar el código funcionando en el computador de quien lo va a usar. No hay variables de entorno ni claves (ver `.env.example`).

## 2. Requisitos del equipo

- Python 3.10 o superior (se probó en 3.10 y 3.12 en el pipeline de CI).
- Git, para clonar el repositorio.
- No necesita internet para ejecutar el programa; solo para instalar las herramientas de desarrollo.

## 3. Pasos

1. Clonar y entrar a la carpeta del proyecto:
   ```bash
   git clone https://github.com/Santiago072005/Calculadora-notas.git
   cd Calculadora-notas
   ```
2. Solo para usar el programa no hace falta más: `python consola.py`.
3. Para desarrollar o verificar, crear el entorno e instalar las herramientas con versión fijada:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate     Linux o macOS: source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```

## 4. Cómo comprobar que quedó bien

| Comprobación | Comando | Resultado esperado |
|---|---|---|
| Pruebas y cobertura | `pytest --cov=calculo --cov=consola --cov-branch --cov-fail-under=90` | 156 pruebas pasan; `calculo.py` 100 %, `consola.py` 97 % |
| Linter | `ruff check .` | Sin avisos |
| Dependencias | `pip-audit -r requirements-dev.txt` | Sin vulnerabilidades (en Python 3.12; ver nota) |
| Uso real | `python consola.py` con `4,5` al 40 % y `3` al 60 % | Nota final 3.6 |

Nota: en Python 3.10 `pip-audit` resuelve `filelock` 4.1.0, que tiene vulnerabilidades, y la versión corregida exige Python 3.11 o superior. Por eso el pipeline ejecuta `pip-audit` solo en 3.12. Es una herramienta de desarrollo; el programa solo usa la librería estándar.

## 5. Despliegue automático (CI)

El archivo [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) ejecuta el linter, las pruebas con cobertura y la auditoría en cada `push` a `main` y en cada pull request. Una versión solo se considera lista si el pipeline está en verde.

## 6. Cómo volver a una versión anterior

Cada cambio es un commit. Para volver a un estado que funcionaba: `git checkout <hash>` para mirarlo, o `git revert <hash>` para deshacer un cambio sin borrar la historia.

## 7. Qué no cubre esta guía

No se publica en un servidor ni como aplicación de celular. Una persona entrevistada dijo que la usaría en el celular; esa necesidad no está cubierta y queda como mejora futura.
