"""
파일 서비스 API 라우터
"""
import logging
logging.basicConfig(level=logging.INFO, force=True)
from fastapi import APIRouter, Query, Path, Body, File, UploadFile, HTTPException
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

from app.services.file.api import raise_test

router = APIRouter()
router.include_router(raise_test.router)

@router.post(
    "/upload",
    summary="파일 및 메타데이터 업로드 (파일 + 메타데이터: JSON 파일 or 직접입력)",
    description="파일(file, 필수)과 메타데이터(metadata_file: JSON 파일 업로드, 또는 metadata_json: JSON 직접입력) 중 하나만 입력. metadata_file과 metadata_json 둘 다 입력/미입력 시 에러.",
)
async def upload(
    file: UploadFile = File(..., description="업로드할 파일 (예: 이미지, 문서 등)"),
    metadata_file: UploadFile = File(None, description="JSON 메타데이터 파일 업로드 (application/json)"),
    metadata_json: FileMetadataRequest = Body(None, description="직접 입력할 JSON 메타데이터 (application/json)")
):
    '''
    - 파일(file)은 필수
    - 메타데이터: metadata_file(.json 파일) 또는 metadata_json(직접 입력) 둘 중 하나만 입력
    - metadata_file과 metadata_json 둘 다 입력/미입력 시 400 에러
    '''
    if metadata_file and metadata_json:
        raise HTTPException(400, "metadata_file(파일) 또는 metadata_json(body) 중 하나만 입력하세요.")
    if not metadata_file and not metadata_json:
        raise HTTPException(400, "metadata_file(파일) 또는 metadata_json(body) 중 하나는 반드시 입력해야 합니다.")
    if metadata_file:
        contents = await metadata_file.read()
        import json
        try:
            data = json.loads(contents)
            metadata_obj = FileMetadataRequest(**data)
        except Exception:
            raise HTTPException(400, "metadata_file의 JSON 파싱 실패 또는 필드 누락")
    else:
        metadata_obj = metadata_json
    return {
        "uploaded_filename": file.filename,
        "metadata": metadata_obj.dict(),
    }

presigned_service = PresignedService()
zip_presigned_service = ZipPresignedService()
meta_query_service = MetaQueryService()
metadata_producer_service = MetadataProducerService()

from app.services.file.services.impl.list_query_service import ListQueryService
from app.services.file.schemas.listing import S3FileEntry
from fastapi import status

@router.get(
    "/imgplt/list/{prefix}",
    response_model=List[S3FileEntry],
    summary="S3 prefix 기반 파일 리스트 조회",
    description="S3 버킷 내 지정된 prefix 하위의 파일 목록을 조회합니다.",
    tags=["File"]
)
async def list_files_by_prefix(prefix: str = Path(..., description="S3 prefix 경로 (예: uploads/2025/)")):
    '''
    지정된 prefix 하위의 S3 파일 목록을 반환합니다. 파일이 없으면 404 반환.
    '''
    service = ListQueryService()
    files = await service.list_files(prefix)
    if not files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="지정한 prefix에 파일이 없습니다.")
    return files

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
    import logging
    logger = logging.getLogger("file-metadata-producer")
    logger.info(f"[FILE] /topics/{topic} called with metadata: {body.dict()}")
    result = await metadata_producer_service.produce_metadata(topic, body)
    logger.info(f"[FILE] Kafka produce result: {result}")
    return result
