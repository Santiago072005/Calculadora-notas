"""Cálculo de la nota final ponderada (capa de cálculo del ADR-001)."""

import math
from decimal import ROUND_HALF_UP, Decimal

NOTA_MINIMA = 0
NOTA_MAXIMA = 5
TOTAL_PORCENTAJES = 100
TOLERANCIA_SUMA = 1e-9
DECIMALES = 2


def _es_numero_valido(valor: object) -> bool:
    """Indica si un valor es un número que se puede usar como nota o porcentaje.

    Args:
        valor: dato a comprobar, de cualquier tipo.

    Returns:
        True si es int o float, no es bool y es finito (ni nan ni inf);
        False en cualquier otro caso, incluidos los enteros demasiado grandes
        para convertirse a float.
    """
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return False
    try:
        return math.isfinite(valor)
    except OverflowError:  # un entero demasiado grande para convertirse a float
        return False


def validar_notas(notas: list[float]) -> None:
    """Comprueba que todas las notas sean números válidos entre 0 y 5.

    Args:
        notas: notas de cada componente evaluado.

    Returns:
        None. Si todas las notas son válidas no devuelve nada.

    Raises:
        ValueError: si una nota no es un número válido («La nota {nota!r} no es
            un número válido») o está fuera de 0 a 5 («La nota {nota} está fuera
            de 0 a 5»). Primero se revisa el tipo de todas las notas y después
            el rango.
    """
    for nota in notas:
        if not _es_numero_valido(nota):
            raise ValueError(f"La nota {nota!r} no es un número válido")
    for nota in notas:
        if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
            raise ValueError(
                f"La nota {nota} está fuera de {NOTA_MINIMA} a {NOTA_MAXIMA}"
            )


def validar_porcentajes(porcentajes: list[float]) -> None:
    """Comprueba que los porcentajes sean números válidos, positivos y sumen 100.

    Args:
        porcentajes: peso de cada componente, en porcentaje (30 significa 30 %).

    Returns:
        None. Si todos los porcentajes son válidos no devuelve nada.

    Raises:
        ValueError: si un porcentaje no es un número válido, si alguno es menor
            o igual a 0 («Cada porcentaje debe ser mayor que 0») o si la suma
            difiere de 100 en más de 1e-9 («Los porcentajes suman {suma} %,
            deben sumar 100 %»). Se revisan en ese orden.
    """
    for porcentaje in porcentajes:
        if not _es_numero_valido(porcentaje):
            raise ValueError(f"El porcentaje {porcentaje!r} no es un número válido")
    if any(porcentaje <= 0 for porcentaje in porcentajes):
        raise ValueError("Cada porcentaje debe ser mayor que 0")
    suma = sum(porcentajes)
    if not math.isclose(suma, TOTAL_PORCENTAJES, rel_tol=0, abs_tol=TOLERANCIA_SUMA):
        raise ValueError(
            f"Los porcentajes suman {suma:.10g} %, deben sumar {TOTAL_PORCENTAJES} %"
        )


def _validar_entrada(notas: list[float], porcentajes: list[float]) -> None:
    """Aplica, en orden, todas las comprobaciones de notas y porcentajes.

    Raises:
        ValueError: con el mensaje de la primera comprobación que falla (listas
            vacías, distinto tamaño, notas o porcentajes inválidos).
    """
    if not notas:
        raise ValueError("Debe haber al menos una nota")
    if len(notas) != len(porcentajes):
        raise ValueError("Debe haber una nota por cada porcentaje")
    validar_notas(notas)
    validar_porcentajes(porcentajes)


def calcular_aportes(notas: list[float], porcentajes: list[float]) -> list[float]:
    """Calcula cuánto aporta cada nota a la nota final (nota * porcentaje / 100).

    Args:
        notas: notas de cada componente, entre 0 y 5 (listas o tuplas).
        porcentajes: peso de cada componente, en el mismo orden que las notas;
            deben ser mayores que 0 y sumar 100.

    Returns:
        Un aporte por componente, sin redondear. Ejemplo: notas [3.0, 0, 5.0]
        con porcentajes [30, 20, 50] da [0.9, 0.0, 2.5].

    Raises:
        ValueError: las mismas que calcular_nota_final.
    """
    _validar_entrada(notas, porcentajes)
    return [
        float(Decimal(str(nota)) * Decimal(str(porcentaje)) / TOTAL_PORCENTAJES)
        for nota, porcentaje in zip(notas, porcentajes, strict=True)
    ]


def calcular_nota_final(notas: list[float], porcentajes: list[float]) -> float:
    """Calcula la nota final ponderada de una materia.

    Cada nota se multiplica por su porcentaje, se suman los aportes y el
    resultado se redondea a 2 decimales con las mitades hacia arriba.

    Args:
        notas: notas de cada componente, entre 0 y 5 (listas o tuplas).
        porcentajes: peso de cada componente, en el mismo orden que las notas;
            deben ser mayores que 0 y sumar 100.

    Returns:
        La nota final como float con 2 decimales. Ejemplo: notas [3.0, 0, 5.0]
        con porcentajes [30, 20, 50] da 3.4.

    Raises:
        ValueError: si las listas están vacías («Debe haber al menos una nota»),
            si tienen distinto tamaño («Debe haber una nota por cada
            porcentaje») o si alguna validación de validar_notas o de
            validar_porcentajes falla. No devuelve ninguna nota en esos casos.
    """
    _validar_entrada(notas, porcentajes)
    total = sum(
        Decimal(str(nota)) * Decimal(str(porcentaje)) / TOTAL_PORCENTAJES
        for nota, porcentaje in zip(notas, porcentajes, strict=True)
    )
    return float(total.quantize(Decimal(1).scaleb(-DECIMALES), rounding=ROUND_HALF_UP))
