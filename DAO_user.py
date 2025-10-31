import mysql.connector
from user import User

class DAOUser:
    def __init__(self, host, user, password):
        self.setHost(host)
        self.setUser(user)
        self.setPassword(password)
        self.setDatabase()
        self.setCursor()

    def setAñadir(self, user):
        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
        valores = (user.getUsername(), user.getPassword())
        self.getCursor().execute(sql, valores)
        self.getDatabase().commit()
        return self.getCursor().rowcount
    
    def obtenerUsuario(self, user):
        sql = "SELECT * FROM user WHERE username = %s AND password = %s"
        valores = (user.getUsername(),user.getPassword())
        self.getCursor().execute(sql, valores)
        fila = self.getCursor().fetchone()
        userConsulta = User(fila[1], fila[2], fila[0])
        return userConsulta
    
    def obtenerPorUsername(self, username):
        sql = "SELECT * FROM user WHERE username = %s"
        valores = (username,)
        self.getCursor().execute(sql, valores)
        fila = self.getCursor().fetchone()
        if fila is None:
            return None
        userConsulta = User(fila[1], fila[2], fila[0])
        return userConsulta

    def setHost(self, host):
        self.__host = host

    def getHost(self):
        return self.__host

    def setUser(self, user):
        self.__user = user

    def getUser(self):
        return self.__user

    def setPassword(self, password):
        self.__password = password

    def getPassword(self):
        return self.__password

    def setDatabase(self):
        self.__database = mysql.connector.connect(
                host=self.getHost(),
                user=self.getUser(),
                password=self.getPassword(),
                database="login")

    def getDatabase(self):
        return self.__database

    def setCursor(self):
        self.__cursor = self.getDatabase().cursor()

    def getCursor(self):
        return self.__cursor
    
    
