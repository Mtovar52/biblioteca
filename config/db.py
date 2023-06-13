import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener los valores de las variables de entorno
db_driver = os.getenv('DB_DRIVER')
db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


engine = create_engine(f'{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

meta_data = MetaData()