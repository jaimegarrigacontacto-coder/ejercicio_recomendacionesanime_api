# Instrucciones para ejecutar recomendacionesanime_api

1. Crear una carpeta con los datasets de animes y ratings. Copiar y pegar la ruta en el archivo ```APIRecomendaciones.py```. En el directorio se guardará la matriz en caso de no existir.
2. Importa el archivo sql en tu workbench para tener lista la tabla users.
3. Iniciar el servidor ```APIRecomendacionesAnime.py``` y luego el cliente ```main.py```.

El servidor puede tardar en iniciarse unos 4 minutos si no existe una matriz de correlaciones en la ruta especificada. En caso de que no exista, se crea una. El servidor se aloja en ```127.0.0.1:5000``` por defecto.

## Dependencias necesarias
Para el correcto funcionamiento del servidor descargar las siguientes librerias en caso que no se tengan.

```
pip install pandas
pip install Flask
pip install requests
```

## Funcionamiento del cliente

Una vez el cliente está abierto identificate con el usuario y contraseña de tu BBDD. Aquí puedes crear usuarios nuevos o entrar con un usuario ya registrado en tu BBDD.

El programa tiene 4 funciones:
1. Añadir ratings: añade 1 o más animes y ratings para preparar tus recomendaciones.
2. Ver recomendaciones: devuelve 20 animes recomendados y su indice de correlación en función a los animes introducidos.
3. Entrenar algoritmo: vuelve a calcular la matriz de correlación en caso de que hayan cambios en los archivos csv o en las intrucciones.
4. Testear algoritmo: ejecuta la opción 2 pero sobre unos datos estáticos.




