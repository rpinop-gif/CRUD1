import os  # Permite trabajar con rutas
from models import CAMPOS_ESTUDIANTE, Estudiantes  # Importa el modelo y sus campos
from shared.json_manager import GestorJSON  # Permite leer y guardar JSON
from shared.herramientas import es_email_valido  # Valida emails

# Crea la ruta del archivo JSON
gestor = GestorJSON(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "estudiantes.json"))

CAMPO_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")  # Campos necesarios
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")  # Campos para buscar


def emails_registrados(excepto_id=None):
    """
    Obtiene los emails que ya están registrados.
    
    Args:
        excepto_id (int, optional): ID que se desea excluir.
    Returns:
        set: Conjunto de emails registrados.
    """
    return {e["email"].lower() for e in gestor.leer() if e["id"] != excepto_id}  # Guarda emails sin repetir


def siguiente_id():
    """
    Obtiene el siguiente ID disponible.
    
    Returns:
        int: Siguiente ID.
    """
    ids = [e["id"] for e in gestor.leer()]  # Obtiene los IDs
    return max(ids) + 1 if ids else 1  # Suma 1 al mayor ID


def crear_estudiante(datos):
    """
    Crea y guarda un nuevo estudiante.
    
    Args:
        datos (dict): Datos del estudiante.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}  # Limpia los datos
        faltantes = [campo for campo in CAMPO_OBLIGATORIOS if not valores[campo]]  # Busca campos vacíos

        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):  # Valida el email
            return False, f"El email '{valores['email']}' no es válido."

        if valores["email"].lower() in emails_registrados():  # Evita emails repetidos
            return False, "El email ya está registrado."

        estudantes = Estudiantes(siguiente_id(), **valores)  # Crea el estudiante
        registro = gestor.leer()  # Lee los registros actuales
        registro.append(estudantes.a_diccionario())  # Agrega el estudiante

        if not gestor.guardar(registro):  # Guarda los cambios
            return False, "Error al guardar el estudiante."

        return True, f"Estudiante {estudantes.obtener_nombre_completo()} creado exitosamente."
    except Exception as error:
        return False, f"Error inesperado: {error}"  # Controla errores


def obtener_todos():
    """
    Obtiene todos los estudiantes registrados.
    
    Returns:
        list: Lista de objetos estudiantes.
    """
    return [Estudiantes.desde_diccionario(e) for e in gestor.leer()]  # Convierte los datos a objetos


def obtener_por_id(id_estudiante):
    """
    Busca un estudiante por su ID.
    
    Args:
        id_estudiante (int): ID del estudiante.
    Returns:
        Estudiantes or None: Estudiante encontrado o None.
    """
    for estudiante in obtener_todos():  # Recorre los estudiantes
        if estudiante.id == id_estudiante:  # Compara el ID
            return estudiante  # Devuelve el encontrado
    return None  # No existe


def buscar_estudiantes(criterio):
    """
    Busca estudiantes por diferentes campos.
    
    Args:
        criterio (str): Texto que se desea buscar.
    Returns:
        list: Lista de estudiantes encontrados.
    """
    criterio = criterio.strip().lower()  # Limpia el criterio
    if not criterio:
        return []  # Si está vacío, no busca

    econtrados = []  # Guarda los resultados

    for estudiante in gestor.leer():  # Recorre los registros
        for campo in CAMPOS_BUSCABLES:  # Revisa cada campo
            if criterio in str(estudiante.get(campo, "")).lower():  # Compara el criterio
                econtrados.append(Estudiantes.desde_diccionario(estudiante))  # Agrega el estudiante
                break  # Evita repetirlo

    return econtrados  # Devuelve los resultados


def actualizar_estudiante(id_estudiante, cambios):
    """
    Actualiza los datos de un estudiante.
    
    Args:
        id_estudiante (int): ID del estudiante.
        cambios (dict): Datos que se desean modificar.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    try:
        desconocido = set(cambios) - set(CAMPOS_ESTUDIANTE)  # Busca campos no permitidos

        if desconocido:
            return False, f"Campos no validos: {', '.join(desconocido)}"

        if not cambios:  # Comprueba si hay cambios
            return False, "No se proporcionaron cambios."

        if "email" in cambios:  # Si se cambia el email
            if not es_email_valido(cambios["email"]):  # Valida el nuevo email
                return False, f"El email '{cambios['email']}' no es válido."

            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):  # Evita repetir email
                return False, "El email ya lo tiene otro estudiante."

        registros = gestor.leer()  # Lee todos los registros
        posicion = None  # Guarda la posición del estudiante

        for indice, reg in enumerate(registros):  # Recorre con posición
            if reg["id"] == id_estudiante:  # Busca el ID
                posicion = indice  # Guarda la posición
                break

        if posicion is None:
            return False, f"No se encontró estudiante con ID {id_estudiante}."

        registros[posicion].update({k: str(c).strip() for k, c in cambios.items()})  # Actualiza los datos

        if not gestor.guardar(registros):  # Guarda cambios
            return False, "Error al guardar los cambios."

        return True, f"Estudiante con ID {id_estudiante} actualizado exitosamente."
    except Exception as error:
        return False, f"Error inesperado: {error}"


