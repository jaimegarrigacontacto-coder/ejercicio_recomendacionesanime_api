from APIRecomendacionesAnime import *
import requests

login = None
opcion = None

host = "localhost"
root = input("Introduce el usuario: ")
password = input("Introduce la contraseña: ")
iniciar_conexion(host, root, password)

while login != 0:
    print("\n1- Iniciar sesión\n2- Registrarse\n0- Salir")
    login = input("\nSelecciona opción: ")
    if login.isdigit():
        login = int(login)
    else:
        print("Error. Opción no válida.")
        continue

    if login == 1:
        username = input("Inserta tu username: ")
        password = input("Inserta password: ")
        datos = {'username': username, 'password': password}
        res = requests.post('http://localhost:5000/login', json=datos)
        print(res.json())

    elif login == 2:
        nuevoUsername = input("Nuevo username: ")
        nuevoPassword = input("Nuevo password: ")

        datos = {
            "username": nuevoUsername,
            "password": nuevoPassword
        }

        try:
            res = requests.post('http://localhost:5000/register', json=datos)
            print(res.json())
        except Exception as e: print(f"Error al registrarse. Nombre de usuario ya está en uso: {e}")

    elif login == 0:
        opcion = 0
    

while opcion != 0:
    print("1- Añadir ratings\n2- Ver recomendaciones")
    opcion = input("\nSelecciona opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        print("Error. Opción no válida.")
        continue

    if opcion == 0:
        print("Saliendo del programa...")