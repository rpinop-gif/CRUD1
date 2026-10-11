import json  # Permite trabajar con archivos en formato JSON.
import os  # Permite trabajar con carpetas y rutas.


class GestorJSON:
    """Clase encargada de leer y guardar datos en archivos JSON."""

    def __init__(self, ruta):
        """Inicializa el gestor JSON.

        Args:
            ruta (str): Ruta donde se encuentra el archivo JSON.

        Returns:
            None: No devuelve ningún valor.
        """
        self.ruta = ruta  # Guarda la ruta del archivo.

        carpeta = os.path.dirname(ruta)  # Obtiene la carpeta de la ruta.

        if carpeta and not os.path.exists(carpeta):  # Comprueba si la carpeta no existe.
            os.makedirs(carpeta)  # Crea la carpeta necesaria.

    def leer(self):
        """Lee los datos almacenados en el archivo JSON.

        Returns:
            list: Lista de diccionarios leídos del archivo.
        """
        if not os.path.exists(self.ruta):  # Comprueba si el archivo no existe.
            return []  # Devuelve una lista vacía.

        try:  # Intenta abrir y leer el archivo.
            with open(
                self.ruta,
                "r",
                encoding="utf-8"
            ) as archivo:  # Abre el archivo en modo lectura.
                datos = json.load(archivo)  # Convierte el JSON en datos de Python.

            return datos if isinstance(datos, list) else []  # Solo acepta listas.

        except (json.JSONDecodeError, OSError):  # Captura errores de JSON o del archivo.
            return []  # Devuelve una lista vacía si existe algún problema.

    def guardar(self, datos):
        """Guarda datos en el archivo JSON.

        Args:
            datos (list): Datos que se desean guardar.

        Returns:
            bool: True si se guardó correctamente, False si ocurrió un error.
        """
        try:  # Intenta guardar los datos.
            with open(
                self.ruta,
                "w",
                encoding="utf-8"
            ) as archivo:  # Abre el archivo en modo escritura.
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )  # Convierte los datos a JSON y los guarda.

            return True  # Indica que se guardó correctamente.

        except (TypeError, OSError):  # Captura errores de datos o del archivo.
            return False  # Indica que no se pudo guardar.