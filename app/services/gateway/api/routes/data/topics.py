from fastapi import APIRouter, Path, HTTPException, Body, Header
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult
from app.common.clients.data_service_client import DataServiceClient
from app.core.config import settings
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter(prefix="/data")
data_client = DataServiceClient(settings.DATA_SERVICE_URL)

@router.get("/topics", summary="토픽 목록 조회", tags=["Data"])
async def get_topics(authorization: Optional[str] = Header(None, description="Bearer accessToken")):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        headers = {}
    try:
        result = await data_client._request(
            "GET", "/topics",
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/topics/{table}",
    response_model=KafkaProduceResult,
    tags=["Data"],
    summary="Kafka를 통한 Mart 단건 적재",
    description="Mart 테이블로 전송할 단건 데이터를 Kafka topic에 발행합니다."
)
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka topic명(Mart 테이블명)"),
    body: TableRecordRequest = Body(...),
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
            "POST", f"/topics/{table}",
            json=body.dict(),
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
