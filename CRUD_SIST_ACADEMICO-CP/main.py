from shared.herramientas import imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar  # Importa las funciones de la interfaz.
from views import EstudianteController, MateriaController, MatriculaController  # Importa los controladores.

estudiantes = EstudianteController()  # Crea el controlador de estudiantes.
materias = MateriaController()  # Crea el controlador de materias.
matriculas = MatriculaController(estudiantes, materias)  # Crea el controlador de matrículas.

def pausa():
    """Pausa el programa hasta que el usuario presione Enter.
    
    Returns:
        None: No devuelve ningún valor.
    """
    input("\nPresione Enter para continuar...")  # Espera que el usuario presione Enter.

def pedir_entero(etiqueta):
    """Solicita un número entero al usuario.
    
    Args:
        etiqueta (str): Texto que se muestra antes de solicitar el número.
    
    Returns:
        int | None: Número ingresado o None si no es válido.
    """
    try:
        return int(input(etiqueta))  # Solicita y convierte el valor a entero.
    except ValueError:
        return None  # Devuelve None si la conversión falla.

def mostrar_resultado(exito, mensaje):
    """Muestra el resultado de una operación.
    
    Args:
        exito (bool): Indica si la operación fue exitosa.
        mensaje (str): Mensaje que se mostrará.
    
    Returns:
        None: Solo muestra el resultado.
    """
    if exito:
        imprimir_exito(mensaje)  # Muestra mensaje de éxito.
    else:
        imprimir_error(mensaje)  # Muestra mensaje de error.

def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Muestra una lista de objetos.
    
    Args:
        objetos (list): Objetos que se desean mostrar.
        vacio (str): Mensaje cuando no existen objetos.
    
    Returns:
        None: Muestra los objetos.
    """
    if not objetos:
        imprimir_info(vacio)  # Muestra mensaje cuando no hay registros.
        return  # Termina la función.
    for objeto in objetos:
        print(f"  {objeto}")  # Muestra cada objeto.
    imprimir_info(f"Total: {len(objetos)}")  # Muestra la cantidad total.

def mostrar_detalle(objeto):
    """Muestra todos los datos de un objeto.
    
    Args:
        objeto (object): Objeto que se desea mostrar.
    
    Returns:
        None: Muestra los datos.
    """
    for clave, valor in objeto.a_diccionario().items():  # Recorre las claves y valores.
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")  # Muestra cada dato.

def crear_estudiante():
    """Solicita los datos y crea un estudiante.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("CREAR ESTUDIANTE")  # Muestra el título.
    datos = {
        "nombre": input("Nombre: "),  # Solicita el nombre.
        "apellido": input("Apellido: "),  # Solicita el apellido.
        "email": input("Email: "),  # Solicita el email.
        "carnet": input("Carnet: "),  # Solicita el carnet.
        "carrera": input("Carrera: ")  # Solicita la carrera.
    }
    mostrar_resultado(*estudiantes.crear(datos))  # Envía los datos al controlador.
    pausa()  # Espera al usuario.

def listar_estudiantes():
    """Muestra todos los estudiantes.
    
    Returns:
        None: Muestra la lista.
    """
    imprimir_titulo("ESTUDIANTES")  # Muestra el título.
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")  # Muestra los estudiantes.
    pausa()  # Espera al usuario.

def buscar_estudiante():
    """Busca estudiantes por diferentes datos.
    
    Returns:
        None: Muestra los resultados.
    """
    imprimir_titulo("BUSCAR ESTUDIANTE")  # Muestra el título.
    termino = input("Nombre, email, carnet o carrera: ")  # Solicita el texto de búsqueda.
    encontrados = estudiantes.buscar(termino)  # Busca los estudiantes.
    mostrar_lista(encontrados, f"Ningún estudiante coincide con '{termino}'.")  # Muestra los resultados.
    pausa()  # Espera al usuario.

def ver_estudiante():
    """Muestra un estudiante por ID.
    
    Returns:
        None: Muestra el estudiante.
    """
    imprimir_titulo("VER ESTUDIANTE POR ID")  # Muestra el título.
    estudiante = estudiantes.obtener(pedir_entero("Id: "))  # Solicita el ID y busca el estudiante.
    if estudiante is None:
        imprimir_error("No encontrado")  # Muestra error.
    else:
        mostrar_detalle(estudiante)  # Muestra los datos del estudiante.
    pausa()  # Espera al usuario.

