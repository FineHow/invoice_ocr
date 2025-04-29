

from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/download/{file_name}", tags=["下载处理表格"])
async def download_file(file_name: str):
    """
    提供文件下载功能。
    """
    file_path = Path("backend/static/") / file_name
    
    if file_path.exists() and file_path.is_file():
        return FileResponse(
            path=str(file_path),
            filename=file_name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    raise HTTPException(status_code=404, detail="File not found")