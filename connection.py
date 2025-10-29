import mysql.connector

class DAOLogin:
    def __init__(self, host, user, password):
        self.setHost(host)
        self.setUser(user)
        self.setPassword(password)
        self.setDatabase()
        self.setCursor()

    def setDatabase(self):
        self.__database = mysql.connector.connect(
                host=self.getHost(),
                user=self.getUser(),
                password=self.getPassword(),
                database="login")
        
    def getDatabase(self):
        return self.__database
        
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
    
    def setCursor(self):
        self.__cursor = self.getDatabase().cursor()

    def getCursor(self):
        return self.__cursor