def actualizar_estudiante():
    """Actualiza los datos de un estudiante.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")  # Muestra el título.
    id_estudiante = pedir_entero("Id: ")  # Solicita el ID.
    estudiante = estudiantes.obtener(id_estudiante)  # Busca el estudiante.
    if estudiante is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Editando: {estudiante.etiqueta()}")  # Muestra el estudiante.
    print("Deje en blanco lo que no quiera cambiar.\n")  # Explica la actualización.
    cambios = {}  # Crea un diccionario vacío.
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)  # Obtiene el valor actual.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.
        if nuevo:
            cambios[campo] = nuevo  # Guarda el cambio.
    mostrar_resultado(*estudiantes.actualizar(id_estudiante, cambios))  # Actualiza el estudiante.
    pausa()  # Espera al usuario.

def eliminar_estudiante():
    """Elimina un estudiante después de confirmarlo.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ELIMINAR ESTUDIANTE")  # Muestra el título.
    id_estudiante = pedir_entero("Id: ")  # Solicita el ID.
    estudiante = estudiantes.obtener(id_estudiante)  # Busca el estudiante.
    if estudiante is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")  # Muestra qué se eliminará.
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_estudiante))  # Elimina el estudiante.
    else:
        imprimir_info("Operación cancelada")  # Muestra mensaje.
    pausa()  # Espera al usuario.

def crear_materia():
    """Solicita los datos y crea una materia.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("CREAR MATERIA")  # Muestra el título.
    datos = {
        "nombre": input("Nombre: "),  # Solicita el nombre.
        "codigo": input("Código: "),  # Solicita el código.
        "creditos": input("Créditos: "),  # Solicita los créditos.
        "cupos": input("Cupos: ")  # Solicita los cupos.
    }
    mostrar_resultado(*materias.crear(datos))  # Crea la materia.
    pausa()  # Espera al usuario.

def listar_materias():
    """Muestra todas las materias.
    
    Returns:
        None: Muestra las materias.
    """
    imprimir_titulo("MATERIAS")  # Muestra el título.
    mostrar_lista(materias.leer(), "Todavía no hay materias.")  # Muestra las materias.
    pausa()  # Espera al usuario.

def buscar_materia():
    """Busca una materia por nombre o código.
    
    Returns:
        None: Muestra los resultados.
    """
    imprimir_titulo("BUSCAR MATERIA")  # Muestra el título.
    termino = input("Nombre o código: ")  # Solicita el texto.
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")  # Muestra los resultados.
    pausa()  # Espera al usuario.

def ver_materia():
    """Muestra una materia por ID.
    
    Returns:
        None: Muestra la materia.
    """
    imprimir_titulo("VER MATERIA POR ID")  # Muestra el título.
    materia = materias.obtener(pedir_entero("Id: "))  # Busca la materia.
    if materia is None:
        imprimir_error("No encontrado")  # Muestra error.
    else:
        mostrar_detalle(materia)  # Muestra los datos.
    pausa()  # Espera al usuario.

def actualizar_materia():
    """Actualiza una materia.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ACTUALIZAR MATERIA")  # Muestra el título.
    id_materia = pedir_entero("Id: ")  # Solicita el ID.
    materia = materias.obtener(id_materia)  # Busca la materia.
    if materia is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Editando: {materia.etiqueta()}")  # Muestra la materia.
    print("Deje en blanco lo que no quiera cambiar.\n")  # Explica la actualización.
    cambios = {}  # Crea un diccionario vacío.
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)  # Obtiene el valor actual.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.
        if nuevo:
            cambios[campo] = nuevo  # Guarda el cambio.
    mostrar_resultado(*materias.actualizar(id_materia, cambios))  # Actualiza la materia.
    pausa()  # Espera al usuario.

