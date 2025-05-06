"""
[📄 metadata_producer_interface.py - File 서비스 인터페이스]

설명:
- 파일 메타데이터를 Kafka로 발행하는 추상 인터페이스 정의
- 실제 구현체(impl/metadata_producer_service.py)에서 상속 및 구현

주요 연동:
- MetadataProducerService (구현체)
"""

from abc import ABC, abstractmethod
from typing import Any

class MetadataProducerInterface(ABC):
    """
    파일 메타데이터 Kafka 발행 인터페이스 (추상)
    - 실제 구현체는 MetadataProducerService
    """
    @abstractmethod
    async def produce_metadata(self, topic: str, metadata: Any) -> dict:
        """
        파일 메타데이터를 Kafka로 발행 (구현체에서 구현)
        Args:
            topic (str): Kafka 토픽명
            metadata (Any): 발행할 메타데이터
        Returns:
            dict: 발행 결과
        """
        pass

    @staticmethod
    def get_service():
        """
        실제 구현체 인스턴스 반환 (factory)
        Returns:
            MetadataProducerService: 실제 구현체
        """
        from app.services.file.services.impl.metadata_producer_service import MetadataProducerService
        return MetadataProducerService()
