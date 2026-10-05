# Ejercicio 1 · Quitar duplicados conservando el orden
# Dada ciudades = ["Quito","Guayaquil","Quito","Cuenca","Guayaquil"],
# obtén una lista sin repetidos respetando el orden de aparición (un set solo no alcanza).

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

sin_repetidos = []

for ciudad in ciudades:
    if ciudad not in sin_repetidos:
        sin_repetidos.append(ciudad)

print(sin_repetidos)

# Ejercicio 2 · Contar con un diccionario
# Con la misma lista, arma un diccionario {"Quito": 2, "Guayaquil": 2, "Cuenca": 1}.

conteo = {}

for ciudad in ciudades:
    if ciudad in conteo:
        conteo[ciudad] += 1
    else:
        conteo[ciudad] = 1

print(conteo)


# Ejercicio 3 · Conjuntos en acción
# inscritos_matematica = {"Ana","Luis","Sol","Marco"} y inscritos_ingles = {"Luis","Marco","Ruth"}. 
# Responde con código: ¿quiénes están en las dos?, ¿quiénes solo en matemática?, ¿cuántos estudiantes distintos hay en total?

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

en_las_dos = inscritos_matematica & inscritos_ingles
solo_matematica = inscritos_matematica - inscritos_ingles
total_distintos = len(inscritos_matematica | inscritos_ingles)

print("En las dos:", en_las_dos)
print("Solo en matemática:", solo_matematica)
print("Estudiantes distintos:", total_distintos)


# Ejercicio 4 · De lista de diccionarios a índice
# Con clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}], crea un diccionario {id: cliente}
#  para acceder por id sin recorrer la lista. Luego imprime el nombre del id 2.

clientes = [
    {"id": 1, "nombre": "Ana"},
    {"id": 2, "nombre": "Luis"}
]

clientes_por_id = {}

for cliente in clientes:
    clientes_por_id[cliente["id"]] = cliente

print(clientes_por_id[2]["nombre"])


# Ejercicio 5 · Tuplas como registros inmutables
# Dada ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)], imprime el mes con mayor venta y el total,
#  usando desempaquetado de tuplas.

ventas = [
    ("enero", 1500),
    ("febrero", 1800),
    ("marzo", 1200)
]

mayor_mes = ""
mayor_venta = 0
total = 0

for mes, venta in ventas:
    total += venta

    if venta > mayor_venta:
        mayor_venta = venta
        mayor_mes = mes

print("Mes con mayor venta:", mayor_mes)
print("Mayor venta:", mayor_venta)
print("Total:", total)


# Ejercicio 6 · Sobre el proyecto
# Agrega al Controlador la función clientes_por_ciudad() que devuelva un diccionario 
# {"Guayaquil": ["Ana", "Luis"], "Quito": ["Sol"]}.

def clientes_por_ciudad(clientes):
    resultado = {}

    for cliente in clientes:
        ciudad = cliente["ciudad"]
        nombre = cliente["nombre"]

        if ciudad not in resultado:
            resultado[ciudad] = []

        resultado[ciudad].append(nombre)

    return resultado