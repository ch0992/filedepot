from fastapi import APIRouter, Path, status, Header
from app.common.exceptions import BadRequestException, NotFoundException, SystemConfigException
from app.services.gateway.services.impl.file_metadata_service import FileMetadataService
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.core.config import settings
from app.services.log.tracing import get_tracer
from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency, auth_service
from fastapi import Depends
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter()
file_metadata_service = FileMetadataService()
tracer = get_tracer("gateway")

@router.post(
    "/topics/{topic}",
    response_model=KafkaProduceResult,
    tags=["File"],
    summary="Kafka를 통한 메타데이터 적재",
    description="단건 메타 정보를 Kafka topic으로 발행합니다."
)

async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = ...,
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    

    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
    # local 모드면 인증 생략
    try:
        result = await file_metadata_service.produce_metadata(topic, body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
