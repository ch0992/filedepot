"""
[📄 list_query_service.py - File 서비스 구현체]

설명:
- S3(Minio)에서 prefix로 파일 목록을 조회하는 서비스 구현체
- 환경변수(MINIO_BUCKET 등) 체크 및 예외처리
- boto3를 통한 S3 연동, pagination 처리

주요 연동:
- boto3 S3 client
- 환경변수: MINIO_BUCKET, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
"""

from app.services.file.services.interfaces.list_query_interface import ListQueryInterface
from app.services.file.schemas.listing import S3FileEntry
from app.core.logging import get_tracer, capture_and_log
import os
import boto3
from typing import List

tracer = get_tracer("file::list_files")

class ListQueryService(ListQueryInterface):
    """
    S3 prefix 파일 목록 조회 서비스 구현체

    - S3의 지정된 prefix로 파일 목록을 조회
    - 환경변수 및 S3 연결 오류, 파일 없음 등 예외처리 포함
    """
    @capture_and_log(tracer)
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
        """
        S3에서 prefix로 파일 목록을 조회

        Args:
            prefix (str): S3 prefix 경로

        Returns:
            List[S3FileEntry]: S3 파일 목록

        Raises:
            SystemConfigException: 환경변수 누락 등 시스템 오류
            NotFoundException: 파일 없음
        """
        # WHY: 환경변수 체크 및 S3 연결 오류를 명확히 예외처리
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("MINIO_ENDPOINT"),
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
        )
        from app.common.exceptions import SystemConfigException, NotFoundException
        bucket = os.getenv("MINIO_BUCKET")
        if not bucket:
            raise SystemConfigException("MINIO_BUCKET 환경변수가 설정되어 있지 않습니다.")
        paginator = s3.get_paginator("list_objects_v2")
        result = []
        # WHY: S3 pagination으로 모든 파일 목록 수집
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                key = obj.get("Key")
                size = obj.get("Size")
                last_modified = obj.get("LastModified")
                if key is None or size is None or last_modified is None:
                    continue  # skip malformed S3 objects
                result.append({
                    "key": key,
                    "size": size,
                    "last_modified": last_modified.isoformat() if hasattr(last_modified, 'isoformat') else str(last_modified)
                })
        if not result:
            raise NotFoundException("지정한 prefix에 파일이 없습니다.")
        return [S3FileEntry(**item) for item in result]
