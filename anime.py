class Anime:
    def __init__(self, anime, rating):
        self.setAnime(anime)
        self.setRating(rating)
    
    def setAnime(self, anime):
        self.__anime = anime

    def setRating(self, rating):
        self.__rating = rating

    def getAnime(self):
        return self.__anime
    
    def getRating(self):
        return self.__rating