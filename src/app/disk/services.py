from database import session_creater
from .schemas import ObjectCreateSchemas, StorageCreaterSchemas, StorageSchemas, ObjectSchemas
from .models import StorageModel
from service.base import BaseServices

from app.auth.models import UserModel


class StorageServices(BaseServices):
    model = StorageModel
    
    @classmethod
    def create_storage(cls, data: StorageCreaterSchemas, user_uuid: str, url: str):
        with session_creater() as s:
            storage = cls.model(
                name = data.name.strip(),
                private = data.private,
                creator_uuid = user_uuid,
                url = url
            )
            
            user = s.query(UserModel).filter_by(
                uuid = user_uuid
            ).first()
            
            user.add_storage(data.name.strip())
            
            s.add(storage)
            s.commit()
            
            return storage
    
    
    @classmethod
    def get_storages(cls, user_uuid: str) -> list:
        with session_creater() as s:
            user = s.query(UserModel).filter_by(uuid = user_uuid).first()
            storages = user.get_storages()
            return storages
        
    
    @classmethod
    def get_one_storage(cls, creator_uuid: str, storage_name: str, url: str = None):
        with session_creater() as s:
            storage = s.query(cls.model).filter(
                cls.model.creator_uuid == creator_uuid,
                cls.model.name == storage_name
            ).first()
            
            if not storage:
                storage = cls.model(
                    name = storage_name.strip(),
                    private = False,
                    creator_uuid = creator_uuid,
                    url = url
                )
                
                s.add(storage)
                s.commit()
            
            return storage
    
    
    @classmethod
    def delete_storage(cls, storage_name: str, user_uuid: str):
        with session_creater() as s:
            s.query(cls.model).filter_by(
                name = storage_name
            ).delete()
            
            user = s.query(UserModel).filter_by(uuid = user_uuid).first()
            user.delete_storage(storage_name)

            s.commit()
    
    
    @classmethod
    def change_private_status(cls, creator_uuid: str, storage_name: str, private_status: bool):
        with session_creater() as s:
            storage = s.query(cls.model).filter_by(
                creator_uuid = creator_uuid,
                name = storage_name
            ).first()
            
            storage.private = private_status
            
            s.commit()
            
    
    @classmethod
    def add_user_to_storage(cls, member_name: str, user_uuid: str, storage_name: str):
        with session_creater() as s:
            member = s.query(UserModel).filter_by(
                username = member_name
            ).first()
            
            storage = s.query(cls.model).filter(
                cls.model.creator_uuid == user_uuid,
                cls.model.name == storage_name
            ).first()
            
            storage.add_member_uuid_to_participants(member.uuid)
            s.commit()
    
    
    @classmethod
    def check_user_storage(cls, user_uuid: str, storage_name: str, url: str):
        with session_creater() as s:
            storage = s.query(cls.model).filter_by(
                name = storage_name,
                uuid = user_uuid
            ).first()
            
            if not storage:
                cls.create_storage(
                    data = StorageCreaterSchemas(
                        name = storage_name,
                        private = False
                    ),
                    user_uuid = user_uuid,
                    url = url
                )
            
