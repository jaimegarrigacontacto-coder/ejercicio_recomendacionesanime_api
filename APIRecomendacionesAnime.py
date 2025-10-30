from flask import Flask, jsonify, request
from DAO_user import *

myDAO = None
myDAO = DAOUser("localhost", "root", "123456")

def iniciar_conexion(host, root, password):
     global myDAO
     myDAO = DAOUser(host, root, password)

app = Flask(__name__)
app.json.sort_keys = False

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

if __name__ == "__main__":
    app.run(debug=True)