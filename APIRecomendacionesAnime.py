from flask import Flask, jsonify, request
from DAO_user import *
import pandas as pd
from conexion import iniciar_conexion
import pickle
import os

corr_matrix_path = "C:/Users/Tarda/Documents/datasets/corrMatrix.pkl"
FILE_PATH = "C:/Users/Tarda/Documents/datasets/"

app = Flask(__name__)
app.json.sort_keys = False

myDAO = None
corrMatrix = None

@app.route("/")
def hola_mundo():
    return "Hola Mundo"

@app.route("/register", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    filas = myDAO.setAñadir(User(username, password))

    return jsonify({
        "inserted": filas,
        "username": username,
        "password": password,
    })

@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    try:
        user = myDAO.obtenerPorUsername(username)
        
        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        if user.getPassword() == password:
            return jsonify({
                "success": True,
                "message": "Login exitoso",
                "user": user.to_dict()
            }), 200
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/recommend", methods=["POST"])
def get_recommendations():
    try:
        data = request.get_json()
        user_ratings = data['ratings']
        
        myRatings = pd.Series(user_ratings)
        simCandidates = pd.Series()
        
        for anime_name, rating in myRatings.items():
            if anime_name in corrMatrix.columns:
                sims = corrMatrix[anime_name].dropna()
                sims = sims.map(lambda x: x * rating)
                simCandidates = pd.concat([simCandidates, sims])
        
        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates.sort_values(inplace=True, ascending=False)
        filteredSims = simCandidates.drop(myRatings.index, errors='ignore')
        recommendations = filteredSims.head(20).to_dict()
        
        return jsonify({
            "success": True,
            "recommendations": recommendations
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Inicializando servidor")
    myDAO = iniciar_conexion("localhost", "root", "123456")

    try:
        if os.path.exists(corr_matrix_path):
            print("Cargando matrix de correlación ya existente...")
            with open(corr_matrix_path, "rb") as f:
                corrMatrix = pickle.load(f)
            print("¡Se ha cargado correctamente!")
            print(f"Tamaño de la matriz: {corrMatrix.shape}")

        else:
            print("Matrix de correlación no encontrada, entrenando modelo... (Esto puede tardar varios minutos.)")

            # Load your data
            ratings = pd.read_csv(f"{FILE_PATH}rating.csv")
            anime = pd.read_csv(f"{FILE_PATH}anime.csv")
            print("Archivos CSV cargados")

            # Apply filters
            print("Aplicando filtros...")
            anime = anime[(anime.type == 'TV') | (anime.type == 'ONA')]
            anime = anime[~anime['genre'].str.contains('Hentai', case=False, na=False)]
            ratings = ratings[ratings.rating != -1]

            # Merge and pivot
            print("Creando tabla pivot...")
            merged = pd.merge(ratings, anime[['anime_id', 'name']], on='anime_id', how='inner')
            userRatings = merged.pivot_table(index='user_id', columns='name', values='rating')

            # Compute correlation matrix
            print("Calculando matriz de correlación...")
            min_ratings = 30
            valid_users = userRatings.count(axis=1) >= min_ratings
            corrMatrix = userRatings[valid_users].corr(method='pearson', min_periods=500)

            print("Matriz de correlación calculada")
            print(f"Tamaño de la matriz: {corrMatrix.shape}")

            # Save it for next time
            with open(corr_matrix_path, "wb") as f:
                pickle.dump(corrMatrix, f)

            print("Correlation matrix saved successfully!")

    except Exception as e:
        print(f"Error cargando datos: {e}")
        corrMatrix = None

    print("¡Servidor operativo!")
    app.run(debug=True, use_reloader=False)
