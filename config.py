# Configuración de rutas de datos (ACTUALIZAR CON TUS RUTAS)
DATA_PATHS = {
    'rating': 'C:\\Users\\Tarda\\Documents\\datasets\\rating.csv',  # Ruta del notebook
    'anime': 'C:\\Users\\Tarda\\Documents\\datasets\\anime.csv'     # Ruta del notebook
}

# Configuración del modelo (PARÁMETROS DEL NOTEBOOK)
MODEL_CONFIG = {
    'min_user_ratings': 30,           # Del notebook: min_ratings = 30
    'min_correlation_periods': 500,   # Del notebook: min_periods=500
    'correlation_method': 'pearson',  # Del notebook: method='pearson'
    'allowed_types': ['TV', 'ONA'],   # Del notebook: (anime.type == 'TV') | (anime.type == 'ONA')
    'banned_genres': ['Hentai']       # Del notebook: ~anime['genre'].str.contains('Hentai')
}

# Configuración de la API
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}