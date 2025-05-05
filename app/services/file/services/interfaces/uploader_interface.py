from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Any

class UploaderInterface(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile) -> Any:
        pass

    @staticmethod
    def get_service():
        from app.services.file.services.impl.uploader_service import UploaderService
        return UploaderService()
