from datetime import date  # Importa date para obtener la fecha actual.


class ModeloBase:
    """Clase base para todos los modelos del sistema."""

    def __init__(self, id_registro):
        """Inicializa un registro con su ID.

        Args:
            id_registro (int): Identificador único del registro.

        Returns:
            None: No devuelve ningún valor.
        """
        self.id = int(id_registro)  # Guarda el ID convertido a entero.

    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un objeto a partir de un diccionario.

        Args:
            datos (dict): Diccionario con los datos del objeto.

        Returns:
            ModeloBase: Objeto creado a partir del diccionario.
        """
        datos = dict(datos)  # Crea una copia del diccionario original.
        id_registro = datos.pop("id")  # Extrae y elimina el ID del diccionario.
        return cls(id_registro, **datos)  # Crea el objeto usando los datos restantes.

    def a_diccionario(self):
        """Convierte el objeto en un diccionario.

        Returns:
            dict: Diccionario que contiene el ID.
        """
        return {"id": self.id}  # Devuelve el ID dentro de un diccionario.

    def etiqueta(self):
        """Obtiene una descripción básica del registro.

        Returns:
            str: Texto descriptivo del registro.
        """
        return f"registro {self.id}"  # Devuelve una etiqueta con el ID.

    def __str__(self):
        """Define cómo se muestra el objeto como texto.

        Returns:
            str: Representación textual del objeto.
        """
        return f"[{self.id}] {self.etiqueta()}"  # Combina ID y etiqueta.


class Persona(ModeloBase):
    """Representa los datos básicos de una persona."""

    def __init__(self, id_registro, nombre, apellido, email):
        """Inicializa una persona.

        Args:
            id_registro (int): Identificador de la persona.
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            email (str): Correo electrónico.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Llama al constructor de ModeloBase.
        self.nombre = nombre  # Guarda el nombre.
        self.apellido = apellido  # Guarda el apellido.
        self.email = email  # Guarda el correo electrónico.

    def nombre_completo(self):
        """Obtiene el nombre completo de la persona.

        Returns:
            str: Nombre y apellido juntos.
        """
        return f"{self.nombre} {self.apellido}"  # Une nombre y apellido.

    def a_diccionario(self):
        """Convierte la persona en un diccionario.

        Returns:
            dict: Datos de la persona.
        """
        datos = super().a_diccionario()  # Obtiene primero el ID de la clase padre.
        datos["nombre"] = self.nombre  # Agrega el nombre.
        datos["apellido"] = self.apellido  # Agrega el apellido.
        datos["email"] = self.email  # Agrega el email.
        return datos  # Devuelve todos los datos.

    def etiqueta(self):
        """Obtiene una etiqueta con el nombre completo.

        Returns:
            str: Nombre completo de la persona.
        """
        return self.nombre_completo()  # Utiliza el método nombre_completo.


