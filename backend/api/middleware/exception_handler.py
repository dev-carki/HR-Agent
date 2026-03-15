from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import TypedDict
from typing import Optional, Any

class BaseErrorResponse(TypedDict):
    code: int
    message: str
    data: Optional[Any]
        
async def global_exception_hanlder(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=BaseErrorResponse(code=exc.status_code, message=exc.detail, data=None)
        )
    
    return JSONResponse(
        status_code=500,
        content=BaseErrorResponse(code=500, message=str(exc), data=None)
    )