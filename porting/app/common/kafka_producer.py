"""
[📄 kafka_producer.py - Kafka Producer]

설명:
- 실제 Kafka 브로커에 메시지를 발행하는 프로듀서 구현체
- 토픽, 메시지, 예외처리 등 핵심 로직 포함

주요 연동:
- faststream (KafkaBroker)
- MessageProducerInterface (interface)
"""

import json
import os
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface
from app.common.kafka_dummy_producer import DummyKafkaProducer
from faststream.kafka import KafkaBroker
from app.core.config import settings

class KafkaMessageProducer(MessageProducerInterface):
    """
    Kafka Message Producer

    - 실제 Kafka 브로커에 메시지를 비동기로 발행
    - faststream의 KafkaBroker 사용
    """
    def __init__(self):
        """
        KafkaMessageProducer 생성자

        - 환경에 따라 실제 Kafka 브로커 또는 Dummy 프로듀서 사용
        """
        if settings.ENV in ["production", "stage"]:
            # WHY: production/stage 환경에서는 실제 Kafka 브로커 사용
            self._broker = KafkaBroker(os.getenv("KAFKA_BROKER_URL", "localhost:9092"))
            self._dummy = False
        else:
            # WHY: 개발 환경에서는 Dummy 프로듀서 사용
            self._dummy = True
            self._dummy_producer = DummyKafkaProducer()

    async def produce(self, topic: str, value: dict):
        """
        Kafka 토픽에 메시지 발행

        Args:
            topic (str): 발행 대상 토픽
            value (dict): 발행할 메시지 데이터
        Returns:
            dict: 발행 결과 (토픽명, 상태)
        """
        if self._dummy:
            # WHY: Dummy 프로듀서 사용시 Dummy 프로듀서의 produce 호출
            return await self._dummy_producer.produce(topic, value)
        try:
            # WHY: 메시지 데이터를 JSON으로 직렬화
            message = json.dumps(value, ensure_ascii=False)
            await self._broker.connect()
            await self._broker.publish(message, topic)
            await self._broker.disconnect()
            return {"topic": topic, "status": "queued"}
        except Exception as e:
            # WHY: 예외 발생시 RuntimeError 발생
            raise RuntimeError(f"Kafka produce failed: {e}")
