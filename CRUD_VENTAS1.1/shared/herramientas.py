import os  # Importa el módulo os para trabajar con funciones del sistema operativo.


# DICCIONARIO: cada color tiene su etiqueta y su código de consola.
# Permite utilizar colores al mostrar mensajes en la terminal.
COLORES = {
    "ROJO": "\033[91m",       # Código para mostrar texto de color rojo.
    "VERDE": "\033[92m",      # Código para mostrar texto de color verde.
    "AZUL": "\033[94m",       # Código para mostrar texto de color azul.
    "AMARILLO": "\033[93m",   # Código para mostrar texto de color amarillo.
    "CYAN": "\033[96m",       # Código para mostrar texto de color cyan.
    "BLANCO": "\033[97m",     # Código para mostrar texto de color blanco.
    "RESET": "\033[0m",       # Reinicia el color de la terminal.
}


# TUPLA: contiene las respuestas que se consideran afirmativas.
# Es una tupla porque sus valores no necesitan modificarse.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """

    # os.name permite saber qué sistema operativo se está utilizando.
    # "posix" normalmente corresponde a Linux y macOS.
    # "cls" se utiliza para limpiar la consola en Windows.
    # "clear" se utiliza en sistemas tipo Unix.
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    """
    Imprime un texto utilizando un color específico.

    Args:
        texto (str): Texto que se desea mostrar en la consola.
        color (str): Nombre del color que se desea utilizar.

    Returns:
        None: No devuelve ningún valor.
    """

    # Busca el código del color dentro del diccionario COLORES.
    # Si el color no existe, utiliza BLANCO como color predeterminado.
    codigo = COLORES.get(color, COLORES["BLANCO"])

    # Imprime el código de color, el texto y finalmente RESET
    # para que los siguientes textos no mantengan ese color.
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """
    Limpia la pantalla y muestra un título decorado en la consola.

    Args:
        texto (str): Texto que se mostrará como título.

    Returns:
        None: No devuelve ningún valor.
    """

    # Primero limpia la pantalla.
    limpiar_pantalla()

    # Imprime una línea de 60 signos "=" en color azul.
    imprimir_color("=" * 60, "AZUL")

    # Centra el texto dentro de un espacio de 60 caracteres.
    print(f"  {texto}".center(60))

    # Imprime otra línea de 60 signos "=" en color azul.
    imprimir_color("=" * 60, "AZUL")

    # Imprime una línea vacía para separar el título del contenido.
    print()


def imprimir_exito(mensaje):
    """
    Muestra un mensaje indicando que una operación fue exitosa.

    Args:
        mensaje (str): Mensaje que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """

    # Muestra el símbolo de éxito y el mensaje en color verde.
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """
    Muestra un mensaje indicando que ocurrió un error.

    Args:
        mensaje (str): Mensaje que explica el error.

    Returns:
        None: No devuelve ningún valor.
    """

    # Muestra el símbolo de error y el mensaje en color rojo.
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """
    Muestra un mensaje informativo en la consola.

    Args:
        mensaje (str): Información que se desea mostrar.

    Returns:
        None: No devuelve ningún valor.
    """

    # Muestra el símbolo de información y el mensaje en color cyan.
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """
    Pregunta al usuario si desea confirmar una acción.

    Args:
        pregunta (str): Pregunta que se mostrará al usuario.

    Returns:
        bool: True si la respuesta es afirmativa.
        False si la respuesta no está en RESPUESTAS_SI.
    """

    # Solicita una respuesta al usuario.
    # strip() elimina espacios al inicio y al final.
    # lower() convierte la respuesta a minúsculas.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()

    # Comprueba si la respuesta está dentro de la tupla RESPUESTAS_SI.
    # Si está, devuelve True; de lo contrario, devuelve False.
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    """
    Comprueba si un texto tiene un formato básico de correo electrónico válido.

    Args:
        texto (str): Texto que se desea comprobar como correo electrónico.

    Returns:
        bool: True si el correo cumple las condiciones básicas.
        False si el correo no cumple alguna de las condiciones.
    """

    # Elimina espacios que puedan existir al inicio o al final.
    texto = texto.strip()

    # Comprueba que exista exactamente un símbolo @.
    # Si hay cero o más de uno, devuelve False.
    if texto.count("@") != 1:
        return False

    # Divide el correo en dos partes:
    # usuario -> parte antes del @
    # dominio -> parte después del @
    usuario, dominio = texto.split("@")

    # Comprueba tres condiciones:
    # 1. Que el usuario tenga al menos un carácter.
    # 2. Que el dominio tenga un punto.
    # 3. Que el dominio no termine con un punto.
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")