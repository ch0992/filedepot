from fastapi import APIRouter, Path, HTTPException, Body, Header, status, Depends
from typing import Optional
from app.services.gateway.services.impl.data_producer_service import DataProducerService
from app.services.gateway.services.impl.auth_module_service import AuthModuleService
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult
from app.common.clients.data_service_client import DataServiceClient
from app.core.config import settings

router = APIRouter(prefix="/data")
data_producer_service = DataProducerService()

def get_data_client():
    return DataServiceClient(settings.DATA_SERVICE_URL)

@router.get("/ping", summary="Data health check", tags=["Health"])
async def data_ping(data_client: DataServiceClient = Depends(get_data_client)):
    """Data 서비스 헬스 체크 엔드포인트 (실제 data 서비스로 전달)"""
    return await data_client.health()

@router.get(
    "/topics",
    tags=["data"],
    summary="토픽 목록 조회",
    description="등록된 Kafka 토픽 목록을 조회합니다."
)
async def get_topics():
    # 실제로는 data 서비스에서 토픽 목록을 가져와야 함
    return ["topic-a", "topic-b"]

def get_data_client():
    return DataServiceClient(settings.DATA_SERVICE_URL)

@router.post(
    "/topics/{table}",
    tags=["data"],
    summary="Kafka 토픽에 데이터 적재",
    description="지정한 테이블(Kafka 토픽)에 데이터를 적재합니다."
)
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka topic명(Mart 테이블명)"),
    body: dict = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken"),
    data_client: DataServiceClient = Depends(get_data_client)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    # 실제 인증 로직에 따라 user_id 추출 필요 (예시)
    user_id = "test-user"
    # data 서비스의 produce_table_record_to_kafka API 호출
    return await data_client._request("POST", f"/topics/{table}", json=body)
