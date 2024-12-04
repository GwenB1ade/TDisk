from typing import Annotated
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from admin.admin import admin
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

import exceptions
from database import create_db
from config import settings


app = FastAPI(
    title = 'TDisk',
    version = '0.0.1',
)

@app.get('/', include_in_schema = False)
async def redirect_to_docs():
    return RedirectResponse('/docs')


# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key = settings.SESSION_SECRET)



# Exceptions
app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, exceptions.exception_500)


# Routing
from app.auth.router import router as auth_router
from app.disk.router import router as disk_router
from app.api.router import router as api_router

app.include_router(auth_router)
app.include_router(disk_router)
app.include_router(api_router)


if __name__ == "__main__":
    create_db()
    uvicorn.run('main:app', reload = True)