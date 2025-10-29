from connection import *

opcion = None

host = "localhost"
root = input("Introduce el usuario: ")
password = input("Introduce la contraseña: ")

myDB = Connection(host, root, password)

while opcion != 0:
    print("\n1- Añadir anime\n2- Recomendaciones")
    opcion = input("\nSelecciona opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        print("Error. Opción no válida.")
        continue

    if opcion == 0:
        print("Saliendo del programa...")
