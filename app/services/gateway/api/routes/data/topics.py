from fastapi import APIRouter, Path, HTTPException, Body, Header, status
from typing import Optional
from app.services.gateway.services.impl.data_producer_service import DataProducerService
from app.services.gateway.services.impl.auth_module_service import AuthModuleService
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

router = APIRouter(prefix="/data")
data_producer_service = DataProducerService()
auth_service = AuthModuleService()

@router.post(
    "/topics/{table}",
    response_model=KafkaProduceResult,
    tags=["data"],
    summary="Kafka를 통한 Mart 단건 적재",
    description="Mart 테이블로 전송할 단건 데이터를 Kafka topic에 발행합니다."
)
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka topic명(Mart 테이블명)"),
    body: TableRecordRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    await auth_service.verify_token_and_get_workspaces(access_token)
    try:
        result = await data_producer_service.produce_record(table, body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
