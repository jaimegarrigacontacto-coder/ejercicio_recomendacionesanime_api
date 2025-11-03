from flask import Flask, jsonify, request
import pandas as pd
import pickle

def trainModel(FILE_PATH, corr_matrix_path):
    # Load your data
        ratings = pd.read_csv(f"{FILE_PATH}rating.csv")
        anime = pd.read_csv(f"{FILE_PATH}anime.csv")
        print("Archivos CSV cargados")

        # Apply filters
        print("Aplicando filtros...")
        anime = anime[(anime.type == 'TV') | (anime.type == 'ONA')]
        anime = anime[~anime['genre'].str.contains('Hentai', case=False, na=False)]
        ratings = ratings[ratings.rating != -1]

        # Merge and pivot
        print("Creando tabla pivot...")
        merged = pd.merge(ratings, anime[['anime_id', 'name']], on='anime_id', how='inner')
        userRatings = merged.pivot_table(index='user_id', columns='name', values='rating')

        # Compute correlation matrix
        print("Calculando matriz de correlación...")
        min_ratings = 30
        valid_users = userRatings.count(axis=1) >= min_ratings
        corrMatrix = userRatings[valid_users].corr(method='pearson', min_periods=500)

        print("Matriz de correlación calculada")
        print(f"Tamaño de la matriz: {corrMatrix.shape}")

        # Save it for next time
        with open(corr_matrix_path, "wb") as f:
            pickle.dump(corrMatrix, f)

        print("¡Matrix de correlación guardada correctamente!")
        
        return corrMatrix
        