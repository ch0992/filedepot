from abc import ABC, abstractmethod
from typing import List
from app.services.file.schemas.listing import S3FileEntry

class FileListInterface(ABC):
    @abstractmethod
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        pass

    @staticmethod
    def get_service():
        from app.services.gateway.services.impl.file_list_service import FileListService
        return FileListService()
