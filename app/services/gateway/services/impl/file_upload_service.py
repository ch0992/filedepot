from fastapi import UploadFile
from app.services.gateway.services.interfaces.file_upload_interface import FileUploadInterface
from app.services.file.services.interfaces.uploader_interface import UploaderInterface
from app.common.kafka_producer import KafkaMessageProducer
import json

class FileUploadService(FileUploadInterface):
    async def upload_file_and_metadata(self, topic: str, file: UploadFile, metadata: str):
        # file 서비스가 파일 업로드 및 메타데이터 Kafka 발행을 모두 처리
        uploader: UploaderInterface = UploaderInterface.get_service()
        upload_response = await uploader.upload_file(file)
        # upload_response에는 kafka_result, location, error 등이 모두 포함됨
        return upload_response
