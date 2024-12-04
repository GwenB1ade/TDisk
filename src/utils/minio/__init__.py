from .minio_disk import MinioStorageClient
from urllib3.exceptions import MaxRetryError

try:
    minio_storage = MinioStorageClient()
except MaxRetryError:
    raise Exception('Невозможно подкючиться к Minio. Возможно вы не запустили Minio сервер или неправильный путь подключения. Подробная ошибка Сверху')