def eliminar_materia():
    """Elimina una materia después de confirmarla.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ELIMINAR MATERIA")  # Muestra el título.
    id_materia = pedir_entero("Id: ")  # Solicita el ID.
    materia = materias.obtener(id_materia)  # Busca la materia.
    if materia is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Se eliminará: {materia.etiqueta()}")  # Muestra la materia.
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_materia))  # Elimina la materia.
    else:
        imprimir_info("Operación cancelada")  # Muestra mensaje.
    pausa()  # Espera al usuario.

def registrar_matricula():
    """Registra una matrícula.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("REGISTRAR MATRÍCULA")  # Muestra el título.
    imprimir_info("Estudiantes:")  # Muestra el encabezado.
    mostrar_lista(estudiantes.leer())  # Muestra los estudiantes.
    imprimir_info("Materias:")  # Muestra el encabezado.
    mostrar_lista(materias.leer())  # Muestra las materias.
    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),  # Solicita el ID del estudiante.
        "materia_id": pedir_entero("Id de la materia: "),  # Solicita el ID de la materia.
        "periodo": input("Periodo: "),  # Solicita el periodo.
        "nota": input("Nota: ")  # Solicita la nota.
    }
    if datos["estudiante_id"] is None or datos["materia_id"] is None:
        imprimir_error("Los IDs deben ser números enteros")  # Muestra error.
        return pausa()  # Regresa al menú.
    mostrar_resultado(*matriculas.crear(datos))  # Crea la matrícula.
    pausa()  # Espera al usuario.

def listar_matriculas():
    """Muestra todas las matrículas.
    
    Returns:
        None: Muestra las matrículas.
    """
    imprimir_titulo("MATRÍCULAS")  # Muestra el título.
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")  # Muestra las matrículas.
    pausa()  # Espera al usuario.

def buscar_matricula():
    """Busca matrículas por periodo.
    
    Returns:
        None: Muestra los resultados.
    """
    imprimir_titulo("BUSCAR MATRÍCULA")  # Muestra el título.
    termino = input("Periodo: ")  # Solicita el periodo.
    mostrar_lista(matriculas.buscar(termino), "Sin coincidencias.")  # Muestra los resultados.
    pausa()  # Espera al usuario.

def ver_matricula():
    """Muestra una matrícula por ID.
    
    Returns:
        None: Muestra la matrícula.
    """
    imprimir_titulo("VER MATRÍCULA POR ID")  # Muestra el título.
    matricula = matriculas.obtener(pedir_entero("Id: "))  # Busca la matrícula.
    if matricula is None:
        imprimir_error("No encontrado")  # Muestra error.
    else:
        mostrar_detalle(matricula)  # Muestra los datos.
    pausa()  # Espera al usuario.

