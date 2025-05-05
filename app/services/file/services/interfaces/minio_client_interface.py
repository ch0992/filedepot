from abc import ABC, abstractmethod

class MinioClientInterface(ABC):
    @abstractmethod
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        pass
    @abstractmethod
    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        pass
