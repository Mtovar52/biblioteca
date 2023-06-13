# BIBLIOTECA


framework: FastApi

Lenguaje: Python

Documentacion: https://fastapi.tiangolo.com/

Reto: servicio de biblioteca, consulta de libros en db interna y externa Api de google books + open library

#El archivo requirements.txt contiene todas las dependencias usadas en este proyecto
para acceder a ellas usa el comando:

pip install -r requirements.txt

#Puedes hacer el paso anterior dentro de un entorno virtual:

python -m venv venv

#para acceder al entorno virtual usa la ruta:  

env\Scripts\activate 

#Debes crear un archivo  .env  en el guarda los siguientes valores para la conexion a la DB:

DB_DRIVER=mysql+pymysql 

DB_NAME=biblioteca 

DB_USERNAME=su_usuario 

DB_PASSWORD=su_password 

DB_HOST=localhost 

DB_PORT=3306 

COMANDOS:

uvicorn main:app --reload   #### correr el servidor 

pip freeze > requirements.txt  ### para guardar nuevas dependencias


# LIBRARY

framework: FastApi

Language: Python

Documentation: https://fastapi.tiangolo.com/

Challenge: library service, consultation of books in internal and external db Google Books API + open library

#The requirements.txt file contains all the dependencies used in this project.
To access them use the command:

pip install -r requirements.txt

#You can do the previous step inside a virtual environment

python -m venv venv

#to access the virtual environment use the path:   

env\Scripts\activate 

#You must create an .env file in which it saves the following values for the connection to the DB

DB_DRIVER=mysql+pymysql

DB_NAME=name_library

DB_USERNAME= xxxxx

DB_PASSWORD= xxxxx

DB_HOST=localhost

DB_PORT=3306

COMMANDS:

uvicorn main:app --reload   #### run serverr 

pip freeze > requirements.txt  ### to save new dependencies
