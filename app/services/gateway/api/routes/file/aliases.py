from fastapi import APIRouter, Header, HTTPException, status, Depends
from typing import List, Optional
from app.services.gateway.services.impl.file_alias_service import FileAliasService
from app.services.file.schemas.aliases import AliasEntry
from app.services.gateway.services.impl.auth_module_service import auth_service

router = APIRouter()
file_alias_service = FileAliasService()

@router.get(
    "/imgplt/aliases",
    response_model=List[AliasEntry],
    tags=["file"],
    summary="적재 가능 alias 목록 조회",
    description="인증된 사용자의 권한 내에서 접근 가능한 파일 적재 alias 목록을 반환합니다."
)
async def get_aliases(
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    user_info = await auth_service.verify_token_and_get_workspaces(access_token)
    # 실제 구현에서는 user_info에서 user_id 등 식별자를 추출하여 전달
    return await file_alias_service.get_aliases(user_info)
