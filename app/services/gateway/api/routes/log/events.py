from fastapi import APIRouter, Header, HTTPException, status, Body
from app.common.clients.log_service_client import LogServiceClient
from app.core.config import settings

router = APIRouter(prefix="/log")
log_client = LogServiceClient(settings.LOG_SERVICE_URL)

@router.post("/event", tags=["Log"], summary="로그 이벤트 기록")
async def log_event(event: dict = Body(...), authorization: str = Header(..., description="Bearer accessToken")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await log_client.log_event(event, access_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
