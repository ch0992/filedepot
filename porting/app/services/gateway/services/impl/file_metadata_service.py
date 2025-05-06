from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

file_client = FileServiceClient(settings.FILE_SERVICE_URL)

class FileMetadataService:
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        result = await file_client._request(
            "POST", f"/topics/{topic}",
            json=body.dict(),
        )
        return KafkaProduceResult(**result)
