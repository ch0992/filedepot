"""
[📄 minio_client_interface.py - File 서비스 인터페이스]

설명:
- Minio S3 연동을 위한 추상 인터페이스 정의
- 실제 구현체(impl/minio_prod_client.py)에서 상속 및 구현

주요 연동:
- MinioProdClient (구현체)
"""

from abc import ABC, abstractmethod
from typing import Any

class MinioClientInterface(ABC):
    """
    Minio S3 연동 인터페이스 (추상)
    - 실제 구현체는 MinioProdClient
    """
    @abstractmethod
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        """
        Minio S3에 파일 업로드 (구현체에서 구현)
        Args:
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            data (bytes): 업로드할 파일 데이터
        Returns:
            str: 업로드 결과
        """
        pass

    @abstractmethod
    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        """
        Minio S3에 파일 멀티파트 업로드 (구현체에서 구현)
        Args:
            file_path (str): 로컬 파일 경로
            bucket (str): S3 버킷명
            key (str): S3 오브젝트 키
            chunk_size (int): 멀티파트 업로드 청크 크기 (기본값: 20MB)
        Returns:
            str: 업로드 결과
        """
        pass