def eliminar_estudiante(id_estudiante):
    """
    Elimina un estudiante registrado.
    
    Args:
        id_estudiante (int): ID del estudiante.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    registro = gestor.leer()  # Obtiene los registros
    quedan = [r for r in registro if r["id"] != id_estudiante]  # Elimina el ID indicado

    if len(quedan) == len(registro):
        return False, f"No se encontró estudiante con ID {id_estudiante}."

    gestor.guardar(quedan)  # Guarda los registros restantes
    return True, f"Estudiante con ID {id_estudiante} eliminado exitosamente."


def estadisticas():
    """
    Obtiene estadísticas generales de los estudiantes.
    
    Returns:
        dict: Total, ciudades y dominios registrados.
    """
    registor = gestor.leer()  # Obtiene los registros
    ciudades = {r.get("ciudad", "").title() for r in registor if r.get("ciudad")}  # Crea conjunto de ciudades
    dominios = {r.get("email", "").split("@")[1].lower() for r in registor if "@" in r.get("email", "")}  # Obtiene dominios

    return {"total": len(registor), "ciudades": sorted(ciudades), "dominios": sorted(dominios)}  # Devuelve estadísticas


def inscribir_materia(id_estudiante, materia):
    """
    Inscribe un estudiante en una materia.
    
    Args:
        id_estudiante (int): ID del estudiante.
        materia (str): Nombre de la materia.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    materia = materia.strip().title()  # Limpia y formatea la materia

    if not materia:
        return False, "La materia no puede estar vacía."

    registros = gestor.leer()  # Obtiene los registros

    for reg in registros:  # Busca al estudiante
        if reg["id"] == id_estudiante:
            materias = set(reg.get("materias", []))  # Convierte materias en conjunto
            materias.add(materia)  # Agrega la materia
            reg["materias"] = sorted(materias)  # Ordena las materias

            if not gestor.guardar(registros):  # Guarda cambios
                return False, "Error al guardar."

            return True, f"Inscrito en {materia}."

    return False, f"No se encontró estudiante con ID {id_estudiante}."


def estudiantes_en_comun(id_a, id_b):
    """
    Obtiene las materias en común entre dos estudiantes.
    
    Args:
        id_a (int): ID del primer estudiante.
        id_b (int): ID del segundo estudiante.
    Returns:
        set: Materias que tienen en común.
    """
    estudiante_a = obtener_por_id(id_a)  # Busca el primer estudiante
    estudiante_b = obtener_por_id(id_b)  # Busca el segundo estudiante

    if estudiante_a is None or estudiante_b is None:  # Verifica que existan
        return set()  # Devuelve conjunto vacío

    return estudiante_a.materias_en_comun(estudiante_b)  # Obtiene materias compartidas


def agregar_nota(id_estudiante, materia, nota):
    """
    Agrega una nota a una materia.
    
    Args:
        id_estudiante (int): ID del estudiante.
        materia (str): Nombre de la materia.
        nota (float): Nota entre 0 y 20.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    materia = materia.strip().title()  # Limpia la materia

    if not materia:
        return False, "La materia no puede estar vacía."

    try:
        nota = float(nota)  # Convierte la nota a número
    except ValueError:
        return False, "La nota debe ser un número."

    if not 0 <= nota <= 20:  # Comprueba el rango
        return False, "La nota debe estar entre 0 y 20."

    registros = gestor.leer()  # Lee los registros

    for reg in registros:  # Busca al estudiante
        if reg["id"] == id_estudiante:
            reg.setdefault("notas", {}).setdefault(materia, []).append(nota)  # Agrega la nota

            materias = set(reg.get("materias", []))  # Obtiene las materias
            materias.add(materia)  # Agrega la nueva materia
            reg["materias"] = sorted(materias)  # Ordena las materias

            if not gestor.guardar(registros):  # Guarda los cambios
                return False, "Error al guardar."

            return True, f"Nota {nota} agregada en {materia}."

    return False, f"No se encontró estudiante con ID {id_estudiante}."

# PRUEBA DE ACTUALIZACION EN GITHUB