from app.services.gateway.services.interfaces.data_producer_interface import DataProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult
from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.services.impl.table_producer_service import TableProducerService

class DataProducerService(DataProducerInterface):
    def __init__(self):
        self.producer: TableProducerInterface = TableProducerService()

    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        return await self.producer.produce_record(table, body)
