import pandas as pd
import numpy as np
from config import MODEL_CONFIG

class AnimeRecommender:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.user_ratings = None
        self.corr_matrix = None
        self.trained = False
        
    def prepare_data(self):
        """Prepara los datos para el entrenamiento"""
        print("Preparando datos...")
        self.user_ratings = self.data_loader.create_user_ratings_matrix()
        print(f"Matriz de ratings creada: {self.user_ratings.shape}")
        
    def train(self):
        """Entrena el modelo de recomendación - CÓDIGO DEL NOTEBOOK"""
        if self.user_ratings is None:
            self.prepare_data()
        
        print("Entrenando modelo...")
        
        # CÓDIGO EXACTO DEL NOTEBOOK
        # Excluir usuarios con menos de 30 ratings
        min_ratings = MODEL_CONFIG['min_user_ratings']
        valid_users = self.user_ratings.count(axis=1) >= min_ratings

        # Calcular matriz de correlación (igual que en el notebook)
        self.corr_matrix = self.user_ratings[valid_users].corr(
            method=MODEL_CONFIG['correlation_method'],
            min_periods=MODEL_CONFIG['min_correlation_periods']
        )
        
        self.trained = True
        print(f"Modelo entrenado. Matriz de correlación: {self.corr_matrix.shape}")
        
    def get_recommendations(self, user_ratings_dict, n_recommendations=10):
        """Obtiene recomendaciones basadas en ratings de usuario - ALGORITMO DEL NOTEBOOK"""
        if not self.trained:
            raise ValueError("El modelo debe ser entrenado primero")
        
        if not user_ratings_dict:
            raise ValueError("Se requieren ratings de usuario")
        
        print(f"Generando recomendaciones para {len(user_ratings_dict)} animes...")
        
        # ALGORITMO EXACTO DEL NOTEBOOK
        simCandidates = pd.Series()
        
        for anime_name, rating in user_ratings_dict.items():
            if anime_name in self.corr_matrix.columns:
                print(f"Añadiendo animes similares a {anime_name}...")
                
                # Recuperar animes similares
                sims = self.corr_matrix[anime_name].dropna()
                
                # Escalar la similaridad multiplicando por el rating
                sims = sims.map(lambda x: x * rating)
                
                # Añadir a candidatos
                simCandidates = pd.concat([simCandidates, sims])
            else:
                print(f"Advertencia: Anime '{anime_name}' no encontrado en el modelo")
        
        if simCandidates.empty:
            return []
        
        print("Ordenando...")
        
        # Agrupar por anime y sumar scores (igual que en el notebook)
        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates.sort_values(inplace=True, ascending=False)
        
        # Filtrar animes ya calificados
        filteredSims = simCandidates.drop(user_ratings_dict.keys(), errors='ignore')
        
        # Obtener top recomendaciones
        top_recommendations = filteredSims.head(n_recommendations)
        
        # Formatear resultados
        result = []
        for anime_name, score in top_recommendations.items():
            result.append({
                'name': anime_name,
                'score': round(float(score), 4)
            })
        
        return result
    
    def get_specific_user_recommendations(self, user_id, n_recommendations=10):
        """Obtiene recomendaciones para un usuario específico - COMO EN EL NOTEBOOK"""
        if not self.trained:
            raise ValueError("El modelo debe ser entrenado primero")
        
        # Obtener ratings del usuario (como en el notebook para user_id=0)
        user_ratings = self.user_ratings.loc[user_id].dropna()
        
        print(f"Ratings del usuario {user_id}:")
        print(user_ratings)
        
        # Usar el mismo algoritmo de recomendación
        return self.get_recommendations(user_ratings.to_dict(), n_recommendations)
    
    def test_recommendation(self):
        """Realiza una prueba básica del sistema - USANDO DATOS DEL NOTEBOOK"""
        # Usar los mismos datos de prueba del notebook
        test_ratings = {
            'Hunter x Hunter (2011)': 10.0,
            'School Days': 1.0
        }
        
        try:
            recommendations = self.get_recommendations(test_ratings, 5)
            return {
                'status': 'success',
                'test_ratings': test_ratings,
                'recommendations': recommendations
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }