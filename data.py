import pandas as pd
import numpy as np
from config import DATA_PATHS, MODEL_CONFIG

class DataLoader:
    def __init__(self):
        self.ratings = None
        self.anime = None
        self.merged_data = None
        self.user_ratings_matrix = None
        
    def load_data(self):
        """Carga y procesa los datos iniciales - CÓDIGO DEL NOTEBOOK"""
        try:
            # Cargar datos (del notebook)
            self.ratings = pd.read_csv(DATA_PATHS['rating'])
            self.anime = pd.read_csv(DATA_PATHS['anime'])
            
            print("Datos cargados exitosamente")
            return True
            
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return False
    
    def filter_data(self):
        """Filtra los datos según la configuración - CÓDIGO DEL NOTEBOOK"""
        if self.anime is None or self.ratings is None:
            raise ValueError("Los datos deben ser cargados primero")
        
        # FILTRADO DEL NOTEBOOK
        # Filtrar animes por tipo (TV o ONA)
        self.anime = self.anime[(self.anime.type == 'TV') | (self.anime.type == 'ONA')]
        
        # Filtrar géneros prohibidos (Hentai)
        self.anime = self.anime[~self.anime['genre'].str.contains('Hentai', case=False, na=False)]
        
        # Filtrar ratings inválidos
        self.ratings = self.ratings[self.ratings.rating != -1]
        
        # Merge de datos (igual que en el notebook)
        self.merged_data = pd.merge(
            self.ratings, 
            self.anime[['anime_id', 'name']], 
            on='anime_id', 
            how='inner'
        )
        
        self._print_stats()
    
    def _print_stats(self):
        """Imprime estadísticas de los datos filtrados - CÓDIGO DEL NOTEBOOK"""
        print(f"Unique anime after filtering: {self.anime['name'].nunique()}")
        print(f"Unique anime in ratings: {self.ratings['anime_id'].nunique()}")
        
        common_anime = set(self.anime['anime_id']).intersection(set(self.ratings['anime_id']))
        print(f"Number of anime with ratings and matching filtered anime: {len(common_anime)}")
    
    def create_user_ratings_matrix(self):
        """Crea la matriz de ratings de usuarios - CÓDIGO DEL NOTEBOOK"""
        if self.merged_data is None:
            raise ValueError("Los datos deben ser filtrados primero")
            
        # EXACTAMENTE COMO EN EL NOTEBOOK
        self.user_ratings_matrix = self.merged_data.pivot_table(
            index='user_id', 
            columns='name', 
            values='rating'
        )
        
        print(f"Matriz de usuarios-animes creada: {self.user_ratings_matrix.shape}")
        return self.user_ratings_matrix
    
    def get_available_anime(self):
        """Retorna la lista de animes disponibles"""
        if self.anime is None:
            return []
        
        return self.anime[['anime_id', 'name', 'genre', 'type']].to_dict('records')