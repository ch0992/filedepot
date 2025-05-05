from app.services.file.services.interfaces.minio_client_interface import MinioClientInterface

class MinioMemoryClient(MinioClientInterface):
    """
    테스트/로컬/개발 환경에서만 사용하는 in-memory S3 mock 구현체
    """
    def __init__(self):
        self.storage = {}

    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        if bucket not in self.storage:
            self.storage[bucket] = {}
        self.storage[bucket][key] = data
        return f"memory://{bucket}/{key}"

    def multipart_upload(self, file_path: str, bucket: str, key: str, chunk_size: int = 20*1024*1024) -> str:
        with open(file_path, "rb") as f:
            data = f.read()
        return self.upload_file(bucket, key, data)
