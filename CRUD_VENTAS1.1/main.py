from shared.herramientas import (  # Importa las funciones auxiliares para mostrar mensajes y confirmar acciones.
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar  # Importa las funciones necesarias.
)

from views import ClienteController, ProductoController, VentaController, PagoController  # Importa los controladores del sistema.
 #ANADI PAGOCONTROLER AQUI Y TAMBIEN ABAJO

# Se crea UN solo controlador de cada tipo.
# Esto permite trabajar con los mismos objetos durante todo el programa.

clientes = ClienteController()  # Crea el controlador encargado de gestionar clientes.
productos = ProductoController()  # Crea el controlador encargado de gestionar productos.
ventas = VentaController(clientes, productos)  # Crea el controlador de ventas usando clientes y productos.
pagos = PagoController(ventas)

# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================


def pausa():
    """
    Pausa la ejecución del programa hasta que el usuario presione Enter.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    input("\nPresione Enter para continuar...")  # Espera que el usuario presione Enter.


def pedir_entero(etiqueta):
    """
    Solicita al usuario un número entero.

    Args:
        etiqueta (str): Texto que se mostrará al solicitar el número.

    Returns:
        int: Número entero ingresado por el usuario.
        None: Si el usuario escribe algo que no es un número entero.
    """
    try:
        return int(input(etiqueta))  # Solicita un valor y lo convierte a entero.
    except ValueError:
        return None  # Si no se puede convertir, devuelve None.


def mostrar_resultado(exito, mensaje):
    """
    Muestra un mensaje de éxito o de error.

    Args:
        exito (bool): Indica si la operación fue exitosa.
        mensaje (str): Mensaje que se mostrará al usuario.

    Returns:
        None: No devuelve ningún valor.
    """
    # Los controladores devuelven una tupla (exito, mensaje).
    if exito:
        imprimir_exito(mensaje)  # Muestra el mensaje en caso de éxito.
    else:
        imprimir_error(mensaje)  # Muestra el mensaje en caso de error.


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """
    Muestra una lista de objetos en la consola.

    Args:
        objetos (list): Lista de objetos que se desean mostrar.
        vacio (str): Mensaje que se muestra si la lista está vacía.

    Returns:
        None: No devuelve ningún valor.
    """
    # Comprueba si la lista está vacía.
    if not objetos:
        imprimir_info(vacio)  # Muestra el mensaje indicando que no hay registros.
        return  # Termina la función.

    # Recorre todos los objetos de la lista.
    for objeto in objetos:
        print(f"  {objeto}")  # Muestra cada objeto.

    imprimir_info(f"Total: {len(objetos)}")  # Muestra la cantidad total de objetos.


def mostrar_detalle(objeto):
    """
    Muestra todos los datos de un objeto.

    Args:
        objeto: Objeto que contiene el método a_diccionario().

    Returns:
        None: No devuelve ningún valor.
    """
    # Convierte el objeto en un diccionario y recorre sus claves y valores.
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")  # Muestra cada dato con formato.

#ESTOOOOOOOO AGREGUE
# =====================================================================
# MENÚ DE PAGOS
# =====================================================================

def registrar_pago():
    """Solicita los datos necesarios para registrar un pago y calcula el vuelto/cambio."""
    imprimir_titulo("REGISTRAR PAGO")

    imprimir_info("Ventas registradas:")
    mostrar_lista(ventas.leer())

    venta_id = pedir_entero("\nId de la venta a pagar: ")
    if venta_id is None:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    venta = ventas.obtener(venta_id)
    if venta is None:
        imprimir_error(f"No existe la venta con id {venta_id}")
        return pausa()

    monto_total = venta.calcular_total()
    imprimir_info(f"Monto a pagar de la Venta #{venta.id}: ${monto_total:.2f}")

    metodo = input("Método (EFECTIVO / TARJETA / TRANSFERENCIA) [EFECTIVO]: ").strip() or "EFECTIVO"
    
    pagado_con = None
    if metodo.upper() == "EFECTIVO":
        pagado_input = input(f"¿Con cuánto dinero paga el cliente? [Mínimo ${monto_total:.2f}]: ").strip()
        pagado_con = pagado_input if pagado_input else monto_total

    datos = {
        "venta_id": venta_id,
        "monto": monto_total,
        "pagado_con": pagado_con,
        "metodo": metodo
    }

    exito, mensaje = pagos.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_pagos():
    """Muestra todos los pagos registrados."""
    imprimir_titulo("PAGOS")
    mostrar_lista(pagos.leer(), "Todavía no hay pagos registrados.")
    pausa()


def ver_pago():
    """Muestra el detalle de un pago por ID."""
    imprimir_titulo("VER PAGO POR ID")
    pago = pagos.obtener(pedir_entero("Id del pago: "))

    if pago is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(pago)

    pausa()


def eliminar_pago():
    """Elimina un pago existente."""
    imprimir_titulo("ELIMINAR PAGO")
    id_pago = pedir_entero("Id del pago: ")

    pago = pagos.obtener(id_pago)
    if pago is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {pago.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*pagos.eliminar(id_pago))
    else:
        imprimir_info("Operación cancelada")

    pausa()

# =====================================================================
# MENÚ DE CLIENTES
# =====================================================================


def crear_cliente():
    """
    Solicita los datos de un cliente y lo crea.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("CREAR CLIENTE")  # Muestra el título de la sección.

    datos = {
        "nombre": input("Nombre: "),  # Solicita el nombre.
        "apellido": input("Apellido: "),  # Solicita el apellido.
        "email": input("Email: "),  # Solicita el correo electrónico.
        "telefono": input("Teléfono: "),  # Solicita el teléfono.
        "ciudad": input("Ciudad: "),  # Solicita la ciudad.
    }

    mostrar_resultado(*clientes.crear(datos))  # Crea el cliente y muestra el resultado.
    pausa()  # Espera que el usuario presione Enter.


