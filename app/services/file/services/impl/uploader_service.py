from fastapi import UploadFile
from app.services.file.services.interfaces.uploader_interface import UploaderInterface
from app.services.file.schemas.upload import UploadResponse
import aiofiles
import uuid
import os
from app.common.minio_client import MinioClient

from app.common.minio_multipart import DummyMinioMultipartClient, multipart_upload

class UploaderService(UploaderInterface):
    async def upload_file(self, file: UploadFile):
        filename = f"{uuid.uuid4()}_{file.filename}"
        bucket = "filedepot-bucket"
        key = filename
        chunk_size = 20 * 1024 * 1024  # 20MB
        client = DummyMinioMultipartClient()

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
                client.upload_part(bucket, key, "single-upload", 1, data)
                location = f"https://dummy-s3/{bucket}/{key}"
                os.remove(temp_path)
                # 파일 업로드 후 메타데이터 Kafka 발행
                producer = KafkaMessageProducer()
                kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": location})
                return UploadResponse(filename=filename, status="uploaded", location=location, kafka_result=kafka_result)
        else:
            # multipart upload (20MB 이상)
            with open(temp_path, "rb") as f:
                result = await multipart_upload(f, bucket, key, client, chunk_size)
            os.remove(temp_path)
            if result.success:
                producer = KafkaMessageProducer()
                kafka_result = await producer.produce("file_metadata", {"filename": filename, "location": result.location})
                return UploadResponse(filename=filename, status="uploaded", location=result.location, kafka_result=kafka_result)
            else:
                return UploadResponse(filename=filename, status="failed", location="", error=result.error, kafka_result=None)

