from app.services.data.services.interfaces.table_producer_interface import TableProducerInterface
from app.services.data.schemas.table import TableRecordRequest, KafkaProduceResult

class TableProducerService(TableProducerInterface):
    async def produce_record(self, table: str, body: TableRecordRequest) -> KafkaProduceResult:
        # 실제 환경에서는 Kafka producer를 사용해 메시지를 발행해야 함
        # 여기서는 더미 구현 (메시지 JSON 직렬화)
        import json
        message = json.dumps(body.dict())
        # Kafka 발행 로직 대신 성공 시뮬레이션
        return KafkaProduceResult(topic=table, message=message, status="success")
