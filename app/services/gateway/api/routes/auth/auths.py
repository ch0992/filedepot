from fastapi import APIRouter, Header, HTTPException, Depends, status
from typing import Optional
from app.services.gateway.services.impl.auth_module_service import AuthModuleService
from app.services.gateway.schemas.auths import AuthWorkspaceList

auth_service = AuthModuleService()
router = APIRouter()

@router.get(
    "/imgplt/auths",
    response_model=AuthWorkspaceList,
    tags=["auth"],
    summary="사용자 토큰 인증 및 workspace 권한 조회",
    description="외부 인증 서버를 통해 accessToken의 유효성을 검증하고 workspace 접근 권한을 조회합니다."
)
async def verify_auth(
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    from app.services.log.tracing import get_tracer
    from app.services.log.exceptions import capture_and_log
    import logging
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::verify_auth"):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        try:
            return await auth_service.verify_token_and_get_workspaces(access_token)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail=str(e))
