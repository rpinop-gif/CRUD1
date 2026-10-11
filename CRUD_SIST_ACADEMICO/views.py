from abc import ABC, abstractmethod  # Importa herramientas para crear clases abstractas.
from models import Estudiante, Materia, Matricula  # Importa los modelos académicos.
from shared.json_manager import GestorJSON  # Importa el gestor de archivos JSON.
from shared.herramientas import es_email_valido  # Importa la validación del email.

class CrudBase(ABC):
    """Define los métodos básicos que debe tener un controlador CRUD."""

    @abstractmethod
    def leer(self):
        """Obtiene todos los registros.

        Returns:
            list: Lista de registros.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def obtener(self, id_registro):
        """Busca un registro por su ID.

        Args:
            id_registro (int): ID del registro.

        Returns:
            object | None: Registro encontrado o None.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def buscar(self, texto):
        """Busca registros utilizando un texto.

        Args:
            texto (str): Texto que se desea buscar.

        Returns:
            list: Registros encontrados.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def siguiente(self):
        """Obtiene el siguiente ID disponible.

        Returns:
            int: Siguiente ID.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def crear(self, datos):
        """Crea un nuevo registro.

        Args:
            datos (dict): Datos del registro.

        Returns:
            tuple: Resultado y mensaje.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def actualizar(self, id_registro, datos):
        """Actualiza un registro.

        Args:
            id_registro (int): ID del registro.
            datos (dict): Datos que se modificarán.

        Returns:
            tuple: Resultado y mensaje.
        """
        pass  # Las clases hijas deben implementar este método.

    @abstractmethod
    def eliminar(self, id_registro):
        """Elimina un registro.

        Args:
            id_registro (int): ID del registro.

        Returns:
            tuple: Resultado y mensaje.
        """
        pass  # Las clases hijas deben implementar este método.


class EstudianteController(CrudBase):
    """Controla las operaciones CRUD de los estudiantes."""

    def __init__(self, archivo="data/estudiantes.json"):
        """Inicializa el controlador de estudiantes.

        Args:
            archivo (str): Ruta del archivo JSON de estudiantes.

        Returns:
            None: No devuelve ningún valor.
        """
        self.gestor = GestorJSON(archivo)  # Crea el gestor para estudiantes.
        self.lista = []  # Crea la lista de estudiantes.
        for datos in self.gestor.leer():  # Recorre los datos del archivo.
            self.lista.append(Estudiante.desde_diccionario(datos))  # Convierte cada diccionario en un objeto.

    def guardar(self):
        """Guarda todos los estudiantes en el archivo JSON.

        Returns:
            None: Guarda los estudiantes.
        """
        datos = []  # Crea una lista vacía.
        for estudiante in self.lista:  # Recorre los estudiantes.
            datos.append(estudiante.a_diccionario())  # Convierte cada estudiante en diccionario.
        self.gestor.guardar(datos)  # Guarda los datos en JSON.

    def validar(self, datos, id_actual=None):
        """Valida los datos de un estudiante.

        Args:
            datos (dict): Datos que se desean validar.
            id_actual (int | None): ID que se está actualizando.

        Returns:
            str | None: Error encontrado o None si es válido.
        """
        if id_actual is None:  # Comprueba si se está creando.
            for campo in ("nombre", "apellido", "email"):  # Recorre los campos obligatorios.
                if str(datos.get(campo, "")).strip() == "":  # Comprueba si está vacío.
                    return f"El campo {campo} es obligatorio"  # Devuelve el error.

        if "email" in datos:  # Comprueba si existe un email.
            email = str(datos["email"]).strip().lower()  # Limpia el email.
            if not es_email_valido(email):  # Comprueba el formato.
                return f"Email inválido: '{email}'"  # Devuelve el error.
            usados = {estudiante.email.lower() for estudiante in self.lista if estudiante.id != id_actual}  # Obtiene emails usados.
            if email in usados:  # Comprueba si el email ya existe.
                return "Ese email ya está registrado"  # Devuelve el error.

        if "carnet" in datos:  # Comprueba si existe un carnet.
            carnet = str(datos["carnet"]).strip()  # Limpia el carnet.
            if carnet != "":  # Comprueba que no esté vacío.
                usados = {estudiante.carnet for estudiante in self.lista if estudiante.id != id_actual}  # Obtiene carnets usados.
                if carnet in usados:  # Comprueba si el carnet ya existe.
                    return "Ese carnet ya está registrado"  # Devuelve el error.

        return None  # Indica que los datos son válidos.

    def leer(self):
        """Obtiene todos los estudiantes.

        Returns:
            list: Lista de estudiantes.
        """
        return self.lista  # Devuelve la lista.

    def obtener(self, id_estudiante):
        """Busca un estudiante por ID.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            Estudiante | None: Estudiante encontrado o None.
        """
        for estudiante in self.lista:  # Recorre los estudiantes.
            if estudiante.id == id_estudiante:  # Compara los IDs.
                return estudiante  # Devuelve el estudiante.
        return None  # No encontró el estudiante.

    def buscar(self, texto):
        """Busca estudiantes por nombre, apellido, email, carnet o carrera.

        Args:
            texto (str): Texto que se desea buscar.

        Returns:
            list: Lista de estudiantes encontrados.
        """
        texto = texto.strip().lower()  # Limpia el texto.
        encontrados = []  # Crea la lista de resultados.
        if texto == "":  # Comprueba si está vacío.
            return encontrados  # Devuelve lista vacía.
        for estudiante in self.lista:  # Recorre los estudiantes.
            if (texto in estudiante.nombre.lower() or texto in estudiante.apellido.lower() or texto in estudiante.email.lower() or texto in estudiante.carnet.lower() or texto in estudiante.carrera.lower()):  # Busca en los campos.
                encontrados.append(estudiante)  # Agrega el estudiante.
        return encontrados  # Devuelve los resultados.

    def siguiente(self):
        """Obtiene el siguiente ID disponible.

        Returns:
            int: Nuevo ID.
        """
        mayor = 0  # Inicializa el ID mayor.
        for estudiante in self.lista:  # Recorre los estudiantes.
            if estudiante.id > mayor:  # Comprueba si el ID es mayor.
                mayor = estudiante.id  # Guarda el ID mayor.
        return mayor + 1  # Devuelve el siguiente ID.

    def crear(self, datos):
        """Crea un nuevo estudiante.

        Args:
            datos (dict): Datos del estudiante.

        Returns:
            tuple: Resultado y mensaje.
        """
        error = self.validar(datos)  # Valida los datos.
        if error:  # Comprueba si existe un error.
            return False, error  # Devuelve el error.

        estudiante = Estudiante(self.siguiente(), str(datos["nombre"]).strip().title(), str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(), str(datos.get("carnet", "")).strip(), str(datos.get("carrera", "")).strip().title())  # Crea el estudiante.
        self.lista.append(estudiante)  # Agrega el estudiante a la lista.
        self.guardar()  # Guarda los cambios.
        return True, f"Estudiante creado: {estudiante.etiqueta()}"  # Devuelve resultado.

    def actualizar(self, id_estudiante, datos):
        """Actualiza los datos de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.
            datos (dict): Datos que se desean modificar.

        Returns:
            tuple: Resultado y mensaje.
        """
        estudiante = self.obtener(id_estudiante)  # Busca el estudiante.
        if estudiante is None:  # Comprueba si existe.
            return False, f"No existe un estudiante con id {id_estudiante}"  # Devuelve error.
        if not datos:  # Comprueba si hay datos.
            return False, "No se indicó ningún cambio"  # Devuelve error.

        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}  # Define los campos permitidos.
        desconocidos = set(datos) - permitidos  # Encuentra campos inválidos.
        if desconocidos:  # Comprueba si existen campos inválidos.
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Devuelve error.

        error = self.validar(datos, id_estudiante)  # Valida los cambios.
        if error:  # Comprueba si existe error.
            return False, error  # Devuelve el error.

        for campo, valor in datos.items():  # Recorre los cambios.
            valor = str(valor).strip()  # Limpia el valor.
            if campo in ("nombre", "apellido", "carrera"):  # Comprueba campos de texto.
                valor = valor.title()  # Coloca la primera letra en mayúscula.
            elif campo == "email":  # Comprueba si es email.
                valor = valor.lower()  # Convierte el email a minúsculas.
            setattr(estudiante, campo, valor)  # Modifica el atributo.

        self.guardar()  # Guarda los cambios.
        return True, f"Estudiante {id_estudiante} actualizado"  # Devuelve resultado.

    def eliminar(self, id_estudiante):
        """Elimina un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            tuple: Resultado y mensaje.
        """
        estudiante = self.obtener(id_estudiante)  # Busca el estudiante.
        if estudiante is None:  # Comprueba si existe.
            return False, f"No existe un estudiante con id {id_estudiante}"  # Devuelve error.
        self.lista.remove(estudiante)  # Elimina el estudiante.
        self.guardar()  # Guarda los cambios.
        return True, f"Estudiante {id_estudiante} eliminado"  # Devuelve resultado.

    def carreras(self):
        """Obtiene las carreras registradas sin repetir.

        Returns:
            list: Lista ordenada de carreras.
        """
        return sorted({estudiante.carrera for estudiante in self.lista if estudiante.carrera != ""})  # Devuelve las carreras sin repetir.


class MateriaController(CrudBase):
    """Controla las operaciones CRUD de las materias."""

    def __init__(self, archivo="data/materias.json"):
        """Inicializa el controlador de materias.

        Args:
            archivo (str): Ruta del archivo JSON.

        Returns:
            None: No devuelve ningún valor.
        """
        self.gestor = GestorJSON(archivo)  # Crea el gestor JSON.
        self.lista = []  # Crea la lista de materias.
        for datos in self.gestor.leer():  # Lee los datos guardados.
            self.lista.append(Materia.desde_diccionario(datos))  # Convierte cada diccionario en Materia.

    def guardar(self):
        """Guarda las materias en el archivo JSON.

        Returns:
            None: Guarda los datos.
        """
        datos = []  # Crea una lista vacía.
        for materia in self.lista:  # Recorre las materias.
            datos.append(materia.a_diccionario())  # Convierte cada materia en diccionario.
        self.gestor.guardar(datos)  # Guarda los datos.

    def validar(self, datos, id_actual=None):
        """Valida los datos de una materia.

        Args:
            datos (dict): Datos de la materia.
            id_actual (int | None): ID de la materia actual.

        Returns:
            str | None: Error o None si es válida.
        """
        if id_actual is None:  # Comprueba si estamos creando.
            for campo in ("nombre", "codigo", "creditos"):  # Recorre los campos obligatorios.
                if str(datos.get(campo, "")).strip() == "":  # Comprueba si está vacío.
                    return f"El campo {campo} es obligatorio"  # Devuelve error.

        if "creditos" in datos:  # Comprueba los créditos.
            try:
                creditos = int(datos["creditos"])  # Convierte a entero.
                if creditos <= 0:  # Comprueba que sea positivo.
                    return "Los créditos deben ser mayores a 0"  # Devuelve error.
            except (TypeError, ValueError):
                return "Los créditos deben ser un número entero"  # Devuelve error.

        if "cupos" in datos:  # Comprueba los cupos.
            try:
                cupos = int(datos["cupos"])  # Convierte a entero.
                if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:  # Comprueba los límites.
                    return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"  # Devuelve error.
            except (TypeError, ValueError):
                return "Los cupos deben ser un número entero"  # Devuelve error.

        if "codigo" in datos:  # Comprueba el código.
            codigo = str(datos["codigo"]).strip().upper()  # Limpia el código.
            for otra in self.lista:  # Recorre las materias.
                if otra.codigo.upper() == codigo and otra.id != id_actual:  # Comprueba si ya existe.
                    return f"Ya existe una materia con código {codigo}"  # Devuelve error.

        return None  # Indica que es válido.

    def leer(self):
        """Obtiene todas las materias.

        Returns:
            list: Lista de materias.
        """
        return self.lista  # Devuelve las materias.

    def obtener(self, id_materia):
        """Busca una materia por ID.

        Args:
            id_materia (int): ID de la materia.

        Returns:
            Materia | None: Materia encontrada o None.
        """
        for materia in self.lista:  # Recorre las materias.
            if materia.id == id_materia:  # Compara los IDs.
                return materia  # Devuelve la materia.
        return None  # No encontró la materia.

    def buscar(self, texto):
        """Busca materias por nombre o código.

        Args:
            texto (str): Texto que se desea buscar.

        Returns:
            list: Materias encontradas.
        """
        texto = texto.strip().lower()  # Limpia el texto.
        encontrados = []  # Crea lista de resultados.
        if texto == "":  # Comprueba si está vacío.
            return encontrados  # Devuelve lista vacía.
        for materia in self.lista:  # Recorre las materias.
            if texto in materia.nombre.lower() or texto in materia.codigo.lower():  # Busca en nombre o código.
                encontrados.append(materia)  # Agrega la materia.
        return encontrados  # Devuelve resultados.

    def siguiente(self):
        """Obtiene el siguiente ID disponible.

        Returns:
            int: Nuevo ID.
        """
        mayor = 0  # Inicializa el ID mayor.
        for materia in self.lista:  # Recorre las materias.
            if materia.id > mayor:  # Comprueba si es mayor.
                mayor = materia.id  # Guarda el ID mayor.
        return mayor + 1  # Devuelve el siguiente ID.

    def crear(self, datos):
        """Crea una nueva materia.

        Args:
            datos (dict): Datos de la materia.

        Returns:
            tuple: Resultado y mensaje.
        """
        error = self.validar(datos)  # Valida los datos.
        if error:  # Comprueba si hay error.
            return False, error  # Devuelve el error.

        materia = Materia(self.siguiente(), str(datos["nombre"]).strip().title(), str(datos["codigo"]).strip().upper(), int(datos["creditos"]), int(datos.get("cupos", Materia.CUPOS_MAXIMOS)))  # Crea la materia.
        self.lista.append(materia)  # Agrega la materia.
        self.guardar()  # Guarda los cambios.
        return True, f"Materia creada: {materia.etiqueta()}"  # Devuelve resultado.

    def actualizar(self, id_materia, datos):
        """Actualiza una materia.

        Args:
            id_materia (int): ID de la materia.
            datos (dict): Datos que se modificarán.

        Returns:
            tuple: Resultado y mensaje.
        """
        materia = self.obtener(id_materia)  # Busca la materia.
        if materia is None:  # Comprueba si existe.
            return False, f"No existe una materia con id {id_materia}"  # Devuelve error.
        if not datos:  # Comprueba si hay cambios.
            return False, "No se indicó ningún cambio"  # Devuelve error.

        permitidos = {"nombre", "codigo", "creditos", "cupos"}  # Define los campos permitidos.
        desconocidos = set(datos) - permitidos  # Encuentra campos inválidos.
        if desconocidos:  # Comprueba si existen.
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Devuelve error.

        error = self.validar(datos, id_materia)  # Valida los cambios.
        if error:  # Comprueba si hay error.
            return False, error  # Devuelve error.

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()  # Actualiza el nombre.
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()  # Actualiza el código.
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])  # Actualiza créditos.
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])  # Actualiza cupos.

        self.guardar()  # Guarda los cambios.
        return True, f"Materia {id_materia} actualizada"  # Devuelve resultado.

    def eliminar(self, id_materia):
        """Elimina una materia.

        Args:
            id_materia (int): ID de la materia.

        Returns:
            tuple: Resultado y mensaje.
        """
        materia = self.obtener(id_materia)  # Busca la materia.
        if materia is None:  # Comprueba si existe.
            return False, f"No existe una materia con id {id_materia}"  # Devuelve error.
        self.lista.remove(materia)  # Elimina la materia.
        self.guardar()  # Guarda los cambios.
        return True, f"Materia {id_materia} eliminada"  # Devuelve resultado.

    def materias_con_cupo(self):
        """Obtiene las materias que tienen cupos disponibles.

        Returns:
            list: Materias que tienen al menos un cupo.
        """
        disponibles = []  # Crea una lista vacía.
        for materia in self.lista:  # Recorre las materias.
            if materia.hay_cupo():  # Comprueba si hay cupos.
                disponibles.append(materia)  # Agrega la materia.
        return disponibles  # Devuelve las materias disponibles.


class MatriculaController(CrudBase):
    """Controla las operaciones CRUD de las matrículas."""

    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        """Inicializa el controlador de matrículas.

        Args:
            estudiantes (EstudianteController): Controlador de estudiantes.
            materias (MateriaController): Controlador de materias.
            archivo (str): Ruta del archivo JSON.

        Returns:
            None: No devuelve ningún valor.
        """
        self.estudiantes = estudiantes  # Guarda el controlador de estudiantes.
        self.materias = materias  # Guarda el controlador de materias.
        self.gestor = GestorJSON(archivo)  # Crea el gestor JSON.
        self.lista = []  # Crea la lista de matrículas.
        for datos in self.gestor.leer():  # Lee las matrículas.
            self.lista.append(Matricula.desde_diccionario(datos))  # Convierte cada diccionario en matrícula.

    def guardar(self):
        """Guarda las matrículas en el archivo JSON.

        Returns:
            None: Guarda los datos.
        """
        datos = []  # Crea una lista vacía.
        for matricula in self.lista:  # Recorre las matrículas.
            datos.append(matricula.a_diccionario())  # Convierte cada matrícula en diccionario.
        self.gestor.guardar(datos)  # Guarda los datos.

    def validar(self, datos):
        """Valida los datos necesarios para una matrícula.

        Args:
            datos (dict): Datos de la matrícula.

        Returns:
            str | None: Error o None si todo es válido.
        """
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))  # Convierte el ID del estudiante.
            materia_id = int(datos.get("materia_id", 0))  # Convierte el ID de la materia.
        except (TypeError, ValueError):
            return "estudiante_id y materia_id deben ser números enteros"  # Devuelve error.

        periodo = str(datos.get("periodo", "")).strip()  # Obtiene el periodo.
        if periodo == "":
            return "El periodo es obligatorio"  # Devuelve error.

        estudiante = self.estudiantes.obtener(estudiante_id)  # Busca el estudiante.
        if estudiante is None:
            return f"No existe un estudiante con id {estudiante_id}"  # Devuelve error.

        materia = self.materias.obtener(materia_id)  # Busca la materia.
        if materia is None:
            return f"No existe una materia con id {materia_id}"  # Devuelve error.

        if not materia.hay_cupo():  # Comprueba si hay cupos.
            return f"No hay cupos disponibles en {materia.nombre}"  # Devuelve error.

        for matricula in self.lista:  # Recorre las matrículas.
            if matricula.estudiante_id == estudiante_id and matricula.materia_id == materia_id and matricula.periodo == periodo:  # Comprueba si ya existe.
                return "El estudiante ya está matriculado en esa materia en ese periodo"  # Devuelve error.

        if "nota" in datos and not Materia.es_nota_valida(datos["nota"]):  # Valida la nota.
            return "La nota debe ser un número entre 0 y 20"  # Devuelve error.

        return None  # Indica que los datos son válidos.

    def leer(self):
        """Obtiene todas las matrículas.

        Returns:
            list: Lista de matrículas.
        """
        return self.lista  # Devuelve las matrículas.

    def obtener(self, id_matricula):
        """Busca una matrícula por ID.

        Args:
            id_matricula (int): ID de la matrícula.

        Returns:
            Matricula | None: Matrícula encontrada o None.
        """
        for matricula in self.lista:  # Recorre las matrículas.
            if matricula.id == id_matricula:  # Compara los IDs.
                return matricula  # Devuelve la matrícula.
        return None  # No encontró la matrícula.

    def buscar(self, texto):
        """Busca matrículas por periodo.

        Args:
            texto (str): Texto que se desea buscar.

        Returns:
            list: Matrículas encontradas.
        """
        texto = texto.strip().lower()  # Limpia el texto.
        encontradas = []  # Crea lista de resultados.
        if texto == "":
            return encontradas  # Devuelve lista vacía.
        for matricula in self.lista:  # Recorre las matrículas.
            if texto in matricula.periodo.lower():  # Busca el texto en el periodo.
                encontradas.append(matricula)  # Agrega la matrícula.
        return encontradas  # Devuelve resultados.

    def siguiente(self):
        """Obtiene el siguiente ID disponible.

        Returns:
            int: Nuevo ID.
        """
        mayor = 0  # Inicializa el ID mayor.
        for matricula in self.lista:  # Recorre las matrículas.
            if matricula.id > mayor:  # Comprueba si es mayor.
                mayor = matricula.id  # Guarda el ID mayor.
        return mayor + 1  # Devuelve el siguiente ID.

    def crear(self, datos):
        """Crea una nueva matrícula.

        Args:
            datos (dict): Datos de la matrícula.

        Returns:
            tuple: Resultado y mensaje.
        """
        error = self.validar(datos)  # Valida los datos.
        if error:
            return False, error  # Devuelve el error.

        materia = self.materias.obtener(int(datos["materia_id"]))  # Obtiene la materia.
        matricula = Matricula(self.siguiente(), int(datos["estudiante_id"]), int(datos["materia_id"]), str(datos["periodo"]).strip(), float(datos.get("nota", 0)))  # Crea la matrícula.

        if not materia.ocupar_cupo():  # Intenta ocupar un cupo.
            return False, "No hay cupos disponibles"  # Devuelve error.

        self.lista.append(matricula)  # Agrega la matrícula.
        self.materias.guardar()  # Guarda los cupos actualizados.
        self.guardar()  # Guarda la matrícula.
        return True, f"Matrícula {matricula.id} registrada"  # Devuelve resultado.

    def actualizar(self, id_matricula, datos):
        """Actualiza el periodo o la nota de una matrícula.

        Args:
            id_matricula (int): ID de la matrícula.
            datos (dict): Datos que se modificarán.

        Returns:
            tuple: Resultado y mensaje.
        """
        matricula = self.obtener(id_matricula)  # Busca la matrícula.
        if matricula is None:
            return False, f"No existe una matrícula con id {id_matricula}"  # Devuelve error.
        if not datos:
            return False, "No se indicó ningún cambio"  # Devuelve error.

        permitidos = {"periodo", "nota"}  # Define los campos permitidos.
        desconocidos = set(datos) - permitidos  # Encuentra campos inválidos.
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Devuelve error.

        if "periodo" in datos:
            periodo = str(datos["periodo"]).strip()  # Limpia el periodo.
            if periodo == "":
                return False, "El periodo no puede estar vacío"  # Devuelve error.
            matricula.periodo = periodo  # Actualiza el periodo.

        if "nota" in datos:
            if not Materia.es_nota_valida(datos["nota"]):  # Valida la nota.
                return False, "La nota debe ser un número entre 0 y 20"  # Devuelve error.
            matricula.nota = float(datos["nota"])  # Actualiza la nota.

        self.guardar()  # Guarda los cambios.
        return True, f"Matrícula {id_matricula} actualizada"  # Devuelve resultado.

    def eliminar(self, id_matricula):
        """Elimina una matrícula y libera un cupo.

        Args:
            id_matricula (int): ID de la matrícula.

        Returns:
            tuple: Resultado y mensaje.
        """
        matricula = self.obtener(id_matricula)  # Busca la matrícula.
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"  # Devuelve error.

        materia = self.materias.obtener(matricula.materia_id)  # Obtiene la materia.
        if materia is not None:
            materia.liberar_cupo()  # Libera un cupo.
            self.materias.guardar()  # Guarda los cupos.

        self.lista.remove(matricula)  # Elimina la matrícula.
        self.guardar()  # Guarda los cambios.
        return True, f"Matrícula {id_matricula} eliminada y cupo liberado"  # Devuelve resultado.

    def matriculas_por_estudiante(self, id_estudiante):
        """Obtiene las matrículas de un estudiante.

        Args:
            id_estudiante (int): ID del estudiante.

        Returns:
            list: Matrículas del estudiante.
        """
        return [matricula for matricula in self.lista if matricula.estudiante_id == id_estudiante]  # Devuelve sus matrículas.

    def estudiantes_en_comun(self, id_a, id_b):
        """Obtiene las materias compartidas por dos estudiantes.

        Args:
            id_a (int): ID del primer estudiante.
            id_b (int): ID del segundo estudiante.

        Returns:
            set: IDs de las materias compartidas.
        """
        materias_a = {matricula.materia_id for matricula in self.lista if matricula.estudiante_id == id_a}  # Obtiene materias del primer estudiante.
        materias_b = {matricula.materia_id for matricula in self.lista if matricula.estudiante_id == id_b}  # Obtiene materias del segundo estudiante.
        return materias_a & materias_b  # Devuelve la intersección de ambos conjuntos.