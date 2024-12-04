from pydantic import ValidationError
import pytest
from contextlib import nullcontext
from src.database import session_creater, create_db
from sqlalchemy.exc import OperationalError

from src.app.auth.services import UserServices, UserCreateSchemas
from src.app.disk.services import StorageServices

def test_create_db():
    try:
        create_db()
    
    except OperationalError as e:
        raise Exception('Unable to connect to the database.')

@pytest.mark.parametrize(
    'username, email, expectation',
    [
        ('test', 'test', nullcontext()),
        (None, None, pytest.raises(ValidationError))
    ]
) 
def test_creating_user(
    username: str,
    email: str,
    expectation
):
    with expectation:
        user = UserServices.create_user(
            UserCreateSchemas(
                username = username,
                email = email,
                password = '123'
            )
        )
        
        assert user.username == username
    
        UserServices.delete_user(user.uuid)
    


    
        