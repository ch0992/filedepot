from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface

class DummyKafkaProducer(MessageProducerInterface):
    async def produce(self, topic: str, value: dict):
        print(f"[DummyKafkaProducer] topic={topic}, value={value}")
        return {"topic": topic, "status": "dummy"}
