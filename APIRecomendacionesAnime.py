from flask import Flask, jsonify, request
from DAO_user import *
import pandas as pd
from conexion import iniciar_conexion
import pickle
import os
from model import *

FILE_PATH = "C:/Users/Tarda/Documents/datasets/"
corr_matrix_path = f"{FILE_PATH}corrMatrix.pkl"

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
    global corrMatrix
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

@app.route("/retrain", methods=["POST"])
def retrain_model():
    global corrMatrix
    try:
        print("Iniciando reentrenamiento del modelo...")
        corrMatrix = trainModel(FILE_PATH, corr_matrix_path)
        return jsonify({
            "success": True,
            "message": "Modelo reentrenado exitosamente",
            "matrix_size": corrMatrix.shape
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
            corrMatrix = trainModel(FILE_PATH, corr_matrix_path)

    except Exception as e:
        print(f"Error cargando datos: {e}")
        corrMatrix = None

    print("¡Servidor operativo!")
    app.run(debug=True, use_reloader=False)