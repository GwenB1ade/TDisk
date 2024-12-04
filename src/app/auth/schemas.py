from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserCreateSchemas(BaseModel):
    username: str
    email: str
    password: str


class UserViewSchemas(BaseModel):
    uuid: str
    username: str
    

class UserSchemas(UserCreateSchemas):
    uuid: str
    refresh_token_name: Optional[str]
    

class LoginSchema(BaseModel):
    email: str
    password: str
    

class DetailResponse(BaseModel):
    detail: str
    

class DetailCodeResponse(DetailResponse):
    code: str