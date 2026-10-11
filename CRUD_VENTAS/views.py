from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para definir clases y métodos abstractos.

from models import Cliente, Producto, Venta  # Importa los modelos que representan clientes, productos y ventas.

from shared.json_manager import GestorJSON  # Importa la herramienta que lee y guarda datos en archivos JSON.

from shared.herramientas import es_email_valido  # Importa la función que comprueba si un correo es válido.

# =====================================================================

# CLASE BASE (ABSTRACTA)

# =====================================================================

# Solo dice QUÉ métodos debe tener todo controlador.

# CÓMO se hace cada uno lo escribe cada controlador, de la forma más simple.

class CrudBase(ABC):  # Define una clase para organizar las operaciones del controlador.
    """Clase abstracta que define los métodos básicos que deben implementar los controladores."""

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def leer(self):  # Define un método del controlador.
        """Devuelve la lista completa de registros cargados.

        Returns:
            list: lista de objetos registrados."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def obtener(self, id_registro):  # Define un método del controlador.
        """Busca un registro por su identificador y lo devuelve; si no existe, devuelve None.

        Args:
            id_registro: Identificador del registro que se consulta o modifica.

        Returns:
            object | None: registro encontrado o None si no existe."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def buscar(self, texto):  # Define un método del controlador.
        """Busca registros que coincidan con el texto indicado y devuelve una lista de resultados.

        Args:
            texto: Texto que se utilizará para buscar coincidencias.

        Returns:
            list: registros que coinciden con el texto de búsqueda."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def siguiente(self):  # Define un método del controlador.
        """Calcula y devuelve el siguiente identificador disponible.

        Returns:
            int: siguiente identificador disponible."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def crear(self, datos):  # Define un método del controlador.
        """Valida los datos, crea un registro nuevo, lo guarda y devuelve el resultado de la operación.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la operación y mensaje informativo o de error."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def actualizar(self, id_registro, datos):  # Define un método del controlador.
        """Valida y aplica los cambios indicados a un registro existente y guarda los cambios.

        Args:
            id_registro: Identificador del registro que se consulta o modifica.
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la actualización y mensaje correspondiente."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

    @abstractmethod  # Indica que este método debe implementarse en las clases hijas.

    def eliminar(self, id_registro):  # Define un método del controlador.
        """Elimina un registro existente y guarda la lista actualizada.

        Args:
            id_registro: Identificador del registro que se consulta o modifica.

        Returns:
            tuple[bool, str]: resultado de la eliminación/anulación y mensaje correspondiente."""

        pass  # No ejecuta ninguna acción; deja la implementación para la clase hija.

# =====================================================================

# CONTROLADOR DE CLIENTES

# =====================================================================

