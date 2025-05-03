from fastapi import APIRouter, Header, HTTPException, status, Depends
from typing import List, Optional
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

router = APIRouter(prefix="/file")

def get_file_client():
    return FileServiceClient(settings.FILE_SERVICE_URL)

@router.get("/ping", summary="File health check", tags=["Health"])
async def file_ping(file_client: FileServiceClient = Depends(get_file_client)):
    """File 서비스 헬스 체크 엔드포인트 (실제 file 서비스로 전달)"""
    return await file_client.health()

@router.get(
    "/imgplt/aliases",
    tags=["file"],
    summary="적재 가능 alias 목록 조회",
    description="인증된 사용자의 권한 내에서 접근 가능한 파일 적재 alias 목록을 반환합니다."
)
async def get_aliases(
    authorization: Optional[str] = Header(None, description="Bearer accessToken"),
    file_client: FileServiceClient = Depends(get_file_client)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    # 실제 인증 로직에 따라 user_id 추출 필요 (예시)
    user_id = "test-user"
    return await file_client.get_aliases(user_id)
