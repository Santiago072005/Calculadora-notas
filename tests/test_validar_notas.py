"""Pruebas de validar_notas (regla R1), derivadas de la tabla revisada."""

import re

import pytest

from calculo import validar_notas

NAN = float("nan")
INF = float("inf")


@pytest.mark.parametrize(
    "notas",
    [
        pytest.param([3], id="R1-P1"),  # R1-P1: un entero válido
        pytest.param([2.5, 4.75], id="R1-P2"),  # R1-P2: decimales válidos
        pytest.param((0, 5.0, 1), id="R1-P3"),  # R1-P3: tupla con extremos
        pytest.param([0], id="R1-L2"),  # R1-L2: extremo inferior entero
        pytest.param([0.0], id="R1-L3"),  # R1-L3: extremo inferior float
        pytest.param([0.01], id="R1-L4"),  # R1-L4: justo sobre el mínimo
        pytest.param([4.99], id="R1-L5"),  # R1-L5: justo bajo el máximo
        pytest.param([5], id="R1-L6"),  # R1-L6: extremo superior entero
        pytest.param([5.0], id="R1-L7"),  # R1-L7: extremo superior float
    ],
)
def test_notas_validas_devuelven_none(notas):
    assert validar_notas(notas) is None


@pytest.mark.parametrize(
    "notas, mensaje",
    [
        # R1-P4: nota negativa
        pytest.param([-1], "La nota -1 está fuera de 0 a 5", id="R1-P4"),
        # R1-P5: nota sobre 5
        pytest.param([6], "La nota 6 está fuera de 0 a 5", id="R1-P5"),
        # R1-P6: texto
        pytest.param(["a"], "La nota 'a' no es un número válido", id="R1-P6"),
        # R1-P7: None
        pytest.param([None], "La nota None no es un número válido", id="R1-P7"),
        # R1-P8: True es bool, no número
        pytest.param([True], "La nota True no es un número válido", id="R1-P8"),
        # R1-P9: False es bool, no número
        pytest.param([False], "La nota False no es un número válido", id="R1-P9"),
        # R1-P10: nan no es finito
        pytest.param([NAN], "La nota nan no es un número válido", id="R1-P10"),
        # R1-P11: infinito positivo
        pytest.param([INF], "La nota inf no es un número válido", id="R1-P11"),
        # R1-P12: infinito negativo
        pytest.param([-INF], "La nota -inf no es un número válido", id="R1-P12"),
        # R1-P13: primero se revisa el tipo de todas, antes que el rango
        pytest.param([6, "x"], "La nota 'x' no es un número válido", id="R1-P13"),
        # R1-P14: dos fuera de rango; se reporta la primera
        pytest.param([7, -2], "La nota 7 está fuera de 0 a 5", id="R1-P14"),
        # R1-L1: primer valor inválido bajo 0
        pytest.param([-0.01], "La nota -0.01 está fuera de 0 a 5", id="R1-L1"),
        # R1-L8: primer valor inválido sobre 5
        pytest.param([5.01], "La nota 5.01 está fuera de 0 a 5", id="R1-L8"),
        # R1-L9: un bool junto a un valor válido
        pytest.param([1, True], "La nota True no es un número válido", id="R1-L9"),
        # R1-X1: nan junto a un valor válido
        pytest.param(
            [4, NAN], "La nota nan no es un número válido", id="R1-X1"
        ),
    ],
)
def test_notas_invalidas_lanzan_value_error(notas, mensaje):
    with pytest.raises(ValueError, match=re.escape(mensaje)):
        validar_notas(notas)
