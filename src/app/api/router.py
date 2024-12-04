from fastapi import APIRouter, File, Header, Response, Request, UploadFile, Body
from fastapi.responses import JSONResponse
from app.auth.auth import active_user

from .schemas import KeySchemas
from .services import StorageAPIServices as services

from app.disk import router as disk_router
from app.auth.auth import UserViewSchemas


router = APIRouter(
    tags = ['API'],
    prefix = '/api'
)


@router.get(
    '/storage/key',
    status_code = 201,
    name = 'Получения ключа'
)
async def get_storage_key(
    storage_name: str,
    active_user: active_user,
):
    """Генерация или получение ключ-доступа к хранилищу."""
    key = services.create_or_get_storage_key(
        uuid = active_user.uuid,
        storage_name = storage_name
    )
    
    return JSONResponse(
        status_code = 201,
        content = {
            'key': key,
        }
    )
    
    

@router.post('/storage/object/add')
async def add_object_in_storage(
    request: Request,
    key: str,
    object_name: str = None,
    file: UploadFile = File(...),
):
    """Добавление файла через ключ доступа"""
    keydata = KeySchemas(key = key)
    storage = keydata.get_storage()
    user = keydata.get_user()
    return await disk_router.add_object(
        request = request,
        storage_name = storage.name,
        file = file,
        object_name = object_name,
        active_user = UserViewSchemas(
            uuid = str(user.uuid),
            username = user.username,
            picture = user.picture
        )
    )


@router.delete('/storage/object/delete')
async def delete_object_from_storage(
    key: str,
    object_name: str
):
    """Удаление файла через ключ доступа"""
    keydata = KeySchemas(key = key)
    storage = keydata.get_storage()
    user = keydata.get_user()
    return await disk_router.delete_object(
        storage_name = storage.name,
        object_name = object_name,
        active_user = UserViewSchemas(
            uuid = str(user.uuid),
            username = user.username,
            picture = user.picture
        )
        
    )