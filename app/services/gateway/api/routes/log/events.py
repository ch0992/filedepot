from fastapi import APIRouter, Header, HTTPException, status, Body
from app.common.clients.log_service_client import LogServiceClient
from app.core.config import settings
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter(prefix="/log")
log_client = LogServiceClient(settings.LOG_SERVICE_URL)

@router.post("/event", tags=["Log"], summary="로그 이벤트 기록")
async def log_event(event: dict = Body(...), 
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
    else:
        access_token = None
    try:
        # LogServiceClient.log_event는 event만 받으므로, access_token은 사용하지 않음
        result = await log_client.log_event(event)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
