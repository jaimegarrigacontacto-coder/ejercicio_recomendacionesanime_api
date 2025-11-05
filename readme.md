Instrucciones para ejecutar recomendacionesanime_api

Primero crear una carpeta con los dataset de animes. Copiar y pegar la ruta en el servidor. Aqui se generará la matriz en caso de no existir.
Segundo importa el archivo sql en tu workbench para tener lista tu tabla users.
Tercero iniciar el servidor (APIRecomendacionesAnime) y luego el cliente (main).

Para el correcto funcionamiento del servidor importar los siguientes módulos en caso que no se tengan.

-os
-pickle
-pandas
-flask
-requests

El servidor puede tardar en iniciarse unos 4 minutos si no existe una matriz de correlaciones en la ruta especificada. En caso de que no exista, crea una. El servidor se aloja en 127.0.0.1:5000 por defecto.

Una vez el cliente está abierto identificate con el usuario y contraseña de tu BBDD. Aquí puedes crear usuarios nuevos o entrar con un usuario ya registrado en tu BBDD.

El programa tiene 4 funciones:
1- Añadir ratings: añade 1 o más animes y ratings para preparar tus recomendaciones.
2- Ver recomendaciones: devuelve 20 animes recomendados y su indice de correlación en función a los animes introducidos.
3- Entrenar algoritmo: vuelve a calcular la matriz de correlación en caso de que hayan cambios en los archivos csv o en las intrucciones.
4- Testear algoritmo: ejecuta la opción 2 pero sobre unos datos estáticos.




