from app.services.file.services.interfaces.minio_client_interface import MinioClientInterface
# 실제 환경에서는 minio/minio-py, boto3 등으로 구현

class MinioProdClient(MinioClientInterface):
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        # TODO: 실제 MinIO/S3 연동 코드 구현
        # 예시: minio_client.put_object(bucket, key, io.BytesIO(data), len(data))
        # 반환: S3/MinIO URL
        raise NotImplementedError("Production MinioClient not implemented.")

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        # TODO: 실제 MinIO/S3 multipart upload 구현
        raise NotImplementedError("Production MinioClient multipart not implemented.")
