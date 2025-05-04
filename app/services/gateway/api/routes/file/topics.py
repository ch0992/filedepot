from fastapi import APIRouter, Path, HTTPException, Header
from app.services.gateway.services.impl.file_metadata_service import FileMetadataService
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult

router = APIRouter()
file_metadata_service = FileMetadataService()

from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency, auth_service
from fastapi import Depends

@router.post(
    "/topics/{topic}",
    response_model=KafkaProduceResult,
    tags=["file"],
    summary="Kafka를 통한 메타데이터 적재",
    description="단건 메타 정보를 Kafka topic으로 발행합니다."
)
async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = ...,
    authorization: str = Header(..., description="Bearer accessToken")
):
    from app.services.log.tracing import get_tracer
    from app.services.log.exceptions import capture_and_log
    import logging
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::produce_metadata_to_kafka"):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
        try:
            result = await file_metadata_service.produce_metadata(topic, body)
            return result
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail=str(e))
