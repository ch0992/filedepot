"""
[📄 presigned_interface.py - File 서비스 인터페이스]

설명:
- S3 presigned URL 생성을 위한 추상 인터페이스 정의
- 실제 구현체(impl/presigned_service.py)에서 상속 및 구현

주요 연동:
- PresignedService (구현체)
"""

from typing import Protocol
from app.services.file.schemas.presigned import PresignedURLResponse

class PresignedInterface(Protocol):
    """
    S3 presigned URL 생성 인터페이스 (추상)
    - 실제 구현체는 PresignedService
    """
    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        """
        S3 presigned URL을 생성 (구현체에서 구현)
        Args:
            file_path (str): 파일 경로
        Returns:
            PresignedURLResponse: presigned URL 응답
        """
        ...
