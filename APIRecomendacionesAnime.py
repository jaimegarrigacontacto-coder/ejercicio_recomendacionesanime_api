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

@app.route("/create", methods=["POST"])
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

@app.route('/selectAll', methods=['GET'])
def get_todo():
    consulta = myDAO.consultaSelectAll()
    resultado = [user.to_dict() for user in consulta]
    return jsonify(resultado)

@app.route("/update", methods=["PUT", "POST"])
def update_user():
    data = request.get_json()
    nombreIndex = data['nombreIndex']
    nuevoUsername = data['nuevoUsername']
    nuevoPassword = data['nuevoPassword']

    filas = myDAO.actualizarUser(
        User(nuevoUsername, nuevoPassword),
        nombreIndex
    )

    return jsonify({"updated": filas})

@app.route("/user/<int:id>", methods=["GET"])
def get_user_por_id(id):
    try:
        user = myDAO.obtenerPorId(User("", "", id))
        
        if user is None:
            return jsonify({"error": "User no encontrado"}), 404
        
        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user_por_id(id):
    try:
        filas = myDAO.borrarUserPorId(User("", "", id))
        if filas == 0:
            return jsonify({"error": "User no encontrado"}), 404
        return jsonify({"deleted": filas, "id": id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)