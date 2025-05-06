from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

from app.common.kafka_producer import KafkaMessageProducer

class TableProducerService(TableProducerInterface):
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        producer = KafkaMessageProducer()
        result = await producer.produce(table, body.dict())
        return KafkaProduceResult(topic=table, message=json.dumps(body.dict()), status=result["status"])

