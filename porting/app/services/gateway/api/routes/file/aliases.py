"""
[📄 aliases.py - Gateway Route]

설명:
- 파일 별칭 목록을 조회하는 엔드포인트 제공
- 인증된 사용자의 별칭만 반환

주요 연동:
- AliasQueryService (서비스)
- get_current_user (의존성)
"""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from app.services.file.services.impl.alias_query_service import AliasQueryService
from app.services.file.schemas.aliases import AliasListResponse
from app.services.auth.dependencies import get_current_user
from app.services.auth.schemas import User
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.get(
    "/imgplt/aliases",
    response_model=AliasListResponse,
    tags=["File"],
    summary="적재 가능 alias 목록 조회",
    description="인증된 사용자의 권한 내에서 접근 가능한 파일 적재 alias 목록을 반환합니다."
)
async def get_aliases(
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    """
    인증된 사용자에게 접근 가능한 alias 목록을 반환하는 API
    Args:
        authorization (Optional[str]): 사용자 인증 토큰 (헤더에서 전달)

    Returns:
        list: 접근 가능한 alias 목록

    Raises:
        HTTPException: 인증 실패 또는 내부 오류 발생 시 500 응답
    """
    # WHY: remote 모드에서는 accessToken 검증을 통해 사용자 권한을 확인해야 함
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        # 실제 인증 로직에 따라 user_id 추출 필요 (예시)
        user_id = "test-user"  # 실제 서비스에서는 토큰에서 user_id 추출
    else:
        user_id = "test-user"
    try:
        # file 서비스에 요청하여 alias 목록 조회
        result = await file_client.get_aliases(user_id)
        return result
    except Exception as e:
        # 예외 발생 시 500 반환
        raise HTTPException(status_code=500, detail=str(e))
