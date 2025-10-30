from APIRecomendacionesAnime import *
import requests

opcion = None

host = "localhost"
root = input("Introduce el usuario: ")
password = input("Introduce la contraseña: ")
iniciar_conexion(host, root, password)

while opcion != 0:
    print("\n1- Añadir user\n2- Actualizar user\n3- Ver users\n4- Borrar user\n0- Salir")
    opcion = input("\nSelecciona opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        print("Error. Opción no válida.")
        continue

    if opcion == 1:
        username = input("Inserta username: ")
        password = input("Inserta password: ")
        datos = {'username': username, 'password': password}
        res = requests.post('http://localhost:5000/create', json=datos)
        print(res.json())

    elif opcion == 2:
        usernameIndex = input("Inserta el username a actualizar: ")
        nuevoUsername = input("Nuevo username: ")
        nuevoPassword = input("Nuevo password: ")

        datos = {
            "nombreIndex": usernameIndex,
            "nuevoUsername": nuevoUsername,
            "nuevoPassword": nuevoPassword
        }
        res = requests.post('http://localhost:5000/update', json=datos)
        print(res.json())

    elif opcion == 3:
        res = requests.get("http://localhost:5000/selectAll")
        try:
            print(res.json())
        except Exception:
            print("Respuesta no válida:", res.text)

    elif opcion == 4:
        try:
            id_user = int(input("Introduce el ID del user a borrar: "))
            res = requests.delete(f"http://localhost:5000/user/{id_user}")
            
            if res.status_code == 200:
                print("User eliminado:", res.json())
            elif res.status_code == 404:
                print("User no encontrado")
            else:
                print(f"Error {res.status_code}: {res.text}")

        except ValueError:
            print("ID inválido, debe ser un número entero")
        except requests.exceptions.RequestException as e:
            print("Error de conexión:", e)

    elif opcion == 0:
        print("Saliendo del programa...")