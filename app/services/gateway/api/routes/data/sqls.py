from fastapi import APIRouter, HTTPException, Body, Header, status
from app.core.config import settings
from app.common.clients.data_service_client import DataServiceClient
from typing import Optional

router = APIRouter(prefix="/data")
data_client = DataServiceClient(settings.DATA_SERVICE_URL)

@router.post(
    "/imgplt/sqls",
    tags=["Data"],
    summary="SQL 실행 결과 조회",
    description="임의 SQL을 실행하고 결과를 반환합니다."
)
async def get_sql_result(
    sql: str = Body(..., embed=True),
    authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await data_client._request("POST", "/imgplt/sqls", json={"sql": sql}, headers={"Authorization": f"Bearer {access_token}"})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
