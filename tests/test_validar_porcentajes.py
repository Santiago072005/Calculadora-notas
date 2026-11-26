"""Pruebas de validar_porcentajes (regla R2), derivadas de la tabla revisada."""

import re

import pytest

from calculo import validar_porcentajes

NAN = float("nan")
INF = float("inf")

NO_VALIDO = "no es un número válido"
MAYOR_0 = "Cada porcentaje debe ser mayor que 0"


@pytest.mark.parametrize(
    "porcentajes",
    [
        pytest.param([100], id="R2-P1"),  # R2-P1: un solo 100
        pytest.param([30, 20, 50], id="R2-P2"),  # R2-P2: tres enteros
        pytest.param([33.3, 33.3, 33.4], id="R2-P3"),  # R2-P3: decimales que suman 100
        pytest.param((60, 40), id="R2-P4"),  # R2-P4: tupla
        pytest.param([0.001, 99.999], id="R2-L2"),  # R2-L2: valores muy pequeños
        pytest.param([50, 50.0000000001], id="R2-L4"),  # R2-L4: dentro de tolerancia
        pytest.param([25, 75], id="R2-L8"),  # R2-L8: suma exacta
    ],
)
def test_porcentajes_validos_devuelven_none(porcentajes):
    assert validar_porcentajes(porcentajes) is None


@pytest.mark.parametrize(
    "porcentajes, mensaje",
    [
        # R2-P5: texto
        pytest.param(["10", 90], f"El porcentaje '10' {NO_VALIDO}", id="R2-P5"),
        # R2-P6: None
        pytest.param([None, 100], f"El porcentaje None {NO_VALIDO}", id="R2-P6"),
        # R2-P7: bool no es número
        pytest.param([True, 99], f"El porcentaje True {NO_VALIDO}", id="R2-P7"),
        # R2-P8a: nan
        pytest.param([NAN, 100], f"El porcentaje nan {NO_VALIDO}", id="R2-P8a"),
        # R2-P8b: infinito
        pytest.param([INF], f"El porcentaje inf {NO_VALIDO}", id="R2-P8b"),
        # R2-P9: cero no es mayor que 0
        pytest.param([0, 100], MAYOR_0, id="R2-P9"),
        # R2-P10: negativo aunque la suma sea 100
        pytest.param([-10, 110], MAYOR_0, id="R2-P10"),
        # R2-P11: suma 90
        pytest.param(
            [50, 40], "Los porcentajes suman 90 %, deben sumar 100 %", id="R2-P11"
        ),
        # R2-P12: suma 100.5
        pytest.param(
            [60, 40.5],
            "Los porcentajes suman 100.5 %, deben sumar 100 %",
            id="R2-P12",
        ),
        # R2-P13: el tipo se revisa antes que <= 0
        pytest.param([0, "a"], f"El porcentaje 'a' {NO_VALIDO}", id="R2-P13"),
        # R2-P14: <= 0 se revisa antes que la suma
        pytest.param([0, 50], MAYOR_0, id="R2-P14"),
        # R2-L3: negativo mínimo, suma 100
        pytest.param([-0.001, 100.001], MAYOR_0, id="R2-L3"),
        # R2-L7: fuera de tolerancia, suma 99.9999999
        pytest.param(
            [50, 49.9999999],
            "Los porcentajes suman 99.9999999 %, deben sumar 100 %",
            id="R2-L7",
        ),
        # R2-L9a: suma 99
        pytest.param(
            [50, 49], "Los porcentajes suman 99 %, deben sumar 100 %", id="R2-L9a"
        ),
        # R2-L9b: suma 101
        pytest.param(
            [50, 51], "Los porcentajes suman 101 %, deben sumar 100 %", id="R2-L9b"
        ),
        # R2-M1 (hallado al romper el código): 3 × 33.3 suma 99.89999999999999 en
        # float; el mensaje debe mostrarla con formato .10g, o sea 99.9
        pytest.param(
            [33.3, 33.3, 33.3],
            "Los porcentajes suman 99.9 %, deben sumar 100 %",
            id="R2-M1",
        ),
        # R2-X1: nan junto a un valor válido
        pytest.param([50, NAN], f"El porcentaje nan {NO_VALIDO}", id="R2-X1"),
    ],
)
def test_porcentajes_invalidos_lanzan_value_error(porcentajes, mensaje):
    with pytest.raises(ValueError, match=re.escape(mensaje)):
        validar_porcentajes(porcentajes)


@pytest.mark.parametrize(
    "porcentajes",
    [
        # R2-L5: apenas sobre la tolerancia de 1e-9 (por arriba)
        pytest.param([50, 50.000000002], id="R2-L5"),
        # R2-L6: apenas sobre la tolerancia de 1e-9 (por abajo)
        pytest.param([50, 49.999999998], id="R2-L6"),
    ],
)
def test_suma_fuera_de_tolerancia_mensaje_con_prefijo(porcentajes):
    # El valor exacto de la suma depende del formato; solo se exige el prefijo.
    with pytest.raises(ValueError, match=re.escape("Los porcentajes suman")):
        validar_porcentajes(porcentajes)