class ClienteController(CrudBase):  # Define una clase para organizar las operaciones del controlador.
    """Controlador que administra el registro, consulta, actualización y eliminación de clientes."""

    def __init__(self, archivo="data/clientes.json"):  # Inicializa el objeto con los datos y recursos necesarios.
        """Inicializa el controlador y carga los registros guardados en el archivo JSON.

        Args:
            archivo: Ruta del archivo JSON utilizado para guardar los registros.

        Returns:
            No devuelve ningún valor; inicializa el objeto."""

        self.gestor = GestorJSON(archivo)  # Crea el gestor encargado de acceder al archivo JSON.

        # Leemos el JSON y convertimos cada diccionario en un objeto Cliente

        self.lista = []  # Crea una lista vacía para almacenar los objetos.

        for datos in self.gestor.leer():  # Recorre los registros leídos del archivo JSON.

            self.lista.append(Cliente.desde_diccionario(datos))  # Convierte el diccionario en un objeto y lo agrega a la lista.

    def guardar(self):  # Define un método del controlador.
        """Guarda en el archivo JSON los registros actuales de la lista.

        Returns:
            No devuelve ningún valor; guarda los datos en el archivo JSON."""

        datos = []  # Crea una lista donde se prepararán los datos para guardarlos.

        for cliente in self.lista:  # Recorre los clientes almacenados.

            datos.append(cliente.a_diccionario())  # Convierte el objeto a diccionario y lo agrega a los datos que se guardarán.

        self.gestor.guardar(datos)  # Guarda los datos en el archivo JSON.

    def validar(self, datos, id_actual=None):  # Define un método del controlador.
        """Valida los datos recibidos antes de crear o actualizar un registro.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.
            id_actual: Identificador del registro actual, excluido al comprobar duplicados.

        Returns:
            str: mensaje de error si los datos no son válidos; None si son válidos."""

        """Devuelve un mensaje de error, o None si todo está bien."""

        # Al crear hay que traer los tres obligatorios; al actualizar, solo lo que cambia

        if id_actual is None:  # Comprueba si se está creando un registro nuevo.

            for campo in ("nombre", "apellido", "email"):  # Recorre los campos que deben validarse.

                if str(datos.get(campo, "")).strip() == "":  # Comprueba si el campo obligatorio está vacío.

                    return f"El campo {campo} es obligatorio"  # Devuelve el mensaje correspondiente al resultado de la operación.

        if "email" in datos:  # Valida el correo solo si fue incluido entre los datos recibidos.

            email = str(datos["email"]).strip().lower()  # Limpia el correo y lo convierte a minúsculas.

            if not es_email_valido(email):  # Comprueba que el formato del correo sea válido.

                return f"Email inválido: '{email}'"  # Devuelve el mensaje correspondiente al resultado de la operación.

            # CONJUNTO con los emails de los OTROS clientes

            usados = {c.email for c in self.lista if c.id != id_actual}  # Crea un conjunto con los correos de los demás clientes.

            if email in usados:  # Comprueba si el correo ya está registrado.

                return "Ese email ya está registrado"  # Devuelve el resultado de la función.

        telefono = str(datos.get("telefono", "")).strip()  # Obtiene el teléfono y elimina espacios sobrantes.

        if telefono != "" and not telefono.isdigit():  # Comprueba que el teléfono contenga solamente dígitos.

            return "El teléfono solo puede tener números"  # Devuelve el resultado de la función.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def leer(self):  # Define un método del controlador.
        """Devuelve la lista completa de registros cargados.

        Returns:
            list: lista de objetos registrados."""

        return self.lista  # Devuelve la lista completa de registros.

    def obtener(self, id_cliente):  # Define un método del controlador.
        """Busca un registro por su identificador y lo devuelve; si no existe, devuelve None.

        Args:
            id_cliente: Identificador del cliente que se consulta o modifica.

        Returns:
            object | None: registro encontrado o None si no existe."""

        for cliente in self.lista:  # Recorre los clientes almacenados.

            if cliente.id == id_cliente:  # Comprueba si el identificador coincide con el solicitado.

                return cliente  # Devuelve el registro encontrado.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def buscar(self, texto):  # Define un método del controlador.
        """Busca registros que coincidan con el texto indicado y devuelve una lista de resultados.

        Args:
            texto: Texto que se utilizará para buscar coincidencias.

        Returns:
            list: registros que coinciden con el texto de búsqueda."""

        texto = texto.strip().lower()  # Inicializa el texto del comprobante con la información indicada.

        encontrados = []  # Crea una lista vacía para los resultados de la búsqueda.

        if texto == "":  # Comprueba si el usuario dejó vacía la búsqueda.

            return encontrados  # Devuelve la lista de resultados encontrados.

        for cliente in self.lista:  # Recorre los clientes almacenados.

            if (texto in cliente.nombre.lower()  # Comprueba si el texto aparece en alguno de los campos buscables.

                    or texto in cliente.apellido.lower()  # Realiza la operación indicada en esta línea.

                    or texto in cliente.email  # Realiza la operación indicada en esta línea.

                    or texto in cliente.telefono  # Realiza la operación indicada en esta línea.

                    or texto in cliente.ciudad.lower()):  # Realiza la operación indicada en esta línea.

                encontrados.append(cliente)  # Agrega el registro que coincide con la búsqueda.

        return encontrados  # Devuelve la lista de resultados encontrados.

    def siguiente(self):  # Define un método del controlador.
        """Calcula y devuelve el siguiente identificador disponible.

        Returns:
            int: siguiente identificador disponible."""

        mayor = 0  # Inicializa el mayor identificador encontrado.

        for cliente in self.lista:  # Recorre los clientes almacenados.

            if cliente.id > mayor:  # Comprueba si este ID supera al mayor encontrado.

                mayor = cliente.id  # Actualiza el mayor identificador encontrado.

        return mayor + 1  # Devuelve un identificador mayor que el máximo actual.

    def crear(self, datos):  # Define un método del controlador.
        """Valida los datos, crea un registro nuevo, lo guarda y devuelve el resultado de la operación.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la operación y mensaje informativo o de error."""

        error = self.validar(datos)  # Ejecuta las validaciones antes de modificar o crear el registro.

        if error:  # Comprueba si la validación encontró un error.

            return False, error  # Devuelve False y el mensaje que explica por qué falló la operación.

        cliente = Cliente(self.siguiente(),  # Realiza la operación indicada en esta línea.

                          str(datos["nombre"]).strip().title(),  # Realiza la operación indicada en esta línea.

                          str(datos["apellido"]).strip().title(),  # Realiza la operación indicada en esta línea.

                          str(datos["email"]).strip().lower(),  # Realiza la operación indicada en esta línea.

                          str(datos.get("telefono", "")).strip(),  # Realiza la operación indicada en esta línea.

                          str(datos.get("ciudad", "")).strip().title())  # Realiza la operación indicada en esta línea.

        self.lista.append(cliente)  # Agrega el nuevo objeto a la lista.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Cliente creado: {cliente.etiqueta()}"  # Devuelve True y un mensaje de confirmación.

    def actualizar(self, id_cliente, datos):  # Define un método del controlador.
        """Valida y aplica los cambios indicados a un registro existente y guarda los cambios.

        Args:
            id_cliente: Identificador del cliente que se consulta o modifica.
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la actualización y mensaje correspondiente."""

        cliente = self.obtener(id_cliente)  # Realiza la operación indicada en esta línea.

        if cliente is None:  # Comprueba si se cumple la condición indicada.

            return False, f"No existe un cliente con id {id_cliente}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        if not datos:  # Comprueba si no se enviaron cambios.

            return False, "No se indicó ningún cambio"  # Devuelve False y el mensaje que explica por qué falló la operación.

        # DIFERENCIA de conjuntos: campos que no existen en un cliente

        permitidos = {"nombre", "apellido", "email", "telefono", "ciudad"}  # Define los campos que se permite modificar.

        desconocidos = set(datos) - permitidos  # Obtiene los campos recibidos que no están permitidos.

        if desconocidos:  # Comprueba si se recibieron campos desconocidos.

            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        # Se valida ANTES de tocar el objeto: si algo falla, no cambia nada

        error = self.validar(datos, id_cliente)  # Ejecuta las validaciones antes de modificar o crear el registro.

        if error:  # Comprueba si la validación encontró un error.

            return False, error  # Devuelve False y el mensaje que explica por qué falló la operación.

        for campo, valor in datos.items():  # Recorre cada campo y su nuevo valor.

            valor = str(valor).strip()  # Convierte el valor a texto y elimina espacios sobrantes.

            if campo in ("nombre", "apellido", "ciudad"):  # Comprueba si el campo necesita un formato específico.

                valor = valor.title()  # Pone en mayúscula la primera letra de cada palabra.

            elif campo == "email":  # Comprueba si el campo actual es el correo.

                valor = valor.lower()  # Convierte el texto a minúsculas.

            setattr(cliente, campo, valor)  # Actualiza en el objeto el atributo indicado.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Cliente {id_cliente} actualizado"  # Devuelve True y un mensaje de confirmación.

    def eliminar(self, id_cliente):  # Define un método del controlador.
        """Elimina un registro existente y guarda la lista actualizada.

        Args:
            id_cliente: Identificador del cliente que se consulta o modifica.

        Returns:
            tuple[bool, str]: resultado de la eliminación/anulación y mensaje correspondiente."""

        cliente = self.obtener(id_cliente)  # Realiza la operación indicada en esta línea.

        if cliente is None:  # Comprueba si se cumple la condición indicada.

            return False, f"No existe un cliente con id {id_cliente}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        self.lista.remove(cliente)  # Elimina de la lista el objeto indicado.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Cliente {id_cliente} eliminado"  # Devuelve True y un mensaje de confirmación.

    # --- propio de clientes ---

    def ciudades(self):  # Define un método del controlador.
        """Devuelve una lista ordenada de las ciudades no vacías, sin repetir valores.

        Returns:
            list[str]: ciudades registradas sin duplicados."""

        """CONJUNTO de ciudades: sin repetidos. sorted() lo devuelve como lista."""

        return sorted({c.ciudad for c in self.lista if c.ciudad != ""})  # Devuelve las ciudades sin repetir y ordenadas alfabéticamente.

