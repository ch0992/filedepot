from fastapi import APIRouter, Query, HTTPException, Header
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings
from app.services.file.schemas.zips import ZipPresignedResponse

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

# 인증 로직이 필요하다면 아래에 직접 구현 또는 기존 auth_service import를 사용하세요.
# 인증 서비스가 필요하다면 아래에 직접 구현 또는 외부 인증 서버 연동 로직을 작성하세요.
# 예시: auth_service = ...

@router.get(
    "/imgplt/zips",
    response_model=ZipPresignedResponse,
    tags=["file"],
    summary="Presigned ZIP 다운로드 링크 생성",
    description="SQL 조건으로 대상 파일들을 조회하고, presigned zip 다운로드 링크를 생성해 반환합니다."
)
async def get_zip_presigned_url(
    sql: str = Query(..., description="SQL 조건"),
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await file_client._request(
            "GET", f"/imgplt/zips?sql={sql}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
