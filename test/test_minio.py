import io
import pytest

def test_minio_connect():
    try:
        from src.utils.minio.minio_disk import MinioStorageClient
        from src.utils.minio import minio_storage
    
    except:
        raise Exception('It is impossible to connect to the Minio server')
    
 
@pytest.mark.parametrize(
    'uuid, storage_name, object_name, object_data, object_len',
    [
        ('test_uuid', 'test_storage', 'object_name.md', io.BytesIO(b"hello"), len('hello'))
    ]
)   
def test_minio_file_func(
    uuid: str,
    storage_name: str,
    object_name: str,
    object_data: str,
    object_len: int,
):
    try:
        from src.utils.minio import minio_storage
        minio_storage.add_object_in_storage(
            uuid = uuid,
            storage_name = storage_name,
            object_name = object_name,
            object_data = object_data,
            object_lenght = object_len,
        )
        
        minio_storage.delete_object(
            uuid = uuid,
            object_name = object_name,
            storage_name = storage_name
        )
    
    except Exception as e:
        raise e