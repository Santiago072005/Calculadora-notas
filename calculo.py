"""Cálculo de la nota final ponderada (capa de cálculo del ADR-001)."""

import math

NOTA_MINIMA = 0
NOTA_MAXIMA = 5
TOTAL_PORCENTAJES = 100
TOLERANCIA_SUMA = 1e-9
DECIMALES = 2


def validar_notas(notas: list[float]) -> None:
    """Lanza ValueError si alguna nota está fuera de 0 a 5."""
    for nota in notas:
        if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
            raise ValueError(
                f"La nota {nota} está fuera de {NOTA_MINIMA} a {NOTA_MAXIMA}"
            )


def validar_porcentajes(porcentajes: list[float]) -> None:
    """Lanza ValueError si un porcentaje es <= 0 o si no suman 100."""
    if any(porcentaje <= 0 for porcentaje in porcentajes):
        raise ValueError("Cada porcentaje debe ser mayor que 0")
    suma = sum(porcentajes)
    if not math.isclose(suma, TOTAL_PORCENTAJES, rel_tol=0, abs_tol=TOLERANCIA_SUMA):
        raise ValueError(
            f"Los porcentajes suman {suma:.10g} %, deben sumar {TOTAL_PORCENTAJES} %"
        )


def calcular_nota_final(notas: list[float], porcentajes: list[float]) -> float:
    """Devuelve la nota final ponderada. Contrato completo en README.md."""
    if not notas:
        raise ValueError("Debe haber al menos una nota")
    if len(notas) != len(porcentajes):
        raise ValueError("Debe haber una nota por cada porcentaje")
    validar_notas(notas)
    validar_porcentajes(porcentajes)
    total = sum(nota * porcentaje / 100 for nota, porcentaje in zip(notas, porcentajes))
    return round(float(total), DECIMALES)
