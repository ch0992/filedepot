from abc import ABC, abstractmethod
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult

class MetadataProducerInterface(ABC):
    @abstractmethod
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        pass
