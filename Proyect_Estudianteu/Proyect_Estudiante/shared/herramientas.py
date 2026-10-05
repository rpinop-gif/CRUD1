
"""Funciones reutilizables para la interfaz de consola."""

import os  # Permite trabajar con el sistema operativo

# DICCIONARIO: guarda los colores y sus códigos de consola
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola.

    Returns:
        None: No devuelve ningún valor.
    """
    os.system("clear" if os.name == "posix" else "cls")  # Usa el comando según el sistema


def imprimir_color(texto, color):
    """
    Imprime un texto con el color indicado.

    Args:
        texto (str): Texto que se desea mostrar.
        color (str): Nombre del color definido en COLORES.

    Returns:
        None: No devuelve ningún valor.
    """
    codigo = COLORES.get(color, COLORES["BLANCO"])  # Obtiene el código o usa blanco
    print(f"{codigo}{texto}{COLORES['RESET']}")  # Imprime y restaura el color


def imprimir_titulo(texto):
    """
    Limpia la consola y muestra un título.

    Args:
        texto (str): Texto que se mostrará como encabezado.

    Returns:
        None: No devuelve ningún valor.
    """
    limpiar_pantalla()  # Limpia la pantalla
    imprimir_color("=" * 60, "AZUL")  # Muestra una línea superior
    print(f"  {texto}".center(60))  # Centra el título
    imprimir_color("=" * 60, "AZUL")  # Muestra una línea inferior
    print()  # Deja un espacio


def imprimir_exito(mensaje):
    """
    Muestra un mensaje de éxito.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"✓ {mensaje}", "VERDE")  # Muestra el mensaje en verde


def imprimir_error(mensaje):
    """
    Muestra un mensaje de error.

    Args:
        mensaje (str): Mensaje de error que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"✗ {mensaje}", "ROJO")  # Muestra el mensaje en rojo


def imprimir_info(mensaje):
    """
    Muestra un mensaje informativo.

    Args:
        mensaje (str): Información que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_color(f"ℹ {mensaje}", "CYAN")  # Muestra información en cyan


def confirmar(pregunta):
    """
    Solicita una confirmación al usuario.

    Args:
        pregunta (str): Pregunta que se mostrará al usuario.

    Returns:
        bool: True si la respuesta es afirmativa, False en caso contrario.
    """
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()  # Lee y limpia la respuesta
    return respuesta in RESPUESTAS_SI  # Comprueba si la respuesta es afirmativa


def es_email_valido(texto):
    """
    Comprueba si un texto tiene un formato básico de email válido.

    Args:
        texto (str): Texto que se desea validar.

    Returns:
        bool: True si el email es válido, False si no lo es.
    """
    texto = texto.strip()  # Elimina espacios
    if texto.count("@") != 1:  # Comprueba que exista un solo @
        return False

    usuario, dominio = texto.split("@")  # Separa usuario y dominio
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")  # Valida el formato

