from abc import ABC, abstractmethod
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

class TableProducerInterface(ABC):
    @abstractmethod
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        pass
