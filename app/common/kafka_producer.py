import json
from faststream.kafka import KafkaBroker
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface

broker = KafkaBroker("localhost:9092")

class KafkaMessageProducer(MessageProducerInterface):
    async def produce(self, topic: str, value: dict):
        try:
            message = json.dumps(value, ensure_ascii=False)
            await broker.publish(message, topic)
            return {"topic": topic, "status": "queued"}
        except Exception as e:
            raise RuntimeError(f"Kafka produce failed: {e}")
