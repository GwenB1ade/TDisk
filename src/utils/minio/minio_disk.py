import io
from minio import Minio
from config import settings


class MinioStorageClient:
    bname = 'disk'
    http_or_https = 'http'
    url = f'{http_or_https}://{settings.MINIO_URL}/{bname}'

    
    def __init__(self):
        self.minio = Minio(
            endpoint = settings.MINIO_URL,
            access_key = settings.MINIO_ACCESS_KEY,
            secret_key = settings.MINIO_SECRET_KEY,
            secure = False,
            cert_check = False,
        )
        if not self.minio.bucket_exists(self.bname):
            self.minio.make_bucket(self.bname)

 
    def create_storage(self, uuid: str, storage_name: str):
        empty_data = io.BytesIO(b"")
        self.minio.put_object(self.bname, f'{uuid}/{storage_name}/.ignore.md', data = empty_data, length = 0)
        return f'{self.url}/{uuid}/{storage_name}'
    

    def add_object_in_storage(self, uuid: str, storage_name: str, object_name: str, object_data: str, object_lenght: int):
        self.minio.put_object(self.bname, f'{uuid}/{storage_name}/{object_name}', data = object_data, length = object_lenght)
        return f'{self.url}/{uuid}/{storage_name}/{object_name}'
    

    def get_objects_urls_from_storage(self, uuid: str, storage_name: str):
        objects = self.minio.list_objects(self.bname, f'{uuid}/{storage_name}/', recursive = True, fetch_owner = True)
        obj_dict = {}
        for obj in objects:
            object_name = obj.object_name.split('/')[-1]
            if object_name != '.ignore.md':
                obj_dict.update({
                    object_name: f'{self.url}/{uuid}/{storage_name}/{object_name}'
                })
        
        return obj_dict
    
    
    def get_object(self, uuid: str, storage_name: str, file_name: str):
        url = f'{self.url}/{uuid}/{storage_name}/{file_name}'
        return url
    
    
    def delete_storage(self, uuid: str, storage_name: str):
        self.minio.remove_object(self.bname, f'{uuid}/{storage_name}')
        objects = self.minio.list_objects(self.bname, prefix = f'{uuid}/{storage_name}/')
        for obj in objects: 
            self.minio.remove_object(self.bname, obj.object_name)
        
        
    def delete_object(self, uuid: str, storage_name: str, object_name: str):
        self.minio.remove_object(self.bname, f'{uuid}/{storage_name}/{object_name}')
        
    def get_storage_url_by_name(self, uuid: str, storage_name: str):
        url = f'{self.url}/{uuid}/{storage_name}'
        return url
    
    
    def get_total_objects_size(self, uuid: str):
        total_size = 0
        objects = self.minio.list_objects(
            bucket_name = self.bname,
            prefix = uuid,
            recursive = True
        )
        
        for obj in objects:
            total_size += obj.size

        return total_size
    
    
    def check_object(self, uuid: str, storage_name: str, object_name: str,) -> bool:
        list_objects = self.minio.list_objects(
            self.bname,
            prefix = f'{uuid}/{storage_name}/'
        )
        

        for obj in list_objects:
            print(obj.object_name)
            if f'{uuid}/{storage_name}/{object_name}' == obj.object_name:
                return True

        return False
    
    
        
        
  
        

