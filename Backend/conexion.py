from Frontend.DAO_user import DAOUser

myDAO = None

def iniciar_conexion(host, root, password):
    global myDAO
    myDAO = DAOUser(host, root, password)
    return myDAO
