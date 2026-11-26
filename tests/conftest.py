"""Fixtures con datos sinteticos (ficticios). Nombres y telefonos inventados."""
import pytest


def _c(nombre, nota, porcentaje):
    return {"nombre": nombre, "nota": nota, "porcentaje": porcentaje}


@pytest.fixture
def cursos_sinteticos():
    return [
        {  # 3.5*.30 + 4.0*.30 + 4.5*.40 = 1.05 + 1.20 + 1.80 = 4.05
            "estudiante": "María José Pérez",
            "telefono": "300 000 0000",
            "materia": "Cálculo Diferencial",
            "componentes": [_c("Parcial 1", 3.5, 30), _c("Parcial 2", 4.0, 30),
                            _c("Final", 4.5, 40)],
            "esperado": 4.05,
        },
        {  # 4.2*.50 + 3.8*.50 = 2.10 + 1.90 = 4.00
            "estudiante": "Nicolás Muñoz",
            "telefono": "3000000001",
            "materia": "Física I",
            "componentes": [_c("Taller", 4.2, 50), _c("Examen", 3.8, 50)],
            "esperado": 4.0,
        },
        {  # 0*.40 + 5*.60 = 0 + 3.00 = 3.00 (nota 0 y nota 5)
            "estudiante": "Sofía D'Ávila",
            "telefono": "300 000 0002",
            "materia": "Programación",
            "componentes": [_c("Quiz", 0, 40), _c("Proyecto", 5, 60)],
            "esperado": 3.0,
        },
        {  # 4.7*1.00 = 4.70 (un solo componente al 100 %)
            "estudiante": "",
            "telefono": "3000000003",
            "materia": "Ética",
            "componentes": [_c("Ensayo", 4.7, 100)],
            "esperado": 4.7,
        },
        {  # 5*.25 + 5*.25 + 5*.50 = 1.25 + 1.25 + 2.50 = 5.00
            "estudiante": "X",
            "telefono": "300 000 0004",
            "materia": "Inglés",
            "componentes": [_c("Oral", 5, 25), _c("Escrito", 5.0, 25),
                            _c("Final", 5, 50)],
            "esperado": 5.0,
        },
        {  # 2.5*.20 + 3.5*.30 + 4.5*.50 = 0.50 + 1.05 + 2.25 = 3.80
            "estudiante": "Jhon Édinson Ñáñez",
            "telefono": "3000000005",
            "materia": "Estadística",
            "componentes": [_c("Taller", 2.5, 20), _c("Parcial", 3.5, 30),
                            _c("Final", 4.5, 50)],
            "esperado": 3.8,
        },
        {  # 3.33*.33 + 3.33*.33 + 3.34*.34 = 1.0989 + 1.0989 + 1.1356
            # = 3.3334 -> 3.33
            "estudiante": "Valentina Ríos",
            "telefono": "300 000 0006",
            "materia": "Química",
            "componentes": [_c("A", 3.33, 33), _c("B", 3.33, 33),
                            _c("C", 3.34, 34)],
            "esperado": 3.33,
        },
        {  # 0*1.00 = 0.00 (todo en cero)
            "estudiante": "Ángel Ñungo",
            "telefono": "3000000007",
            "materia": "Álgebra Lineal",
            "componentes": [_c("Único", 0, 100)],
            "esperado": 0.0,
        },
        {  # 4.5*.10 + 3.0*.20 + 4.0*.30 + 5.0*.40
            # = 0.45 + 0.60 + 1.20 + 2.00 = 4.25
            "estudiante": "Luz Ángela Ospina",
            "telefono": "300 000 0008",
            "materia": "Historia de Colombia",
            "componentes": [_c("Taller", 4.5, 10), _c("Quiz", 3.0, 20),
                            _c("Parcial", 4.0, 30), _c("Final", 5.0, 40)],
            "esperado": 4.25,
        },
        {  # 4.5*.05 + 5.0*.95 = 0.225 + 4.75 = 4.975 -> 4.98 (mitad arriba)
            "estudiante": "Tomás Gómez",
            "telefono": "3000000009",
            "materia": "Economía",
            "componentes": [_c("Asistencia", 4.5, 5), _c("Final", 5.0, 95)],
            "esperado": 4.98,
        },
    ]


@pytest.fixture(params=range(10), ids=lambda i: f"curso{i + 1}")
def curso(request, cursos_sinteticos):
    """Un curso sintetico a la vez, para que cada uno sea su propia prueba."""
    return cursos_sinteticos[request.param]


@pytest.fixture(params=["4,5", "", " ", "cinco", "4.5", "5 ", "None"],
                ids=["coma", "vacio", "espacio", "palabra", "punto-texto",
                     "con-espacio", "None-texto"])
def texto_invalido(request):
    """Texto que alguien podria teclear como nota (debe rechazarse)."""
    return request.param
