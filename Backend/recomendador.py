import pandas as pd

class Recomendador:
    def __init__(self, matrix):
        self.matrix = matrix
        
    def recomendar(self, user_ratings):
        myRatings = pd.Series(user_ratings)
        simCandidates = pd.Series()
        
        for anime_name, rating in myRatings.items():
            if anime_name in self.matrix.columns:
                sims = self.matrix[anime_name].dropna()
                sims = sims.map(lambda x: x * rating)
                simCandidates = pd.concat([simCandidates, sims])
        
        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates.sort_values(inplace=True, ascending=False)
        filteredSims = simCandidates.drop(myRatings.index, errors='ignore')
        
        return filteredSims.head(20).to_dict()
        