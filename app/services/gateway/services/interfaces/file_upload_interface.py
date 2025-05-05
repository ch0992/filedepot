from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any

class FileUploadInterface(ABC):
    @abstractmethod
    async def upload_file_and_metadata(self, topic: str, file: UploadFile, metadata: str) -> Any:
        pass

    @staticmethod
    def get_service():
        from app.services.gateway.services.impl.file_upload_service import FileUploadService
        return FileUploadService()
