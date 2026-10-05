
import sys  # Permite trabajar con la configuración de Python
sys.stdout.reconfigure(encoding="utf-8")  # Permite mostrar tildes y emojis

from models import CAMPOS_ESTUDIANTE  # Importa los campos del estudiante
from shared.herramientas import imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar  # Importa funciones de ayuda
from views import crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes, actualizar_estudiante, eliminar_estudiante, agregar_nota, estudiantes_en_comun  # Importa funciones del sistema


def pausa():
    """Pausa el programa hasta que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")  # Espera al usuario


def mostrar_tabla(estudiantes):
    """Muestra una lista de estudiantes en forma de tabla.
    Args:
        estudiantes (list): Lista de estudiantes que se mostrarán.
    """
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<30}{'CARNET':<15}")  # Muestra encabezados
    print("-" * 75)  # Dibuja una línea

    for estudiante in estudiantes:  # Recorre los estudiantes
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}{estudiante.email:<30}{estudiante.carnet:<15}")  # Muestra datos

    print("-" * 75)         # Dibuja otra línea
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")  # Muestra cantidad


# ---------- CREAR ----------
def opcion_crear():
    """Permite crear un nuevo estudiante."""
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")  # Muestra el título
    datos = {}  # Crea un diccionario vacío

    for campo in CAMPOS_ESTUDIANTE:  # Recorre los campos
        datos[campo] = input(f"{campo.capitalize()}: ")  # Pide cada dato

    exito, mensaje = crear_estudiante(datos)  # Envía los datos a views

    if exito:
        imprimir_exito(mensaje)  # Muestra éxito
    else:
        imprimir_error(mensaje)  # Muestra error

    pausa()  # Espera al usuario


# ---------- VER TODOS ----------
def opcion_ver_todos():
    """Muestra todos los estudiantes registrados."""
    imprimir_titulo("LISTA DE ESTUDIANTES")  # Muestra el título
    estudiantes = obtener_todos()  # Obtiene todos los estudiantes

    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")  # Informa si está vacío
    else:
        mostrar_tabla(estudiantes)  # Muestra los estudiantes

    pausa()  # Espera al usuario


# ---------- BUSCAR ----------
def opcion_buscar():
    """Busca un estudiante por nombre, apellido, email o carnet."""
    imprimir_titulo("BUSCAR ESTUDIANTE")  # Muestra el título
    termino = input("Nombre, apellido, email o carnet: ")  # Pide el criterio
    encontrados = buscar_estudiantes(termino)  # Realiza la búsqueda

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")  # Informa si no encuentra
    else:
        mostrar_tabla(encontrados)  # Muestra los resultados

    pausa()  # Espera al usuario


# ---------- VER POR ID ----------
def opcion_ver_por_id():
    """Muestra la información de un estudiante mediante su ID."""
    imprimir_titulo("VER ESTUDIANTE POR ID")  # Muestra el título

    try:
        id_estudiante = int(input("Id del estudiante: "))  # Pide el ID
    except ValueError:
        imprimir_error("El id debe ser un número entero")  # Controla error
        return pausa()

    estudiante = obtener_por_id(id_estudiante)  # Busca el estudiante

    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")  # Informa si no existe
    else:
        for clave, valor in estudiante.a_diccionario().items():  # Recorre los datos
            print(f"  {clave.capitalize():<12}: {valor}")  # Muestra cada dato

        print(f"  {'Promedio':<12}: {estudiante.obtener_promedio()}")  # Muestra promedio

    pausa()  # Espera al usuario


# ---------- ACTUALIZAR ----------
def opcion_actualizar():
    """Permite modificar los datos de un estudiante."""
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")  # Muestra el título

    try:
        id_estudiante = int(input("Id del estudiante: "))  # Pide el ID
    except ValueError:
        imprimir_error("El id debe ser un número entero")  # Controla error
        return pausa()

    estudiante = obtener_por_id(id_estudiante)  # Busca el estudiante

    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")  # Informa si no existe
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")  # Muestra estudiante
    print("Deje en blanco el campo que no quiera cambiar.\n")  # Explica la actualización
    cambios = {}  # Guarda los cambios

    for campo in CAMPOS_ESTUDIANTE:  # Recorre los campos
        actual = getattr(estudiante, campo)  # Obtiene el valor actual
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Pide nuevo valor

        if nuevo:
            cambios[campo] = nuevo  # Guarda el campo cambiado

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)  # Actualiza

    if exito:
        imprimir_exito(mensaje)  # Muestra éxito
    else:
        imprimir_error(mensaje)  # Muestra error

    pausa()  # Espera al usuario


# ---------- ELIMINAR ----------
def opcion_eliminar():
    """Permite eliminar un estudiante después de confirmar."""
    imprimir_titulo("ELIMINAR ESTUDIANTE")  # Muestra el título

    try:
        id_estudiante = int(input("Id del estudiante: "))  # Pide el ID
    except ValueError:
        imprimir_error("El id debe ser un número entero")  # Controla error
        return pausa()

    estudiante = obtener_por_id(id_estudiante)  # Busca el estudiante

    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")  # Informa si no existe
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")  # Muestra el estudiante

    if confirmar("¿Confirma la eliminación?"):  # Pide confirmación
        exito, mensaje = eliminar_estudiante(id_estudiante)  # Elimina estudiante

        if exito:
            imprimir_exito(mensaje)  # Muestra éxito
        else:
            imprimir_error(mensaje)  # Muestra error
    else:
        imprimir_info("Operación cancelada")  # Informa cancelación

    pausa()  # Espera al usuario


# ---------- AGREGAR NOTA ----------
def opcion_agregar_nota():
    """Permite agregar una nota entre 0 y 20 a un estudiante."""
    imprimir_titulo("AGREGAR NOTA")  # Muestra el título

    try:
        id_estudiante = int(input("Id del estudiante: "))  # Pide el ID
    except ValueError:
        imprimir_error("El id debe ser un número entero")  # Controla error
        return pausa()

    estudiante = obtener_por_id(id_estudiante)  # Busca estudiante

    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")  # Informa si no existe
        return pausa()

    materia = input("Materia: ").strip()  # Pide materia
    nota = input("Nota (0-20): ").strip()  # Pide nota
    exito, mensaje = agregar_nota(id_estudiante, materia, nota)  # Agrega la nota

    if exito:
        imprimir_exito(mensaje)  # Muestra éxito
    else:
        imprimir_error(mensaje)  # Muestra error

    pausa()  # Espera al usuario


# ---------- VER PROMEDIO ----------
def opcion_ver_promedio():
    """Muestra el promedio de un estudiante."""
    imprimir_titulo("VER PROMEDIO")  # Muestra el título

    try:
        id_estudiante = int(input("Id del estudiante: "))  # Pide el ID
    except ValueError:
        imprimir_error("El id debe ser un número entero")  # Controla error
        return pausa()

    estudiante = obtener_por_id(id_estudiante)  # Busca estudiante

    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")  # Informa si no existe
        return pausa()

    print(f"\nEstudiante: {estudiante.obtener_nombre_completo()}")  # Muestra nombre
    print(f"Promedio: {estudiante.obtener_promedio()}")  # Muestra promedio

    pausa()  # Espera al usuario


# ---------- MATERIAS EN COMÚN ----------
def opcion_materias_comun():
    """Muestra las materias que comparten dos estudiantes."""
    imprimir_titulo("MATERIAS EN COMÚN")  # Muestra el título

    try:
        id_a = int(input("Id del primer estudiante: "))  # Pide primer ID
        id_b = int(input("Id del segundo estudiante: "))  # Pide segundo ID
    except ValueError:
        imprimir_error("Los ids deben ser números enteros")  # Controla error
        return pausa()

    estudiante_a = obtener_por_id(id_a)  # Busca primer estudiante
    estudiante_b = obtener_por_id(id_b)  # Busca segundo estudiante

    if not estudiante_a:
        imprimir_error(f"No existe un estudiante con id {id_a}")  # Informa si no existe
        return pausa()

    if not estudiante_b:
        imprimir_error(f"No existe un estudiante con id {id_b}")  # Informa si no existe
        return pausa()

    materias = estudiantes_en_comun(id_a, id_b)  # Obtiene materias comunes

    if not materias:
        imprimir_info("Los estudiantes no tienen materias en común.")  # Informa si no hay
    else:
        print("\nMaterias en común:")  # Muestra título

        for materia in sorted(materias):  # Recorre las materias
            print(f"  - {materia}")  # Muestra cada materia

    pausa()  # Espera al usuario


# ---------- SALIR ----------
def salir():
    """Finaliza la ejecución del programa."""
    imprimir_info("¡Hasta luego! 👋")  # Muestra despedida
    return "salir"  # Indica que debe finalizar


# ---------- MENÚ ----------
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),  # Crear estudiante
    "2": ("Ver todos", opcion_ver_todos),  # Ver estudiantes
    "3": ("Buscar", opcion_buscar),  # Buscar estudiante
    "4": ("Ver por id", opcion_ver_por_id),  # Buscar por ID
    "5": ("Actualizar", opcion_actualizar),  # Actualizar
    "6": ("Eliminar", opcion_eliminar),  # Eliminar
    "7": ("Agregar nota", opcion_agregar_nota),  # Agregar nota
    "8": ("Ver promedio", opcion_ver_promedio),  # Ver promedio
    "9": ("Materias en común", opcion_materias_comun),  # Comparar materias
    "0": ("Salir", salir)  # Salir
}


def mostrar_menu():
    """Muestra las opciones disponibles del sistema."""
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")  # Muestra título

    for tecla, (texto, _funcion) in OPCIONES.items():  # Recorre las opciones
        print(f"  {tecla}. {texto}")  # Muestra cada opción

    print()  # Deja un espacio


def main():
    """Ejecuta el menú principal del sistema."""
    while True:  # Mantiene el programa activo
        mostrar_menu()  # Muestra el menú
        tecla = input("Seleccione una opción: ").strip()  # Pide una opción

        if tecla not in OPCIONES:  # Verifica si existe
            imprimir_error("Opción no válida")  # Muestra error
            pausa()  # Espera
            continue  # Regresa al menú

        _texto, funcion = OPCIONES[tecla]  # Obtiene la función seleccionada

        if funcion() == "salir":  # Ejecuta la opción
            break  # Termina el programa


if __name__ == "__main__":
    try:
        main()  # Inicia el programa
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")  # Controla Ctrl+C

