import json
import os
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface
from app.common.kafka_dummy_producer import DummyKafkaProducer
from faststream.kafka import KafkaBroker
from app.core.config import settings

class KafkaMessageProducer(MessageProducerInterface):
    def __init__(self):
        if settings.ENV in ["production", "stage"]:
            self._broker = KafkaBroker(os.getenv("KAFKA_BROKER_URL", "localhost:9092"))
            self._dummy = False
        else:
            self._dummy = True
            self._dummy_producer = DummyKafkaProducer()

    async def produce(self, topic: str, value: dict):
        if self._dummy:
            return await self._dummy_producer.produce(topic, value)
        try:
            message = json.dumps(value, ensure_ascii=False)
            await self._broker.connect()
            await self._broker.publish(message, topic)
            await self._broker.disconnect()
            return {"topic": topic, "status": "queued"}
        except Exception as e:
            raise RuntimeError(f"Kafka produce failed: {e}")
