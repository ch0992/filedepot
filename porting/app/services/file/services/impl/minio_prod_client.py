"""
[📄 minio_prod_client.py - File 서비스 구현체]

설명:
- Minio S3 연동을 위한 실제 운영 클라이언트 구현체
- S3 버킷/키/파일을 받아 실제 업로드 수행

주요 연동:
- MinioClientInterface (인터페이스)
"""

from app.services.file.services.interfaces.minio_client_interface import MinioClientInterface
# 실제 환경에서는 minio/minio-py, boto3 등으로 구현

class MinioProdClient(MinioClientInterface):
    """
    Minio S3 연동 운영 클라이언트 구현체
    """
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        """
        실제 S3에 파일 업로드
        Args:
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            data (bytes): 업로드할 파일 데이터
        Returns:
            str: 업로드 결과 (S3/MinIO URL)
        """
        # WHY: 실제 S3 업로드 로직은 운영 환경에서만 사용
        # TODO: 실제 MinIO/S3 연동 코드 구현
        # 예시: minio_client.put_object(bucket, key, io.BytesIO(data), len(data))
        # 반환: S3/MinIO URL
        raise NotImplementedError("Production MinioClient not implemented.")

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        """
        실제 S3에 파일 멀티파트 업로드
        Args:
            file_path (str): 업로드할 파일 경로
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            chunk_size (int): 멀티파트 업로드 청크 크기 (기본값: 20MB)
        Returns:
            str: 업로드 결과 (S3/MinIO URL)
        """
        # WHY: 실제 S3 멀티파트 업로드 로직은 운영 환경에서만 사용
        # TODO: 실제 MinIO/S3 멀티파트 업로드 구현
        raise NotImplementedError("Production MinioClient multipart not implemented.")
