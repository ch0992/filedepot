from app.services.gateway.services.interfaces.file_zip_interface import FileZipInterface
from app.services.file.schemas.zips import ZipPresignedResponse
from app.services.file.services.impl.zip_presigned_service import ZipPresignedService

class FileZipService(FileZipInterface):
    def __init__(self):
        self.zip_presigned_service = ZipPresignedService()

    async def create_zip_presigned_url(self, sql: str) -> ZipPresignedResponse:
        return await self.zip_presigned_service.create_zip_presigned_url(sql)
