class User:
    def __init__(self, username, password):
        self.setUsername(username)
        self.setPassword(password)
    
    def setUsername(self, username):
        self.__username = username

    def setPassword(self, password):
        self.__password = password