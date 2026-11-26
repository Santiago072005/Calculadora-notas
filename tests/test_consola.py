"""Pruebas de la capa de consola (consola.py) con entradas y salidas simuladas."""

import consola


def guion(*respuestas):
    """Devuelve una función que reemplaza a input() con respuestas fijas."""
    pendientes = iter(respuestas)
    return lambda pregunta="": next(pendientes)


def ejecutar(*respuestas):
    """Corre main() con esas respuestas y devuelve todo lo que imprimió."""
    salida = []
    consola.main(entrada=guion(*respuestas), salida=salida.append)
    return "\n".join(salida)


def test_leer_numero_acepta_coma_decimal():
    # Un estudiante colombiano escribe 4,5 y debe entenderse como 4.5
    assert consola.leer_numero("Nota: ", guion("4,5"), lambda texto: None) == 4.5


def test_leer_numero_repite_la_pregunta_si_no_es_numero():
    salida = []
    valor = consola.leer_numero("Nota: ", guion("abc", "", "3"), salida.append)
    assert valor == 3.0
    assert len(salida) == 2  # un aviso por cada intento inválido
    assert "no es un número" in salida[0]


def test_leer_entero_pide_un_entero_positivo():
    salida = []
    respuestas = guion("0", "x", "2.5", "3")
    cantidad = consola.leer_entero("Cuántas: ", respuestas, salida.append)
    assert cantidad == 3
    assert len(salida) == 3


def test_flujo_completo_muestra_la_nota_final_y_los_aportes():
    texto = ejecutar("3", "Parcial", "3.0", "30", "Taller", "0", "20",
                     "Final", "5.0", "50", "n")
    assert "Nota final: 3.4" in texto  # 0.9 + 0 + 2.5
    assert "Parcial" in texto
    assert "0.9" in texto and "2.5" in texto  # aportes de Parcial y Final


def test_nombre_vacio_usa_un_nombre_por_defecto():
    texto = ejecutar("1", "", "4.0", "100", "n")
    assert "Evaluación 1" in texto
    assert "Nota final: 4.0" in texto


def test_error_de_porcentajes_muestra_el_mensaje_y_no_da_nota():
    texto = ejecutar("3", "A", "3", "30", "B", "4", "20", "C", "5", "40", "n")
    assert "Los porcentajes suman 90 %, deben sumar 100 %" in texto
    assert "Nota final" not in texto


def test_error_de_nota_fuera_de_rango_muestra_el_mensaje():
    texto = ejecutar("1", "A", "5,5", "100", "n")
    assert "La nota 5.5 está fuera de 0 a 5" in texto
    assert "Nota final" not in texto


def test_despues_de_un_error_se_puede_calcular_otra_vez():
    texto = ejecutar("1", "A", "6", "100", "s",  # error y vuelve a empezar
                     "1", "A", "4,5", "100", "n")
    assert "La nota 6 está fuera de 0 a 5" in texto
    assert "Nota final: 4.5" in texto


def test_responder_s_permite_calcular_otra_nota():
    texto = ejecutar("1", "A", "3", "100", "s", "1", "B", "5", "100", "n")
    assert "Nota final: 3.0" in texto
    assert "Nota final: 5.0" in texto


def test_cerrar_la_entrada_termina_sin_error():
    def sin_entrada(pregunta=""):
        raise EOFError

    salida = []
    consola.main(entrada=sin_entrada, salida=salida.append)  # no debe lanzar nada
    assert any("Hasta luego" in linea for linea in salida)
