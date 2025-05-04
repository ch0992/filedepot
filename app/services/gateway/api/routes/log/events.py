from fastapi import APIRouter, Header, HTTPException, status, Depends, Body
from typing import Optional
from app.common.clients.log_service_client import LogServiceClient
from app.core.config import settings

router = APIRouter(prefix="/log")

def get_log_client():
    return LogServiceClient(settings.LOG_SERVICE_URL)

from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log
import logging

@router.get("/ping", summary="Log health check", tags=["Health"])
async def log_ping(log_client: LogServiceClient = Depends(get_log_client)):
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::log_ping"):
        try:
            return await log_client.health()
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/log/event", tags=["log"], summary="로그 이벤트 기록")
async def log_event(
    event: dict = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken"),
    log_client: LogServiceClient = Depends(get_log_client)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    return await log_client.log_event(event)
