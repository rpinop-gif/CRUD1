from datetime import date  # Importa date para trabajar con fechas.


# =====================================================================
# CLASE BASE: lo que los tres modelos comparten
# =====================================================================

class ModeloBase:
    """
    Clase padre de todos los modelos del sistema.

    Guarda el ID del registro y define comportamientos
    que pueden utilizar las clases hijas.
    """ 

    def __init__(self, id_registro):
        """
        Inicializa el modelo con su identificador.

        Args:
            id_registro (int): Identificador del registro.

        Returns:
            None: No devuelve ningún valor.
        """
        self.id = int(id_registro)  # Convierte el ID a entero y lo guarda en el objeto.


    # ---- ÚNICO MÉTODO DE CLASE DEL PROYECTO ----

    @classmethod
    def desde_diccionario(cls, datos):
        """
        Convierte un diccionario en un objeto de la clase correspondiente.

        Args:
            datos (dict): Diccionario con los datos del objeto.

        Returns:
            ModeloBase: Objeto creado a partir del diccionario.
        """
        datos = dict(datos)  # Crea una copia del diccionario para no modificar el original.

        id_registro = datos.pop("id")  # Extrae y elimina el ID del diccionario.

        return cls(id_registro, **datos)  # Crea el objeto usando el ID y los demás datos.


    # ---- MÉTODOS DE INSTANCIA ----

    def a_diccionario(self):
        """
        Convierte el objeto en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Diccionario que contiene el ID del objeto.
        """
        return {"id": self.id}  # Devuelve un diccionario con el ID.


    def etiqueta(self):
        """
        Devuelve una etiqueta básica para identificar el registro.

        Args:
            No recibe argumentos.

        Returns:
            str: Texto que identifica el registro.
        """
        return f"registro {self.id}"  # Devuelve el texto con el ID del registro.


    def __str__(self):
        """
        Define cómo se muestra el objeto cuando se utiliza print().

        Args:
            No recibe argumentos.

        Returns:
            str: Representación en texto del objeto.
        """
        return f"[{self.id}] {self.etiqueta()}"  # Devuelve el ID y la etiqueta del objeto.


# =====================================================================
# HERENCIA: Persona es la base de Cliente
# =====================================================================

class Persona(ModeloBase):
    """
    Representa los datos comunes de una persona del sistema.

    Hereda de ModeloBase.
    """

    def __init__(self, id_registro, nombre, apellido, email):
        """
        Inicializa una persona.

        Args:
            id_registro (int): Identificador de la persona.
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            email (str): Correo electrónico de la persona.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Llama al constructor del padre para guardar el ID.

        self.nombre = nombre  # Guarda el nombre.

        self.apellido = apellido  # Guarda el apellido.

        self.email = email  # Guarda el correo electrónico.


    def nombre_completo(self):
        """
        Une el nombre y apellido de la persona.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre completo de la persona.
        """
        return f"{self.nombre} {self.apellido}"  # Devuelve nombre y apellido juntos.


    def a_diccionario(self):
        """
        Convierte los datos de la persona en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Diccionario con ID, nombre, apellido y email.
        """
        datos = super().a_diccionario()  # Obtiene el diccionario con el ID creado por ModeloBase.

        datos["nombre"] = self.nombre  # Agrega el nombre al diccionario.

        datos["apellido"] = self.apellido  # Agrega el apellido al diccionario.

        datos["email"] = self.email  # Agrega el email al diccionario.

        return datos  # Devuelve el diccionario completo.


    def etiqueta(self):
        """
        Devuelve una etiqueta con el nombre completo de la persona.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre completo de la persona.
        """
        return self.nombre_completo()  # Utiliza el método nombre_completo().


class Cliente(Persona):
    """
    Representa un cliente del sistema.

    Hereda de Persona y agrega teléfono y ciudad.
    """

    def __init__(self, id_registro, nombre, apellido, email, telefono="", ciudad=""):
        """
        Inicializa un cliente.

        Args:
            id_registro (int): Identificador del cliente.
            nombre (str): Nombre del cliente.
            apellido (str): Apellido del cliente.
            email (str): Correo electrónico.
            telefono (str): Número telefónico.
            ciudad (str): Ciudad del cliente.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro, nombre, apellido, email)  # Inicializa la parte heredada de Persona.

        self.telefono = telefono  # Guarda el teléfono.

        self.ciudad = ciudad  # Guarda la ciudad.


    def a_diccionario(self):
        """
        Convierte los datos del cliente en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Diccionario con todos los datos del cliente.
        """
        datos = super().a_diccionario()  # Obtiene los datos de Persona.

        datos["telefono"] = self.telefono  # Agrega el teléfono.

        datos["ciudad"] = self.ciudad  # Agrega la ciudad.

        return datos  # Devuelve todos los datos.


    def etiqueta(self):
        """
        Crea una etiqueta personalizada para el cliente.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre, email y ciudad del cliente.
        """
        # Utiliza la etiqueta de Persona y agrega email y ciudad.
        return f"{super().etiqueta()} · {self.email} · {self.ciudad or 'sin ciudad'}"


