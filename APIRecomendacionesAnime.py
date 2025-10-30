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

if __name__ == "__main__":
    app.run(debug=True)