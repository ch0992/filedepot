from fastapi import APIRouter, Path, Query, HTTPException, Header
from typing import Optional
from app.services.gateway.services.impl.file_download_service import FileDownloadService
from app.services.file.schemas.presigned import PresignedURLResponse

router = APIRouter()
file_download_service = FileDownloadService()

from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency, auth_service
from fastapi import Depends

@router.get(
    "/imgplt/s3/{file_path:path}",
    response_model=PresignedURLResponse,
    tags=["file"],
    summary="Presigned S3 파일 다운로드 링크 생성",
    description="파일 경로를 입력받아 presigned URL을 생성하고 다운로드 링크를 제공합니다."
)
async def get_presigned_url(
    file_path: str = Path(..., description="다운로드할 파일 경로"),
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    await auth_service.verify_token_and_get_workspaces(access_token)
    try:
        result = await file_download_service.create_presigned_url(file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
