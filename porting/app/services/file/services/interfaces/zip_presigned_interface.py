"""
[📄 zip_presigned_interface.py - File 서비스 인터페이스]

설명:
- S3 zip presigned URL 생성을 위한 추상 인터페이스 정의
- 실제 구현체(impl/zip_presigned_service.py)에서 상속 및 구현

주요 연동:
- ZipPresignedService (구현체)
"""

from abc import ABC, abstractmethod
from app.services.file.schemas.zips import ZipPresignedResponse

class ZipPresignedInterface(ABC):
    """
    S3 zip presigned URL 생성 인터페이스 (추상)
    - 실제 구현체는 ZipPresignedService
    """
    @abstractmethod
    async def create_zip_presigned_url(self, sql: str) -> ZipPresignedResponse:
        """
        S3 zip presigned URL을 생성 (구현체에서 구현)
        Args:
            sql (str): SQL 쿼리문
        Returns:
            ZipPresignedResponse: presigned URL 응답
        """
        pass
