from fastapi import UploadFile
from app.services.gateway.services.interfaces.file_upload_interface import FileUploadInterface
from app.services.file.services.interfaces.uploader_interface import UploaderInterface
from app.common.kafka_producer import KafkaMessageProducer
from app.core.config import settings
import json
import logging
import os
import sys
from app.services.gateway.services.impl.file_metadata_service import FileMetadataService
from app.services.file.schemas.metadata import FileMetadataRequest

logging.basicConfig(level=logging.INFO, force=True)

logger = logging.getLogger("gateway-upload")

# boto3가 없으면 설치 안내
try:
    import boto3
except ImportError:
    boto3 = None

# tqdm 진행률 바
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

class FileUploadService(FileUploadInterface):
    async def upload_file_and_metadata_file(self, topic: str, file: UploadFile, metadata_file: UploadFile):
        logger.info(f"[Gateway] 파일 업로드 요청 시작: filename={file.filename}, content_type={file.content_type}")
        sys.stdout.flush()
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        logger.info(f"[Gateway] 파일 크기: {size} bytes")
        sys.stdout.flush()
        chunk_size = 20 * 1024 * 1024  # 20MB

        # metadata 파싱은 맨 앞에서 단 한 번만!
        try:
            logger.info(f"[Gateway] 메타데이터 파싱 시도: {metadata_file.filename}")
            metadata = await self._parse_metadata_file(metadata_file)
        except Exception as e:
            logger.error(f"[Gateway] 메타데이터 파싱 실패: {e}, 입력값: {metadata_file.filename}")
            raise ValueError(f"메타데이터 파싱 실패: {e}, 입력값: {metadata_file.filename}")
        
        return await self._upload_file_and_produce_metadata(topic, file, metadata)

    async def upload_file_and_metadata_json(self, topic: str, file: UploadFile, metadata: str):
        logger.info(f"[Gateway] 파일 업로드 요청 시작: filename={file.filename}, content_type={file.content_type}")
        sys.stdout.flush()
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        logger.info(f"[Gateway] 파일 크기: {size} bytes")
        sys.stdout.flush()
        chunk_size = 20 * 1024 * 1024  # 20MB

        # metadata 파싱은 맨 앞에서 단 한 번만!
        try:
            logger.info(f"[Gateway] 메타데이터 파싱 시도: {metadata}")
            metadata = await self._parse_metadata_json(metadata)
        except Exception as e:
            logger.error(f"[Gateway] 메타데이터 파싱 실패: {e}, 입력값: {metadata}")
            raise ValueError(f"메타데이터 파싱 실패: {e}, 입력값: {metadata}")
        
        return await self._upload_file_and_produce_metadata(topic, file, metadata)

    async def upload_file_and_metadata(self, topic: str, file: UploadFile, metadata: str):
        """
        DEPRECATED: Use upload_file_and_metadata_file or upload_file_and_metadata_json instead.
        """
        logger.warning("DEPRECATED: upload_file_and_metadata is deprecated. Use upload_file_and_metadata_file or upload_file_and_metadata_json instead.")
        return await self.upload_file_and_metadata_json(topic, file, metadata)

    async def _parse_metadata_file(self, metadata_file: UploadFile):
        try:
            metadata = await metadata_file.read()
            metadata = json.loads(metadata)
            return FileMetadataRequest(**metadata)
        except Exception as e:
            raise e

    async def _parse_metadata_json(self, metadata: str):
        try:
            if not metadata or (isinstance(metadata, str) and metadata.strip() == ""):
                raise ValueError("metadata 값이 비어있거나 None입니다.")
            if isinstance(metadata, dict):
                return FileMetadataRequest(**metadata)
            else:
                return FileMetadataRequest(**json.loads(metadata))
        except Exception as e:
            raise e

    async def _upload_file_and_produce_metadata(self, topic: str, file: UploadFile, metadata: FileMetadataRequest):
        if settings.ENV in ["stage", "production"]:
            # gateway에서 직접 MinIO로 multipart 업로드
            if not boto3:
                logger.error("boto3 라이브러리가 없습니다. 'pip install boto3'로 설치하세요.")
                raise ImportError("boto3 라이브러리가 없습니다. 'pip install boto3'로 설치하세요.")
            if not tqdm:
                logger.warning("tqdm 라이브러리가 없습니다. 'pip install tqdm'로 설치 시 진행률 바를 볼 수 있습니다.")
            minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
            minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
            minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
            minio_bucket = os.getenv("MINIO_BUCKET", "filedepot-bucket")
            s3 = boto3.client(
                's3',
                endpoint_url=minio_endpoint,
                aws_access_key_id=minio_access_key,
                aws_secret_access_key=minio_secret_key,
                region_name='ap-northeast-2',
            )
            filename = file.filename
            extra_args = {"ContentType": file.content_type}
            mpu = s3.create_multipart_upload(Bucket=minio_bucket, Key=filename, **extra_args)
            upload_id = mpu["UploadId"]
            parts = []
            part_num = 1
            uploaded = 0
            file.file.seek(0)
            try:
                if tqdm:
                    with tqdm(total=file.file.tell(), unit='B', unit_scale=True, desc="[Gateway] Minio Upload") as pbar:
                        while uploaded < file.file.tell():
                            chunk = file.file.read(20 * 1024 * 1024)
                            if not chunk:
                                break
                            resp = s3.upload_part(
                                Bucket=minio_bucket,
                                Key=filename,
                                PartNumber=part_num,
                                UploadId=upload_id,
                                Body=chunk
                            )
                            etag = resp["ETag"]
                            parts.append({"ETag": etag, "PartNumber": part_num})
                            uploaded += len(chunk)
                            pbar.update(len(chunk))
                            logger.info(f"[Gateway] [Minio 멀티파트 업로드 진행] {uploaded}/{file.file.tell()} bytes ({int(uploaded/file.file.tell()*100)}%) part={part_num}")
                            part_num += 1
                else:
                    while uploaded < file.file.tell():
                        chunk = file.file.read(20 * 1024 * 1024)
                        if not chunk:
                            break
                        resp = s3.upload_part(
                            Bucket=minio_bucket,
                            Key=filename,
                            PartNumber=part_num,
                            UploadId=upload_id,
                            Body=chunk
                        )
                        etag = resp["ETag"]
                        parts.append({"ETag": etag, "PartNumber": part_num})
                        uploaded += len(chunk)
                        logger.info(f"[Gateway] [Minio 멀티파트 업로드 진행] {uploaded}/{file.file.tell()} bytes ({int(uploaded/file.file.tell()*100)}%) part={part_num}")
                        part_num += 1
                result = s3.complete_multipart_upload(
                    Bucket=minio_bucket,
                    Key=filename,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts}
                )
                logger.info(f"[Gateway] [Minio 멀티파트 업로드 완료] 파일명={filename}, 전체용량={file.file.tell()} bytes, 총 파트={part_num-1}, location={result.get('Location','')} ")
                sys.stdout.flush()
                # 메타데이터 Kafka 발행
                kafka_result = await FileMetadataService().produce_metadata(topic, metadata)
                return {"filename": filename, "status": "uploaded", "location": result.get("Location", ""), "kafka_result": kafka_result.dict()}
            except Exception as e:
                s3.abort_multipart_upload(Bucket=minio_bucket, Key=filename, UploadId=upload_id)
                logger.error(f"[Gateway] [Minio 멀티파트 업로드 실패] {e}")
                raise
        else:
            # 개발/테스트: 기존 file 서비스 HTTP API로 전송
            uploader: UploaderInterface = UploaderInterface.get_service()
            if file.file.tell() < 20 * 1024 * 1024:
                upload_response = await uploader.upload_file(file)
                logger.info(f"[Gateway] 파일 업로드 응답: {json.dumps(upload_response.dict(), ensure_ascii=False)}")
                sys.stdout.flush()
                kafka_result = await FileMetadataService().produce_metadata(topic, metadata)
                if hasattr(upload_response, 'dict'):
                    resp = upload_response.dict()
                else:
                    resp = dict(upload_response)
                resp["kafka_result"] = kafka_result.dict()
                return resp
            else:
                uploaded = 0
                part_num = 1
                file.file.seek(0)
                while uploaded < file.file.tell():
                    chunk = file.file.read(20 * 1024 * 1024)
                    if not chunk:
                        break
                    logger.info(f"[Gateway] [멀티파트 업로드 진행] {uploaded + len(chunk)}/{file.file.tell()} bytes ({int((uploaded + len(chunk))/file.file.tell()*100)}%) part={part_num}")
                    sys.stdout.flush()
                    uploaded += len(chunk)
                    part_num += 1
                logger.info(f"[Gateway] [멀티파트 업로드 완료] 파일명={file.filename}, 전체용량={file.file.tell()} bytes, 총 파트={part_num-1}")
                sys.stdout.flush()
                upload_response = await uploader.upload_file(file)
                logger.info(f"[Gateway] 파일 업로드 최종 응답: {json.dumps(upload_response.dict(), ensure_ascii=False)}")
                sys.stdout.flush()
                kafka_result = await FileMetadataService().produce_metadata(topic, metadata)
                if hasattr(upload_response, 'dict'):
                    resp = upload_response.dict()
                else:
                    resp = dict(upload_response)
                resp["kafka_result"] = kafka_result.dict()
                return resp
