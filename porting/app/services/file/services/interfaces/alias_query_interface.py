"""
[📄 alias_query_interface.py - File 서비스 인터페이스]

설명:
- 파일 alias 목록 조회를 위한 추상 인터페이스 정의
- 실제 구현체(impl/alias_query_service.py)에서 상속 및 구현

주요 연동:
- AliasEntry 스키마
- AliasQueryService (구현체)
"""

from abc import ABC, abstractmethod
from typing import List
from app.services.file.schemas.aliases import AliasEntry

class AliasQueryInterface(ABC):
    """
    파일 alias 목록 조회 인터페이스 (추상)

    - 실제 구현체는 AliasQueryService
    """
    @abstractmethod
    async def get_aliases(self, user_id: str) -> List[AliasEntry]:
        """
        파일 alias 목록을 조회 (구현체에서 구현)

        Args:
            user_id (str): 사용자 ID
        Returns:
            List[AliasEntry]: alias 목록
        """
        pass

    @staticmethod
    def get_service():
        """
        실제 구현체 인스턴스 반환 (factory)
        Returns:
            AliasQueryService: 실제 구현체
        """
        from app.services.file.services.impl.alias_query_service import AliasQueryService
        return AliasQueryService()
