from fastapi import APIRouter, Path, HTTPException, Header, Body
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.post(
    "/topics/{topic}",
    response_model=KafkaProduceResult,
    tags=["file"],
    summary="Kafka를 통한 메타데이터 적재",
    description="단건 메타 정보를 Kafka topic으로 발행합니다."
)
async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = Body(...),
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await file_client._request(
            "POST", f"/topics/{topic}",
            json=body.dict(),
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
