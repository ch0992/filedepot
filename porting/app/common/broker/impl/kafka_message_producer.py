import json
from faststream.kafka import KafkaBroker
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface
from app.services.log.exceptions import capture_and_log

broker = KafkaBroker("localhost:9092")

class KafkaMessageProducer(MessageProducerInterface):
    async def produce(self, topic: str, value: dict):
        try:
            message = json.dumps(value, ensure_ascii=False)
            await broker.publish(message, topic)
        except Exception as e:
            capture_and_log(e, None)
            raise
