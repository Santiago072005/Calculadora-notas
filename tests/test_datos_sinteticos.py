"""Pruebas con datos sinteticos (ficticios)."""
import pytest

from calculo import calcular_nota_final


def test_curso_sintetico_da_la_nota_esperada(curso):
    notas = [c["nota"] for c in curso["componentes"]]
    porcentajes = [c["porcentaje"] for c in curso["componentes"]]
    resultado = calcular_nota_final(notas, porcentajes)
    assert resultado == pytest.approx(curso["esperado"]), curso["materia"]


def test_texto_tecleado_como_nota_se_rechaza(texto_invalido):
    with pytest.raises(ValueError, match="^La nota"):
        calcular_nota_final([texto_invalido], [100])