# =====================================================================

# CONTROLADOR DE PRODUCTOS

# =====================================================================

class ProductoController(CrudBase):  # Define una clase para organizar las operaciones del controlador.
    """Controlador que administra productos y sus existencias en el inventario."""

    def __init__(self, archivo="data/productos.json"):  # Inicializa el objeto con los datos y recursos necesarios.
        """Inicializa el controlador y carga los registros guardados en el archivo JSON.

        Args:
            archivo: Ruta del archivo JSON utilizado para guardar los registros.

        Returns:
            No devuelve ningún valor; inicializa el objeto."""

        self.gestor = GestorJSON(archivo)  # Crea el gestor encargado de acceder al archivo JSON.

        self.lista = []  # Crea una lista vacía para almacenar los objetos.

        for datos in self.gestor.leer():  # Recorre los registros leídos del archivo JSON.

            self.lista.append(Producto.desde_diccionario(datos))  # Convierte el diccionario en un objeto y lo agrega a la lista.

    def guardar(self):  # Define un método del controlador.
        """Guarda en el archivo JSON los registros actuales de la lista.

        Returns:
            No devuelve ningún valor; guarda los datos en el archivo JSON."""

        datos = []  # Crea una lista donde se prepararán los datos para guardarlos.

        for producto in self.lista:  # Recorre los productos almacenados.

            datos.append(producto.a_diccionario())  # Convierte el objeto a diccionario y lo agrega a los datos que se guardarán.

        self.gestor.guardar(datos)  # Guarda los datos en el archivo JSON.

    def validar(self, datos, id_actual=None):  # Define un método del controlador.
        """Valida los datos recibidos antes de crear o actualizar un registro.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.
            id_actual: Identificador del registro actual, excluido al comprobar duplicados.

        Returns:
            str: mensaje de error si los datos no son válidos; None si son válidos."""

        if id_actual is None:  # Comprueba si se está creando un registro nuevo.

            for campo in ("nombre", "precio"):  # Recorre los campos que deben validarse.

                if str(datos.get(campo, "")).strip() == "":  # Comprueba si el campo obligatorio está vacío.

                    return f"El campo {campo} es obligatorio"  # Devuelve el mensaje correspondiente al resultado de la operación.

        # es_precio_valido es el método ESTÁTICO de Producto

        if "precio" in datos and not Producto.es_precio_valido(datos["precio"]):  # Valida el precio si fue incluido en los datos recibidos.

            return f"Precio inválido: '{datos['precio']}' (debe ser un número mayor a 0)"  # Devuelve el mensaje correspondiente al resultado de la operación.

        stock = str(datos.get("stock", "")).strip()  # Obtiene el stock recibido y elimina espacios sobrantes.

        if stock != "" and not stock.isdigit():  # Comprueba que el stock indicado tenga un formato válido.

            return "El stock debe ser un número entero positivo"  # Devuelve el resultado de la función.

        if "nombre" in datos:  # Procesa el nombre solo si se incluyó en los datos recibidos.

            nombre = str(datos["nombre"]).strip().title()  # Limpia el nombre y aplica formato de título.

            for otro in self.lista:  # Recorre los productos existentes para detectar duplicados.

                if otro.nombre == nombre and otro.id != id_actual:  # Comprueba si otro producto ya tiene ese nombre.

                    return f"Ya existe un producto llamado {nombre}"  # Devuelve el mensaje correspondiente al resultado de la operación.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def leer(self):  # Define un método del controlador.
        """Devuelve la lista completa de registros cargados.

        Returns:
            list: lista de objetos registrados."""

        return self.lista  # Devuelve la lista completa de registros.

    def obtener(self, id_producto):  # Define un método del controlador.
        """Busca un registro por su identificador y lo devuelve; si no existe, devuelve None.

        Args:
            id_producto: Identificador del producto que se consulta o modifica.

        Returns:
            object | None: registro encontrado o None si no existe."""

        for producto in self.lista:  # Recorre los productos almacenados.

            if producto.id == id_producto:  # Comprueba si el identificador coincide con el solicitado.

                return producto  # Devuelve el registro encontrado.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def buscar(self, texto):  # Define un método del controlador.
        """Busca registros que coincidan con el texto indicado y devuelve una lista de resultados.

        Args:
            texto: Texto que se utilizará para buscar coincidencias.

        Returns:
            list: registros que coinciden con el texto de búsqueda."""

        texto = texto.strip().lower()  # Inicializa el texto del comprobante con la información indicada.

        encontrados = []  # Crea una lista vacía para los resultados de la búsqueda.

        if texto == "":  # Comprueba si el usuario dejó vacía la búsqueda.

            return encontrados  # Devuelve la lista de resultados encontrados.

        for producto in self.lista:  # Recorre los productos almacenados.

            if texto in producto.nombre.lower():  # Comprueba si el texto aparece en alguno de los campos buscables.

                encontrados.append(producto)  # Agrega el registro que coincide con la búsqueda.

        return encontrados  # Devuelve la lista de resultados encontrados.

    def siguiente(self):  # Define un método del controlador.
        """Calcula y devuelve el siguiente identificador disponible.

        Returns:
            int: siguiente identificador disponible."""

        mayor = 0  # Inicializa el mayor identificador encontrado.

        for producto in self.lista:  # Recorre los productos almacenados.

            if producto.id > mayor:  # Comprueba si este ID supera al mayor encontrado.

                mayor = producto.id  # Actualiza el mayor identificador encontrado.

        return mayor + 1  # Devuelve un identificador mayor que el máximo actual.

    def crear(self, datos):  # Define un método del controlador.
        """Valida los datos, crea un registro nuevo, lo guarda y devuelve el resultado de la operación.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la operación y mensaje informativo o de error."""

        error = self.validar(datos)  # Ejecuta las validaciones antes de modificar o crear el registro.

        if error:  # Comprueba si la validación encontró un error.

            return False, error  # Devuelve False y el mensaje que explica por qué falló la operación.

        # Si no escribieron el stock, empieza en 0

        stock = str(datos.get("stock", "")).strip()  # Obtiene el stock recibido y elimina espacios sobrantes.

        producto = Producto(self.siguiente(),  # Realiza la operación indicada en esta línea.

                            str(datos["nombre"]).strip().title(),  # Realiza la operación indicada en esta línea.

                            float(datos["precio"]),  # Realiza la operación indicada en esta línea.

                            int(stock) if stock != "" else 0)  # Realiza la operación indicada en esta línea.

        self.lista.append(producto)  # Agrega el nuevo objeto a la lista.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Producto creado: {producto.etiqueta()}"  # Devuelve True y un mensaje de confirmación.

    def actualizar(self, id_producto, datos):  # Define un método del controlador.
        """Valida y aplica los cambios indicados a un registro existente y guarda los cambios.

        Args:
            id_producto: Identificador del producto que se consulta o modifica.
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la actualización y mensaje correspondiente."""

        producto = self.obtener(id_producto)  # Realiza la operación indicada en esta línea.

        if producto is None:  # Comprueba si el producto no existe.

            return False, f"No existe un producto con id {id_producto}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        if not datos:  # Comprueba si no se enviaron cambios.

            return False, "No se indicó ningún cambio"  # Devuelve False y el mensaje que explica por qué falló la operación.

        desconocidos = set(datos) - {"nombre", "precio", "stock"}  # Obtiene los campos recibidos que no están permitidos.

        if desconocidos:  # Comprueba si se recibieron campos desconocidos.

            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        error = self.validar(datos, id_producto)  # Ejecuta las validaciones antes de modificar o crear el registro.

        if error:  # Comprueba si la validación encontró un error.

            return False, error  # Devuelve False y el mensaje que explica por qué falló la operación.

        if "nombre" in datos:  # Procesa el nombre solo si se incluyó en los datos recibidos.

            producto.nombre = str(datos["nombre"]).strip().title()  # Actualiza el nombre del producto.

        if "precio" in datos:  # Valida el precio si fue incluido en los datos recibidos.

            producto.precio = float(datos["precio"])  # Convierte el precio a decimal y actualiza el producto.

        if "stock" in datos:  # Comprueba si se proporcionó un stock nuevo.

            producto.stock = int(datos["stock"])  # Convierte el stock a entero y actualiza el producto.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Producto {id_producto} actualizado"  # Devuelve True y un mensaje de confirmación.

    def eliminar(self, id_producto):  # Define un método del controlador.
        """Elimina un registro existente y guarda la lista actualizada.

        Args:
            id_producto: Identificador del producto que se consulta o modifica.

        Returns:
            tuple[bool, str]: resultado de la eliminación/anulación y mensaje correspondiente."""

        producto = self.obtener(id_producto)  # Realiza la operación indicada en esta línea.

        if producto is None:  # Comprueba si el producto no existe.

            return False, f"No existe un producto con id {id_producto}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        self.lista.remove(producto)  # Elimina de la lista el objeto indicado.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Producto {id_producto} eliminado"  # Devuelve True y un mensaje de confirmación.

    # --- propio de productos ---

    def con_stock_bajo(self):  # Define un método del controlador.
        """Devuelve una lista de productos cuyo stock está bajo.

        Returns:
            list: productos cuyo stock está bajo."""

        bajos = []  # Crea una lista para los productos con stock bajo.

        for producto in self.lista:  # Recorre los productos almacenados.

            if producto.stock_bajo():  # Comprueba si el producto tiene pocas unidades.

                bajos.append(producto)  # Agrega el producto a la lista de stock bajo.

        return bajos  # Devuelve el resultado de la función.

