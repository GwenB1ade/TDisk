from fastapi import HTTPException
from fastapi_easyauth import hash_password
from database import session_creater
from service.base import BaseServices

from .models import UserModel
from .schemas import UserCreateSchemas, UserViewSchemas


class UserServices(BaseServices):
    model = UserModel
            
    @classmethod
    def delete_user(cls, uuid: str):
        with session_creater() as s:
            s.query(cls.model).filter_by(
                uuid = uuid
            ).delete()
            
            s.commit()
            
    
    @classmethod
    def get_userdata(cls, uuid: str):
        with session_creater() as s:
            user = s.query(cls.model).filter_by(
                uuid = uuid
            ).first()
            
            return UserViewSchemas(
                uuid = str(user.uuid),
                username = user.username,
            )
    
    
    @classmethod
    def create_user(cls, userdata: UserCreateSchemas):
        with session_creater() as s:
            user = s.query(cls.model).filter(
                cls.model.email == userdata.email
            ).first()
            
            if user:
                raise HTTPException(
                    status_code = 400,
                    detail = 'A user with this email has already been created'
                )
            
            user = cls.model(
                username = userdata.username,
                email = userdata.email,
                password = hash_password(userdata.password),
            )
            
            s.add(user)
            s.commit()
            
            return UserViewSchemas(
                    uuid = str(user.uuid),
                    username = user.username,
                )
            
    @classmethod
    def check_user_by_email_and_password(cls, email: str, password: str):
        with session_creater() as s:
            user = s.query(cls.model).filter(
                cls.model.email == email,
                cls.model.password == hash_password(password)
            ).first()
            
            return True if user else False
    
    
    @classmethod
    def get_userdata_by_email(cls, email: str):
        with session_creater() as s:
            user = s.query(cls.model).filter_by(
                email = email
            ).first()
            
            return UserViewSchemas(
                uuid = str(user.uuid),
                username = user.username,
            )