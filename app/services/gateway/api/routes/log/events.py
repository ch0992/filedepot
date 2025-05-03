from fastapi import APIRouter, Header, HTTPException, status, Depends, Body
from typing import Optional
from app.common.clients.log_service_client import LogServiceClient
from app.core.config import settings

router = APIRouter(prefix="/log")

def get_log_client():
    return LogServiceClient(settings.LOG_SERVICE_URL)

@router.get("/ping", summary="Log health check", tags=["Health"])
async def log_ping(log_client: LogServiceClient = Depends(get_log_client)):
    """Log 서비스 헬스 체크 엔드포인트 (실제 log 서비스로 전달)"""
    return await log_client.health()

@router.post("/log/event", tags=["log"], summary="로그 이벤트 기록")
async def log_event(
    event: dict = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken"),
    log_client: LogServiceClient = Depends(get_log_client)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    return await log_client.log_event(event)
