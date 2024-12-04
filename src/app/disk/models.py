from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import JSON, String, UUID, ForeignKey
import uuid
import json


class StorageModel(Base):
    __tablename__ = 'Storage'
    uuid: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    name: Mapped[str]
    creator_uuid: Mapped[str] = mapped_column(ForeignKey('User.uuid'))
    
    private: Mapped[bool] = mapped_column(default = False)
    participants_uuids: Mapped[str] = mapped_column(JSON(), nullable = True)
    
    url: Mapped[str]
    
    key: Mapped[str] = mapped_column(default = False, nullable = True)
    
    
    def add_member_uuid_to_participants(self, uuid: str):
        members = json.loads(self.participants_uuids) if self.participants_uuids else []
        members.append(str(uuid))
        self.participants_uuids = json.dumps(members)
    
    
    def get_members_uuids(self):
        members_list = json.loads(self.participants_uuids) if self.participants_uuids else []
        return members_list


    
    