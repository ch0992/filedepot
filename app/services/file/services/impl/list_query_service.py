from app.services.file.services.interfaces.list_query_interface import ListQueryInterface
from app.services.file.schemas.listing import S3FileEntry
from app.core.logging import get_tracer, capture_and_log
import os
import boto3
from typing import List

tracer = get_tracer("file::list_files")

class ListQueryService(ListQueryInterface):
    @capture_and_log(tracer)
    async def list_files(self, prefix: str) -> List[S3FileEntry]:
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
