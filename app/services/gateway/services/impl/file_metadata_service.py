from app.services.gateway.services.interfaces.file_metadata_interface import FileMetadataInterface
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.services.file.services.impl.metadata_producer_service import MetadataProducerService

class FileMetadataService(FileMetadataInterface):
    def __init__(self):
        self.producer = MetadataProducerService()

    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        return await self.producer.produce_metadata(topic, body)
