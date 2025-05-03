from app.services.file.services.interfaces.presigned_interface import PresignedInterface
from app.services.file.schemas.presigned import PresignedURLResponse

class PresignedService(PresignedInterface):
    async def create_presigned_url(self, file_path: str) -> PresignedURLResponse:
        # 실제로는 MinIO 또는 AWS S3 SDK 활용
        # 여기서는 더미 presigned URL 반환
        url = f"https://minio.local/bucket/{file_path}?presigned=1"
        return PresignedURLResponse(url=url, expires_in=3600)
