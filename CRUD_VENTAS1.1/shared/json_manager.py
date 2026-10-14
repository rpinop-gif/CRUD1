import json  # Importa el módulo json para leer y guardar datos en formato JSON.
import os  # Importa el módulo os para trabajar con archivos, carpetas y rutas.


class GestorJSON:
    """
    Gestiona la lectura y escritura de datos en archivos JSON.

    La clase se encarga de crear la carpeta si no existe,
    leer los datos del archivo y guardar nuevos datos.

    Args:
        ruta (str): Ruta donde se encuentra o se creará el archivo JSON.
    """

    def __init__(self, ruta):
        """
        Inicializa el gestor con la ruta del archivo JSON.

        Args:
            ruta (str): Ruta del archivo JSON que se utilizará.

        Returns:
            None: No devuelve ningún valor.
        """
        self.ruta = ruta  # Guarda la ruta del archivo en el atributo de la clase.

        carpeta = os.path.dirname(ruta)  # Obtiene solamente la carpeta donde estará el archivo.

        if carpeta and not os.path.exists(carpeta):  # Comprueba si existe una carpeta y si todavía no existe.
            os.makedirs(carpeta)  # Crea la carpeta y las carpetas necesarias.


    def leer(self):
        """
        Lee los datos almacenados en el archivo JSON.

        Si el archivo no existe, está dañado o no contiene una lista,
        devuelve una lista vacía.

        Args:
            No recibe argumentos.

        Returns:
            list: Lista de diccionarios obtenida del archivo JSON.
            Si existe algún problema, devuelve una lista vacía.
        """

        # Comprueba si el archivo no existe.
        if not os.path.exists(self.ruta):
            return []  # Si no existe, devuelve una lista vacía.

        try:
            # Abre el archivo en modo lectura con codificación UTF-8.
            with open(self.ruta, "r", encoding="utf-8") as archivo:

                # Convierte el contenido JSON del archivo en datos de Python.
                datos = json.load(archivo)

            # Comprueba que los datos sean una lista.
            # Si son una lista, la devuelve; si no, devuelve una lista vacía.
            return datos if isinstance(datos, list) else []

        except (json.JSONDecodeError, OSError):
            # Captura errores relacionados con JSON o con el archivo.
            return []  # Si ocurre un error, devuelve una lista vacía.


    def guardar(self, datos):
        """
        Guarda una lista de datos en el archivo JSON.

        Args:
            datos (list): Lista de diccionarios que se desea guardar.

        Returns:
            bool: True si los datos se guardaron correctamente.
            False si ocurrió un error.
        """

        try:
            # Abre el archivo en modo escritura.
            # Si no existe, lo crea.
            # Si existe, reemplaza su contenido.
            with open(self.ruta, "w", encoding="utf-8") as archivo:

                # Convierte los datos de Python a formato JSON.
                # ensure_ascii=False permite guardar caracteres como ñ y tildes.
                # indent=2 organiza el JSON con sangría de 2 espacios.
                json.dump(datos, archivo, ensure_ascii=False, indent=2)

            return True  # Indica que el guardado se realizó correctamente.

        except (TypeError, OSError):
            # Captura errores relacionados con los datos o con el archivo.
            return False  # Indica que ocurrió un error al guardar.