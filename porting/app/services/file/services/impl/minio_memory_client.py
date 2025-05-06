"""
[📄 minio_memory_client.py - File 서비스 구현체]

설명:
- Minio S3 연동을 위한 메모리 기반 클라이언트 구현체 (테스트/로컬용)
- 실제 S3 업로드 대신 메모리 내 객체 저장

주요 연동:
- MinioClientInterface (인터페이스)
"""

from app.services.file.services.interfaces.minio_client_interface import MinioClientInterface
from typing import Any

class MinioMemoryClient(MinioClientInterface):
    """
    Minio S3 연동 메모리 클라이언트 구현체 (테스트/로컬)

    테스트/로컬/개발 환경에서만 사용하는 in-memory S3 mock 구현체
    """

    def __init__(self):
        """
        MinioMemoryClient 초기화

        메모리 내 객체 저장을 위한 초기화
        """
        # WHY: 메모리 내 객체 저장을 위한 초기화
        self.storage = {}

    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        """
        메모리 내에 파일 업로드 (테스트/로컬)

        Args:
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            data (bytes): 업로드할 파일 데이터

        Returns:
            str: 업로드 결과 (메모리 내 객체 경로)
        """
        # WHY: 버킷이 존재하지 않을 경우 생성
        if bucket not in self.storage:
            self.storage[bucket] = {}
        # WHY: 파일 데이터를 메모리 내 객체 저장
        self.storage[bucket][key] = data
        return f"memory://{bucket}/{key}"

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        with open(file_path, "rb") as f:
            data = f.read()
        return self.upload_file(bucket, key, data)
