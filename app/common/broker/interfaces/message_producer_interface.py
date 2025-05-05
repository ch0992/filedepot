from abc import ABC, abstractmethod

class MessageProducerInterface(ABC):
    """
    인프라 계층: 메시지 브로커(예: Kafka)에 메시지를 발행하는 추상화
    """
    @abstractmethod
    async def produce(self, topic: str, value: dict):
        pass
