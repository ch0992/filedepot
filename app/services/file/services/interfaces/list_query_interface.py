from abc import ABC, abstractmethod
from typing import List
from app.services.file.schemas.listing import S3FileEntry

class ListQueryInterface(ABC):
    @abstractmethod
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        pass

    @staticmethod
    def get_service():
        from app.services.file.services.impl.list_query_service import ListQueryService
        return ListQueryService()
