from fastapi import APIRouter, Header, HTTPException, status, Depends
from typing import List, Optional
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

router = APIRouter(prefix="/file")

def get_file_client():
    return FileServiceClient(settings.FILE_SERVICE_URL)

from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log
import logging

@router.get("/ping", summary="File health check", tags=["Health"])
async def file_ping(file_client: FileServiceClient = Depends(get_file_client)):
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::file_ping"):
        try:
            return await file_client.health()
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail="Internal Server Error")

from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log

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
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::get_aliases"):
        try:
            if not authorization or not authorization.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
            # 실제 인증 로직에 따라 user_id 추출 필요 (예시)
            user_id = "test-user"
            return await file_client.get_aliases(user_id)
        except Exception as e:
            capture_and_log(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
