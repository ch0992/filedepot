from app.services.file.services.interfaces.metadata_producer_interface import MetadataProducerInterface
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
import json

class MetadataProducerService(MetadataProducerInterface):
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        # Kafka 발행 로직은 실제 환경에서는 aiokafka 등 비동기 Kafka 클라이언트 사용
        # 여기서는 시뮬레이션 (실제 Kafka 연결/발행 코드로 교체 필요)
        # 예시: 성공적으로 발행했다고 가정
        message = json.dumps(body.dict(), ensure_ascii=False)
        # 실제 Kafka 발행 시 producer.send_and_wait(topic, message) 등 사용
        return KafkaProduceResult(
            topic=topic,
            message=message,
            status="success"
        )
