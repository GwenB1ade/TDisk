from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


async def exception_500(request: Request, exc):
    return JSONResponse(
        status_code = 500,
        content = {
            'detail': 'Internal Server Error'
        }
    )
    