def listar_clientes():
    """
    Muestra todos los clientes registrados.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("CLIENTES")  # Muestra el título de clientes.
    mostrar_lista(clientes.leer(), "Todavía no hay clientes.")  # Obtiene y muestra todos los clientes.
    pausa()  # Espera que el usuario presione Enter.


def buscar_cliente():
    """
    Busca clientes utilizando un término de búsqueda.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("BUSCAR CLIENTE")  # Muestra el título de búsqueda.

    termino = input("Nombre, email, teléfono o ciudad: ")  # Solicita el texto de búsqueda.

    encontrados = clientes.buscar(termino)  # Busca los clientes que coincidan con el término.

    mostrar_lista(encontrados, f"Ningún cliente coincide con '{termino}'.")  # Muestra los resultados.
    pausa()  # Espera que el usuario presione Enter.


def ver_cliente():
    """
    Busca y muestra un cliente utilizando su ID.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("VER CLIENTE POR ID")  # Muestra el título.

    cliente = clientes.obtener(pedir_entero("Id: "))  # Solicita el ID y obtiene el cliente.

    if cliente is None:
        imprimir_error("No encontrado")  # Muestra error si no existe.
    else:
        mostrar_detalle(cliente)  # Muestra los datos del cliente.

    pausa()  # Espera que el usuario presione Enter.


def actualizar_cliente():
    """
    Permite modificar los datos de un cliente existente.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("ACTUALIZAR CLIENTE")  # Muestra el título.

    id_cliente = pedir_entero("Id: ")  # Solicita el ID del cliente.

    cliente = clientes.obtener(id_cliente)  # Busca el cliente mediante su ID.

    if cliente is None:
        imprimir_error("No encontrado")  # Informa que el cliente no existe.
        return pausa()  # Finaliza la función después de pausar.

    imprimir_info(f"Editando: {cliente.etiqueta()}")  # Muestra el cliente que se está editando.

    print("Deje en blanco lo que no quiera cambiar.\n")  # Indica que Enter conserva el valor actual.

    cambios = {}  # Crea un diccionario vacío para almacenar los cambios.

    # Recorre los campos que pueden ser modificados.
    for campo in ("nombre", "apellido", "email", "telefono", "ciudad"):
        actual = getattr(cliente, campo)  # Obtiene el valor actual del atributo.

        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.

        if nuevo:
            cambios[campo] = nuevo  # Guarda el nuevo valor solamente si el usuario escribió algo.

    mostrar_resultado(*clientes.actualizar(id_cliente, cambios))  # Actualiza el cliente y muestra el resultado.

    pausa()  # Espera que el usuario presione Enter.


