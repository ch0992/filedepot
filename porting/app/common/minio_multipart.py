# [📄 minio_multipart.py - Minio Multipart Uploader]

# 설명:
# - Minio S3 호환 스토리지에 멀티파트 업로드를 수행하는 유틸리티 클래스
# - 파일 업로드를 위한 래퍼 및 예외처리 포함

# 주요 연동:
# - minio (Minio SDK)

import math
from typing import BinaryIO, List

class MultipartUploadResult:
    """
    멀티파트 업로드 결과

    - 업로드 성공 여부
    - 업로드된 파트 목록
    - 업로드된 파일 위치
    - 에러 메시지 (실패 시)
    """
    def __init__(self, success: bool, parts: List[dict], location: str = "", error: str = ""):
        """
        MultipartUploadResult 생성자

        Args:
            success (bool): 업로드 성공 여부
            parts (List[dict]): 업로드된 파트 목록
            location (str): 업로드된 파일 위치 (성공 시)
            error (str): 에러 메시지 (실패 시)
        """
        self.success = success
        self.parts = parts
        self.location = location
        self.error = error

class DummyMinioMultipartClient:
    """
    Minio Multipart Client (Dummy)

    - 실제 환경에서는 boto3.client('s3') 또는 minio.Minio 객체로 대체하세요.
    - 이 예시는 구조만 보여줍니다.
    """
    def __init__(self):
        """
        DummyMinioMultipartClient 생성자
        """
        # WHY: 테스트를 위한 Dummy Minio Client
        self.storage = {}

    def create_multipart_upload(self, bucket: str, key: str) -> str:
        """
        멀티파트 업로드를 생성

        Args:
            bucket (str): 버킷명
            key (str): 업로드할 파일 키

        Returns:
            str: 업로드 ID
        """
        # WHY: 업로드 ID 생성
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
