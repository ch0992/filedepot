"""
파일 서비스 API 라우터
"""
from fastapi import APIRouter, Query, Path, Body
from app.services.file.schemas.aliases import AliasEntry
from typing import List

from app.services.file.services.impl.presigned_service import PresignedService
from app.services.file.schemas.presigned import PresignedURLResponse
from app.services.file.services.impl.zip_presigned_service import ZipPresignedService
from app.services.file.schemas.zips import ZipPresignedResponse
from app.services.file.services.impl.meta_query_service import MetaQueryService
from app.services.file.schemas.sqls import MetaInfoSchema
from app.services.file.services.impl.metadata_producer_service import MetadataProducerService
from app.services.file.schemas.metadata import FileMetadataRequest, KafkaProduceResult

router = APIRouter()

presigned_service = PresignedService()
zip_presigned_service = ZipPresignedService()
meta_query_service = MetaQueryService()
metadata_producer_service = MetadataProducerService()

@router.get("/ping", summary="Ping-pong API")
async def ping():
    return {"message": "pong"}

@router.get("/aliases", response_model=List[AliasEntry], summary="사용자별 적재 alias 목록 조회")
async def aliases(user_id: str = Query(...)):
    # 실제로는 DB 등에서 user_id별 alias 조회
    return [
        AliasEntry(alias="project-a", description="프로젝트 A 적재 경로"),
        AliasEntry(alias="project-b", description="프로젝트 B 적재 경로")
    ]

@router.get("/imgplt/s3/{file_path}", response_model=PresignedURLResponse, summary="Presigned S3 다운로드 링크 생성")
async def get_presigned_url(file_path: str = Path(...)):
    print("[FILE] /imgplt/s3/{file_path} called")
    return await presigned_service.create_presigned_url(file_path)

@router.get("/imgplt/zips", response_model=ZipPresignedResponse, summary="Presigned ZIP 다운로드 링크 생성")
async def get_zip_presigned_url(sql: str = Query(..., description="SQL 조건")):
    print("[FILE] /imgplt/zips called")
    return await zip_presigned_service.create_zip_presigned_url(sql)

@router.get("/imgplt/sqls", response_model=List[MetaInfoSchema], summary="SQL 기반 메타데이터 조회")
async def get_meta_sqls(query: str = Query(..., description="실행할 SQL 쿼리")):
    print("[FILE] /imgplt/sqls called")
    return await meta_query_service.query_metadata(query)

@router.post("/topics/{topic}", response_model=KafkaProduceResult, summary="Kafka 메타데이터 적재")
async def produce_metadata_to_kafka(
    topic: str = Path(..., description="Kafka topic명"),
    body: FileMetadataRequest = Body(...)
):
    print(f"[FILE] /topics/{{topic}} called")
    return await metadata_producer_service.produce_metadata(topic, body)
