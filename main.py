from conexion import iniciar_conexion
import requests

login = None
opcion = None
session = requests.Session()

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
        res = session.post('http://localhost:5000/login', json=datos)
        
        respuesta = res.json()
        
        if res.status_code == 200 and respuesta.get("success"):
            print(f"¡Bienvenido/a!")
            login = 0
        else:
            print("Error")

    elif login == 2:
        nuevoUsername = input("Nuevo username: ")
        nuevoPassword = input("Nuevo password: ")

        datos = {
            "username": nuevoUsername,
            "password": nuevoPassword
        }

        try:
            res = session.post('http://localhost:5000/register', json=datos)
            print(res.json())
        except Exception as e: 
            print(f"Error al registrarse: {e}. Usuario ya existente.")

    elif login == 0:
        opcion = 0

user_ratings = {}

while opcion != 0:
    print("\n1- Añadir ratings\n2- Ver recomendaciones\n3- Entrenar modelo\n4- Testear modelo\n0- Salir")
    opcion = input("\nSelecciona opción: ")
    if opcion.isdigit():
        opcion = int(opcion)
    else:
        print("Error. Opción no válida.")
        continue

    if opcion == 1:
        print("\n--- Añadir Rating ---")
        anime_name = input("Nombre del anime: ")
        try:
            rating = float(input("Rating (1-10): "))
            if 1 <= rating <= 10:
                user_ratings[anime_name] = rating
                print(f"Rating añadido: {anime_name} - {rating}")
            else:
                print("El rating debe estar entre 1 y 10")
        except ValueError:
            print("Rating debe ser un número")
            
    elif opcion == 2:
        if not user_ratings:
            print("Primero añade algunos ratings")
            continue
            
        print(f"\nTus ratings: {user_ratings}")
        print("Generando recomendaciones!")
        
        datos = {'ratings': user_ratings}
        res = session.post('http://localhost:5000/recommend', json=datos)
        
        if res.status_code == 200:
            respuesta = res.json()
            recommendations = respuesta.get('recommendations', {})
            
            print("\nTus recomendaciones: ")
            for i, (anime, score) in enumerate(recommendations.items(), 1):
                print(f"{i}. {anime}: {score:.2f}")
        else:
            print(f"Error: {res.json()}")

    elif opcion == 3:
        print("\n--- Entrenar Modelo ---")
        print("Reentrenando el modelo de recomendación... (Esto puede tardar varios minutos)")
        
        try:
            res = session.post('http://localhost:5000/retrain')
            
            if res.status_code == 200:
                respuesta = res.json()
                print(f"¡Modelo reentrenado exitosamente!")
                print(f"Tamaño de la nueva matriz: {respuesta.get('matrix_size')}")
            else:
                error_msg = res.json().get('error', 'Error desconocido')
                print(f"Error al reentrenar el modelo: {error_msg}")
                
        except Exception as e:
            print(f"Error de conexión: {e}")

    elif opcion == 4:
        print("\n--- Testear Modelo ---")
        print("Generando recomendaciones con datos de prueba...")
        
        test_ratings = {
            "Hunter x Hunter (2011)": 10.0,
            "School Days": 1.0
        }
        
        print(f"Datos de prueba: {test_ratings}")
        print("Generando recomendaciones!")
        
        datos = {'ratings': test_ratings}
        res = session.post('http://localhost:5000/recommend', json=datos)
        
        if res.status_code == 200:
            respuesta = res.json()
            recommendations = respuesta.get('recommendations', {})
            
            print("\nRecomendaciones del test: ")
            for i, (anime, score) in enumerate(recommendations.items(), 1):
                print(f"{i}. {anime}: {score:.2f}")
        else:
            print(f"Error: {res.json()}")

    elif opcion == 0:
        print("Saliendo del programa...")