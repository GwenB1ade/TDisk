from fastapi import HTTPException
from service.base import BaseServices
from database import session_creater
from app.disk.models import StorageModel

from secrets import token_urlsafe


class StorageAPIServices(BaseServices):
    model = StorageModel
    
    
    @classmethod
    def create_or_get_storage_key(cls, uuid: str, storage_name: str):
        with session_creater() as s:
            storage = s.query(cls.model).filter_by(
                creator_uuid = uuid,
                name = storage_name
            ).first()
            
            if storage:
                key = storage.key
                if not key:
                    storage.key = token_urlsafe(18)
                    key = storage.key
                    s.commit()
                
                return key
            
            raise HTTPException(
                status_code = 400,
                detail = 'There is no such repository'
            )
    
    
    @classmethod
    def get_storage_by_key(cls, key: str):
        with session_creater() as s:
            storage = s.query(cls.model).filter_by(
                key = key
            ).first()
            
            if not storage:
                raise HTTPException(
                    status_code = 400,
                    detail = 'Failed to connect to the storage. Check if the access key is correct. The storage has probably been deleted or the access key has been updated'
                )
            
            return storage