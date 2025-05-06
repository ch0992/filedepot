from fastapi import APIRouter, HTTPException, Body, Header
from app.services.data.schemas.curs import CursorQueryRequest
from app.common.clients.data_service_client import DataServiceClient
from app.core.config import settings
from app.common.utils.auth_mode import get_auth_mode
from typing import Optional


router = APIRouter()
data_client = DataServiceClient(settings.DATA_SERVICE_URL)

@router.post(
    "/imgplt/curs",
    summary="Cursor 기반 대용량 레코드 조회",
    tags=["Data"],
    description="SQL 기반 대용량 데이터를 cursor 키를 기준으로 나누어 순차적으로 조회합니다."
)
async def cursor_query_endpoint(
    body: CursorQueryRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        headers = {}
    try:
        result = await data_client._request(
            "POST", "/imgplt/curs",
            json=body.dict(),
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
