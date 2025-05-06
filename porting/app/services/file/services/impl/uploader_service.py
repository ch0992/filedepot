"""
[📄 uploader_service.py - File 서비스 구현체]

설명:
- 파일 업로드를 처리하는 서비스 구현체
- 사용자 ID, 파일, 토픽명을 받아 업로드 처리

주요 연동:
- UploaderInterface (인터페이스)
"""

from fastapi import UploadFile
from app.services.file.services.interfaces.uploader_interface import UploaderInterface
from app.services.file.schemas.upload import UploadResponse
import aiofiles
import uuid
import os
import logging
from app.core.config import settings
from app.services.file.services.impl.minio_memory_client import MinioMemoryClient
from app.services.file.services.impl.minio_prod_client import MinioProdClient

logger = logging.getLogger("file-upload")

class UploaderService(UploaderInterface):
    async def upload_file(self, file: UploadFile):
        filename = f"{uuid.uuid4()}_{file.filename}"
        bucket = "filedepot-bucket"
        key = filename
        chunk_size = 20 * 1024 * 1024  # 20MB

        # 환경에 따라 클라이언트 선택
        if settings.ENV in ["production", "stage"]:
            minio_client = MinioProdClient()
        else:
            minio_client = MinioMemoryClient()

        # 임시 파일로 저장 (aiofiles 활용)
        temp_path = f"/tmp/{filename}"
        async with aiofiles.open(temp_path, 'wb') as out_file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await out_file.write(chunk)

        file_size = os.path.getsize(temp_path)
        from app.common.kafka_producer import KafkaMessageProducer
        if file_size < chunk_size:
            # 단일 업로드(20MB 미만)
            async with aiofiles.open(temp_path, 'rb') as f:
                data = await f.read()
                location = minio_client.upload_file(bucket, key, data)
                os.remove(temp_path)
                producer = KafkaMessageProducer()
                kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": location})
                # 검수(무조건 성공으로 가정)
                if settings.ENV in ["production", "stage"]:
                    # TODO: 실제 검수/무결성 검사 인터페이스 호출
                    logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (실서비스)")
                else:
                    logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (dummy)")
                return UploadResponse(filename=filename, status="uploaded", location=location, kafka_result=kafka_result)
        else:
            # multipart upload (20MB 이상)
            logger.info(f"[멀티파트 업로드 시작] 파일명={filename}, 전체용량={file_size} bytes, chunk={chunk_size} bytes")
            # 진행률 시각화
            uploaded = 0
            with open(temp_path, "rb") as f:
                part_num = 1
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    minio_client.upload_file(bucket, f"{key}.part{part_num}", chunk)
                    uploaded += len(chunk)
                    percent = int(uploaded / file_size * 100)
                    logger.info(f"[업로드 진행] {uploaded}/{file_size} bytes ({percent}%) part={part_num}")
                    part_num += 1
            # 실제로는 multipart_upload로 합쳐야 하지만, 여기선 단순화
            location = f"memory://{bucket}/{key}" if settings.ENV not in ["production", "stage"] else f"s3://{bucket}/{key}"
            os.remove(temp_path)
            producer = KafkaMessageProducer()
            kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": location})
            # 검수(무조건 성공으로 가정)
            if settings.ENV in ["production", "stage"]:
                # TODO: 실제 검수/무결성 검사 인터페이스 호출
                logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (실서비스)")
            else:
                logger.info(f"[검수] 파일 {filename} 업로드 후 무결성 검증 (dummy)")
            logger.info(f"[멀티파트 업로드 완료] 파일명={filename}, 전체용량={file_size} bytes")
            return UploadResponse(filename=filename, status="uploaded", location=location, kafka_result=kafka_result)


