from fastapi import APIRouter, Path, HTTPException, Header
from app.services.file.schemas.presigned import PresignedURLResponse
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode
router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.get(
    "/imgplt/s3/{file_path:path}",
    response_model=PresignedURLResponse,
    tags=["File"],
    summary="Presigned S3 파일 다운로드 링크 생성",
    description="파일 경로를 입력받아 presigned URL을 생성하고 다운로드 링크를 제공합니다."
)
async def get_presigned_url(
    file_path: str = Path(..., description="다운로드할 파일 경로"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    

    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        headers = {}
    try:
        result = await file_client._request(
            "GET", f"/imgplt/s3/{file_path}",
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
