"""
[📄 list_query_interface.py - File 서비스 인터페이스]

설명:
- S3 prefix 기반 파일 목록 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/list_query_service.py)에서 상속 및 구현

주요 연동:
- S3FileEntry 스키마
- ListQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.services.file.schemas.listing import S3FileEntry

class ListQueryInterface(ABC):
    """
    S3 prefix 파일 목록 조회 인터페이스 (추상)

    - 실제 구현체는 ListQueryService
    """
    @abstractmethod
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        """
        S3 prefix로 파일 목록을 조회 (구현체에서 구현)

        Args:
            prefix (str): S3 prefix 경로
        Returns:
            List[S3FileEntry]: S3 파일 목록
        """
        pass

    @staticmethod
    def get_service():
        """
        실제 구현체 인스턴스 반환 (factory)
        Returns:
            ListQueryService: 실제 구현체
        """
        from app.services.file.services.impl.list_query_service import ListQueryService
        return ListQueryService()
