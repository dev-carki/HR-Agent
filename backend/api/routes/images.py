import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)

@router.get("/{file_path:path}")
async def get_image(file_path: str):
    full_path = f"uploads/{file_path}"
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="파일 경로를 찾을 수 없습니다.")
    
    return FileResponse(
        path=full_path
    )