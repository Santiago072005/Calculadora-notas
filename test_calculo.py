"""Pruebas de HU-01: calcular la nota final ponderada.

Se escribieron antes que la implementación (ver historial de git).
"""
import pytest

from calculo import calcular_nota_final


# ---------- Casos normales ----------

def test_tres_componentes_con_un_cero_y_un_cinco():
    # 3.0*0.30 + 0*0.20 + 5.0*0.50 = 3.4
    assert calcular_nota_final([3.0, 0, 5.0], [30, 20, 50]) == pytest.approx(3.4)


def test_tres_componentes_ejemplo_del_curso():
    # 4.0*0.30 + 3.5*0.20 + 5.0*0.50 = 4.4
    assert calcular_nota_final([4.0, 3.5, 5.0], [30, 20, 50]) == pytest.approx(4.4)


def test_resultado_redondeado_a_dos_decimales():
    # 3.7*0.33 + 4.1*0.33 + 2.9*0.34 = 3.56 (valor exacto 3.5599999999999996)
    assert calcular_nota_final([3.7, 4.1, 2.9], [33, 33, 34]) == 3.56


def test_redondeo_de_una_nota_con_tres_decimales():
    # 3.333*0.30 + 3.333*0.30 + 3.333*0.40 = 3.333 -> 3.33
    assert calcular_nota_final([3.333, 3.333, 3.333], [30, 30, 40]) == 3.33


# ---------- Casos límite ----------

def test_un_solo_componente_con_100_por_ciento():
    assert calcular_nota_final([4.2], [100]) == pytest.approx(4.2)


def test_todas_las_notas_en_cero():
    resultado = calcular_nota_final([0, 0, 0], [30, 20, 50])
    assert resultado == 0.0
    assert isinstance(resultado, float)


def test_todas_las_notas_en_cinco():
    resultado = calcular_nota_final([5, 5, 5], [30, 20, 50])
    assert resultado == 5.0
    assert isinstance(resultado, float)


def test_porcentajes_con_decimales_que_suman_100_en_flotante_inexacto():
    # sum([3.1, 32.8, 64.1]) da 99.99999999999999 en Python, pero suman 100
    assert calcular_nota_final([4.0, 3.0, 5.0], [3.1, 32.8, 64.1]) == pytest.approx(4.31)


# ---------- Casos de error ----------

def test_error_si_los_porcentajes_no_suman_100():
    with pytest.raises(ValueError, match="suman 90 %, deben sumar 100 %"):
        calcular_nota_final([3.0, 4.0, 5.0], [30, 20, 40])


@pytest.mark.parametrize("nota, mensaje", [
    (5.5, "La nota 5.5 está fuera de 0 a 5"),
    (-0.1, "La nota -0.1 está fuera de 0 a 5"),
])
def test_error_si_una_nota_esta_fuera_de_0_a_5(nota, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        calcular_nota_final([3.0, nota], [50, 50])


def test_error_si_un_porcentaje_es_cero():
    with pytest.raises(ValueError, match="mayor que 0"):
        calcular_nota_final([3.0, 4.0], [100, 0])


def test_error_si_las_listas_tienen_distinto_tamano():
    with pytest.raises(ValueError, match="una nota por cada porcentaje"):
        calcular_nota_final([3.0, 4.0], [100])


def test_error_si_las_listas_estan_vacias():
    with pytest.raises(ValueError, match="al menos una nota"):
        calcular_nota_final([], [])


# ---------- Casos de error agregados tras revisar los huecos ----------

def test_error_si_un_porcentaje_es_negativo():
    # [120, -20] suman 100: solo la regla «mayor que 0» puede detectarlo
    with pytest.raises(ValueError, match="mayor que 0"):
        calcular_nota_final([3.0, 4.0], [120, -20])


def test_error_si_los_porcentajes_suman_mas_de_100():
    with pytest.raises(ValueError, match="suman 100.5 %, deben sumar 100 %"):
        calcular_nota_final([3.0, 4.0], [50, 50.5])


def test_error_si_la_suma_difiere_de_100_por_mas_que_la_tolerancia():
    # 99.999999 está a 1e-6 de 100, mucho más que la tolerancia de 1e-9
    with pytest.raises(ValueError, match="deben sumar 100 %"):
        calcular_nota_final([3.0, 4.0], [50, 49.999999])


@pytest.mark.parametrize("notas, porcentajes, mensaje", [
    ([], [50], "al menos una nota"),
    ([6.0], [90], "La nota 6.0 está fuera de 0 a 5"),
    ([3.0], [0], "mayor que 0"),
])
def test_orden_de_validacion(notas, porcentajes, mensaje):
    # Cada caso rompe dos reglas a la vez; gana la primera de la tabla del README
    with pytest.raises(ValueError, match=mensaje):
        calcular_nota_final(notas, porcentajes)