class Estudiante(Persona):
    """Representa a un estudiante del sistema académico."""

    def __init__(
        self,
        id_registro,
        nombre,
        apellido,
        email,
        carnet="",
        carrera=""
    ):
        """Inicializa un estudiante.

        Args:
            id_registro (int): Identificador del estudiante.
            nombre (str): Nombre del estudiante.
            apellido (str): Apellido del estudiante.
            email (str): Correo electrónico.
            carnet (str): Carnet del estudiante.
            carrera (str): Carrera que estudia.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro, nombre, apellido, email)  # Inicializa la parte Persona.
        self.carnet = carnet  # Guarda el carnet.
        self.carrera = carrera  # Guarda la carrera.

    def a_diccionario(self):
        """Convierte el estudiante en un diccionario.

        Returns:
            dict: Datos completos del estudiante.
        """
        datos = super().a_diccionario()  # Obtiene los datos heredados.
        datos["carnet"] = self.carnet  # Agrega el carnet.
        datos["carrera"] = self.carrera  # Agrega la carrera.
        return datos  # Devuelve todos los datos.

    def etiqueta(self):
        """Obtiene una descripción del estudiante.

        Returns:
            str: Nombre, carnet y carrera del estudiante.
        """
        return f"{super().etiqueta()} · {self.carnet} · {self.carrera}"  # Construye la etiqueta.


class Materia(ModeloBase):
    """Representa una materia del sistema académico."""

    CUPOS_MAXIMOS = 30  # Define el máximo de cupos permitidos.
    NOTA_APROBACION = 14  # Define la nota mínima para aprobar.

    def __init__(
        self,
        id_registro,
        nombre,
        codigo,
        creditos,
        cupos=30
    ):
        """Inicializa una materia.

        Args:
            id_registro (int): Identificador de la materia.
            nombre (str): Nombre de la materia.
            codigo (str): Código de la materia.
            creditos (int): Número de créditos.
            cupos (int): Cantidad de cupos disponibles.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Inicializa el ID heredado.
        self.nombre = nombre  # Guarda el nombre.
        self.codigo = codigo  # Guarda el código.
        self.creditos = int(creditos)  # Convierte los créditos a entero.
        self.cupos = int(cupos)  # Convierte los cupos a entero.

    @staticmethod
    def es_nota_valida(valor):
        """Comprueba si una nota está entre 0 y 20.

        Args:
            valor (int | float): Nota que se desea validar.

        Returns:
            bool: True si la nota es válida, False si no.
        """
        try:  # Intenta convertir el valor a número.
            return 0 <= float(valor) <= 20  # Comprueba que esté entre 0 y 20.
        except (TypeError, ValueError):  # Captura valores que no pueden convertirse.
            return False  # Indica que la nota no es válida.

    def hay_cupo(self):
        """Comprueba si todavía existe un cupo disponible.

        Returns:
            bool: True si hay cupos, False si no.
        """
        return self.cupos > 0  # Devuelve True cuando hay al menos un cupo.

    def ocupar_cupo(self):
        """Reduce en uno los cupos disponibles.

        Returns:
            bool: True si pudo ocupar un cupo, False si no había cupos.
        """
        if self.hay_cupo():  # Comprueba si existe un cupo.
            self.cupos -= 1  # Reduce un cupo.
            return True  # Indica que la operación fue exitosa.

        return False  # Indica que no había cupos.

    def liberar_cupo(self):
        """Aumenta un cupo disponible sin superar el máximo.

        Returns:
            None: Modifica los cupos de la materia.
        """
        if self.cupos < Materia.CUPOS_MAXIMOS:  # Comprueba que no supere el máximo.
            self.cupos += 1  # Devuelve un cupo.

    def a_diccionario(self):
        """Convierte la materia en un diccionario.

        Returns:
            dict: Datos completos de la materia.
        """
        datos = super().a_diccionario()  # Obtiene el ID.
        datos["nombre"] = self.nombre  # Agrega el nombre.
        datos["codigo"] = self.codigo  # Agrega el código.
        datos["creditos"] = self.creditos  # Agrega los créditos.
        datos["cupos"] = self.cupos  # Agrega los cupos.
        return datos  # Devuelve todos los datos.

    def etiqueta(self):
        """Obtiene una descripción de la materia.

        Returns:
            str: Nombre, código, créditos y cupos.
        """
        return (
            f"{self.nombre} · {self.codigo} · "
            f"{self.creditos} créditos · cupos {self.cupos}"
        )  # Devuelve la información resumida.


class Matricula(ModeloBase):
    """Representa la matrícula de un estudiante en una materia."""

    def __init__(
        self,
        id_registro,
        estudiante_id,
        materia_id,
        periodo,
        nota=0,
        fecha=""
    ):
        """Inicializa una matrícula.

        Args:
            id_registro (int): Identificador de la matrícula.
            estudiante_id (int): ID del estudiante.
            materia_id (int): ID de la materia.
            periodo (str): Periodo académico.
            nota (float): Nota obtenida.
            fecha (str): Fecha de la matrícula.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Inicializa el ID heredado.
        self.estudiante_id = int(estudiante_id)  # Guarda el ID del estudiante.
        self.materia_id = int(materia_id)  # Guarda el ID de la materia.
        self.periodo = periodo  # Guarda el periodo académico.
        self.nota = float(nota)  # Convierte la nota a decimal.
        self.fecha = fecha or date.today().isoformat()  # Usa la fecha dada o la fecha actual.

    def esta_aprobada(self):
        """Comprueba si el estudiante aprobó la materia.

        Returns:
            bool: True si la nota es igual o superior a 14.
        """
        return self.nota >= Materia.NOTA_APROBACION  # Compara la nota con 14.

    def estado(self):
        """Obtiene el estado académico de la matrícula.

        Returns:
            str: Aprobado o Reprobado.
        """
        return "Aprobado" if self.esta_aprobada() else "Reprobado"  # Decide el estado.

    def a_diccionario(self):
        """Convierte la matrícula en un diccionario.

        Returns:
            dict: Datos completos de la matrícula.
        """
        datos = super().a_diccionario()  # Obtiene el ID.
        datos["estudiante_id"] = self.estudiante_id  # Agrega el estudiante.
        datos["materia_id"] = self.materia_id  # Agrega la materia.
        datos["periodo"] = self.periodo  # Agrega el periodo.
        datos["nota"] = self.nota  # Agrega la nota.
        datos["fecha"] = self.fecha  # Agrega la fecha.
        return datos  # Devuelve todos los datos.

    def etiqueta(self):
        """Obtiene una descripción de la matrícula.

        Returns:
            str: Información resumida de la matrícula.
        """
        return (
            f"{self.fecha} · estudiante {self.estudiante_id} · "
            f"materia {self.materia_id} · periodo {self.periodo} · "
            f"nota {self.nota:.2f} · {self.estado()}"
        )  # Devuelve la información de la matrícula.