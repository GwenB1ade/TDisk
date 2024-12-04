from fastapi.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from database import engine
from config import settings

from .auth import UsernameAndPasswordProvider

from app.auth.models import UserModel
from app.disk.models import StorageModel

admin = Admin(
    engine,
    title = 'Admin Panel',
    auth_provider = UsernameAndPasswordProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)]
)

admin.add_view(
    ModelView(UserModel)
)

admin.add_view(
    ModelView(StorageModel)
)