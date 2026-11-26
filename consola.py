"""Capa de consola (ADR-001): la única parte del programa que usa input y print.

Pide las notas y los porcentajes, llama a calculo.py y muestra el resultado o el
mensaje de error. Las funciones reciben `entrada` y `salida` para poder probarse
sin teclado ni pantalla.
"""

from calculo import calcular_aportes, calcular_nota_final


def leer_numero(pregunta, entrada=input, salida=print):
    """Pide un número y repite la pregunta hasta que se escriba uno.

    Acepta coma decimal («4,5»), habitual en Colombia.
    """
    while True:
        texto = entrada(pregunta).strip()
        try:
            normalizado = texto.replace(",", ".")
            # Un 6 escrito como entero se queda como 6, no como 6.0 (mensajes fieles)
            if normalizado.lstrip("+-").isdigit():
                return int(normalizado)
            return float(normalizado)
        except ValueError:
            salida(f"«{texto}» no es un número. Escríbelo con dígitos, por ejemplo 4.5")


def leer_entero(pregunta, entrada=input, salida=print):
    """Pide un entero mayor que 0 y repite la pregunta hasta que se escriba uno."""
    while True:
        texto = entrada(pregunta).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        salida(f"«{texto}» no es una cantidad válida. Escribe un entero, por ejemplo 3")


def solicitar_datos(entrada=input, salida=print):
    """Pide los componentes y devuelve (nombres, notas, porcentajes)."""
    cantidad = leer_entero("¿Cuántas evaluaciones tiene la materia? ", entrada, salida)
    nombres, notas, porcentajes = [], [], []
    for numero in range(1, cantidad + 1):
        nombre = entrada(f"Nombre de la evaluación {numero} (Enter para omitir): ")
        nombres.append(nombre.strip() or f"Evaluación {numero}")
        notas.append(leer_numero(f"  Nota de {nombres[-1]} (0 a 5): ", entrada, salida))
        pregunta = f"  Porcentaje de {nombres[-1]} (por ejemplo 30): "
        porcentajes.append(leer_numero(pregunta, entrada, salida))
    return nombres, notas, porcentajes


def mostrar_resultado(nombres, notas, porcentajes, aportes, nota_final, salida=print):
    """Muestra una línea por evaluación con su aporte y la nota final."""
    salida("")
    salida("Evaluación            Nota   Porcentaje   Aporte")
    for nombre, nota, porcentaje, aporte in zip(
        nombres, notas, porcentajes, aportes, strict=True
    ):
        salida(f"{nombre:<20} {nota:>5g} {porcentaje:>10g} % {aporte:>8g}")
    salida(f"Nota final: {nota_final}")


def mostrar_error(mensaje, salida=print):
    """Muestra un error de datos sin dar ninguna nota."""
    salida(f"Error: {mensaje}")


def main(entrada=input, salida=print):
    """Calcula notas finales hasta que la persona responda que no quiere más."""
    salida("Calculadora de nota final ponderada")
    try:
        while True:
            nombres, notas, porcentajes = solicitar_datos(entrada, salida)
            try:
                aportes = calcular_aportes(notas, porcentajes)
                nota_final = calcular_nota_final(notas, porcentajes)
            except ValueError as error:
                mostrar_error(error, salida)
            else:
                mostrar_resultado(
                    nombres, notas, porcentajes, aportes, nota_final, salida
                )
            if entrada("¿Calcular otra nota? (s/n): ").strip().lower() != "s":
                break
    except (EOFError, KeyboardInterrupt):
        salida("")
    salida("Hasta luego")


if __name__ == "__main__":
    main()
