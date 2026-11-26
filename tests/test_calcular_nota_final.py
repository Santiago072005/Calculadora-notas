"""Pruebas de calcular_nota_final (regla R3), derivadas de la tabla revisada.

Los valores esperados son de 2 decimales ya redondeados (el contrato exige
redondeo a 2 decimales), por eso se comparan con igualdad exacta: un literal
como 0.13 es el mismo float que devuelve el redondeo, y la igualdad exacta
detecta errores de redondeo que una tolerancia podria ocultar.
"""

import re

import pytest

from calculo import calcular_nota_final


@pytest.mark.parametrize(
    "notas, porcentajes, esperado",
    [
        # R3-P1: ejemplo del contrato
        pytest.param([3.0, 0, 5.0], [30, 20, 50], 3.4, id="R3-P1"),
        # R3-P2: una sola nota
        pytest.param([4.5], [100], 4.5, id="R3-P2"),
        # R3-P3: tuplas
        pytest.param((4, 2), (25, 75), 2.5, id="R3-P3"),
        # R3-P4: promedio simple
        pytest.param([4, 2], [50, 50], 3.0, id="R3-P4"),
        # R3-P5: 0.124 redondea hacia abajo
        pytest.param([1.24, 0], [10, 90], 0.12, id="R3-P5"),
        # R3-P6: 0.125 es mitad y sube
        pytest.param([1.25, 0], [10, 90], 0.13, id="R3-P6"),
        # R3-P7: 0.126 sube
        pytest.param([1.26, 0], [10, 90], 0.13, id="R3-P7"),
        # R3-P8: todo en cero
        pytest.param([0, 0], [50, 50], 0.0, id="R3-P8"),
        # R3-P9: todo en 5
        pytest.param([5, 5], [40, 60], 5.0, id="R3-P9"),
        # R3-M1 (hallado al romper el código): 2.675 en binario es 2.67499999...,
        # pero la regla pide redondear lo que se ve: 2.675 -> 2.68
        pytest.param([2.675], [100], 2.68, id="R3-M1"),
        # R3-M2 (hallado al romper el código): igual que M1 con 1.005 -> 1.01
        pytest.param([1.005], [100], 1.01, id="R3-M2"),
        # R3-L1: mínimo posible
        pytest.param([0], [100], 0.0, id="R3-L1"),
        # R3-L6: extremos 0 y 5
        pytest.param([0, 5], [50, 50], 2.5, id="R3-L6"),
        # R3-X1a: cada peso va con su nota
        pytest.param([5, 0], [80, 20], 4.0, id="R3-X1a"),
        # R3-X1b: orden inverso de las notas
        pytest.param([0, 5], [80, 20], 1.0, id="R3-X1b"),
    ],
)
def test_nota_final_valor_esperado(notas, porcentajes, esperado):
    assert calcular_nota_final(notas, porcentajes) == esperado


def test_nota_final_entera_se_devuelve_como_float():
    # R3-P10: [3], [100] -> 3.0 y de tipo float (no int)
    resultado = calcular_nota_final([3], [100])
    assert resultado == 3.0
    assert type(resultado) is float


@pytest.mark.parametrize(
    "notas, porcentajes, mensaje",
    [
        # R3-L3: una nota y dos porcentajes
        pytest.param(
            [3], [50, 50], "Debe haber una nota por cada porcentaje", id="R3-L3"
        ),
        # R3-L4: dos notas y un porcentaje
        pytest.param(
            [3, 4], [100], "Debe haber una nota por cada porcentaje", id="R3-L4"
        ),
        # R3-L5: nota fuera de rango por 0.01
        pytest.param(
            [5.01, 0], [50, 50], "La nota 5.01 está fuera de 0 a 5", id="R3-L5"
        ),
        # R3-L7: suma 99
        pytest.param(
            [3, 3],
            [50, 49],
            "Los porcentajes suman 99 %, deben sumar 100 %",
            id="R3-L7",
        ),
        # R3-D1: listas vacías
        pytest.param([], [], "Debe haber al menos una nota", id="R3-D1"),
        # R3-D2a: el tamaño se revisa antes que la nota inválida
        pytest.param(
            [9], [50, 50], "Debe haber una nota por cada porcentaje", id="R3-D2a"
        ),
        # R3-D2b: el tamaño se revisa antes que el porcentaje 0
        pytest.param(
            [3, 3, 3], [0, 100], "Debe haber una nota por cada porcentaje", id="R3-D2b"
        ),
        # R3-D3a: la nota se revisa antes que el porcentaje 0
        pytest.param([6], [0], "La nota 6 está fuera de 0 a 5", id="R3-D3a"),
        # R3-D3b: nota de tipo inválido antes que porcentajes
        pytest.param(
            ["a"], [100], "La nota 'a' no es un número válido", id="R3-D3b"
        ),
        # R3-D3c: tipo de todas las notas antes que el rango
        pytest.param(
            [6, "x"], [50, 50], "La nota 'x' no es un número válido", id="R3-D3c"
        ),
        # R3-D3d: bool como nota
        pytest.param(
            [True], [100], "La nota True no es un número válido", id="R3-D3d"
        ),
        # R3-D4a: porcentaje 0
        pytest.param([3], [0], "Cada porcentaje debe ser mayor que 0", id="R3-D4a"),
        # R3-D4b: porcentaje de tipo inválido
        pytest.param(
            [3], ["a"], "El porcentaje 'a' no es un número válido", id="R3-D4b"
        ),
        # R3-D4c: negativo, antes de revisar la suma
        pytest.param(
            [3, 3], [-10, 110], "Cada porcentaje debe ser mayor que 0", id="R3-D4c"
        ),
        # R3-D5a: suma 90
        pytest.param(
            [3, 3],
            [50, 40],
            "Los porcentajes suman 90 %, deben sumar 100 %",
            id="R3-D5a",
        ),
        # R3-D5b: suma 100.5
        pytest.param(
            [3, 3],
            [60, 40.5],
            "Los porcentajes suman 100.5 %, deben sumar 100 %",
            id="R3-D5b",
        ),
    ],
)
def test_nota_final_errores_con_mensaje_exacto(notas, porcentajes, mensaje):
    with pytest.raises(ValueError, match=re.escape(mensaje)):
        calcular_nota_final(notas, porcentajes)


def test_nota_final_entero_gigante_no_es_numero_valido():
    # R3-X3: 10**400 no es convertible a float; se exige prefijo y sufijo,
    # sin fijar el repr completo del entero.
    patron = re.escape("La nota ") + ".*" + re.escape("no es un número válido")
    with pytest.raises(ValueError, match=patron):
        calcular_nota_final([10**400], [100])