def actualizar_matricula():
    """Actualiza el periodo o la nota de una matrícula.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ACTUALIZAR MATRÍCULA")  # Muestra el título.
    id_matricula = pedir_entero("Id: ")  # Solicita el ID.
    matricula = matriculas.obtener(id_matricula)  # Busca la matrícula.
    if matricula is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Editando: {matricula.etiqueta()}")  # Muestra la matrícula.
    print("Deje en blanco lo que no quiera cambiar.\n")  # Explica la actualización.
    cambios = {}  # Crea un diccionario vacío.
    for campo in ("periodo", "nota"):
        actual = getattr(matricula, campo)  # Obtiene el valor actual.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.
        if nuevo:
            cambios[campo] = nuevo  # Guarda el cambio.
    mostrar_resultado(*matriculas.actualizar(id_matricula, cambios))  # Actualiza la matrícula.
    pausa()  # Espera al usuario.

def eliminar_matricula():
    """Elimina una matrícula y libera un cupo.
    
    Returns:
        None: Muestra el resultado.
    """
    imprimir_titulo("ELIMINAR MATRÍCULA")  # Muestra el título.
    id_matricula = pedir_entero("Id: ")  # Solicita el ID.
    matricula = matriculas.obtener(id_matricula)  # Busca la matrícula.
    if matricula is None:
        imprimir_error("No encontrado")  # Muestra error.
        return pausa()  # Regresa al menú.
    imprimir_info(f"Se eliminará: {matricula.etiqueta()}")  # Muestra la matrícula.
    if confirmar("¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_matricula))  # Elimina la matrícula.
    else:
        imprimir_info("Operación cancelada")  # Muestra mensaje.
    pausa()  # Espera al usuario.

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),  # Opción para crear.
    "2": ("Ver todos", listar_estudiantes),  # Opción para listar.
    "3": ("Buscar", buscar_estudiante),  # Opción para buscar.
    "4": ("Ver por id", ver_estudiante),  # Opción para consultar uno.
    "5": ("Actualizar", actualizar_estudiante),  # Opción para actualizar.
    "6": ("Eliminar", eliminar_estudiante),  # Opción para eliminar.
    "0": ("Volver", None)  # Opción para regresar.
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),  # Opción para crear.
    "2": ("Ver todas", listar_materias),  # Opción para listar.
    "3": ("Buscar", buscar_materia),  # Opción para buscar.
    "4": ("Ver por id", ver_materia),  # Opción para consultar una.
    "5": ("Actualizar", actualizar_materia),  # Opción para actualizar.
    "6": ("Eliminar", eliminar_materia),  # Opción para eliminar.
    "0": ("Volver", None)  # Opción para regresar.
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),  # Opción para registrar.
    "2": ("Ver todas", listar_matriculas),  # Opción para listar.
    "3": ("Buscar", buscar_matricula),  # Opción para buscar.
    "4": ("Ver por id", ver_matricula),  # Opción para consultar una.
    "5": ("Actualizar", actualizar_matricula),  # Opción para actualizar.
    "6": ("Eliminar", eliminar_matricula),  # Opción para eliminar.
    "0": ("Volver", None)  # Opción para regresar.
}

def ejecutar_menu(titulo, opciones):
    """Ejecuta un submenú del sistema.
    
    Args:
        titulo (str): Título que se mostrará.
        opciones (dict): Opciones disponibles en el menú.
    
    Returns:
        None: Ejecuta las opciones seleccionadas.
    """
    while True:
        imprimir_titulo(titulo)  # Muestra el título del menú.
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")  # Muestra cada opción.
        print()  # Deja una línea vacía.
        tecla = input("Opción: ").strip()  # Solicita una opción.
        if tecla not in opciones:
            imprimir_error("Opción no válida")  # Muestra error.
            pausa()  # Espera al usuario.
            continue  # Regresa al inicio.
        _texto, funcion = opciones[tecla]  # Obtiene la función seleccionada.
        if funcion is None:
            break  # Sale del submenú.
        funcion()  # Ejecuta la función.

def resumen():
    """Muestra un resumen general del sistema.
    
    Returns:
        None: Muestra las cantidades principales.
    """
    imprimir_titulo("RESUMEN")  # Muestra el título.
    print(f"  Estudiantes : {len(estudiantes.leer())}")  # Muestra la cantidad de estudiantes.
    print(f"  Carreras    : {', '.join(estudiantes.carreras()) or '-'}")  # Muestra las carreras.
    print(f"  Materias    : {len(materias.leer())}")  # Muestra la cantidad de materias.
    disponibles = materias.materias_con_cupo()  # Obtiene las materias con cupos.
    print(f"  Con cupo    : {len(disponibles)}")  # Muestra la cantidad disponible.
    print(f"  Matrículas  : {len(matriculas.leer())}")  # Muestra la cantidad de matrículas.
    pausa()  # Espera al usuario.

def main():
    """Ejecuta el menú principal del sistema académico.
    
    Returns:
        None: Mantiene el programa ejecutándose.
    """
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")  # Muestra el título principal.
        print("  1. Estudiantes")  # Opción estudiantes.
        print("  2. Materias")  # Opción materias.
        print("  3. Matrículas")  # Opción matrículas.
        print("  4. Resumen")  # Opción resumen.
        print("  0. Salir\n")  # Opción salir.
        tecla = input("Opción: ").strip()  # Solicita una opción.
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)  # Abre el menú de estudiantes.
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)  # Abre el menú de materias.
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)  # Abre el menú de matrículas.
        elif tecla == "4":
            resumen()  # Muestra el resumen.
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")  # Muestra mensaje de salida.
            break  # Termina el programa.
        else:
            imprimir_error("Opción no válida")  # Muestra error.
            pausa()  # Espera al usuario.

if __name__ == "__main__":  # Comprueba si el archivo se ejecuta directamente.
    try:
        main()  # Ejecuta el programa.
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")  # Muestra mensaje al presionar Ctrl+C.