# =====================================================================
# ÚNICA CLASE CON ATRIBUTOS Y MÉTODOS ESTÁTICOS
# =====================================================================

class Producto(ModeloBase):
    """
    Representa un producto del sistema.

    Hereda de ModeloBase y contiene atributos y métodos estáticos.
    """

    # ATRIBUTOS ESTÁTICOS: pertenecen a la clase y son compartidos.

    STOCK_MINIMO = 5  # Cantidad mínima de stock para generar una alerta.

    IVA = 0.15  # Porcentaje de IVA utilizado en los productos.

    total_creados = 0  # Contador compartido de productos creados.


    def __init__(self, id_registro, nombre, precio, stock=0):
        """
        Inicializa un producto.

        Args:
            id_registro (int): Identificador del producto.
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.
            stock (int): Cantidad disponible del producto.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Inicializa el ID utilizando ModeloBase.

        self.nombre = nombre  # Guarda el nombre del producto.

        self.precio = float(precio)  # Convierte el precio a número decimal.

        self.stock = int(stock)  # Convierte el stock a entero.

        Producto.total_creados += 1  # Aumenta el contador compartido de productos.


    # MÉTODOS ESTÁTICOS: no necesitan un objeto específico.

    @staticmethod
    def es_precio_valido(valor):
        """
        Comprueba si un precio es válido.

        Args:
            valor: Valor que se desea comprobar.

        Returns:
            bool: True si el valor es mayor que cero.
            False si no es válido.
        """
        try:
            return float(valor) > 0  # Convierte el valor a decimal y comprueba que sea mayor que cero.
        except (TypeError, ValueError):
            return False  # Devuelve False si el valor no puede convertirse a número.


    @staticmethod
    def con_iva(monto):
        """
        Calcula el precio de un monto incluyendo IVA.

        Args:
            monto (float): Valor al que se aplicará el IVA.

        Returns:
            float: Monto final con IVA incluido.
        """
        return round(monto * (1 + Producto.IVA), 2)  # Calcula el IVA y redondea a dos decimales.


    # MÉTODOS DE INSTANCIA: trabajan con los datos de un producto específico.

    def stock_bajo(self):
        """
        Comprueba si el producto tiene stock bajo.

        Args:
            No recibe argumentos.

        Returns:
            bool: True si el stock es menor o igual al mínimo.
            False si el stock es mayor al mínimo.
        """
        return self.stock <= Producto.STOCK_MINIMO  # Compara el stock con el mínimo establecido.


    def hay_stock(self, cantidad):
        """
        Comprueba si existe suficiente stock para una cantidad.

        Args:
            cantidad (int): Cantidad que se desea comprobar.

        Returns:
            bool: True si existe suficiente stock.
            False si no existe suficiente stock.
        """
        return 0 < cantidad <= self.stock  # Comprueba que la cantidad sea positiva y esté disponible.


    def descontar_stock(self, cantidad):
        """
        Reduce el stock del producto.

        Args:
            cantidad (int): Cantidad que se desea descontar.

        Returns:
            None: No devuelve ningún valor.
        """
        self.stock -= cantidad  # Resta la cantidad indicada al stock.


    def devolver_stock(self, cantidad):
        """
        Aumenta el stock del producto.

        Args:
            cantidad (int): Cantidad que se desea devolver.

        Returns:
            None: No devuelve ningún valor.
        """
        self.stock += cantidad  # Suma la cantidad indicada al stock.


    def a_diccionario(self):
        """
        Convierte los datos del producto en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Diccionario con los datos del producto.
        """
        datos = super().a_diccionario()  # Obtiene el ID desde ModeloBase.

        datos["nombre"] = self.nombre  # Agrega el nombre.

        datos["precio"] = self.precio  # Agrega el precio.

        datos["stock"] = self.stock  # Agrega el stock.

        return datos  # Devuelve el diccionario completo.


    def etiqueta(self):
        """
        Crea una descripción del producto mostrando su información principal.

        Args:
            No recibe argumentos.

        Returns:
            str: Nombre, precio, stock y alerta si existe stock bajo.
        """
        alerta = " ⚠ stock bajo" if self.stock_bajo() else ""  # Agrega una alerta si el stock es bajo.

        return f"{self.nombre} · ${self.precio:.2f} · stock {self.stock}{alerta}"  # Devuelve la información del producto.


# =====================================================================

class Venta(ModeloBase):
    """
    Representa una venta realizada en el sistema.

    Una venta contiene un cliente, un producto y una cantidad.
    """

    def __init__(self, id_registro, cliente_id, producto_id, cantidad,
                 precio_unitario, fecha=""):
        """
        Inicializa una venta.

        Args:
            id_registro (int): Identificador de la venta.
            cliente_id (int): ID del cliente que realizó la compra.
            producto_id (int): ID del producto vendido.
            cantidad (int): Cantidad de productos vendidos.
            precio_unitario (float): Precio de cada producto.
            fecha (str): Fecha de la venta.

        Returns:
            None: No devuelve ningún valor.
        """
        super().__init__(id_registro)  # Inicializa el ID utilizando ModeloBase.

        self.cliente_id = int(cliente_id)  # Guarda el ID del cliente como entero.

        self.producto_id = int(producto_id)  # Guarda el ID del producto como entero.

        self.cantidad = int(cantidad)  # Guarda la cantidad como entero.

        self.precio_unitario = float(precio_unitario)  # Guarda el precio como decimal.

        self.fecha = fecha or date.today().isoformat()  # Usa la fecha indicada o la fecha actual.


    def calcular_total(self):
        """
        Calcula el valor total de la venta.

        Args:
            No recibe argumentos.

        Returns:
            float: Total de la venta redondeado a dos decimales.
        """
        # El total se calcula cada vez para evitar que quede desactualizado.
        return round(self.cantidad * self.precio_unitario, 2)  # Multiplica cantidad por precio unitario.


    def a_diccionario(self):
        """
        Convierte los datos de la venta en un diccionario.

        Args:
            No recibe argumentos.

        Returns:
            dict: Diccionario con todos los datos de la venta.
        """
        datos = super().a_diccionario()  # Obtiene el ID desde ModeloBase.

        datos["cliente_id"] = self.cliente_id  # Agrega el ID del cliente.

        datos["producto_id"] = self.producto_id  # Agrega el ID del producto.

        datos["cantidad"] = self.cantidad  # Agrega la cantidad.

        datos["precio_unitario"] = self.precio_unitario  # Agrega el precio unitario.

        datos["fecha"] = self.fecha  # Agrega la fecha.

        return datos  # Devuelve el diccionario completo.


    def etiqueta(self):
        """
        Crea una descripción de la venta.

        Args:
            No recibe argumentos.

        Returns:
            str: Fecha, cliente, cantidad, producto y total de la venta.
        """
        return (f"{self.fecha} · cliente {self.cliente_id} · "  # Agrega la fecha y el cliente.
                f"{self.cantidad} x producto {self.producto_id} "  # Agrega cantidad y producto.
                f"= ${self.calcular_total():.2f}")  # Calcula y muestra el total.




    # =====================================================================
# MODELO DE PAGOS
# =====================================================================

class Pago(ModeloBase):
    """
    Representa un pago realizado para una venta.

    Relaciona un pago con el ID de una venta, monto, método de pago y fecha.
    """

    METODOS_PERMITIDOS = ("EFECTIVO", "TARJETA", "TRANSFERENCIA")

    def __init__(self, id_registro, venta_id, monto, metodo="EFECTIVO", fecha=""):
        """
        Inicializa un pago.

        Args:
            id_registro (int): Identificador del pago.
            venta_id (int): ID de la venta asociada.
            monto (float): Monto pagado.
            metodo (str): Método de pago (EFECTIVO, TARJETA, TRANSFERENCIA).
            fecha (str): Fecha del pago.
        """
        super().__init__(id_registro)
        self.venta_id = int(venta_id)
        self.monto = float(monto)
        self.metodo = str(metodo).upper()
        self.fecha = fecha or date.today().isoformat()

    def a_diccionario(self):
        """Convierte los datos del pago en un diccionario."""
        datos = super().a_diccionario()
        datos["venta_id"] = self.venta_id
        datos["monto"] = self.monto
        datos["metodo"] = self.metodo
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        """Crea una descripción corta del pago."""
        return f"{self.fecha} · Venta #{self.venta_id} · ${self.monto:.2f} ({self.metodo})"