def eliminar_cliente():
    """
    Elimina un cliente después de pedir confirmación.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("ELIMINAR CLIENTE")  # Muestra el título.

    id_cliente = pedir_entero("Id: ")  # Solicita el ID del cliente.

    cliente = clientes.obtener(id_cliente)  # Busca el cliente.

    if cliente is None:
        imprimir_error("No encontrado")  # Muestra error si no existe.
        return pausa()  # Finaliza la función.

    imprimir_info(f"Se eliminará: {cliente.etiqueta()}")  # Muestra el cliente que será eliminado.

    if confirmar("¿Confirma?"):
        mostrar_resultado(*clientes.eliminar(id_cliente))  # Elimina el cliente si confirma.
    else:
        imprimir_info("Operación cancelada")  # Informa que no se eliminó.

    pausa()  # Espera que el usuario presione Enter.


# =====================================================================
# MENÚ DE PRODUCTOS
# =====================================================================


def crear_producto():
    """
    Solicita los datos de un producto y lo crea.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("CREAR PRODUCTO")  # Muestra el título.

    datos = {
        "nombre": input("Nombre: "),  # Solicita el nombre del producto.
        "precio": input("Precio: "),  # Solicita el precio.
        "stock": input("Stock: "),  # Solicita la cantidad disponible.
    }

    mostrar_resultado(*productos.crear(datos))  # Crea el producto y muestra el resultado.

    pausa()  # Espera que el usuario presione Enter.


def listar_productos():
    """
    Muestra todos los productos registrados.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("PRODUCTOS")  # Muestra el título.

    mostrar_lista(productos.leer(), "Todavía no hay productos.")  # Obtiene y muestra los productos.

    pausa()  # Espera que el usuario presione Enter.


def buscar_producto():
    """
    Busca productos por nombre.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("BUSCAR PRODUCTO")  # Muestra el título.

    termino = input("Nombre: ")  # Solicita el nombre a buscar.

    mostrar_lista(productos.buscar(termino), "Sin coincidencias.")  # Busca y muestra los productos.

    pausa()  # Espera que el usuario presione Enter.


def ver_producto():
    """
    Busca y muestra un producto mediante su ID.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("VER PRODUCTO POR ID")  # Muestra el título.

    producto = productos.obtener(pedir_entero("Id: "))  # Solicita el ID y busca el producto.

    if producto is None:
        imprimir_error("No encontrado")  # Muestra error si no existe.
    else:
        mostrar_detalle(producto)  # Muestra los datos del producto.

        # Calcula y muestra el precio del producto con IVA.
        imprimir_info(f"Precio con IVA: ${producto.con_iva(producto.precio):.2f}")

    pausa()  # Espera que el usuario presione Enter.


def actualizar_producto():
    """
    Permite modificar los datos de un producto existente.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("ACTUALIZAR PRODUCTO")  # Muestra el título.

    id_producto = pedir_entero("Id: ")  # Solicita el ID del producto.

    producto = productos.obtener(id_producto)  # Busca el producto.

    if producto is None:
        imprimir_error("No encontrado")  # Muestra error si no existe.
        return pausa()  # Finaliza la función.

    imprimir_info(f"Editando: {producto.etiqueta()}")  # Muestra el producto que se está editando.

    print("Deje en blanco lo que no quiera cambiar.\n")  # Indica que se puede conservar el valor actual.

    cambios = {}  # Crea un diccionario para guardar los cambios.

    for campo in ("nombre", "precio", "stock"):
        actual = getattr(producto, campo)  # Obtiene el valor actual.

        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()  # Solicita el nuevo valor.

        if nuevo:
            cambios[campo] = nuevo  # Guarda el cambio si se escribió un valor.

    mostrar_resultado(*productos.actualizar(id_producto, cambios))  # Actualiza el producto.

    pausa()  # Espera que el usuario presione Enter.


