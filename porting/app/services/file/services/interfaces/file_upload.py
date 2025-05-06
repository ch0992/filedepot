"""
[📄 file_upload.py - File 서비스 인터페이스]

설명:
- 파일 및 메타데이터 파일 업로드를 위한 추상 인터페이스 정의
- 실제 구현체(impl/uploader_service.py)에서 상속 및 구현

주요 연동:
- UploaderService (구현체)
"""

from typing import Protocol
from pydantic import BaseModel

class FileUploadRequest(BaseModel):
    """
    파일 업로드 요청 모델
    """
    filename: str  # 업로드할 파일명
    content: bytes  # 업로드할 파일 내용

class FileUploadResponse(BaseModel):
    """
    파일 업로드 응답 모델
    """
    url: str  # 업로드된 파일 URL

class IFileUploadService(Protocol):
    """
    파일 업로드 인터페이스 (추상)
    - 실제 구현체는 UploaderService
    """
    def upload(self, req: FileUploadRequest) -> FileUploadResponse:
        """
        파일 업로드 (구현체에서 구현)
        Args:
            req (FileUploadRequest): 파일 업로드 요청 모델
        Returns:
            FileUploadResponse: 파일 업로드 응답 모델
        """
        ...
