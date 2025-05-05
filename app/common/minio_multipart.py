# S3(Minio) Multipart Upload Helper (boto3 스타일, 실제 구현은 minio-py 등으로 대체 가능)
# 실제 S3 연동은 환경에 따라 적절히 교체하세요.

import math
from typing import BinaryIO, List

class MultipartUploadResult:
    def __init__(self, success: bool, parts: List[dict], location: str = "", error: str = ""):
        self.success = success
        self.parts = parts
        self.location = location
        self.error = error

class DummyMinioMultipartClient:
    """
    실제 환경에서는 boto3.client('s3') 또는 minio.Minio 객체로 대체하세요.
    이 예시는 구조만 보여줍니다.
    """
    def __init__(self):
        self.storage = {}

    def create_multipart_upload(self, bucket: str, key: str) -> str:
        upload_id = f"dummy-upload-{key}"
        self.storage[upload_id] = []
        return upload_id

    def upload_part(self, bucket: str, key: str, upload_id: str, part_number: int, data: bytes) -> dict:
        # 실제 S3/Minio는 ETag 등 반환
        self.storage[upload_id].append((part_number, data))
        return {"ETag": f"etag-{part_number}", "PartNumber": part_number}

    def complete_multipart_upload(self, bucket: str, key: str, upload_id: str, parts: List[dict]) -> str:
        # 실제 S3/Minio는 파일을 조립
        return f"https://dummy-s3/{bucket}/{key}"

    def abort_multipart_upload(self, bucket: str, key: str, upload_id: str):
        if upload_id in self.storage:
            del self.storage[upload_id]

async def multipart_upload(file: BinaryIO, bucket: str, key: str, client: DummyMinioMultipartClient, chunk_size: int = 20*1024*1024) -> MultipartUploadResult:
    upload_id = client.create_multipart_upload(bucket, key)
    parts = []
    part_number = 1
    try:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            part = client.upload_part(bucket, key, upload_id, part_number, data)
            parts.append(part)
            part_number += 1
        location = client.complete_multipart_upload(bucket, key, upload_id, parts)
        return MultipartUploadResult(True, parts, location)
    except Exception as e:
        client.abort_multipart_upload(bucket, key, upload_id)
        return MultipartUploadResult(False, parts, error=str(e))
