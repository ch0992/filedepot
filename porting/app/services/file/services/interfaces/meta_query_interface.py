"""
[📄 meta_query_interface.py - File 서비스 인터페이스]

설명:
- 파일 메타데이터 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/meta_query_service.py)에서 상속 및 구현

주요 연동:
- FileMeta 스키마
- MetaQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.services.file.schemas.meta import FileMeta

class MetaQueryInterface(ABC):
    """
    파일 메타데이터 조회 인터페이스 (추상)
    - 실제 구현체는 MetaQueryService
    """
    @abstractmethod
    async def get_file_meta(self, file_key: str) -> FileMeta:
        """
        파일 메타데이터를 조회 (구현체에서 구현)
        Args:
            file_key (str): 파일 키
        Returns:
            FileMeta: 파일 메타데이터
        """
        pass

    @staticmethod
    def get_service():
        """
        실제 구현체 인스턴스 반환 (factory)
        Returns:
            MetaQueryService: 실제 구현체
        """
        from app.services.file.services.impl.meta_query_service import MetaQueryService
        return MetaQueryService()
