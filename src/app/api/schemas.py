from pydantic import BaseModel, field_validator, PrivateAttr
from typing import Any, TYPE_CHECKING
from .services import StorageAPIServices
from app.auth.services import UserServices

if TYPE_CHECKING:
    from app.disk.models import StorageModel
    from app.auth.models import UserModel


class KeySchemas(BaseModel):
    key: str
    _storage: 'StorageModel' = PrivateAttr()
    _user: 'UserModel' = PrivateAttr()
    
    @field_validator('key')
    @classmethod
    def validate_key(cls, v: Any):
        print(v)
        storage = StorageAPIServices.get_storage_by_key(
            key = v
        )
        
        cls._storage = storage
        cls._user = UserServices.get_object_by_uuid(uuid = storage.creator_uuid)
        
        return v

    @classmethod
    def get_storage(cls):
        return cls._storage
    
    
    @classmethod
    def get_user(cls):
        return cls._user