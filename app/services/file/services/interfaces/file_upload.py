"""
IFileUploadService: 파일 업로드 기능 인터페이스 정의
"""
from typing import Protocol
from pydantic import BaseModel

class FileUploadRequest(BaseModel):
    filename: str
    content: bytes

class FileUploadResponse(BaseModel):
    url: str

class IFileUploadService(Protocol):
    def upload(self, req: FileUploadRequest) -> FileUploadResponse:
        ...
