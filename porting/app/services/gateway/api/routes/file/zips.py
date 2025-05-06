from fastapi import APIRouter, Query, HTTPException, Header
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings
from app.common.utils.auth_mode import get_auth_mode
from app.services.file.schemas.zips import ZipPresignedResponse
from typing import Optional


router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)


@router.get(
    "/imgplt/zips",
    response_model=ZipPresignedResponse,
    tags=["File"],
    summary="Presigned ZIP 다운로드 링크 생성",
    description="SQL 조건으로 대상 파일들을 조회하고, presigned zip 다운로드 링크를 생성해 반환합니다."
)
async def get_zip_presigned_url(
    sql: str = Query(..., description="SQL 조건"),
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
            "GET", f"/imgplt/zips?sql={sql}",
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
