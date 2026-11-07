"""Cálculo de la nota final ponderada (capa de cálculo del ADR-001)."""

import math

_TOLERANCIA = 1e-9


def calcular_nota_final(notas: list[float], porcentajes: list[float]) -> float:
    """Devuelve la nota final ponderada. Contrato completo en README.md."""
    if not notas:
        raise ValueError("Debe haber al menos una nota")
    if len(notas) != len(porcentajes):
        raise ValueError("Debe haber una nota por cada porcentaje")
    for nota in notas:
        if nota < 0 or nota > 5:
            raise ValueError(f"La nota {nota} está fuera de 0 a 5")
    if any(p <= 0 for p in porcentajes):
        raise ValueError("Cada porcentaje debe ser mayor que 0")
    suma = sum(porcentajes)
    if not math.isclose(suma, 100, rel_tol=0, abs_tol=_TOLERANCIA):
        raise ValueError(f"Los porcentajes suman {suma:g} %, deben sumar 100 %")
    total = sum(n * p / 100 for n, p in zip(notas, porcentajes))
    return round(float(total), 2)
