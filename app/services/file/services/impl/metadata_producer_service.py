from app.services.file.services.interfaces.metadata_producer_interface import MetadataProducerInterface
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult
from app.common.broker.impl.kafka_message_producer import KafkaMessageProducer
from app.services.log.exceptions import capture_and_log
import json

kafka_producer = KafkaMessageProducer()

class MetadataProducerService(MetadataProducerInterface):
    async def produce_metadata(self, topic: str, body: FileMetadataRequest) -> KafkaProduceResult:
        try:
            await kafka_producer.produce(topic, body.dict())
            message = json.dumps(body.dict(), ensure_ascii=False)
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
