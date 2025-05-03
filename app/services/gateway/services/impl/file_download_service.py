from app.services.gateway.services.interfaces.file_download_interface import FileDownloadInterface
from app.services.file.services.interfaces.presigned_interface import PresignedInterface
from app.services.file.services.impl.presigned_service import PresignedService
from app.services.file.schemas.presigned import PresignedURLResponse

class FileDownloadService(FileDownloadInterface):
    def __init__(self):
        self.presigned_service: PresignedInterface = PresignedService()

    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        return await self.presigned_service.create_presigned_url(file_path)
