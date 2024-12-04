import io
import re
from typing import Dict
from fastapi import APIRouter, Request, Depends, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from app.auth.auth import auth, UserViewSchemas

from .schemas import StorageCreaterSchemas, StorageViewSchema, ObjectSchemas
from .services import StorageServices as services
from utils.minio import minio_storage
from utils import memory
from schemas.responses_schemas import DetailResponse

import requests

router = APIRouter(
    prefix = '/disk',
    tags = ['TDisk']
)


@router.get('/storages', tags = ['Storage CRUD'], response_model = list[StorageViewSchema])
async def get_storages(
    request: Request,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Getting all repositories and references to objects"""
    # storages_list = services.get_storages(active_user.uuid)
    # result = {}
    # for storage in storages_list:
    #     objects = minio_storage.get_objects_urls_from_storage(active_user.uuid, storage)

    #     objs = {}
    #     for key in objects:
    #         url = change_minio_url_to_main(
    #             request,
    #             objects.get(key)
    #         )
    #         objs.update({key: url})
        
    #     result.update({storage: objs})
        
    # return result
    
    storages_list = services.get_storages(active_user.uuid)
    result = []
    for storage in storages_list:
        objects = minio_storage.get_objects_urls_from_storage(active_user.uuid, storage)
        objs = []
        for key in objects:
            url = change_minio_url_to_main(
                request,
                objects.get(key)
             )
            
            objs.append(ObjectSchemas(
                name = key,
                url = url
            ))
        
        result.append(
            StorageViewSchema(
                name = storage,
                objects = objs
            )
        )
    
    return result


@router.post('/storage', tags = ['Storage CRUD'], response_model = DetailResponse)
async def create_storage(
    data: StorageCreaterSchemas,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Creating a repository. In a simple way, create a directory"""
    # Создаем папку в Minio
    url = minio_storage.create_storage(
        active_user.uuid,
        data.name.strip()
    )
    
    # Сохраняем юрл адрес в бд
    services.create_storage(
        data = data,
        user_uuid = active_user.uuid,
        url = url,
    )
    
    
    return JSONResponse(
        status_code = 201,
        content = {
            'detail': 'The repository was successfully created'
        }
    )
    

@router.get('/storage', tags = ['Storage CRUD'], response_model = list[ObjectSchemas])
async def get_objects_from_storage(
    request: Request,
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """getting links to objects from the repository."""
    
    # objs = minio_storage.get_objects_urls_from_storage(active_user.uuid, storage_name.strip())
    # result_objs = {}
    # for key in objs:
    #     url = request.url_for('send_object', creator_uuid = active_user.uuid, file_name = key, storage_name = storage_name)
    #     result_objs.update({
    #         key: url._url
    #     })
    # return result_objs
    
    objs = minio_storage.get_objects_urls_from_storage(active_user.uuid, storage_name.strip())
    result_objs = []
    for key in objs:
        url = request.url_for('send_object', creator_uuid = active_user.uuid, file_name = key, storage_name = storage_name)
        result_objs.append(ObjectSchemas(
            name = key,
            url = url._url
        ))
        
    return result_objs
    

@router.delete('/storage', tags = ['Storage CRUD'], response_model = DetailResponse)
async def delete_storage(
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Deleting Storage"""
    
    services.delete_storage(storage_name = storage_name, user_uuid = active_user.uuid)
    minio_storage.delete_storage(storage_name = storage_name, uuid = active_user.uuid)
    return JSONResponse(
        status_code = 200,
        content = {
            'detail': 'The storage has been deleted'
        }
    )
    


@router.put('/storage/object/add', tags = ['Object CRUD'], response_model = ObjectSchemas)
async def add_object(
    request: Request,
    storage_name: str,
    file: UploadFile = File(...),
    object_name: str = None,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Add an object to the repository. If the entered storage does not exist, it will create a new one and upload a file to it"""
    object_name = object_name if object_name else file.filename # Получаем имя файла
    file_type = file.content_type.split('/')[1] # Получаем тип файла

    # Проверка на кириллицу в названии
    if bool(re.search(r'[А-Яа-яЁё]', object_name)):
        raise HTTPException(
            status_code = 400,
            detail = 'The file name cannot contain Cyrillic letters'
        )
    
    # Проверяем, не выходит ли общая память файлов, при добавлении файла, за приделы разрешенного кол-во памяти   
    if memory.bytes_to_gigabytes(file.size) + memory.bytes_to_gigabytes(minio_storage.get_total_objects_size(active_user.uuid)) > 10:
        raise HTTPException(
            status_code = 400,
            detail = 'At the moment, you own 10 gigabytes of memory. You cannot exceed this limit'
        )
    
    object_name = f'{object_name}.{file_type}' if object_name else file.filename # Имя файла с типом
    # Добавляем в хранилище файл
    minio_storage.add_object_in_storage(
        uuid = active_user.uuid,
        storage_name = storage_name,
        object_name = object_name,
        object_data = file.file,
        object_lenght = file.size
    )
    
    # Проверяем, есть ли в бд хранилище, если нет, то добавляем
    services.check_user_storage(
        user_uuid = active_user.uuid,
        storage_name = storage_name,
        url = minio_storage.get_storage_url_by_name(active_user.uuid, storage_name)
    )
    
    # Адрес файла
    url = request.url_for('send_object', creator_uuid = active_user.uuid, file_name = object_name.strip(), storage_name = storage_name.strip())._url
    
    return ObjectSchemas(
        name = object_name,
        url = url
    )



    

@router.delete('/storage/object/delete', tags = ['Object CRUD'], response_model = DetailResponse)
async def delete_object(
    storage_name: str,
    object_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Deleting an object from storage"""
    minio_storage.delete_object(active_user.uuid, storage_name, object_name)
    return JSONResponse(
        status_code = 200,
        content = {
            'detail': 'The object has been deleted'
        }
    )


# Storage Settings

@router.put('/storage/settings/private', tags = ['Setting'], response_model = DetailResponse)
async def private_setting(
    private: bool,
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Changes the storage's privacy status"""
    services.change_private_status(
        creator_uuid = active_user.uuid,
        storage_name = storage_name,
        private_status = private
    )
    
    response_text_true = 'Now you or the users you have added to the list of participants can use this repository.'
    response_text_false = 'This repository is now public. Any user can use your products.'
    
    return JSONResponse(
        status_code = 200,
        content = {
            'detail': f'The privacy status has been changed to {private}.' + ' ' + response_text_true if private else response_text_false
        }
    )
    

@router.post('/storage/settings/add/member', tags = ['Setting'], response_model = DetailResponse)
async def add_member_to_storage(
    storage_name: str,
    member_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Adds a user to the list of participants. These users can view storage objects, even if the storage is private"""
    services.add_user_to_storage(
        member_name = member_name,
        user_uuid = active_user.uuid,
        storage_name = storage_name
    )
    
    return JSONResponse(
        status_code = 200,
        content = {
            'detail': f'You have successfully added a user with the name: "{member_name}"'
        }
    )


@router.get('/storage/data', tags = ['Setting'])
async def get_storage_data(
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    memory_is_used = memory.bytes_to_gigabytes(minio_storage.get_total_objects_size(active_user.uuid))
    total_memory = 10
    return JSONResponse(
        status_code = 200,
        content = {
            'total_memory': f'{total_memory} Gb',
            'memory_used': f'{round(memory_is_used, 2)} Gb',
            'memory_left': f'{round(total_memory - memory_is_used, 2)} Gb'
        }
    )


@router.get('/storage/dowload', tags = ['Dowload Files'])
async def dowload_storages(
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Установить все файлы с хранилища"""

    return await send_storage_files(
        creator_uuid = active_user.uuid,
        storage_name = storage_name,
        active_user = active_user
    )
    

@router.get('/storage/object/dowload', tags = ['Dowload Files'])
async def dowload_object(
    storage_name: str,
    object_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Установить объект"""
    
    return await send_object(
        creator_uuid = active_user.uuid,
        file_name = object_name,
        storage_name = storage_name,
        active_user = active_user
    )


# AWS
# Снизу код с работой S3 хранилищем

import requests
import io
import zipfile
from utils import memory
MEDIA_TYPE="application/octet-stream"

def headers_template(file_name: str):
    return {"Content-Disposition": f"attachment; filename*=UTF-8''{file_name}"}


@router.get('/s3/{creator_uuid}/{storage_name}/{file_name}', tags = ['S3'])
async def send_object(
    creator_uuid: str,
    file_name: str,
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Getting an object. You can get an object from this link. If you do not have access, you will not receive the file"""
    if not minio_storage.check_object(creator_uuid, storage_name, file_name):
        return JSONResponse(
            status_code = 400,
            content = {
                'detail': 'There is no such file'
            }
        )
    
    minio_url = minio_storage.get_object(creator_uuid, storage_name, file_name) # Получаем ссылку с объектом
    storage = services.get_one_storage(creator_uuid, storage_name, url = minio_url) # Получаем данные о хранилище
    
    # Проверяем на право доступа к файлу
    if storage.private and active_user.uuid not in storage.get_members_uuids() and active_user.uuid != creator_uuid:
        return JSONResponse(
            status_code = 403,
            content = {
                'detail': 'You do not have the right to access this object and storage. To gain access, the repository creator must add you to the repository members'
            }
        )

    response = requests.get(minio_url, stream = True)
    file = io.BytesIO(response.content)
    headers = headers_template(file_name)
    return StreamingResponse(file, media_type = MEDIA_TYPE, headers = headers)


@router.get('/s3/{creator_uuid}/{storage_name}', tags = ['S3'])
async def send_storage_files(
    creator_uuid: str,
    storage_name: str,
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    try:
        storage = services.get_one_storage(creator_uuid, storage_name) # Получаем данные о хранилище
    
    except:
        raise HTTPException(
            status_code = 400,
            detail = 'There is no such repository'
        )
        
    # Проверяем на право доступа к хранилищу
    if storage.private and active_user.uuid not in storage.get_members_uuids() and active_user.uuid != creator_uuid:
        return JSONResponse(
            status_code = 403,
            content = {
                'detail': 'You do not have the right to access this object and storage. To gain access, the repository creator must add you to the repository members'
            }
        )
    
    objects_list = []
    urls = minio_storage.get_objects_urls_from_storage(creator_uuid, storage_name) # получаем все ссылки на скачивание объектов
    for file_name in urls:
        response =  requests.get(urls.get(file_name), stream = True)
        file = io.BytesIO(response.content)
        objects_list.append([file_name, file])
    
    io_zipfile = io.BytesIO()
    with zipfile.ZipFile(io_zipfile, 'w', zipfile.ZIP_DEFLATED) as zfile:
        for file_data in objects_list:
            zfile.writestr(file_data[0], file_data[1].getvalue())
    
    io_zipfile.seek(0)
            
    return StreamingResponse(io_zipfile, media_type = MEDIA_TYPE, headers = headers_template(f'{storage_name}.zip'))


def change_minio_url_to_main(
    request: Request,
    minio_url: str
):
    minio_c = minio_url.split('/')
    adress = '/'.join(minio_c[4:])
    return f'{request.base_url}disk/s3/{adress}'