def eliminar_producto():
    """
    Elimina un producto después de pedir confirmación.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("ELIMINAR PRODUCTO")  # Muestra el título.

    id_producto = pedir_entero("Id: ")  # Solicita el ID.

    producto = productos.obtener(id_producto)  # Busca el producto.

    if producto is None:
        imprimir_error("No encontrado")  # Muestra error si no existe.
        return pausa()  # Finaliza la función.

    imprimir_info(f"Se eliminará: {producto.etiqueta()}")  # Muestra el producto que será eliminado.

    if confirmar("¿Confirma?"):
        mostrar_resultado(*productos.eliminar(id_producto))  # Elimina el producto.
    else:
        imprimir_info("Operación cancelada")  # Informa que se canceló.

    pausa()  # Espera que el usuario presione Enter.


# =====================================================================
# MENÚ DE VENTAS
# =====================================================================


def registrar_venta():
    """
    Solicita los datos necesarios para registrar una venta.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("REGISTRAR VENTA")  # Muestra el título.

    imprimir_info("Clientes:")  # Muestra el título de clientes.
    mostrar_lista(clientes.leer())  # Muestra los clientes disponibles.

    imprimir_info("Productos:")  # Muestra el título de productos.
    mostrar_lista(productos.leer())  # Muestra los productos disponibles.

    datos = {
        "cliente_id": pedir_entero("\nId del cliente: "),  # Solicita el ID del cliente.
        "producto_id": pedir_entero("Id del producto: "),  # Solicita el ID del producto.
        "cantidad": pedir_entero("Cantidad: "),  # Solicita la cantidad.
    }

    if None in datos.values():
        imprimir_error("Todos los datos deben ser números enteros")  # Muestra error si algún dato no es entero.
        return pausa()  # Finaliza la función.

    mostrar_resultado(*ventas.crear(datos))  # Registra la venta y muestra el resultado.

    pausa()  # Espera que el usuario presione Enter.


def listar_ventas():
    """
    Muestra todas las ventas registradas.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("VENTAS")  # Muestra el título.

    mostrar_lista(ventas.leer(), "Todavía no hay ventas.")  # Obtiene y muestra las ventas.

    pausa()  # Espera que el usuario presione Enter.


def ver_comprobante():
    """
    Busca y muestra el comprobante de una venta.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("COMPROBANTE")  # Muestra el título.

    texto = ventas.comprobante(pedir_entero("Id de la venta: "))  # Solicita el ID y obtiene el comprobante.

    if texto is None:
        imprimir_error("No existe esa venta")  # Informa que la venta no existe.
    else:
        print(texto)  # Muestra el comprobante.

    pausa()  # Espera que el usuario presione Enter.


def anular_venta():
    """
    Anula una venta después de pedir confirmación.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("ANULAR VENTA")  # Muestra el título.

    id_venta = pedir_entero("Id de la venta: ")  # Solicita el ID de la venta.

    if id_venta and confirmar("Se devolverá el stock. ¿Confirma?"):
        mostrar_resultado(*ventas.eliminar(id_venta))  # Elimina o anula la venta.
    else:
        imprimir_info("Operación cancelada")  # Informa que la operación fue cancelada.

    pausa()  # Espera que el usuario presione Enter.


def resumen():
    """
    Muestra un resumen general del sistema.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    imprimir_titulo("RESUMEN")  # Muestra el título del resumen.

    print(f"  Clientes  : {len(clientes.leer())}")  # Muestra la cantidad de clientes.

    print(f"  Ciudades  : {', '.join(clientes.ciudades()) or '-'}")  # Muestra las ciudades registradas.

    print(f"  Productos : {len(productos.leer())}")  # Muestra la cantidad de productos.

    bajos = productos.con_stock_bajo()  # Obtiene los productos que tienen poco stock.

    print(f"  Stock bajo: {', '.join(p.nombre for p in bajos) or 'ninguno'}")  # Muestra los productos con stock bajo.

    print(f"  Ventas    : {len(ventas.leer())}")  # Muestra la cantidad de ventas.

    print(f"  Vendido   : ${ventas.total_vendido():.2f}")  # Muestra el total vendido.

    print(f"  Pagos     : {len(pagos.leer())}")  # <-- Nueva métrica

    pausa()  # Espera que el usuario presione Enter.


# =====================================================================
# MENÚS: DICCIONARIOS tecla -> (texto, función)
# =====================================================================


