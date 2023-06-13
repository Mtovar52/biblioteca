from firebase_admin import storage as firebase_storage
import uuid


class FirebaseImageRepository:
    def __init__(self, bucket_name):
        self.bucket = firebase_storage.bucket(bucket_name)

    def set_file(self, image_path, route_sprintf):
        try:
            # Generar un nombre aleatorio para el archivo
            random_name = route_sprintf % str(uuid.uuid4())

            # Obtener una referencia al archivo en Firebase Storage
            blob = self.bucket.blob(random_name)

            # Cargar el archivo en Firebase Storage
            blob.upload_from_filename(image_path)

            # Establecer la URL del archivo
            blob.make_public()
            image_url = blob.public_url

            return image_url
        
        except Exception as e:
            print(f"Error al subir el archivo: {str(e)}")
        
        return None

    def delete_file(self, route_sprintf, name):
        try:
            # Obtener el nombre completo del objeto
            object_name = route_sprintf % name

            # Obtener el objeto
            blob = self.bucket.blob(object_name)

            # Eliminar el objeto
            blob.delete()
            
        except Exception as e:
            print(f"Error al eliminar el archivo: {str(e)}")
    
    def new_update_file(self, request_house):
        # Implementa aquí la lógica para generar una estructura de datos de actualización de archivo
        pass