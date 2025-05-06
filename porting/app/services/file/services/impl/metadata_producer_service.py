"""
[📄 metadata_producer_service.py - File 서비스 구현체]

설명:
- 파일 메타데이터를 Kafka로 발행하는 서비스 구현체
- Kafka 토픽명과 메타데이터를 받아 발행 처리

주요 연동:
- MetadataProducerInterface (인터페이스)
"""

from app.services.file.services.interfaces.metadata_producer_interface import MetadataProducerInterface
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.common.broker.impl.kafka_message_producer import KafkaMessageProducer
import json

# Initialize Kafka producer instance
kafka_producer = KafkaMessageProducer()

class MetadataProducerService(MetadataProducerInterface):
    """
    파일 메타데이터 Kafka 발행 서비스 구현체
    """
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        """
        Kafka로 파일 메타데이터 발행
        Args:
            topic (str): Kafka 토픽명
            body (FileMetadataRequest): 발행할 메타데이터
        Returns:
            KafkaProduceResult: 발행 결과
        """
        try:
            # WHY: Kafka producer를 통해 메타데이터 발행
            await kafka_producer.produce(topic, body.dict())
            
            # WHY: 발행한 메타데이터를 JSON 형식으로 변환
            message = json.dumps(body.dict(), ensure_ascii=False)
            
            # WHY: 발행 결과를 반환
            return KafkaProduceResult(
                topic=topic,
                message=message,
                status="queued"
            )
        except Exception as e:
            capture_and_log(e, None)
            return KafkaProduceResult(
                topic=topic,
                message=str(e),
                status="error"
            )
