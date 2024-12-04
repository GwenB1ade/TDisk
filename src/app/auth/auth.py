from database import r
from datetime import timedelta
from fastapi import HTTPException, Request, Depends
from fastapi_easyauth.jwt import Jwt
from fastapi_easyauth.sessionauth import SessionAuth
from typing import Annotated, Union

from config import settings
from .schemas import UserViewSchemas, UserCreateSchemas
from utils.redis.auth_redis import AuthRedis


jwt = Jwt(
    secret = settings.jwt_secret,
    auto_error = False,
    access_expires_delta = timedelta(minutes = 15),
    refresh_expires_delta = timedelta(days = 15),
    model = UserViewSchemas
)

sessionauth = SessionAuth(
    jwt = jwt,
    name_in_session = 'access-token'
)

auth_redis = AuthRedis(r)


class Auth:
    
    def __init__(self): ...
    
    
    def create_access_and_refresh_token(self, schemas: UserViewSchemas):
        access_token = jwt.create_access_token(schemas.model_dump())
        refresh_token = jwt.create_refresh_token(schemas.model_dump())
        
        return access_token, refresh_token
    
    
    def save_tokens(self, uuid: str, request: Request, access_token: str, refresh_token: str):
        request.session['uuid'] = uuid
        sessionauth.save_token_in_session(access_token, request)
        auth_redis.save_token(name = f'refresh:{uuid}', token = refresh_token)
        
    
    def active_user(self, request: Request):
        try:
            token = sessionauth.get_token_from_session(request)
            user = jwt.decode_token(token, full = False)
            return user
        
        except:
            try: 
                uuid = request.session['uuid']
                refresh_token = auth_redis.get_token(f'refresh:{uuid}')
                user = jwt.decode_token(refresh_token, full = False)
                
                access_token, refresh_token = self.create_access_and_refresh_token(user)
                self.save_tokens(uuid, request, access_token, refresh_token)
                
                return user
            
            except Exception as e:
                raise HTTPException(
                    status_code = 401,
                    detail = 'Unauthorized'
                )
    
    def delete_tokens(self, request: Request):
        uuid = request.session['uuid']
        sessionauth.delete_token_from_session(request)
        auth_redis.delete_token(uuid)
        
    
    def get_user_info_by_token(self, token: str) -> Union[UserViewSchemas, None]:
        data = sessionauth.jwt.decode_token_in_model(
            token = token,
            model = UserViewSchemas
    )
    
        if not data:
            return None
        
        return data
        
        
            
            

auth = Auth()
active_user = Annotated[UserViewSchemas, Depends(auth.active_user)]
