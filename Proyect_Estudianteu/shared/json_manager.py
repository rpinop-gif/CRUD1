
import json  # Permite trabajar con archivos JSON
import os  # Permite trabajar con rutas y carpetas


class GestorJSON:
    """Clase encargada de leer y guardar datos en archivos JSON."""

    def __init__(self, ruta):
        """
        Inicializa el gestor con la ruta del archivo.

        Args:
            ruta (str): Ruta donde se encuentra el archivo JSON.
        """
        self.ruta = ruta  # Guarda la ruta del archivo
        carpeta = os.path.dirname(ruta)  # Obtiene la carpeta de la ruta

        if carpeta and not os.path.exists(carpeta):  # Comprueba si la carpeta no existe
            os.makedirs(carpeta)  # Crea la carpeta


    def leer(self):
        """
        Lee los datos almacenados en el archivo JSON.

        Returns:
            list: Lista de datos del archivo o lista vacía si ocurre un error.
        """
        if not os.path.exists(self.ruta):  # Comprueba si existe el archivo
            return []  # Devuelve lista vacía si no existe

        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:  # Abre el archivo
                datos = json.load(archivo)  # Convierte el JSON en datos de Python

            return datos if isinstance(datos, list) else []  # Devuelve los datos si son una lista

        except (json.JSONDecodeError, OSError):  # Controla errores de lectura
            return []  # Devuelve lista vacía si ocurre un error


    def guardar(self, datos):
        """
        Guarda datos en el archivo JSON.

        Args:
            datos (list): Datos que se desean guardar.

        Returns:
            bool: True si se guardó correctamente, False si ocurrió un error.
        """
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:  # Abre el archivo para escribir
                json.dump(datos, archivo, ensure_ascii=False, indent=2)  # Guarda los datos en formato JSON

            return True  # Indica que se guardó correctamente

        except (TypeError, OSError):  # Controla errores de escritura
            return False  # Indica que no se pudo guardar

