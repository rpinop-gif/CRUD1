
import os
from models import CAMPOS_ESTUDIANTE, Estudiantes
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "estudiantes.json"))

CAMPO_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


def emails_registrados(excepto_id=None):
    """Obtiene los emails registrados.
    Args:
        excepto_id (int, optional): ID que se desea excluir.
    Returns:
        set: Conjunto de emails registrados.
    """
    return {e["email"].lower() for e in gestor.leer() if e["id"] != excepto_id}


def siguiente_id():
    """Obtiene el siguiente ID disponible.
    Returns:
        int: Siguiente ID.
    """
    ids = [e["id"] for e in gestor.leer()]
    return max(ids) + 1 if ids else 1


def crear_estudiante(datos):
    """Crea y guarda un nuevo estudiante.
    Args:
        datos (dict): Datos del estudiante.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}
        faltantes = [campo for campo in CAMPO_OBLIGATORIOS if not valores[campo]]

        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no es válido."
        if valores["email"].lower() in emails_registrados():
            return False, "El email ya está registrado."

        estudantes = Estudiantes(siguiente_id(), **valores)
        registro = gestor.leer()
        registro.append(estudantes.a_diccionario())

        if not gestor.guardar(registro):
            return False, "Error al guardar el estudiante."

        return True, f"Estudiante {estudantes.obtener_nombre_completo()} creado exitosamente."
    except Exception as error:
        return False, f"Error inesperado: {error}"


def obtener_todos():
    """Obtiene todos los estudiantes.
    Returns:
        list: Lista de estudiantes.
    """
    return [Estudiantes.desde_diccionario(e) for e in gestor.leer()]


def obtener_por_id(id_estudiante):
    """Busca un estudiante por su ID.
    Args:
        id_estudiante (int): ID del estudiante.
    Returns:
        Estudiantes or None: Estudiante encontrado o None.
    """
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


def buscar_estudiantes(criterio):
    """Busca estudiantes por diferentes campos.
    Args:
        criterio (str): Texto que se desea buscar.
    Returns:
        list: Estudiantes encontrados.
    """
    criterio = criterio.strip().lower()
    if not criterio:
        return []

    econtrados = []
    for estudiante in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if criterio in str(estudiante.get(campo, "")).lower():
                econtrados.append(Estudiantes.desde_diccionario(estudiante))
                break
    return econtrados


def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza los datos de un estudiante.
    Args:
        id_estudiante (int): ID del estudiante.
        cambios (dict): Campos que se desean modificar.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    try:
        desconocido = set(cambios) - set(CAMPOS_ESTUDIANTE)

        if desconocido:
            return False, f"Campos no validos: {', '.join(desconocido)}"
        if not cambios:
            return False, "No se proporcionaron cambios."

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, f"El email '{cambios['email']}' no es válido."
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "El email ya lo tiene otro estudiante."

        registros = gestor.leer()
        posicion = None

        for indice, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No se encontró estudiante con ID {id_estudiante}."

        registros[posicion].update({k: str(c).strip() for k, c in cambios.items()})

        if not gestor.guardar(registros):
            return False, "Error al guardar los cambios."

        return True, f"Estudiante con ID {id_estudiante} actualizado exitosamente."
    except Exception as error:
        return False, f"Error inesperado: {error}"


def eliminar_estudiante(id_estudiante):
    """Elimina un estudiante.
    Args:
        id_estudiante (int): ID del estudiante.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    registro = gestor.leer()
    quedan = [r for r in registro if r["id"] != id_estudiante]

    if len(quedan) == len(registro):
        return False, f"No se encontró estudiante con ID {id_estudiante}."

    gestor.guardar(quedan)
    return True, f"Estudiante con ID {id_estudiante} eliminado exitosamente."


def estadisticas():
    """Obtiene estadísticas generales de los estudiantes.
    Returns:
        dict: Total, ciudades y dominios registrados.
    """
    registor = gestor.leer()
    ciudades = {r.get("ciudad", "").title() for r in registor if r.get("ciudad")}
    dominios = {r.get("email", "").split("@")[1].lower() for r in registor if "@" in r.get("email", "")}

    return {"total": len(registor), "ciudades": sorted(ciudades), "dominios": sorted(dominios)}


def inscribir_materia(id_estudiante, materia):
    """Inscribe un estudiante en una materia.
    Args:
        id_estudiante (int): ID del estudiante.
        materia (str): Nombre de la materia.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    materia = materia.strip().title()

    if not materia:
        return False, "La materia no puede estar vacía."

    registros = gestor.leer()

    for reg in registros:
        if reg["id"] == id_estudiante:
            materias = set(reg.get("materias", []))
            materias.add(materia)
            reg["materias"] = sorted(materias)

            if not gestor.guardar(registros):
                return False, "Error al guardar."

            return True, f"Inscrito en {materia}."

    return False, f"No se encontró estudiante con ID {id_estudiante}."


def estudiantes_en_comun(id_a, id_b):
    """Obtiene las materias en común entre dos estudiantes.
    Args:
        id_a (int): ID del primer estudiante.
        id_b (int): ID del segundo estudiante.
    Returns:
        set: Materias que tienen en común.
    """
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None or estudiante_b is None:
        return set()

    return estudiante_a.materias_en_comun(estudiante_b)


def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota a una materia.
    Args:
        id_estudiante (int): ID del estudiante.
        materia (str): Nombre de la materia.
        nota (float): Nota entre 0 y 20.
    Returns:
        tuple: Resultado de la operación y mensaje.
    """
    materia = materia.strip().title()

    if not materia:
        return False, "La materia no puede estar vacía."

    try:
        nota = float(nota)
    except ValueError:
        return False, "La nota debe ser un número."

    if not 0 <= nota <= 20:
        return False, "La nota debe estar entre 0 y 20."

    registros = gestor.leer()

    for reg in registros:
        if reg["id"] == id_estudiante:
            reg.setdefault("notas", {}).setdefault(materia, []).append(nota)
            materias = set(reg.get("materias", []))
            materias.add(materia)
            reg["materias"] = sorted(materias)

            if not gestor.guardar(registros):
                return False, "Error al guardar."

            return True, f"Nota {nota} agregada en {materia}."

    return False, f"No se encontró estudiante con ID {id_estudiante}."

