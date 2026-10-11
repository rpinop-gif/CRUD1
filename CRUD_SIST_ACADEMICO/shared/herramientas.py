import os  # Permite utilizar funciones del sistema operativo.


# DICCIONARIO: guarda los colores disponibles para la consola.
COLORES = {
    "ROJO": "\033[91m",  # Código para color rojo.
    "VERDE": "\033[92m",  # Código para color verde.
    "AZUL": "\033[94m",  # Código para color azul.
    "AMARILLO": "\033[93m",  # Código para color amarillo.
    "CYAN": "\033[96m",  # Código para color cyan.
    "BLANCO": "\033[97m",  # Código para color blanco.
    "RESET": "\033[0m",  # Código para regresar al color normal.
}


# TUPLA: contiene respuestas que significan "sí".
RESPUESTAS_SI = (
    "si",
    "sí",
    "s",
    "yes",
    "y"
)


def limpiar_pantalla():
    """Limpia la pantalla de la consola.

    Returns:
        None: No devuelve ningún valor.
    """
    os.system(
        "clear" if os.name == "posix" else "cls"
    )  # Usa clear en Linux/Mac y cls en Windows.


def imprimir_color(texto, color):
    """Imprime un texto utilizando un color.

    Args:
        texto (str): Texto que se desea imprimir.
        color (str): Nombre del color almacenado en COLORES.

    Returns:
        None: Imprime el texto en la consola.
    """
    codigo = COLORES.get(
        color,
        COLORES["BLANCO"]
    )  # Busca el código del color o usa blanco si no existe.

    print(
        f"{codigo}{texto}{COLORES['RESET']}"
    )  # Imprime el texto con el color indicado.


def imprimir_titulo(texto):
    """Limpia la pantalla y muestra un título.

    Args:
        texto (str): Título que se desea mostrar.

    Returns:
        None: Muestra el título en pantalla.
    """
    limpiar_pantalla()  # Limpia la consola.

    imprimir_color(
        "=" * 60,
        "AZUL"
    )  # Imprime una línea decorativa.

    print(
        f"  {texto}".center(60)
    )  # Centra el título.

    imprimir_color(
        "=" * 60,
        "AZUL"
    )  # Imprime otra línea decorativa.

    print()  # Deja una línea vacía.


def imprimir_exito(mensaje):
    """Muestra un mensaje de operación exitosa.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: Muestra el mensaje en verde.
    """
    imprimir_color(
        f"✓ {mensaje}",
        "VERDE"
    )  # Muestra el mensaje utilizando verde.


def imprimir_error(mensaje):
    """Muestra un mensaje de error.

    Args:
        mensaje (str): Mensaje de error.

    Returns:
        None: Muestra el mensaje en rojo.
    """
    imprimir_color(
        f"✗ {mensaje}",
        "ROJO"
    )  # Muestra el mensaje utilizando rojo.


def imprimir_info(mensaje):
    """Muestra un mensaje informativo.

    Args:
        mensaje (str): Información que se desea mostrar.

    Returns:
        None: Muestra el mensaje en cyan.
    """
    imprimir_color(
        f"ℹ {mensaje}",
        "CYAN"
    )  # Muestra el mensaje utilizando cyan.


def confirmar(pregunta):
    """Pregunta al usuario si desea confirmar una acción.

    Args:
        pregunta (str): Pregunta que se mostrará al usuario.

    Returns:
        bool: True si responde afirmativamente, False en otro caso.
    """
    respuesta = input(
        f"{pregunta} (si/no): "
    ).strip().lower()  # Lee y normaliza la respuesta.

    return respuesta in RESPUESTAS_SI  # Comprueba si la respuesta es afirmativa.


def es_email_valido(texto):
    """Realiza una validación básica de un correo electrónico.

    Args:
        texto (str): Correo electrónico que se desea validar.

    Returns:
        bool: True si el correo tiene un formato básico válido.
    """
    texto = texto.strip()  # Elimina espacios al principio y al final.

    if texto.count("@") != 1:  # Comprueba que exista exactamente un @.
        return False  # El correo no es válido.

    usuario, dominio = texto.split("@")  # Divide el correo en usuario y dominio.

    return (
        len(usuario) > 0
        and "." in dominio
        and not dominio.endswith(".")
    )  # Comprueba las condiciones mínimas del correo.