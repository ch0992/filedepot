from fastapi import APIRouter, HTTPException, Body, Header
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult
from app.common.clients.data_service_client import DataServiceClient
from app.core.config import settings

router = APIRouter()

@router.post(
    "/imgplt/curs",
    summary="Cursor 기반 대용량 레코드 조회",
    tags=["data"],
    description="SQL 기반 대용량 데이터를 cursor 키를 기준으로 나누어 순차적으로 조회합니다."
)
async def cursor_query_endpoint(
    body: CursorQueryRequest = Body(...),
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await data_client._request(
            "POST", "/imgplt/curs",
            json=body.dict(),
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
