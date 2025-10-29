from connection import *

opcion = None
login = None

host = "localhost"
root = input("Introduce el usuario: ")
password = input("Introduce la contraseña: ")

myDB = Connection(host, root, password)

while login != 0:
    print("\n LOGIN: RECOMENDACIONES ANIME\n--------------\n1. Iniciar sesión\n2. Registrarse\n0. Salir")
    login = input("\nSelecciona opción: ")
    if login.isdigit():
        login = int(login)
    else:
        print("Error. Opción no válida.")
        continue

    if login == 0:
        print("Saliendo del programa...")
        opcion = 0


while opcion != 0:
    print("\n1- Añadir valoración anime\n2- Recomendaciones")
    opcion = input("\nSelecciona opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        print("Error. Opción no válida.")
        continue

    if opcion == 0:
        print("Saliendo del programa...")
