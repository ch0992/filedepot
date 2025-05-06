"""
[📄 kafka_dummy_producer.py - Kafka Dummy Producer]

설명:
- 테스트/로컬 환경에서 Kafka 대신 로그로 메시지를 출력하는 더미 프로듀서 구현체
- 실제 Kafka 연동 없이 메시지 발행 로직을 검증할 때 사용

주요 연동:
- MessageProducerInterface (interface)

구현:
- MessageProducerInterface를 구현하여 Kafka 메시지 발행 로직을 제공
- 실제 Kafka 연동 없이 로그 출력을 통해 메시지 발행을 시뮬레이션

사용 방법:
- MessageProducerInterface를 사용하는 코드에서 DummyKafkaProducer를 대신 사용
- 실제 Kafka 연동 없이 메시지 발행 로직을 검증
"""

from app.common.interfaces.message_producer_interface import MessageProducerInterface

class DummyKafkaProducer(MessageProducerInterface):
    """
    Kafka Dummy Producer

    - 실제 Kafka로 메시지를 보내지 않고, 로그로만 출력
    - 개발/테스트 환경에서 Kafka 연동 대체용
    """
    async def produce(self, topic: str, value: dict):
        """
        더미 Kafka 메시지 발행 (로그 출력)

        Args:
            topic (str): 메시지 발행 대상 토픽
            value (dict): 발행할 메시지 데이터

        Returns:
            dict: 발행 결과 (토픽명, 상태)
        """
        # WHY: 실제 Kafka 연동 없이 메시지 발행 로직을 검증하기 위함
        print(f"[DummyKafkaProducer] topic={topic}, value={value}")
        return {"topic": topic, "status": "dummy"}
