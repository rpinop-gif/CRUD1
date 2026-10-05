import json  # Permite trabajar con datos JSON

# TUPLA: contiene los campos que tiene un estudiante
CAMPOS_ESTUDIANTE = (
    "nombre", "apellido", "email", "carnet", "telefono", "ciudad"
)


class Estudiantes:
    """Representa los datos y operaciones de un estudiante."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 telefono="", ciudad="", notas=None, materias=None):
        """
        Inicializa un estudiante.

        Args:
            id_estudiante (int): Identificador del estudiante.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electrónico.
            carnet (str): Número de carnet.
            telefono (str): Número telefónico.
            ciudad (str): Ciudad del estudiante.
            notas (dict): Diccionario con las notas.
            materias (list/set): Materias del estudiante.
        """
        self.id = id_estudiante                          # Guarda el ID
        self.nombre = nombre                             # Guarda el nombre
        self.apellido = apellido                         # Guarda el apellido
        self.email = email                               # Guarda el email
        self.carnet = carnet                             # Guarda el carnet
        self.telefono = telefono                         # Guarda el teléfono
        self.ciudad = ciudad                             # Guarda la ciudad
        self.notas = notas if notas else {}              # Guarda las notas
        self.materias = set(materias) if materias else set()                   # Guarda materias sin repetir

    def obtener_nombre_completo(self):
        """
        Obtiene el nombre completo del estudiante.

        Returns:
            str: Nombre y apellido juntos.
        """
        return f"{self.nombre} {self.apellido}"            # Une nombre y apellido

    def inscribir_materia(self, materia):
        """
        Inscribe al estudiante en una materia.

        Args:
            materia (str): Nombre de la materia.

        Returns:
            None: No devuelve ningún valor.
        """
        self.materias.add(materia)                      # Agrega la materia al conjunto

    def agregar_nota(self, materia, nota):
        """
        Agrega una nota a una materia.

        Args:
            materia (str): Nombre de la materia.
            nota (float): Nota obtenida.

        Returns:
            None: No devuelve ningún valor.
        """
        self.inscrib

