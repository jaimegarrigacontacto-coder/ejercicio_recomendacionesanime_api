class User:
    def __init__(self, username, password, iduser = None):
        self.__iduser = iduser
        self.setUsername(username)
        self.setPassword(password)
    
    def setUsername(self, username):
        self.__username = username

    def setPassword(self, password):
        self.__password = password

    def getUsername(self):
        return self.__username
    
    def getPassword(self):
        return self.__password
    
    def getId(self):
        return self.__iduser
    
    def to_dict(self):
        return {
            'iduser': self.__iduser,
            'username': self.__username,
            'password': self.__password,
        }