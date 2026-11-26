"""Pruebas de calcular_aportes (HU-04): lo que aporta cada nota a la nota final."""

import re

import pytest

from calculo import calcular_aportes


@pytest.mark.parametrize(
    "notas, porcentajes, esperado",
    [
        # Ejemplo del contrato: 3.0 x 30 %, 0 x 20 %, 5.0 x 50 %
        pytest.param([3.0, 0, 5.0], [30, 20, 50], [0.9, 0.0, 2.5], id="contrato"),
        # Una sola nota con 100 %: aporta toda la nota
        pytest.param([4.5], [100], [4.5], id="una-nota"),
        # Tuplas: 4 x 25 % = 1.0 y 2 x 75 % = 1.5
        pytest.param((4, 2), (25, 75), [1.0, 1.5], id="tuplas"),
        # Sin redondear: 3.33 x 33 % = 1.0989
        pytest.param([3.33, 3.33, 3.34], [33, 33, 34], [1.0989, 1.0989, 1.1356],
                     id="sin-redondear"),
    ],
)
def test_aportes_valor_esperado(notas, porcentajes, esperado):
    assert calcular_aportes(notas, porcentajes) == pytest.approx(esperado)


@pytest.mark.parametrize(
    "notas, porcentajes, mensaje",
    [
        # Listas vacías
        pytest.param([], [], "Debe haber al menos una nota", id="vacias"),
        # Distinto tamaño
        pytest.param([3], [50, 50], "Debe haber una nota por cada porcentaje",
                     id="tamano"),
        # Nota fuera de rango
        pytest.param([6], [100], "La nota 6 está fuera de 0 a 5", id="nota-rango"),
        # Porcentajes que no suman 100
        pytest.param([3, 4], [50, 40],
                     "Los porcentajes suman 90 %, deben sumar 100 %", id="suma"),
    ],
)
def test_aportes_lanza_los_mismos_errores_que_la_nota_final(
    notas, porcentajes, mensaje
):
    with pytest.raises(ValueError, match=re.escape(mensaje)):
        calcular_aportes(notas, porcentajes)
