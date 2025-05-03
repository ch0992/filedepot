from typing import Protocol
from app.services.file.schemas.presigned import PresignedURLResponse

class FileDownloadInterface(Protocol):
    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        ...
