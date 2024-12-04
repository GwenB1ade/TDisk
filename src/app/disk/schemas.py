from typing import Dict, Union
from pydantic import BaseModel, AnyUrl


class StorageCreaterSchemas(BaseModel):
    name: str
    private: bool = False
    

class StorageSchemas(StorageCreaterSchemas):
    uuid: str
    creator_uuid: str
    participants_uuids: list
    url: str
    objects: list
    

class ObjectCreateSchemas(BaseModel):
    name: str
    storage_uuid: str
    url: str
    author_uuid: str


class ObjectSchemas(BaseModel):
    name: str
    url: AnyUrl
    

class StorageViewSchema(BaseModel):
    name: str
    objects: list[ObjectSchemas]
    