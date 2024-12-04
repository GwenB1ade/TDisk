from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, UUID
from typing import Optional
import uuid
import json

class UserModel(Base):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}
    uuid: Mapped[str] = mapped_column(UUID(as_uuid = True), default = uuid.uuid4, primary_key = True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique = True)
    password: Mapped[str]
    refresh_token_name: Mapped[Optional[str]]
    
    storages: Mapped[str] = mapped_column(JSON(), nullable = True)
    
    
    def add_storage(self, storage_name: str) -> None:
        storage_list = json.loads(self.storages) if self.storages else []
        storage_list.append(storage_name)
        self.storages = json.dumps(storage_list)
    
    def get_storages(self) -> list:
        storage_list = json.loads(self.storages) if self.storages else []
        return storage_list
    
    def delete_storage(self, storage_name: str) -> None:
        storage_list = json.loads(self.storages) if self.storages else []
        if not storage_list == [] and storage_name in storage_list:
            storage_list.remove(storage_name)
        
        self.storages = json.dumps(storage_list)
        
        