MENU_CLIENTES = {
    "1": ("Crear cliente", crear_cliente),  # Opción 1: crear cliente.
    "2": ("Ver todos", listar_clientes),  # Opción 2: listar clientes.
    "3": ("Buscar", buscar_cliente),  # Opción 3: buscar cliente.
    "4": ("Ver por id", ver_cliente),  # Opción 4: buscar por ID.
    "5": ("Actualizar", actualizar_cliente),  # Opción 5: actualizar cliente.
    "6": ("Eliminar", eliminar_cliente),  # Opción 6: eliminar cliente.
    "0": ("Volver", None),  # Opción 0: regresar al menú anterior.
}


MENU_PRODUCTOS = {
    "1": ("Crear producto", crear_producto),  # Opción 1: crear producto.
    "2": ("Ver todos", listar_productos),  # Opción 2: listar productos.
    "3": ("Buscar", buscar_producto),  # Opción 3: buscar producto.
    "4": ("Ver por id", ver_producto),  # Opción 4: buscar por ID.
    "5": ("Actualizar", actualizar_producto),  # Opción 5: actualizar producto.
    "6": ("Eliminar", eliminar_producto),  # Opción 6: eliminar producto.
    "0": ("Volver", None),  # Opción 0: regresar al menú anterior.
}


MENU_VENTAS = {
    "1": ("Registrar venta", registrar_venta),  # Opción 1: registrar venta.
    "2": ("Ver todas", listar_ventas),  # Opción 2: listar ventas.
    "3": ("Ver comprobante", ver_comprobante),  # Opción 3: mostrar comprobante.
    "4": ("Anular venta", anular_venta),  # Opción 4: anular venta.
    "0": ("Volver", None),  # Opción 0: regresar al menú anterior.
}

MENU_PAGOS = {
    "1": ("Registrar pago", registrar_pago),
    "2": ("Ver todos", listar_pagos),
    "3": ("Ver por id", ver_pago),
    "4": ("Eliminar pago", eliminar_pago),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """
    Ejecuta un menú reutilizable del sistema.

    Args:
        titulo (str): Título que se mostrará en el menú.
        opciones (dict): Diccionario que relaciona teclas con textos y funciones.

    Returns:
        None: No devuelve ningún valor.
    """
    while True:
        imprimir_titulo(titulo)  # Muestra el título del menú.

        # Recorre las opciones del diccionario.
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")  # Muestra cada opción.

        print()  # Deja una línea vacía.

        tecla = input("Opción: ").strip()  # Solicita al usuario una opción.

        # Comprueba si la tecla existe en el diccionario.
        if tecla not in opciones:
            imprimir_error("Opción no válida")  # Muestra error si no existe.
            pausa()  # Espera que el usuario presione Enter.
            continue  # Regresa al inicio del menú.

        _texto, funcion = opciones[tecla]  # Obtiene el texto y la función asociada.

        if funcion is None:  # Comprueba si se eligió la opción "Volver".
            break  # Sale del menú.

        funcion()  # Ejecuta la función correspondiente.


def main():
    """
    Ejecuta el menú principal del sistema de ventas.

    Args:
        No recibe argumentos.

    Returns:
        None: No devuelve ningún valor.
    """
    while True:
        imprimir_titulo("SISTEMA DE VENTAS")  # Muestra el título principal.

        print("  1. Clientes")  # Muestra la opción de clientes.
        print("  2. Productos")  # Muestra la opción de productos.
        print("  3. Ventas")  # Muestra la opción de ventas.
        print("  4. Pagos")     # <-- Opción agregada
        print("  5. Resumen")   # <-- Opción desplazada
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()  # Solicita una opción al usuario.

        if tecla == "1":
            ejecutar_menu("CLIENTES", MENU_CLIENTES)  # Abre el menú de clientes.

        elif tecla == "2":
            ejecutar_menu("PRODUCTOS", MENU_PRODUCTOS)  # Abre el menú de productos.

        elif tecla == "3":
            ejecutar_menu("VENTAS", MENU_VENTAS)  # Abre el menú de ventas.

        elif tecla == "4":
            ejecutar_menu("PAGOS", MENU_PAGOS)  # <-- Ejecución del menú de pagos
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()  # Ejecuta la función principal del programa.
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")  # Maneja Ctrl + C sin mostrar un error.
        