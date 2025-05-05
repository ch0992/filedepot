from fastapi import APIRouter, Header, HTTPException
from typing import Optional
# 인증 서비스가 필요하다면 아래에 직접 구현 또는 외부 인증 서버 연동 로직을 작성하세요.
from app.services.gateway.schemas.auths import AuthWorkspaceList

# 예시: auth_service = ... (외부 인증 서버 연동)
router = APIRouter(prefix="/auth")

@router.get(
    "/imgplt/auths",
    response_model=AuthWorkspaceList,
    tags=["Auth"],
    summary="사용자 토큰 인증 및 workspace 권한 조회",
    description="외부 인증 서버를 통해 accessToken의 유효성을 검증하고 workspace 접근 권한을 조회합니다."
)
async def verify_auth(
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    raise HTTPException(status_code=501, detail="Not implemented: 실제 인증 서비스 연동 필요")
