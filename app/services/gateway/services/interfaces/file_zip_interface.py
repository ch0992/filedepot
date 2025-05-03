from abc import ABC, abstractmethod
from app.services.file.schemas.zips import ZipPresignedResponse

class FileZipInterface(ABC):
    @abstractmethod
    async def create_zip_presigned_url(self, sql: str) -> ZipPresignedResponse:
        pass