# =====================================================================

# CONTROLADOR DE VENTAS

# =====================================================================

class VentaController(CrudBase):  # Define una clase para organizar las operaciones del controlador.
    """Controlador que registra y administra ventas relacionadas con clientes y productos."""

    def __init__(self, clientes, productos, archivo="data/ventas.json"):  # Inicializa el objeto con los datos y recursos necesarios.
        """Inicializa el controlador y carga los registros guardados en el archivo JSON.

        Args:
            clientes: Controlador de clientes utilizado por las ventas.
            productos: Controlador de productos utilizado por las ventas.
            archivo: Ruta del archivo JSON utilizado para guardar los registros.

        Returns:
            No devuelve ningún valor; inicializa el objeto."""

        # La venta USA a los otros dos controladores.

        # Hay que pasarle los MISMOS que usa main.py.

        self.clientes = clientes  # Guarda la referencia al controlador de clientes.

        self.productos = productos  # Guarda la referencia al controlador de productos.

        self.gestor = GestorJSON(archivo)  # Crea el gestor encargado de acceder al archivo JSON.

        self.lista = []  # Crea una lista vacía para almacenar los objetos.

        for datos in self.gestor.leer():  # Recorre los registros leídos del archivo JSON.

            self.lista.append(Venta.desde_diccionario(datos))  # Convierte el diccionario en un objeto y lo agrega a la lista.

    def guardar(self):  # Define un método del controlador.
        """Guarda en el archivo JSON los registros actuales de la lista.

        Returns:
            No devuelve ningún valor; guarda los datos en el archivo JSON."""

        datos = []  # Crea una lista donde se prepararán los datos para guardarlos.

        for venta in self.lista:  # Recorre las ventas almacenadas.

            datos.append(venta.a_diccionario())  # Convierte el objeto a diccionario y lo agrega a los datos que se guardarán.

        self.gestor.guardar(datos)  # Guarda los datos en el archivo JSON.

    def validar(self, datos):  # Define un método del controlador.
        """Valida los datos recibidos antes de crear o actualizar un registro.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            str: mensaje de error si los datos no son válidos; None si son válidos."""

        try:  # Intenta convertir los valores recibidos al tipo numérico requerido.

            cliente_id = int(datos.get("cliente_id", 0))  # Convierte el ID del cliente a un número entero.

            producto_id = int(datos.get("producto_id", 0))  # Convierte el ID del producto a un número entero.

            cantidad = int(datos.get("cantidad", 0))  # Convierte la cantidad solicitada a un número entero.

        except (TypeError, ValueError):  # Captura errores de conversión para evitar que el programa se detenga.

            return "cliente_id, producto_id y cantidad deben ser números enteros"  # Devuelve el resultado de la función.

        if cantidad <= 0:  # Comprueba que la cantidad solicitada sea positiva.

            return "La cantidad debe ser mayor a 0"  # Devuelve el resultado de la función.

        if self.clientes.obtener(cliente_id) is None:  # Comprueba que el cliente exista.

            return f"No existe un cliente con id {cliente_id}"  # Devuelve el mensaje correspondiente al resultado de la operación.

        producto = self.productos.obtener(producto_id)  # Busca el producto asociado a la operación.

        if producto is None:  # Comprueba si el producto no existe.

            return f"No existe un producto con id {producto_id}"  # Devuelve el mensaje correspondiente al resultado de la operación.

        if not producto.hay_stock(cantidad):  # Comprueba si hay suficiente stock para la venta.

            return (f"Stock insuficiente de {producto.nombre}: "  # Devuelve un mensaje con el stock disponible y la cantidad solicitada.

                    f"hay {producto.stock}, piden {cantidad}")  # Realiza la operación indicada en esta línea.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def leer(self):  # Define un método del controlador.
        """Devuelve la lista completa de registros cargados.

        Returns:
            list: lista de objetos registrados."""

        return self.lista  # Devuelve la lista completa de registros.

    def obtener(self, id_venta):  # Define un método del controlador.
        """Busca un registro por su identificador y lo devuelve; si no existe, devuelve None.

        Args:
            id_venta: Identificador de la venta que se consulta, anula o imprime.

        Returns:
            object | None: registro encontrado o None si no existe."""

        for venta in self.lista:  # Recorre las ventas almacenadas.

            if venta.id == id_venta:  # Comprueba si el identificador coincide con el solicitado.

                return venta  # Devuelve el registro encontrado.

        return None  # Indica que no se encontró un registro o que no hay errores.

    def buscar(self, texto):  # Define un método del controlador.
        """Busca registros que coincidan con el texto indicado y devuelve una lista de resultados.

        Args:
            texto: Texto que se utilizará para buscar coincidencias.

        Returns:
            list: registros que coinciden con el texto de búsqueda."""

        # Las ventas se buscan por fecha, ej: "2026-09"

        texto = texto.strip()  # Inicializa el texto del comprobante con la información indicada.

        encontradas = []  # Crea una lista vacía para los resultados de la búsqueda.

        if texto == "":  # Comprueba si el usuario dejó vacía la búsqueda.

            return encontradas  # Devuelve la lista de resultados encontrados.

        for venta in self.lista:  # Recorre las ventas almacenadas.

            if texto in venta.fecha:  # Comprueba si el texto aparece en alguno de los campos buscables.

                encontradas.append(venta)  # Agrega el registro que coincide con la búsqueda.

        return encontradas  # Devuelve la lista de resultados encontrados.

    def siguiente(self):  # Define un método del controlador.
        """Calcula y devuelve el siguiente identificador disponible.

        Returns:
            int: siguiente identificador disponible."""

        mayor = 0  # Inicializa el mayor identificador encontrado.

        for venta in self.lista:  # Recorre las ventas almacenadas.

            if venta.id > mayor:  # Comprueba si este ID supera al mayor encontrado.

                mayor = venta.id  # Actualiza el mayor identificador encontrado.

        return mayor + 1  # Devuelve un identificador mayor que el máximo actual.

    def crear(self, datos):  # Define un método del controlador.
        """Valida los datos, crea un registro nuevo, lo guarda y devuelve el resultado de la operación.

        Args:
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la operación y mensaje informativo o de error."""

        # datos = {"cliente_id": 1, "producto_id": 2, "cantidad": 3}

        error = self.validar(datos)  # Ejecuta las validaciones antes de modificar o crear el registro.

        if error:  # Comprueba si la validación encontró un error.

            return False, error  # Devuelve False y el mensaje que explica por qué falló la operación.

        producto = self.productos.obtener(int(datos["producto_id"]))  # Busca el producto asociado a la operación.

        venta = Venta(self.siguiente(),  # Crea la venta con su ID, cliente, producto, cantidad y precio.

                      int(datos["cliente_id"]),  # Realiza la operación indicada en esta línea.

                      producto.id,  # Realiza la operación indicada en esta línea.

                      int(datos["cantidad"]),  # Realiza la operación indicada en esta línea.

                      producto.precio)          # foto del precio del momento

        producto.descontar_stock(venta.cantidad)  # Resta del inventario las unidades vendidas.

        self.productos.guardar()                # guarda el stock nuevo en productos.json

        self.lista.append(venta)  # Agrega el nuevo objeto a la lista.

        self.guardar()                          # guarda la venta en ventas.json

        return True, f"Venta {venta.id} registrada por ${venta.calcular_total():.2f}"  # Devuelve True y un mensaje de confirmación.

    def actualizar(self, id_venta, datos):  # Define un método del controlador.
        """Valida y aplica los cambios indicados a un registro existente y guarda los cambios.

        Args:
            id_venta: Identificador de la venta que se consulta, anula o imprime.
            datos: Diccionario con los datos que se crearán, validarán o actualizarán.

        Returns:
            tuple[bool, str]: resultado de la actualización y mensaje correspondiente."""

        # Una venta registrada no se modifica: se anula y se registra otra

        return False, "Las ventas no se pueden modificar: anúlela y registre otra"  # Devuelve False y el mensaje que explica por qué falló la operación.

    def eliminar(self, id_venta):  # Define un método del controlador.
        """Elimina un registro existente y guarda la lista actualizada.

        Args:
            id_venta: Identificador de la venta que se consulta, anula o imprime.

        Returns:
            tuple[bool, str]: resultado de la eliminación/anulación y mensaje correspondiente."""

        """Anular una venta: se borra y el stock vuelve al producto."""

        venta = self.obtener(id_venta)  # Busca la venta por su identificador.

        if venta is None:  # Comprueba si se cumple la condición indicada.

            return False, f"No existe la venta {id_venta}"  # Devuelve False y el mensaje que explica por qué falló la operación.

        producto = self.productos.obtener(venta.producto_id)  # Busca el producto asociado a la operación.

        if producto is not None:  # Comprueba si se cumple la condición indicada.

            producto.devolver_stock(venta.cantidad)  # Devuelve al inventario las unidades de la venta anulada.

            self.productos.guardar()  # Realiza la operación indicada en esta línea.

        self.lista.remove(venta)  # Elimina de la lista el objeto indicado.

        self.guardar()  # Guarda los cambios en el archivo correspondiente.

        return True, f"Venta {id_venta} anulada y stock devuelto"  # Devuelve True y un mensaje de confirmación.

    # --- propio de ventas ---

    def comprobante(self, id_venta):  # Define un método del controlador.
        """Genera y devuelve el texto del comprobante de una venta; devuelve None si no existe.

        Args:
            id_venta: Identificador de la venta que se consulta, anula o imprime.

        Returns:
            str | None: texto del comprobante o None si la venta no existe."""

        venta = self.obtener(id_venta)  # Busca la venta por su identificador.

        if venta is None:  # Comprueba si se cumple la condición indicada.

            return None  # Indica que no se encontró un registro o que no hay errores.

        cliente = self.clientes.obtener(venta.cliente_id)  # Busca los datos del cliente asociado a la venta.

        producto = self.productos.obtener(venta.producto_id)  # Busca el producto asociado a la operación.

        total = venta.calcular_total()  # Calcula el subtotal de la venta.

        texto = f"COMPROBANTE #{venta.id}   fecha: {venta.fecha}\n"

        texto += f"Cliente : {cliente.nombre_completo() if cliente else 'eliminado'}\n"  # Añade una línea de información al comprobante.

        texto += f"Producto: {producto.nombre if producto else 'eliminado'}\n"  # Añade una línea de información al comprobante.

        texto += f"Cantidad: {venta.cantidad} x ${venta.precio_unitario:.2f}\n"  # Añade una línea de información al comprobante.

        texto += "-" * 42 + "\n"  # Añade una línea de información al comprobante.

        texto += f"SUBTOTAL: ${total:.2f}\n"  # Añade una línea de información al comprobante.

        texto += f"TOTAL con IVA: ${Producto.con_iva(total):.2f}"  # Añade una línea de información al comprobante.

        return texto  # Devuelve el resultado de la función.

    def ventas_por_cliente(self):  # Define un método del controlador.
        """Agrupa las ventas en un diccionario usando el ID del cliente como clave.

        Returns:
            dict: diccionario que relaciona cada ID de cliente con su lista de ventas."""

        """DICCIONARIO de LISTAS: {cliente_id: [ventas de ese cliente]}."""

        agrupadas = {}  # Crea un diccionario vacío para agrupar las ventas por cliente.

        for venta in self.lista:  # Recorre las ventas almacenadas.

            if venta.cliente_id not in agrupadas:  # Comprueba si todavía no existe una entrada para este cliente.

                agrupadas[venta.cliente_id] = []  # Crea una lista para guardar las ventas de ese cliente.

            agrupadas[venta.cliente_id].append(venta)  # Agrega la venta a la lista del cliente correspondiente.

        return agrupadas  # Devuelve el resultado de la función.

    def total_vendido(self):  # Define un método del controlador.
        """Calcula y devuelve la suma total de las ventas redondeada a dos decimales.

        Returns:
            float: suma de los importes de las ventas, redondeada a dos decimales."""

        total = 0  # Inicializa el acumulador del importe total.

        for venta in self.lista:  # Recorre las ventas almacenadas.

            total += venta.calcular_total()  # Suma el importe de esta venta al total acumulado.

        return round(total, 2)  # Devuelve el total redondeado a dos decimales.