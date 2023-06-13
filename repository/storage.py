from google.cloud import storage
import uuid

class GCSImageRepository:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def set_file(self, image_url, route_sprintf):
        try:
            # Generar un nombre aleatorio para el archivo
            random_name = route_sprintf % str(uuid.uuid4())

            # Obtener el bucket
            bucket = self.client.bucket(self.bucket_name)

            # Crear un objeto Blob en el bucket
            blob = bucket.blob(random_name)

            # Establecer las opciones del objeto
            blob.cache_control = "no-cache, max-age=0"

            # Establecer la URL del objeto
            blob.upload_from_string("", content_type="image/jpeg")
            blob.make_public()

            # Generar la URL del objeto
            image_url = f"https://storage.googleapis.com/{self.bucket_name}/{random_name}"

            return image_url
        
        except Exception as e:
            print(f"Error al subir el archivo: {str(e)}")
        
        return None
    def delete_file(self, route_sprintf, name):
        try:
            # Obtener el nombre completo del objeto
            object_name = route_sprintf % name

            # Obtener el bucket
            bucket = self.client.bucket(self.bucket_name)

            # Obtener el objeto
            blob = bucket.blob(object_name)

            # Eliminar el objeto
            blob.delete()
            
        except Exception as e:
            print(f"Error al eliminar el archivo: {str(e)}")
    
    def new_update_file(self, request_house):
        # Implementa aquí la lógica para generar una estructura de datos de actualización de archivo
        pass
