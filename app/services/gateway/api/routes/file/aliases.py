from fastapi import APIRouter, Header, HTTPException, status
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.get(
    "/imgplt/aliases",
    tags=["file"],
    summary="적재 가능 alias 목록 조회",
    description="인증된 사용자의 권한 내에서 접근 가능한 파일 적재 alias 목록을 반환합니다."
)
async def get_aliases(
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    # 실제 인증 로직에 따라 user_id 추출 필요 (예시)
    user_id = "test-user"  # 실제 서비스에서는 토큰에서 user_id 추출
    try:
        result = await file_client.get_aliases(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
