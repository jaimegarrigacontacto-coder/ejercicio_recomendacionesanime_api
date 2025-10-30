class Anime:
    def __init__(self, anime, rating):
        self.setAnime(anime)
        self.setRating(rating)
    
    def setUsername(self, anime):
        self.__anime = anime

    def setPassword(self, rating):
        self.__rating = rating