from fastapi import APIRouter, Depends, HTTPException, Request

from .auth import auth, active_user
from .schemas import (UserCreateSchemas,
                      UserSchemas,
                      UserViewSchemas,
                      LoginSchema,
                      DetailResponse,
                      DetailCodeResponse
                    )
from .services import UserServices


router = APIRouter(
    tags = ['Auth'],
    prefix = '/auth'
)


@router.post('', response_model = DetailResponse)
async def create_account(
    userdata: UserCreateSchemas
):
    """Create Account"""
    user = UserServices.create_user(userdata)
    if user:
        return DetailResponse(
            detail = 'You have successfully created an account'
        )


@router.post('/login', response_model = DetailCodeResponse)
async def login_account(
    request: Request,
    login_form: LoginSchema
):
    """User authorization"""
    if not UserServices.check_user_by_email_and_password(
        email = login_form.email,
        password = login_form.password
    ):
        raise HTTPException(
            status_code = 400,
            detail = 'Invalid password or email'
        )
    
    user = UserServices.get_userdata_by_email(email = login_form.email)
    access_token, refresh_token = auth.create_access_and_refresh_token(user)
    auth.save_tokens(user.uuid, request, access_token, refresh_token)
    
    return DetailCodeResponse(
        detail = 'You have successfully logged in',
        code = refresh_token
    )
    

@router.get('/logout', response_model = DetailResponse)
async def logout(
    request: Request
):
    auth.delete_tokens(request)
    return DetailResponse(
        detail = 'You have successfully logged out of your account'
    )
    

@router.get('/me', response_model = UserViewSchemas)
async def me(
    active_user: UserViewSchemas = Depends(auth.active_user)
):
    """Get data about an active user"""
    return active_user


@router.put('/info', response_model = UserViewSchemas)
async def get_user_info(
    code: str
):
    """
    code: access_token or refresh_token \n
    Get user info
    """
    info = auth.get_user_info_by_token(code)
    return info
        
    

    