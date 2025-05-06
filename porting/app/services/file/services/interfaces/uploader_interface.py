"""
[📄 uploader_interface.py - File 서비스 인터페이스]

설명:
- 파일 업로드를 위한 추상 인터페이스 정의
- 실제 구현체(impl/uploader_service.py)에서 상속 및 구현

주요 연동:
- UploaderService (구현체)
"""

from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any

class UploaderInterface(ABC):
    """
    파일 업로드 인터페이스 (추상)
    - 실제 구현체는 UploaderService
    """
    @abstractmethod
    async def upload_file(self, file: UploadFile) -> Any:
        """
        파일을 업로드 (구현체에서 구현)
        Args:
            file (UploadFile): 업로드할 파일
        Returns:
            Any: 업로드 결과
        """
        pass

    @staticmethod
    def get_service():
        """
        실제 구현체 인스턴스 반환 (factory)
        Returns:
            UploaderService: 실제 구현체
        """
        from app.services.file.services.impl.uploader_service import UploaderService
        return UploaderService()
